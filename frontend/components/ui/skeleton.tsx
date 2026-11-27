import * as React from "react";

export function Skeleton(props: { className?: string }) {
  return (
    <div
      className={props.className}
      style={{
        background: "linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%)",
        backgroundSize: "200% 100%",
        animation: "skeleton-shimmer 1.5s infinite",
        borderRadius: "0.375rem",
      }}
    />
  );
}

export function ProductCardSkeleton() {
  return (
    <div className="rounded-xl bg-card p-4 shadow-sm animate-pulse">
      <div className="aspect-square rounded-lg bg-muted mb-3 w-full" />
      <div className="h-4 w-3/4 rounded bg-muted mb-1" />
      <div className="h-3 w-1/2 rounded bg-muted mb-2" />
      <div className="h-8 w-full rounded bg-muted mb-3" />
      <div className="flex gap-2">
        <div className="h-8 w-1/3 rounded bg-muted" />
        <div className="h-8 w-1/3 rounded bg-muted" />
      </div>
    </div>
  );
}
