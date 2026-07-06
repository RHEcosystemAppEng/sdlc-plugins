# Ready for QA — Filtering Analysis

## Query Construction

The Ready for QA query identifies triaged CVE Vulnerability issues that are not yet closed or in QA, so their linked remediation Tasks can be inspected for completion.

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Parameters used:**
- Project key: `TC` (from Jira Configuration)
- Issue type ID: `10024` (Vulnerability, from Security Configuration)
- Label filter: `ai-cve-triaged` (only previously triaged issues)
- Status exclusions: `Closed`, `Verified`, `ON_QA` (already past the transition point)
- Fields requested: `summary`, `labels`, `status`, `created`, `issuelinks`

**Results returned:** 3 candidate issues

---

## Filtering Criteria

Per the SKILL.md discovery mode protocol, each candidate is evaluated by inspecting its `issuelinks` for linked Tasks with link type "Depend":

1. **ALL linked remediation Tasks are Done or Closed** --> qualifies as Ready for QA
2. **ANY linked Task is still open** --> excluded (remediation in progress)
3. **NO linked Tasks with type "Depend" exist** --> excluded (no remediation to verify)

---

## Per-Issue Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

| Field | Value |
|-------|-------|
| Status | Modified |
| CVE | CVE-2026-38901 |
| Created | 2026-05-15 |
| Labels | CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged |

**Linked Remediation Tasks (Depend):**

| Task Key | Issue Type | Status | Terminal? |
|----------|-----------|--------|-----------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Evaluation:** ALL 2 linked remediation Tasks are in terminal status (Done or Closed).

**Result: QUALIFIES — Ready for QA**

**Recommendation:** Consider transitioning TC-9020 to ON_QA. All remediation work is complete and the fix is ready for verification.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

| Field | Value |
|-------|-------|
| Status | In Progress |
| CVE | CVE-2026-39102 |
| Created | 2026-05-10 |
| Labels | CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged |

**Linked Remediation Tasks (Depend):**

| Task Key | Issue Type | Status | Terminal? |
|----------|-----------|--------|-----------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Evaluation:** TC-9025 is still In Progress. 1 of 2 linked Tasks is incomplete.

**Result: EXCLUDED — Remediation in progress**

TC-9025 must reach Done or Closed before TC-9023 can be considered for ON_QA transition.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

| Field | Value |
|-------|-------|
| Status | Modified |
| CVE | CVE-2026-39330 |
| Created | 2026-05-05 |
| Labels | CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged |

**Linked Remediation Tasks (Depend):** None

**Evaluation:** No linked Tasks with link type "Depend" exist on this issue.

**Result: EXCLUDED — No remediation to verify**

This issue has no linked remediation Tasks. It may need re-triage to determine whether remediation tasks should be created, or it may have been triaged as not affected but not yet closed.

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Done? | Ready for QA? |
|-------|-----|--------|-------------|-----------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**Qualifying issues:** 1 of 3

**Action items:**
- **TC-9020**: Consider transitioning to ON_QA. All remediation Tasks are complete.
