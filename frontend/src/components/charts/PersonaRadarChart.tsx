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
import { PersonaDetail, SKUInfo } from "../../types";

interface PersonaRadarChartProps {
  personas: PersonaDetail[];
  candidatePrice: number;
  sku: SKUInfo;
}

export const PersonaRadarChart: React.FC<PersonaRadarChartProps> = ({
  personas,
  candidatePrice,
  sku,
}) => {
  const data = personas.map((p) => ({
    name: p.name.replace(" Customer", "").replace(" Shopper", "").replace(" Buyer", ""),
    baselineProb: Math.round(p.baseline_prob * 100),
    candidateProb: Math.round(p.candidate_prob * 100),
    weight: p.weight_pct,
    delta: p.delta_prob_pct,
    reservePrice: p.reserve_price,
  }));

  return (
    <div className="w-full h-full flex flex-col justify-between">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h3 className="text-sm font-semibold tracking-tight text-white flex items-center gap-2">
            <span>Virtual Population Market Response</span>
            <span className="text-[10px] font-normal px-2 py-0.5 rounded-full bg-cyan-950/80 border border-cyan-800/70 text-cyan-300 font-mono">
              5 Archetypes
            </span>
          </h3>
          <p className="text-[11px] text-slate-400">
            Conversion probability: Baseline (${sku.base_price.toFixed(2)}) vs. Candidate (${candidatePrice.toFixed(2)})
          </p>
        </div>
      </div>

      <div className="w-full h-[250px] min-h-[250px]">
        <ResponsiveContainer width="100%" height="100%" minHeight={250}>
          <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="2 2" stroke="#1E293B" vertical={false} opacity={0.6} />
            <XAxis
              dataKey="name"
              stroke="#475569"
              tick={{ fill: "#94A3B8", fontSize: 10 }}
              tickLine={false}
              axisLine={{ stroke: "#1E293B" }}
            />
            <YAxis
              stroke="#475569"
              tickFormatter={(v) => `${v}%`}
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
                    <p className="text-white font-bold mb-1">{d.name}</p>
                    <div className="flex justify-between gap-4 py-0.5 text-slate-400">
                      <span>Population Weight:</span>
                      <span className="text-cyan-400 font-bold">{d.weight}%</span>
                    </div>
                    <div className="flex justify-between gap-4 py-0.5 text-slate-300">
                      <span>Baseline Conversion:</span>
                      <span className="text-slate-300 font-bold">{d.baselineProb}%</span>
                    </div>
                    <div className="flex justify-between gap-4 py-0.5 text-slate-300">
                      <span>Candidate Conversion:</span>
                      <span className={`font-bold ${d.delta >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
                        {d.candidateProb}% ({d.delta >= 0 ? "+" : ""}{d.delta}%)
                      </span>
                    </div>
                    <div className="flex justify-between gap-4 py-0.5 text-slate-400 border-t border-slate-800 mt-1 pt-1">
                      <span>Reserve Price Ceiling:</span>
                      <span className="text-amber-300 font-bold">${d.reservePrice.toFixed(2)}</span>
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
            <Bar dataKey="baselineProb" fill="#475569" radius={[4, 4, 0, 0]} name="Baseline Prob %" />
            <Bar dataKey="candidateProb" fill="#0EA5E9" radius={[4, 4, 0, 0]} name="Candidate Prob %" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono pt-1 border-t border-slate-800/60">
        <span>Persona Conversion Rates % (Y-Axis)</span>
        <span>Huang & Wang (Columbia 2026)</span>
      </div>
    </div>
  );
};
