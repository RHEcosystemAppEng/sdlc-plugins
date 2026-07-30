# Duplicate Check — TC-8003

## Step 4 — Duplicate, Sibling, Overlap, and Reconciliation Check

### JQL Search for Sibling Issues

A JQL search for sibling Vulnerability issues with label `CVE-2026-31812` in project TC
(excluding TC-8003 itself) returns **one result**:

| Issue | Status | Labels | Affects Versions | Stream Suffix |
|-------|--------|--------|------------------|---------------|
| TC-7999 | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

### Duplicate Classification

**TC-8003 is a same-stream duplicate of TC-7999.**

Reasoning:
1. **Same CVE**: Both issues carry the label `CVE-2026-31812`.
2. **Same stream**: Both issues have the stream suffix `[rhtpa-2.2]`, mapping to the 2.2.x version stream.
3. **Same component**: Both issues carry the label `pscomponent:org/rhtpa-server`.
4. **TC-7999 is already active**: TC-7999 is in `In Progress` status, meaning triage and remediation are already underway.
5. **Affects Versions overlap**: TC-7999 already covers RHTPA 2.2.0 and RHTPA 2.2.1. TC-8003 only lists RHTPA 2.2.0 (a subset of TC-7999's coverage).

When two Vulnerability issues target the same CVE within the same stream, the newer
issue is the duplicate. TC-8003 (status: New) is the newer issue; TC-7999 (status: In Progress)
is the original that is already being remediated.

### Recommended Actions

1. **Link TC-8003 to TC-7999** with link type "Duplicate" (TC-8003 is duplicated by TC-7999).
2. **Close TC-8003** as a duplicate with resolution "Duplicate".
3. **Post a comment on TC-8003** explaining the duplicate finding:

   > This issue is a duplicate of TC-7999, which covers the same CVE (CVE-2026-31812)
   > in the same stream [rhtpa-2.2] and is already In Progress.
   >
   > TC-7999 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1
   > TC-8003 Affects Versions: RHTPA 2.2.0 (subset of TC-7999)
   >
   > Closing this issue as Duplicate. Remediation is tracked under TC-7999.

4. **Add the `ai-cve-triaged` label** to TC-8003 to mark it as triaged.

### Affects Versions Note

TC-8003 lists only RHTPA 2.2.0, while TC-7999 already lists RHTPA 2.2.0 and RHTPA 2.2.1.
The version impact analysis (Step 2) shows RHTPA 2.2.2 is also affected. However, since
TC-8003 is being closed as a duplicate, the Affects Versions correction should be applied
to TC-7999 (the surviving issue) rather than TC-8003. TC-7999 may need RHTPA 2.2.2 added
to its Affects Versions, but that is outside the scope of triaging TC-8003.

### Cross-CVE Overlap (Step 4.3)

The Upstream Affected Component custom field is not configured in Security Configuration.
Step 4.3 (cross-CVE overlap detection) is skipped.

### Preemptive Task Reconciliation (Step 4.4)

Not applicable — TC-8003 is being closed as a duplicate, so no remediation tasks are
being created that would need reconciliation.
