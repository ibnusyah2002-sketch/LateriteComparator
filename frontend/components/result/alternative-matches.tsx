import type { AlternativeMatch } from "@/types/result";
import { AlternativeMatchCard } from "@/components/result/alternative-match-card";

interface AlternativeMatchesProps {
  matches: AlternativeMatch[];
}

export function AlternativeMatches({ matches }: AlternativeMatchesProps) {
  return (
    <section aria-label="Alternative matches">
      <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-[#9CA3AF]">
        Alternative Matches
      </h2>
      <div className="flex flex-col gap-2">
        {matches.map((match) => (
          <AlternativeMatchCard key={match.code} match={match} />
        ))}
      </div>
    </section>
  );
}
