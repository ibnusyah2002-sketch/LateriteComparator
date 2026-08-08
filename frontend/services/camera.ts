import { CAMERA_ERROR_MESSAGES, SCAN_IMAGE_CONFIG } from "@/constants/scan";

export async function requestEnvironmentCamera(): Promise<MediaStream> {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    throw new Error(CAMERA_ERROR_MESSAGES.notSupported);
  }

  try {
    return await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: {
          ideal: "environment",
        },
      },
      audio: false,
    });
  } catch {
    throw new Error(CAMERA_ERROR_MESSAGES.permissionDenied);
  }
}

export function stopCameraStream(stream: MediaStream | null): void {
  if (!stream) return;

  stream.getTracks().forEach((track) => {
    track.stop();
  });
}

export async function captureVideoFrame(
  videoElement: HTMLVideoElement
): Promise<string> {
  if (!videoElement.videoWidth || !videoElement.videoHeight) {
    throw new Error(CAMERA_ERROR_MESSAGES.notReady);
  }

  const canvas = document.createElement("canvas");
  canvas.width = videoElement.videoWidth;
  canvas.height = videoElement.videoHeight;

  const context = canvas.getContext("2d");

  if (!context) {
    throw new Error(CAMERA_ERROR_MESSAGES.captureFailed);
  }

  context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

  return resizeImageDataUrl(canvas.toDataURL("image/jpeg", 0.92));
}

export function readImageFileAsDataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    if (!file.type.startsWith("image/")) {
      reject(new Error(CAMERA_ERROR_MESSAGES.uploadInvalid));
      return;
    }

    const reader = new FileReader();

    reader.onload = async () => {
      try {
        if (typeof reader.result !== "string") {
          reject(new Error(CAMERA_ERROR_MESSAGES.uploadFailed));
          return;
        }

        const resizedImage = await resizeImageDataUrl(reader.result);
        resolve(resizedImage);
      } catch {
        reject(new Error(CAMERA_ERROR_MESSAGES.uploadFailed));
      }
    };

    reader.onerror = () => {
      reject(new Error(CAMERA_ERROR_MESSAGES.uploadFailed));
    };

    reader.readAsDataURL(file);
  });
}

export function resizeImageDataUrl(imageDataUrl: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const image = new Image();

    image.onload = () => {
      const { width, height } = getResizedDimensions(
        image.width,
        image.height,
        SCAN_IMAGE_CONFIG.maxWidth,
        SCAN_IMAGE_CONFIG.maxHeight
      );

      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;

      const context = canvas.getContext("2d");

      if (!context) {
        reject(new Error(CAMERA_ERROR_MESSAGES.captureFailed));
        return;
      }

      context.drawImage(image, 0, 0, width, height);

      resolve(
        canvas.toDataURL("image/jpeg", SCAN_IMAGE_CONFIG.jpegQuality)
      );
    };

    image.onerror = () => {
      reject(new Error(CAMERA_ERROR_MESSAGES.uploadFailed));
    };

    image.src = imageDataUrl;
  });
}

function getResizedDimensions(
  originalWidth: number,
  originalHeight: number,
  maxWidth: number,
  maxHeight: number
): { width: number; height: number } {
  const widthRatio = maxWidth / originalWidth;
  const heightRatio = maxHeight / originalHeight;
  const ratio = Math.min(widthRatio, heightRatio, 1);

  return {
    width: Math.round(originalWidth * ratio),
    height: Math.round(originalHeight * ratio),
  };
}