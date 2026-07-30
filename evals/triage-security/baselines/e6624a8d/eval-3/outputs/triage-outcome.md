# Triage Outcome — TC-8003

## Decision: Close as Duplicate

TC-8003 is closed as a **duplicate** of TC-7999. No remediation tasks are created.

## Rationale

The duplicate check in Step 4 identified TC-7999 as an existing sibling issue for CVE-2026-31812
in the same version stream [rhtpa-2.2]. TC-7999 is already `In Progress`, meaning triage has
been completed and remediation work is actively underway. Creating additional remediation tasks
from TC-8003 would result in duplicated work.

### Key Evidence

| Criterion | TC-8003 (this issue) | TC-7999 (existing) |
|-----------|---------------------|---------------------|
| CVE | CVE-2026-31812 | CVE-2026-31812 |
| Stream | [rhtpa-2.2] (2.2.x) | [rhtpa-2.2] (2.2.x) |
| Component | pscomponent:org/rhtpa-server | pscomponent:org/rhtpa-server |
| Status | New | In Progress |
| Affects Versions | RHTPA 2.2.0 | RHTPA 2.2.0, RHTPA 2.2.1 |

TC-7999 is the authoritative issue: it was created first, is already in progress, and has
broader Affects Versions coverage (RHTPA 2.2.0 and 2.2.1 vs. only 2.2.0 on TC-8003).

## Jira Actions (would be performed with engineer confirmation)

1. **Link**: Create "Duplicate" link — TC-8003 duplicates TC-7999
2. **Label**: Add `ai-cve-triaged` to TC-8003
3. **Transition**: Close TC-8003 with resolution "Duplicate"
4. **Comment on TC-8003**:

   > This issue is a duplicate of TC-7999, which covers the same CVE (CVE-2026-31812)
   > in the same stream [rhtpa-2.2] and is already In Progress.
   >
   > TC-7999 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1
   > TC-8003 Affects Versions: RHTPA 2.2.0 (subset of TC-7999)
   >
   > Closing this issue as Duplicate. Remediation is tracked under TC-7999.

## Steps Not Executed

Because TC-8003 is closed as a duplicate, the following steps are not performed:

- **Step 3 (Affects Versions Correction)**: Not applied to TC-8003 since it is being closed.
  Note: TC-7999 may need RHTPA 2.2.2 added to its Affects Versions (it ships quinn-proto 0.11.12,
  which is vulnerable), but that correction belongs to TC-7999's triage, not this one.
- **Step 5 (Version Lifecycle Check)**: Not needed for a duplicate closure.
- **Step 6 (Already Fixed Check)**: Not applicable — TC-7999 is In Progress, not Resolved.
- **Step 7 (Concurrent Triage Detection)**: Skipped because Upstream Affected Component custom
  field is not configured.
- **Step 8 (Remediation)**: No tasks created — remediation is tracked under TC-7999.
- **Case A (Cross-stream impact)**: Not evaluated for TC-8003. The 2.1.x stream is also
  affected (RHTPA 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9), but cross-stream proactive
  remediation is the responsibility of TC-7999 (the surviving issue), not this duplicate.

## Version Impact Summary (for reference)

Although no action is taken from TC-8003, the version impact analysis was completed:

### 2.2.x stream (in scope)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 | YES (retag of 2.2.1) |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) |

### 2.1.x stream (cross-stream)

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.1.0 | 0.11.9 | YES |
| RHTPA 2.1.1 | 0.11.9 | YES |
