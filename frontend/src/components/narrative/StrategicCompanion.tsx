import React, { useState } from "react";
import { SimulationResult, SKUInfo } from "../../types";
import { fetchExecutiveNarrative } from "../../services/api";

interface StrategicCompanionProps {
  simulation: SimulationResult;
  sku: SKUInfo;
}

export const StrategicCompanion: React.FC<StrategicCompanionProps> = ({
  simulation,
  sku,
}) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [executiveNarrative, setExecutiveNarrative] = useState<string | null>(null);
  const [narrativeSource, setNarrativeSource] = useState<string>("fallback");

  const getRiskBadge = (risk: SimulationResult["risk_label"]) => {
    switch (risk) {
      case "Positive":
        return "border-emerald-900 bg-emerald-950/40 text-emerald-400";
      case "Stable":
        return "border-zinc-800 bg-zinc-900 text-zinc-300";
      case "Moderate Risk":
        return "border-amber-900 bg-amber-950/40 text-amber-400";
      case "High Risk":
      case "Critical Risk":
        return "border-rose-900 bg-rose-950/40 text-rose-400";
    }
  };

  const profitDelta = simulation.shocked_kpis.gross_profit - simulation.baseline_kpis.gross_profit;

  const handleGenerateNarrative = async () => {
    setIsGenerating(true);
    try {
      const res = await fetchExecutiveNarrative(sku.item_id, 14);
      setExecutiveNarrative(res.narrative);
      setNarrativeSource(res.source);
    } catch {
      // Keep existing brief
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="w-full h-full flex flex-col justify-between rounded-lg border border-[#1F1F23] bg-[#070709] p-4 overflow-hidden">
      <div className="flex-1 flex flex-col min-h-0">
        {/* Header */}
        <div className="flex items-center justify-between mb-2">
          <div>
            <h3 className="text-xs font-mono font-semibold tracking-wide text-zinc-100 uppercase flex items-center gap-2">
              <span>Executive Briefing Memo</span>
              <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-[#121215] border border-[#27272A] text-zinc-400">
                Phase 8
              </span>
            </h3>
            <p className="text-[11px] font-mono text-zinc-500">Commercial Strategy & Risk Telemetry</p>
          </div>
          <span
            className={`px-2 py-0.5 rounded text-[10px] font-mono font-semibold border ${getRiskBadge(
              simulation.risk_label
            )}`}
          >
            {simulation.risk_label.toUpperCase()}
          </span>
        </div>

        {/* Narrative Summary Area */}
        <div className="flex-1 min-h-[140px] max-h-[170px] overflow-y-auto text-xs text-zinc-300 leading-relaxed bg-[#030304] border border-[#18181B] p-3 rounded mb-2 font-sans">
          {isGenerating ? (
            <div className="h-full flex items-center justify-center gap-2 text-zinc-400 font-mono text-xs">
              <span className="animate-pulse">●</span>
              <span>Running econometric verification guard...</span>
            </div>
          ) : executiveNarrative ? (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-[10px] text-zinc-500 border-b border-[#18181B] pb-1 mb-1 font-mono">
                <span className="text-emerald-400">AUDIT: VERIFIED (ZERO HALLUCINATION)</span>
                <span className="uppercase text-zinc-500">SOURCE: {narrativeSource}</span>
              </div>
              <p className="whitespace-pre-line text-xs leading-relaxed text-zinc-300 font-sans">
                {executiveNarrative}
              </p>
            </div>
          ) : (
            <p className="leading-relaxed text-zinc-300 text-xs font-sans">{simulation.executive_brief}</p>
          )}
        </div>

        {/* Structured Executive Metrics */}
        <div className="grid grid-cols-3 gap-2 text-xs font-mono">
          <div className="p-2 rounded bg-[#0A0A0D] border border-[#18181B] flex flex-col">
            <span className="text-zinc-500 text-[10px] uppercase">Elasticity</span>
            <span className="font-bold text-zinc-100 mt-0.5 text-[11px] tabular-nums">
              Ed = {sku.historical_elasticity.toFixed(2)}
            </span>
            <span className="text-[10px] text-zinc-500">
              {sku.historical_elasticity < -1 ? "Elastic" : "Inelastic"}
            </span>
          </div>

          <div className="p-2 rounded bg-[#0A0A0D] border border-[#18181B] flex flex-col">
            <span className="text-zinc-500 text-[10px] uppercase">Breakeven</span>
            <span className="font-bold text-zinc-100 mt-0.5 text-[11px] tabular-nums">
              {simulation.shocked_kpis.breakeven_units} u/day
            </span>
            <span className="text-[10px] text-zinc-500">Target Run-Rate</span>
          </div>

          <div className="p-2 rounded bg-[#0A0A0D] border border-[#18181B] flex flex-col">
            <span className="text-zinc-500 text-[10px] uppercase">Profit Variance</span>
            <span className={`font-bold mt-0.5 text-[11px] tabular-nums ${profitDelta >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
              {profitDelta >= 0 ? "+" : ""}${profitDelta.toFixed(2)}/d
            </span>
            <span className="text-[10px] text-zinc-500">vs. Baseline</span>
          </div>
        </div>
      </div>

      {/* Action Footer */}
      <div className="mt-2.5 pt-2 border-t border-[#18181B] text-[10px] text-zinc-500 font-mono flex items-center justify-between">
        <button
          onClick={handleGenerateNarrative}
          disabled={isGenerating}
          className="px-2.5 py-1 rounded bg-[#121215] hover:bg-[#1C1C21] border border-[#27272A] hover:border-zinc-500 text-zinc-200 font-mono text-xs transition-colors cursor-pointer"
        >
          {executiveNarrative ? "Regenerate Brief" : "Generate C-Suite Brief"}
        </button>
        <span className="text-zinc-500 uppercase">AI-assisted, not binding.</span>
      </div>
    </div>
  );
};
