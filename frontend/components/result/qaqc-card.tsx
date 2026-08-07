interface QaqcCardProps {
  label: string;
  value: number;
  unit?: string;
}

export function QaqcCard({ label, value, unit = "%" }: QaqcCardProps) {
  return (
    <article className="rounded-[18px] border border-white/8 bg-[#161616] p-3">
      <p className="text-[10px] font-medium uppercase tracking-wide text-[#9CA3AF]">
        {label}
      </p>
      <p className="mt-1 text-lg font-bold text-white">
        {value}
        <span className="ml-0.5 text-sm font-medium text-[#9CA3AF]">
          {unit}
        </span>
      </p>
    </article>
  );
}
