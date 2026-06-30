## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/10 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 2/5 | 3 | 40% |
| eval-15 | 4/5 | 1 | 80% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 4/5 | 1 | 80% |
| eval-2 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 5/6 | 1 | 83% |
| eval-6 | 5/6 | 1 | 83% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 5/5 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-14: 3 failing assertions</summary>

- **Assertion:** "SBOM verification uses cosign download sbom to compare the final container image SBOM against the base image SBOM (Step 2.3.5 sub-steps 2 and 4)"
  **Evidence:** "sbom-verification.md only shows '$ which cosign' being run to confirm cosign availability. No 'cosign download sbom' command is shown or referenced anywhere in the output files. The 'Final image SBOM' and 'Base image SBOM' rows appear in the tables without any command evidence showing cosign download sbom was used to obtain them."

- **Assertion:** "The rpms.lock.yaml classification remains the primary signal — the SBOM result supplements but does not override it (Step 2.3.5 non-MVP enhancement)"
  **Evidence:** "version-impact.md line 28 labels the origin as '**disputed**' rather than keeping rpms.lock.yaml as the primary signal. sbom-verification.md states 'Until this disagreement is resolved, the remediation task template should note both possible paths' and presents both remediation paths as equal alternatives, not treating rpms.lock.yaml as primary. There is no statement in any output file that rpms.lock.yaml is the authoritative/primary signal."

- **Assertion:** "The SBOM verification result is presented alongside the rpms.lock.yaml result in the dependency chain output, not as a separate section (Step 2.3.5 sub-step 6)"
  **Evidence:** "While version-impact.md does show both results together in lines 22-28, a dedicated standalone file 'sbom-verification.md' exists as a separate output section containing the full SBOM verification results. This contradicts the assertion that the SBOM result should appear 'not as a separate section' — the output structure explicitly separates SBOM verification into its own file."

</details>

<details>
<summary>eval-15: 1 failing assertion</summary>

- **Assertion:** "Step 0 extracts the ProdSec Jira account ID from the Security Configuration as an optional field without raising an error (Step 0 config validation)"
  **Evidence:** "No Step 0 config validation output file exists in the outputs directory. The four output files are: affects-versions.md, data-extraction.md, remediation.md, and version-impact.md. None of them document Step 0 config extraction or reference extraction of a ProdSec Jira account ID from Security Configuration."

</details>

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "None of the four output files (data-extraction.md, embargo-check.md, version-impact.md, remediation.md) contain any content about Low or Moderate severity CVE handling, the gate being skipped, or behavior when CVSS &lt; 7.0. The eval run only covers a High severity (CVSS 7.5) scenario. There is no concrete evidence in the outputs demonstrating that the gate is silently skipped for sub-threshold severities."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Dependency chain context includes an SBOM verification line — either showing the cosign comparison result or noting that SBOM verification was skipped because cosign is not available (Step 2.3.5 Optional SBOM verification)"
  **Evidence:** "A search for 'sbom', 'SBOM', and 'cosign' across all four output files (data-extraction.md, version-impact.md, affects-versions.md, remediation.md) returned no matches. Neither an SBOM verification result nor a note that SBOM verification was skipped appears anywhere in the outputs."

</details>

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "Each listed issue shows: issue key, status, CVE ID (from labels), summary, and created date"
  **Evidence:** "In discovery-listing.md, Query 1 (Untriaged) and Query 2 (Triaged but still New) tables have columns '# | Issue | CVE | Summary | Created' — status is NOT a per-row column. Status appears only as section subheadings ('### Status: New', '### Status: In Progress') for Query 1, and is entirely absent as a per-row value in Query 2's table. Only Query 3's Ready for QA table includes a per-row 'Status' column."

</details>

**Pass rate:** 92% · **Tokens:** 50,919 · **Duration:** 111s

**Baseline** (`7142c02`): 98% · 41,725 tokens · 94s

