# TC-8011 — Triage Outcome

**CVE-2026-45678 — webpack < 5.98.0, Arbitrary Code Execution via loader chain (CVSS 7.8) — stream 2.2.x (rhtpa-ui)**

## Decision

**Not closed. Not covered by an existing remediation. New remediation is required (Case B), after a manual version impact check.**

### Why not closed as a cross-CVE overlap

Step 4.3 found related CVE TC-8012 (CVE-2026-43210) for the same upstream component (webpack), PS Component (pscomponent:org/rhtpa-ui) and stream (rhtpa-2.2). Its remediation task TC-8013 bumps webpack only to **5.96.1**. This CVE's fix threshold is **5.98.0**, and 5.96.1 < 5.98.0, so the earlier bump does not cover this CVE. The skill's "related CVEs exist but no covering remediation" branch applies:
- No Related or Depend links to TC-8012/TC-8013 are created by Step 4.3.
- No closure recommendation.
- Proceed to new remediation task creation.

### Why version impact needs manual assessment

- The 2.2.x security matrix Ecosystem Mappings cover only Cargo (backend) and RPM. npm/rhtpa-ui is not mapped, and rhtpa-ui is not in Source Repositories. The skill flags this as an **Unsupported ecosystem: npm** case and requires manual assessment.
- No webpack lock-file data is available. Per the guardrails, no webpack version is invented for any 2.2.x release.
- Therefore Step 2 (version impact table) and Step 3 (Affects Versions correction) cannot be completed automatically. The PSIRT-assigned Affects Versions (RHTPA 2.2.0) is left unchanged pending evidence. Lock-file evidence would need to come from `rhtpa-ui` `package-lock.json` at each pinned 2.2.x build (2.2.0–2.2.4, where 2.2.2 is a retag of 2.2.1) and at dev HEAD.
- Indirect evidence: TC-8013 (Done) put rhtpa-2.2 on webpack 5.96.1, which is still inside the vulnerable range (< 5.98.0). The stream is therefore very likely affected. This is a strong but unverified indication.

## Other step results

| Step | Result |
|---|---|
| 0 Config | Present. The Upstream/PS Component/Stream custom-field IDs are missing from CLAUDE.md Security Configuration. They were taken from the issue/task. Recommend adding them. |
| 0.3 Staleness | Matrix last updated 2026-06-28, 145 days ago. Stale warning. Proceeded anyway (eval). Refresh is recommended. |
| 0.8 Assign | Would assign TC-8011 to the triager and transition New → Assigned (after confirmation). Not executed. |
| 1.5 Enrichment | Not run (no external calls). Used the Jira threshold 5.98.0, with reduced confidence. |
| 1.7 Embargo | Skipped: no embargo policy URL configured (CVSS 7.8 would otherwise trigger it). |
| 4.1/4.2 Siblings | None. |
| 4.3 Overlap | TC-8012/TC-8013 found. **Not covering** (5.96.1 < 5.98.0). |
| 4.4 Preemptive | None. |
| 5 Lifecycle | Not checked (no external calls). 2.2.x is the latest stream and assumed supported. |
| 6 Already fixed | No resolved siblings for CVE-2026-45678. TC-8012's fix does not resolve this CVE. Not already fixed. |
| 7 Concurrent triage | No in-progress webpack triages provided (TC-8012 is Closed). Proceed. |
| 7.5 Release Jira | Would find or create the "RHTPA 2.2.x" release Epic/Task (next patch default 2.2.5 if none exists). **7.5.3 dedup caution:** a component-only match on TC-8013 must NOT suppress task creation, because Step 4.3 proved it does not meet the 5.98.0 threshold, and it is Closed. |
| Case A | Not applicable. The 2.1.x matrix also has no npm mapping, so cross-stream impact is unknown. Recommend a manual check of 2.1.x rhtpa-ui. |

## Recommended remediation (pending engineer confirmation and manual version impact)

npm is a source-dependency ecosystem, so there are 2 tasks for stream 2.2.x:

1. **Dependency bump** (or upstream backport if the 2.2 branch cannot take it): "Bump webpack to >= 5.98.0 in rhtpa-ui [rhtpa-2.2]". Fixes CVE-2026-45678. The current baseline is presumably 5.96.1 from TC-8013. Labels: CVE-2026-45678, ai-generated-jira. Link: TC-8011 → task (Depend). Deployment context: upstream (default). If webpack is build-only, consider adding the `dev-dependency` label and setting priority to Normal per the dependency-scope rules.
2. **Downstream propagation** to the Konflux release repo rhtpa-release.0.4.z. Blocked by task 1 (Blocks). Depend-linked to TC-8011.

Both tasks would be Blocks-linked to the 2.2.x release Task, and TC-8011 would be Related-linked to the release Task.

Optionally, for traceability only, a Related link TC-8011 ↔ TC-8012 could be proposed, since both are webpack CVEs in the same stream. Step 4.3 does not require it in the non-covering case, and no Depend link to TC-8013 should be made.

## Post-triage (after confirmation)

- Add the `ai-cve-triaged` label to TC-8011.
- Post a summary comment with the overlap table above, the manual-assessment note, the created task keys, and the release Jira refs. @mention the reporter and include the Comment Footnote (`triage-security`).

No Jira mutations were performed. All actions above are proposals awaiting engineer confirmation.
