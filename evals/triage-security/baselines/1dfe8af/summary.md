## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/10 | 0 | 100% |
| eval-10 | 5/5 | 0 | 100% |
| eval-11 | 5/5 | 0 | 100% |
| eval-12 | 5/5 | 0 | 100% |
| eval-13 | 5/5 | 0 | 100% |
| eval-15 | 4/5 | 1 | 80% |
| eval-16 | 7/7 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 5/5 | 0 | 100% |
| eval-5 | 5/5 | 0 | 100% |
| eval-6 | 6/6 | 0 | 100% |
| eval-7 | 5/5 | 0 | 100% |
| eval-8 | 5/5 | 0 | 100% |
| eval-9 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-15: 1 failing assertion</summary>

- **Assertion:** "Step 0 extracts the ProdSec Jira account ID from the Security Configuration as an optional field without raising an error (Step 0 config validation)"
  **Evidence:** "No Step 0 output file exists in the outputs directory. The four output files are: data-extraction.md (Step 1), version-impact.md (Step 2), affects-versions.md (Step 3), and remediation.md (Step 7). No file contains any reference to 'Step 0', 'config validation', 'Security Configuration', or extraction of the ProdSec account ID as an optional field. While the ProdSec account ID is used in Step 3, there is no evidence of a Step 0 explicitly extracting it from configuration."

</details>

**Pass rate:** 99% · **Tokens:** 42,610 · **Duration:** 91s

**Baseline** (`14692f2`): 100% · 43,037 tokens · 87s

