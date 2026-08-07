import { ImageIcon } from "lucide-react";
import type { RecentScanItem } from "@/types/scan";

interface HistoryCardProps {
  scan: RecentScanItem;
}

export function HistoryCard({ scan }: HistoryCardProps) {
  return (
    <article className="flex gap-3 rounded-[18px] border border-white/8 bg-[#161616] p-3 transition-colors duration-150 hover:border-white/12 hover:bg-[#1a1a1a]">
      <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-[14px] border border-white/8 bg-[#0B0F0C]">
        <ImageIcon
          className="h-7 w-7 text-[#9CA3AF]/35"
          strokeWidth={1.5}
        />
      </div>
      <div className="flex min-w-0 flex-1 flex-col justify-center gap-1">
        <p className="truncate text-sm font-bold text-white">
          {scan.materialCode}
        </p>
        <p className="text-xs text-[#9CA3AF]">
          Similarity:{" "}
          <span className="font-medium text-[#66BB6A]">{scan.similarity}%</span>
        </p>
        <p className="text-xs text-[#9CA3AF]">{scan.date}</p>
      </div>
    </article>
  );
}
