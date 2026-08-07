import { ScanSearch, Upload } from "lucide-react";
import { LinkButton } from "@/components/layout/link-button";

export function AnalyzeActions() {
  return (
    <section aria-label="Analyze actions" className="flex flex-col gap-3">
      <LinkButton href="/result" variant="primary" fullWidth>
        <ScanSearch className="h-5 w-5" strokeWidth={1.5} />
        Analyze Material
      </LinkButton>
      <button
        type="button"
        className="inline-flex min-h-[56px] w-full items-center justify-center gap-2.5 rounded-2xl border border-white/8 bg-[#161616] px-6 text-base font-medium text-white transition-all duration-150 ease-out hover:border-white/12 hover:bg-[#202020] active:scale-[0.98]"
      >
        <Upload className="h-5 w-5" strokeWidth={1.5} />
        Upload Image
      </button>
    </section>
  );
}
