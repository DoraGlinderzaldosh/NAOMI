import React from "react";
import { SimulationSliders } from "../../types";
import { CustomSlider } from "./CustomSlider";

interface ScenarioControlsProps {
  sliders: SimulationSliders;
  onChangeSliders: (newSliders: SimulationSliders) => void;
}

export const ScenarioControls: React.FC<ScenarioControlsProps> = ({
  sliders,
  onChangeSliders,
}) => {
  const presets = [
    {
      id: "baseline",
      label: "Baseline",
      isActive: sliders.priceDeltaPct === 0 && sliders.demandShockPct === 0 && sliders.costSurgePct === 0 && sliders.competitorDropPct === 0,
      apply: () => onChangeSliders({ priceDeltaPct: 0, demandShockPct: 0, costSurgePct: 0, competitorDropPct: 0 }),
    },
    {
      id: "price_up",
      label: "Price +5%",
      isActive: sliders.priceDeltaPct === 5 && sliders.demandShockPct === 0 && sliders.costSurgePct === 0 && sliders.competitorDropPct === 0,
      apply: () => onChangeSliders({ priceDeltaPct: 5, demandShockPct: 0, costSurgePct: 0, competitorDropPct: 0 }),
    },
    {
      id: "macro_shock",
      label: "Macro -15%",
      isActive: sliders.priceDeltaPct === 0 && sliders.demandShockPct === -15 && sliders.costSurgePct === 0 && sliders.competitorDropPct === 0,
      apply: () => onChangeSliders({ priceDeltaPct: 0, demandShockPct: -15, costSurgePct: 0, competitorDropPct: 0 }),
    },
    {
      id: "cost_surge",
      label: "Cost +10%",
      isActive: sliders.priceDeltaPct === 0 && sliders.demandShockPct === 0 && sliders.costSurgePct === 10 && sliders.competitorDropPct === 0,
      apply: () => onChangeSliders({ priceDeltaPct: 0, demandShockPct: 0, costSurgePct: 10, competitorDropPct: 0 }),
    },
    {
      id: "price_war",
      label: "Price War",
      isActive: sliders.priceDeltaPct === 0 && sliders.demandShockPct === 0 && sliders.costSurgePct === 0 && sliders.competitorDropPct === 10,
      apply: () => onChangeSliders({ priceDeltaPct: 0, demandShockPct: 0, costSurgePct: 0, competitorDropPct: 10 }),
    },
    {
      id: "stagflation",
      label: "Stagflation",
      isActive: sliders.priceDeltaPct === 0 && sliders.demandShockPct === -8 && sliders.costSurgePct === 10 && sliders.competitorDropPct === 0,
      apply: () => onChangeSliders({ priceDeltaPct: 0, demandShockPct: -8, costSurgePct: 10, competitorDropPct: 0 }),
    },
  ];

  const handleReset = () => {
    onChangeSliders({
      priceDeltaPct: 0,
      demandShockPct: 0,
      costSurgePct: 0,
      competitorDropPct: 0,
    });
  };

  return (
    <div className="w-full h-full flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-2.5">
          <div>
            <h3 className="text-xs font-mono font-semibold tracking-wide text-zinc-100 uppercase">
              Counterfactual Levers
            </h3>
            <p className="text-[11px] font-mono text-zinc-500">Exogenous Stress & Pricing Levers</p>
          </div>
          <button
            onClick={handleReset}
            className="text-[11px] font-mono text-zinc-400 hover:text-white px-2 py-0.5 rounded bg-[#121215] border border-[#27272A] hover:border-zinc-500 transition-colors cursor-pointer"
          >
            Reset
          </button>
        </div>

        {/* Presets Grid */}
        <div className="grid grid-cols-3 sm:grid-cols-6 gap-1.5 mb-3">
          {presets.map((preset) => (
            <button
              key={preset.id}
              onClick={preset.apply}
              className={`py-1 px-1.5 text-center rounded text-xs font-mono transition-colors ${
                preset.isActive
                  ? "bg-zinc-200 text-black font-bold border border-zinc-300"
                  : "bg-[#101014] border border-[#27272A] text-zinc-400 hover:text-zinc-200 hover:border-zinc-600"
              }`}
            >
              {preset.label}
            </button>
          ))}
        </div>

        {/* 4 Precision Sliders */}
        <div className="space-y-1">
          <CustomSlider
            label="Candidate Price Adjustment"
            value={sliders.priceDeltaPct}
            min={-30}
            max={40}
            step={1}
            unit="%"
            onChange={(val) => onChangeSliders({ ...sliders, priceDeltaPct: val })}
          />

          <CustomSlider
            label="Macro Demand Shock"
            value={sliders.demandShockPct}
            min={-50}
            max={30}
            step={1}
            unit="%"
            onChange={(val) => onChangeSliders({ ...sliders, demandShockPct: val })}
          />

          <CustomSlider
            label="Unit Cost Surge"
            value={sliders.costSurgePct}
            min={0}
            max={50}
            step={1}
            unit="%"
            onChange={(val) => onChangeSliders({ ...sliders, costSurgePct: val })}
          />

          <CustomSlider
            label="Competitor Price Cut"
            value={sliders.competitorDropPct}
            min={0}
            max={30}
            step={1}
            unit="%"
            onChange={(val) => onChangeSliders({ ...sliders, competitorDropPct: val })}
          />
        </div>
      </div>
    </div>
  );
};
