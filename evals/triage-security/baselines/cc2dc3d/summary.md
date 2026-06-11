## Eval Results: triage-security

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 10/10 | 0 | 100% |
| eval-2 | 5/5 | 0 | 100% |
| eval-3 | 5/5 | 0 | 100% |
| eval-4 | 4/5 | 1 | 80% |
| eval-5 | 5/5 | 0 | 100% |

### Failed Assertions

<details>
<summary>eval-4: 1 failing assertion</summary>

- **Assertion:** "Cross-stream impact notice is NOT generated because the issue is unscoped — it covers all streams by definition (Step 7 Case B applies only to scoped issues)"
  **Evidence:** "remediation.md correctly does NOT generate a cross-stream impact notice. However, the reason given is 'No cross-stream impact notice (Case B) is needed because the other stream is already fixed' -- not because the issue is unscoped. The assertion requires the rationale to be that Case B applies only to scoped issues and this issue is unscoped, but the output gives a different justification (the other stream being already fixed). While the behavioral outcome is correct (no notice generated), the reasoning does not match the assertion's required logic."

</details>

**Pass rate:** 96% · **Tokens:** 42,161 · **Duration:** 106s

**Baseline** (`750b4ac`): 100% · 37,926 tokens · 85s

