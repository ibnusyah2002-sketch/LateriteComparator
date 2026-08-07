import { Camera } from "lucide-react";
import { LinkButton } from "@/components/layout/link-button";

export function ScanAgainAction() {
  return (
    <section aria-label="Scan again" className="pt-2">
      <LinkButton href="/scan" variant="primary" fullWidth>
        <Camera className="h-5 w-5" strokeWidth={1.5} />
        Scan Again
      </LinkButton>
    </section>
  );
}
