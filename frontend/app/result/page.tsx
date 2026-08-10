"use client";

import Image from "next/image";
import { useEffect, useMemo, useState } from "react";
import { ArrowLeft, Camera, Database, ImageIcon, RefreshCcw } from "lucide-react";
import { useRouter } from "next/navigation";
import { fetchMockAnalysis, submitAnalysisImage } from "@/services/analysis";
import {
  SCAN_SESSION_CREATED_AT_KEY,
  SCAN_SESSION_IMAGE_KEY,
  SCAN_SESSION_SOURCE_KEY,
} from "@/constants/scan";
import type { AnalysisPayload } from "@/types/analysis";

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

  async function loadBackendResult(imageOverride?: string | null) {
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
  }

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
  }, []);

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
      <section className="mx-auto max-w-3xl px-5 py-6">
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

        <section className="mt-6 rounded-[2rem] border border-white/10 bg-white/[0.04] p-4">
          <div className="flex items-center gap-2 text-sm text-neutral-400">
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
              <p className="text-lg font-medium leading-7">{analysis.message}</p>

              <div className="mt-4 grid gap-3 rounded-3xl bg-black/30 p-4 text-sm sm:grid-cols-3">
                <Info label="Code" value={analysis.matched_sample.code} />
                <Info label="Zone" value={analysis.matched_sample.zone} />
                <Info label="Color" value={analysis.matched_sample.color} />
              </div>
            </div>
          ) : null}
        </section>

        <section className="mt-5 grid gap-5 md:grid-cols-2">
          <ImagePanel
            title="Scanned Material"
            subtitle={`${scanSession.source ?? "scan"} · ${scannedAtLabel}`}
            imageUrl={scanSession.image}
            isSessionImage
          />

          <ImagePanel
            title="Comparator Match"
            subtitle={analysis?.images.raw.storage_path ?? "Supabase signed URL"}
            imageUrl={analysis?.images.raw.signed_url ?? null}
          />
        </section>

        {analysis ? (
          <>
            <section className="mt-5 rounded-[2rem] border border-white/10 bg-white/[0.04] p-5">
              <h2 className="text-lg font-semibold">Material Description</h2>

              <dl className="mt-4 grid gap-4 text-sm">
                <Info label="Size" value={analysis.matched_sample.size_text} />
                <Info
                  label="Composition"
                  value={analysis.matched_sample.composition}
                />
                <Info
                  label="Description"
                  value={analysis.matched_sample.description}
                />
              </dl>
            </section>

            <section className="mt-5 rounded-[2rem] border border-white/10 bg-white/[0.04] p-5">
              <h2 className="text-lg font-semibold">QAQC Reference</h2>

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

            <section className="mt-5 rounded-[2rem] border border-white/10 bg-white/[0.04] p-5">
              <h2 className="text-lg font-semibold">Scale Image</h2>

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
  isSessionImage = false,
}: {
  title: string;
  subtitle: string;
  imageUrl: string | null;
  isSessionImage?: boolean;
}) {
  return (
    <div className="overflow-hidden rounded-[2rem] border border-white/10 bg-white/[0.04]">
      <div className="relative aspect-[4/3] bg-black/40">
        {imageUrl ? (
          isSessionImage ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={imageUrl}
              alt={title}
              className="h-full w-full object-cover"
            />
          ) : (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={imageUrl}
              alt={title}
              className="h-full w-full object-cover"
            />
          )
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

function Info({
  label,
  value,
}: {
  label: string;
  value: string | null | undefined;
}) {
  return (
    <div>
      <dt className="text-xs uppercase tracking-[0.2em] text-neutral-500">
        {label}
      </dt>
      <dd className="mt-1 text-neutral-100">{value ?? "-"}</dd>
    </div>
  );
}

function Metric({
  label,
  value,
  suffix = "",
}: {
  label: string;
  value: number | null;
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