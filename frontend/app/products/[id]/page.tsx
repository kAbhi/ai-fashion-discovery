import { notFound } from "next/navigation";
import ProductDetailClient from "./product-detail-client";
import { getProduct } from "@/lib/api";

export default async function ProductDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  const product = await getProduct(id).catch(() => null);

  if (!product) {
    notFound();
  }

  return <ProductDetailClient product={product} />;
}
