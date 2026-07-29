## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/11 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 4/5 | 1 | 80% |
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
| eval-29 | 4/5 | 1 | 80% |
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
<summary>eval-13: 1 failing assertion</summary>

- **Assertion:** "The remediation output sequences digest comments BEFORE issue links (Depend, Blocks) or other comments in the described procedure for each task (§1.66, shared/description-digest-protocol.md Rules)"
  **Evidence:** "Contradictory evidence: The document's section layout for all four tasks consistently places the 'Linkage' section (showing create_link calls with Depend/Blocks/Related) BEFORE the 'Description Digest Comment' section. For example, Task 1 has Linkage at lines 82-88 and Digest at lines 90-107; Task 2 has Linkage at lines 167-181 and Digest at lines 183-198. While the text within each digest section says 'before creating issue links or other comments' (e.g., line 103) and the summary reiterates this at line 449, the structural ordering of the procedure contradicts this instruction. Per grading rules, contradictory evidence means FAIL."

</details>

<details>
<summary>eval-14: 1 failing assertion</summary>

- **Assertion:** "The rpms.lock.yaml classification remains the primary signal — the SBOM result supplements but does not override it (Step 2.3.5 non-MVP enhancement)"
  **Evidence:** "The dependency chain output labels the origin as 'DISPUTED (explicit install per rpms.lock.yaml; base image per SBOM)' rather than preserving the rpms.lock.yaml classification as the primary signal. The SBOM Disagreement Summary section states 'Manual investigation is required to determine the correct remediation approach before creating remediation tasks', effectively halting the workflow pending manual review. This means the SBOM result has overridden the rpms.lock.yaml classification by changing the origin from 'explicit install' to 'DISPUTED', rather than supplementing it. If rpms.lock.yaml were truly the primary signal, the origin would remain 'explicit install' with the SBOM disagreement noted as supplementary context."

</details>

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "No output file contains evidence about behavior for CVEs with CVSS &lt; 7.0. The embargo-check.md only covers the current case (CVSS 7.5, which meets the threshold). While the threshold table implies CVSS &gt;= 7.0 is the trigger condition, there is no explicit statement or demonstration that the gate is skipped silently for Low or Moderate severity CVEs. The burden of proof is on PASS and no concrete evidence exists for below-threshold behavior."

</details>

<details>
<summary>eval-20: 3 failing assertions</summary>

- **Assertion:** "Step 0.3 determines the matrix is within the 14-day threshold and proceeds without displaying a staleness warning"
  **Evidence:** "staleness-check.md shows the matrix was found to be 31 days old, exceeding the 14-day threshold. Line 25 states 'Result: STALE' and lines 27-28 warn 'The matrix may not reflect recent releases.' A staleness warning with three options was displayed (lines 33-41)."

- **Assertion:** "No user prompt or options are presented for a fresh matrix — the check is silent on success"
  **Evidence:** "The matrix was determined to be stale (not fresh), and staleness-check.md lines 33-41 explicitly present a user prompt with three options: 'Refresh now', 'Proceed anyway', and 'Stop'. The check was not silent."

- **Assertion:** "The triage continues to Step 0.5 and beyond without interruption from the staleness check"
  **Evidence:** "staleness-check.md line 41 explicitly states: 'The engineer must choose an option before triage proceeds past this step.' The staleness check interrupted the triage flow by requiring user input before continuing."

</details>

<details>
<summary>eval-29: 1 failing assertion</summary>

- **Assertion:** "The validation result is Pass — no warnings, no auto-repairs, no user prompt — triage proceeds silently to aggregation"
  **Evidence:** "The overall validation result is PASS with no auto-repairs. However, the output is NOT silent. It includes a staleness warning: 'Staleness note: Both streams share a Last-Updated timestamp of 2026-06-28T10:00:00Z, which is 31 days old and exceeds the 14-day staleness threshold. Per Step 0.3, the user would be prompted to choose: refresh now, proceed anyway, or stop.' This staleness concern explicitly mentions prompting the user, which contradicts the assertion's requirement of 'no warnings, no user prompt'. Furthermore, each stream result notes the timestamps are 'STALE, exceeds 14-day threshold', which constitutes a warning. The assertion requires a fully silent pass with no warnings and no user prompt."

</details>

**Pass rate:** 95% · **Tokens:** 51,651 · **Duration:** 114s

**Baseline** (`7aaa377a`): 99% · 84,117 tokens · 131s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.7*

