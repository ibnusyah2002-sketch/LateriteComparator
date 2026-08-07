import { PageShell } from "@/components/layout/page-shell";
import { BottomNav } from "@/components/layout/bottom-nav";
import { HistoryList } from "@/components/history/history-list";
import styles from "@/components/home/home-animations.module.css";

export default function HistoryPage() {
  return (
    <PageShell className={styles.fadeIn}>
      <header className="px-4 pt-6 pb-4">
        <h1 className="text-lg font-bold text-white">Scan History</h1>
        <p className="mt-1 text-sm text-[#9CA3AF]">
          Recent comparator scan records
        </p>
      </header>

      <main className="flex flex-1 flex-col px-4 pb-32">
        <HistoryList />
      </main>

      <BottomNav />
    </PageShell>
  );
}
