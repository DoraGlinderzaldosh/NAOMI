import React from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceDot,
  Legend,
} from "recharts";
import { FrontierPoint, SKUInfo } from "../../types";

interface RiskFrontierChartProps {
  frontier: FrontierPoint[];
  currentLambda: number;
  sku: SKUInfo;
}

export const RiskFrontierChart: React.FC<RiskFrontierChartProps> = ({
  frontier,
  currentLambda,
  sku,
}) => {
  // Sort points by tail risk exposure ascending
  const data = frontier.map((pt) => ({
    lambda: pt.lambda,
    tailRisk: Math.round(pt.tail_risk_exposure * 100) / 100,
    expectedProfit: Math.round(pt.expected_profit * 100) / 100,
    cvarProfit: Math.round(pt.cvar_downside_profit * 100) / 100,
    price: pt.optimal_price,
  }));

  // Find closest point to currentLambda
  const activePt = data.reduce((prev, curr) =>
    Math.abs(curr.lambda - currentLambda) < Math.abs(prev.lambda - currentLambda) ? curr : prev
  );

  return (
    <div className="w-full h-full flex flex-col justify-between">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h3 className="text-sm font-semibold tracking-tight text-white flex items-center gap-2">
            <span>Executive Risk Frontier (CVaR)</span>
            <span className="text-[10px] font-normal px-2 py-0.5 rounded-full bg-rose-950/80 border border-rose-800/70 text-rose-300 font-mono">
              λ = {currentLambda.toFixed(2)}
            </span>
          </h3>
          <p className="text-[11px] text-slate-400">
            Expected Enterprise Profit vs. Tail-Risk Downside Exposure
          </p>
        </div>
        <div className="text-right">
          <span className="text-[10px] text-slate-400 font-mono block">Optimal Price</span>
          <span className="text-xs font-bold text-white font-mono">${activePt.price.toFixed(2)}</span>
        </div>
      </div>

      <div className="w-full h-[250px] min-h-[250px]">
        <ResponsiveContainer width="100%" height="100%" minHeight={250}>
          <LineChart data={data} margin={{ top: 10, right: 15, left: -15, bottom: 0 }}>
            <CartesianGrid strokeDasharray="2 2" stroke="#1E293B" vertical={false} opacity={0.6} />
            <XAxis
              dataKey="tailRisk"
              stroke="#475569"
              tickFormatter={(v) => `$${v}`}
              tick={{ fill: "#94A3B8", fontSize: 10, fontFamily: "JetBrains Mono" }}
              tickLine={false}
              axisLine={{ stroke: "#1E293B" }}
            />
            <YAxis
              dataKey="expectedProfit"
              stroke="#475569"
              tickFormatter={(v) => `$${v}`}
              tick={{ fill: "#94A3B8", fontSize: 10, fontFamily: "JetBrains Mono" }}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (!active || !payload || !payload.length) return null;
                const d = payload[0].payload;
                return (
                  <div className="rounded-lg border border-slate-800 bg-[#111827] p-2.5 shadow-xl text-xs font-mono">
                    <p className="text-rose-400 font-bold mb-1">Risk Aversion λ: {d.lambda.toFixed(2)}</p>
                    <div className="flex justify-between gap-4 py-0.5 text-slate-300">
                      <span>Expected Profit:</span>
                      <span className="font-bold text-emerald-400">${d.expectedProfit.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between gap-4 py-0.5 text-slate-300">
                      <span>CVaR (Worst 10%):</span>
                      <span className="font-bold text-rose-300">${d.cvarProfit.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between gap-4 py-0.5 text-slate-300">
                      <span>Tail-Risk Gap:</span>
                      <span className="font-bold text-amber-300">${d.tailRisk.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between gap-4 py-0.5 text-slate-300 border-t border-slate-800 mt-1 pt-1">
                      <span>Price:</span>
                      <span className="font-bold text-white">${d.price.toFixed(2)}</span>
                    </div>
                  </div>
                );
              }}
            />
            <Legend
              verticalAlign="top"
              align="right"
              iconType="circle"
              wrapperStyle={{ fontSize: "11px", paddingBottom: "6px" }}
            />
            <Line
              type="monotone"
              dataKey="expectedProfit"
              stroke="#10B981"
              strokeWidth={2.5}
              dot={{ r: 3, fill: "#10B981" }}
              name="Expected Profit E[Π]"
            />
            <Line
              type="monotone"
              dataKey="cvarProfit"
              stroke="#E11D48"
              strokeWidth={2}
              strokeDasharray="4 4"
              dot={{ r: 2, fill: "#E11D48" }}
              name="Downside CVaR_10%"
            />
            {activePt && (
              <ReferenceDot
                x={activePt.tailRisk}
                y={activePt.expectedProfit}
                r={6}
                fill="#38BDF8"
                stroke="#FFFFFF"
                strokeWidth={2}
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono pt-1 border-t border-slate-800/60">
        <span>Tail Risk Exposure (X-Axis)</span>
        <span>Huang & Wang (Columbia, 2026)</span>
      </div>
    </div>
  );
};
