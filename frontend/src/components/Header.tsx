import React from "react";
import { SKUInfo } from "../types";
import { CURATED_SKUS } from "../services/api";

interface HeaderProps {
  selectedSku: SKUInfo;
  onSelectSku: (sku: SKUInfo) => void;
  horizon: number;
  onSelectHorizon: (h: number) => void;
}

export const Header: React.FC<HeaderProps> = ({
  selectedSku,
  onSelectSku,
  horizon,
  onSelectHorizon,
}) => {
  const horizons = [
    { label: "1D", value: 1 },
    { label: "7D", value: 7 },
    { label: "30D", value: 30 },
  ];

  return (
    <header className="sticky top-0 z-50 bg-[#000000] border-b border-[#1F1F23] px-6 py-2.5">
      <div className="max-w-[1540px] mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
        
        {/* Brand & System Status */}
        <div className="flex items-center gap-3">
          <div className="h-7 px-2 rounded bg-white text-black font-mono font-bold text-xs flex items-center justify-center tracking-wider">
            NAOMI
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-semibold text-xs tracking-wide text-zinc-100 uppercase">
                Enterprise Decision Platform
              </span>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-[#121215] text-zinc-400 border border-[#27272A]">
                v2.0 • M5 Core
              </span>
            </div>
            <p className="text-[10px] font-mono text-zinc-500">
              Econometric Pricing Engine • 1,913-Day Walmart Time-Series
            </p>
          </div>
        </div>

        {/* Center: SKU Ticker Selector */}
        <div className="flex items-center gap-1 p-0.5 bg-[#09090B] border border-[#1F1F23] rounded-md overflow-x-auto max-w-full no-scrollbar">
          {CURATED_SKUS.map((sku) => {
            const isSelected = sku.item_id === selectedSku.item_id;
            return (
              <button
                key={sku.item_id}
                onClick={() => onSelectSku(sku)}
                className={`px-2.5 py-1 rounded text-xs font-mono transition-colors whitespace-nowrap flex items-center gap-2 ${
                  isSelected
                    ? "bg-[#1C1C21] text-white border border-zinc-600 font-semibold shadow-sm"
                    : "text-zinc-400 hover:text-zinc-200 hover:bg-[#121215] border border-transparent"
                }`}
              >
                <span className="text-[10px] text-zinc-500 uppercase">{sku.category.slice(0, 4)}</span>
                <span className="font-sans font-medium">{sku.item_name.replace(" Item ", " ")}</span>
                <span className={`text-[10px] tabular-nums ${isSelected ? "text-emerald-400" : "text-zinc-400"}`}>
                  ${sku.base_price.toFixed(2)}
                </span>
              </button>
            );
          })}
        </div>

        {/* Right: Horizon Selector */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1 p-0.5 bg-[#09090B] border border-[#1F1F23] rounded-md font-mono text-xs">
            <span className="text-[10px] text-zinc-500 px-2 uppercase tracking-wider">Horizon:</span>
            {horizons.map((h) => {
              const isActive = horizon === h.value;
              return (
                <button
                  key={h.value}
                  onClick={() => onSelectHorizon(h.value)}
                  className={`px-2 py-0.5 rounded text-xs transition-colors ${
                    isActive
                      ? "bg-zinc-200 text-black font-bold"
                      : "text-zinc-400 hover:text-zinc-200"
                  }`}
                >
                  {h.label}
                </button>
              );
            })}
          </div>
        </div>

      </div>
    </header>
  );
};
