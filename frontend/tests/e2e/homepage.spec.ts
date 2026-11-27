import { test, expect } from "@playwright/test";

test("homepage loads successfully", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle(/Fashion Discovery/);
  await expect(page.getByRole("heading", { name: /Fashion Discovery/i })).toBeVisible();
});

test("homepage has search input", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByLabel(/Describe what you're looking for/i)).toBeVisible();
});

test("search submission navigates to results page", async ({ page }) => {
  await page.goto("/");
  await page.getByLabel(/Describe what you're looking for/i).fill("wedding outfit");
  await page.getByRole("button", { name: /Search/i }).click();
  await expect(page).toHaveURL(/\/search/);
});

test("suggested prompts are displayed", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("Wedding guest outfits")).toBeVisible();
  await expect(page.getByText("Goa vacation wardrobe")).toBeVisible();
  await expect(page.getByText("Office wear upgrade")).toBeVisible();
});

test("system status component is visible", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("System status")).toBeVisible();
});

test("homepage is responsive on mobile", async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Fashion Discovery/i })).toBeVisible();
  await expect(page.getByLabel(/Describe what you're looking for/i)).toBeVisible();
});
