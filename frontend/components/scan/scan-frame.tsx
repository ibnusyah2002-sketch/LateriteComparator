import { Camera } from "lucide-react";
import { ScannerOverlay } from "@/components/home/scanner-overlay";
import styles from "@/components/home/home-animations.module.css";

export function ScanFrame() {
  return (
    <section
      aria-label="Scan frame"
      className={`relative flex min-h-[min(55vh,400px)] flex-col items-center justify-center overflow-hidden rounded-[18px] border border-white/8 bg-[#161616] ${styles.scannerGlow}`}
    >
      <ScannerOverlay />

      <div className="relative z-10 flex flex-col items-center px-6 text-center">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full border border-white/8 bg-[#0B0F0C]/80">
          <Camera className="h-8 w-8 text-[#66BB6A]" strokeWidth={1.5} />
        </div>
        <p className="max-w-[280px] text-sm leading-relaxed text-[#9CA3AF]">
          Position the laterite material inside the frame.
        </p>
      </div>
    </section>
  );
}
