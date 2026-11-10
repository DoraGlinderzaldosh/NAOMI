import React from "react";
import { cn } from "../../lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  highlight?: boolean;
}

export const SpotlightCard: React.FC<CardProps> = ({
  children,
  className,
  highlight = false,
  ...props
}) => {
  return (
    <div
      className={cn(
        "rounded-lg border bg-[#070709] p-4 transition-colors",
        highlight
          ? "border-zinc-500"
          : "border-[#1F1F23] hover:border-[#2E2E33]",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
