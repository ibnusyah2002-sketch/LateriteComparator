import { Camera } from "lucide-react";
import { ScannerOverlay } from "@/components/home/scanner-overlay";
import styles from "@/components/home/home-animations.module.css";

export function CameraPreview() {
  return (
    <section
      aria-label="Camera preview"
      className={`relative flex min-h-[min(60vh,420px)] flex-col items-center justify-center overflow-hidden rounded-[18px] border border-white/8 bg-[#161616] ${styles.scannerGlow}`}
    >
      <ScannerOverlay />

      <div className="relative z-10 flex flex-col items-center px-6 text-center">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full border border-white/8 bg-[#0B0F0C]/80">
          <Camera
            className="h-8 w-8 text-[#66BB6A]"
            strokeWidth={1.5}
          />
        </div>
        <p className="text-sm font-medium text-white">Camera Preview</p>
        <p className="mt-3 max-w-[260px] text-xs leading-relaxed text-[#9CA3AF]">
          Place the laterite material inside the scanner area before capture.
        </p>
      </div>
    </section>
  );
}
