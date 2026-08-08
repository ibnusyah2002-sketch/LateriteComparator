"use client";

import { useEffect, useRef } from "react";
import Link from "next/link";
import { Camera, CameraOff, Loader2, ScanLine, ShieldAlert } from "lucide-react";
import { useCamera } from "@/hooks/useCamera";

type CameraPreviewProps = {
  className?: string;
};

export function CameraPreview({ className = "" }: CameraPreviewProps) {
  const videoRef = useRef<HTMLVideoElement | null>(null);

  const {
    stream,
    error,
    isStarting,
    isCameraActive,
    startCamera,
    stopCamera,
    clearError,
  } = useCamera();

  useEffect(() => {
    if (!videoRef.current || !stream) return;

    videoRef.current.srcObject = stream;
  }, [stream]);

  const handleStartCamera = async () => {
    clearError();
    await startCamera();
  };

  return (
    <div
      className={`relative min-h-[360px] overflow-hidden rounded-[24px] border border-white/10 bg-black ${className}`}
    >
      {isCameraActive ? (
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="h-full min-h-[360px] w-full object-cover"
        />
      ) : (
        <div className="flex min-h-[360px] items-center justify-center px-8 text-center">
          <div>
            <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full border border-[#4CAF50]/40 bg-[#4CAF50]/10">
              {error ? (
                <ShieldAlert className="h-7 w-7 text-red-300" />
              ) : (
                <Camera className="h-7 w-7 text-[#4CAF50]" />
              )}
            </div>

            <p className="text-lg font-semibold text-white">
              {error ? "Camera Permission Needed" : "Camera Preview"}
            </p>

            <p className="mt-2 text-sm leading-6 text-white/55">
              {error
                ? "Camera is not active. You can retry permission or continue to scan page and upload an image."
                : "Enable live preview before scanning laterite material."}
            </p>
          </div>
        </div>
      )}

      <div className="pointer-events-none absolute inset-6 rounded-[22px] border border-[#4CAF50]/25" />
      <div className="pointer-events-none absolute left-6 top-6 h-10 w-10 border-l-2 border-t-2 border-[#4CAF50]" />
      <div className="pointer-events-none absolute right-6 top-6 h-10 w-10 border-r-2 border-t-2 border-[#4CAF50]" />
      <div className="pointer-events-none absolute bottom-6 left-6 h-10 w-10 border-b-2 border-l-2 border-[#4CAF50]" />
      <div className="pointer-events-none absolute bottom-6 right-6 h-10 w-10 border-b-2 border-r-2 border-[#4CAF50]" />

      <div className="absolute left-4 right-4 top-4 flex items-center justify-between gap-3">
        <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-black/45 px-3 py-2 backdrop-blur">
          <span
            className={`h-2 w-2 rounded-full ${
              isCameraActive ? "bg-[#4CAF50]" : "bg-white/30"
            }`}
          />
          <span className="text-xs font-medium text-white/75">
            {isCameraActive ? "Live Preview" : "Standby"}
          </span>
        </div>

        {isCameraActive && (
          <button
            type="button"
            onClick={stopCamera}
            className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-black/45 px-3 py-2 text-xs font-medium text-white/75 backdrop-blur transition hover:bg-white/10 hover:text-white"
          >
            <CameraOff className="h-3.5 w-3.5" />
            Stop
          </button>
        )}
      </div>

      <div className="absolute bottom-4 left-4 right-4 space-y-3">
        {!isCameraActive && (
          <button
            type="button"
            onClick={handleStartCamera}
            disabled={isStarting}
            className="flex w-full items-center justify-center gap-2 rounded-2xl bg-[#4CAF50] px-5 py-3 text-sm font-semibold text-black transition hover:bg-[#66BB6A] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isStarting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Starting Camera...
              </>
            ) : (
              <>
                <Camera className="h-4 w-4" />
                {error ? "Retry Camera Permission" : "Enable Camera Preview"}
              </>
            )}
          </button>
        )}

        {isCameraActive && (
          <Link
            href="/scan"
            className="flex w-full items-center justify-center gap-2 rounded-2xl bg-[#4CAF50] px-5 py-3 text-sm font-semibold text-black transition hover:bg-[#66BB6A]"
          >
            <ScanLine className="h-4 w-4" />
            Continue to Scan
          </Link>
        )}
      </div>
    </div>
  );
}

export default CameraPreview;