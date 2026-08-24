# Triage Outcome -- Step 4.2 Pre-existing Link Handling: TC-8006

## Context

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a **pre-existing "Related" link**
to sibling issue TC-8001 (CVE-2026-31812, stream [rhtpa-2.2]). This link was
already present on the issue before triage began:

- Link ID: 1990401
- Type: Related
- Direction: outward (TC-8006 --> TC-8001)

## How Step 4.2 Handled the Pre-existing Link

Step 4.2 defines an **idempotent link creation** protocol. Before creating any
cross-stream "Related" link, the skill checks the current issue's `issuelinks`
array (fetched in Step 1) for an existing link satisfying all of:

1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key (TC-8001)

In this case, the issuelinks array already contains a Related link with
`outwardIssue.key = TC-8001`. Both conditions are satisfied.

### Outcome

The skill **skipped link creation** and logged:

> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call was made. This is the correct idempotent behavior:
the pre-existing link fully satisfies the cross-stream coordination requirement,
and creating a duplicate link would be redundant.

### Remaining Step 4.2 actions (unaffected by the pre-existing link)

The link idempotency check only gates the `create_link` call. The other
Step 4.2 actions proceed normally regardless of whether the link was
pre-existing or newly created:

1. **Affects Versions overlap check** -- verified that TC-8006 (RHTPA 2.1.0)
   and TC-8001 (RHTPA 2.2.0, RHTPA 2.2.1) have no overlapping versions.
   Each issue carries versions only from its own stream.

2. **Sibling landscape presentation** -- the full companion issue table was
   presented to the engineer for awareness:

   | Issue | Stream | Status | Affects Versions |
   |-------|--------|--------|------------------|
   | TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
   | TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Why This Matters

The idempotent link check prevents duplicate "Related" links from accumulating
on an issue when triage is re-run or when links are created by other processes
(e.g., PSIRT tooling, manual linking, or a prior triage run). Without this
check, each triage invocation would add another "Related" link to the same
sibling, cluttering the issue's link list.

The pre-existing link (Link ID 1990401) already establishes the cross-stream
relationship between TC-8006 and TC-8001. Step 4.2's idempotent check
recognizes this and avoids redundant Jira API calls.

## Overall Triage Path

With the sibling check complete:

- **Step 4.1**: No same-stream duplicates found -- TC-8006 is not a duplicate
- **Step 4.2**: Cross-stream sibling TC-8001 identified; pre-existing Related
  link detected and reused (no new link created); no Affects Versions overlap
- **Step 4.3**: Skipped (Upstream Affected Component custom field not configured)
- **Step 4.4**: No preemptive tasks found for this CVE and stream

Triage continues to Step 5 (Version Lifecycle Check) and beyond. Since both
versions in the 2.1.x stream (RHTPA 2.1.0 and RHTPA 2.1.1) ship vulnerable
quinn-proto 0.11.9 (below fix threshold 0.11.14), remediation tasks would be
needed for the 2.1.x stream (Case B), assuming the versions pass the lifecycle
check.
