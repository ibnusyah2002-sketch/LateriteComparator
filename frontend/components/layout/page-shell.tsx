import { cn } from "@/lib/utils";

interface PageShellProps {
  children: React.ReactNode;
  className?: string;
}

export function PageShell({ children, className }: PageShellProps) {
  return (
    <div
      className={cn(
        "mx-auto flex min-h-screen max-w-[640px] flex-col bg-[#0B0F0C]",
        className,
      )}
    >
      {children}
    </div>
  );
}
