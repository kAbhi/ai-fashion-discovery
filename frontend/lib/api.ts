/**
 * API client for backend communication.
 * Reads NEXT_PUBLIC_API_BASE_URL from environment.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export interface Product {
  id: string;
  name: string;
  brand: string;
  description?: string | null;
  category: string;
  subcategory?: string | null;
  gender_audience?: string | null;
  style_tags?: string[] | null;
  occasion_tags?: string[] | null;
  image_references?: string[] | null;
  variants?: Array<{
    id: string;
    product_id: string;
    size?: string | null;
    colour?: string | null;
    variant_attributes?: Record<string, unknown> | null;
  }>;
  merchant_listings?: Array<{
    id: string;
    product_id: string;
    merchant: string;
    current_price: number;
    original_price?: number | null;
    currency: string;
    availability?: string | null;
    purchase_url?: string | null;
  }>;
  min_price?: number | null;
  currency: string;
  created_at: string;
}

export interface PaginatedProducts {
  items: Product[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface HealthResponse {
  status: "ok" | "degraded" | "unreachable" | "misconfigured";
  environment: string;
  database: "ok" | "unavailable";
}

export interface ProductFilters {
  category?: string;
  subcategory?: string;
  brand?: string;
  gender?: string;
  occasion?: string;
  style?: string;
  colour?: string;
  min_price?: number;
  max_price?: number;
  q?: string;
  page?: number;
  page_size?: number;
}

async function fetchJson<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorBody = await response.text().catch(() => "");
    throw new Error(
      `API error: ${response.status} ${errorBody || response.statusText}`
    );
  }

  return response.json();
}

export async function getHealth(): Promise<HealthResponse> {
  return fetchJson<HealthResponse>("/health");
}

export async function listProducts(
  filters: ProductFilters = {}
): Promise<PaginatedProducts> {
  const params = new URLSearchParams();
  if (filters.category) params.set("category", filters.category);
  if (filters.subcategory) params.set("subcategory", filters.subcategory);
  if (filters.brand) params.set("brand", filters.brand);
  if (filters.gender) params.set("gender", filters.gender);
  if (filters.occasion) params.set("occasion", filters.occasion);
  if (filters.style) params.set("style", filters.style);
  if (filters.colour) params.set("colour", filters.colour);
  if (filters.min_price !== undefined)
    params.set("min_price", String(filters.min_price));
  if (filters.max_price !== undefined)
    params.set("max_price", String(filters.max_price));
  if (filters.q) params.set("q", filters.q);
  if (filters.page) params.set("page", String(filters.page));
  if (filters.page_size) params.set("page_size", String(filters.page_size));

  return fetchJson<PaginatedProducts>(`/api/v1/products?${params.toString()}`);
}

export async function getProduct(productId: string): Promise<Product> {
  return fetchJson<Product>(`/api/v1/products/${productId}`);
}

export async function getSimilarProducts(productId: string): Promise<Product[]> {
  return fetchJson<Product[]>(`/api/v1/products/${productId}/similar`);
}

export async function getMerchantListings(productId: string) {
  return fetchJson(
    `/api/v1/merchant-listings?product_id=${encodeURIComponent(productId)}`
  );
}

export { API_BASE_URL };
