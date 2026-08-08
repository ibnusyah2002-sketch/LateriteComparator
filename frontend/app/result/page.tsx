"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  ArrowLeft,
  BarChart3,
  Database,
  RotateCcw,
  ScanSearch,
} from "lucide-react";
import {
  SCAN_SESSION_CREATED_AT_KEY,
  SCAN_SESSION_IMAGE_KEY,
  SCAN_SESSION_SOURCE_KEY,
} from "@/constants/scan";

const qaqcData = [
  { label: "Ni", value: "1.82", unit: "%" },
  { label: "Co", value: "0.08", unit: "%" },
  { label: "Fe", value: "23.41", unit: "%" },
  { label: "MgO", value: "9.62", unit: "%" },
  { label: "SiO₂", value: "41.20", unit: "%" },
];

const descriptionData = [
  { label: "Zona", value: "Earthy Saprolite" },
  { label: "Warna", value: "Brown Greenish" },
  { label: "Ukuran", value: "Gravel - Boulder" },
  {
    label: "Komposisi",
    value: "Serpentine, Goethite, Garnierite traces",
  },
  {
    label: "Keterangan",
    value:
      "Weathered ultramafic material with greenish brown tone and earthy texture.",
  },
];

const alternativeMatches = [
  { code: "RB4-011", similarity: "95.4%" },
  { code: "RB4-007", similarity: "93.8%" },
  { code: "RB4-021", similarity: "91.2%" },
];

export default function ResultPage() {
  const [userImage, setUserImage] = useState<string | null>(null);
  const [source, setSource] = useState<string | null>(null);
  const [createdAt, setCreatedAt] = useState<string | null>(null);

  useEffect(() => {
    setUserImage(sessionStorage.getItem(SCAN_SESSION_IMAGE_KEY));
    setSource(sessionStorage.getItem(SCAN_SESSION_SOURCE_KEY));
    setCreatedAt(sessionStorage.getItem(SCAN_SESSION_CREATED_AT_KEY));
  }, []);

  return (
    <main className="min-h-screen bg-[#0B0F0C] px-4 py-6 text-white">
      <div className="mx-auto max-w-[430px] space-y-6 pb-10">
        <header className="space-y-4">
          <Link
            href="/"
            className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/70 transition hover:bg-white/10 hover:text-white"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Scanner
          </Link>

          <div>
            <p className="text-sm font-medium uppercase tracking-[0.3em] text-[#4CAF50]">
              Comparator Result
            </p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight text-white">
              Visual Match Found
            </h1>
            <p className="mt-3 text-sm leading-6 text-white/60">
              This scanned material is visually similar to comparator sample
              RB4-015.
            </p>
          </div>
        </header>

        <section className="rounded-[28px] border border-[#4CAF50]/30 bg-[#131816] p-5 shadow-2xl">
          <div className="flex items-end justify-between gap-4">
            <div>
              <p className="text-sm text-white/55">Best Match</p>
              <h2 className="mt-1 text-3xl font-semibold text-white">
                RB4-015
              </h2>
              <p className="mt-2 text-sm text-white/60">Earthy Saprolite</p>
            </div>

            <div className="text-right">
              <p className="text-4xl font-bold text-[#4CAF50]">98.7%</p>
              <p className="mt-1 text-sm text-white/55">Very High</p>
            </div>
          </div>

          <div className="mt-5 grid grid-cols-2 gap-3">
            <div className="rounded-2xl border border-white/10 bg-black/20 p-3">
              <div className="flex items-center gap-2 text-xs text-white/45">
                <ScanSearch className="h-4 w-4" />
                Source
              </div>
              <p className="mt-2 text-sm font-medium capitalize text-white">
                {source ?? "Local scan"}
              </p>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/20 p-3">
              <div className="flex items-center gap-2 text-xs text-white/45">
                <Database className="h-4 w-4" />
                Database
              </div>
              <p className="mt-2 text-sm font-medium text-white">
                Local Comparator
              </p>
            </div>
          </div>

          {createdAt && (
            <p className="mt-4 text-xs text-white/35">
              Analysis generated from temporary local scan data.
            </p>
          )}
        </section>

        <section className="grid grid-cols-2 gap-3">
          <div className="rounded-[24px] border border-white/10 bg-[#131816] p-3">
            <p className="mb-3 text-sm font-medium text-white/70">
              User Photo
            </p>
            <div className="flex aspect-square items-center justify-center overflow-hidden rounded-[18px] bg-black">
              {userImage ? (
                <img
                  src={userImage}
                  alt="Scanned laterite material"
                  className="h-full w-full object-cover"
                />
              ) : (
                <p className="px-4 text-center text-xs text-white/40">
                  No scan image found
                </p>
              )}
            </div>
          </div>

          <div className="rounded-[24px] border border-white/10 bg-[#131816] p-3">
            <p className="mb-3 text-sm font-medium text-white/70">
              Comparator
            </p>
            <div className="flex aspect-square items-center justify-center rounded-[18px] border border-[#4CAF50]/20 bg-[#4CAF50]/10">
              <div className="text-center">
                <p className="text-lg font-semibold text-white">RB4-015</p>
                <p className="mt-1 px-3 text-xs leading-5 text-white/45">
                  Comparator image placeholder
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-[24px] border border-white/10 bg-[#131816] p-5">
          <div className="flex items-center gap-2 text-white/55">
            <BarChart3 className="h-4 w-4" />
            <p className="text-sm font-medium">Material Summary</p>
          </div>
          <h3 className="mt-2 text-xl font-semibold text-white">
            Brown Greenish Earthy Saprolite
          </h3>
          <p className="mt-3 text-sm leading-6 text-white/60">
            Visual characteristics indicate similarity with laterite comparator
            material in the earthy saprolite zone.
          </p>
        </section>

        <section className="space-y-3">
          <h3 className="text-lg font-semibold text-white">QAQC Data</h3>
          <div className="grid grid-cols-2 gap-3">
            {qaqcData.map((item) => (
              <div
                key={item.label}
                className="rounded-2xl border border-white/10 bg-[#131816] p-4"
              >
                <p className="text-sm text-white/45">{item.label}</p>
                <p className="mt-2 text-2xl font-semibold text-white">
                  {item.value}
                  <span className="ml-1 text-sm text-white/45">
                    {item.unit}
                  </span>
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="space-y-3">
          <h3 className="text-lg font-semibold text-white">
            Dynamic Description
          </h3>

          {descriptionData.map((item) => (
            <div
              key={item.label}
              className="rounded-2xl border border-white/10 bg-[#131816] p-4"
            >
              <p className="text-sm text-[#4CAF50]">{item.label}</p>
              <p className="mt-2 text-sm leading-6 text-white/70">
                {item.value}
              </p>
            </div>
          ))}
        </section>

        <section className="space-y-3">
          <h3 className="text-lg font-semibold text-white">
            Alternative Matches
          </h3>

          {alternativeMatches.map((match) => (
            <div
              key={match.code}
              className="flex items-center justify-between rounded-2xl border border-white/10 bg-[#131816] p-4"
            >
              <p className="font-semibold text-white">{match.code}</p>
              <p className="text-sm font-medium text-[#4CAF50]">
                {match.similarity}
              </p>
            </div>
          ))}
        </section>

        <Link
          href="/"
          className="flex w-full items-center justify-center gap-2 rounded-2xl bg-[#4CAF50] px-5 py-4 text-center text-base font-semibold text-black transition hover:bg-[#66BB6A]"
        >
          <RotateCcw className="h-5 w-5" />
          Scan Again
        </Link>
      </div>
    </main>
  );
}