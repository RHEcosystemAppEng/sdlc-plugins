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
  **Evidence:** "review-50001.md does classify the comment as a normal 'Code Change Request' from 'reviewer-b (human reviewer)' and correctly states it is 'NOT an eval result'. However, lines 27-29 of review-50001.md include an 'Eval Result Detection' section that explicitly references eval detection criteria: 'This comment is from reviewer-b (a human reviewer), NOT from github-actions[bot]. It does not contain "## Eval Results" and does not contain "sdlc-workflow/run-evals". It fails all three conditions of the eval result detection heuristic and is therefore correctly processed as a normal review comment.' The assertion states the classification 'does not reference eval detection or eval metrics.' The classification file does reference eval detection (the heuristic criteria), though it does not reference eval metrics. Reading the assertion more carefully: 'its classification does not reference eval detection or eval metrics' -- the review-50001.md file explicitly has an 'Eval Result Detection' section discussing eval detection criteria, which contradicts the assertion that the classification does not reference eval detection."

</details>

**Pass rate:** 98% · **Tokens:** 63,377 · **Duration:** 175s

**Baseline** (`91c3899`): 98% · 71,339 tokens · 241s

