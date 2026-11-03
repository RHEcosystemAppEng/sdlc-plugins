# Criterion 7: Step 6a verdict mapping includes Documentation Coverage

**Verdict: PASS (with advisory)**

## Evidence

In `plugins/sdlc-workflow/skills/verify-pr/SKILL.md`:

```diff
 | Style/Conventions | Eval Quality              | Test Quality *(combined)* |
+| Style/Conventions | Documentation Coverage    | Style Quality *(new)*     |
```

## Reasoning

The Step 6a sub-agent-to-report-row mapping now has a `Style/Conventions | Documentation Coverage` row. The criterion asks only that the mapping include Documentation Coverage, so it is met.

## Advisory (does not change the verdict, but needs follow-up)

The task's Files to Modify entry says the SKILL.md change should "include Documentation Coverage in the combined Style/Conventions verdict". The new row instead maps to a new report row, `Style Quality *(new)*`, that nothing else defines:

- The Step 8 report template has no `Style Quality` row.
- The Step 8 "Verdict source mapping" table has no `Style Quality` entry.
- The Test Quality combination rule in Step 6a, which combines Repetitive Test Detection, Test Documentation and Eval Quality, is unchanged and does not include Documentation Coverage.

As a result, the orchestrator has nowhere to show the Documentation Coverage verdict, and it would likely be dropped from the final report. No reviewer flagged this, so verify-pr creates no sub-task for it (sub-tasks come only from review, CI or eval feedback). It is raised in the report summary for the human reviewer. Two possible fixes: add `Style Quality` to the Step 8 template and source mapping, or fold Documentation Coverage into the combined Test Quality rule.
