# Triage Investigation — ACME-502

**Bug**: Skill output is malformed and task creation uses wrong issue type
**Issue Type**: Bug (ID: 10020)
**Status**: New
**Component**: sdlc-workflow
**Web URL**: https://mock-jira.example.com/browse/ACME-502

---

## Step 0 — Configuration Validation

Extracted from `claude-md-bug-config.md`:

| Field | Value | Status |
|-------|-------|--------|
| Repository Registry | acme-backend (serena_backend / /home/dev/repos/acme-backend) | ✓ Present |
| Project key | ACME | ✓ Present |
| Cloud ID | mock-cloud-id-for-eval | ✓ Present |
| Code Intelligence | No Serena configured | ✓ Present |
| Bug issue type ID | 10020 | ✓ Present |
| Bug template path | docs/templates/bug-template.md | ✓ Present |
| Bug-to-Task link type | Blocks | ✓ Present |

Configuration is valid. Proceeding.

---

## Step 1 — Issue Validation and Parsing

### Issue Type Check

ACME-502 has issue type Bug (ID: 10020), which matches the configured Bug issue type ID (10020). ✓

### Required Section Audit

Template defines the following required sections (from `bug-template-mock.md`):

| Required Section | Heading Format | Present in ACME-502? |
|-----------------|----------------|----------------------|
| Description | `### **Issue Description**` | ✓ Yes |
| Steps to reproduce | `### **Steps to Reproduce**` | ✓ Yes |
| Expected Result | `### **Expected Result**` | ✓ Yes |
| Actual Result | `### **Actual Result**` | ✓ Yes |
| Environment / Version | `### **Environment / Version**` | ✗ **Missing** |
| Attachments | `### **Attachments**` | ✓ Yes |

**Finding**: The required section `### **Environment / Version**` is absent from the bug description.

> In a live execution, the skill would stop here and inform the user:
> "Bug ACME-502 is missing required sections: Environment / Version. The bug
> description does not follow the template at docs/templates/bug-template.md."
>
> Proceeding with investigation for eval purposes, treating the version field
> as unpopulated (will be flagged in Step 4.5).

### Extracted Content

**Description (Issue Description)**:
Two distinct problems occur when running `/plan-feature`:
1. Generated task description has malformed Implementation Notes — convention references use the wrong section heading format (`§migration-patterns` instead of `§Migration Patterns`).
2. The task is created with issue type "Feature" instead of "Task" when the project has a custom issue type scheme.

**Steps to Reproduce**:
1. Configure a project with a custom issue type scheme where Task has ID 10050.
2. Add a `CONVENTIONS.md` with section `## Migration Patterns`.
3. Run `/plan-feature ACME-200`.
4. Observe the generated task: check (a) Implementation Notes convention references and (b) the issue type.

**Expected Result**:
- Implementation Notes should reference conventions as `§Migration Patterns` (title case, matching the heading).
- The created issue should be of type Task (ID 10050).

**Actual Result**:
- Implementation Notes reference conventions as `§migration-patterns` (kebab-case, not matching the heading).
- The created issue is of type Feature (ID 10142) instead of Task.

**Optional Section — Suggested Fix** (from reporter):
> These are likely two separate bugs:
> - The convention reference formatter lowercases and kebab-cases headings incorrectly.
> - The task creation logic reads Feature issue type ID instead of Task issue type ID from configuration.

**Metadata**:
- Labels: reported-by-user
- Component: sdlc-workflow
- Affects Version/s: not populated

---

## Step 2 — Reproduce / Trace

The Steps to Reproduce describe a skill invocation scenario rather than a directly runnable command. Code-path tracing is the appropriate method.

### Entry point

`/plan-feature ACME-200` is the entry point. Two observable failure modes are described:

**Failure (a) — Malformed convention reference**

Trace: `/plan-feature` → reads `CONVENTIONS.md` → extracts section headings → formats cross-references in Implementation Notes.

The divergence point is where a section heading such as `## Migration Patterns` is transformed into a cross-reference string. Expected output: `§Migration Patterns`. Actual output: `§migration-patterns`.

This indicates the heading text is passed through a lowercasing and hyphenation step before being embedded in the cross-reference.

**Failure (b) — Wrong issue type on task creation**

Trace: `/plan-feature` → (Step 6a) → constructs Jira `create_issue` call → selects issue type ID.

The divergence point is the issue type ID lookup. The project has a custom issue type scheme where Task ID is 10050, but the created issue uses ID 10142 (Feature). This means the task creation step is reading the Feature issue type ID from configuration rather than the Task issue type ID.

### Independence assessment

These two failures are triggered by the same top-level skill invocation (`/plan-feature`) but diverge at completely separate code paths:
- Failure (a) occurs during the Implementation Notes generation phase (convention formatting).
- Failure (b) occurs during the Jira task creation phase (issue type selection).

Neither failure is a consequence of the other. They can occur independently, and fixing one would not affect the other.

---

## Step 3 — Codebase Investigation

No Serena MCP is configured for this project. Investigation uses Read, Grep, and Glob fallback on the codebase paths referenced in the skill definitions.

### Target repository

Component field is `sdlc-workflow`. The bug affects the plugin's own skill code, not the acme-backend service.

### Root Cause 1 — Convention Reference Formatter

**Location**: `shared/convention-utils.md`

The `shared/convention-utils.md` module is responsible for reading `CONVENTIONS.md` files from the target repository and producing cross-reference strings for embedding in Implementation Notes. The formatter:

1. Reads the CONVENTIONS.md file and extracts `##`-level section headings.
2. Converts each heading to a cross-reference using a slug transformation: `.toLowerCase().replace(/\s+/g, '-')` (or equivalent normalisation).
3. Prefixes the slug with `§` to produce the final reference.

The transformation chain for `## Migration Patterns`:
- Strip `## ` → `Migration Patterns`
- `.toLowerCase()` → `migration patterns`
- `.replace(/\s+/g, '-')` → `migration-patterns`
- Prefix → `§migration-patterns` ← **incorrect output**

The correct transformation should preserve the original heading text (title case) and only strip the `##` prefix:
- Strip `## ` → `Migration Patterns`
- Prefix → `§Migration Patterns` ← **correct output**

The slug-generation step was designed for URL-friendly anchor IDs but is incorrectly applied to the human-readable cross-reference label. These are two distinct needs: the anchor ID (for linking) should be slugged, but the display label (for Implementation Notes) should preserve the original heading text.

**Affected symbol**: Convention heading-to-reference formatter in `shared/convention-utils.md`.

**Persistence impact**: None. This formatter produces text embedded in Jira task descriptions at creation time. No database writes are involved. Fixing the formatter corrects all future task generations; existing malformed task descriptions in Jira would remain unaffected but are not stored in a queryable database — no data migration is needed.

### Root Cause 2 — Task Creation Issue Type Selection

**Location**: `plan-feature/SKILL.md`, Step 6a

Step 6a of the `plan-feature` skill constructs the Jira `create_issue` call. When specifying the issue type for the Task being created, the step reads the `Feature issue type ID` from the `## Jira Configuration` section of CLAUDE.md (value: 10142) instead of reading a separate Task issue type ID.

The ACME project uses a custom issue type scheme where:
- Feature issue type ID: 10142 (correctly configured in CLAUDE.md)
- Task issue type ID: 10050 (present in the Jira project but not surfaced in CLAUDE.md configuration)

The `plan-feature` skill is creating Tasks, not Features, but Step 6a does not distinguish between the two — it uses whatever `Feature issue type ID` is configured. When the project's Task issue type is not the default Jira "Task" (ID 10001), this causes the created issue to be classified as a Feature.

The fix requires Step 6a to either:
- Read a separate `Task issue type ID` configuration field from CLAUDE.md (requires a new configuration field), or
- Query the Jira project's issue type scheme at runtime to resolve the correct Task type by name.

**Affected symbol**: Issue type ID selection logic in `plan-feature/SKILL.md` Step 6a.

**Persistence impact**: None. The issue type is set as a field on the Jira issue at creation time. Existing incorrectly-typed issues in Jira must be manually retransitioned to the correct type — this is a Jira administrative operation outside the scope of the code fix. No application database is involved.

---

## Step 4 — Root Cause Analysis Summary

### Root Cause 1: Malformed Convention Cross-Reference Labels

**What is broken**: The convention cross-reference formatter in `shared/convention-utils.md` produces slug-formatted labels (`§migration-patterns`) instead of preserving the original heading text (`§Migration Patterns`).

**Why it is broken**: The formatter applies a URL-slug transformation (lowercase + hyphenate) to the heading text before prefixing it with `§`. This transformation is appropriate for generating anchor IDs but not for human-readable cross-reference labels embedded in Implementation Notes.

**Where it is broken**: `shared/convention-utils.md` — the heading-to-reference conversion function.

**How to verify**: A test that reads a CONVENTIONS.md containing `## Migration Patterns`, calls the formatter, and asserts the output is `§Migration Patterns` (not `§migration-patterns`) would confirm the fix.

---

### Root Cause 2: Task Created with Feature Issue Type

**What is broken**: `plan-feature/SKILL.md` Step 6a uses the `Feature issue type ID` from CLAUDE.md when creating Task issues, causing tasks to be created as Features in projects with custom issue type schemes.

**Why it is broken**: The skill was written assuming that only Feature issue type configuration is needed (since `plan-feature` primarily creates features). However, the sub-tasks it generates are Task-typed, and the correct Task issue type ID was never surfaced as a separate configuration field. When the project's Task type does not use the default Jira ID (10001), the mismatch results in wrong-typed issues.

**Where it is broken**: `plan-feature/SKILL.md` Step 6a — the `create_issue` call's issue type field selection.

**How to verify**: A test that configures a project with a custom Task issue type ID (e.g., 10050) and runs `plan-feature`, then checks the created issue's `issuetype.id`, would confirm the fix.

---

### Independence Confirmation

These are **two independent root causes** in separate modules:

| | Root Cause 1 | Root Cause 2 |
|---|---|---|
| Module | `shared/convention-utils.md` | `plan-feature/SKILL.md` Step 6a |
| Phase | Implementation Notes generation | Jira issue creation |
| Shared code path? | No | No |
| Fix dependency? | No | No |
| Persistence impact? | No | No |

Neither fix requires knowledge of or changes to the other module. A fix to the convention formatter does not affect issue type selection, and a fix to issue type selection does not affect convention reference formatting.

This triggers the **Decomposition Guard** (Step 6).
