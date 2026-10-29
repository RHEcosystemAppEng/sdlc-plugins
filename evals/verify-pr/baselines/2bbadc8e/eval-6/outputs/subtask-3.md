# Sub-task: Root-cause — improve convention upgrade pipeline coverage in implement-task

**Issue Type:** Task
**Labels:** ai-generated-jira, root-cause

---

## Repository
sdlc-plugins

## Description
Root-cause investigation from TC-9106 verification identified a method-based skill gap in the implement-task phase. The implementation of the verify-pr skill's convention upgrade pipeline did not ensure that all suggestions flow through convention upgrade evaluation. The eval-3 assertion failures reveal that the suggestion-to-code-change-request upgrade path is not reliably triggered for all suggestion-classified comments.

The fix should improve the implement-task skill's code analysis to ensure that when a skill defines a pipeline with explicit flow requirements (e.g., "every suggestion must go through convention upgrade evaluation"), the implementation covers all branches of that flow — not just the common case.

## Files to Modify
- Analysis of implement-task skill patterns to identify why the convention upgrade pipeline branch was missed during implementation

## Implementation Notes
- This is a universal knowledge gap (method-based): the principle "verify all defined pipeline branches are implemented" applies to any repository
- The defect was in the implement-task phase — the task description correctly specified convention upgrade evaluation, but the implementation did not trigger it for all suggestion-classified comments
- Root-cause analysis: reviewer flagged missing convention upgrade evaluation in eval-3 → plan-feature phase correctly described the pipeline → implement-task missed the branch coverage

## Acceptance Criteria
- [ ] Identify the implement-task pattern that should catch missing pipeline branch coverage
- [ ] Document or improve the implement-task skill to verify that all defined pipeline branches are implemented
