import { getApiBaseUrl } from "@/lib/config";

// Mirrors backend `HealthResponse`. From Phase 1 onward, API types will be
// generated from the backend OpenAPI schema instead of written by hand.
export type HealthResponse = {
  status: "ok" | "degraded";
  environment: string;
  database: "ok" | "unavailable";
};

export type HealthResult =
  | { kind: "ok"; data: HealthResponse }
  | { kind: "degraded"; data: HealthResponse }
  | { kind: "unreachable"; message: string }
  | { kind: "misconfigured"; message: string };

function isHealthResponse(value: unknown): value is HealthResponse {
  if (typeof value !== "object" || value === null) return false;
  const v = value as Record<string, unknown>;
  return (
    (v.status === "ok" || v.status === "degraded") &&
    typeof v.environment === "string" &&
    (v.database === "ok" || v.database === "unavailable")
  );
}

export async function fetchHealth(
  fetchImpl: typeof fetch = fetch,
  baseUrl: string | null = getApiBaseUrl(),
): Promise<HealthResult> {
  if (!baseUrl) {
    return { kind: "misconfigured", message: "NEXT_PUBLIC_API_BASE_URL is not set." };
  }

  let response: Response;
  try {
    response = await fetchImpl(`${baseUrl}/health`, { cache: "no-store" });
  } catch {
    return { kind: "unreachable", message: "Could not reach the backend API." };
  }

  let body: unknown;
  try {
    body = await response.json();
  } catch {
    return { kind: "unreachable", message: `Unexpected response (HTTP ${response.status}).` };
  }

  if (!isHealthResponse(body)) {
    return { kind: "unreachable", message: `Unexpected response (HTTP ${response.status}).` };
  }
  return body.status === "ok" ? { kind: "ok", data: body } : { kind: "degraded", data: body };
}
