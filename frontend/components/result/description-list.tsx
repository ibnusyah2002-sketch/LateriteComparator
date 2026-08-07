import type { DescriptionAttribute } from "@/types/result";
import { DescriptionCard } from "@/components/result/description-card";

interface DescriptionListProps {
  attributes: DescriptionAttribute[];
}

export function DescriptionList({ attributes }: DescriptionListProps) {
  return (
    <section aria-label="Material description">
      <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-[#9CA3AF]">
        Description
      </h2>
      <div className="flex flex-col gap-3">
        {attributes.map((attribute) => (
          <DescriptionCard key={attribute.label} attribute={attribute} />
        ))}
      </div>
    </section>
  );
}
