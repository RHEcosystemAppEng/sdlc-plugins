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
| eval-30 | 4/4 | 0 | 100% |
| eval-31 | 4/4 | 0 | 100% |
| eval-32 | 4/4 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 8/8 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-14: 1 failing assertion</summary>

- **Assertion:** "The rpms.lock.yaml classification remains the primary signal — the SBOM result supplements but does not override it (Step 2.3.5 non-MVP enhancement)"
  **Evidence:** "When rpms.lock.yaml and SBOM disagree, the output changes the origin to 'DISPUTED (rpms.lock.yaml: explicit install / SBOM: base image)' rather than keeping the rpms.lock.yaml classification as primary. The DISPUTED status effectively dilutes the rpms.lock.yaml classification. The output does not explicitly state that rpms.lock.yaml is the primary signal. The remediation guidance says 'investigate discrepancy before proceeding' and presents both possibilities as equally valid ('If explicit install is confirmed... If base image origin is confirmed...'), treating them as co-equal rather than rpms.lock.yaml as primary."

</details>

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "No output file demonstrates or explicitly states that the gate is skipped for CVSS &lt; 7.0. The eval only tests a CVSS 7.5 scenario where the gate triggers. While the threshold table (line 17: 'Trigger threshold: CVSS &gt;= 7.0') implies the behavior, there is no concrete evidence of the gate being skipped silently for a sub-threshold CVE."

</details>

<details>
<summary>eval-20: 3 failing assertions</summary>

- **Assertion:** "Step 0.3 determines the matrix is within the 14-day threshold and proceeds without displaying a staleness warning"
  **Evidence:** "staleness-check.md lines 16-17: 'Age: 24 days... Status: STALE -- exceeds the 14-day threshold by 10 days'. The matrix is NOT within the 14-day threshold; it is 24 days old and classified as STALE. Lines 29-46 display staleness warnings for both streams. The output directly contradicts the assertion."

- **Assertion:** "No user prompt or options are presented for a fresh matrix — the check is silent on success"
  **Evidence:** "staleness-check.md lines 29-46 explicitly present staleness warnings with three user options (Refresh now, Proceed anyway, Stop) for both streams. The check is NOT silent; it displays prompts requiring user input. This contradicts the assertion that no prompts are presented."

- **Assertion:** "The triage continues to Step 0.5 and beyond without interruption from the staleness check"
  **Evidence:** "staleness-check.md lines 47-49: 'The engineer must choose an option before triage can proceed to Step 1.' The staleness check explicitly interrupts triage by requiring user input. While data-extraction.md exists (showing triage eventually continued), the staleness check did present an interruption. The assertion requires no interruption from the staleness check, but the check fired and blocked progress pending user response."

</details>

**Pass rate:** 96% · **Tokens:** 56,144 · **Duration:** 107s

**Baseline** (`1dab64e0`): 99% · 58,180 tokens · 124s

