"use client";

import { useEffect, useState } from "react";
import { fetchMockAnalysis } from "@/services/analysis";
import type { AnalysisPayload } from "@/types/analysis";

export default function BackendTestPage() {
  const [data, setData] = useState<AnalysisPayload | null>(null);
  const [code, setCode] = useState("BG1 - 01");
  const [inputCode, setInputCode] = useState("BG1 - 01");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function loadAnalysis(targetCode: string) {
    try {
      setIsLoading(true);
      setError(null);

      const result = await fetchMockAnalysis(targetCode);
      setData(result);
      setCode(targetCode);
    } catch (caughtError) {
      setData(null);
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Failed to load backend data.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    void loadAnalysis(code);
  }, []);

  return (
    <main className="min-h-screen bg-[#0B0B0B] px-5 py-8 text-white">
      <section className="mx-auto flex max-w-3xl flex-col gap-6">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-green-400">
            LCGC Backend Test
          </p>
          <h1 className="mt-2 text-3xl font-semibold">
            Supabase Comparator Response
          </h1>
          <p className="mt-2 text-sm text-neutral-400">
            This page tests whether the frontend can fetch backend analysis data
            and render signed image URLs from a private Supabase bucket.
          </p>
        </div>

        <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-4">
          <label className="text-sm text-neutral-300" htmlFor="code">
            Comparator Code
          </label>

          <div className="mt-3 flex flex-col gap-3 sm:flex-row">
            <input
              id="code"
              value={inputCode}
              onChange={(event) => setInputCode(event.target.value)}
              className="flex-1 rounded-2xl border border-white/10 bg-black/40 px-4 py-3 text-white outline-none focus:border-green-400"
              placeholder="BG1 - 01"
            />

            <button
              type="button"
              onClick={() => void loadAnalysis(inputCode)}
              disabled={isLoading}
              className="rounded-2xl bg-green-500 px-5 py-3 font-semibold text-black disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isLoading ? "Loading..." : "Fetch"}
            </button>
          </div>
        </div>

        {error ? (
          <div className="rounded-3xl border border-red-500/30 bg-red-500/10 p-4 text-red-200">
            {error}
          </div>
        ) : null}

        {data ? (
          <section className="grid gap-5">
            <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-5">
              <p className="text-sm text-neutral-400">Message</p>
              <p className="mt-2 text-lg font-medium">{data.message}</p>
            </div>

            <div className="grid gap-5 md:grid-cols-2">
              <ImageCard
                title="Raw Comparator Image"
                imageUrl={data.images.raw.signed_url}
                storagePath={data.images.raw.storage_path}
              />

              <ImageCard
                title="Scale Comparator Image"
                imageUrl={data.images.scale.signed_url}
                storagePath={data.images.scale.storage_path}
              />
            </div>

            <div className="rounded-3xl border border-white/10 bg-white/[0.04] p-5">
              <h2 className="text-xl font-semibold">
                {data.matched_sample.code}
              </h2>

              <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
                <Info label="Zone" value={data.matched_sample.zone} />
                <Info label="Color" value={data.matched_sample.color} />
                <Info label="Size" value={data.matched_sample.size_text} />
                <Info label="Composition" value={data.matched_sample.composition} />
                <Info label="Description" value={data.matched_sample.description} />
                <Info label="Ni" value={data.qaqc.ni?.toString()} />
                <Info label="Fe" value={data.qaqc.fe?.toString()} />
                <Info label="MgO" value={data.qaqc.mgo?.toString()} />
              </dl>
            </div>
          </section>
        ) : null}
      </section>
    </main>
  );
}

function ImageCard({
  title,
  imageUrl,
  storagePath,
}: {
  title: string;
  imageUrl: string | null;
  storagePath: string | null;
}) {
  return (
    <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/[0.04]">
      <div className="aspect-[4/3] bg-black/40">
        {imageUrl ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={imageUrl}
            alt={title}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-sm text-neutral-400">
            No signed URL
          </div>
        )}
      </div>

      <div className="p-4">
        <h3 className="font-semibold">{title}</h3>
        <p className="mt-1 break-all text-xs text-neutral-500">{storagePath}</p>
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
      <dt className="text-neutral-500">{label}</dt>
      <dd className="mt-1 text-neutral-100">{value ?? "-"}</dd>
    </div>
  );
}