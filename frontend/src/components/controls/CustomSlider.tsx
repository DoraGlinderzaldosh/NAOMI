import React from "react";

interface CustomSliderProps {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  unit?: string;
  formatSign?: boolean;
  onChange: (val: number) => void;
}

export const CustomSlider: React.FC<CustomSliderProps> = ({
  label,
  value,
  min,
  max,
  step,
  unit = "%",
  formatSign = true,
  onChange,
}) => {
  const percentage = ((value - min) / (max - min)) * 100;
  const sign = formatSign && value > 0 ? "+" : "";

  return (
    <div className="flex flex-col gap-1 py-1">
      <div className="flex items-center justify-between text-xs font-mono">
        <span className="text-zinc-300 font-sans text-xs">{label}</span>
        <span className="text-[11px] font-mono tabular-nums text-zinc-100 bg-[#121215] border border-[#27272A] px-1.5 py-0.2 rounded">
          {sign}{value}{unit}
        </span>
      </div>

      <div className="relative flex items-center py-1">
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => onChange(parseFloat(e.target.value))}
          className="w-full"
          style={{
            background: `linear-gradient(to right, #71717A 0%, #71717A ${percentage}%, #18181B ${percentage}%, #18181B 100%)`,
          }}
        />
      </div>
    </div>
  );
};
