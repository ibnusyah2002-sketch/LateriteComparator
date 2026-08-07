import { RECENT_SCANS_DUMMY } from "@/constants/recentScans";
import { ScanCard } from "@/components/home/scan-card";

export function RecentScan() {
  return (
    <section aria-label="Recent scans">
      <h2 className="mb-3 text-base font-bold text-white">Recent Scan</h2>
      <div className="-mx-4 flex gap-3 overflow-x-auto px-4 pb-1 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
        {RECENT_SCANS_DUMMY.map((scan) => (
          <ScanCard key={scan.id} scan={scan} />
        ))}
      </div>
    </section>
  );
}
