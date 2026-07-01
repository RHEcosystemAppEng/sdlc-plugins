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

- **Assertion:** "Root-cause investigation runs on the created eval failure sub-tasks — the report includes a Root-Cause Investigation verdict that is not N/A, indicating the investigation pipeline processed the eval failure sub-tasks"
  **Evidence:** "Report line 6: '| Root-Cause Investigation | SKIPPED | Sub-tasks were created for eval failures; root-cause investigation not applicable to eval-driven sub-tasks |'. The verdict is SKIPPED, not N/A, but the assertion requires that 'the investigation pipeline processed the eval failure sub-tasks.' The SKIPPED verdict with the explanation 'root-cause investigation not applicable to eval-driven sub-tasks' indicates the pipeline explicitly did NOT run the investigation on the eval failure sub-tasks. The assertion requires the pipeline to have actually processed them, which did not happen."

</details>

**Pass rate:** 98% · **Tokens:** 32,355 · **Duration:** 144s

**Baseline** (`1f575ac4`): 100% · 69,734 tokens · 228s

