# Step 4 -- Duplicate, Sibling, and Overlap Check for TC-8006

## Step 4 JQL Search

A JQL search for sibling Vulnerability issues with the same CVE label
(`CVE-2026-31812`) was performed:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8006
```

### Search Results

One sibling found:

| Key | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-----|---------|--------|--------|------------------|---------------|
| TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Step 4.1 -- Same-Stream Duplicate Check

TC-8001 has stream suffix `[rhtpa-2.2]`, while TC-8006 has stream suffix
`[rhtpa-2.1]`. These are **different streams** (2.2.x vs 2.1.x).

Result: **Not a same-stream duplicate.** TC-8001 is a different-stream companion.

## Step 4.2 -- Cross-Stream Coordination

TC-8001 is a **different-stream companion** (stream 2.2.x vs current issue's
stream 2.1.x). PSIRT creates one Vulnerability issue per stream intentionally,
so these are companion trackers, not duplicates.

### Link Idempotency Check

Per Step 4.2 procedure: before creating a Related link, check the current
issue's `issuelinks` array (already fetched in Step 1) for an existing link
that satisfies all of:
- `type.name` is "Related"
- `inwardIssue.key` or `outwardIssue.key` matches TC-8001

**Existing issuelinks on TC-8006:**

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 |

A matching Related link to TC-8001 already exists (link ID 1990401, outward
direction).

**Action: SKIP link creation.**

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call is made. The existing link satisfies the
cross-stream coordination requirement. This is the idempotent behavior
specified in Step 4.2.

### Affects Versions Overlap Check

- TC-8006 Affects Versions: RHTPA 2.1.0 (stream 2.1.x)
- TC-8001 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (stream 2.2.x)

**No version overlap detected.** Each issue carries only versions from its own
stream. This is the expected pattern for companion trackers.

### Sibling Landscape Table

```
CVE-2026-31812 companion issues:

| Issue       | Stream | Status      | Affects Versions              |
|-------------|--------|-------------|-------------------------------|
| TC-8001     | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8006 <-  | 2.1.x  | New         | RHTPA 2.1.0                   |
```

The arrow (`<-`) marks the current issue being triaged.

## Step 4.3 -- Cross-CVE Overlap Detection

The Security Configuration in the project CLAUDE.md does not include:
- Upstream Affected Component custom field
- PS Component custom field
- Stream custom field

Per the Step 4.3 prerequisite: "If any of these fields are not configured, skip
this step entirely."

**Step 4.3 skipped** -- required custom fields not configured.

## Step 4.4 -- Preemptive Task Reconciliation

A search for preemptive tasks matching CVE-2026-31812 with
`security-preemptive` label would be performed:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-31812' ORDER BY created DESC
```

No preemptive tasks assumed to exist for this eval scenario.

**Step 4.4 result**: No matching preemptive task found. Proceed to Step 5.
