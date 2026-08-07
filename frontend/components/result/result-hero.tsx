import type { ComparatorResult } from "@/types/result";

interface ResultHeroProps {
  result: ComparatorResult;
}

export function ResultHero({ result }: ResultHeroProps) {
  return (
    <section aria-label="Comparator match summary" className="text-center">
      <p className="text-5xl font-bold tracking-tight text-[#66BB6A]">
        {result.similarity}%
      </p>
      <p className="mt-1 text-sm font-medium uppercase tracking-wide text-[#9CA3AF]">
        Visual Similarity
      </p>
      <span className="mt-3 inline-flex rounded-full border border-[#4CAF50]/30 bg-[#4CAF50]/10 px-3 py-1 text-xs font-medium text-[#66BB6A]">
        {result.confidence} Confidence
      </span>
      <p className="mt-4 text-sm leading-relaxed text-[#9CA3AF]">
        This scanned material is visually similar to comparator sample{" "}
        <span className="font-medium text-white">{result.code}</span>.
      </p>
    </section>
  );
}
