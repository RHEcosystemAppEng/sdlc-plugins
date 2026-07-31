# Step 4 -- Duplicate, Sibling, and Overlap Check

## Sibling Issue Search

### JQL Query

The following JQL query is used to search for sibling Vulnerability issues with the same CVE label, excluding the current issue:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

### Search Results

The JQL search returned **1 result**:

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Sibling Classification

### TC-7999

- **TC-7999 stream suffix**: `[rhtpa-2.2]` --> stream 2.2.x
- **TC-8003 stream suffix**: `[rhtpa-2.2]` --> stream 2.2.x
- **Classification**: **Same-stream sibling** -- both issues track the same CVE (CVE-2026-31812) for the same stream (2.2.x)

Since TC-7999 has the same stream suffix `[rhtpa-2.2]` as the current issue TC-8003, this is a **same-stream duplicate**, not a cross-stream companion.

## Step 4.1 -- Same-Stream Duplicate Detection

TC-7999 is a same-stream sibling that is currently **In Progress** (open and actively being worked on). Per Step 4.1 of the triage-security skill:

- TC-7999 is open and in progress, tracking the same CVE-2026-31812 for the same stream 2.2.x
- TC-7999 already has corrected Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1
- TC-8003 is a duplicate of TC-7999

**Recommendation**: Close TC-8003 as **Duplicate** of TC-7999.

### Sibling Landscape

```
CVE-2026-31812 companion issues:

| Issue      | Stream | Status      | Affects Versions          |
|------------|--------|-------------|---------------------------|
| TC-7999    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8003 <- | 2.2.x  | New         | RHTPA 2.2.0              |
```

Both issues track the **same CVE** (CVE-2026-31812) for the **same stream** (2.2.x). TC-7999 is already In Progress with more complete Affects Versions. TC-8003 is a duplicate and should be closed.

## Steps 4.3 and 4.4

Skipped -- duplicate detection short-circuits the triage flow. No cross-CVE overlap or preemptive task reconciliation is needed.
