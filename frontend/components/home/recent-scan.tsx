import { Clock, History, TrendingUp } from "lucide-react";

const recentScans = [
  {
    code: "RB4-015",
    zone: "Earthy Saprolite",
    similarity: "94%",
    time: "Today",
  },
  {
    code: "SP2-042",
    zone: "Rocky Saprolite",
    similarity: "87%",
    time: "Yesterday",
  },
  {
    code: "LT3-008",
    zone: "Limonite",
    similarity: "82%",
    time: "2 days ago",
  },
];

export function RecentScan() {
  return (
    <section className="space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold text-white">Recent Scan</p>
          <p className="text-xs text-white/40">Latest comparator activity</p>
        </div>

        <div className="flex h-9 w-9 items-center justify-center rounded-full border border-white/10 bg-white/5">
          <History className="h-4 w-4 text-[#4CAF50]" />
        </div>
      </div>

      <div className="space-y-2">
        {recentScans.map((scan) => (
          <div
            key={scan.code}
            className="flex items-center justify-between rounded-2xl border border-white/10 bg-[#131816] px-4 py-3 transition hover:bg-white/[0.06]"
          >
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <p className="text-sm font-semibold text-white">{scan.code}</p>
                <span className="rounded-full border border-[#4CAF50]/20 bg-[#4CAF50]/10 px-2 py-0.5 text-[10px] font-medium text-[#4CAF50]">
                  {scan.zone}
                </span>
              </div>

              <div className="mt-1 flex items-center gap-1.5 text-xs text-white/40">
                <Clock className="h-3 w-3" />
                <span>{scan.time}</span>
              </div>
            </div>

            <div className="flex items-center gap-1.5 rounded-full bg-black/30 px-3 py-1.5">
              <TrendingUp className="h-3.5 w-3.5 text-[#4CAF50]" />
              <span className="text-sm font-semibold text-[#4CAF50]">
                {scan.similarity}
              </span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default RecentScan;