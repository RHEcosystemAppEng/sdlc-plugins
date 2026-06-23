# Step 4 -- Duplicate, Sibling, and Overlap Check

## 4.0 -- JQL Sibling Search

Query:
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: 1 sibling found.

| Issue | Summary | Status | Stream Suffix |
|-------|---------|--------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] |

## 4.1 -- Same-stream duplicate check

- TC-8006 stream scope: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream scope: `[rhtpa-2.2]` (stream 2.2.x)

Classification: **DIFFERENT-stream companion** (not a duplicate).

TC-8001 is a companion tracker for the same CVE in a different stream. PSIRT creates one Vulnerability issue per stream intentionally -- this is expected behavior, not a duplicate.

## 4.2 -- Cross-stream coordination

### Pre-existing link check (idempotent)

Before creating a "Related" link to TC-8001, checking TC-8006's existing `issuelinks` array (fetched in Step 1):

- Link found: type.name = "Related", outwardIssue.key = "TC-8001", Link ID = 1990401

**Related link to TC-8001 already exists -- skipping.**

No call to `jira.create_link` is made. The existing link satisfies the cross-stream coordination requirement. This idempotent check prevents duplicate link creation when the issue already has the required relationship.

### Affects Versions overlap check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

No version overlap detected. Each issue correctly owns only versions from its own stream.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

The sibling landscape shows two companion issues tracking the same CVE across different streams. TC-8001 (2.2.x) is already In Progress, indicating remediation work has begun on that stream. TC-8006 (2.1.x) is the current issue under triage.
