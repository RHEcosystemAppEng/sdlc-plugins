# Triage Outcome for TC-8003

## Decision: Close as Duplicate

TC-8003 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) should be **closed as a Duplicate** of TC-7999.

## Rationale

### Duplicate Detection (Step 4)

A JQL search for sibling issues with the same CVE label (CVE-2026-31812) returned TC-7999, which is a **same-stream duplicate**:

| Attribute | TC-8003 (current) | TC-7999 (sibling) |
|-----------|-------------------|-------------------|
| CVE | CVE-2026-31812 | CVE-2026-31812 |
| Stream suffix | [rhtpa-2.2] | [rhtpa-2.2] |
| Stream | 2.2.x | 2.2.x |
| Status | New | In Progress |
| Affects Versions | RHTPA 2.2.0 | RHTPA 2.2.0, RHTPA 2.2.1 |
| Component | pscomponent:org/rhtpa-server | pscomponent:org/rhtpa-server |

Both issues track the exact same vulnerability for the exact same product stream. TC-7999 is already In Progress and has more complete Affects Versions coverage.

### Version Impact Summary

The version impact analysis (performed before the duplicate check) confirmed:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO (fixed) |
| 2.2.4 | 0.11.14 | NO (fixed) |

The vulnerability affects versions 2.2.0-2.2.2 but is already resolved in versions 2.2.3+ which ship quinn-proto 0.11.14 (the fixed version). This analysis is consistent with TC-7999's Affects Versions of RHTPA 2.2.0 and RHTPA 2.2.1.

### Cross-Stream Impact Note

The version impact analysis also revealed that stream 2.1.x is affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). However, since TC-8003 is scoped to stream 2.2.x and is being closed as a duplicate, cross-stream impact for the 2.1.x stream is informational only. PSIRT is responsible for creating separate stream-scoped Vulnerability issues for 2.1.x if needed.

## Steps Skipped Due to Duplicate Closure

The following steps are skipped because the issue is being closed as a duplicate. The active tracker (TC-7999) is responsible for these:

- **Step 5 -- Version Lifecycle Check**: TC-7999 should verify lifecycle status of affected versions.
- **Step 6 -- Already Fixed Check**: TC-7999 should check if versions 2.2.3+ already resolve the CVE (they do -- quinn-proto 0.11.14 is shipped).
- **Step 7 -- Remediation**: TC-7999 should determine if remediation tasks are needed for versions 2.2.0-2.2.2 (which are affected) or if those versions are already superseded by 2.2.3+.

## Proposed Jira Mutations (All Require Engineer Confirmation)

### 1. Add comment to TC-8003

> Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap: quinn-proto versions 0.11.9 (2.2.0) and 0.11.12 (2.2.1) are both vulnerable (< 0.11.14). The fix is already shipped in versions 2.2.3+ (quinn-proto 0.11.14).
>
> _This triage was performed by the triage-security skill._

### 2. Transition TC-8003 to Closed

- Resolution: **Duplicate**

### 3. Assign TC-8003

- Assign to current user

### 4. Add label to TC-8003

- Add label: `ai-cve-triaged`

## Summary

TC-8003 is a duplicate of TC-7999. Both issues track CVE-2026-31812 (quinn-proto denial of service via excessive stream counts) for the same product stream (2.2.x / [rhtpa-2.2]). TC-7999 is already In Progress with correct Affects Versions coverage. The recommended action is to close TC-8003 as Duplicate, add the `ai-cve-triaged` label, and let TC-7999 continue as the active tracker for this vulnerability.
