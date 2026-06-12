## Repository
sdlc-plugins

## Target Branch
main

## Description
The Documentation Coverage check was added to the Step 6a verdict mapping table in SKILL.md, mapping to "Style Quality *(new)*". However, no corresponding "Style Quality" row was added to the Step 8 report template or the verdict source mapping table. This means the Documentation Coverage verdict is collected by the orchestrator but never appears in the final verification report.

Either add a "Style Quality" row to the Step 8 report template and verdict source mapping, or reconsider the mapping to integrate Documentation Coverage into an existing report row.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` — add a "Style Quality" row to the Step 8 report template table and to the verdict source mapping table, or remap Documentation Coverage to an existing report row

## Implementation Notes
- The Step 8 report template (around line 891-911) defines the verification report table with rows like Review Feedback, Scope Containment, CI Status, etc. A new "Style Quality" row needs to be added here with its verdict options (PASS/WARN/N/A)
- The verdict source mapping table (around line 914-927) maps each report row to its source sub-agent. A new entry for Style Quality should reference the Style/Conventions sub-agent (Documentation Coverage check)
- Consider whether Style Quality should follow the same informational-only pattern as Test Quality and Test Change Classification (excluded from Overall result determination), or whether it should affect the Overall result
- The overall result rules (PASS/WARN/FAIL determination) may need updating if Style Quality is to be included in the determination
- Alternative approach: instead of creating a new report row, Documentation Coverage could be combined into the existing "Test Quality" row (renamed to something broader like "Code Quality") — but this would be a larger change affecting the combination logic

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Acceptance Criteria
- [ ] The Step 8 report template includes a row for Documentation Coverage verdict
- [ ] The verdict source mapping table includes an entry mapping the new row to the Style/Conventions sub-agent
- [ ] The Documentation Coverage verdict is visible in the final verification report output
- [ ] The overall result rules document whether the new row is informational or affects the Overall result
