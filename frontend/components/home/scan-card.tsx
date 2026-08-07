import { ImageIcon } from "lucide-react";
import type { RecentScanItem } from "@/types/scan";

interface ScanCardProps {
  scan: RecentScanItem;
}

export function ScanCard({ scan }: ScanCardProps) {
  return (
    <article className="flex w-[148px] shrink-0 flex-col overflow-hidden rounded-[18px] border border-white/8 bg-[#161616] transition-colors duration-150 hover:border-white/12 hover:bg-[#1a1a1a]">
      <div className="flex aspect-square items-center justify-center bg-[#0B0F0C]">
        <ImageIcon
          className="h-8 w-8 text-[#9CA3AF]/35"
          strokeWidth={1.5}
        />
      </div>
      <div className="flex flex-col gap-2 p-3">
        <div>
          <p className="text-[10px] uppercase tracking-wide text-[#9CA3AF]">
            Material Code
          </p>
          <p className="truncate text-sm font-medium text-white">
            {scan.materialCode}
          </p>
        </div>
        <div>
          <p className="text-[10px] uppercase tracking-wide text-[#9CA3AF]">
            Similarity
          </p>
          <p className="text-sm font-medium text-[#66BB6A]">
            {scan.similarity}%
          </p>
        </div>
        <div>
          <p className="text-[10px] uppercase tracking-wide text-[#9CA3AF]">
            Date
          </p>
          <p className="text-xs text-[#9CA3AF]">{scan.date}</p>
        </div>
      </div>
    </article>
  );
}
