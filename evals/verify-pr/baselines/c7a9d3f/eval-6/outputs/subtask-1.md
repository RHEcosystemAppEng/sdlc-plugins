## Repository
sdlc-plugins

## Target Branch
main

## Description
Fix the Documentation Coverage verdict mapping in SKILL.md Step 6a. The current mapping references a "Style Quality *(new)*" report row that does not exist in Step 8's verification report table or verdict source mapping. The mapping must either add the "Style Quality" row to Step 8 or map Documentation Coverage into an existing report row (such as the combined "Test Quality" row or a new dedicated row), ensuring the orchestrator can correctly process and display the Documentation Coverage verdict.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` -- fix the Step 6a verdict mapping row for Documentation Coverage to reference a valid report row, and update Step 8's report table and verdict source mapping to include the corresponding row if a new row is intended

## Implementation Notes
- The current Step 6a mapping row reads: `| Style/Conventions | Documentation Coverage | Style Quality *(new)* |`
- Step 8's report table (lines 899-914) has no "Style Quality" row
- Step 8's verdict source mapping (lines 921-935) has no "Style Quality" entry
- Two valid approaches:
  1. **Add a new report row:** Add "Style Quality" to the Step 8 report table, add an entry to the verdict source mapping, and decide whether it is informational (like Test Quality and Test Change Classification) or affects the PASS/WARN/FAIL determination
  2. **Use existing row:** Map Documentation Coverage into the existing "Test Quality" combined row, following the pattern of Repetitive Test Detection, Test Documentation, and Eval Quality. This would require updating the Test Quality combination logic in Step 6a to include Documentation Coverage as a fourth input
- Either approach must ensure consistency between Step 6a mapping, Step 8 report table, and Step 8 verdict source mapping

## Review Context
The original review comment (reviewer-b, comment 50001) flagged the Markdown exclusion rule in Check 6 but did not identify this mapping defect. This defect was identified during verification by analyzing the consistency between Step 6a's mapping table and Step 8's report format.

The mapping row `| Style/Conventions | Documentation Coverage | Style Quality *(new)* |` was added in the PR diff for SKILL.md but the corresponding Step 8 changes were omitted, leaving the report format incomplete.

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] Step 6a verdict mapping for Documentation Coverage references a report row that exists in Step 8's report table
- [ ] Step 8's report table includes the target report row for Documentation Coverage
- [ ] Step 8's verdict source mapping includes an entry for the Documentation Coverage report row
- [ ] If a new report row is added, the Overall result rules clarify whether it is informational or affects PASS/WARN/FAIL determination
