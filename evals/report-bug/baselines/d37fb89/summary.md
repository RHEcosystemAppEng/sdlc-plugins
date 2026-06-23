## Eval Results: report-bug

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/13 | 1 | 92.3% |
| eval-2 | 8/9 | 1 | 88.9% |
| eval-3 | 6/6 | 0 | 100% |
| eval-4 | 12/12 | 0 | 100% |
| eval-5 | 7/7 | 0 | 100% |

**Pass rate:** 96% · **Tokens:** 20,267 · **Duration:** 44s

**Baseline** (`4073ac0`): 100% · 24,038 tokens · 49s

### Regressions

**eval-1** (Interactive complete) — 1 failure:
- `outputs/jira-create.md includes the label 'ai-generated-jira'` — **FAILED**: used label `bug` instead of `ai-generated-jira`

**eval-2** (Interactive partial) — 1 failure:
- `outputs/jira-create.md includes the label 'ai-generated-jira'` — **FAILED**: used label `bug` instead of `ai-generated-jira`

### Analysis

The same assertion failed in eval-1 and eval-2: the agent used the label `bug` instead of the required `ai-generated-jira` label. The SKILL.md (Step 4 and Step 5) clearly specifies `ai-generated-jira` as the label to apply. Eval-4 and eval-5 correctly used `ai-generated-jira`, suggesting the failure is non-deterministic — the agent sometimes defaults to a generic "bug" label instead of reading the exact label from the skill specification.

All other assertions passed, including all security/adversarial tests (eval-5), programmatic mode parsing (eval-4), missing config detection (eval-3), and optional section omission (eval-2).

Token usage decreased 16% vs baseline (20,267 vs 24,038). Duration decreased 10% (44s vs 49s).
