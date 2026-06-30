## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/10 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-14 | 5/5 | 0 | 100% |
| eval-15 | 5/5 | 0 | 100% |
| eval-16 | 7/7 | 0 | 100% |
| eval-17 | 5/5 | 0 | 100% |
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
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Dependency chain context includes an SBOM verification line — either showing the cosign comparison result or noting that SBOM verification was skipped because cosign is not available (Step 2.3.5 Optional SBOM verification)"
  **Evidence:** "version-impact.md section 2.3.5 (Dependency Chain Context) contains only: rpms.lock.yaml presence check, origin classification (explicit install), remediation guidance, and a note about the package being directly managed. There is no mention of SBOM, cosign, SBOM verification, or any statement that SBOM verification was skipped. The section completely omits the optional SBOM verification step."

</details>

**Pass rate:** 99% · **Tokens:** 56,582 · **Duration:** 119s

**Baseline** (`7142c02`): 98% · 41,725 tokens · 94s

