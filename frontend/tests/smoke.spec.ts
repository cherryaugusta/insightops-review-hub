import { test, expect } from "@playwright/test";

test("InsightOps smoke flow", async ({ page }) => {
  const runId = Date.now().toString();

  await page.goto("/login");

  await page.getByLabel("Username").fill("demoanalyst");
  await page.getByLabel("Password").fill("StrongPassword123!");
  await page.getByRole("button", { name: "Sign in" }).click();

  await expect(page).toHaveURL(/\/dashboard/);
  await expect(page.getByRole("main").getByRole("heading", { name: "Dashboard" })).toBeVisible();

  await page.goto("/workspaces/new");
  await page.getByLabel("Title").fill(`Playwright Workspace ${runId}`);
  await page.getByLabel("Slug").fill(`playwright-workspace-${runId}`);
  await page.getByLabel("Description").fill("Workspace created by smoke flow.");
  await page.getByRole("button", { name: "Create workspace" }).click();

  await expect(page).toHaveURL(/\/workspaces\/\d+$/);
  const workspaceDetailUrl = page.url();

  await page.getByRole("link", { name: "Sources" }).click();
  await page.getByRole("link", { name: "Create source" }).click();
  await page.getByLabel("Title").fill("Playwright Source");
  await page.getByLabel("Source type").selectOption("note");
  await page.getByLabel("Filename").fill("playwright-source.txt");
  await page
    .getByLabel("Raw text")
    .fill(
      "Customer risk is increasing because service delays, complaint volume, and review bottlenecks are visible in the source material. Review gates and evidence visibility are required.",
    );
  await page.getByRole("button", { name: "Create source" }).click();

  await expect(page.getByText("Generate excerpts")).toBeVisible();
  await page.getByRole("button", { name: "Generate excerpts" }).click();
  await expect(page.getByRole("heading", { name: "Excerpts" })).toBeVisible();

  await page.goto(page.url().replace(/\/sources\/\d+$/, "/briefings/new"));
  await page.getByLabel("Title").fill("Playwright Briefing");
  await page.getByLabel("Question").fill("What are the main customer risks?");
  await page.getByLabel("Audience").fill("Operations Lead");
  await page.getByLabel("Goal").fill("Prepare a concise executive briefing.");
  await page.getByRole("button", { name: "Create briefing" }).click();

  await page.getByRole("button", { name: "Generate answer" }).click();
  await expect(page.getByRole("heading", { name: "Answers" })).toBeVisible();

  await page.getByRole("link", { name: "Open answer" }).first().click();
  await expect(page.getByRole("heading", { name: "Citations" })).toBeVisible();

  await page.getByRole("link", { name: "Open evaluation" }).click();
  await expect(page.getByRole("main").getByRole("heading", { name: "Evaluation detail" })).toBeVisible();

  await page.goto(workspaceDetailUrl);
  await page.getByRole("link", { name: "Audit", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Audit timeline" })).toBeVisible();
});
