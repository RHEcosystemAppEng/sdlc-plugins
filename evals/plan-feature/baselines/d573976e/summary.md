## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/16 | 5 | 69% |
| eval-2 | 8/14 | 6 | 57% |
| eval-3 | 10/15 | 5 | 67% |
| eval-4 | 6/11 | 5 | 55% |
| eval-5 | 8/15 | 7 | 53% |
| eval-6 | 5/14 | 9 | 36% |

### Failed Assertions

<details>
<summary>eval-1: 5 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output files contain any SHA-256 digest comments. The outputs directory contains only impact-map.md and 5 task files. None of these files contain the string 'sha256-md:', 'sha256-adf:', '[sdlc-workflow] Description digest:', or any 64-character hex string. There is no evidence that description digest comments were posted after task creation."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the 5 task files contain any convention applicability rationales in the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. No task's Implementation Notes contain references to 'Per CONVENTIONS.md §' or the 'Applies:' rationale format. The convention-aware enrichment process is entirely absent from the outputs."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature issue (feature-standard.md) has 'Priority: Major'. However, none of the 5 task files contain an 'additional_fields' section or any mention of 'priority: Major' being inherited. The task files contain no mechanism for propagating the priority field to created Jira tasks."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature issue has 'Fix Versions: RHTPA 1.5.0' and CLAUDE.md has no '### Jira Field Defaults' section (so fixVersion scope defaults to 'both'). However, none of the 5 task files contain an 'additional_fields' section or any reference to 'fixVersions' or 'RHTPA 1.5.0'. The fixVersions field was not propagated to tasks."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No summary comment file exists in the outputs directory. The outputs contain only impact-map.md and 5 task files. There is no file representing a summary comment posted to the feature issue, and no file mentions the inherited priority ('Major') or fixVersion ('RHTPA 1.5.0') propagation status."

</details>

<details>
<summary>eval-2: 6 failing assertions</summary>

- **Assertion:** "Tasks document assumptions where they fill in missing details, labeled as assumptions pending clarification"
  **Evidence:** "While the impact-map.md documents ambiguities and 'Planning assumptions' in its table, these are labeled as 'Planning assumption' not 'assumptions pending clarification'. The individual task descriptions do not contain any sections or labels marking assumptions as pending clarification. The impact map says 'In a real engagement, these would be raised with the product owner before proceeding' but does not use the 'pending clarification' label."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "None of the output files contain any reference to 'sha256', 'digest', 'Description digest', or '[sdlc-workflow]'. No digest comments are present in any of the 7 output files (impact-map.md and task-1 through task-6)."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the 6 task descriptions contain any reference to 'CONVENTIONS.md', 'Per CONVENTIONS.md', or 'Applies:' rationale lines. The convention-aware enrichment process is completely absent from all task outputs. No convention applicability analysis is documented anywhere in the output files."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature has Priority: Normal (not Undefined). The impact-map.md states 'Priority: Normal (propagated to all tasks)' under 'Fields Inherited from Feature'. However, none of the 6 task descriptions contain an 'additional_fields' section or any mention of 'priority' being set as a field. The priority inheritance is documented only at the impact map level, not in the actual task output format that would be sent to Jira."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature has Fix Versions: RHTPA 1.6.0. There is no fixVersion scope config in CLAUDE.md, so it defaults to 'both', meaning tasks should include fixVersions. The impact-map.md states 'Fix Versions: RHTPA 1.6.0 (propagated to all tasks)'. However, none of the 6 task descriptions contain an 'additional_fields' section or any mention of 'fixVersions' being set. The fixVersion inheritance is documented only at the impact map level, not in the actual task output."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "There is no summary comment output file in the outputs directory. The impact-map.md mentions 'Priority: Normal (propagated to all tasks)' and 'Fix Versions: RHTPA 1.6.0 (propagated to all tasks)' under 'Fields Inherited from Feature', but there is no dedicated summary comment file that would represent a comment posted on the feature issue (Step 6c). The outputs only contain impact-map.md and task-1 through task-6."

</details>

<details>
<summary>eval-3: 5 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output file contains any sha256 digest, '[sdlc-workflow]' marker, or digest comment. Searched all output files for 'sha256', 'digest', and 'sdlc-workflow' - zero matches found. The description digest comments are entirely absent from the outputs."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task output contains any convention applicability rationale in the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. Searching for 'Per CONVENTIONS' and 'Applies:' yielded no matches across all task files. The only mentions of 'conventions' are generic references like 'per project conventions' (task-5), 'serialization conventions' (task-2), and 'integration test convention' (task-8), which are not the prescribed convention-enrichment format from convention-applicability-rules.md."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature issue (TC-9003) has Priority: Critical. However, no task output file contains any mention of 'priority', 'Critical', or 'additional_fields'. The priority inheritance is completely absent from all task descriptions."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature issue (TC-9003) has Fix Versions: RHTPA 1.5.0. The CLAUDE.md has no '### Jira Field Defaults' section, so the default scope 'both' applies, meaning fixVersions should be propagated to tasks. However, no task output file contains any mention of 'fixVersions', 'RHTPA', 'fix version', or 'additional_fields'. The fixVersion inheritance is completely absent from all task descriptions."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No output file contains a summary comment for the feature issue. Searched all outputs for 'summary', 'priority', 'fixVersion', 'RHTPA', 'Critical', and 'propagat' - no matches found. There is no file representing a summary comment posted to the feature issue TC-9003."

</details>

<details>
<summary>eval-4: 5 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output file contains any SHA-256 digest comment, '[sdlc-workflow] Description digest:' marker, or any hash value. The outputs consist only of the impact-map.md and 5 task description files. There is no evidence that description digest comments were posted."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task description contains any convention references, 'Per CONVENTIONS.md' citations, or 'Applies:' rationale lines. The Implementation Notes sections in all 5 tasks reference existing code patterns and file paths but do not cite any CONVENTIONS.md sections or include applicability rationales in the prescribed format. Convention-aware enrichment appears to not have been performed at all."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature issue has Priority: Major (not 'Undefined'), so every task should include priority in additional_fields. However, no task description contains an 'additional_fields' section or any mention of 'priority: Major' being inherited. The word 'priority' does not appear in any task file in the context of field inheritance."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature issue has Fix Versions: RHTPA 1.5.0, and CLAUDE.md has no ### Jira Field Defaults section (so fixVersion scope defaults to 'both'). Therefore every task should include fixVersions in additional_fields. However, no task description contains an 'additional_fields' section or any mention of fixVersions being inherited. 'RHTPA 1.5.0' does not appear in any task file."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No output file contains a summary comment. The outputs consist only of impact-map.md and 5 task description files. There is no file representing a summary comment on the feature issue, and no content in any file discusses inherited priority (Major) or fixVersion (RHTPA 1.5.0) propagation to tasks."

</details>

<details>
<summary>eval-5: 7 failing assertions</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "Task 1 (task-1-create-feature-branch.md) is missing 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections — it only has Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements, Dependencies. Task 8 (task-8-merge-feature-branch.md) is similarly missing these sections. While these are bookend tasks, the assertion requires ALL task files to contain these sections."

- **Assertion:** "The plan includes a workflow:feature-branch label decision to be applied to the feature issue"
  **Evidence:** "No output file contains the text 'workflow:feature-branch' or any mention of a label decision to be applied to the feature issue. The impact-map.md discusses workflow mode selection but does not mention applying a 'workflow:feature-branch' label. Grep across all output files for 'label' and 'workflow' found no relevant matches."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output file contains any SHA-256 digest, 'sha256-md:', 'sha256-adf:', or '[sdlc-workflow] Description digest' marker. Grep across all output files for 'sha256' and 'digest' returned zero matches."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No output file contains the text 'Applies:', 'convention-applicability', or any structured convention rationale. While tasks reference project conventions in free-form prose (e.g., 'Follow the existing migration pattern' in task 2, 'per project conventions' in task 5), there is no formal convention-aware enrichment with applicability validation or prescribed-format rationale."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature issue has Priority: High. However, no output file contains the text 'additional_fields', 'priority', or 'High'. No task file includes any field inheritance or propagation metadata."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature issue has Fix Versions: RHTPA 2.0.0 and there is no fixVersion scope config in CLAUDE.md (defaulting to 'both'). However, no output file contains the text 'additional_fields', 'fixVersions', or 'RHTPA'. No task file includes any field inheritance metadata."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No output file contains a summary comment referencing inherited priority or fixVersion values. No file mentions 'propagated', 'inherited', 'RHTPA', 'High' (as priority), or any statement about omission of these fields."

</details>

<details>
<summary>eval-6: 9 failing assertions</summary>

- **Assertion:** "Each task specifies its parent Epic key in the output — tasks targeting trustify-backend are assigned to the backend Epic, tasks targeting trustify-ui are assigned to the frontend Epic"
  **Evidence:** "The individual task files (task-2 through task-6) do not contain any reference to a parent Epic key. Tasks specify a Repository but not a parent Epic. The impact-map.md shows the Epic-to-task assignment in a table (backend Epic: Tasks 2, 3; UI Epic: Tasks 4, 5, 6), but the individual task files themselves do not specify their parent Epic key. The assertion requires 'each task specifies its parent Epic key in the output'."

- **Assertion:** "Incorporates links are created from the Feature to each Epic (not from Feature to individual Tasks)"
  **Evidence:** "No output file mentions 'Incorporates' links or any Jira link creation from the Feature (TC-9006) to Epics. The impact-map.md documents Epic grouping but does not describe link creation. No evidence of Incorporates link creation in any output file."

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "Task 1 (task-1-create-feature-branch.md) is missing 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. It only has Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, and Test Requirements. Task 7 (task-7-merge-feature-branch.md) is also missing 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. Tasks 2-6 all contain the required sections. Since the assertion says 'each task file', Tasks 1 and 7 fail this check. Note: these are bookend tasks, which may have different template requirements, but the assertion does not exclude them."

- **Assertion:** "Epics are created with the level-1 issue type name ('Epic') and parent set to the feature issue key"
  **Evidence:** "No output file contains evidence of Epics being created with issue type 'Epic' or with a parent set to 'TC-9006'. The impact-map.md documents the Epic grouping plan but does not specify the issue type name or parent field values used for Epic creation. No Jira API call outputs or Epic creation confirmations are present in the outputs."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output file contains any SHA-256 digest comment, '[sdlc-workflow] Description digest:' marker, or any hash value. The outputs consist only of task markdown files and an impact map, with no evidence of digest comments being posted."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any convention-applicability rationale in the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The task files reference conventions implicitly through Implementation Notes (e.g., 'Follow the existing module pattern', 'Follow the endpoint registration pattern'), but these are free-form prose descriptions of patterns, not convention-applicability formatted rationales. There is no evidence of convention-applicability validation per convention-applicability-rules.md."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature TC-9006 has priority 'Major'. The impact-map.md mentions 'Priority: Major (inherited from TC-9006, propagated to all Epics and Tasks)' under Field Inheritance. However, no task file contains an 'additional_fields' section or any explicit priority field. The priority inheritance is only documented in the impact map, not in the individual task outputs as 'additional_fields'."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature TC-9006 has fixVersions 'RHTPA 1.5.0'. The CLAUDE.md has no explicit fixVersion scope config, so it defaults to 'both'. The impact-map.md mentions 'Fix Versions: RHTPA 1.5.0 (inherited from TC-9006, propagated to all Epics and Tasks — fixVersion scope defaults to "both")'. However, no task file contains an 'additional_fields' section with 'fixVersions'. The fixVersion inheritance is only documented in the impact map, not in the individual task outputs."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No output file contains a summary comment for the feature issue. The impact-map.md mentions field inheritance (Priority: Major, Fix Versions: RHTPA 1.5.0) but this is in the impact map, not in a summary comment on the feature issue. There is no file in the outputs directory that represents a summary comment posted to TC-9006."

</details>

**Pass rate:** 56% · **Tokens:** 60,925 · **Duration:** 210s

**Baseline** (`b22bcfd2`): 76% · 47,235 tokens · 217s

