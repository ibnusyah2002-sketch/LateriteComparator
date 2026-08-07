import type { DescriptionAttribute } from "@/types/result";

interface DescriptionCardProps {
  attribute: DescriptionAttribute;
}

export function DescriptionCard({ attribute }: DescriptionCardProps) {
  return (
    <article className="rounded-[18px] border border-white/8 bg-[#161616] p-4">
      <p className="text-[10px] font-medium uppercase tracking-wide text-[#9CA3AF]">
        {attribute.label}
      </p>
      <p className="mt-1.5 text-sm leading-relaxed text-white">
        {attribute.value}
      </p>
    </article>
  );
}
