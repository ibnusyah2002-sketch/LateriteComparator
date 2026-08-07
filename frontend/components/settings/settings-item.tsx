interface SettingsItemProps {
  label: string;
  value: string;
}

export function SettingsItem({ label, value }: SettingsItemProps) {
  return (
    <div className="flex items-center justify-between gap-4 border-b border-white/8 px-4 py-3.5 last:border-b-0">
      <dt className="text-sm text-[#9CA3AF]">{label}</dt>
      <dd className="text-right text-sm font-medium text-white">{value}</dd>
    </div>
  );
}
