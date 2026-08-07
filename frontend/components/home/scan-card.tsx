import { ImageIcon } from "lucide-react";

export function ScanCard() {
  return (
    <article className="flex w-[140px] shrink-0 flex-col overflow-hidden rounded-[var(--radius-card)] border border-lcgc-border bg-lcgc-surface">
      <div className="flex aspect-square items-center justify-center bg-lcgc-background">
        <ImageIcon
          className="h-8 w-8 text-lcgc-text-secondary/40"
          strokeWidth={1.5}
        />
      </div>
      <div className="flex flex-col gap-1.5 p-3">
        <div>
          <p className="text-[10px] uppercase tracking-wide text-lcgc-text-secondary">
            Material Code
          </p>
          <p className="text-sm font-medium text-lcgc-text-secondary">—</p>
        </div>
        <div>
          <p className="text-[10px] uppercase tracking-wide text-lcgc-text-secondary">
            Similarity
          </p>
          <p className="text-sm font-medium text-lcgc-text-secondary">—</p>
        </div>
        <div>
          <p className="text-[10px] uppercase tracking-wide text-lcgc-text-secondary">
            Date
          </p>
          <p className="text-xs text-lcgc-text-secondary">—</p>
        </div>
      </div>
    </article>
  );
}
