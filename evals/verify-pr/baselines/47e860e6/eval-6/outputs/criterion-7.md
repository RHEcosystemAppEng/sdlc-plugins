# Criterion 7: Step 6a verdict mapping includes Documentation Coverage

**Verdict: FAIL**

## What the task requires
- Acceptance Criteria: "Step 6a verdict mapping includes Documentation Coverage"
- Files to Modify: "`plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — update Step 6a verdict mapping to include Documentation Coverage **in the combined Style/Conventions verdict**"

## What the PR does
The PR makes one change to `SKILL.md` (hunk `@@ -354,6 +354,7 @@ Add a new mapping row:`):

```
+| Style/Conventions | Documentation Coverage    | Style Quality *(new)*     |
```

## Why this fails
1. **The target report row does not exist.** The row maps Documentation Coverage to a report row called `Style Quality *(new)*`. The PR does not add that row to the Step 8 report template table (`| Check | Result | Details |`). It also does not add it to the Step 8 "Verdict source mapping" table, and it defines no combination rule for it. Every other Style/Conventions mapping goes to an existing report row (Test Quality *(combined)*, Test Change Classification) or to Step 6b processing. As written, the Documentation Coverage verdict is mapped to a destination the orchestrator never renders, so it would be dropped from the final report.
2. **It is not part of the combined verdict, which the task asked for.** The task says Documentation Coverage must go "in the combined Style/Conventions verdict". The existing combined row is **Test Quality**, and its combination rule in Step 6a ("If any of the three is WARN → Test Quality is WARN…") names exactly three inputs: Repetitive Test Detection, Test Documentation and Eval Quality. The PR leaves that rule unchanged and does not create a new combined row with its own rule. Documentation Coverage therefore feeds no combined verdict.
3. **The edit location is questionable.** The hunk is around line 354 and sits inside a fenced code block introduced by "Add a new mapping row:". In the current `SKILL.md`, the Step 6a mapping table is a plain Markdown table under `### Step 6a – Collect Sub-Agent Results` (around line 574), not a fenced snippet near line 354. From the diff alone I cannot confirm that the live Step 6a table was edited, as opposed to an example block.

A mapping row naming Documentation Coverage exists, but it does not wire the check into any verdict that appears in the report. The intent of the criterion, as stated in Files to Modify, is not met.

## What a fix needs
Either (a) map Documentation Coverage to `Test Quality *(combined)*` and extend the Test Quality combination rule to four inputs, or (b) add a new `Style Quality` row to the Step 8 report template and the Verdict source mapping, with its own combination and Overall-impact rule. In both cases, edit the actual Step 6a table.

## Related review comments
None. No reviewer raised this gap, so no review-feedback sub-task covers it. It is reported in the verification report for the PR author and the human reviewer.
