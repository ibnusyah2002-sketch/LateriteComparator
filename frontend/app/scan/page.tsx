import { PageShell } from "@/components/layout/page-shell";
import { ScanHeader } from "@/components/scan/scan-header";
import { ScanFrame } from "@/components/scan/scan-frame";
import { AnalyzeActions } from "@/components/scan/analyze-actions";
import styles from "@/components/home/home-animations.module.css";

export default function ScanPage() {
  return (
    <PageShell className={styles.fadeIn}>
      <ScanHeader />

      <main className="flex flex-1 flex-col gap-6 px-4 pb-8">
        <ScanFrame />
        <AnalyzeActions />
      </main>
    </PageShell>
  );
}
