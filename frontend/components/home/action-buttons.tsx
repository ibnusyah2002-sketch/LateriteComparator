"use client";

import { Camera, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";

export function ActionButtons() {
  return (
    <section aria-label="Scan actions" className="flex flex-col gap-3">
      <Button variant="primary" fullWidth>
        <Camera className="h-5 w-5" strokeWidth={1.5} />
        Capture
      </Button>
      <Button variant="secondary" fullWidth>
        <Upload className="h-5 w-5" strokeWidth={1.5} />
        Upload Image
      </Button>
    </section>
  );
}
