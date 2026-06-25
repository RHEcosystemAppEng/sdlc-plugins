# Triage Outcome: TC-8003

## Decision: Close as Duplicate of TC-7999

### Rationale

TC-8003 is a duplicate of TC-7999. Both issues track the same vulnerability (CVE-2026-31812 in quinn-proto) for the same product version stream (2.2.x, identified by the `[rhtpa-2.2]` stream suffix in both issue summaries).

TC-7999 is already **In Progress**, meaning active remediation work has begun. Its Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1) are a superset of TC-8003's Affects Versions (RHTPA 2.2.0). Maintaining TC-8003 as a separate issue would create redundant tracking and risk conflicting remediation efforts.

### Evidence Summary

| Criterion | TC-8003 (current) | TC-7999 (sibling) |
|-----------|--------------------|--------------------|
| CVE | CVE-2026-31812 | CVE-2026-31812 |
| Library | quinn-proto | quinn-proto |
| Stream suffix | [rhtpa-2.2] | [rhtpa-2.2] |
| Mapped stream | 2.2.x | 2.2.x |
| Status | New | In Progress |
| Affects Versions | RHTPA 2.2.0 | RHTPA 2.2.0, RHTPA 2.2.1 |

### JQL Query Used

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

This query searches for all Vulnerability issues in project TC that carry the CVE-2026-31812 label, excluding the current issue. The single result (TC-7999) was then classified by comparing its stream suffix against TC-8003's stream suffix.

### Proposed Jira Mutations (require engineer confirmation)

1. **Comment on TC-8003:**
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1] and covers this issue's scope entirely. Closing as duplicate. Version impact analysis confirms overlap: both issues target the 2.2.x stream where quinn-proto ships at versions below the 0.11.14 fix threshold.

2. **Transition TC-8003** to Closed with resolution "Duplicate".

3. **Assign TC-8003** to current user.

### What is NOT done (short-circuited by duplicate detection)

The following steps are **skipped** because duplicate detection in Step 4.1 terminates the triage workflow early:

- **Step 5 (Version Lifecycle Check)** -- not needed; TC-7999 already covers lifecycle assessment for this CVE/stream.
- **Step 6 (Already Fixed Check)** -- not needed; TC-7999 is In Progress, not resolved.
- **Step 7 (Remediation Task Creation)** -- not needed; any remediation tasks belong under TC-7999, not this duplicate. Creating tasks under TC-8003 would result in duplicate remediation work.
- **Post-triage label (`ai-cve-triaged`)** -- would still be applied to TC-8003 after closing as duplicate, to prevent re-triage.
