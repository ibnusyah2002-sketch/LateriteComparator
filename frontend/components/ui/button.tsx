import { cn } from "@/lib/utils";

type ButtonVariant = "primary" | "secondary";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  fullWidth?: boolean;
}

const variantStyles: Record<ButtonVariant, string> = {
  primary:
    "bg-lcgc-primary text-white hover:bg-lcgc-primary-hover active:bg-lcgc-primary-hover",
  secondary:
    "bg-lcgc-surface text-lcgc-text-primary border border-lcgc-border hover:bg-lcgc-surface-hover active:bg-lcgc-surface-hover",
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
        "inline-flex min-h-14 items-center justify-center gap-2 rounded-[var(--radius-button)] px-6 text-base font-medium transition-colors duration-150",
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
