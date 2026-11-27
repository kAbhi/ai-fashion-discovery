"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Search, ArrowLeft } from "lucide-react";
import { Navigation } from "@/components/navigation";
import { ProductCard } from "@/components/ui/product-card";
import { ProductCardSkeleton } from "@/components/ui/skeleton";
import { listProducts, Product } from "@/lib/api";


export default function SearchResultsPage() {
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);
  const [initialized, setInitialized] = useState(false);

  const [results, setResults] = useState<Product[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const pageSize = 24;

  useEffect(() => {
    if (typeof window !== "undefined") {
      const searchParams = new URLSearchParams(window.location.search);
      setQuery(searchParams.get("q") || "");
      setPage(parseInt(searchParams.get("page") || "1", 10));
      setInitialized(true);
    }
  }, []);

  const loadResults = async () => {
    if (!initialized) return;
    try {
      setLoading(true);
      setError(null);
      const result = await listProducts({
        q: query,
        page,
        page_size: pageSize,
      });
      setResults(result.items);
      setTotal(result.total);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to load results"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadResults();
  }, [query, page, initialized]);

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className="min-h-dvh bg-background">
      <Navigation />

      <main className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <header className="mb-8 flex items-center gap-2">
          <ButtonBack />
          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              Search results
            </h1>
            <p className="text-sm text-muted-foreground">
              {total} products found for &quot;{query}&quot;
            </p>
          </div>
        </header>

        {/* Error state */}
        {error && (
          <div className="rounded-xl border border-destructive/50 bg-destructive/10 p-4 text-destructive mb-8">
            <p>{error}</p>
            <button
              onClick={() => void loadResults()}
              className="mt-3 text-sm underline underline-offset-4"
            >
              Try again
            </button>
          </div>
        )}

        {/* Empty state */}
        {!loading && !error && total === 0 && (
          <div className="text-center py-16 mb-8">
            <Search className="size-12 mx-auto text-muted-foreground mb-4" aria-hidden="true" />
            <h2 className="text-xl font-semibold">No products found</h2>
            <p className="text-muted-foreground mt-2">
              Try adjusting your search terms or browse our collections.
            </p>
            <Link
              href="/"
              className="mt-4 inline-block px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90"
            >
              Back to home
            </Link>
          </div>
        )}

        {/* Results grid */}
        {!loading && !error && total > 0 && (
          <>
            <div className="flex items-center justify-between mb-4">
              <p className="text-sm text-muted-foreground">
                Showing {results.length} of {total} products
              </p>
              <div className="flex gap-2">
                <button
                  disabled={page <= 1}
                  onClick={() => {
                  const url = new URL(window.location.href);
                  url.searchParams.set("page", String(page - 1));
                  window.location.href = url.toString();
                }}
                  className="px-3 py-2 rounded-lg border border-border disabled:opacity-50 disabled:pointer-events-none text-sm hover:bg-muted"
                >
                  Previous
                </button>
                <button
                  disabled={page >= totalPages || totalPages === 0}
                  onClick={() => {
                  const url = new URL(window.location.href);
                  url.searchParams.set("page", String(page + 1));
                  window.location.href = url.toString();
                }}
                  className="px-3 py-2 rounded-lg border border-border disabled:opacity-50 disabled:pointer-events-none text-sm hover:bg-muted"
                >
                  Next
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {loading
                ? Array.from({ length: 12 }).map((_, i) => (
                    <ProductCardSkeleton key={i} />
                  ))
                : results.map((p) => (
                    <ProductCard
                      key={p.id}
                      product={{
                        id: p.id,
                        name: p.name,
                        brand: p.brand,
                        price: p.min_price ?? null,
                        currency: p.currency,
                        image:
                          p.image_references?.[0] ||
                          "https://placehold.co/400x400/e2e8f0/475569?text=Product",
                        styleTags: p.style_tags || undefined,
                        occasionTags: p.occasion_tags || undefined,
                      }}
                    />
                  ))}
            </div>
          </>
        )}
      </main>
    </div>
  );
}

function ButtonBack() {
  return (
    <Link
      href="/"
      className="inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
    >
      <ArrowLeft className="size-4" />
      Back
    </Link>
  );
}
