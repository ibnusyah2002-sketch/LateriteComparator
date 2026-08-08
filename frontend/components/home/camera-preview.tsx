"use client";

import { ChangeEvent, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import {
  AlertTriangle,
  Camera,
  CameraOff,
  CheckCircle2,
  Image as ImageIcon,
  Loader2,
  RotateCcw,
  ScanLine,
  Upload,
} from "lucide-react";
import { useCamera } from "@/hooks/useCamera";
import { readImageFileAsDataUrl } from "@/services/camera";
import {
  SCAN_SESSION_CREATED_AT_KEY,
  SCAN_SESSION_IMAGE_KEY,
  SCAN_SESSION_SOURCE_KEY,
} from "@/constants/scan";

type CameraPreviewProps = {
  className?: string;
};

type SelectedImageSource = "camera" | "upload";

export function CameraPreview({ className = "" }: CameraPreviewProps) {
  const router = useRouter();
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const {
    stream,
    error,
    isStarting,
    isCameraActive,
    startCamera,
    stopCamera,
    captureImage,
    clearError,
  } = useCamera();

  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [selectedImageSource, setSelectedImageSource] =
    useState<SelectedImageSource | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const activeError = error || uploadError;

  useEffect(() => {
    if (!videoRef.current || !stream) return;

    videoRef.current.srcObject = stream;
  }, [stream]);

  const handleToggleCamera = async () => {
    setUploadError(null);
    clearError();

    if (isCameraActive) {
      stopCamera();
      return;
    }

    await startCamera();
  };

  const handleCaptureImage = async () => {
    if (!isCameraActive) return;

    const imageDataUrl = await captureImage(videoRef.current);

    if (!imageDataUrl) return;

    setSelectedImage(imageDataUrl);
    setSelectedImageSource("camera");
    setUploadError(null);
    stopCamera();
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleUploadImage = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (!file) return;

    setUploadError(null);
    clearError();

    try {
      const imageDataUrl = await readImageFileAsDataUrl(file);

      stopCamera();
      setSelectedImage(imageDataUrl);
      setSelectedImageSource("upload");
    } catch (uploadIssue) {
      const message =
        uploadIssue instanceof Error
          ? uploadIssue.message
          : "Unable to upload image.";

      setUploadError(message);
    } finally {
      event.target.value = "";
    }
  };

  const handleRetake = async () => {
    setSelectedImage(null);
    setSelectedImageSource(null);
    setUploadError(null);
    clearError();
    await startCamera();
  };

  const handleAnalyzeMaterial = () => {
    if (!selectedImage) return;

    setIsAnalyzing(true);

    sessionStorage.setItem(SCAN_SESSION_IMAGE_KEY, selectedImage);
    sessionStorage.setItem(
      SCAN_SESSION_SOURCE_KEY,
      selectedImageSource ?? "camera"
    );
    sessionStorage.setItem(
      SCAN_SESSION_CREATED_AT_KEY,
      new Date().toISOString()
    );

    router.push("/analysis");
  };

  return (
    <div
      className={`relative overflow-hidden rounded-[24px] border border-white/10 bg-black ${className}`}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleUploadImage}
      />

      <div className="relative min-h-[430px]">
        {selectedImage ? (
          <img
            src={selectedImage}
            alt="Selected laterite material"
            className="h-[430px] w-full object-cover"
          />
        ) : isCameraActive ? (
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="h-[430px] w-full object-cover"
          />
        ) : (
          <div className="flex min-h-[430px] items-center justify-center px-8 text-center">
            <div>
              <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full border border-[#4CAF50]/40 bg-[#4CAF50]/10">
                {activeError ? (
                  <AlertTriangle className="h-7 w-7 text-red-300" />
                ) : (
                  <Camera className="h-7 w-7 text-[#4CAF50]" />
                )}
              </div>

              <p className="text-lg font-semibold text-white">
                {activeError ? "Camera Not Active" : "Ready to Scan"}
              </p>

              <p className="mt-2 text-sm leading-6 text-white/55">
                {activeError
                  ? "Retry camera permission from the top-right button or upload an image."
                  : "Activate the camera from the top-right button before capturing material."}
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
          <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-black/50 px-3 py-2 backdrop-blur">
            <span
              className={`h-2 w-2 rounded-full ${
                selectedImage
                  ? "bg-[#4CAF50]"
                  : isCameraActive
                    ? "bg-[#4CAF50]"
                    : "bg-white/30"
              }`}
            />
            <span className="text-xs font-medium text-white/80">
              {selectedImage
                ? selectedImageSource === "upload"
                  ? "Image Uploaded"
                  : "Image Captured"
                : isCameraActive
                  ? "Live Preview"
                  : "Standby"}
            </span>
          </div>

          {!selectedImage && (
            <button
              type="button"
              onClick={handleToggleCamera}
              disabled={isStarting}
              className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-black/55 px-3 py-2 text-xs font-medium text-white/80 backdrop-blur transition hover:bg-white/10 hover:text-white disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isStarting ? (
                <>
                  <Loader2 className="h-3.5 w-3.5 animate-spin" />
                  Starting
                </>
              ) : isCameraActive ? (
                <>
                  <CameraOff className="h-3.5 w-3.5" />
                  Stop
                </>
              ) : (
                <>
                  <Camera className="h-3.5 w-3.5" />
                  Enable
                </>
              )}
            </button>
          )}
        </div>

        {selectedImage && (
          <div className="absolute bottom-4 left-4 right-4 rounded-2xl border border-[#4CAF50]/25 bg-black/60 p-3 backdrop-blur">
            <div className="flex items-center gap-2 text-sm font-medium text-white">
              <CheckCircle2 className="h-4 w-4 text-[#4CAF50]" />
              Material image ready for analysis
            </div>
          </div>
        )}
      </div>

      {activeError && (
        <div className="border-t border-white/10 bg-red-500/10 px-4 py-3 text-sm leading-6 text-red-100">
          {activeError}
        </div>
      )}

          <div className="space-y-3 border-t border-white/10 bg-[#131816] p-4">
          {!selectedImage && (
            <button
              type="button"
              onClick={handleCaptureImage}
              disabled={!isCameraActive || isStarting}
              className="flex w-full items-center justify-center gap-2 rounded-2xl bg-[#4CAF50] px-5 py-4 text-base font-semibold text-black transition hover:bg-[#66BB6A] disabled:cursor-not-allowed disabled:bg-white/15 disabled:text-white/35"
            >
              <ScanLine className="h-5 w-5" />
              Capture Material
            </button>
          )}

          {selectedImage ? (
            <button
              type="button"
              onClick={handleAnalyzeMaterial}
              disabled={isAnalyzing}
              className="flex w-full items-center justify-center gap-2 rounded-2xl bg-[#4CAF50] px-5 py-4 text-base font-semibold text-black transition hover:bg-[#66BB6A] disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isAnalyzing ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  Preparing Analysis...
                </>
              ) : (
                <>
                  <ScanLine className="h-5 w-5" />
                  Analyze Material
                </>
              )}
            </button>
          ) : (
            <button
              type="button"
              onClick={handleUploadClick}
              className="flex w-full items-center justify-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-5 py-4 text-base font-semibold text-white transition hover:bg-white/10"
            >
              <Upload className="h-5 w-5" />
              Upload Image
            </button>
          )}

          {selectedImage && (
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={handleRetake}
                className="flex items-center justify-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-4 py-4 text-sm font-semibold text-white transition hover:bg-white/10"
              >
                <RotateCcw className="h-4 w-4" />
                Retake
              </button>

              <button
                type="button"
                onClick={handleUploadClick}
                className="flex items-center justify-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-4 py-4 text-sm font-semibold text-white transition hover:bg-white/10"
              >
                <ImageIcon className="h-4 w-4" />
                Change
              </button>
            </div>
          )}  
        <p className="text-center text-xs leading-5 text-white/45">
          The material photo will be compared visually against the local
          comparator database.
        </p>
      </div>
    </div>
  );
}

export default CameraPreview;