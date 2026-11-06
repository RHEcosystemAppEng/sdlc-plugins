# Criterion 7 — Step 6a verdict mapping includes Documentation Coverage

**Verdict: NOT MET (FAIL)**

## Evidence (from the PR diff, `plugins/sdlc-workflow/skills/verify-pr/SKILL.md`)

```diff
@@ -354,6 +354,7 @@ Add a new mapping row:
 | Style/Conventions | Repetitive Test Detection | Test Quality *(combined)* |
 | Style/Conventions | Test Documentation        | Test Quality *(combined)* |
 | Style/Conventions | Eval Quality              | Test Quality *(combined)* |
+| Style/Conventions | Documentation Coverage    | Style Quality *(new)*     |
 ```
```

## Task requirement

- Acceptance Criterion: "Step 6a verdict mapping includes Documentation Coverage"
- Files to Modify: "`SKILL.md` — update Step 6a verdict mapping to include Documentation Coverage **in the combined Style/Conventions verdict**"

## Reasoning

A row naming `Documentation Coverage` was added, so a literal reading of the criterion is satisfied. The change still does not do what the task asked, and the verdict would never appear in the report:

1. **It maps to a report row that does not exist.** The new mapping points to `Style Quality *(new)*`. No such row appears anywhere in SKILL.md. The diff does not touch the Step 8 report template (whose rows are Review Feedback, Root-Cause Investigation, Scope Containment, Diff Size, Commit Traceability, Sensitive Patterns, CI Status, Acceptance Criteria, Test Quality, Test Change Classification, Verification Commands) or the "Verdict source mapping" table. The orchestrator would collect a Documentation Coverage verdict and then have no row to put it in, so it would be silently dropped.
2. **It is not part of the combined verdict.** The task says Documentation Coverage should feed "the combined Style/Conventions verdict". The only combined Style/Conventions row is `Test Quality *(combined)*`, and its combination rules (any WARN → WARN; all non-N/A PASS → PASS; all N/A → N/A) list only Repetitive Test Detection, Test Documentation and Eval Quality. The PR neither adds Documentation Coverage to those rules nor defines rules for a new combined row.
3. **The `*(new)*` annotation is unclear.** Every other mapping row names an existing report row, sometimes with a note such as *(combined)* or *(processed in Step 6b)*. "Style Quality *(new)*" reads like a placeholder, not a finished mapping. The hunk's context line ("Add a new mapping row:") followed by a closing code fence also suggests the row may sit in an instructional or example block instead of the live Step 6a table. That needs to be checked against the full file.

Because the mapping is incomplete (no report row, no combination rule, Step 8 not updated), the end-to-end behavior the criterion stands for, Documentation Coverage showing up in the verify-pr result, is missing. This criterion is marked **not met**.

## What a fix requires

- Either map Documentation Coverage to `Test Quality *(combined)*` and extend the combination rules, or add a new report row (for example `Documentation Coverage` or `Style Quality`) to the Step 8 template and the Verdict source mapping, with combination or informational rules stated explicitly.
- Confirm the row is in the real Step 6a mapping table, not a fenced example block.
- Update the Step 6a "Extract verdicts" explanation to match.
