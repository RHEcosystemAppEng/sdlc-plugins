## Eval Results: triage-bug

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 8/9 | 1 | 89% |
| eval-2 | 4/4 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 6/6 | 0 | 100% |
| eval-5 | 4/4 | 0 | 100% |
| eval-6 | 4/4 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Bug validation confirms the issue type ID (10020) matches the Bug issue type ID from Bug Configuration (Step 1)"
  **Evidence:** "bug-parsing.md records 'Issue Type: Bug (ID: 10020)' on line 8, but the Validation Result section (lines 69-77) only flags the missing 'Environment / Version' section. There is no explicit validation or confirmation that the issue type ID 10020 matches the Bug issue type ID from Bug Configuration. The output does not compare 10020 against any configured Bug issue type ID value."

</details>

**Pass rate:** 98% · **Tokens:** 31,681 · **Duration:** 111s

**Baseline** (`3337d1fd`): 100% · 32,974 tokens · 101s

