# Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

## 4.0 -- JQL Sibling Search

JQL query (simulated):

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

Results: **1 sibling found**

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## 4.1 -- Same-Stream Duplicate Check

- TC-8006 stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8001 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

Classification: **Different-stream sibling** (companion tracker, not a duplicate).

TC-8001 is scoped to stream 2.2.x while TC-8006 is scoped to stream 2.1.x. These are companion trackers created by PSIRT intentionally -- one per stream. No duplicate closure is warranted.

## 4.2 -- Cross-Stream Coordination

TC-8001 is a different-stream sibling. Per the Step 4.2 protocol, before creating a "Related" link, check the current issue's existing `issuelinks` array.

### Existing Link Check

TC-8006's issue links (from Step 1 data extraction):

| Link Type | Direction | Linked Issue | Link ID |
|-----------|-----------|--------------|---------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | 1990401 |

Checking for existing link satisfying all of:
- `type.name` is `"Related"` -- **YES** (type is Related)
- `outwardIssue.key` matches the sibling key TC-8001 -- **YES** (outward link to TC-8001)

**Result: A matching Related link to TC-8001 already exists.**

> Related link to TC-8001 already exists -- skipping

Link creation is **skipped**. The pre-existing link (ID: 1990401) already satisfies the cross-stream coordination requirement. No Jira mutation is needed.

### Affects Versions Overlap Check

| Issue | Stream | Affects Versions |
|-------|--------|------------------|
| TC-8006 | 2.1.x | RHTPA 2.1.0 |
| TC-8001 | 2.2.x | RHTPA 2.2.0, RHTPA 2.2.1 |

**No version overlap detected.** Each issue carries only versions from its own stream. TC-8006 owns 2.1.x versions and TC-8001 owns 2.2.x versions. No conflict to flag.

### Sibling Landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## 4.3 -- Cross-CVE Overlap Detection

The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are **not configured** in the project's Security Configuration. Per the skill documentation: "If any of these fields are not configured, skip this step entirely."

**Step 4.3 skipped.**

## 4.4 -- Preemptive Task Reconciliation

JQL query (simulated):

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No matching preemptive tasks found for CVE-2026-31812 scoped to stream rhtpa-2.1.

**Step 4.4: No reconciliation needed.** Proceed to Step 5.
