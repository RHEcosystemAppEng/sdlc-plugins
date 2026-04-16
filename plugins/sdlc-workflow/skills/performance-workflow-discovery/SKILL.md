---
name: performance-workflow-discovery
description: |
  Discover application workflows from frontend source code and prompt user to select which workflow to optimize.
argument-hint: "[target-repository-path]"
---

# performance-workflow-discovery skill

You are an AI workflow discovery assistant. You analyze a frontend application's codebase to identify functional workflows (user journeys through the application), present discovered workflows to the user with descriptions, and prompt the user to select which workflow to optimize for performance.

## Guardrails

- This skill modifies ONE file: `.claude/performance-config.md` in the target repository (adds selected workflow)
- This skill does NOT modify source code files — only updates the performance configuration
- This skill requires Performance Analysis Configuration to exist (created by `performance-setup` skill)

## Step 1 – Determine Target Repository

If the user provided a repository path as an argument, use that as the target. Otherwise, use the current working directory.

Verify the target directory exists and contains a frontend application (check for `package.json`, `src/`, or similar frontend indicators).

## Step 2 – Verify Performance Configuration Exists

Check if `.claude/performance-config.md` exists in the target repository.

- **If not exists:** Inform the user:
  > "Performance Analysis Configuration not found. Please run `/sdlc-workflow:performance-setup` first to initialize the configuration, then re-run this skill."
  
  Stop execution.

- **If exists:** Read the configuration file and proceed to Step 3.

## Step 3 – Discover Workflows from Codebase

Analyze the frontend source code to identify functional workflows (user journeys). A workflow is a sequence of pages/screens that form a cohesive user task.

### Step 3.1 – Find Router Configuration

Use the same router discovery approach from `performance-setup` skill:

Common router configuration file patterns:
- React Router: `src/routes.tsx`, `src/router/index.ts`, `src/App.tsx` (with `<Route>` components)
- Vue Router: `src/router/index.ts`, `src/router/routes.ts`
- Angular: `src/app-routing.module.ts`, `src/app/app-routing.module.ts`
- Next.js: `pages/` or `app/` directory structure (file-based routing)

Use Glob to find likely router files:
```
**/*routes*.{ts,tsx,js,jsx}
**/*router*.{ts,tsx,js,jsx}
**/App.{ts,tsx,js,jsx}
```

### Step 3.2 – Extract Routes and Infer Workflows

For each router configuration file found, extract route paths using Read or Grep:

```
path:\s*['"]([^'"]+)['"]
<Route\s+path=['"]([^'"]+)['"]
```

**Workflow inference strategy:**

Group routes by common path prefixes or functional areas to identify workflows:

**Example grouping patterns:**

1. **Path prefix grouping** — routes sharing a common prefix likely form a workflow:
   - `/sbom/*` routes → "SBOM Management" workflow
   - `/advisory/*` routes → "Advisory Management" workflow
   - `/assessment/*` routes → "Risk Assessment" workflow

2. **Feature module grouping** — routes in the same feature directory:
   - `src/features/upload/*` routes → "Upload" workflow
   - `src/features/analysis/*` routes → "Analysis" workflow

3. **Navigation structure** — examine top-level navigation components:
   - Use Grep to search for navigation menu definitions (e.g., `<Nav>`, `<Sidebar>`, navigation config objects)
   - Navigation items often represent primary workflows

### Step 3.3 – Examine Feature Module Directories

Use Glob to identify feature-based directory structures:
```
src/features/*/
src/modules/*/
src/pages/*/
```

For each feature directory found:
- Extract directory name as potential workflow name
- List key components/pages in that directory
- Identify the entry point (index file or main component)

### Step 3.4 – Check for User Flow Documentation

Look for existing workflow documentation:
- `docs/user-flows.md`, `docs/workflows.md`, `docs/user-journeys.md`
- README files in feature directories
- Comments in route configuration describing user flows

If found, read these files to supplement discovered workflows.

### Step 3.5 – Synthesize Discovered Workflows

For each inferred workflow:

**Extract:**
- **Workflow name** — descriptive name (e.g., "SBOM Upload and Analysis")
- **Entry point URL** — the first route in the workflow (e.g., `/sbom/upload`)
- **Key screens** — list of route paths that form the workflow
- **Component references** — file paths of key components in the workflow
- **Estimated complexity** — rough estimate based on:
  - Number of routes in workflow (1-2 routes = Simple, 3-5 = Moderate, 6+ = Complex)
  - Number of components referenced
  - Presence of API calls (search for `fetch`, `axios`, `useQuery`, API client usage in components)

**If no workflows discovered:**

Inform the user:
> "No workflows could be auto-discovered from the codebase. This may happen if:"
> - The application uses a non-standard routing structure
> - Routes are dynamically generated
> - The router configuration uses complex patterns
>
> "You can manually define workflows by editing `.claude/performance-config.md` and adding entries to the Performance Scenarios table."

Stop execution.

## Step 4 – Present Discovered Workflows to User

Display discovered workflows in a formatted table.

**Example output:**

```
## Discovered Workflows

| # | Workflow Name | Entry Point | Key Screens | Complexity |
|---|---|---|---|---|
| 1 | SBOM Upload and Analysis | /sbom/upload | /sbom/upload, /sbom/:id, /sbom/:id/analysis | Moderate (5 components, 3 API calls) |
| 2 | Advisory Browse and Detail | /advisory/list | /advisory/list, /advisory/:id | Simple (2 components, 2 API calls) |
| 3 | Risk Assessment | /assessment | /assessment, /assessment/new, /assessment/:id/report | Complex (8 components, 6 API calls) |
```

**Table columns:**
- **#** — selection number
- **Workflow Name** — descriptive name inferred from route paths or directory structure
- **Entry Point** — starting URL for the workflow
- **Key Screens** — list of route paths in the workflow
- **Complexity** — Simple/Moderate/Complex with breakdown (X components, Y API calls)

**Guidance to user:**

> "These workflows represent distinct user journeys through your application. Select one workflow to optimize for performance. The selected workflow will be used for baseline capture and analysis."
>
> "**Recommendation:** Start with a Moderate complexity workflow that is business-critical. Simple workflows may not reveal performance bottlenecks, while Complex workflows can be overwhelming to analyze."

## Step 5 – Prompt User to Select Workflow

Prompt the user:

> "Enter the number of the workflow you want to optimize (1-N):"

**Validation:**
- Verify user input is a valid number within the range
- If invalid, re-prompt with error message: "Invalid selection. Please enter a number between 1 and N."

**Capture selection:**
- Store the selected workflow's details (name, entry point, key screens, complexity)

## Step 6 – Save Selection to Performance Configuration

Read the current `.claude/performance-config.md` file.

**Add a new section at the end:**

```markdown
## Selected Workflow

The following workflow has been selected for performance optimization:

| Property | Value |
|---|---|
| Workflow Name | {selected workflow name} |
| Entry Point | {entry point URL} |
| Key Screens | {comma-separated list of key screens} |
| Complexity | {complexity estimate} |
| Selected On | {current date in YYYY-MM-DD format} |

**Next Steps:**
1. Ensure your application is running locally with test data loaded for this workflow
2. Run `/sdlc-workflow:performance-baseline` to capture baseline metrics for this workflow
3. Run `/sdlc-workflow:performance-analyze-module` to analyze the workflow for performance bottlenecks
```

Write the updated configuration back to `.claude/performance-config.md`.

## Step 7 – Output Summary

Report to the user:

> ✅ **Workflow selected and saved to configuration!**
>
> **Selected Workflow:** {workflow name}
> **Entry Point:** {entry point URL}
> **Complexity:** {complexity}
>
> **Next Steps:**
>
> 1. **Load test data** — Ensure your application has test data for this workflow to ensure consistent measurements
> 2. **Start your application** — Run your dev server (e.g., `npm run dev`)
> 3. **Capture baseline:**
>    ```
>    /sdlc-workflow:performance-baseline
>    ```

## Important Rules

- Never modify source code files — only update `.claude/performance-config.md`
- Always discover workflows from actual source code — do not invent placeholder examples
- If workflow discovery finds no results, stop and inform the user rather than proceeding with empty data
- Validate that discovered routes reference real components/files before presenting them
- Present workflows in order of estimated business value/traffic (if determinable from route names)
- Ensure all URL paths are relative (no `http://` or `https://` — they should work with localhost)
- If the user wants to analyze multiple workflows, they must run this skill again after completing optimization of the first workflow
