## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/11 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 4/5 | 1 | 80% |
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
| eval-23 | 3/4 | 1 | 75% |
| eval-24 | 4/4 | 0 | 100% |
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
| eval-8 | 5/8 | 3 | 62% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-13: 1 failing assertion</summary>

- **Assertion:** "The remediation output sequences digest comments BEFORE issue links (Depend, Blocks) or other comments in the described procedure for each task (§1.66, shared/description-digest-protocol.md Rules)"
  **Evidence:** "In remediation.md, the document structure consistently places the Jira link sections BEFORE the digest comment sections for all tasks. Task 1: '**Jira link:**' with create_link (Depend) at lines 78-85 appears before '#### Description Digest Comment (Task 1)' at line 87. Task 2: '**Jira links:**' with create_link (Depend, Blocks) at lines 174-189 appears before digest section at line 191. Task 3: '**Jira link**' (Related) at lines 306-313 appears before digest section at line 315. Task 4: '**Jira links:**' (Related, Blocks) at lines 404-420 appears before digest section at line 422. While each digest section's step 4 contains a parenthetical '(before creating issue links or other comments)', the document's structural ordering contradicts this by presenting links first in the procedural flow. Contradictory evidence per grading rule 6."

</details>

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "The outputs only demonstrate the positive case (CVSS 7.5 triggering the gate). While embargo-check.md line 11 defines the threshold as 'CVSS &gt;= 7.0', there is no explicit evidence of what happens when severity is below 7.0. No output file documents the below-threshold behavior or confirms silent skipping. The threshold definition alone is insufficient -- there is no demonstration or explicit statement that the gate is skipped silently for Low/Moderate CVEs."

</details>

<details>
<summary>eval-23: 1 failing assertion</summary>

- **Assertion:** "Step 0 extracts the Deployment Context column from the Source Repositories table and parses rhtpa-backend as customer-shipped (§1.77)"
  **Evidence:** "No Step 0 section exists in the outputs. The data-extraction.md begins at 'Step 1 -- Data Extraction: TC-8001'. The Deployment Context Lookup does appear in Step 1 (lines 39-52) and correctly extracts the column and parses rhtpa-backend as customer-shipped, but the assertion specifically requires Step 0 to perform this extraction. Compare with eval 24 where Step 0 explicitly handles Source Repositories and Deployment Context column detection. Burden of proof on PASS: the required step is absent."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Each listed issue shows: issue key, status, CVE ID (from labels), summary, and created date"
  **Evidence:** "Most issues show all five fields, but the 'Excluded from Ready for QA' table in discovery-listing.md (lines 85-87) lists TC-9023 and TC-9026 with columns: Issue, Status, CVE, Summary, Reason -- but omits the Created date column. TC-9023 shows 'In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1]' and TC-9026 shows 'Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]', both without created dates."

</details>

<details>
<summary>eval-8: 3 failing assertions</summary>

- **Assertion:** "Step 4.3 creates a Related link between the current CVE (TC-8010) and the related CVE (TC-8008) with an idempotency check on existing issuelinks before creating"
  **Evidence:** "The link was proposed but not confirmed as created. overlap-check.md line 58 uses conditional language: 'the following links and comment would be created'. triage-outcome.md line 30 lists this under 'Proposed Jira Actions (pending engineer confirmation)'. While data-extraction.md lines 46-48 show an idempotency check ('Existing Issue Links: No existing links on TC-8010'), the link creation itself was not executed -- only proposed."

- **Assertion:** "Step 4.3 creates a Depend link from the covering remediation task (TC-8009) to the current CVE (TC-8010) with an idempotency check on existing issuelinks before creating"
  **Evidence:** "Same as the Related link: the Depend link was proposed but not confirmed as created. overlap-check.md line 60: 'Depend link: TC-8010 -&gt; TC-8009 (covering remediation task)' appears under 'the following links and comment would be created'. triage-outcome.md line 33 lists it under 'Proposed Jira Actions (pending engineer confirmation)'. No evidence of actual API call execution or confirmation of link creation."

- **Assertion:** "A comment is posted on the current CVE documenting the cross-CVE overlap finding — including the related CVE key (TC-8008), covering task key (TC-8009), library (axios), bump version (1.9.0), and fix threshold (1.8.2)"
  **Evidence:** "The comment content is drafted in overlap-check.md lines 63-69 and contains all required elements (TC-8008, TC-8009, axios, 1.9.0, 1.8.2). However, it was not actually posted. overlap-check.md line 58 says 'the following links and comment would be created' (conditional). triage-outcome.md line 34 lists 'Post overlap comment on TC-8010' under 'Proposed Jira Actions (pending engineer confirmation)'. No evidence the comment was actually posted to Jira."

</details>

**Pass rate:** 96% · **Tokens:** 62,341 · **Duration:** 125s

**Baseline** (`363ef53a`): 96% · 58,613 tokens · 102s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.10*

