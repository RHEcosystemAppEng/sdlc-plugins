## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/10 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-15 | 4/5 | 1 | 80% |
| eval-2 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 5/5 | 0 | 100% |
| eval-6 | 5/5 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 5/5 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-15: 1 failing assertion</summary>

- **Assertion:** "Step 0 extracts the ProdSec Jira account ID from the Security Configuration as an optional field without raising an error (Step 0 config validation)"
  **Evidence:** "No Step 0 output file exists in the outputs directory. The available files are: data-extraction.md (Step 1), version-impact.md (Step 2), affects-versions.md (Step 3), and remediation.md (Step 7). There is no explicit evidence of a Step 0 config validation that extracts the ProdSec Jira account ID as an optional field from Security Configuration."

</details>

**Pass rate:** 99% · **Tokens:** 42,421 · **Duration:** 94s

**Baseline** (`14692f2`): 100% · 43,037 tokens · 87s

