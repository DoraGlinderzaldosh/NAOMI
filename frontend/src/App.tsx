import React, { useState, useMemo } from "react";
import { Header } from "./components/Header";
import { KpiHeroGrid } from "./components/KpiHeroGrid";
import { DemandTrajectoryChart } from "./components/charts/DemandTrajectoryChart";
import { ProfitLandscapeChart } from "./components/charts/ProfitLandscapeChart";
import { RiskFrontierChart } from "./components/charts/RiskFrontierChart";
import { PersonaRadarChart } from "./components/charts/PersonaRadarChart";
import { ScenarioComparisonChart } from "./components/charts/ScenarioComparisonChart";
import { ScenarioControls } from "./components/controls/ScenarioControls";
import { StrategicCompanion } from "./components/narrative/StrategicCompanion";
import { SpotlightCard } from "./components/ui/Spotlight";
import {
  CURATED_SKUS,
  getHistoricalDemand,
  getForecastSeries,
  computeProfitLandscape,
  computeSimulation,
  computeExecutiveRiskFrontier,
  getVirtualPopulationSync,
} from "./services/api";
import { SKUInfo, SimulationSliders } from "./types";

export const App: React.FC = () => {
  const [selectedSku, setSelectedSku] = useState<SKUInfo>(CURATED_SKUS[0]);
  const [horizon, setHorizon] = useState<number>(7);
  const [activeTab, setActiveTab] = useState<"operational" | "risk">("operational");
  const [sliders, setSliders] = useState<SimulationSliders>({
    priceDeltaPct: 0,
    demandShockPct: 0,
    costSurgePct: 0,
    competitorDropPct: 0,
  });

  // Real-time analytical computation
  const historical = useMemo(() => getHistoricalDemand(selectedSku.item_id), [selectedSku.item_id]);
  const forecast = useMemo(() => getForecastSeries(selectedSku.item_id, horizon), [selectedSku.item_id, horizon]);
  const optData = useMemo(() => computeProfitLandscape(selectedSku), [selectedSku]);
  const simulation = useMemo(() => computeSimulation(selectedSku, sliders), [selectedSku, sliders]);
  const riskFrontier = useMemo(() => computeExecutiveRiskFrontier(selectedSku), [selectedSku]);
  const virtualPopulation = useMemo(
    () => getVirtualPopulationSync(selectedSku, simulation.candidate_price),
    [selectedSku, simulation.candidate_price]
  );

  return (
    <div className="min-h-screen bg-[#000000] text-zinc-100 flex flex-col font-sans selection:bg-zinc-800 selection:text-white">
      {/* Institutional Top Navigation */}
      <Header
        selectedSku={selectedSku}
        onSelectSku={setSelectedSku}
        horizon={horizon}
        onSelectHorizon={setHorizon}
      />

      {/* Main Terminal Workspace */}
      <main className="max-w-[1540px] w-full mx-auto px-6 py-4 space-y-4 flex-1">
        
        {/* Row 1: KPI Hero Bento Cards */}
        <section>
          <KpiHeroGrid
            optData={optData}
            sku={selectedSku}
            horizon={horizon}
          />
        </section>

        {/* View Switcher Bar */}
        <section className="flex items-center justify-between border-b border-[#1F1F23] pb-2 pt-1">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-mono text-zinc-500 uppercase tracking-widest">ANALYTICAL MODULE:</span>
            <div className="flex items-center p-0.5 bg-[#09090B] border border-[#1F1F23] rounded">
              <button
                onClick={() => setActiveTab("operational")}
                className={`px-3 py-1 text-xs font-mono rounded transition-colors ${
                  activeTab === "operational"
                    ? "bg-[#18181B] text-white border border-zinc-700 font-bold"
                    : "text-zinc-400 hover:text-zinc-200"
                }`}
              >
                01 // DEMAND & PROFIT INFLECTION
              </button>
              <button
                onClick={() => setActiveTab("risk")}
                className={`px-3 py-1 text-xs font-mono rounded transition-colors ${
                  activeTab === "risk"
                    ? "bg-[#18181B] text-white border border-zinc-700 font-bold"
                    : "text-zinc-400 hover:text-zinc-200"
                }`}
              >
                02 // CVaR RISK FRONTIER & PERSONAS
              </button>
            </div>
          </div>

          <div className="text-[11px] font-mono text-zinc-500 hidden sm:flex items-center gap-3">
            <span>● FEED: WALMART M5 (1,913D)</span>
            <span>MODEL: CO-ORDINATE DESCENT</span>
          </div>
        </section>

        {/* Row 2: Analytical Visualizations */}
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-3.5">
          {activeTab === "operational" ? (
            <>
              <SpotlightCard className="h-[340px]">
                <DemandTrajectoryChart
                  historical={historical}
                  forecast={forecast}
                  sku={selectedSku}
                />
              </SpotlightCard>

              <SpotlightCard className="h-[340px]">
                <ProfitLandscapeChart
                  optData={optData}
                  sku={selectedSku}
                />
              </SpotlightCard>
            </>
          ) : (
            <>
              <SpotlightCard className="h-[340px]">
                <RiskFrontierChart
                  frontier={riskFrontier}
                  currentLambda={0.4}
                  sku={selectedSku}
                />
              </SpotlightCard>

              <SpotlightCard className="h-[340px]">
                <PersonaRadarChart
                  personas={virtualPopulation.personas}
                  candidatePrice={simulation.candidate_price}
                  sku={selectedSku}
                />
              </SpotlightCard>
            </>
          )}
        </section>

        {/* Row 3: Decision Workspace (3 Columns) */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-3.5">
          {/* Sliders (4 cols) */}
          <div className="lg:col-span-4">
            <SpotlightCard className="h-[350px]">
              <ScenarioControls
                sliders={sliders}
                onChangeSliders={setSliders}
              />
            </SpotlightCard>
          </div>

          {/* Variance Bars (4 cols) */}
          <div className="lg:col-span-4">
            <SpotlightCard className="h-[350px]">
              <ScenarioComparisonChart simulation={simulation} />
            </SpotlightCard>
          </div>

          {/* Strategic Memo (4 cols) */}
          <div className="lg:col-span-4">
            <div className="h-[350px]">
              <StrategicCompanion
                simulation={simulation}
                sku={selectedSku}
              />
            </div>
          </div>
        </section>

      </main>

      {/* Terminal Footer */}
      <footer className="border-t border-[#1F1F23] bg-[#000000] py-2.5 px-6 text-[11px] font-mono text-zinc-500">
        <div className="max-w-[1540px] mx-auto flex items-center justify-between">
          <span>NAOMI // COMMERCIAL INTELLIGENCE CORE • PEER-REVIEWED METHODOLOGY</span>
          <a
            href="https://github.com/princexpoddar/NAOMI"
            target="_blank"
            rel="noreferrer"
            className="text-zinc-400 hover:text-white transition-colors"
          >
            REPOSITORY
          </a>
        </div>
      </footer>
    </div>
  );
};

export default App;
