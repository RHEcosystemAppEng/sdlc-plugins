# Criterion 7 — Step 6a verdict mapping includes Documentation Coverage

**Verdict: FAIL**

## What the PR implements
The single SKILL.md change:
```
@@ -354,6 +354,7 @@ Add a new mapping row:
 | Style/Conventions | Repetitive Test Detection | Test Quality *(combined)* |
 | Style/Conventions | Test Documentation        | Test Quality *(combined)* |
 | Style/Conventions | Eval Quality              | Test Quality *(combined)* |
+| Style/Conventions | Documentation Coverage    | Style Quality *(new)*     |
 ```
```

## Reasoning
1. **Wrong location.**
   - The hunk context is "Add a new mapping row:", and the added row is followed straight away by a closing code fence. So the row sits inside a fenced example block, not in the live Step 6a table.
   - In SKILL.md, the real Step 6a table (base lines ~574–587) is an unfenced table inside numbered item 1. After its `Eval Quality` row comes `| Style/Conventions | Test Change Classification | ... |`, not a fence.
   - The text "Add a new mapping row" does not appear anywhere in base SKILL.md.
   - Result: the orchestrator's actual mapping table never gets a Documentation Coverage entry.
2. **The target report row does not exist.**
   - The row maps to `Style Quality *(new)*`. Neither the Step 8 report table nor the "Verdict source mapping" table has a Style Quality row, and the PR changes neither.
   - Even if the orchestrator read this row, the Documentation Coverage verdict would never show up in the report.
3. **Not "combined" as the task asks.**
   - Files to Modify says to add Documentation Coverage "in the combined Style/Conventions verdict".
   - The PR adds no combination rule: the Test Quality rule still lists three checks. It also does not say whether the new row is informational, the way the Overall-result note does for the other rows.

The PR adds a line that mentions Documentation Coverage, but the Step 6a mapping does not actually include it, and the verdict cannot reach the report.

## Evidence
- PR diff, `SKILL.md` hunk `@@ -354,6 +354,7 @@`.
- Base `plugins/sdlc-workflow/skills/verify-pr/SKILL.md`: Step 6a table (~574–587), Test Quality combination rule (~589–596), Step 8 report table (~1121–1135), verdict source mapping (~1144–1156).

## Follow-up
Sub-task 4 (wire Documentation Coverage into the live Step 6a table and define its report row).
