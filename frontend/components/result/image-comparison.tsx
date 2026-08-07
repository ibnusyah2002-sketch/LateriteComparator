import { ImageIcon } from "lucide-react";

export function ImageComparison() {
  return (
    <section aria-label="Image comparison">
      <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-[#9CA3AF]">
        Comparison
      </h2>
      <div className="grid grid-cols-2 gap-3">
        <figure className="overflow-hidden rounded-[18px] border border-white/8 bg-[#161616]">
          <div className="flex aspect-square items-center justify-center bg-[#0B0F0C]">
            <ImageIcon
              className="h-10 w-10 text-[#9CA3AF]/35"
              strokeWidth={1.5}
            />
          </div>
          <figcaption className="border-t border-white/8 px-3 py-2 text-center text-xs font-medium text-[#9CA3AF]">
            Your Scan
          </figcaption>
        </figure>
        <figure className="overflow-hidden rounded-[18px] border border-white/8 bg-[#161616]">
          <div className="flex aspect-square items-center justify-center bg-[#0B0F0C]">
            <ImageIcon
              className="h-10 w-10 text-[#9CA3AF]/35"
              strokeWidth={1.5}
            />
          </div>
          <figcaption className="border-t border-white/8 px-3 py-2 text-center text-xs font-medium text-[#9CA3AF]">
            Comparator
          </figcaption>
        </figure>
      </div>
    </section>
  );
}
