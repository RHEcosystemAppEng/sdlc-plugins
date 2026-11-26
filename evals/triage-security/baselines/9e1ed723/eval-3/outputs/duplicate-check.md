# Step 4 – Duplicate, Sibling, Overlap, and Reconciliation Check: TC-8003

## Sibling search (simulated)

JQL that would be run:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

Simulated result: 1 issue.

| Issue | Summary | Stream suffix | Stream | Status | Affects Versions |
|-------|---------|---------------|--------|--------|------------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8003 (current) | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | 2.2.x | New | RHTPA 2.2.0 |

## Classification

- **TC-7999 is a same-stream sibling.** It has the same CVE label (CVE-2026-31812), the same stream suffix `[rhtpa-2.2]` (2.2.x), the same component label `pscomponent:org/rhtpa-server`, and an identical summary.
- TC-7999 is **open (In Progress)**, so Step 4.1 (Same-stream duplicates) applies.
- No different-stream siblings were found, so Step 4.2 creates no cross-stream Related links.

## 4.1 – Same-stream duplicate result

**Recommendation: Close TC-8003 as Duplicate of TC-7999.**

Supporting evidence:
- Both issues track the same CVE for the same stream (2.2.x).
- Affects Versions overlap. TC-8003's only version (RHTPA 2.2.0) is already covered by TC-7999 (RHTPA 2.2.0, 2.2.1), so TC-8003 adds no version coverage.
- The version impact analysis confirms the overlap. Within 2.2.x the affected versions are 2.2.0, 2.2.1 and 2.2.2, and none of these fall outside what TC-7999 is meant to track.
- TC-7999 is already In Progress, which means someone is working on it. Remediation should stay with TC-7999 so that duplicate remediation tasks are not created.

Proposed Jira actions (require engineer confirmation; NOT executed in this eval):

1. Add a comment on TC-8003:
   > Duplicate of TC-7999 — same CVE (CVE-2026-31812) tracked for the same stream 2.2.x
   > ([rhtpa-2.2]). Version impact analysis confirms overlap: within 2.2.x, quinn-proto
   > < 0.11.14 ships in RHTPA 2.2.0 (0.11.9), 2.2.1 (0.11.12) and 2.2.2 (retag of 2.2.1);
   > 2.2.3 and 2.2.4 ship 0.11.14 (not affected). TC-8003's Affects Versions (RHTPA 2.2.0)
   > is a subset of TC-7999's.
   >
   > (Comment Footnote per shared/comment-footnote.md, skill name `triage-security`)
2. Transition TC-8003 to Closed with resolution **Duplicate**.
3. Assign TC-8003 to the current user. Step 0.8 already proposes this.
4. Optional traceability: link TC-8003 to TC-7999 with a Duplicate or Related link.

## Additional findings to raise on TC-7999 (advisory)

- **Affects Versions may be incomplete on TC-7999.** The matrix lists RHTPA 2.2.2 as a backend retag of 2.2.1 (`v0.4.8`, quinn-proto 0.11.12), which makes 2.2.2 affected too. TC-7999 lists only 2.2.0 and 2.2.1. The owner of TC-7999 should consider adding RHTPA 2.2.2. This is advisory only; TC-7999 is not modified by this triage.
- **Cross-stream gap.** Stream 2.1.x (2.1.0 and 2.1.1, both quinn-proto 0.11.9) is also affected, and the sibling search found no 2.1.x tracker. TC-8003 is being closed as a duplicate, so Case A preemptive task creation for 2.1.x is not done from TC-8003. That decision belongs to the canonical 2.2.x issue (TC-7999) or a PSIRT-created 2.1.x issue. The finding is reported here so it is not lost.

## 4.3 – Cross-CVE overlap detection

Skipped. The Upstream Affected Component, PS Component and Stream custom fields are not
configured in Security Configuration.

## 4.4 – Preemptive task reconciliation

Not needed. TC-8003 is closed as a duplicate, so it does not take ownership of any
remediation task. If a preemptive task labelled `security-preemptive` + `CVE-2026-31812`
exists for `rhtpa-2.2`, it should be reconciled against TC-7999, the canonical issue.
