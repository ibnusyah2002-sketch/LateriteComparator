import { Camera } from "lucide-react";

export function CameraPreview() {
  return (
    <section
      aria-label="Camera preview"
      className="relative flex min-h-[min(60vh,420px)] flex-col items-center justify-center rounded-[var(--radius-image)] border border-lcgc-border bg-lcgc-surface"
    >
      <Camera
        className="mb-3 h-10 w-10 text-lcgc-text-secondary"
        strokeWidth={1.5}
      />
      <p className="text-sm font-medium text-lcgc-text-secondary">
        Camera Preview
      </p>
    </section>
  );
}
