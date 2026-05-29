## Eval Results: setup

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 7/7 | 0 | 100% |
| eval-2 | 6/6 | 0 | 100% |
| eval-3 | 5/6 | 1 | 83% |
| eval-4 | 6/6 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "outputs/claude-md-result.md contains a '## Repository Registry' section with the table headers (Repository, Role, Serena Instance, Path) but no data rows, or explicitly notes that no repositories are configured"
  **Evidence:** "The file contains the ## Repository Registry section with correct table headers (Repository, Role, Serena Instance, Path), but it includes a data row: '| my-project | Web application | — | ./ |' (line 24). The assertion requires either no data rows OR an explicit note that no repositories are configured. Neither condition is met — there is a populated data row and no such note."

</details>

**Pass rate:** 96% · **Tokens:** 22,307 · **Duration:** 58s

**Baseline** (`d3d6601`): 100% · 17,000 tokens · 36s

