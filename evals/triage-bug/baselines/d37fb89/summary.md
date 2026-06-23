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
  **Evidence:** "bug-parsing.md lists 'Issue Type: Bug (ID: 10020)' in the Metadata section (line 7), which matches the Bug Configuration's 'Bug issue type ID: 10020' from claude-md-bug-config.md. However, bug-parsing.md does not contain any explicit validation statement confirming or comparing that the issue type ID matches the Bug Configuration. The ID is listed but no validation step is documented."

</details>

**Pass rate:** 96% · **Tokens:** 27,747 · **Duration:** 67s

**Baseline** (`41f6a7e`): 100% · 31,308 tokens · 74s

