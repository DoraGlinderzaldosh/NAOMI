import React from "react";
import { OptimizationData, SKUInfo } from "../types";

interface KpiHeroGridProps {
  optData: OptimizationData;
  sku: SKUInfo;
  horizon: number;
}

export const KpiHeroGrid: React.FC<KpiHeroGridProps> = ({
  optData,
  sku,
  horizon,
}) => {
  const baseDemand = optData.optimal_demand / Math.pow(optData.optimal_price / sku.base_price, sku.historical_elasticity);
  const demandDeltaPct = ((optData.optimal_demand - baseDemand) / baseDemand) * 100;
  const horizonRevenue = optData.optimal_revenue * horizon;

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
      
      {/* 1. Optimal Price (P*) */}
      <div className="rounded-lg border border-[#1F1F23] bg-[#070709] p-3.5 flex flex-col justify-between">
        <div className="flex items-center justify-between text-[11px] text-zinc-400 font-mono uppercase tracking-wider">
          <span>OPTIMAL PRICE [P*]</span>
          <span className={`text-[10px] font-bold px-1.5 py-0.2 rounded border ${
            optData.price_change_pct >= 0
              ? "border-emerald-900/80 bg-emerald-950/40 text-emerald-400"
              : "border-zinc-800 bg-zinc-900 text-zinc-300"
          }`}>
            {optData.price_change_pct >= 0 ? "+" : ""}{optData.price_change_pct.toFixed(1)}%
          </span>
        </div>
        <div className="my-2">
          <span className="text-2xl lg:text-3xl font-bold tracking-tight text-white font-mono tabular-nums">
            ${optData.optimal_price.toFixed(2)}
          </span>
        </div>
        <div className="text-[11px] text-zinc-500 font-mono flex items-center justify-between border-t border-[#18181B] pt-1.5">
          <span>Current: ${sku.base_price.toFixed(2)}</span>
          <span className="text-zinc-400">Inflection Point</span>
        </div>
      </div>

      {/* 2. Target Demand (Q*) */}
      <div className="rounded-lg border border-[#1F1F23] bg-[#070709] p-3.5 flex flex-col justify-between">
        <div className="flex items-center justify-between text-[11px] text-zinc-400 font-mono uppercase tracking-wider">
          <span>EQUILIBRIUM VOLUME [Q*]</span>
          <span className="text-[10px] font-mono text-zinc-500">
            {horizon}D WINDOW
          </span>
        </div>
        <div className="my-2">
          <span className="text-2xl lg:text-3xl font-bold tracking-tight text-white font-mono tabular-nums">
            {optData.optimal_demand.toFixed(1)}
          </span>
          <span className="text-xs font-mono text-zinc-500 ml-1.5">units/day</span>
        </div>
        <div className="text-[11px] text-zinc-500 font-mono flex items-center justify-between border-t border-[#18181B] pt-1.5">
          <span>Volume Delta</span>
          <span className={demandDeltaPct >= 0 ? "text-emerald-400" : "text-zinc-300"}>
            {demandDeltaPct >= 0 ? "+" : ""}{demandDeltaPct.toFixed(1)}%
          </span>
        </div>
      </div>

      {/* 3. Projected Daily Revenue */}
      <div className="rounded-lg border border-[#1F1F23] bg-[#070709] p-3.5 flex flex-col justify-between">
        <div className="flex items-center justify-between text-[11px] text-zinc-400 font-mono uppercase tracking-wider">
          <span>PROJECTED REVENUE</span>
          <span className="text-[10px] font-mono text-zinc-500">${horizonRevenue.toFixed(0)} / {horizon}D</span>
        </div>
        <div className="my-2">
          <span className="text-2xl lg:text-3xl font-bold tracking-tight text-white font-mono tabular-nums">
            ${optData.optimal_revenue.toFixed(2)}
          </span>
          <span className="text-xs font-mono text-zinc-500 ml-1.5">/day</span>
        </div>
        <div className="text-[11px] text-zinc-500 font-mono flex items-center justify-between border-t border-[#18181B] pt-1.5">
          <span>Gross Run-Rate</span>
          <span className="text-zinc-400">P* × Q*</span>
        </div>
      </div>

      {/* 4. Operating Profit (Pi*) */}
      <div className="rounded-lg border border-[#1F1F23] bg-[#070709] p-3.5 flex flex-col justify-between">
        <div className="flex items-center justify-between text-[11px] text-zinc-400 font-mono uppercase tracking-wider">
          <span>NET OPERATING PROFIT</span>
          <span className="text-[10px] font-mono px-1.5 py-0.2 rounded border border-emerald-900/80 bg-emerald-950/40 text-emerald-400 font-bold">
            +{optData.profit_uplift_pct.toFixed(1)}%
          </span>
        </div>
        <div className="my-2">
          <span className="text-2xl lg:text-3xl font-bold tracking-tight text-emerald-400 font-mono tabular-nums">
            ${optData.optimal_profit.toFixed(2)}
          </span>
          <span className="text-xs font-mono text-zinc-500 ml-1.5">/day</span>
        </div>
        <div className="text-[11px] text-zinc-500 font-mono flex items-center justify-between border-t border-[#18181B] pt-1.5">
          <span>Overhead Deducted</span>
          <span className="text-zinc-400">Net Contribution</span>
        </div>
      </div>

      {/* 5. Gross Margin & Breakeven */}
      <div className="rounded-lg border border-[#1F1F23] bg-[#070709] p-3.5 flex flex-col justify-between col-span-2 md:col-span-1">
        <div className="flex items-center justify-between text-[11px] text-zinc-400 font-mono uppercase tracking-wider">
          <span>MARGIN / BREAKEVEN</span>
          <span className="text-[10px] font-mono text-zinc-400 font-bold">
            {optData.gross_margin_pct.toFixed(1)}% MARGIN
          </span>
        </div>
        <div className="my-2">
          <span className="text-2xl lg:text-3xl font-bold tracking-tight text-white font-mono tabular-nums">
            {optData.breakeven_units}
          </span>
          <span className="text-xs font-mono text-zinc-500 ml-1.5">units/day</span>
        </div>
        <div className="text-[11px] text-zinc-500 font-mono flex items-center justify-between border-t border-[#18181B] pt-1.5">
          <span>Breakeven Threshold</span>
          <span className="text-zinc-400">Daily Target</span>
        </div>
      </div>

    </div>
  );
};
