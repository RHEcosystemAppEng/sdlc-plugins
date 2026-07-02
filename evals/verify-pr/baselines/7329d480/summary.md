## Eval Results: verify-pr

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/12 | 0 | 100% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 14/14 | 0 | 100% |
| eval-4 | 10/10 | 0 | 100% |
| eval-5 | 10/10 | 0 | 100% |
| eval-6 | 9/10 | 1 | 90% |

### Failed Assertions

<details>
<summary>eval-6: 1 failing assertion</summary>

- **Assertion:** "The human reviewer comment from reviewer-b (comment id 50001) is NOT misidentified as an eval result — it is processed as a normal review comment (classified in review-50001.md) and its classification does not reference eval detection or eval metrics"
  **Evidence:** "review-50001.md correctly classifies comment 50001 as 'CODE CHANGE REQUEST' (line 17) and processes it through the normal review classification pipeline. The comment is NOT misidentified as an eval result. However, lines 23-24 of review-50001.md explicitly reference eval detection criteria: 'This is a human reviewer comment, not an eval result. The review (id 40002) is from user "reviewer-b" (a human user), not from github-actions[bot], and does not contain the `## Eval Results` marker or `sdlc-workflow/run-evals` footer.' The classification output references eval detection heuristic criteria (github-actions[bot], ## Eval Results marker, sdlc-workflow/run-evals footer), contradicting the assertion that 'its classification does not reference eval detection or eval metrics.'"

</details>

**Pass rate:** 98% · **Tokens:** 0 · **Duration:** 0s

**Baseline** (`be2d4411`): 100% · 38,430 tokens · 181s

