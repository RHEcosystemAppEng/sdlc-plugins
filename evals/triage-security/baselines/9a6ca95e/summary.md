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
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 6/6 | 0 | 100% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 8/8 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-17: 1 failing assertion</summary>

- **Assertion:** "The embargo warning gate does NOT trigger for Low or Moderate severity CVEs (CVSS &lt; 7.0) — it is skipped silently when severity is below threshold (§1.70)"
  **Evidence:** "The outputs only demonstrate the case where CVSS &gt;= 7.0 triggers the gate (CVE-2026-31812 with CVSS 7.5). While embargo-check.md establishes the threshold ('Trigger Threshold | Critical or Important (CVSS &gt;= 7.0)'), there is no explicit evidence about what happens when the threshold is NOT met. No output file states that the gate is 'skipped silently' for CVSS &lt; 7.0, and there is no demonstration or specification of the below-threshold behavior. The burden of proof is on PASS and no concrete evidence of silent skipping for low/moderate CVEs exists in the outputs."

</details>

**Pass rate:** 99% · **Tokens:** 53,857 · **Duration:** 136s

**Baseline** (`fcbfa091`): 100% · 44,507 tokens · 106s

