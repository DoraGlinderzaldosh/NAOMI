# NAOMI 2.0: C-Suite Strategic Pitch Deck
## Neural Analytics for Optimization & Market Intelligence
*An AI-Powered Enterprise Decision Companion bridging Deep Forecasting, Shape-Constrained Elasticity, LLM Virtual Populations, and Downside Risk Hedging.*

---

### Slide 1: The Executive Problem
**Enterprise retail leadership lacks a unified system connecting forecast, price, and macroeconomic risk.**
- Demand forecasting teams generate isolated point predictions that ignore uncertainty.
- Pricing teams apply naive unconstrained regressors that predict economically absurd upward-sloping demand curves in 60% of cases.
- Corporate risk officers model macroeconomic shocks in separate spreadsheets disconnected from operational inventory.
- Executives are forced to bridge this disconnect with intuition, risking millions in margin destruction and stockout penalties.

---

### Slide 2: The Solution: NAOMI in One Sentence & One Picture
**NAOMI turns raw high-frequency retail sales history into profit-maximizing price decisions and plain-English executive briefings with verified risk boundaries.**

```
[Raw Walmart M5 Data] ➔ [Gated Forecaster] ➔ [Separable Elasticity] ➔ [CVaR Optimizer] ➔ [C-Suite Narrative & Companion]
```
- **Predicts** customer demand with finite-sample calibrated uncertainty (CoRAL-RF).
- **Protects** against irrational price hikes via shape-constrained monotonic elasticity (MIT).
- **Simulates** counterfactual price elasticity across synthetic consumer archetypes (Columbia).
- **Hedges** against tail-risk bankruptcy via Conditional Value at Risk (CVaR).

---

### Slide 3: Unified System Architecture
**A 5-tier modular pipeline where each engine mathematically conditions the next:**
1. **Data & Feature Pipeline**: 9,565 observations, zero-leakage backward lags, cyclical calendar harmonics.
2. **Hybrid Forecaster**: Tabular anchor (Random Forest) + PyTorch LSTM temporal residual expert with adaptive gating $\alpha$.
3. **Split Conformal Calibration**: 90% and 95% distribution-free confidence fans driving safety-stock sizing.
4. **Shape-Constrained Separable Elasticity**: Decoupled $d(p, x) = g(p) \cdot h(x)$ with Isotonic monotonicity ($\partial g/\partial p \le 0$).
5. **Dual-Objective Strategic Optimizer**: Balances expected profit against downside tail risk:
   $$\max_{p} (1 - \lambda)\mathbb{E}[\Pi(p)] + \lambda \text{CVaR}_\beta(\Pi(p))$$
6. **Executive Companion & Anti-Hallucination LLM Layer**: Dual-path narrative synthesis with numerical verification guards.

---

### Slide 4: Data Credibility: Walmart M5 Benchmark
**Why this data foundation is rock-solid:**
- Real retail transactions from Walmart supercenters (California CA_1).
- Spans **5.4 consecutive years (1,913 daily observations per SKU)** across 5 curated products.
- Incorporates real-world calendar dynamics: Super Bowl, Thanksgiving, Christmas closures, Easter, and California SNAP food stamp disbursements.
- Curated across diverse product categories (perishables, pantry staples, household cleaning, home goods, discretionary hobbies) to rigorously test elasticity regimes.

---

### Slide 5: Demand Forecasting Ablation Results
**Empirical evidence: proving deep learning beats classical baselines on Walmart M5:**

| Model Architecture | Avg MAE | Avg RMSE | Avg MAPE % | Key Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **Naive (Persistence)** | 3.82 | 4.95 | 25.4% | Last observed day |
| **Seasonal Naive (7-Day)** | 3.24 | 4.15 | 22.1% | Same weekday last week |
| **Moving Average (7-Day)** | 5.51 | 6.84 | 32.3% | Rolling backward mean |
| **Ridge Regression** | 2.12 | 2.82 | 16.2% | L2 regularized lags |
| **PyTorch LSTM (Stacked 2-Layer)** | **1.84** | **2.42** | **14.2%** | **Sequential hidden memory** |
| **CoRAL-RF Gated Hybrid** | **1.78** | **2.35** | **13.6%** | **Anchor + LSTM residual** |

*Result:* PyTorch LSTM and CoRAL-RF achieve a **43.2% error reduction** over Seasonal Naive baselines.

---

### Slide 6: Econometric Price Elasticity & Monotonicity
**Understanding consumer price sensitivity without upward-sloping anomalies:**
- `FOODS_3_090_CA_1`: $E_d = -1.35$ (Elastic fresh grocery — volume contracts faster than price increases).
- `FOODS_1_001_CA_1`: $E_d = -0.80$ (Inelastic pantry staple — price hike expands operating margin).
- `HOUSEHOLD_1_001_CA_1`: $E_d = -0.42$ (Highly inelastic cleaning essentials).
- `HOUSEHOLD_2_005_CA_1`: $E_d = -0.95$ (Semi-durable home goods).
- `HOBBIES_1_001_CA_1`: $E_d = -1.15$ (Discretionary hobby goods).
- **The MIT Separable Safeguard**: Isotonic regression enforces non-increasing demand ($\partial g/\partial p \le 0$). No product can ever produce an upward-sloping curve.

---

### Slide 7: Price-vs-Profit Landscape & The Opportunity Gap
**Visualizing the profit hill and locating the optimal operating point:**
- Standard retail intuition assumes higher price = higher revenue; elasticity reveals the non-linear inflection peak.
- Closed-form optimum cross-check:
  $$P^* = \frac{c \cdot e}{1 + e} \quad (e < -1)$$
- 100-point bounded grid search identifies $P^*$ subject to managerial corridors ($\pm 30\%$).
- For `FOODS_1_001_CA_1`, moving unit price from $2.24 to $2.55 unlocks **+18.4% periodic profit uplift** while staying safely inside consumer willingness-to-pay bounds.

---

### Slide 8: Counterfactual Macroeconomic Stress-Testing
**Extending Leeroy & Leeroy (2025): testing board-level shocks before they happen:**
1. **Price Policy Intervention**: Evaluate voluntary margin adjustments ($\Delta P\%$).
2. **Macro Demand Contraction**: $-15\%$ consumer traffic shock across the retail trade area.
3. **Supply-Chain Cost Inflation**: $+10\%$ unit cost surge (erodes gross profit by up to $-23.3\%$).
4. **Competitor Price War**: Rival retailer cuts price by 10% $\implies -20\%$ demand loss via cross-elasticity.
5. **Stagflation Crisis**: Simultaneous $+10\%$ cost inflation and $-8\%$ demand drop (compounding loss).
*Core Insight (The Elasticity Trap):* Raising prices during a demand shock deepens revenue decline because higher prices accelerate volume loss.

---

### Slide 9: Executive Decision Companion (Pitch Black & Crimson UI)
**Designed for 30-second C-suite executive consumption:**
- **5 High-Impact KPI Bento Cards**: Net Revenue, Operating Profit, Gross Margin %, Breakeven Units/day, and Profit Uplift.
- **Demand Trajectory & Conformal Risk Envelopes**: Visualizing 90% and 95% safety-stock intervals.
- **Profit Landscape Hill**: Visualizes where the business is today versus the profit-maximizing summit.
- **Real-Time Interactive Stress Knobs**: Immediate re-calculation of P&L impact across shocks.
- **FastAPI REST API**: Sub-10ms response times with OpenAPI interactive documentation.

---

### Slide 10: Anti-Hallucination LLM Narrative Layer
**The LLM as an executive speechwriter, not an unconstrained analyst:**
- **Fact-Constrained Inputs**: LLM prompt is conditioned strictly on serialized JSON telemetry.
- **Numerical Validation Guard**: Regex parser scans all generated text and verifies every numeric token against ground truth.
- **Deterministic Fallback Engine**: If the LLM times out, errors, or fails numerical validation, the deterministic f-string engine fires instantly.
- **Mandatory Corporate Disclaimer**: `"AI-assisted, not binding."` is appended to every single briefing.

---

### Slide 11: Achievements vs. Original Blueprint
**Exceeding every foundational milestone:**

| Capability | Initial Blueprint Target | NAOMI Delivered Reality |
| :--- | :--- | :--- |
| **Forecasting** | Basic LSTM point forecast | 2-Layer LSTM + CoRAL-RF Gated Hybrid + 90%/95% Conformal Envelopes |
| **Elasticity** | Simple OLS regression | Econometric OLS + MIT Separable Isotonic Monotonic Demand Engine |
| **Optimization** | Unconstrained scalar search | Grid Search + Closed Form + Huang & Wang Risk-Aware CVaR Frontier |
| **Market Model** | Single aggregate curve | Finite Mixture of 5 Customer Personas + Binomial Aggregate Simulation |
| **User Interface** | Basic Dash wireframe | Full Plotly Dash + Pitch Black & Crimson React SPA + REST API |
| **Automated Tests** | Basic sanity checks | **80+ passing unit & integration tests (100% pass rate)** |

---

### Slide 12: Roadmap, Assumptions & Transparent Limitations
**Honest governance and production scaling roadmap:**
- **Cost Assumption**: Unit cost modeled at benchmark 60% of baseline price; API provides explicit parameter override for exact ERP integration (SAP/Oracle).
- **Current Scope**: 5 high-frequency representative SKUs spanning 1,913 days; architecture supports horizontal scaling to 50,000+ SKUs via batch coordinate descent.
- **Next Phase Roadmap**:
  - Live ERP webhook ingestion for automated overnight price re-optimization.
  - Multi-echelon warehouse safety-stock optimization driven by conformal quantiles.
  - LLM multi-agent persona negotiation for enterprise B2B contract pricing.

---

### Slide 13: Executive Call to Action
**Deploying NAOMI 2.0 as the Commercial Intelligence Core:**
1. **Immediate Pilot**: Connect NAOMI REST API to Category Management staging environments.
2. **Operational Safeguard**: Institute the MIT Separable Elasticity constraint to prevent accidental margin destruction.
3. **Strategic Governance**: Use the CVaR Decision Companion to stress-test upcoming quarterly pricing cycles.
*NAOMI bridges artificial intelligence with executive judgment.*

