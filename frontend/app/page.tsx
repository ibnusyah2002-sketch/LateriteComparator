import { PageShell } from "@/components/layout/page-shell";
import { BottomNav } from "@/components/layout/bottom-nav";
import { Header } from "@/components/layout/header";
import { CameraPreview } from "@/components/home/camera-preview";
import { ActionButtons } from "@/components/home/action-buttons";
import { RecentScan } from "@/components/home/recent-scan";
import styles from "@/components/home/home-animations.module.css";

export default function HomePage() {
  return (
    <PageShell className={styles.fadeIn}>
      <Header />

      <main className="flex flex-1 flex-col gap-6 px-4 pb-32">
        <CameraPreview />
        <ActionButtons />
        <RecentScan />
      </main>

      <BottomNav />
    </PageShell>
  );
}
