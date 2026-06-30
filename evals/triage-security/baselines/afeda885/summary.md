## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/10 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 4/5 | 1 | 80% |
| eval-15 | 4/5 | 1 | 80% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 3/5 | 2 | 60% |
| eval-2 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 5/6 | 1 | 83% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 5/5 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-14: 1 failing assertion</summary>

- **Assertion:** "The SBOM verification result is presented alongside the rpms.lock.yaml result in the dependency chain output, not as a separate section (Step 2.3.5 sub-step 6)"
  **Evidence:** "The SBOM results are in a separate file (sbom-verification.md) from the main version impact/dependency chain output (version-impact.md). version-impact.md contains only rpms.lock.yaml data in its dependency version extraction table (lines 18-31) and version impact table (lines 35-43) with no SBOM information. While sbom-verification.md does present both signals side-by-side within its own tables, the SBOM data is not integrated into the main dependency chain output — it exists as a separate document/section."

</details>

<details>
<summary>eval-15: 1 failing assertion</summary>

- **Assertion:** "Step 0 extracts the ProdSec Jira account ID from the Security Configuration as an optional field without raising an error (Step 0 config validation)"
  **Evidence:** "In data-extraction.md (covering Step 0/Step 1), there is no explicit mention of extracting a ProdSec Jira account ID from Security Configuration. The file lists parsed CVE data fields (lines 5-23) but does not include a ProdSec account ID field or reference Security Configuration extraction. While the ProdSec account ID '557058:prodsec-mock-account-id' is used in Step 3 (affects-versions.md line 28), there is no evidence in the outputs that Step 0 specifically extracted it from Security Configuration as an optional field or performed config validation for this field."

</details>

<details>
<summary>eval-17: 2 failing assertions</summary>

- **Assertion:** "Step 0 extracts the Embargo policy URL from the Security Configuration as an optional field without raising an error (§1.71 — backward compatible extraction)"
  **Evidence:** "There is no Step 0 output file or section in any output. The data-extraction.md is labeled 'Step 1 — Data Extraction' and does not mention the embargo policy URL. The embargo policy URL appears in embargo-check.md (Step 1.7) line 5: 'Embargo policy URL is configured in Security Configuration: https://example.com/security/embargo-policy', but this is Step 1.7 not Step 0, and there is no indication the field is treated as optional (no mention of optionality, fallback behavior, or backward compatibility handling when the field is absent)."

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "The outputs only demonstrate the positive case (CVSS 7.5, which exceeds the threshold). While embargo-check.md defines the threshold as 'CVSS &gt;= 7.0', there is no explicit statement or evidence that the gate is skipped silently for CVEs below this threshold. No output file mentions behavior for Low or Moderate severity CVEs, and no evidence of silent skipping is documented. The threshold definition alone does not constitute evidence that below-threshold CVEs are handled correctly by being silently skipped."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Dependency chain context includes an SBOM verification line — either showing the cosign comparison result or noting that SBOM verification was skipped because cosign is not available (Step 2.3.5 Optional SBOM verification)"
  **Evidence:** "version-impact.md lines 24-31 contain the Dependency Chain Context section. It includes only: rpms.lock.yaml presence check, origin classification ('explicit install'), and remediation guidance. There is no SBOM verification line — no mention of cosign, SBOM, or any indication that SBOM verification was performed or skipped."

</details>

**Pass rate:** 94% · **Tokens:** 51,293 · **Duration:** 122s

**Baseline** (`7142c02`): 98% · 41,725 tokens · 94s

