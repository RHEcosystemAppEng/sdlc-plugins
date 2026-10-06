# Ready for QA — Detailed Filtering Analysis

## Overview

Query 3 searches for triaged Vulnerability issues that are not yet Closed,
Verified, or ON_QA. For each candidate, the linked remediation Tasks (link
type "Depend") are inspected to determine whether all remediation work is
complete.

**JQL used:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged)
  AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**3 candidates** returned. Each is evaluated below.

---

## Candidate 1: TC-9020

**CVE-2026-38901** -- hyper - HTTP request smuggling [rhtpa-2.2]
**Status:** Modified
**Created:** 2026-05-15

### Linked Remediation Tasks (Depend)

| Linked Task | Type | Status |
|-------------|------|--------|
| TC-9021 | Task | Done |
| TC-9022 | Task | Closed |

### Analysis

- TC-9021 is **Done** (terminal state).
- TC-9022 is **Closed** (terminal state).
- **All** 2 linked remediation Tasks are in a completed state.

### Verdict: READY FOR QA

All linked remediation Tasks are Done or Closed. TC-9020 is a candidate for
transition to ON_QA.

---

## Candidate 2: TC-9023

**CVE-2026-39102** -- rustls - Certificate validation bypass [rhtpa-2.1]
**Status:** In Progress
**Created:** 2026-05-10

### Linked Remediation Tasks (Depend)

| Linked Task | Type | Status |
|-------------|------|--------|
| TC-9024 | Task | Done |
| TC-9025 | Task | In Progress |

### Analysis

- TC-9024 is **Done** (terminal state).
- TC-9025 is **In Progress** (still open -- remediation work ongoing).
- At least one linked Task is not in a completed state.

### Verdict: EXCLUDED (remediation in progress)

TC-9025 is still In Progress. The CVE cannot move to ON_QA until all
remediation Tasks are completed.

---

## Candidate 3: TC-9026

**CVE-2026-39330** -- openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]
**Status:** Modified
**Created:** 2026-05-05

### Linked Remediation Tasks (Depend)

No issue links with type "Depend" found.

### Analysis

- The issue has no linked remediation Tasks.
- Without Depend-linked Tasks, there is no remediation work to verify completion of.

### Verdict: EXCLUDED (no remediation to verify)

No linked Tasks with type "Depend" exist. Cannot determine remediation
completeness -- the issue may need remediation tasks created first.

---

## Summary

| Issue | CVE | Status | Linked Tasks | All Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No -- TC-9025 open |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No -- no Depend links |

**Result:** 1 of 3 candidates qualifies for QA transition (TC-9020).
