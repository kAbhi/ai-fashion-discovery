import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { ProductCard } from "@/components/ui/product-card";

const mockProduct = {
  id: "test-product-1",
  name: "Test Cotton Kurta",
  brand: "TestBrand",
  price: 1499,
  currency: "INR",
  image: "https://example.com/kurta.jpg",
  styleTags: ["casual", "traditional"],
  occasionTags: ["casual", "office"],
};

describe("ProductCard", () => {
  it("renders product name and brand", () => {
    render(<ProductCard product={mockProduct} />);
    expect(screen.getByText("Test Cotton Kurta")).toBeInTheDocument();
    expect(screen.getByText("TestBrand")).toBeInTheDocument();
  });

  it("renders price", () => {
    render(<ProductCard product={mockProduct} />);
    expect(screen.getByText("1499 INR")).toBeInTheDocument();
  });

  it("renders save button", () => {
    render(<ProductCard product={mockProduct} />);
    expect(screen.getByRole("button", { name: /save/i })).toBeInTheDocument();
  });

  it("renders compare button", () => {
    render(<ProductCard product={mockProduct} />);
    expect(screen.getByRole("button", { name: /compare/i })).toBeInTheDocument();
  });

  it("shows saved state when isInWishlist is true", () => {
    render(<ProductCard product={mockProduct} isInWishlist />);
    expect(screen.getByText("Saved")).toBeInTheDocument();
  });
});
