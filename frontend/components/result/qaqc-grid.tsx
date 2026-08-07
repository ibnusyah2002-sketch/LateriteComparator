import type { QaqcValues } from "@/types/result";
import { QaqcCard } from "@/components/result/qaqc-card";

interface QaqcGridProps {
  qaqc: QaqcValues;
}

const QAQC_FIELDS: { key: keyof QaqcValues; label: string }[] = [
  { key: "ni", label: "Ni" },
  { key: "co", label: "Co" },
  { key: "fe", label: "Fe" },
  { key: "mgo", label: "MgO" },
  { key: "sio2", label: "SiO2" },
];

export function QaqcGrid({ qaqc }: QaqcGridProps) {
  return (
    <section aria-label="QAQC data">
      <h2 className="mb-3 text-sm font-bold uppercase tracking-wide text-[#9CA3AF]">
        QAQC
      </h2>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
        {QAQC_FIELDS.map(({ key, label }) => (
          <QaqcCard key={key} label={label} value={qaqc[key]} />
        ))}
      </div>
    </section>
  );
}
