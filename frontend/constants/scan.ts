export const SCAN_SESSION_IMAGE_KEY = "lcgc_current_scan_image";
export const SCAN_SESSION_SOURCE_KEY = "lcgc_current_scan_source";
export const SCAN_SESSION_CREATED_AT_KEY = "lcgc_current_scan_created_at";

export const SCAN_IMAGE_CONFIG = {
  maxWidth: 1280,
  maxHeight: 1280,
  jpegQuality: 0.85,
} as const;

export const CAMERA_ERROR_MESSAGES = {
  notSupported: "Camera is not supported by this browser.",
  permissionDenied:
    "Camera access is required to preview and scan material. You can still upload an image.",
  notReady: "Camera is not ready yet. Please wait a moment.",
  captureFailed: "Unable to capture image from camera.",
  uploadInvalid: "Please upload a valid image file.",
  uploadFailed: "Unable to read image file.",
} as const;