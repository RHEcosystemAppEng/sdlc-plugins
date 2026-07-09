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
  **Evidence:** "review-50001.md correctly classifies the comment as 'code change request' and processes it through the normal review classification pipeline. However, the classification DOES reference eval detection: reasoning point 5 is explicitly titled 'Not an eval result' and discusses eval detection criteria ('This comment is from a human reviewer (reviewer-b, user ID 10002), not from github-actions[bot]. It does not contain "## Eval Results" or "sdlc-workflow/run-evals".') The assertion requires the classification does NOT reference eval detection or eval metrics, but the classification explicitly references eval detection criteria to rule them out."

</details>

**Pass rate:** 98% · **Tokens:** 65,110 · **Duration:** 231s

**Baseline** (`6051c055`): 100% · 135,404 tokens · 421s

