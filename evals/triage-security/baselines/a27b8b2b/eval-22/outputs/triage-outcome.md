# Triage Outcome -- TC-8021

## Version Impact Summary

Based on the security-matrix.md data for the 2.2.x stream (scoped by issue suffix `[rhtpa-2.2]`), using pinned commit tags from the supportability matrix:

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | >= 0.11.14 |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | >= 0.11.14 |

## Step 7 -- Concurrent Triage Detection

No concurrent triages detected on upstream component `quinn-proto`. The JQL search for in-progress triages with `cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8021` returned zero results.

**Proceeding directly to Case A/B/C branching without warning.**

## Case Determination

- **Affected versions exist** within the scoped 2.2.x stream (2.2.0, 2.2.1, 2.2.2 are affected).
- **Unaffected versions** (2.2.3, 2.2.4) ship quinn-proto >= 0.11.14.
- This is **not** Case C (some versions are affected).

### Cross-stream impact (Case A check)

The issue is scoped to stream 2.2.x. Checking the 2.1.x stream for cross-stream impact:

| Version | Tag | quinn-proto | Affected? |
|---------|-----|-------------|-----------|
| 2.1.0 | `v0.3.8` | 0.11.9 | YES |
| 2.1.1 | `v0.3.12` | 0.11.9 | YES |

Stream 2.1.x is also affected. **Case A applies** -- a cross-stream impact comment would be posted on TC-8021 noting that the 2.1.x stream is also affected. Sibling CVE Jiras for the 2.1.x stream would be checked; if none exist, preemptive remediation tasks would be created for that stream.

### Case B -- Remediation for the 2.2.x stream

Since the issue is scoped to 2.2.x and versions 2.2.0, 2.2.1, and 2.2.2 are affected:

**Proposed remediation tasks** (Cargo ecosystem -- source dependency -- 2 tasks):

1. **Upstream backport task**: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)"
   - Repository: backend
   - Target Branch: release/0.4.z
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Link: Depend to TC-8021

2. **Downstream propagation subtask**: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
   - Repository: rhtpa-release.0.4.z
   - Target Branch: main
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
   - Link: Depend to TC-8021
   - Blocked by: upstream backport task (Blocks link)

## Post-Triage Actions

After remediation task creation (pending engineer confirmation):

1. Add `ai-cve-triaged` label to TC-8021
2. Transition TC-8021 to In Progress
3. Post summary comment with version impact table, Affects Versions correction, remediation task links, and @mention of the issue reporter
