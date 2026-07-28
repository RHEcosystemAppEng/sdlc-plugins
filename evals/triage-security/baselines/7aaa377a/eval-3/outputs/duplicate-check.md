# Step 4 -- Duplicate, Sibling, and Overlap Check

## Sibling Search

Searched for sibling Vulnerability issues with the same CVE label, excluding the
current issue:

**JQL query:**
```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

**Results:** 1 sibling found.

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Sibling Classification

**TC-7999 stream suffix**: `[rhtpa-2.2]`
**TC-8003 stream suffix**: `[rhtpa-2.2]`

Both issues have the **same stream suffix** (`[rhtpa-2.2]`), meaning they track
the same CVE for the same version stream. TC-7999 is classified as a
**same-stream sibling**.

## Step 4.1 -- Same-Stream Duplicate Detection

TC-7999 is a same-stream sibling that is currently **In Progress**. Per Step 4.1,
when a same-stream sibling exists and is open or in progress, the current issue
(TC-8003) should be closed as a Duplicate.

**Classification**: TC-7999 is a **duplicate** of TC-8003 (or rather, TC-8003 is
a duplicate of TC-7999, since TC-7999 was created first and is already In Progress).

**Sibling landscape:**

```
CVE-2026-31812 companion issues:

| Issue     | Stream | Status      | Affects Versions            |
|-----------|--------|-------------|-----------------------------|
| TC-7999   | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1   |
| TC-8003 * | 2.2.x  | New         | RHTPA 2.2.0                 |

(* = current issue, duplicate)
```

TC-7999 is already In Progress and has a more complete set of Affects Versions
(RHTPA 2.2.0, RHTPA 2.2.1), indicating it has already undergone triage. TC-8003
is a duplicate entry tracking the same CVE for the same stream.

## Duplicate Decision

**Recommendation**: Close TC-8003 as Duplicate of TC-7999.

Triage does **not** proceed to Steps 5, 6, 7, or 8. Duplicate detection
short-circuits the triage flow -- no version impact analysis, no remediation
task creation, no Affects Versions correction is performed for TC-8003.
