import { ScanCard } from "@/components/home/scan-card";

const PLACEHOLDER_COUNT = 3;

export function RecentScan() {
  return (
    <section aria-label="Recent scans">
      <h2 className="mb-3 text-base font-bold">Recent Scan</h2>
      <div className="-mx-4 flex gap-3 overflow-x-auto px-4 pb-1 scrollbar-none">
        {Array.from({ length: PLACEHOLDER_COUNT }, (_, index) => (
          <ScanCard key={index} />
        ))}
      </div>
    </section>
  );
}
