# Idempotency Check: TC-8001 (Re-Run)

This document records every pre-existing triage artifact detected on TC-8001 and the corresponding skip decision for each step of the triage-security skill.

## Summary

TC-8001 has already been fully triaged by a prior run of `sdlc-workflow/triage-security`. All triage artifacts are present. A second run detects each artifact and skips the corresponding mutation, producing **zero new Jira mutations**.

## Artifact-by-Artifact Analysis

### 1. Label: `ai-cve-triaged`

- **Detected**: YES -- the label `ai-cve-triaged` is present in the issue's Labels field.
- **Skill behavior**: The Post-Triage Summary step adds this label to mark the issue as triaged. Since it already exists, adding it again would be a no-op (Jira deduplicates labels), but the skill recognizes the label as a signal that triage has already been completed.
- **Action**: SKIP -- no label mutation needed.

### 2. Status: In Progress

- **Detected**: YES -- the issue status is "In Progress", which is past the "New" and "Assigned" states.
- **Skill behavior**: Step 0.7 transitions from New to Assigned. The status-aware handling (Inputs section) detects that the issue is already "In Progress" and warns: "This issue is already in In Progress. It may be actively worked on." In this eval, we proceed with analysis but recognize no status transition is needed.
- **Action**: SKIP -- no status transition needed. The issue is already beyond Assigned.

### 3. Assignee

- **Detected**: YES -- the issue is assigned to engineer-a@example.com.
- **Skill behavior**: Step 0.7 assigns the issue to the current user. In a re-run, the assignment would update to the current user (which may be the same or different person). This is the one mutation that could theoretically occur, but since we are not calling Jira MCP in this eval, it is noted and skipped.
- **Action**: SKIP (eval mode -- no Jira calls).

### 4. Remediation Tasks: TC-8100 and TC-8101

- **Detected**: YES -- two "Depend" links exist on the issue:
  - TC-8100 (upstream backport) -- Status: In Progress
  - TC-8101 (downstream propagation) -- Status: Open, Blocks TC-8100
- **Skill behavior**: Step 8 (Case B) creates remediation tasks for affected streams. The ecosystem is Cargo (source dependency), so 2 tasks are expected per stream. The issue is scoped to the 2.2.x stream, so exactly 2 tasks are expected. Both already exist with the correct structure (upstream + downstream, with blocking relationship).
- **Action**: SKIP -- remediation tasks already exist and are linked. Creating duplicates would violate the skill's guardrails. The existing tasks match the expected template: upstream backport task + downstream propagation task with the correct CVE label, `ai-generated-jira` label, and `Security` label.

### 5. Description Digest Comment

- **Detected**: YES -- comment #1 contains the digest marker `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`, posted by `sdlc-workflow/triage-security` on 2026-07-01T10:00:00Z.
- **Skill behavior**: The description digest protocol (shared/description-digest-protocol.md) posts a digest comment to enable integrity verification. A second digest comment would be redundant (the description has not changed).
- **Action**: SKIP -- digest comment already exists.

### 6. Post-Triage Summary Comment

- **Detected**: YES -- comment #2 is a full post-triage summary documenting version impact, Affects Versions correction, remediation tasks created, and the transition to In Progress. It includes the Comment Footnote referencing `sdlc-workflow/triage-security v0.11.1`.
- **Skill behavior**: The Post-Triage Summary step posts a summary comment as the final triage action. Posting a duplicate summary would create noise on the issue.
- **Action**: SKIP -- post-triage summary already exists.

### 7. Affects Versions

- **Detected**: The current Affects Versions are RHTPA 2.2.0 and RHTPA 2.2.1.
- **Skill behavior**: Step 3 corrects Affects Versions based on lock file evidence. The version impact table shows RHTPA 2.2.0 (quinn-proto 0.11.9) and RHTPA 2.2.1 (quinn-proto 0.11.12) are affected. The current Affects Versions already match the lock file evidence.
- **Action**: SKIP -- Affects Versions are already correct. No correction needed.

### 8. Duplicate/Sibling Check (Step 4)

- **Skill behavior**: Step 4 searches for sibling Vulnerability issues with the same CVE. In this eval, no sibling data is provided, so no duplicates are detected.
- **Action**: SKIP -- no duplicate detection artifacts to reconcile.

## Pre-Existing Artifacts Summary Table

| Artifact | Expected by Skill Step | Present? | Action |
|----------|----------------------|----------|--------|
| `ai-cve-triaged` label | Post-Triage Summary | YES | SKIP |
| Status >= Assigned | Step 0.7 | YES (In Progress) | SKIP |
| Remediation task (upstream) | Step 8, Case B | YES (TC-8100) | SKIP |
| Remediation task (downstream) | Step 8, Case B | YES (TC-8101) | SKIP |
| Depend links to CVE issue | Step 8, Case B | YES (both linked) | SKIP |
| Blocks link (TC-8101 blocks TC-8100) | Step 8, Case B | YES | SKIP |
| Description digest comment | Remediation Task Creation | YES | SKIP |
| Post-triage summary comment | Post-Triage Summary | YES | SKIP |
| Affects Versions corrected | Step 3 | YES (matches evidence) | SKIP |
