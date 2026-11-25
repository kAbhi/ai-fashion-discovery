import { describe, expect, it, vi } from "vitest";

import { fetchHealth } from "@/services/health";

const BASE = "https://api.example.test";

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

describe("fetchHealth", () => {
  it("returns ok when backend and database are healthy", async () => {
    const body = { status: "ok", environment: "local", database: "ok" };
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse(body));

    const result = await fetchHealth(fetchMock, BASE);

    expect(fetchMock).toHaveBeenCalledWith(`${BASE}/health`, { cache: "no-store" });
    expect(result).toEqual({ kind: "ok", data: body });
  });

  it("returns degraded when the database is unavailable (HTTP 503)", async () => {
    const body = { status: "degraded", environment: "local", database: "unavailable" };
    const result = await fetchHealth(vi.fn().mockResolvedValue(jsonResponse(body, 503)), BASE);

    expect(result).toEqual({ kind: "degraded", data: body });
  });

  it("returns unreachable on network failure", async () => {
    const result = await fetchHealth(vi.fn().mockRejectedValue(new TypeError("fail")), BASE);
    expect(result.kind).toBe("unreachable");
  });

  it("returns unreachable on an unexpected payload", async () => {
    const result = await fetchHealth(vi.fn().mockResolvedValue(jsonResponse({ foo: 1 })), BASE);
    expect(result.kind).toBe("unreachable");
  });

  it("returns misconfigured when no API base URL is set", async () => {
    const fetchMock = vi.fn();
    const result = await fetchHealth(fetchMock, null);

    expect(result.kind).toBe("misconfigured");
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
