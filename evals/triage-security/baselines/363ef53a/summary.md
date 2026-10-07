## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/11 | 0 | 100% |
| eval-10 | 3/5 | 2 | 60% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 4/5 | 1 | 80% |
| eval-14 | 4/5 | 1 | 80% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 5/5 | 0 | 100% |
| eval-18 | 5/5 | 0 | 100% |
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 4/4 | 0 | 100% |
| eval-21 | 4/4 | 0 | 100% |
| eval-22 | 4/4 | 0 | 100% |
| eval-23 | 4/4 | 0 | 100% |
| eval-24 | 3/4 | 1 | 75% |
| eval-25 | 4/4 | 0 | 100% |
| eval-26 | 5/5 | 0 | 100% |
| eval-27 | 5/5 | 0 | 100% |
| eval-28 | 5/5 | 0 | 100% |
| eval-29 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-30 | 4/4 | 0 | 100% |
| eval-31 | 4/4 | 0 | 100% |
| eval-32 | 4/4 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 5/6 | 1 | 83% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 8/8 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-10: 2 failing assertions</summary>

- **Assertion:** "Step 8 Case A creates standard remediation tasks for the current stream (rhtpa-2.2) with standard labels ['ai-generated-jira', 'Security', 'CVE-2026-55123'] and 'Depend' link to TC-8020"
  **Evidence:** "The output creates standard remediation tasks for rhtpa-2.2 with the correct labels (ai-generated-jira, Security, CVE-2026-55123) and 'Depend' link to TC-8020, but labels this as 'Case B', not 'Case A'. remediation.md line 12: 'Case B: Standard Remediation Tasks for Current Stream (rhtpa-2.2)'. The triage outcome on line 5 also states 'Case B (affected): stream rhtpa-2.2 is affected -- create standard remediation tasks'. The assertion specifies 'Case A' but the output assigns 'Case B' to the current stream's standard tasks."

- **Assertion:** "Step 8 Case B detects that stream rhtpa-2.1 is also affected but has no CVE Jira — creates proactive preemptive remediation tasks (§1.60)"
  **Evidence:** "The output creates preemptive remediation tasks for rhtpa-2.1 (detecting it is affected with no CVE Jira), but labels this as 'Case A', not 'Case B'. remediation.md line 5: 'Case A (cross-stream impact): stream rhtpa-2.1 is also affected, no CVE Jira exists for that stream -- create preemptive remediation tasks'. Line 124: 'Case A: Preemptive Remediation Tasks for Stream rhtpa-2.1'. The assertion specifies 'Case B' but the output assigns 'Case A' to the cross-stream preemptive tasks."

</details>

<details>
<summary>eval-13: 1 failing assertion</summary>

- **Assertion:** "The remediation output sequences digest comments BEFORE issue links (Depend, Blocks) or other comments in the described procedure for each task (§1.66, shared/description-digest-protocol.md Rules)"
  **Evidence:** "In all four tasks, the Jira linkage step is described BEFORE the digest comment step. Task 1: 'Jira linkage' with Depend link at lines 100-103, then 'Description Digest Comment' at lines 105-123. Task 2: 'Jira linkage' with Depend and Blocks links at lines 187-190, then 'Description Digest Comment' at lines 194-211. Task 3: 'Jira linkage (preemptive)' with Related link at lines 293-295, then 'Description Digest Comment' at lines 299-315. Task 4: 'Jira linkage (preemptive)' with Related and Blocks links at lines 385-388, then 'Description Digest Comment' at lines 390-408. The digest comments are sequenced AFTER issue links in all four cases, violating the required ordering."

</details>

<details>
<summary>eval-14: 1 failing assertion</summary>

- **Assertion:** "The rpms.lock.yaml classification remains the primary signal -- the SBOM result supplements but does not override it (Step 2.3.5 non-MVP enhancement)"
  **Evidence:** "In version-impact.md, when SBOM disagrees with rpms.lock.yaml, the output sets 'Origin: CONFLICTING -- investigate manually' (lines 45, 59, 75) rather than keeping the rpms.lock.yaml classification as primary. The classification summary table shows Agreement column as 'NO -- disagrees' with no indication that rpms.lock.yaml takes precedence. The final paragraph (lines 92-93) states 'This discrepancy requires manual investigation to determine the true origin' -- effectively putting both signals on equal footing rather than treating rpms.lock.yaml as the primary signal that SBOM merely supplements. The SBOM result overrides the rpms.lock.yaml classification from 'explicit install' to 'CONFLICTING'."

</details>

<details>
<summary>eval-24: 1 failing assertion</summary>

- **Assertion:** "Step 0 detects the absence of the Deployment Context column in the Source Repositories table and defaults all repositories to upstream (§1.78)"
  **Evidence:** "data-extraction.md lines 38-42: The output detects the absence of the Deployment Context column ('The Source Repositories table does not have a Deployment Context column') but does NOT explicitly default repositories to 'upstream'. Instead it states: 'Per backward compatibility rules, coordination guidance is omitted from remediation task descriptions.' The word 'upstream' does not appear anywhere in the deployment context section. Compare with eval-28's data-extraction.md which does explicitly say 'Result: default to upstream'. The assertion requires defaulting to upstream, which is not recorded."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Each listed issue shows: issue key, status, CVE ID (from labels), summary, and created date"
  **Evidence:** "Most issues show all five fields, but the 'Excluded from Ready for QA' table (lines 73-74 in discovery-listing.md) lists TC-9023 and TC-9026 with columns Issue, Status, CVE, Reason — omitting both the full summary and created date. Additionally, the untriaged issues tables (sections 1) lack a per-row Status column, conveying status only via section headers."

</details>

**Pass rate:** 96% · **Tokens:** 58,613 · **Duration:** 102s

**Baseline** (`6f9a9909`): 97% · 55,789 tokens · 118s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.9*

