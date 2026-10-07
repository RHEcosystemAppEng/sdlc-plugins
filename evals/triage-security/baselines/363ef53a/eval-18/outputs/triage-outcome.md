# Triage Outcome -- Why the Second Run Produces No New Mutations

## Context

TC-8001 (CVE-2026-31812, quinn-proto, `[rhtpa-2.2]`) was previously triaged
by `/triage-security`. A complete set of triage artifacts exists on the issue:
the `ai-cve-triaged` label, In Progress status, two remediation tasks
(TC-8100 upstream backport, TC-8101 downstream propagation) linked via
Depend, corrected Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1), a description
digest comment, and a post-triage summary comment.

This document explains why a second invocation of `/triage-security TC-8001`
produces no new Jira mutations.

## Step-by-Step Analysis

### Step 0 -- Validate Configuration

Configuration validation is a read-only operation. It extracts project key
(TC), Cloud ID, Jira version prefix (RHTPA), Vulnerability issue type ID
(10024), Product pages URL, component label pattern (pscomponent:), VEX
Justification field (customfield_12345), and version streams. No mutations.
Outcome: **pass (read-only)**.

### Step 0.3 -- Matrix Staleness Check

The security matrix has `Last-Updated: 2026-06-28T10:00:00Z`. At the time
of this eval (2026-10-07), the matrix is over 14 days old, which would
trigger a staleness warning. However, this is a read-only check that
prompts the user for a decision. No mutations.
Outcome: **pass (read-only)**.

### Step 0.5 -- Jira Access Initialization

Connection setup is a read-only operation. No mutations.
Outcome: **pass (read-only)**.

### Step 0.7 -- Assign and Transition to Assigned

- **Assignment**: The skill always assigns the issue to the current user,
  even on re-runs. If the current user is the same as the existing
  assignee (engineer-a@example.com), this is effectively a no-op. If
  different, this is the one permissible mutation -- updating the assignee
  to reflect who is currently reviewing the issue.
- **Transition**: The issue is in `In Progress`, which is past `Assigned`.
  The skill skips the transition silently per the status-aware handling
  rule: "If the issue is already in Assigned or any later status, skip
  the transition silently."

Outcome: **no new mutation** (assignment is idempotent if same user;
transition skipped because status is already past Assigned).

### Step 1 -- Data Extraction

Read-only. Fetches issue data, remote links, parses CVE metadata. No
mutations. See `data-extraction.md` for the parsed data table.
Outcome: **pass (read-only)**.

### Step 1.5 -- External CVE Data Enrichment

Read-only. Queries MITRE CVE API and OSV.dev for structured version data.
No mutations. (In this eval, external APIs are not called per instructions.)
Outcome: **pass (read-only)**.

### Step 1.7 -- Embargo Check

CVE-2026-31812 has CVSS 7.5 (High), which meets the threshold. The embargo
check is an advisory gate -- it presents a warning and waits for user
confirmation. No mutations.
Outcome: **pass (read-only gate)**.

### Step 2 -- Version Impact Analysis

Read-only. Loads security matrix, extracts dependency versions from mock
lock file data, builds version impact table. No mutations.

Version impact table (from mock data, scoped to 2.2.x):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

Outcome: **pass (read-only)**.

### Step 3 -- Affects Versions Correction

The current Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1) match the version
impact analysis for the 2.2.x stream scope. No correction needed.
Outcome: **no mutation (already correct)**.

### Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

- Step 4.1/4.2: Sibling search would run JQL for other issues with the
  CVE-2026-31812 label. This is read-only. Any link creation would check
  for existing links first (idempotent).
- Step 4.3: Cross-CVE overlap detection queries for issues with the same
  Upstream Affected Component (quinn-proto). Read-only search. Any links
  or comments would check for existing artifacts first.
- Step 4.4: Preemptive task reconciliation searches for `security-preemptive`
  tasks. Read-only search.
Outcome: **no new mutations** (read-only searches; link creation is
idempotent -- existing links detected and skipped).

### Step 5 -- Version Lifecycle Check

Read-only. Fetches product lifecycle page to verify support status. No
mutations.
Outcome: **pass (read-only)**.

### Step 6 -- Already Fixed Check

Read-only. Cross-references resolved sibling issues. No mutations.
Outcome: **pass (read-only)**.

### Step 7 -- Concurrent Triage Detection

Read-only JQL search. No mutations. Presents findings for user decision.
Outcome: **pass (read-only)**.

### Step 7.5 -- Release Jira Orchestration

Searches for existing release Epic and release Task. If they already exist,
reuses them. The find-or-create pattern means no new creation is needed if
the release structure was established in the first triage run.
Outcome: **no new mutations** (reuses existing release Jira structure if
present).

### Step 8 -- Remediation (Case B)

This is where the idempotency check is most critical. The skill would
normally create remediation tasks for each affected stream. However:

1. **Two remediation tasks already exist**: TC-8100 (upstream backport) and
   TC-8101 (downstream propagation) are linked to TC-8001 via Depend.
2. **Task coverage matches expectations**: The Cargo ecosystem produces
   exactly 2 tasks per stream (upstream + downstream). Both exist.
3. **Stream coverage is complete**: The issue is scoped to 2.2.x, and both
   tasks target the 2.2.x stream (release/0.4.z upstream branch, rhtpa-2.2
   stream identifier in summaries).
4. **Cross-CVE dedup (Step 7.5.3)** would also detect TC-8100 as covering
   the same Upstream Affected Component (quinn-proto) for the same release
   version, triggering the dedup path that skips task creation.

Outcome: **no new mutations** (existing remediation tasks cover the full
scope; dedup detection prevents duplicate creation).

### Post-Triage Summary

All post-triage artifacts are already present:

1. **`ai-cve-triaged` label**: Already in the labels array. Skip.
2. **Summary comment**: Already posted (comment 2, 2026-07-01T10:01:00Z).
   Posting a second summary would create a misleading audit trail. Skip.

Outcome: **no new mutations**.

## Conclusion

The second run of `/triage-security TC-8001` produces **no new Jira
mutations** because every mutable artifact that the triage process would
create or modify already exists in its correct final state:

| Artifact | State After First Run | Second Run Action |
|----------|----------------------|-------------------|
| `ai-cve-triaged` label | Present | Skip (already present) |
| Status | In Progress | Skip transition (already past Assigned) |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 | Skip (already correct) |
| Remediation task (upstream) | TC-8100 (In Progress) | Skip (exists, linked via Depend) |
| Remediation task (downstream) | TC-8101 (Open) | Skip (exists, linked via Depend) |
| Description digest comment | Present | Skip (already posted) |
| Post-triage summary comment | Present | Skip (already posted) |
| Assignee | engineer-a@example.com | Idempotent update (same or re-assign) |

The triage skill is inherently idempotent for re-runs: it detects existing
artifacts at each step and skips mutations that would produce duplicates.
The only permissible mutation on re-run is the assignee update in Step 0.7,
which always runs but is functionally a no-op when the same user re-triages.
All read-only steps (data extraction, version impact analysis, lifecycle
checks) execute normally to produce an up-to-date analysis, but no
write operations are emitted to Jira.
