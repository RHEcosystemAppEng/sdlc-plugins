## Eval Results: triage-bug

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 8/9 | 1 | 89% |
| eval-2 | 4/4 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Bug validation confirms the issue type ID (10020) matches the Bug issue type ID from Bug Configuration (Step 1)"
  **Evidence:** "bug-parsing.md lists 'Issue Type: Bug (ID: 10020)' in the Metadata section. However, there is no explicit validation statement confirming that this ID matches or mismatches the Bug Configuration's Bug issue type ID. The CLAUDE.md Bug Configuration specifies Bug issue type ID as 10016, not 10020. The output does not flag this mismatch — it simply records 10020 without comparing it. The assertion requires the output to confirm the ID matches, but 10020 != 10016 (the configured value), and the output does not perform or document any such validation check."

</details>

**Pass rate:** 96% · **Tokens:** 34,208 · **Duration:** 72s

**Baseline** (`1dfe8af`): 100% · 29,402 tokens · 84s

