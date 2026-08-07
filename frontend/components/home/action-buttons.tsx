import { Camera, Upload } from "lucide-react";
import { LinkButton } from "@/components/layout/link-button";

export function ActionButtons() {
  return (
    <section aria-label="Scan actions" className="flex flex-col gap-3">
      <LinkButton href="/scan" variant="primary" fullWidth>
        <Camera className="h-5 w-5" strokeWidth={1.5} />
        Capture Material
      </LinkButton>
      <LinkButton href="/scan" variant="secondary" fullWidth>
        <Upload className="h-5 w-5" strokeWidth={1.5} />
        Upload Image
      </LinkButton>
    </section>
  );
}
