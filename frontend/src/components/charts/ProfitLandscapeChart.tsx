import React from "react";
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ReferenceLine,
  ReferenceDot,
  Legend,
} from "recharts";
import { OptimizationData, SKUInfo } from "../../types";

interface ProfitLandscapeChartProps {
  optData: OptimizationData;
  sku: SKUInfo;
}

export const ProfitLandscapeChart: React.FC<ProfitLandscapeChartProps> = ({
  optData,
  sku,
}) => {
  const data = optData.curve_prices.map((p, i) => ({
    price: p,
    profit: optData.curve_profits[i],
    revenue: optData.curve_revenues[i],
  }));

  return (
    <div className="w-full h-full flex flex-col justify-between">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h3 className="text-xs font-mono font-semibold tracking-wide text-zinc-100 uppercase flex items-center gap-2">
            <span>Profit & Revenue Optimization Curve</span>
            <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-[#121215] border border-[#27272A] text-zinc-400">
              MIT Separable
            </span>
          </h3>
          <p className="text-[11px] font-mono text-zinc-500">
            Parabolic Inflection Frontier Across Managerial Corridor (±30%)
          </p>
        </div>
        <div className="text-right">
          <span className="text-[10px] font-mono text-zinc-500 block uppercase">P* Optimum</span>
          <span className="text-xs font-mono font-bold text-white tabular-nums">${optData.optimal_price.toFixed(2)}</span>
        </div>
      </div>

      <div className="w-full h-[260px] min-h-[260px]">
        <ResponsiveContainer width="100%" height="100%" minHeight={260}>
          <ComposedChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="1 1" stroke="#18181B" vertical={false} />

            <XAxis
              dataKey="price"
              stroke="#3F3F46"
              tickFormatter={(val) => `$${Number(val).toFixed(2)}`}
              tick={{ fill: "#71717A", fontSize: 10, fontFamily: "JetBrains Mono" }}
              tickLine={false}
              axisLine={{ stroke: "#1F1F23" }}
            />
            <YAxis
              stroke="#3F3F46"
              tickFormatter={(val) => `$${Number(val).toFixed(0)}`}
              tick={{ fill: "#71717A", fontSize: 10, fontFamily: "JetBrains Mono" }}
              tickLine={false}
              axisLine={false}
            />

            <Tooltip
              content={({ active, payload }) => {
                if (!active || !payload || !payload.length) return null;
                const p = payload[0].payload.price;
                const profit = payload[0].payload.profit;
                const revenue = payload[0].payload.revenue;
                return (
                  <div className="rounded border border-[#27272A] bg-[#09090B] p-2.5 shadow-2xl text-xs font-mono">
                    <p className="text-zinc-300 font-bold mb-1 border-b border-[#18181B] pb-1">Price Point: ${Number(p).toFixed(2)}</p>
                    <div className="flex items-center justify-between gap-4 py-0.5">
                      <span className="text-zinc-400">Net Profit:</span>
                      <span className="font-bold text-emerald-400 tabular-nums">${Number(profit).toFixed(2)}</span>
                    </div>
                    <div className="flex items-center justify-between gap-4 py-0.5">
                      <span className="text-zinc-400">Gross Revenue:</span>
                      <span className="font-bold text-zinc-200 tabular-nums">${Number(revenue).toFixed(2)}</span>
                    </div>
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

            {/* Current Price Marker */}
            <ReferenceLine
              x={sku.base_price}
              stroke="#71717A"
              strokeDasharray="2 2"
              label={{
                value: `Current $${sku.base_price.toFixed(2)}`,
                fill: "#71717A",
                fontSize: 9,
                fontFamily: "JetBrains Mono",
                position: "insideTopLeft",
              }}
            />

            {/* Optimal Price Peak Marker */}
            <ReferenceLine
              x={optData.optimal_price}
              stroke="#10B981"
              strokeDasharray="2 2"
              label={{
                value: `P* $${optData.optimal_price.toFixed(2)}`,
                fill: "#10B981",
                fontSize: 9,
                fontFamily: "JetBrains Mono",
                position: "insideTopRight",
              }}
            />

            <Line
              type="monotone"
              dataKey="revenue"
              stroke="#52525B"
              strokeWidth={1.5}
              dot={false}
              name="Revenue P·Q"
            />

            <Line
              type="monotone"
              dataKey="profit"
              stroke="#10B981"
              strokeWidth={2.2}
              dot={false}
              name="Operating Profit Π"
            />

            <ReferenceDot
              x={optData.optimal_price}
              y={optData.optimal_profit}
              r={4.5}
              fill="#10B981"
              stroke="#FFFFFF"
              strokeWidth={1.5}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      <div className="flex items-center justify-between text-[10px] font-mono text-zinc-500 border-t border-[#18181B] pt-1">
        <span>Shape Constraint: ∂g/∂p ≤ 0 (Monotone Non-Increasing)</span>
        <span>Simchi-Levi et al. (MIT)</span>
      </div>
    </div>
  );
};
