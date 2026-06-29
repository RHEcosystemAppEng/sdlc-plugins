# Triage Outcome for TC-8003

## Decision: Close as Duplicate of TC-7999

TC-8003 is a duplicate of TC-7999. Both issues track CVE-2026-31812 (quinn-proto panic on large stream counts) for the same product version stream (2.2.x), as indicated by their identical stream suffix `[rhtpa-2.2]`. TC-7999 is already In Progress and has more complete Affects Versions (RHTPA 2.2.0 and RHTPA 2.2.1 vs. only RHTPA 2.2.0 on TC-8003).

## Rationale

1. **Same CVE**: Both TC-8003 and TC-7999 carry the label CVE-2026-31812.
2. **Same stream**: Both have the summary suffix `[rhtpa-2.2]`, scoping them to the 2.2.x version stream.
3. **Same component**: Both carry the label `pscomponent:org/rhtpa-server`.
4. **TC-7999 is already In Progress**: Active remediation work is underway on TC-7999, making TC-8003 redundant.
5. **TC-7999 has broader coverage**: TC-7999 already lists Affects Versions RHTPA 2.2.0 and RHTPA 2.2.1, while TC-8003 only lists RHTPA 2.2.0. The version impact analysis confirms both versions are affected.

## Proposed Jira Mutations (require engineer confirmation)

The following actions are proposed but NOT executed. Each requires explicit engineer approval:

### 1. Add comment to TC-8003

```
Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2].
Version impact analysis confirms overlap:
- RHTPA 2.2.0: ships quinn-proto 0.11.9 (affected, < 0.11.14)
- RHTPA 2.2.1: ships quinn-proto 0.11.12 (affected, < 0.11.14)

TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1].
No additional fix required from this issue.

---
_Automated triage by triage-security skill_
```

### 2. Transition TC-8003 to Closed

- Resolution: **Duplicate**
- Assign to current user

### 3. Add ai-cve-triaged label to TC-8003

Add the `ai-cve-triaged` label to mark the issue as triaged.

## Steps Not Executed (due to duplicate closure)

The following steps are skipped because the issue is being closed as a duplicate. These concerns are deferred to TC-7999:

- **Step 3 (Affects Versions Correction)**: Not needed -- TC-8003 is being closed. TC-7999 already has the correct stream-scoped Affects Versions.
- **Step 5 (Version Lifecycle Check)**: Deferred to TC-7999's triage.
- **Step 6 (Already Fixed Check)**: Deferred to TC-7999's triage.
- **Step 7 (Remediation)**: Deferred to TC-7999's triage. Note that the version impact analysis shows:
  - Versions 2.2.0, 2.2.1, and 2.2.2 are affected within the 2.2.x stream
  - Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, the fixed version)
  - Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9) -- this is a cross-stream concern for TC-7999 to address

## Cross-Stream Impact Note

The version impact analysis reveals that stream 2.1.x is also affected:

| Version | Stream | quinn-proto | Affected? |
|---------|--------|-------------|-----------|
| 2.1.0 | 2.1.x | 0.11.9 | YES |
| 2.1.1 | 2.1.x | 0.11.9 | YES |

No sibling Vulnerability issue was found for the 2.1.x stream (no issue with suffix `[rhtpa-2.1]` appeared in the JQL search results). This cross-stream impact should be addressed during TC-7999's triage under Step 7 Case B (proactive remediation for streams without their own CVE Jira).

## Version Impact Summary

For reference, the complete version impact table:

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |

Fix threshold: quinn-proto 0.11.14 (versions below this are vulnerable to CVE-2026-31812).
