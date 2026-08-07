import Link from "next/link";
import { ChevronLeft } from "lucide-react";

interface BackHeaderProps {
  title: string;
  backHref?: string;
}

export function BackHeader({ title, backHref = "/" }: BackHeaderProps) {
  return (
    <header className="flex items-center gap-2 px-4 pt-6 pb-4">
      <Link
        href={backHref}
        aria-label="Go back"
        className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-white/8 bg-[#161616] text-[#9CA3AF] transition-all duration-150 hover:border-white/12 hover:text-white active:scale-95"
      >
        <ChevronLeft className="h-5 w-5" strokeWidth={1.5} />
      </Link>
      <h1 className="text-lg font-bold text-white">{title}</h1>
    </header>
  );
}
