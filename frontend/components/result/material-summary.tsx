import type { ComparatorResult } from "@/types/result";

interface MaterialSummaryProps {
  result: ComparatorResult;
}

export function MaterialSummary({ result }: MaterialSummaryProps) {
  return (
    <section
      aria-label="Material summary"
      className="rounded-[18px] border border-white/8 bg-[#161616] p-4"
    >
      <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-[#9CA3AF]">
        Material Summary
      </h2>
      <dl className="grid gap-3">
        <div className="flex items-center justify-between gap-4">
          <dt className="text-sm text-[#9CA3AF]">Material Code</dt>
          <dd className="text-sm font-bold text-white">{result.code}</dd>
        </div>
        <div className="flex items-center justify-between gap-4">
          <dt className="text-sm text-[#9CA3AF]">Zone</dt>
          <dd className="text-right text-sm font-medium text-white">
            {result.zone}
          </dd>
        </div>
        <div className="flex items-center justify-between gap-4">
          <dt className="text-sm text-[#9CA3AF]">Color</dt>
          <dd className="text-right text-sm font-medium text-white">
            {result.color}
          </dd>
        </div>
      </dl>
    </section>
  );
}
