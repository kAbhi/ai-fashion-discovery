"use client";

import Link from "next/link";
import { Sparkles, ShoppingBag, Search, ArrowRight } from "lucide-react";
import { useEffect, useState } from "react";
import { ProductCard } from "@/components/ui/product-card";
import { ProductCardSkeleton } from "@/components/ui/skeleton";
import { Navigation } from "@/components/navigation";
import { getHealth, listProducts, Product } from "@/lib/api";

const SUGGESTED_PROMPTS = [
  { text: "Wedding guest outfits", occasion: "wedding" },
  { text: "Goa vacation wardrobe", occasion: "vacation" },
  { text: "Office wear upgrade", occasion: "office" },
  { text: "Cocktail party attire", occasion: "party" },
  { text: "Everyday sneakers", occasion: "casual" },
  { text: "Minimal office wardrobe", occasion: "office" },
];

interface ProductCardData {
  id: string;
  name: string;
  brand: string;
  price: number | null;
  currency: string;
  image: string;
  styleTags?: string[];
  occasionTags?: string[];
}

export default function HomePage() {
  const [backendHealth, setBackendHealth] = useState<
    "ok" | "degraded" | "unreachable" | "misconfigured" | "loading"
  >("loading");
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  const checkBackend = async () => {
    try {
      const health = await getHealth();
      setBackendHealth(health.status);
    } catch {
      setBackendHealth("unreachable");
    }
  };

  const loadFeaturedProducts = async () => {
    try {
      const result = await listProducts({ page_size: 8 });
      setProducts(result.items);
    } catch (error) {
      console.error("Failed to load featured products:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      const url = new URL(window.location.origin + "/search");
      url.searchParams.set("q", searchQuery.trim());
      window.location.href = url.toString();
    }
  };

  useEffect(() => {
    void checkBackend();
    void loadFeaturedProducts();
  }, []);

  return (
    <div className="min-h-dvh bg-background">
      <Navigation />

      <main className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-8">
        <header className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="size-6" aria-hidden="true" />
            <h1 className="text-3xl font-bold tracking-tight">Fashion Discovery</h1>
          </div>
          <p className="text-lg text-muted-foreground">
            Discover what you want to buy, even when you don&apos;t know exactly what you&apos;re looking for.
          </p>
        </header>

        {/* System status */}
        <div className="mb-8">
          {backendHealth === "loading" ? (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <div className="h-3 w-3 rounded-full bg-muted animate-pulse" />
              Checking system status…
            </div>
          ) : backendHealth === "ok" ? (
            <div className="flex items-center gap-2 text-sm text-emerald-600">
              <span className="h-2 w-2 rounded-full bg-emerald-600" />
              System operational
            </div>
          ) : (
            <div className="flex items-center gap-2 text-sm text-amber-600">
              <span className="h-2 w-2 rounded-full bg-amber-600" />
              System degraded — some features may be limited
            </div>
          )}
        </div>

        {/* Search */}
        <section className="mb-8 rounded-xl border border-border p-6 sm:p-8 shadow-sm">
          <h2 className="text-xl font-semibold mb-4">What are you looking for?</h2>
          <form onSubmit={handleSearch} className="relative max-w-2xl">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 size-5 text-muted-foreground" aria-hidden="true" />
            <input
              type="text"
              name="q"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-12 pr-10 py-4 rounded-xl border border-border focus-ring focus-ring-offset-background w-full text-lg"
              placeholder="e.g., Find me something to wear to a friend's wedding"
              aria-label="Describe what you're looking for"
            />
            <button
              type="submit"
              className="absolute right-3 top-1/2 -translate-y-1/2 rounded-xl bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
              aria-label="Search"
            >
              Search
            </button>
          </form>
        </section>

        {/* Suggested prompts */}
        <section className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Try these occasions</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {SUGGESTED_PROMPTS.map((prompt) => (
              <Link
                key={prompt.text}
                href={{
                  pathname: "/search",
                  query: { q: `Show me ${prompt.text.toLowerCase()}` },
                }}
                className="group block p-4 rounded-xl border border-border hover:border-primary/50 hover:bg-primary/5 transition-colors cursor-pointer"
              >
                <Search className="size-4 opacity-40 group-hover:opacity-0 mb-3" aria-hidden="true" />
                <p className="text-sm font-medium group-hover:text-primary transition-colors">
                  {prompt.text}
                </p>
                <ArrowRight className="size-3.5 opacity-0 group-hover:opacity-100 ml-1 transition-opacity" aria-hidden="true" />
              </Link>
            ))}
          </div>
        </section>

        {/* Featured products */}
        <section className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Featured collections</h2>
            <Link href="/search" className="text-sm font-medium text-primary hover:underline">
              View all
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {loading
              ? Array.from({ length: 8 }).map((_, i) => (
                  <ProductCardSkeleton key={i} />
                ))
              : products.length === 0
              ? <p className="col-span-full text-center text-muted-foreground">No products available.</p>
              : products.map((p) => (
                  <ProductCard
                    key={p.id}
                    product={{
                      id: p.id,
                      name: p.name,
                      brand: p.brand,
                      price: p.min_price ?? null,
                      currency: p.currency,
                      image: (p.image_references?.[0] || "https://placehold.co/400x400/e2e8f0/475569?text=Product"),
                      styleTags: p.style_tags || undefined,
                      occasionTags: p.occasion_tags || undefined,
                    }}
                  />
                ))}
          </div>
        </section>
      </main>
    </div>
  );
}
