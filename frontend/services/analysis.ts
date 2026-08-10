import type { AnalysisPayload } from "@/types/analysis";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export async function fetchMockAnalysis(
  code = "BG1 - 01",
): Promise<AnalysisPayload> {
  const params = new URLSearchParams({
    code,
  });

  const response = await fetch(
    `${API_BASE_URL}/api/analysis/mock?${params.toString()}`,
    {
      method: "GET",
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch mock analysis: ${response.status}`);
  }

  return response.json();
}

export async function submitAnalysisImage({
  imageDataUrl,
  source = "unknown",
}: {
  imageDataUrl: string;
  source?: string | null;
}): Promise<AnalysisPayload> {
  const response = await fetch(`${API_BASE_URL}/api/analysis`, {
    method: "POST",
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      image_data_url: imageDataUrl,
      source,
    }),
  });

  if (!response.ok) {
    throw new Error(`Failed to submit analysis image: ${response.status}`);
  }

  return response.json();
}