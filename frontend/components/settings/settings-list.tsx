import { SettingsItem } from "@/components/settings/settings-item";

const SETTINGS = [
  { label: "App Name", value: "Laterite Comparator" },
  { label: "Edition", value: "Grade Control" },
  { label: "Version", value: "MVP 0.1" },
  { label: "Data Source", value: "Local Comparator Database" },
  { label: "Theme", value: "Dark Industrial" },
] as const;

export function SettingsList() {
  return (
    <section
      aria-label="Application settings"
      className="overflow-hidden rounded-[18px] border border-white/8 bg-[#161616]"
    >
      <dl>
        {SETTINGS.map((item) => (
          <SettingsItem key={item.label} label={item.label} value={item.value} />
        ))}
      </dl>
    </section>
  );
}
