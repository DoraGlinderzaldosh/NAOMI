import React from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from "recharts";
import { SimulationResult } from "../../types";

interface ScenarioComparisonChartProps {
  simulation: SimulationResult;
}

export const ScenarioComparisonChart: React.FC<ScenarioComparisonChartProps> = ({
  simulation,
}) => {
  const data = [
    {
      metric: "Demand (u)",
      Baseline: simulation.baseline_kpis.demand,
      Simulated: simulation.shocked_kpis.demand,
    },
    {
      metric: "Revenue ($)",
      Baseline: simulation.baseline_kpis.revenue,
      Simulated: simulation.shocked_kpis.revenue,
    },
    {
      metric: "Net Profit ($)",
      Baseline: simulation.baseline_kpis.gross_profit,
      Simulated: simulation.shocked_kpis.gross_profit,
    },
  ];

  return (
    <div className="w-full h-full flex flex-col justify-between">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h3 className="text-xs font-mono font-semibold tracking-wide text-zinc-100 uppercase">
            Scenario Variance vs. Baseline
          </h3>
          <p className="text-[11px] font-mono text-zinc-500">
            Counterfactual Impact on Operating Metrics
          </p>
        </div>
        <span className="text-[10px] font-mono px-1.5 py-0.2 rounded border border-[#27272A] bg-[#121215] text-zinc-400">
          Delta Audit
        </span>
      </div>

      <div className="w-full h-[250px] min-h-[250px]">
        <ResponsiveContainer width="100%" height="100%" minHeight={250}>
          <BarChart data={data} margin={{ top: 10, right: 10, left: -15, bottom: 0 }}>
            <CartesianGrid strokeDasharray="1 1" stroke="#18181B" vertical={false} />

            <XAxis
              dataKey="metric"
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
                    <p className="text-zinc-400 font-bold mb-1 border-b border-[#18181B] pb-1">{label}</p>
                    {payload.map((entry, idx) => (
                      <div key={idx} className="flex items-center justify-between gap-4 py-0.5">
                        <span className="text-zinc-500">{entry.name}:</span>
                        <span className="font-bold text-zinc-100 tabular-nums">
                          {Number(entry.value).toLocaleString(undefined, { maximumFractionDigits: 1 })}
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
              iconType="square"
              wrapperStyle={{ fontSize: "10px", fontFamily: "JetBrains Mono", paddingBottom: "6px" }}
            />

            <Bar dataKey="Baseline" fill="#27272A" radius={[2, 2, 0, 0]} name="Baseline" />
            <Bar
              dataKey="Simulated"
              fill={simulation.profit_change_pct >= 0 ? "#10B981" : "#EF4444"}
              radius={[2, 2, 0, 0]}
              name="Simulated"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="flex items-center justify-between text-[10px] font-mono text-zinc-500 border-t border-[#18181B] pt-1">
        <span>Profit Variance: {simulation.profit_change_pct >= 0 ? "+" : ""}{simulation.profit_change_pct.toFixed(1)}%</span>
        <span>Leeroy & Leeroy (2025)</span>
      </div>
    </div>
  );
};
