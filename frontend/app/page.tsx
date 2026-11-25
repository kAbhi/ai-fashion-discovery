import { Sparkles } from "lucide-react";
import { useEffect, useState } from "react";

import { SystemStatus } from "@/components/system-status";

type HealthStatus = "ok" | "degraded" | "unreachable" | "misconfigured";

export default function HomePage() {
  const [backendHealth, setBackendHealth] = useState<HealthStatus>();
  const [searchQuery, setSearchQuery] = useState("");

  const checkBackend = async () => {
    const result = await fetch("/api/health");
    const json = await result.json();
    if (result.ok) {
      setBackendHealth(json.status as HealthStatus);
    } else {
      setBackendHealth("unreachable");
    }
  };

  useEffect(() => {
    void checkBackend();
  }, []);

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const target = e.currentTarget;
    const input = target.querySelector("input") as HTMLInputElement;
    if (input?.value.trim()) {
      window.location.href = `/search?q=${encodeURIComponent(input.value.trim())}`;
    }
  };

  return (
    <main className="mx-auto flex min-h-dvh w-full max-w-md flex-col items-center justify-center gap-8 px-5 py-12 sm:max-w-lg bg-background">
      <header className="flex flex-col items-center gap-3 text-center">
        <Sparkles className="size-8" aria-hidden="true" />
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
          Fashion Discovery
        </h1>
        <p className="text-sm text-muted-foreground">
          Occasion-first AI-powered shopping experience
        </p>
      </header>

      <div className="w-full max-w-2xl space-y-6">
        <SystemStatus />

        <div>
          <h2 className="text-xl font-semibold text-center text-muted-foreground mb-4">
            Tell us what you're looking for
          </h2>

          <form onSubmit={handleSearch}>
            <div className="relative">
              <svg
                className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground"
                aria-hidden="true"
                viewBox="0 0 24 24"
              >
                <path
                  d="M21 21l-5.3-5.3a.75.75 0 0 0-1.06 0L13 19.9l-4.3-4.3a.75.75 0 0 0-1.06 0L2 15l8.6 8.6a.75.75 0 0 0 1.06 0z"
                />
              </svg>

              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-4 py-3 rounded-xl border border-border focus-ring focus-ring-offset-background w-full"
                placeholder="Find me something to wear to a friend's wedding..."
                required
                aria-label="Describe what you're looking for"
              />
            </div>

            <button
              type="submit"
              className="absolute right-3 top-1/2 -translate-y-1/2 rounded-xl bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
              aria-label="Search"
            >
              Search
            </button>
          </form>
        </div>

        {backendHealth && backendHealth !== "unreachable" && (
          <div>
            <h2 className="text-xl font-semibold text-center text-muted-foreground mb-4">
              Inspired by your shopping needs
            </h2>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {["Wedding guest outfits", "Goa vacation wardrobe", "Office wear upgrade", "Cocktail party attire", "Everyday sneakers"].map(
                (prompt) => (
                  <article
                    key={prompt}
                    className="border rounded-xl p-4 hover:bg-card/50 transition-colors cursor-pointer"
                    onClick={() => window.location.href = `/search?q=${encodeURIComponent(prompt)}`}
                    role="button"
                    aria-label={`Browse ${prompt}`}
                  >
                    <Sparkles className="size-4 mb-3 opacity-50" aria-hidden="true" />
                    <p className="text-sm line-clamp-2">{prompt}</p>
                  </article>
                )
              )}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
