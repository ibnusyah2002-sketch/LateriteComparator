"use client";

import { cn } from "@/lib/utils";

type ButtonVariant = "primary" | "secondary";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  fullWidth?: boolean;
}

const variantStyles: Record<ButtonVariant, string> = {
  primary:
    "bg-[#4CAF50] text-white hover:bg-[#43A047] hover:brightness-105 active:scale-[0.98] active:bg-[#388E3C]",
  secondary:
    "border border-white/8 bg-[#161616] text-white hover:bg-[#202020] hover:border-white/12 active:scale-[0.98] active:bg-[#1a1a1a]",
};

export function Button({
  variant = "primary",
  fullWidth = false,
  className,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      type="button"
      className={cn(
        "inline-flex min-h-[56px] items-center justify-center gap-2.5 rounded-2xl px-6 text-base font-medium transition-all duration-150 ease-out",
        variantStyles[variant],
        fullWidth && "w-full",
        className,
      )}
      {...props}
    >
      {children}
    </button>
  );
}
