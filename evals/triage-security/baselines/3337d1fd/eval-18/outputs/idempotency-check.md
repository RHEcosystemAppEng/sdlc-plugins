# Idempotency Check: TC-8001 (Re-Run)

This document analyzes all pre-existing triage artifacts detected on TC-8001 during a second invocation of `triage-security`. Each step that would normally produce a Jira mutation is evaluated against the current issue state to determine whether the mutation should be executed or skipped.

## Summary

**All triage artifacts from the prior run are already present.** The re-run detects every artifact and skips all mutations. No new Jira writes are produced.

---

## Step 0.7 -- Assign and Transition

| Check | Current State | Action |
|-------|---------------|--------|
| Assignee | engineer-a@example.com (already assigned) | **Skip** -- re-assignment to the same user is a no-op |
| Status | In Progress | **Skip** -- issue is already past "Assigned" status; transition is not needed (the skill only transitions to Assigned if the issue is in New status, and skips silently for any later status) |

**Artifact detected**: Issue is already assigned and past the Assigned status. No mutation required.

## Step 1 -- Data Extraction

Data extraction is a read-only step. It produces the same parsed CVE data table regardless of whether it is the first or Nth invocation. No mutations occur here.

**Existing comments detected**:

| Comment | Presence | Implication |
|---------|----------|-------------|
| Description digest (`sha256-md:a1b2c3d4...`) | Present (2026-07-01T10:00:00Z) | Prior run already posted the digest -- indicates prior triage completed Step 1 |
| Post-triage summary | Present (2026-07-01T10:01:00Z) | Prior run completed all steps including the final summary |

## Step 3 -- Affects Versions Correction

| Check | Current State | Action |
|-------|---------------|--------|
| Current Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 | Matches the version impact analysis |
| Expected Affects Versions (scoped to 2.2.x stream) | RHTPA 2.2.0, RHTPA 2.2.1 | Same as current |

**Artifact detected**: Affects Versions are already correct. The prior run corrected them. The re-run compares current values against the version impact table, finds agreement, and notes "Affects Versions are already correct" without issuing an edit.

**Skipped**: No `jira.edit_issue` call for Affects Versions. No correction comment posted (correction was already documented in the prior run's post-triage summary).

## Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

Step 4 is primarily a read-only JQL search step. The only mutations it can produce are:

1. **Related links to sibling issues** -- any links created in the first run would already be present; the idempotent link-creation check (`issuelinks` array inspection before `create_link`) would detect them and skip.
2. **Cross-CVE overlap links and comments** -- same idempotent link-creation logic applies.
3. **Preemptive task reconciliation** -- no preemptive tasks exist for this CVE (the prior run created standard remediation tasks, not preemptive ones).

**Artifact detected**: No new links or comments would be created.

## Step 5 -- Version Lifecycle Check

Read-only check against the Product pages URL. No mutations produced by this step. The outcome (versions are within support lifecycle) is unchanged between runs.

**Skipped**: No mutation.

## Step 6 -- Already Fixed Check

Read-only cross-reference of resolved sibling issues. No mutations produced by this step.

**Skipped**: No mutation.

## Step 7 -- Concurrent Triage Detection

Read-only JQL search for in-progress triages on the same upstream component (quinn-proto). The current issue itself is In Progress, but the JQL excludes the current issue key (`key != TC-8001`). Any concurrent triages would be presented to the user, but no mutations are produced by this step.

**Skipped**: No mutation.

## Step 8 -- Remediation Task Creation

| Check | Current State | Action |
|-------|---------------|--------|
| Upstream backport task | TC-8100 exists, linked via Depend, labels include ai-generated-jira, Security, CVE-2026-31812 | **Skip** -- task already exists |
| Downstream propagation task | TC-8101 exists, linked via Depend, labels include ai-generated-jira, Security, CVE-2026-31812; blocked by TC-8100 | **Skip** -- task already exists |
| Depend link: TC-8001 -> TC-8100 | Present | **Skip** -- link already exists |
| Depend link: TC-8001 -> TC-8101 | Present | **Skip** -- link already exists |
| Blocks link: TC-8100 -> TC-8101 | Present | **Skip** -- link already exists |
| Status transition to In Progress | Already In Progress | **Skip** -- already in target status |

**Detection method**: The existing `issuelinks` array on TC-8001 (fetched in Step 1) reveals two Depend-linked remediation Tasks (TC-8100, TC-8101) with matching CVE label (CVE-2026-31812) and ai-generated-jira label. Their summaries match the expected remediation task naming pattern for quinn-proto on the rhtpa-2.2 stream. The skill recognizes these as the remediation tasks it would create and skips task creation entirely.

## Post-Triage Summary

| Check | Current State | Action |
|-------|---------------|--------|
| `ai-cve-triaged` label | Present in issue labels | **Skip** -- label already exists |
| Post-triage summary comment | Present (comment #2, posted 2026-07-01T10:01:00Z) | **Skip** -- summary already posted |
| Description digest comment | Present (comment #1, posted 2026-07-01T10:00:00Z) | **Skip** -- digest already posted |

**Detection method**: The `ai-cve-triaged` label is found in the issue's labels array. The post-triage summary comment is identified by its content pattern (begins with "Triage complete for CVE-2026-31812") and its author (sdlc-workflow/triage-security). The description digest comment is identified by its `[sdlc-workflow] Description digest:` prefix.

---

## Complete Artifact Inventory

| Artifact | Type | Expected by Skill | Present on TC-8001? | Re-Run Action |
|----------|------|-------------------|---------------------|---------------|
| `ai-cve-triaged` label | Label | Post-Triage Summary | Yes | Skip |
| Status: In Progress | Transition | Step 8 / Post-Triage | Yes | Skip |
| Assignee: engineer-a | Assignment | Step 0.7 | Yes | Skip (no-op reassignment) |
| Affects Versions: RHTPA 2.2.0, 2.2.1 | Field edit | Step 3 | Yes (already correct) | Skip |
| Depend link -> TC-8100 | Issue link | Step 8 | Yes | Skip |
| Depend link -> TC-8101 | Issue link | Step 8 | Yes | Skip |
| Blocks link TC-8100 -> TC-8101 | Issue link | Step 8 | Yes | Skip |
| TC-8100 (upstream backport task) | Issue creation | Step 8 | Yes | Skip |
| TC-8101 (downstream propagation task) | Issue creation | Step 8 | Yes | Skip |
| Description digest comment | Comment | Step 8 / Post-Triage | Yes | Skip |
| Post-triage summary comment | Comment | Post-Triage | Yes | Skip |
