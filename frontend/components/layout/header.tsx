import { Logo } from "@/components/ui/logo";

export function Header() {
  return (
    <header className="px-4 pt-6 pb-4">
      <div className="flex items-center gap-3">
        <Logo className="h-11 w-11 shrink-0" />
        <div className="min-w-0">
          <h1 className="text-lg font-bold leading-tight tracking-tight">
            Laterite Comparator
          </h1>
          <p className="text-sm font-medium text-lcgc-primary">Grade Control</p>
        </div>
      </div>
      <p className="mt-3 text-sm text-lcgc-text-secondary">
        Scan. Compare. Identify.
      </p>
    </header>
  );
}
