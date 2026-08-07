import { PageShell } from "@/components/layout/page-shell";
import { BottomNav } from "@/components/layout/bottom-nav";
import { SettingsList } from "@/components/settings/settings-list";
import styles from "@/components/home/home-animations.module.css";

export default function SettingsPage() {
  return (
    <PageShell className={styles.fadeIn}>
      <header className="px-4 pt-6 pb-4">
        <h1 className="text-lg font-bold text-white">Settings</h1>
        <p className="mt-1 text-sm text-[#9CA3AF]">
          Application configuration
        </p>
      </header>

      <main className="flex flex-1 flex-col px-4 pb-32">
        <SettingsList />
      </main>

      <BottomNav />
    </PageShell>
  );
}
