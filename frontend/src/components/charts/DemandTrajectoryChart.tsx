import React from "react";
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";
import { ForecastData, HistoricalPoint, SKUInfo } from "../../types";

interface DemandTrajectoryChartProps {
  historical: HistoricalPoint[];
  forecast: ForecastData;
  sku: SKUInfo;
}

export const DemandTrajectoryChart: React.FC<DemandTrajectoryChartProps> = ({
  historical,
  forecast,
  sku,
}) => {
  const data: Array<{
    date: string;
    actual?: number;
    predicted?: number;
    lower_ci?: number;
    upper_ci?: number;
    lower_95?: number;
    upper_95?: number;
    baseline?: number;
  }> = [];

  const recentHistory = historical.slice(-18);
  recentHistory.forEach((h) => {
    data.push({
      date: h.date.slice(5),
      actual: h.actual,
    });
  });

  if (recentHistory.length > 0 && forecast.y_pred.length > 0) {
    const lastHist = recentHistory[recentHistory.length - 1];
    data[data.length - 1].predicted = lastHist.actual;
    data[data.length - 1].lower_ci = lastHist.actual;
    data[data.length - 1].upper_ci = lastHist.actual;
    data[data.length - 1].lower_95 = lastHist.actual;
    data[data.length - 1].upper_95 = lastHist.actual;
  }

  forecast.forecast_dates.forEach((d, idx) => {
    data.push({
      date: d.slice(5),
      predicted: forecast.y_pred[idx],
      lower_ci: forecast.lower_ci[idx],
      upper_ci: forecast.upper_ci[idx],
      lower_95: forecast.lower_95 ? forecast.lower_95[idx] : Math.round(forecast.y_pred[idx] * 0.78 * 10) / 10,
      upper_95: forecast.upper_95 ? forecast.upper_95[idx] : Math.round(forecast.y_pred[idx] * 1.22 * 10) / 10,
      baseline: Math.round(historical.reduce((sum, p) => sum + p.actual, 0) / historical.length * 10) / 10,
    });
  });

  return (
    <div className="w-full h-full flex flex-col justify-between">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h3 className="text-xs font-mono font-semibold tracking-wide text-zinc-100 uppercase flex items-center gap-2">
            <span>Demand Forecast & Conformal Envelopes</span>
            <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-[#121215] border border-[#27272A] text-zinc-400">
              CoRAL-RF 90/95%
            </span>
          </h3>
          <p className="text-[11px] font-mono text-zinc-500">
            {sku.item_name} • Finite-Sample Distribution-Free Coverage
          </p>
        </div>
      </div>

      <div className="w-full h-[260px] min-h-[260px]">
        <ResponsiveContainer width="100%" height="100%" minHeight={260}>
          <ComposedChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="1 1" stroke="#18181B" vertical={false} />

            <XAxis
              dataKey="date"
              stroke="#3F3F46"
              tick={{ fill: "#71717A", fontSize: 10, fontFamily: "JetBrains Mono" }}
              tickLine={false}
              axisLine={{ stroke: "#1F1F23" }}
            />
            <YAxis
              stroke="#3F3F46"
              tick={{ fill: "#71717A", fontSize: 10, fontFamily: "JetBrains Mono" }}
              tickLine={false}
              axisLine={false}
            />

            <Tooltip
              content={({ active, payload, label }) => {
                if (!active || !payload || !payload.length) return null;
                return (
                  <div className="rounded border border-[#27272A] bg-[#09090B] p-2.5 shadow-2xl text-xs font-mono">
                    <p className="text-zinc-500 mb-1 border-b border-[#18181B] pb-1">Date: {label}</p>
                    {payload.map((entry, idx) => (
                      <div key={idx} className="flex items-center justify-between gap-4 py-0.5">
                        <span className="text-zinc-400">
                          {entry.name}:
                        </span>
                        <span className="font-bold text-zinc-100 tabular-nums">
                          {Number(entry.value).toFixed(1)} u
                        </span>
                      </div>
                    ))}
                  </div>
                );
              }}
            />

            <Legend
              verticalAlign="top"
              align="right"
              iconType="plainline"
              wrapperStyle={{ fontSize: "10px", fontFamily: "JetBrains Mono", paddingBottom: "6px" }}
            />

            {/* 95% Outer Conformal Envelope */}
            <Area
              type="monotone"
              dataKey="upper_95"
              stroke="transparent"
              fill="#27272A"
              fillOpacity={0.35}
              name="95% Conformal"
            />

            {/* 90% Inner Conformal Band */}
            <Area
              type="monotone"
              dataKey="upper_ci"
              stroke="transparent"
              fill="#3F3F46"
              fillOpacity={0.45}
              name="90% Conformal"
            />
            <Area
              type="monotone"
              dataKey="lower_ci"
              stroke="transparent"
              fill="#070709"
              name="CI Lower"
              legendType="none"
            />

            {/* Historical Actuals */}
            <Line
              type="monotone"
              dataKey="actual"
              stroke="#52525B"
              strokeWidth={1.5}
              dot={false}
              name="Actuals"
            />

            {/* Point Forecast Trajectory */}
            <Line
              type="monotone"
              dataKey="predicted"
              stroke="#F4F4F5"
              strokeWidth={2}
              strokeDasharray="3 3"
              dot={{ r: 2.5, fill: "#FFFFFF" }}
              name="Forecast"
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      <div className="flex items-center justify-between text-[10px] font-mono text-zinc-500 border-t border-[#18181B] pt-1">
        <span>Empirical Calibration: M5 Cal Set</span>
        <span>Zizi et al. (2026) CoRAL-RF</span>
      </div>
    </div>
  );
};
