## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/11 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 4/5 | 1 | 80% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 4/5 | 1 | 80% |
| eval-18 | 5/5 | 0 | 100% |
| eval-19 | 5/5 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-20 | 1/4 | 3 | 25% |
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
<summary>eval-14: 1 failing assertion</summary>

- **Assertion:** "The rpms.lock.yaml classification remains the primary signal — the SBOM result supplements but does not override it (Step 2.3.5 non-MVP enhancement)"
  **Evidence:** "The output shows 'Origin: CONFLICTING (rpms.lock.yaml says explicit install; SBOM says base image)' for each affected version. Rather than keeping rpms.lock.yaml as the primary classification with SBOM as supplementary context, the output elevates the SBOM to equal status by reclassifying the origin to 'CONFLICTING'. The SBOM Verification Summary further states 'Manual investigation is required to determine the correct origin' and presents two equally-weighted remediation paths. This effectively overrides the rpms.lock.yaml classification rather than supplementing it."

</details>

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "The outputs only demonstrate the case where CVSS is 7.5 (above threshold). While embargo-check.md documents the threshold as 'CVSS &gt;= 7.0', there is no output, statement, or demonstration showing the gate being skipped silently for CVEs with CVSS &lt; 7.0. No below-threshold scenario is addressed anywhere in the output files. Burden of proof is on PASS and no direct evidence exists."

</details>

<details>
<summary>eval-20: 3 failing assertions</summary>

- **Assertion:** "Step 0.3 determines the matrix is within the 14-day threshold and proceeds without displaying a staleness warning"
  **Evidence:** "staleness-check.md lines 29-34 show the agent calculated 29 days elapsed, exceeding the 14-day threshold, and declared 'Result: STALE'. A staleness warning was displayed for both streams rather than proceeding silently."

- **Assertion:** "No user prompt or options are presented for a fresh matrix — the check is silent on success"
  **Evidence:** "staleness-check.md lines 43-56 present explicit options to the user for each stream: '1. Refresh now -- re-run matrix population, 2. Proceed anyway -- continue triage with the current matrix, 3. Stop -- halt triage so I can investigate'. The check was not silent."

- **Assertion:** "The triage continues to Step 0.5 and beyond without interruption from the staleness check"
  **Evidence:** "staleness-check.md lines 63-65 state: 'The staleness warning should be presented to the engineer before proceeding with triage. The engineer must choose an option for each stream before Steps 1-8 can begin.' The staleness check created an explicit interruption point requiring user input before triage could continue."

</details>

<details>
<summary>eval-30: 1 failing assertion</summary>

- **Assertion:** "The missing section is NOT auto-repaired — only Forward Pointer is eligible for auto-repair"
  **Evidence:** "The output confirms Ecosystem Mappings was NOT auto-repaired ('Auto-Repairs Applied: None — no auto-repairable issues detected'). However, the output never states or demonstrates that Forward Pointer is the only section eligible for auto-repair. There is no mention of the Forward Pointer auto-repair eligibility rule anywhere in the output. The Forward Pointer section happened to be present (PASS in the section check), so the auto-repair distinction was never exercised or articulated."

</details>

<details>
<summary>eval-8: 3 failing assertions</summary>

- **Assertion:** "Step 4.3 creates a Related link between the current CVE (TC-8010) and the related CVE (TC-8008) with an idempotency check on existing issuelinks before creating"
  **Evidence:** "overlap-check.md line 58 labels the links as 'Traceability Links (Proposed)' -- the link is proposed, not created. Line 61 shows 'Related link: TC-8010 &lt;-&gt; TC-8008' but there is no evidence of an idempotency check on existing issuelinks before creation. No mention of checking whether a Related link already exists between TC-8010 and TC-8008."

- **Assertion:** "Step 4.3 creates a Depend link from the covering remediation task (TC-8009) to the current CVE (TC-8010) with an idempotency check on existing issuelinks before creating"
  **Evidence:** "overlap-check.md line 58 labels the links as 'Traceability Links (Proposed)' -- the link is proposed, not created. Line 62 shows 'Depend link: TC-8010 -&gt; TC-8009' but there is no evidence of an idempotency check on existing issuelinks before creation. No mention of checking whether a Depend link already exists between TC-8009 and TC-8010."

- **Assertion:** "A comment is posted on the current CVE documenting the cross-CVE overlap finding — including the related CVE key (TC-8008), covering task key (TC-8009), library (axios), bump version (1.9.0), and fix threshold (1.8.2)"
  **Evidence:** "overlap-check.md line 64 labels the comment as 'Cross-CVE Overlap Comment (Proposed)' and triage-outcome.md line 26 lists it under 'Actions (Proposed)'. The comment content (lines 66-72) does contain all required elements: TC-8008, TC-8009, axios, 1.9.0, and 1.8.2. However, the comment is proposed, not posted -- there is no evidence the comment was actually posted to Jira on TC-8010."

</details>

**Pass rate:** 94% · **Tokens:** 48,769 · **Duration:** 104s

**Baseline** (`a27b8b2b`): 100% · 84,263 tokens · 127s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.7*

