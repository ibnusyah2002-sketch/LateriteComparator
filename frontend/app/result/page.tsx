"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  ArrowLeft,
  Camera,
  Database,
  ImageIcon,
  RefreshCcw,
  ShieldCheck,
} from "lucide-react";
import { useRouter } from "next/navigation";

import { fetchMockAnalysis, submitAnalysisImage } from "@/services/analysis";
import {
  SCAN_SESSION_CREATED_AT_KEY,
  SCAN_SESSION_IMAGE_KEY,
  SCAN_SESSION_SOURCE_KEY,
} from "@/constants/scan";
import type { AnalysisPayload, TopCandidate } from "@/types/analysis";

type ScanSession = {
  image: string | null;
  source: string | null;
  createdAt: string | null;
};

export default function ResultPage() {
  const router = useRouter();

  const [scanSession, setScanSession] = useState<ScanSession>({
    image: null,
    source: null,
    createdAt: null,
  });
  const [analysis, setAnalysis] = useState<AnalysisPayload | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const scannedAtLabel = useMemo(() => {
    if (!scanSession.createdAt) {
      return "Current scan";
    }

    try {
      return new Intl.DateTimeFormat("id-ID", {
        dateStyle: "medium",
        timeStyle: "short",
      }).format(new Date(scanSession.createdAt));
    } catch {
      return "Current scan";
    }
  }, [scanSession.createdAt]);

  const alternativeCandidates = useMemo(() => {
    const candidates = analysis?.similarity.top_candidates ?? [];
    const matchedCode = analysis?.matched_sample.code;

    return candidates.filter((candidate) => candidate.code !== matchedCode);
  }, [analysis]);

  const loadBackendResult = useCallback(async (imageOverride?: string | null) => {
    try {
      setIsLoading(true);
      setErrorMessage(null);

      const imageForAnalysis =
        imageOverride ?? window.sessionStorage.getItem(SCAN_SESSION_IMAGE_KEY);
      const source =
        window.sessionStorage.getItem(SCAN_SESSION_SOURCE_KEY) ?? "unknown";

      const result = imageForAnalysis
        ? await submitAnalysisImage({
            imageDataUrl: imageForAnalysis,
            source,
          })
        : await fetchMockAnalysis("BG1 - 01");

      setAnalysis(result);
    } catch (error) {
      setAnalysis(null);
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Failed to load backend analysis result.",
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    const image = window.sessionStorage.getItem(SCAN_SESSION_IMAGE_KEY);
    const source = window.sessionStorage.getItem(SCAN_SESSION_SOURCE_KEY);
    const createdAt = window.sessionStorage.getItem(SCAN_SESSION_CREATED_AT_KEY);

    setScanSession({
      image,
      source,
      createdAt,
    });

    void loadBackendResult(image);
  }, [loadBackendResult]);

  function handleScanAgain() {
    window.sessionStorage.removeItem(SCAN_SESSION_IMAGE_KEY);
    window.sessionStorage.removeItem(SCAN_SESSION_SOURCE_KEY);
    window.sessionStorage.removeItem(SCAN_SESSION_CREATED_AT_KEY);

    router.push("/");
  }

  if (!scanSession.image && !isLoading && !analysis) {
    return (
      <main className="min-h-screen bg-[#0B0B0B] px-5 py-8 text-white">
        <section className="mx-auto flex min-h-[70vh] max-w-xl flex-col items-center justify-center text-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-white/[0.06]">
            <Camera className="h-7 w-7 text-neutral-400" />
          </div>

          <h1 className="mt-6 text-2xl font-semibold">No scan result yet</h1>
          <p className="mt-3 text-sm leading-6 text-neutral-400">
            Capture or upload a material photo first to generate a comparator
            result.
          </p>

          <button
            type="button"
            onClick={() => router.push("/")}
            className="mt-8 rounded-2xl bg-green-500 px-5 py-3 font-semibold text-black"
          >
            Back to Scanner
          </button>
        </section>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#0B0B0B] pb-24 text-white">
      <section className="mx-auto max-w-4xl px-5 py-6">
        <header className="flex items-center justify-between gap-4">
          <button
            type="button"
            onClick={() => router.push("/")}
            className="flex h-11 w-11 items-center justify-center rounded-full border border-white/10 bg-white/[0.04]"
            aria-label="Back to scanner"
          >
            <ArrowLeft className="h-5 w-5" />
          </button>

          <div className="text-right">
            <p className="text-xs uppercase tracking-[0.3em] text-green-400">
              LCGC Result
            </p>
            <h1 className="mt-1 text-xl font-semibold">Comparator Analysis</h1>
          </div>
        </header>

        {/* 1. Backend Connected Result */}
        <section className="mt-6 rounded-[2rem] border border-green-400/20 bg-green-400/10 p-4">
          <div className="flex items-center gap-2 text-sm text-green-200">
            <Database className="h-4 w-4 text-green-400" />
            <span>Backend connected result</span>
          </div>

          {isLoading ? (
            <div className="mt-4 rounded-3xl border border-white/10 bg-black/30 p-5">
              <div className="h-4 w-40 animate-pulse rounded-full bg-white/10" />
              <div className="mt-4 h-3 w-full animate-pulse rounded-full bg-white/10" />
              <div className="mt-2 h-3 w-3/4 animate-pulse rounded-full bg-white/10" />
            </div>
          ) : null}

          {errorMessage ? (
            <div className="mt-4 rounded-3xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
              <p>{errorMessage}</p>

              <button
                type="button"
                onClick={() => void loadBackendResult()}
                className="mt-4 inline-flex items-center gap-2 rounded-2xl bg-red-400 px-4 py-2 font-semibold text-black"
              >
                <RefreshCcw className="h-4 w-4" />
                Retry
              </button>
            </div>
          ) : null}

          {analysis ? (
            <div className="mt-4">
              <p className="text-lg font-medium leading-7">
                {analysis.message}
              </p>

              <div className="mt-4 grid gap-3 rounded-3xl bg-black/30 p-4 text-sm sm:grid-cols-3">
                <Info label="Code" value={analysis.matched_sample.code} />
                <Info label="Zone" value={analysis.matched_sample.zone} />
                <Info label="Color" value={analysis.matched_sample.color} />
              </div>

              <div className="mt-4 grid gap-3 rounded-3xl bg-black/30 p-4 text-sm sm:grid-cols-3">
                <Info
                  label="Similarity Method"
                  value={analysis.similarity.method}
                />
                <Info
                  label="Score"
                  value={formatPercent(analysis.similarity.score)}
                />
                <Info
                  label="Confidence"
                  value={analysis.similarity.confidence_label}
                />
              </div>
            </div>
          ) : null}
        </section>

        {analysis ? (
          <>
            {/* 2. Visual Similarity Reference */}
            <section className="mt-5 rounded-[2rem] border border-amber-400/20 bg-amber-400/10 p-5">
              <div className="flex items-start gap-3">
                <ShieldCheck className="mt-1 h-5 w-5 shrink-0 text-amber-300" />

                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-300">
                    Visual Similarity Reference
                  </p>

                  <h2 className="mt-2 text-lg font-semibold text-white">
                    Comparator-based interpretation
                  </h2>

                  <p className="mt-3 text-sm leading-6 text-neutral-300">
                    This result compares the scanned laterite material against
                    documented comparator samples. The displayed zone and QAQC
                    values are references from the matched comparator sample, not
                    a definitive field classification or final grade prediction.
                  </p>

                  <p className="mt-3 text-sm leading-6 text-neutral-400">
                    Final grade control decisions should still refer to validated
                    sampling, QAQC procedures, and laboratory assay results.
                  </p>
                </div>
              </div>
            </section>

            {/* 3. Foto lapangan dan raw comparator kanan-kiri */}
            <section className="mt-5 grid gap-5 md:grid-cols-2">
              <ImagePanel
                title="Field Scan"
                subtitle={`${scanSession.source ?? "scan"} · ${scannedAtLabel}`}
                imageUrl={scanSession.image}
              />

              <ImagePanel
                title="Raw Comparator"
                subtitle={
                  analysis.images.raw.storage_path ?? "Supabase signed URL"
                }
                imageUrl={analysis.images.raw.signed_url ?? null}
              />
            </section>

            {/* 4. Material description dari raw comparator */}
            <section className="mt-5 rounded-[2rem] border border-white/10 bg-white/[0.04] p-5">
              <p className="text-xs uppercase tracking-[0.2em] text-neutral-500">
                Matched Raw Comparator
              </p>

              <h2 className="mt-2 text-lg font-semibold">
                Material Description
              </h2>

              <div className="mt-4 grid gap-4 text-sm">
                <Info label="Code" value={analysis.matched_sample.code} />
                <Info label="Zone" value={analysis.matched_sample.zone} />
                <Info label="Color" value={analysis.matched_sample.color} />
                <Info label="Size" value={analysis.matched_sample.size_text} />
                <Info
                  label="Composition"
                  value={analysis.matched_sample.composition}
                />
                <Info
                  label="Description"
                  value={analysis.matched_sample.description}
                />
              </div>
            </section>

            {/* 5. QAQC hasil lab material raw */}
            <section className="mt-5 rounded-[2rem] border border-white/10 bg-white/[0.04] p-5">
              <p className="text-xs uppercase tracking-[0.2em] text-neutral-500">
                Laboratory Reference
              </p>

              <h2 className="mt-2 text-lg font-semibold">
                QAQC Lab Reference
              </h2>

              <p className="mt-1 text-sm text-neutral-400">
                Laboratory assay values from the matched raw comparator sample.
              </p>

              <div className="mt-4 grid grid-cols-2 gap-3 text-sm sm:grid-cols-4">
                <Metric label="Ni" value={analysis.qaqc.ni} suffix="%" />
                <Metric label="Co" value={analysis.qaqc.co} suffix="%" />
                <Metric label="Fe" value={analysis.qaqc.fe} suffix="%" />
                <Metric label="SiO₂" value={analysis.qaqc.sio2} suffix="%" />
                <Metric label="CaO" value={analysis.qaqc.cao} suffix="%" />
                <Metric label="MgO" value={analysis.qaqc.mgo} suffix="%" />
                <Metric label="Fe/Ni" value={analysis.qaqc.fe_ni} />
                <Metric label="S/M" value={analysis.qaqc.s_m} />
              </div>
            </section>

            {/* 6. Scale image */}
            <section className="mt-5 rounded-[2rem] border border-white/10 bg-white/[0.04] p-5">
              <p className="text-xs uppercase tracking-[0.2em] text-neutral-500">
                Scale Documentation
              </p>

              <h2 className="mt-2 text-lg font-semibold">Scale Image</h2>

              <p className="mt-1 text-sm text-neutral-400">
                Scale or reference documentation image from the matched
                comparator sample.
              </p>

              <div className="mt-4 overflow-hidden rounded-3xl border border-white/10 bg-black/30">
                {analysis.images.scale.signed_url ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={analysis.images.scale.signed_url}
                    alt="Scale comparator"
                    className="h-auto w-full"
                  />
                ) : (
                  <div className="flex aspect-[4/3] items-center justify-center text-sm text-neutral-500">
                    No scale image URL
                  </div>
                )}
              </div>
            </section>

            {/* 7. Alternative candidates selain result utama */}
            <section className="mt-5 rounded-[2rem] border border-white/10 bg-white/[0.04] p-5">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.2em] text-neutral-500">
                    Comparator Alternatives
                  </p>

                  <h2 className="mt-2 text-lg font-semibold">
                    Alternative Candidates
                  </h2>

                  <p className="mt-1 text-sm leading-6 text-neutral-400">
                    Additional visual matches outside the main backend result.
                    These candidates help users compare similar laterite
                    appearances and should be treated as references, not
                    definitive classifications.
                  </p>
                </div>

                <div className="shrink-0 rounded-full border border-green-400/30 bg-green-400/10 px-3 py-1 text-xs font-medium text-green-300">
                  {analysis.similarity.method ?? "similarity_baseline"}
                </div>
              </div>

              {alternativeCandidates.length ? (
                <div className="mt-4 grid gap-3">
                  {alternativeCandidates.map((candidate, index) => (
                    <AlternativeCandidateCard
                      key={`${candidate.code}-${index}`}
                      candidate={candidate}
                      index={index}
                    />
                  ))}
                </div>
              ) : (
                <div className="mt-4 rounded-3xl border border-white/10 bg-black/30 p-4 text-sm text-neutral-400">
                  No alternative candidates are available outside the main
                  matched result.
                </div>
              )}
            </section>
          </>
        ) : null}

        <div className="mt-6 grid gap-3 sm:grid-cols-2">
          <button
            type="button"
            onClick={handleScanAgain}
            className="rounded-2xl bg-green-500 px-5 py-3 font-semibold text-black"
          >
            Scan Again
          </button>

          <button
            type="button"
            onClick={() => void loadBackendResult()}
            className="rounded-2xl border border-white/10 bg-white/[0.04] px-5 py-3 font-semibold text-white"
          >
            Refresh Backend Result
          </button>
        </div>
      </section>
    </main>
  );
}

function ImagePanel({
  title,
  subtitle,
  imageUrl,
}: {
  title: string;
  subtitle: string;
  imageUrl: string | null;
}) {
  return (
    <div className="overflow-hidden rounded-[2rem] border border-white/10 bg-white/[0.04]">
      <div className="relative aspect-[4/3] bg-black/40">
        {imageUrl ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={imageUrl}
            alt={title}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full flex-col items-center justify-center gap-3 text-neutral-500">
            <ImageIcon className="h-8 w-8" />
            <span className="text-sm">No image available</span>
          </div>
        )}
      </div>

      <div className="p-4">
        <h3 className="font-semibold">{title}</h3>
        <p className="mt-1 break-all text-xs text-neutral-500">{subtitle}</p>
      </div>
    </div>
  );
}

function AlternativeCandidateCard({
  candidate,
  index,
}: {
  candidate: TopCandidate;
  index: number;
}) {
  return (
    <div className="rounded-3xl border border-white/10 bg-black/30 p-4">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-neutral-500">
            Alternative {index + 1}
          </p>

          <h3 className="mt-1 text-lg font-semibold">
            {candidate.code ?? "-"}
          </h3>
        </div>

        <div className="text-right">
          <p className="text-xs text-neutral-500">Score</p>
          <p className="text-lg font-semibold text-green-300">
            {formatPercent(candidate.score)}
          </p>
        </div>
      </div>

      <div className="mt-4 grid gap-3 text-sm sm:grid-cols-3">
        <Info label="Zone" value={candidate.zone} />
        <Info label="Color" value={candidate.color} />
        <Info label="Confidence" value={candidate.confidence_label} />
      </div>

      <div className="mt-4 grid grid-cols-2 gap-3 text-sm sm:grid-cols-5">
        <Metric label="Ni" value={candidate.qaqc.ni} suffix="%" />
        <Metric label="Fe" value={candidate.qaqc.fe} suffix="%" />
        <Metric label="MgO" value={candidate.qaqc.mgo} suffix="%" />
        <Metric label="Fe/Ni" value={candidate.qaqc.fe_ni} />
        <Metric label="S/M" value={candidate.qaqc.s_m} />
      </div>

      {candidate.description ? (
        <p className="mt-4 text-sm leading-6 text-neutral-400">
          {candidate.description}
        </p>
      ) : null}
    </div>
  );
}

function Info({
  label,
  value,
}: {
  label: string;
  value: string | number | null | undefined;
}) {
  return (
    <div>
      <dt className="text-xs uppercase tracking-[0.2em] text-neutral-500">
        {label}
      </dt>
      <dd className="mt-1 break-words text-neutral-100">
        {value === null || value === undefined || value === "" ? "-" : value}
      </dd>
    </div>
  );
}

function Metric({
  label,
  value,
  suffix = "",
}: {
  label: string;
  value: number | null | undefined;
  suffix?: string;
}) {
  return (
    <div className="rounded-2xl bg-black/30 p-4">
      <p className="text-xs uppercase tracking-[0.2em] text-neutral-500">
        {label}
      </p>
      <p className="mt-2 text-lg font-semibold">
        {typeof value === "number" ? `${formatNumber(value)}${suffix}` : "-"}
      </p>
    </div>
  );
}

function formatNumber(value: number) {
  return new Intl.NumberFormat("id-ID", {
    maximumFractionDigits: 2,
  }).format(value);
}

function formatPercent(value: number | null | undefined) {
  if (typeof value !== "number") {
    return "-";
  }

  return `${Math.round(value * 100)}%`;
}