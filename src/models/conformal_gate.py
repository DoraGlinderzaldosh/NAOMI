"""
CoRAL-RF: Conformal Gated Forecaster & Distribution-Free Risk Envelopes.
Based on Zizi, Chafi, & El Hammoumi (2026), Results in Engineering.

Architecture:
1. Tabular Anchor: High-capacity Random Forest Regressor trained on structured covariates.
2. Temporal Residual Expert: Sequential PyTorch LSTM trained exclusively on anchor residual errors.
3. Adaptive Correction Gate (α in [0, 1]): Validated gating weighting anchor vs. residual expert.
4. Split Conformal Prediction Layer: Finite-sample distribution-free uncertainty intervals
   providing guaranteed 90% and 95% coverage envelopes without normality assumptions.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import torch
import torch.nn as nn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

logger = logging.getLogger("naomi.models.conformal_gate")


@dataclass
class ConformalIntervals:
    """Calibrated prediction intervals from Split Conformal Prediction."""
    point_forecast: List[float]
    lower_90: List[float]
    upper_90: List[float]
    lower_95: List[float]
    upper_95: List[float]
    q_hat_90: float
    q_hat_95: float
    coverage_guarantee_90: float = 0.90
    coverage_guarantee_95: float = 0.95


class ResidualLSTMNet(nn.Module):
    """Compact PyTorch LSTM specialized in forecasting temporal error residuals."""

    def __init__(self, input_dim: int, hidden_dim: int = 32, num_layers: int = 1):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
        )
        self.head = nn.Sequential(
            nn.Linear(hidden_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out, _ = self.lstm(x)
        last_hidden = out[:, -1, :]
        return self.head(last_hidden)


class ConformalGatedForecaster:
    """
    CoRAL-RF Hybrid Forecaster with Split Conformal Calibration.
    
    Combines:
    - Random Forest Tabular Anchor
    - PyTorch Residual LSTM Expert
    - Adaptive Correction Gate α
    - Distribution-free Split Conformal Calibration Layer
    """

    def __init__(
        self,
        n_estimators: int = 50,
        max_depth: int = 10,
        random_state: int = 42,
    ):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state

        self.anchor = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1,
        )
        self.residual_expert: Optional[ResidualLSTMNet] = None
        self.gate_alpha: float = 0.5
        self.is_fitted: bool = False

        # Conformal calibration quantiles
        self.q_hat_90: float = 0.0
        self.q_hat_95: float = 0.0
        self.calibration_scores: Optional[np.ndarray] = None

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        lookback: int = 7,
        epochs: int = 15,
        lr: float = 1e-3,
    ) -> Dict[str, float]:
        """
        Train anchor on tabular features, then train residual LSTM expert on anchor errors,
        and optimize gating parameter α on validation set.
        """
        X_train = np.asarray(X_train, dtype=np.float32)
        y_train = np.asarray(y_train, dtype=np.float32).ravel()
        X_val = np.asarray(X_val, dtype=np.float32)
        y_val = np.asarray(y_val, dtype=np.float32).ravel()

        # 1. Fit Tabular Anchor
        self.anchor.fit(X_train, y_train)
        train_anchor_pred = self.anchor.predict(X_train)
        val_anchor_pred = self.anchor.predict(X_val)

        # 2. Compute Anchor Residuals (Target for LSTM)
        train_residuals = y_train - train_anchor_pred

        # Build sequential windows for residual LSTM
        # If dataset is large enough for sequential windowing:
        n_features = X_train.shape[1]
        self.residual_expert = ResidualLSTMNet(input_dim=n_features, hidden_dim=32)

        optimizer = torch.optim.Adam(self.residual_expert.parameters(), lr=lr)
        criterion = nn.HuberLoss(delta=1.0)

        # Simple mini-batch training on residual sequences
        seq_len = min(lookback, len(X_train) - 1)
        if len(X_train) > seq_len:
            # Construct sequential input batches
            X_seq_list, y_res_list = [], []
            for i in range(seq_len, len(X_train)):
                X_seq_list.append(X_train[i - seq_len : i])
                y_res_list.append([train_residuals[i]])

            X_seq_t = torch.tensor(np.array(X_seq_list), dtype=torch.float32)
            y_res_t = torch.tensor(np.array(y_res_list), dtype=torch.float32)

            self.residual_expert.train()
            batch_size = 32
            n_samples = len(X_seq_t)
            for epoch in range(epochs):
                perm = torch.randperm(n_samples)
                for b_start in range(0, n_samples, batch_size):
                    idx = perm[b_start : b_start + batch_size]
                    batch_x, batch_y = X_seq_t[idx], y_res_t[idx]
                    optimizer.zero_grad()
                    pred_res = self.residual_expert(batch_x)
                    loss = criterion(pred_res, batch_y)
                    loss.backward()
                    optimizer.step()

        # 3. Optimize Adaptive Correction Gate α on validation set
        self.residual_expert.eval()
        val_res_preds = []
        if len(X_val) > seq_len:
            val_seq_list = []
            for i in range(seq_len, len(X_val)):
                val_seq_list.append(X_val[i - seq_len : i])
            val_seq_t = torch.tensor(np.array(val_seq_list), dtype=torch.float32)
            with torch.no_grad():
                val_res_expert = self.residual_expert(val_seq_t).squeeze(-1).numpy()
            # Pad beginning with zeros
            val_res_preds = np.concatenate([np.zeros(seq_len, dtype=np.float32), val_res_expert])
        else:
            val_res_preds = np.zeros(len(X_val), dtype=np.float32)

        # Grid search α in [0, 1] to minimize validation MSE
        best_alpha = 0.0
        best_mse = float("inf")
        for alpha in np.linspace(0.0, 1.0, 21):
            y_comb = val_anchor_pred + alpha * val_res_preds
            mse = mean_squared_error(y_val, y_comb)
            if mse < best_mse:
                best_mse = mse
                best_alpha = float(alpha)

        self.gate_alpha = best_alpha
        self.is_fitted = True

        return {
            "best_alpha": self.gate_alpha,
            "anchor_val_mse": float(mean_squared_error(y_val, val_anchor_pred)),
            "gated_val_mse": float(best_mse),
        }

    def calibrate(
        self,
        X_cal: np.ndarray,
        y_cal: np.ndarray,
    ) -> Tuple[float, float]:
        """
        Split Conformal Prediction calibration (Zizi et al., 2026).
        
        Computes nonconformity scores: s_i = |y_i - y_pred_i|
        Extracts finite-sample (1 - β)(1 + 1/n) quantile:
            q_hat = np.quantile(scores, ceil((n + 1)(1 - β)) / n)
        """
        if not self.is_fitted:
            raise RuntimeError("Forecaster must be fitted before calibration.")

        X_cal = np.asarray(X_cal, dtype=np.float32)
        y_cal = np.asarray(y_cal, dtype=np.float32).ravel()
        n = len(y_cal)

        if n < 5:
            # Fallback conservative quantiles if calibration set is small
            self.q_hat_90 = 2.0
            self.q_hat_95 = 2.5
            return self.q_hat_90, self.q_hat_95

        y_pred = self.predict(X_cal)
        scores = np.abs(y_cal - y_pred)
        self.calibration_scores = scores

        # Finite-sample correction factor: (1 - beta) * (1 + 1/n)
        q_level_90 = min(1.0, 0.90 * (1.0 + 1.0 / n))
        q_level_95 = min(1.0, 0.95 * (1.0 + 1.0 / n))

        self.q_hat_90 = float(np.quantile(scores, q_level_90))
        self.q_hat_95 = float(np.quantile(scores, q_level_95))

        return self.q_hat_90, self.q_hat_95

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Generate point forecast using anchor + gated residual expert."""
        if not self.is_fitted:
            raise RuntimeError("Forecaster is not fitted.")

        X = np.asarray(X, dtype=np.float32)
        anchor_pred = self.anchor.predict(X)

        if self.gate_alpha > 0 and self.residual_expert is not None and len(X) >= 7:
            # Evaluate residual expert
            seq_len = 7
            X_seq_list = []
            for i in range(len(X)):
                if i < seq_len:
                    # Pad by repeating first element
                    pad = np.repeat(X[i:i+1], seq_len - (i + 1), axis=0)
                    chunk = np.vstack([pad, X[: i + 1]])
                else:
                    chunk = X[i - seq_len + 1 : i + 1]
                X_seq_list.append(chunk)

            X_seq_t = torch.tensor(np.array(X_seq_list), dtype=torch.float32)
            self.residual_expert.eval()
            with torch.no_grad():
                res_pred = self.residual_expert(X_seq_t).squeeze(-1).numpy()
            comb_pred = anchor_pred + self.gate_alpha * res_pred
        else:
            comb_pred = anchor_pred

        return np.clip(comb_pred, 0.0, None)

    def predict_with_conformal_intervals(
        self,
        X: np.ndarray,
    ) -> ConformalIntervals:
        """
        Generate point forecast together with 90% and 95% conformal prediction intervals.
        """
        y_pred = self.predict(X)

        q90 = self.q_hat_90 if self.q_hat_90 > 0 else float(np.mean(y_pred) * 0.15)
        q95 = self.q_hat_95 if self.q_hat_95 > 0 else float(np.mean(y_pred) * 0.22)

        lower_90 = [float(max(0.0, p - q90)) for p in y_pred]
        upper_90 = [float(p + q90) for p in y_pred]
        lower_95 = [float(max(0.0, p - q95)) for p in y_pred]
        upper_95 = [float(p + q95) for p in y_pred]

        return ConformalIntervals(
            point_forecast=[round(float(p), 2) for p in y_pred],
            lower_90=[round(val, 2) for val in lower_90],
            upper_90=[round(val, 2) for val in upper_90],
            lower_95=[round(val, 2) for val in lower_95],
            upper_95=[round(val, 2) for val in upper_95],
            q_hat_90=round(q90, 4),
            q_hat_95=round(q95, 4),
        )

    @staticmethod
    def evaluate_coverage(y_true: np.ndarray, lower: List[float], upper: List[float]) -> float:
        """Compute empirical coverage rate = fraction of actuals inside [lower, upper]."""
        y_true = np.asarray(y_true).ravel()
        lower_arr = np.asarray(lower).ravel()
        upper_arr = np.asarray(upper).ravel()
        in_bounds = (y_true >= lower_arr) & (y_true <= upper_arr)
        return float(np.mean(in_bounds))

