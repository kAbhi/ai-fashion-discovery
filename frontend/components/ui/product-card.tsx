import * as React from "react";
import Image from "next/image";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
import { Button } from "./button";

const productCardVariants = cva(
  "group rounded-xl bg-card p-4 shadow-sm transition-all hover:shadow-md",
  {
    variants: {
      variant: {
        default: "",
        elevated: "border-border",
        compact: "py-3",
      },
      size: {
        default: "h-80",
        sm: "h-64",
        lg: "h-96",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

interface ProductCardProps {
  product: {
    id: string;
    name: string;
    brand: string;
    price: number | null;
    currency: string;
    image: string;
    styleTags?: string[] | undefined;
    occasionTags?: string[] | undefined;
  };
  onAddToWishlist?: () => void;
  onCompare?: () => void;
  isInWishlist?: boolean;
}

export function ProductCard({
  product,
  onAddToWishlist,
  onCompare,
  isInWishlist = false,
}: ProductCardProps) {
  const { styleTags, occasionTags } = product;
  const tagsValid = styleTags && styleTags.length > 0;
  const occasionsValid = occasionTags && occasionTags.length > 0;

  return (
    <div
      className={cn(productCardVariants({ variant: "default", size: "default" }))}
      aria-label={`View ${product.name} by ${product.brand}`}
    >
      <Image
        src={product.image}
        alt={`${product.name} by ${product.brand}`}
        className="aspect-square rounded-t-lg object-cover mb-3 w-full"
        width={400}
        height={400}
      />

      <h3 className="text-sm font-medium line-clamp-2">{product.name}</h3>
      <p className="text-xs text-muted-foreground line-clamp-1">{product.brand}</p>

      <div className="mt-3 flex items-baseline gap-1">
        {product.price !== null && (
          <p className="text-lg font-medium">{product.price} {product.currency || "₹"}</p>
        )}
      </div>

      <div className="mt-4 flex flex-col gap-2">
        {tagsValid && (
          <div className="flex flex-wrap gap-1 text-xs">
            {styleTags!.map((tag) => (
              <span key={tag} className="px-2 py-0.5 rounded bg-muted/30 text-muted-foreground">
                {tag}
              </span>
            ))}
          </div>
        )}
        {occasionsValid && (
          <div className="flex flex-wrap gap-1 text-xs">
            {occasionTags!.map((tag) => (
              <span key={tag} className="px-2 py-0.5 rounded bg-primary/10 text-primary">
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="mt-4 pt-4 border-t border-border">
        <Button
          variant="outline"
          size="sm"
          onClick={onAddToWishlist}
          className="w-full"
        >
          {isInWishlist ? (
            <span className="align-middle">
              <i className="check size-3" aria-hidden="true" />
              Saved
            </span>
          ) : (
            <span className="align-middle">
              <i className="plus size-3" aria-hidden="true" />
              Save
            </span>
          )}
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={onCompare}
          className="mt-1 w-full text-sm"
          aria-label="Compare this product"
        >
          Compare
        </Button>
      </div>
    </div>
  );
}
