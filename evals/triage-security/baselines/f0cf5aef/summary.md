## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/11 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 5/5 | 0 | 100% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 3/5 | 2 | 60% |
| eval-18 | 5/5 | 0 | 100% |
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 3/4 | 1 | 75% |
| eval-21 | 4/4 | 0 | 100% |
| eval-22 | 4/4 | 0 | 100% |
| eval-23 | 4/4 | 0 | 100% |
| eval-24 | 4/4 | 0 | 100% |
| eval-25 | 4/4 | 0 | 100% |
| eval-26 | 5/5 | 0 | 100% |
| eval-27 | 5/5 | 0 | 100% |
| eval-28 | 5/5 | 0 | 100% |
| eval-29 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-30 | 3/4 | 1 | 75% |
| eval-31 | 4/4 | 0 | 100% |
| eval-32 | 4/4 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 5/8 | 3 | 62% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-17: 2 failing assertions</summary>

- **Assertion:** "Step 0 extracts the Embargo policy URL from the Security Configuration as an optional field without raising an error (§1.71 — backward compatible extraction)"
  **Evidence:** "No Step 0 output file exists. The data-extraction.md file (labeled 'Step 1 -- Data Extraction') does not mention or extract the Embargo policy URL at all. While embargo-check.md (Step 1.7) references the URL as 'configured in Security Configuration' and notes 'Since the Embargo policy URL is configured, this step is not skipped,' this extraction appears in Step 1.7, not Step 0. There is no evidence of a dedicated Step 0 extracting this field as an optional configuration value."

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "The outputs only demonstrate the case where CVSS &gt;= 7.0 (the specific CVE has CVSS 7.5). While embargo-check.md defines the threshold as 'CVSS &gt;= 7.0', there is no explicit evidence in any output file showing what happens when severity is below the threshold. There is no demonstration of the gate being skipped silently for a low-severity CVE, and no explicit statement that the gate is bypassed for CVSS &lt; 7.0. The threshold logic is stated but the below-threshold behavior (silent skip) is not evidenced."

</details>

<details>
<summary>eval-20: 1 failing assertion</summary>

- **Assertion:** "Step 0.3 determines the matrix is within the 14-day threshold and proceeds without displaying a staleness warning"
  **Evidence:** "The agent states the matrix is 'Within 14-day threshold' with status 'Fresh', but the timestamp 2026-06-28T10:00:00Z is approximately 100 days before today's date of 2026-10-06, which is clearly NOT within 14 days. The agent's date calculation is incorrect -- the matrix is actually stale but was incorrectly classified as fresh."

</details>

<details>
<summary>eval-30: 1 failing assertion</summary>

- **Assertion:** "The missing section is NOT auto-repaired — only Forward Pointer is eligible for auto-repair"
  **Evidence:** "The output confirms the missing section is NOT auto-repaired: 'Auto-Repairs Applied: None.' and 'This issue cannot be auto-repaired.' However, the output never states that only Forward Pointer is eligible for auto-repair. It only explains why Ecosystem Mappings cannot be auto-repaired (requires product-specific configuration). There is no evidence that Forward Pointer is identified as the sole auto-repair-eligible section."

</details>

<details>
<summary>eval-8: 3 failing assertions</summary>

- **Assertion:** "Step 4.3 creates a Related link between the current CVE (TC-8010) and the related CVE (TC-8008) with an idempotency check on existing issuelinks before creating"
  **Evidence:** "overlap-check.md Section 6 says 'Traceability Links (would be created)' — conditional language indicating the link was proposed but NOT actually created. triage-outcome.md confirms: 'Triage Actions (would be performed with engineer confirmation)'. Additionally, no explicit idempotency check is performed in Step 4.3 — there is no evidence of checking TC-8010's existing issuelinks for a pre-existing Related link to TC-8008 before proposing the link creation."

- **Assertion:** "Step 4.3 creates a Depend link from the covering remediation task (TC-8009) to the current CVE (TC-8010) with an idempotency check on existing issuelinks before creating"
  **Evidence:** "overlap-check.md Section 6 says 'Traceability Links (would be created)' — conditional language indicating the link was proposed but NOT actually created. triage-outcome.md confirms: 'Triage Actions (would be performed with engineer confirmation)'. No explicit idempotency check is performed — there is no evidence of checking TC-8009's existing issuelinks for a pre-existing Depend link to TC-8010 before proposing the link creation."

- **Assertion:** "A comment is posted on the current CVE documenting the cross-CVE overlap finding — including the related CVE key (TC-8008), covering task key (TC-8009), library (axios), bump version (1.9.0), and fix threshold (1.8.2)"
  **Evidence:** "overlap-check.md Section 6 shows a comment with the heading '(would be posted to TC-8010)' — conditional language indicating the comment was drafted but NOT actually posted. The comment text does contain all required elements (TC-8008, TC-8009, axios, 1.9.0, 1.8.2), but the assertion requires the comment to be 'posted', and the output shows it was only proposed, pending engineer confirmation per triage-outcome.md."

</details>

**Pass rate:** 96% · **Tokens:** 46,471 · **Duration:** 106s

**Baseline** (`f08a8547`): 97% · 55,253 tokens · 119s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.9*

