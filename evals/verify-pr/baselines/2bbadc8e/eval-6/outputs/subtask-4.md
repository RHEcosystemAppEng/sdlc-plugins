# Sub-task: Root-cause — improve convention upgrade flow traceability in plan-feature

**Issue Type:** Task
**Labels:** ai-generated-jira, root-cause

---

## Repository
sdlc-plugins

## Description
Root-cause investigation from TC-9106 verification identified a gap in how the plan-feature phase specifies pipeline flow coverage. The eval-3 assertion failures about convention upgrade eligibility suggest that the task description for TC-9106 (plan-feature output) did not explicitly call out that the convention upgrade evaluation must be triggered and documented for all suggestion-classified comments. While the implementation notes reference "follow the structure of existing Checks 1-5," they do not explicitly require verifying that the convention upgrade pipeline (Check 1 in style-conventions.md) processes the new check's feedback.

## Files to Modify
- Analysis of plan-feature skill patterns to identify whether acceptance criteria should explicitly require pipeline integration testing

## Implementation Notes
- The eval-3 failures indicate that the convention upgrade evaluation was not connected to the new Check 6 output
- The task acceptance criteria covered Check 6 verdicts and output format but not the integration with the existing convention upgrade pipeline
- This is a plan-feature gap: when adding a new check to an existing sub-agent, the task should include criteria verifying integration with existing pipelines (e.g., convention upgrade, test quality combination)

## Acceptance Criteria
- [ ] Identify whether plan-feature should generate acceptance criteria for pipeline integration when new checks are added to existing sub-agents
- [ ] Recommend improvements to plan-feature task generation for sub-agent check additions
