import { Header } from "@/components/layout/header";
import { BottomNav } from "@/components/layout/bottom-nav";
import { CameraPreview } from "@/components/home/camera-preview";
import { ActionButtons } from "@/components/home/action-buttons";
import { RecentScan } from "@/components/home/recent-scan";

export default function HomePage() {
  return (
    <div className="mx-auto flex min-h-screen max-w-[640px] flex-col">
      <Header />

      <main className="flex flex-1 flex-col gap-6 px-4 pb-28">
        <CameraPreview />
        <ActionButtons />
        <RecentScan />
      </main>

      <BottomNav />
    </div>
  );
}
