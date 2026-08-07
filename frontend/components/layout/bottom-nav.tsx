import { History, Home, Settings } from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { label: "Home", icon: Home, active: true },
  { label: "History", icon: History, active: false },
  { label: "Settings", icon: Settings, active: false },
] as const;

export function BottomNav() {
  return (
    <nav
      aria-label="Main navigation"
      className="fixed inset-x-0 bottom-0 z-50 border-t border-lcgc-border bg-lcgc-surface/95 backdrop-blur-sm"
    >
      <div className="mx-auto flex max-w-[640px] items-center justify-around px-4 py-2">
        {navItems.map(({ label, icon: Icon, active }) => (
          <button
            key={label}
            type="button"
            aria-current={active ? "page" : undefined}
            className={cn(
              "flex min-h-14 min-w-[72px] flex-col items-center justify-center gap-1 rounded-[var(--radius-input)] px-3 transition-colors",
              active
                ? "text-lcgc-primary"
                : "text-lcgc-text-secondary hover:text-lcgc-text-primary",
            )}
          >
            <Icon className="h-5 w-5" strokeWidth={1.5} />
            <span className="text-[11px] font-medium">{label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
}
