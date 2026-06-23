# Duplicate Check — TC-8003

## Step 4 — Duplicate, Sibling, and Overlap Check

### JQL Search

Simulated JQL query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

**Results**: 1 sibling issue found.

### Sibling Analysis

| Issue | Summary | Stream Suffix | Status | Affects Versions |
|-------|---------|---------------|--------|------------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8003 (current) | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | New | RHTPA 2.2.0 |

### Classification

**TC-7999 is a same-stream sibling.** Both TC-7999 and TC-8003 share:
- The same CVE: CVE-2026-31812
- The same stream suffix: [rhtpa-2.2] (both scoped to the 2.2.x stream)
- The same component label: pscomponent:org/rhtpa-server

This makes TC-8003 a **duplicate** of TC-7999 per Step 4.1 of the triage-security skill.

### Duplicate Determination

TC-7999 is the earlier issue and is already **In Progress**, meaning active remediation work has begun. TC-8003 is in **New** status and was filed later. Per the triage protocol:

- TC-7999 is the primary tracker for CVE-2026-31812 in the 2.2.x stream
- TC-7999 already has broader Affects Versions coverage (RHTPA 2.2.0, RHTPA 2.2.1) compared to TC-8003 (RHTPA 2.2.0 only)
- TC-7999 is actively being worked on (In Progress status)

**Recommendation**: Close TC-8003 as **Duplicate** of TC-7999.

### Proposed Actions

1. Add comment to TC-8003: "Duplicate of TC-7999 — same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap."
2. Transition TC-8003 to **Closed** with resolution **Duplicate**.
3. Assign TC-8003 to current user.

### Affects Versions Note

TC-7999 already carries RHTPA 2.2.0 and RHTPA 2.2.1 in its Affects Versions, which covers the affected versions in the 2.2.x stream. TC-8003 only had RHTPA 2.2.0, which is a subset. No Affects Versions correction is needed on TC-7999 since it already covers the affected versions (2.2.0 and 2.2.1; 2.2.2 is a retag of 2.2.1 and may or may not have a Jira version entry).

### Step 4.3 — Cross-CVE Overlap Detection

The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are **not configured** in the Security Configuration (claude-md-security-config.md does not include these optional fields). Per the skill instructions, Step 4.3 is **skipped entirely** when these fields are not configured.
