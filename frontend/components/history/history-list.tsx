import { RECENT_SCANS_DUMMY } from "@/constants/recentScans";
import { HistoryCard } from "@/components/history/history-card";

export function HistoryList() {
  return (
    <section aria-label="Scan history" className="flex flex-col gap-3">
      {RECENT_SCANS_DUMMY.map((scan) => (
        <HistoryCard key={scan.id} scan={scan} />
      ))}
    </section>
  );
}
