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
      className="pointer-events-none fixed inset-x-0 bottom-0 z-50 px-4 pb-4 pt-2"
    >
      <div className="pointer-events-auto mx-auto max-w-[640px] rounded-[18px] border border-white/8 bg-[#161616]/95 shadow-[0_8px_32px_rgba(0,0,0,0.45)] backdrop-blur-md">
        <div className="flex items-center justify-around px-2 py-1.5">
          {navItems.map(({ label, icon: Icon, active }) => (
            <button
              key={label}
              type="button"
              aria-current={active ? "page" : undefined}
              className={cn(
                "flex min-h-14 min-w-[72px] flex-col items-center justify-center gap-1 rounded-xl px-3 transition-all duration-150",
                active
                  ? "text-[#4CAF50]"
                  : "text-[#9CA3AF] hover:text-white active:scale-95",
              )}
            >
              <Icon className="h-5 w-5" strokeWidth={1.5} />
              <span className="text-[11px] font-medium">{label}</span>
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
}
