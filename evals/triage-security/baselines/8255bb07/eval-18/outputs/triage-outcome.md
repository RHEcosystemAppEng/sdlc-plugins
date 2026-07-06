# Triage Outcome: TC-8001 Re-Run -- No New Mutations

## Context

TC-8001 (CVE-2026-31812, quinn-proto panic on large stream counts) was fully
triaged in a prior run of `triage-security`. This document explains why the
second invocation produces zero Jira mutations.

## Prior Triage State (first run)

The first triage run completed all eight steps and produced the following
artifacts on TC-8001:

1. **Label** `ai-cve-triaged` added to mark the issue as triaged
2. **Status** transitioned from New through Assigned to In Progress
3. **Affects Versions** corrected to RHTPA 2.2.0 and RHTPA 2.2.1 (the two
   versions shipping quinn-proto < 0.11.14)
4. **Remediation task TC-8100** created (upstream backport: backport quinn-proto
   fix to >= 0.11.14 on release/0.4.z), linked via Depend
5. **Remediation task TC-8101** created (downstream propagation: propagate
   quinn-proto bump to rhtpa-server release branch), linked via Depend, with
   Blocks relationship to TC-8100
6. **Description digest comment** posted with hash
   `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`
7. **Post-triage summary comment** posted documenting the full triage outcome

## Why the Second Run Produces No Mutations

The `triage-security` skill is designed to be idempotent. Each step checks for
pre-existing artifacts before performing mutations. On this re-run, every
checkpoint finds its artifact already in place:

### Step 0.7 -- Assign and Transition

The issue is already in **In Progress** status, which is beyond Assigned. The
status-aware handling logic detects a non-New status and presents a warning.
Even if the engineer chooses to proceed, the transition to Assigned is skipped
because the issue has already progressed past that state. Assignment to the
current user may be re-applied (a no-op if the assignee is unchanged).

### Step 1 -- Data Extraction

Data extraction is read-only and produces the same parsed CVE data as the first
run. The description has not changed, so the same fields are extracted. This
step produces no mutations regardless of run count.

### Step 2 -- Version Impact Analysis

Lock file inspection via `git show` is read-only. The version impact table is
identical to the first run because the security matrix and lock file data have
not changed. No mutations at this step.

### Step 3 -- Affects Versions Correction

The current Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1) already match the
version impact analysis. No correction is needed -- the Jira field update is
skipped.

### Step 4 -- Duplicate/Sibling/Overlap Check

The JQL search for sibling issues would return the same results as the first
run. Any links created during the first run already exist. No new links or
comments are produced.

### Steps 5-6 -- Lifecycle and Already-Fixed Checks

These are read-only analysis steps that inform the remediation decision. They
produce no direct mutations.

### Step 7 -- Concurrent Triage Detection

Read-only check for other active triages on the same upstream component.
Produces no mutations.

### Step 8 -- Remediation (Case A)

This is where the key idempotency checks prevent duplicate work:

1. **Remediation tasks**: The skill detects existing Depend links to TC-8100
   and TC-8101. Both task summaries match the expected remediation template
   output for a Cargo ecosystem vulnerability on stream 2.2.x. Since matching
   remediation tasks already exist and are linked, no new tasks are created.

2. **Cross-stream impact (Case B)**: Stream 2.1.x is also affected (quinn-proto
   0.11.9 < 0.11.14 in versions 2.1.0 and 2.1.1), but any cross-stream comment
   from the first run already exists on the issue. No duplicate comment is posted.

### Post-Triage Summary

1. **`ai-cve-triaged` label**: Already present on the issue. Adding it again is
   a no-op in Jira, but the skill recognizes its presence and skips the add.

2. **Summary comment**: A post-triage summary comment already exists (comment #2,
   posted 2026-07-01T10:01:00Z). Posting a duplicate summary would create
   confusing redundancy in the audit trail. The skill detects the existing
   summary and skips.

3. **Description digest comment**: Already present (comment #1). The digest
   protocol checks for an existing digest before posting. Skipped.

## Conclusion

The second run of `triage-security` on TC-8001 is fully idempotent. All seven
categories of triage artifacts (label, status, Affects Versions, two Depend
links, digest comment, summary comment) are detected as already present. The
re-run performs read-only data extraction and version impact analysis but
produces zero Jira mutations. This is the correct and expected behavior --
re-running triage on a fully triaged issue should be safe and side-effect-free.
