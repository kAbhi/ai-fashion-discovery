/**
 * Public (browser-visible) runtime configuration.
 *
 * NEXT_PUBLIC_API_BASE_URL is inlined at build time, so it must be set per
 * environment (local .env.local, Vercel Preview, Vercel Production).
 * There is deliberately no localhost fallback: a missing value is surfaced
 * as a configuration error instead of silently calling the wrong host.
 */
export function getApiBaseUrl(): string | null {
  const value = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!value) return null;
  return value.replace(/\/+$/, "");
}
