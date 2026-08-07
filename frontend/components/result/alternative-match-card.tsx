import type { AlternativeMatch } from "@/types/result";
import { GitCompare } from "lucide-react";

interface AlternativeMatchCardProps {
  match: AlternativeMatch;
}

export function AlternativeMatchCard({ match }: AlternativeMatchCardProps) {
  return (
    <article className="flex items-center justify-between rounded-[18px] border border-white/8 bg-[#161616] px-4 py-3 transition-colors duration-150 hover:border-white/12 hover:bg-[#1a1a1a]">
      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/8 bg-[#0B0F0C]">
          <GitCompare className="h-4 w-4 text-[#66BB6A]" strokeWidth={1.5} />
        </div>
        <div>
          <p className="text-sm font-medium text-white">{match.code}</p>
          <p className="text-xs text-[#9CA3AF]">Comparator sample</p>
        </div>
      </div>
      <p className="text-sm font-bold text-[#66BB6A]">{match.similarity}%</p>
    </article>
  );
}
