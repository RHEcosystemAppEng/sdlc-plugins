# Step 4 -- Duplicate, Sibling, and Overlap Check: TC-8006

## Step 4 JQL Search

Simulated JQL query:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

One sibling issue found:

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

## Step 4.1 -- Same-stream duplicate check

TC-8001 has stream suffix `[rhtpa-2.2]`, which is **different** from TC-8006's
stream suffix `[rhtpa-2.1]`. Therefore TC-8001 is NOT a same-stream duplicate.

Result: No same-stream duplicates found. Proceeding to Step 4.2.

## Step 4.2 -- Cross-stream coordination

TC-8001 is a **different-stream sibling** (companion tracker). PSIRT created
one issue per stream intentionally.

### Link idempotency check

Per Step 4.2, before creating a "Related" link, the skill checks the current
issue's `issuelinks` array (already fetched in Step 1) for an existing link
where:

- `type.name` is `"Related"`
- `inwardIssue.key` or `outwardIssue.key` matches `TC-8001`

**Result**: A matching link already exists on TC-8006:

- Link ID: 1990401
- Type: Related
- Direction: outward (TC-8006 --> TC-8001)

**Action**: Skip link creation. Log:

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call is made. The pre-existing link satisfies the
cross-stream coordination requirement.

### Affects Versions overlap check

Checking for version overlap between TC-8006 and TC-8001:

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

**No overlap detected.** Each issue carries versions only from its own stream.

### Sibling landscape

CVE-2026-31812 companion issues:

| Issue | Stream | Status | Affects Versions |
|-------|--------|--------|------------------|
| TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Step 4.3 -- Cross-CVE overlap detection

The Upstream Affected Component custom field is not configured in the
project's Security Configuration. Per the skill instructions, Step 4.3
is skipped entirely when this field is not configured.

## Step 4.4 -- Preemptive task reconciliation

Simulated JQL query for preemptive tasks:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

Assumed result: No matching preemptive tasks found for CVE-2026-31812
in the 2.1.x stream.

Proceeding to Step 5.
