"use client";

import { useCallback, useEffect, useState } from "react";
import {
  captureVideoFrame,
  requestEnvironmentCamera,
  stopCameraStream,
} from "@/services/camera";

type UseCameraReturn = {
  stream: MediaStream | null;
  error: string | null;
  isStarting: boolean;
  isCameraActive: boolean;
  startCamera: () => Promise<void>;
  stopCamera: () => void;
  captureImage: (videoElement: HTMLVideoElement | null) => Promise<string | null>;
  clearError: () => void;
};

export function useCamera(): UseCameraReturn {
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isStarting, setIsStarting] = useState(false);

  const startCamera = useCallback(async () => {
    setIsStarting(true);
    setError(null);

    try {
      const cameraStream = await requestEnvironmentCamera();
      setStream(cameraStream);
    } catch (cameraError) {
      const message =
        cameraError instanceof Error
          ? cameraError.message
          : "Unable to start camera.";

      setError(message);
    } finally {
      setIsStarting(false);
    }
  }, []);

  const stopCamera = useCallback(() => {
    stopCameraStream(stream);
    setStream(null);
  }, [stream]);

  const captureImage = useCallback(
    async (videoElement: HTMLVideoElement | null): Promise<string | null> => {
      setError(null);

      if (!videoElement) {
        setError("Camera preview is not ready yet.");
        return null;
      }

      try {
        return await captureVideoFrame(videoElement);
      } catch (captureError) {
        const message =
          captureError instanceof Error
            ? captureError.message
            : "Unable to capture image.";

        setError(message);
        return null;
      }
    },
    []
  );

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  useEffect(() => {
    return () => {
      stopCameraStream(stream);
    };
  }, [stream]);

  return {
    stream,
    error,
    isStarting,
    isCameraActive: Boolean(stream),
    startCamera,
    stopCamera,
    captureImage,
    clearError,
  };
}
