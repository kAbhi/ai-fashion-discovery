"use client";

import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";
import { ArrowLeft, Sparkles } from "lucide-react";
import { Navigation } from "@/components/navigation";
import { Product } from "@/lib/api";


export default function ProductDetailClient({
  product,
}: {
  product: Product;
}) {

  const primaryImage =
    product.image_references?.[0] ||
    "https://placehold.co/800x800/e2e8f0/475569?text=Product";
  const merchant = product.merchant_listings?.[0];

  return (
    <div className="min-h-dvh bg-background">
      <Navigation />

      <main className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-8">
        <Link
          href="/search"
          className="inline-flex items-center gap-1.5 text-sm font-medium text-muted-foreground hover:text-foreground mb-6"
        >
          <ArrowLeft className="size-4" />
          Back to results
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Image gallery */}
          <div className="lg:col-span-8 space-y-4">
            <div
              className="relative aspect-square rounded-xl overflow-hidden bg-muted"
            >
              <Image
                src={primaryImage}
                alt={product.name}
                fill
                sizes="(max-width: 768px) 100vw, 50vw"
                className="object-cover"
                priority
                loading="eager"
              />
              {product.image_references?.length && product.image_references.length > 1 && (
                <div className="absolute inset-0 flex items-end justify-center p-2 gap-2">
                  {product.image_references.slice(0, 4).map((img, i) => (
                    <Image
                      key={i}
                      src={img}
                      alt=""
                      className="h-12 w-12 rounded-full object-cover border-2 border-white/80 bg-white shadow-sm"
                      sizes="48px"
                    />
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Product info */}
          <div className="lg:col-span-4 space-y-6">
            <div>
              <div className="flex items-center gap-2 text-xs text-muted-foreground uppercase tracking-wider mb-2">
                <span>{product.category}</span>
                {product.subcategory && <span>•</span>}
                {product.subcategory}
              </div>
              <h1 className="text-3xl font-bold tracking-tight mb-2">
                {product.name}
              </h1>
              <p className="text-xl font-semibold text-foreground">{product.brand}</p>
              <p className="mt-4 text-muted-foreground leading-relaxed">
                {product.description || "No description available."}
              </p>
            </div>

            {/* Price */}
            <div className="pt-4 border-t border-border">
              <p className="text-xs text-muted-foreground uppercase tracking-wider">Price</p>
              <div className="flex items-baseline gap-1 mt-1">
                <span className="text-2xl font-bold">
                  {merchant?.current_price != null
                    ? merchant.current_price
                    : product.min_price ?? "—"}{" "}
                  {merchant?.currency || product.currency || "₹"}
                </span>
                {merchant?.original_price && merchant.original_price > merchant.current_price && (
                  <span className="text-sm text-muted-foreground line-through">
                    {merchant.original_price} {merchant.currency || "₹"}
                  </span>
                )}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                {merchant?.availability || "Availability information not provided"}
              </p>
            </div>

            {/* Merchant */}
            {merchant && (
              <div className="pt-4 border-t border-border">
                <p className="text-xs text-muted-foreground uppercase tracking-wider">Merchant</p>
                <div className="flex items-center gap-2 mt-1">
                  <Sparkles className="size-4" />
                  <span className="text-sm font-medium">{merchant.merchant}</span>
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="pt-4 border-t border-border space-y-3">
              {merchant?.purchase_url && (
                <a
                  href={merchant.purchase_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full py-3 px-4 rounded-xl bg-primary text-primary-foreground text-center font-medium hover:bg-primary/90 transition-colors"
                >
                  Buy from {merchant.merchant}
                </a>
              )}
              <button
                className="block w-full py-3 px-4 rounded-xl border border-border text-center font-medium hover:bg-muted transition-colors"
                onClick={() => {
                  // Save to wishlist - Phase 3
                }}
              >
                Save to wishlist
              </button>
            </div>

            {/* Attributes */}
            <div className="pt-4 border-t border-border">
              <p className="text-xs text-muted-foreground uppercase tracking-wider">Product details</p>
              <div className="mt-2 space-y-2 text-sm">
                {product.gender_audience && (
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Gender</span>
                    <span>{product.gender_audience}</span>
                  </div>
                )}
                {product.subcategory && (
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Subcategory</span>
                    <span>{product.subcategory}</span>
                  </div>
                )}
                {product.style_tags && product.style_tags.length > 0 && (
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Styles</span>
                    <span>{product.style_tags.join(", ")}</span>
                  </div>
                )}
                {product.occasion_tags && product.occasion_tags.length > 0 && (
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Occasions</span>
                    <span>{product.occasion_tags.join(", ")}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Variants */}
            {product.variants && product.variants.length > 0 && (
              <div className="pt-4 border-t border-border">
                <p className="text-xs text-muted-foreground uppercase tracking-wider">Available variants</p>
                <div className="mt-2 grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {product.variants.map((v) => (
                    <button
                      key={`${v.size}-${v.colour}`}
                      className="px-3 py-2 rounded-lg border border-border text-sm hover:bg-muted transition-colors"
                    >
                      {v.size}{v.colour ? ` / ${v.colour}` : ""}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Similar products */}
        <section className="mt-12">
          <h2 className="text-xl font-semibold mb-4">You might also like</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="rounded-xl bg-card p-4 shadow-sm animate-pulse">
                <div className="aspect-square rounded-lg bg-muted mb-3 w-full" />
                <div className="h-4 w-3/4 rounded bg-muted mb-1" />
                <div className="h-3 w-1/2 rounded bg-muted mb-2" />
                <div className="h-8 w-full rounded bg-muted mb-3" />
                <div className="flex gap-2">
                  <div className="h-8 w-1/3 rounded bg-muted" />
                  <div className="h-8 w-1/3 rounded bg-muted" />
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
