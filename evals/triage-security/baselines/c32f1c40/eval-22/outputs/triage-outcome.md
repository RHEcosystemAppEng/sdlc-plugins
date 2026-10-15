# Triage Outcome for TC-8021

## Summary

CVE-2026-31812 affects the quinn-proto crate (versions < 0.11.14). The issue is scoped to the 2.2.x stream via the `[rhtpa-2.2]` suffix.

## Step 7 -- Concurrent Triage Detection Result

Step 7 executed a concurrent triage check for upstream component `quinn-proto` (customfield_10632). The JQL search:

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'quinn-proto' AND status IN ('In Progress', 'Code Review') AND key != TC-8021
```

returned **zero results**. No concurrent triages were detected on the same upstream component. The analysis proceeds directly to Case A/B/C branching without presenting a concurrent triage warning. No wait/skip/proceed options are presented since no conflict exists.

## Version Impact Summary

Based on the mock lock file data from security-matrix.md:

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Case A/B/C Branching Decision

Since Step 7 detected no concurrent triages, the triage proceeds to the standard branching:

- **Versions affected in-scope (2.2.x stream)**: 2.2.0, 2.2.1, 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.
- **Cross-stream impact (2.1.x stream)**: 2.1.0 and 2.1.1 are also affected (quinn-proto 0.11.9 < 0.11.14). Since this is a scoped issue (`[rhtpa-2.2]`), Case A applies -- a cross-stream impact notice would be posted, and preemptive remediation tasks may be created for 2.1.x if no sibling CVE Jira exists for that stream.
- **Case B applies for the in-scope stream**: remediation tasks would be created for the 2.2.x stream. Since Cargo is a source dependency ecosystem, two tasks are created: an upstream backport task (bump quinn-proto to >= 0.11.14 in the backend repository) and a downstream propagation subtask (update the source reference in the Konflux release repo).

### Proposed remediation tasks (2.2.x stream)

1. **Upstream backport task**: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (rhtpa-2.2)"
   - Repository: backend
   - Target Branch: release/0.4.z
   - Labels: [ai-generated-jira, Security, CVE-2026-31812]
   - Link: Depend to TC-8021

2. **Downstream propagation subtask**: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)"
   - Repository: rhtpa-release.0.4.z
   - Target Branch: main
   - Labels: [ai-generated-jira, Security, CVE-2026-31812]
   - Link: Depend to TC-8021, Blocks relationship (upstream blocks downstream)

### Affects Versions correction (proposed)

Current: [RHTPA 2.0.0] (PSIRT-assigned, incorrect -- no 2.0 stream exists)
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2] (scoped to 2.2.x stream, based on lock file evidence)

### Post-triage actions (proposed)

- Add label `ai-cve-triaged` to TC-8021
- Transition TC-8021 to In Progress
- Post summary comment with version impact table and remediation task links
