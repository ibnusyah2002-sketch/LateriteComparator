"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Database, Loader2, ScanSearch, Sparkles } from "lucide-react";
import { SCAN_SESSION_IMAGE_KEY } from "@/constants/scan";

const analysisStages = [
  {
    title: "Analyzing Material Image",
    description: "Reading visual texture, color tone, and surface pattern.",
    icon: ScanSearch,
  },
  {
    title: "Searching Comparator Database",
    description: "Finding the closest visual match from comparator samples.",
    icon: Database,
  },
  {
    title: "Generating Result",
    description: "Preparing similarity score, QAQC data, and material summary.",
    icon: Sparkles,
  },
];

export default function AnalysisPage() {
  const router = useRouter();
  const [activeStage, setActiveStage] = useState(0);
  const [scanImage, setScanImage] = useState<string | null>(null);

  useEffect(() => {
    const storedImage = sessionStorage.getItem(SCAN_SESSION_IMAGE_KEY);

    if (!storedImage) {
      router.replace("/");
      return;
    }

    setScanImage(storedImage);

    const stageInterval = window.setInterval(() => {
      setActiveStage((currentStage) =>
        currentStage < analysisStages.length - 1
          ? currentStage + 1
          : currentStage
      );
    }, 950);

    const resultTimeout = window.setTimeout(() => {
      router.replace("/result");
    }, 3200);

    return () => {
      window.clearInterval(stageInterval);
      window.clearTimeout(resultTimeout);
    };
  }, [router]);

  return (
    <main className="min-h-screen bg-[#0B0F0C] px-4 py-6 text-white">
      <div className="mx-auto flex min-h-[calc(100vh-3rem)] max-w-[430px] flex-col justify-center space-y-6">
        <section className="rounded-[28px] border border-white/10 bg-[#131816] p-5 shadow-2xl">
          <div className="flex items-center gap-4">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-[#4CAF50]/30 bg-[#4CAF50]/10">
              <Loader2 className="h-7 w-7 animate-spin text-[#4CAF50]" />
            </div>

            <div>
              <p className="text-sm font-medium uppercase tracking-[0.25em] text-[#4CAF50]">
                LCGC Analysis
              </p>
              <h1 className="mt-1 text-2xl font-semibold tracking-tight text-white">
                Comparing Material
              </h1>
            </div>
          </div>

          <p className="mt-4 text-sm leading-6 text-white/60">
            Your scanned material is being visually compared against the local
            comparator database.
          </p>
        </section>

        {scanImage && (
          <section className="rounded-[28px] border border-white/10 bg-[#131816] p-4">
            <div className="overflow-hidden rounded-[22px] bg-black">
              <img
                src={scanImage}
                alt="Material prepared for analysis"
                className="h-64 w-full object-cover"
              />
            </div>
          </section>
        )}

        <section className="space-y-3">
          {analysisStages.map((stage, index) => {
            const Icon = stage.icon;
            const isActive = index === activeStage;
            const isDone = index < activeStage;

            return (
              <div
                key={stage.title}
                className={`rounded-2xl border p-4 transition ${
                  isActive
                    ? "border-[#4CAF50]/40 bg-[#4CAF50]/10"
                    : "border-white/10 bg-[#131816]"
                }`}
              >
                <div className="flex items-start gap-3">
                  <div
                    className={`mt-0.5 flex h-9 w-9 items-center justify-center rounded-xl border ${
                      isDone || isActive
                        ? "border-[#4CAF50]/40 bg-[#4CAF50]/10 text-[#4CAF50]"
                        : "border-white/10 bg-white/5 text-white/40"
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                  </div>

                  <div>
                    <p className="font-medium text-white">{stage.title}</p>
                    <p className="mt-1 text-sm leading-5 text-white/50">
                      {stage.description}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </section>
      </div>
    </main>
  );
}