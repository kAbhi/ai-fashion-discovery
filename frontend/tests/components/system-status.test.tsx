import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { SystemStatus } from "@/components/system-status";

function stubFetch(impl: () => Promise<Response>) {
  const fetchMock = vi.fn(impl);
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

const healthy = () =>
  Promise.resolve(
    new Response(JSON.stringify({ status: "ok", environment: "local", database: "ok" }), {
      status: 200,
    }),
  );

describe("SystemStatus", () => {
  it("shows connected status when the backend is healthy", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_BASE_URL", "https://api.example.test");
    stubFetch(healthy);

    render(<SystemStatus />);

    expect(await screen.findByText("Connected")).toBeInTheDocument();
    expect(screen.getByText("Reachable")).toBeInTheDocument();
    expect(screen.getByText("local")).toBeInTheDocument();
  });

  it("shows an error when the backend cannot be reached, and rechecks on click", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_BASE_URL", "https://api.example.test");
    const fetchMock = stubFetch(() => Promise.reject(new TypeError("network")));

    render(<SystemStatus />);
    expect(await screen.findByText("Could not reach the backend API.")).toBeInTheDocument();

    fetchMock.mockImplementation(healthy);
    await userEvent.click(screen.getByRole("button", { name: /recheck/i }));

    expect(await screen.findByText("Connected")).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it("reports missing configuration instead of calling a default host", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_BASE_URL", "");
    const fetchMock = stubFetch(healthy);

    render(<SystemStatus />);

    expect(await screen.findByText("NEXT_PUBLIC_API_BASE_URL is not set.")).toBeInTheDocument();
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
