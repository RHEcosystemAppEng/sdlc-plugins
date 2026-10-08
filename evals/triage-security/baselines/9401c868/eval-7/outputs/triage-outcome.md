# Triage Outcome -- Step 4.2 Pre-Existing Link Handling for TC-8006

## Summary

TC-8006 (CVE-2026-31812, stream [rhtpa-2.1]) has a **pre-existing Related link**
to sibling issue TC-8001 (CVE-2026-31812, stream [rhtpa-2.2]). Step 4.2 of the
triage-security skill handled this idempotently by detecting the existing link
and skipping link creation.

## Step 4.2 Idempotent Link Logic

The Step 4.2 procedure requires checking for an existing link **before** creating
one. The check examines the current issue's `issuelinks` array (fetched in Step 1)
for any link satisfying ALL of:

1. `type.name` is `"Related"`
2. `inwardIssue.key` or `outwardIssue.key` matches the sibling key

### Applied to TC-8006

**Input:** TC-8006's existing `issuelinks` array contains:
- Link ID: 1990401
  - Type: Related
  - Direction: outward (TC-8006 -> TC-8001)
  - outwardIssue.key: TC-8001

**Evaluation:**
- Condition 1: `type.name == "Related"` -- YES (link type is Related)
- Condition 2: `outwardIssue.key == "TC-8001"` -- YES (matches the sibling key from JQL)

**Both conditions satisfied.** A matching link exists.

### Outcome

**Link creation skipped.** The skill logged:
> "Related link to TC-8001 already exists -- skipping"

No `jira.create_link` call was made. This is the correct idempotent behavior
defined in Step 4.2 of `jira-triage-operations.md`: the skill does not create
duplicate links when a Related link to the sibling already exists, regardless of
link direction (inward or outward).

## Why This Matters

Idempotent link handling prevents duplicate Related links when:
- A previous triage run already linked the issues
- PSIRT or another engineer manually linked the issues before triage
- The sibling's triage (TC-8001) already created the link in the other direction

Without idempotency, re-running triage or triaging a pre-linked issue would
create redundant links, cluttering the issue's link section.

## Remaining Step 4.2 Actions

After the link check, Step 4.2 completed the remaining actions:

1. **Affects Versions overlap check**: No overlap detected. TC-8006 carries only
   2.1.x versions (RHTPA 2.1.0), TC-8001 carries only 2.2.x versions (RHTPA 2.2.0,
   RHTPA 2.2.1). Each issue owns only its own stream's versions.

2. **Sibling landscape presented**:

   | Issue | Stream | Status | Affects Versions |
   |-------|--------|--------|------------------|
   | TC-8001 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
   | TC-8006 (current) | 2.1.x | New | RHTPA 2.1.0 |

## Triage Continues

With Step 4.2 complete (link verified as existing, no version overlap, sibling
landscape presented), triage proceeds to Step 4.3 (Cross-CVE overlap detection),
Step 4.4 (Preemptive task reconciliation), and subsequent steps.
