# Triage Outcome — TC-8003

## Decision: Close as Duplicate

TC-8003 should be **closed as Duplicate** of **TC-7999**.

## Rationale

1. **Same CVE**: Both TC-8003 and TC-7999 track CVE-2026-31812 (quinn-proto panic on large stream counts).

2. **Same stream scope**: Both issues carry the stream suffix `[rhtpa-2.2]`, scoping them to the 2.2.x version stream. This makes TC-7999 a same-stream sibling, not a cross-stream companion.

3. **TC-7999 is already In Progress**: Active triage and/or remediation work is already underway on TC-7999. Continuing triage on TC-8003 would produce duplicate effort and potentially duplicate remediation tasks.

4. **TC-7999 has broader coverage**: TC-7999 already has Affects Versions `[RHTPA 2.2.0, RHTPA 2.2.1]`, which fully subsumes TC-8003's Affects Versions `[RHTPA 2.2.0]`. There are no versions on TC-8003 that are not already covered by TC-7999.

5. **Version impact confirmation**: The lock file analysis confirms that versions 2.2.0 (quinn-proto 0.11.9) and 2.2.1 (quinn-proto 0.11.12) are affected (both below the fix threshold of 0.11.14). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 and are not affected. This is consistent with TC-7999's existing Affects Versions.

## Actions Required (pending engineer confirmation)

The following Jira mutations would be performed after engineer confirmation:

### 1. Assign TC-8003

Assign TC-8003 to the current user and transition to Assigned status (Step 0.8).

### 2. Add Duplicate Comment

Post a comment to TC-8003 documenting the duplicate finding:

> Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream (2.2.x). TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1], which subsumes this issue's Affects Versions [RHTPA 2.2.0]. Version impact analysis confirms overlap.
>
> [Comment Footnote]

### 3. Close as Duplicate

Transition TC-8003 to **Closed** with resolution **"Duplicate"**.

### 4. Add ai-cve-triaged Label

Add the `ai-cve-triaged` label to TC-8003 to mark it as triaged.

## Steps Skipped Due to Duplicate Closure

The following steps are not performed because TC-8003 is being closed as a duplicate:

- **Step 3 (Affects Versions Correction)**: Not needed — the issue is being closed, not corrected. TC-7999 already carries the correct Affects Versions.
- **Step 5 (Version Lifecycle Check)**: Not needed — lifecycle assessment is handled by TC-7999's triage.
- **Step 6 (Already Fixed Check)**: Not needed — TC-7999 is In Progress (not resolved), so there is no already-fixed scenario for the duplicate check to surface.
- **Step 7 (Concurrent Triage Detection)**: Skipped — Upstream Affected Component custom field is not configured.
- **Step 7.5 (Release Jira Orchestration)**: Not needed — no remediation tasks are created for a duplicate issue.
- **Step 8 (Remediation)**: Not needed — all remediation for CVE-2026-31812 in stream 2.2.x is handled through TC-7999. No new remediation tasks should be created.

## Cross-Stream Note

The version impact analysis also shows that the 2.1.x stream (versions 2.1.0 and 2.1.1, both shipping quinn-proto 0.11.9) is affected by this CVE. However, since TC-8003 is being closed as a duplicate, cross-stream impact reporting (Case A) is not performed here. TC-7999 (the surviving issue) is the appropriate place for cross-stream analysis when its triage reaches Step 8.
