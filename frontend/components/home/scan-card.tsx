import { CameraPreview } from "./camera-preview";

export function ScanCard() {
  return (
    <section className="rounded-[28px] border border-white/10 bg-[#131816] p-4 shadow-2xl">
      <CameraPreview />

      <div className="mt-4 text-center">
        <p className="text-sm font-medium text-white/70">
          Position the laterite material inside the scanner frame.
        </p>
        <p className="mt-2 text-xs leading-5 text-white/40">
          Capture or upload one material image, then continue to visual
          comparator analysis.
        </p>
      </div>
    </section>
  );
}

export default ScanCard;