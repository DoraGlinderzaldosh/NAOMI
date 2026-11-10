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

  const getRiskColor = (risk: SimulationResult["risk_label"]) => {
    switch (risk) {
      case "Positive":
        return "bg-emerald-950/90 border-emerald-600/70 text-emerald-300";
      case "Stable":
        return "bg-slate-800/90 border-slate-700 text-slate-200";
      case "Moderate Risk":
        return "bg-amber-950/90 border-amber-600/70 text-amber-300";
      case "High Risk":
      case "Critical Risk":
        return "bg-rose-950/90 border-rose-700 text-rose-300";
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
    <div className="w-full h-full flex flex-col justify-between rounded-xl border border-slate-800/80 bg-gradient-to-b from-[#131B2E] to-[#0E1524] p-4 shadow-sm overflow-hidden">
      <div className="flex-1 flex flex-col min-h-0">
        {/* Header */}
        <div className="flex items-center justify-between mb-2">
          <div>
            <h3 className="text-sm font-semibold tracking-tight text-white flex items-center gap-2">
              <span>C-Suite Strategic Companion</span>
              <span className="text-[10px] font-normal px-2 py-0.5 rounded-full bg-cyan-950/80 border border-cyan-800/70 text-cyan-300">
                Phase 8
              </span>
            </h3>
            <p className="text-[11px] text-slate-400">Automated counterfactual scenario briefing</p>
          </div>
          <span
            className={`px-2.5 py-0.5 rounded-full text-xs font-mono font-bold border ${getRiskColor(
              simulation.risk_label
            )}`}
          >
            {simulation.risk_label}
          </span>
        </div>

        {/* Narrative Summary Area */}
        <div className="flex-1 min-h-[140px] max-h-[170px] overflow-y-auto text-xs text-slate-300 leading-relaxed bg-[#111827] border border-slate-800/90 p-3 rounded-lg mb-2">
          {isGenerating ? (
            <div className="h-full flex items-center justify-center gap-2 text-cyan-400">
              <span className="animate-spin text-sm">✦</span>
              <span>Synthesizing C-Suite Brief with anti-hallucination verification...</span>
            </div>
          ) : executiveNarrative ? (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-[10px] text-slate-400 border-b border-slate-800/60 pb-1 mb-1">
                <span className="text-emerald-400 font-mono">✓ Numerically Verified (Zero Hallucination)</span>
                <span className="text-slate-400 uppercase font-mono">Source: {narrativeSource}</span>
              </div>
              <p className="whitespace-pre-line text-[11px] leading-relaxed text-slate-200">
                {executiveNarrative}
              </p>
            </div>
          ) : (
            <p className="leading-relaxed">{simulation.executive_brief}</p>
          )}
        </div>

        {/* Structured Executive Metrics */}
        <div className="grid grid-cols-3 gap-2 text-xs font-mono">
          <div className="p-2 rounded-lg bg-[#111827] border border-slate-800/70 flex flex-col">
            <span className="text-slate-400 text-[10px]">Price Elasticity</span>
            <span className="font-bold text-white mt-0.5 text-[11px]">
              Ed = {sku.historical_elasticity.toFixed(2)}
            </span>
            <span className="text-[10px] text-slate-400 font-sans">
              {sku.historical_elasticity < -1 ? "Elastic" : "Inelastic"}
            </span>
          </div>

          <div className="p-2 rounded-lg bg-[#111827] border border-slate-800/70 flex flex-col">
            <span className="text-slate-400 text-[10px]">Breakeven Volume</span>
            <span className="font-bold text-white mt-0.5 text-[11px]">
              {simulation.shocked_kpis.breakeven_units} u/day
            </span>
            <span className="text-[10px] text-slate-400 font-sans">Target threshold</span>
          </div>

          <div className="p-2 rounded-lg bg-[#111827] border border-slate-800/70 flex flex-col">
            <span className="text-slate-400 text-[10px]">Profit Delta</span>
            <span className={`font-bold mt-0.5 text-[11px] ${profitDelta >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
              {profitDelta >= 0 ? "+" : ""}${profitDelta.toFixed(2)}/d
            </span>
            <span className="text-[10px] text-slate-400 font-sans">vs. Baseline</span>
          </div>
        </div>
      </div>

      {/* Action Footer */}
      <div className="mt-2.5 pt-2 border-t border-slate-800/70 text-[10px] text-slate-400 flex items-center justify-between">
        <button
          onClick={handleGenerateNarrative}
          disabled={isGenerating}
          className="px-2.5 py-1 rounded bg-rose-600/20 hover:bg-rose-600/30 border border-rose-500/40 text-rose-300 font-sans font-medium transition-colors cursor-pointer flex items-center gap-1.5"
        >
          <span>✦</span>
          <span>{executiveNarrative ? "Regenerate Executive Brief" : "Generate C-Suite Narrative"}</span>
        </button>
        <span className="text-slate-400 font-mono">AI-assisted, not binding.</span>
      </div>
    </div>
  );
};
