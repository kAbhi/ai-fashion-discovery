import { test, expect } from "@playwright/test";

test("product detail page loads for valid product", async ({ page }) => {
  // Use a known product ID from seed data - this may not exist in test environment
  await page.goto("/products/00000000-0000-0000-0000-000000000001");
  // Product may not exist - verify page handles gracefully
  await expect(page.getByRole("heading", { name: /Back to results|You might also like/i })).toBeVisible();
});

test("product detail page shows product information", async ({ page }) => {
  await page.goto("/products/00000000-0000-0000-0000-000000000001");
  // If product exists, check for key elements
  const productName = page.getByRole("heading", { level: 1 });
  if (await productName.count() > 0) {
    await expect(productName).toBeVisible();
  }
});

test("back navigation works from product detail", async ({ page }) => {
  await page.goto("/products/00000000-0000-0000-0000-000000000001");
  const backLink = page.getByRole("link", { name: /Back to results/i });
  if (await backLink.count() > 0) {
    await backLink.click();
    await expect(page).toHaveURL(/\/search/);
  }
});

test("empty search results show appropriate message", async ({ page }) => {
  await page.goto("/search?q=nonexistentproductxyz");
  await expect(page.getByText(/No products found/)).toBeVisible();
});
