## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 13/13 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 5/5 | 0 | 100% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 4/5 | 1 | 80% |
| eval-18 | 5/5 | 0 | 100% |
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 4/4 | 0 | 100% |
| eval-21 | 4/4 | 0 | 100% |
| eval-22 | 4/4 | 0 | 100% |
| eval-23 | 4/4 | 0 | 100% |
| eval-24 | 4/4 | 0 | 100% |
| eval-25 | 4/4 | 0 | 100% |
| eval-26 | 5/5 | 0 | 100% |
| eval-27 | 3/5 | 2 | 60% |
| eval-28 | 5/5 | 0 | 100% |
| eval-29 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-30 | 4/4 | 0 | 100% |
| eval-31 | 4/4 | 0 | 100% |
| eval-32 | 4/4 | 0 | 100% |
| eval-33 | 8/8 | 0 | 100% |
| eval-34 | 7/7 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 5/6 | 1 | 83% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 6/8 | 2 | 75% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "The eval scenario only tests a CVSS 7.5 (High) CVE, which is above threshold. While embargo-check.md line 16 defines the threshold as 'Critical or Important (CVSS &gt;= 7.0)', there is no output demonstrating below-threshold behavior. No file shows a Low or Moderate CVE being processed with the gate skipped silently. The positive-case threshold definition alone does not constitute evidence that below-threshold CVEs are handled correctly (skipped silently rather than, e.g., shown as informational)."

</details>

<details>
<summary>eval-27: 2 failing assertions</summary>

- **Assertion:** "The VEX justification prompt recommends 'Vulnerable Code not in Execute Path' as the justification for skipping remediation"
  **Evidence:** "feature-gate-prompt.md recommends 'Vulnerable Code not Present' (stated twice: 'Recommended VEX justification: **Vulnerable Code not Present**' and 'it should be set to: **Vulnerable Code not Present**'), not the required 'Vulnerable Code not in Execute Path'. While version-impact.md mentions 'Vulnerable Code not in Execute Path' in the Step 2.3.5 remediation note, the actual VEX justification prompt uses a different justification."

- **Assertion:** "If the user chooses to skip remediation, the version is closed as not affected with the VEX justification — no remediation tasks are created for that version"
  **Evidence:** "No output file shows the result of the user choosing the skip option. feature-gate-prompt.md ends at 'Choose (1/2):' with no subsequent output demonstrating the skip path was executed. No evidence of versions being closed as not affected and no evidence that remediation tasks were skipped."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Each listed issue shows: issue key, status, CVE ID (from labels), summary, and created date"
  **Evidence:** "Most issues show all five fields, but the 'Excluded from Ready for QA' table in discovery-listing.md (lines 72-75) lists TC-9023 and TC-9026 with columns: Issue, Status, CVE, Summary, Exclusion Reason — the 'Created' date column is replaced by 'Exclusion Reason', so these two listed issues are missing created date. All other issues (TC-9001, TC-9002, TC-9003, TC-9004 in Query 1; TC-9010 in Query 2; TC-9020 in Query 3) do show all five fields."

</details>

<details>
<summary>eval-8: 2 failing assertions</summary>

- **Assertion:** "Step 4.3 creates a Related link between the current CVE (TC-8010) and the related CVE (TC-8008) with an idempotency check on existing issuelinks before creating"
  **Evidence:** "overlap-check.md line 61 proposes 'create_link(inwardIssue: TC-8010, outwardIssue: TC-8008, type: "Related")' but there is no explicit idempotency check documented in Step 4.3. While data-extraction.md line 24 notes 'Existing Issue Links | (none)' in Step 1, Step 4.3 itself does not reference or verify existing issuelinks on TC-8010 or TC-8008 before proposing the Related link creation. No conditional check such as 'if link does not already exist' is present."

- **Assertion:** "Step 4.3 creates a Depend link from the covering remediation task (TC-8009) to the current CVE (TC-8010) with an idempotency check on existing issuelinks before creating"
  **Evidence:** "overlap-check.md line 64 proposes 'create_link(inwardIssue: TC-8010, outwardIssue: TC-8009, type: "Depend")' but there is no explicit idempotency check documented in Step 4.3. The overlap-check.md Proposed Actions section does not mention verifying whether a Depend link between TC-8009 and TC-8010 already exists before creating one. No conditional or deduplication logic is documented."

</details>

**Pass rate:** 97% · **Tokens:** 65,259 · **Duration:** 149s

**Baseline** (`f32bd713`): 99% · 59,221 tokens · 139s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10*

