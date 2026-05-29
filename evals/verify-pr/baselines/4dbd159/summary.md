## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 10/11 | 1 | 91% |
| eval-3 | 15/15 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — the 3-criteria detection (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) found no matches, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "report.md line 15: '| Eval Quality | N/A | No eval result reviews exist in the PR |'. The Eval Quality row is N/A and the reason matches ('No eval result reviews exist in the PR'). However, the report does not mention the specific 3-criteria detection mechanism (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals). There is no evidence that these three specific detection criteria were used or referenced anywhere in the output files."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Eval Quality is N/A because no eval result reviews exist in the PR — the 3-criteria detection (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals) found no matches, so Eval Quality does not affect the Test Quality combination"
  **Evidence:** "report.md line 13: 'Test Quality | PASS | No repetitive test functions detected (Meszaros heuristic: each test exercises distinct behavior). All test functions have doc comments. Eval Quality: N/A (no eval result reviews).' The report states Eval Quality is N/A with the reason 'no eval result reviews', but it does NOT mention the specific 3-criteria detection mechanism (author github-actions[bot], marker ## Eval Results, footer sdlc-workflow/run-evals). The assertion requires that the 3-criteria detection is referenced — the report only says 'no eval result reviews' without specifying the detection criteria used."

</details>

**Pass rate:** 96% · **Tokens:** 36,927 · **Duration:** 169s

**Baseline** (`d3d6601`): 96% · 57,413 tokens · 185s

