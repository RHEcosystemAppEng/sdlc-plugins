## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/13 | 2 | 85% |
| eval-2 | 6/11 | 5 | 55% |
| eval-3 | 9/12 | 3 | 75% |
| eval-4 | 6/8 | 2 | 75% |
| eval-5 | 8/12 | 4 | 67% |

### Failed Assertions

<details>
<summary>eval-1: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "Searched all output files for 'sha256', 'digest', and 'Description digest' — no matches found in any of the 7 output files (impact-map.md, task-1 through task-6). No description digest comments are present in the outputs directory."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "Searched all 6 task files for 'CONVENTIONS', 'Applies:', and convention-related content. No task contains any reference to CONVENTIONS.md sections or convention applicability rationales in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'). The only convention-related references are to docs/constraints.md sections (e.g., 'Per docs/constraints.md Section 5 (Code Change Rules)' and 'Per docs/constraints.md Section 2 (Commit Rules)'), which are not the same as CONVENTIONS.md convention enrichment. No convention-aware enrichment with applicability validation was performed."

</details>

<details>
<summary>eval-2: 4 failing assertions</summary>

- **Assertion:** "Plan acknowledges that 'Better UI' (non-MVP) cannot be planned without design mockups or frontend repository and excludes it from scope"
  **Evidence:** "The impact-map.md does not mention 'Better UI' at all. While no task addresses the Better UI requirement, the plan never explicitly acknowledges its exclusion or explains that it cannot be planned without design mockups or a frontend repository. The Ambiguity Assessment section lists 4 ambiguities but does not include the Better UI requirement among them. The impact map's changes list covers only backend search improvements with no mention of excluding the non-MVP UI work."

- **Assertion:** "Tasks document assumptions where they fill in missing details, labeled as assumptions pending clarification"
  **Evidence:** "The impact-map.md states 'The following assumptions were made' and lists 4 assumptions, but these are not labeled as 'pending clarification.' The individual task descriptions (task-1 through task-5) do not contain any assumptions sections or labels indicating assumptions pending clarification. The assumptions in the impact map use language like 'Interpreted as:' but never use the phrase 'pending clarification' or similar labeling. The tasks themselves proceed as if the interpretations are final decisions rather than documenting them as assumptions awaiting confirmation."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output file contains any digest comment. Searching all output files for 'sha256', 'digest', 'sdlc-workflow' yields no matches related to description digests. None of the 5 task files or the impact-map.md contain a '[sdlc-workflow] Description digest: sha256-md:' or 'sha256-adf:' marker. No separate digest output files exist in the outputs directory."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task description contains any convention-aware enrichment section. None of the 5 task files contain the prescribed rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. There are no convention applicability assessments anywhere in the output files. While tasks reference docs/constraints.md sections (e.g., 'Per docs/constraints.md section 2 (Commit Rules)' in task-1 line 29), these are free-form prose references, not the prescribed convention enrichment format with applicability validation."

</details>

<details>
<summary>eval-3: 3 failing assertions</summary>

- **Assertion:** "UI-facing frontend tasks (pages, components) reference Figma design context mentioning specific PatternFly components and visual specifications — API-layer frontend tasks (API types, client functions, hooks) are exempt from this requirement"
  **Evidence:** "Task 6 (SbomComparePage) references Figma design context ('following the Figma design', 'Badge colors match Figma') and mentions specific PatternFly components (Select, ExpandableSection, Badge, Table, EmptyState, Skeleton, Dropdown, CodeBranchIcon). However, Task 7 (SbomListPage selection) is a UI-facing task (adds checkboxes and a button to a page) and does NOT reference Figma design context at all — it mentions PatternFly components but has zero 'Figma' or 'design' references. Task 5 (API types/hooks) and Task 8 (test fixtures) are API-layer tasks and are exempt."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output file contains any reference to 'sha256', 'digest', or '[sdlc-workflow]'. Grep across all output files returned zero matches. There are no digest comments in any of the output files."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task output contains any convention references in the prescribed format. Grep for 'convention' and 'CONVENTIONS' in all output files found only two incidental uses: task-8 mentions 'naming conventions' (referring to fixture naming patterns, not CONVENTIONS.md enrichment) and task-5 mentions 'field conventions' (referring to interface naming patterns). No task contains 'Per CONVENTIONS.md', 'Applies: task modifies', or any other evidence of convention-aware enrichment with applicability rationales."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "Searched all output files for 'sha256-md:', 'sha256-adf:', 'sdlc-workflow', and 'Description digest'. No matches found in any file. No digest comments are present in the outputs."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention applicability rationales in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;') were found in any task file. The tasks reference 'docs/constraints.md' sections (e.g., 'Per docs/constraints.md section 5') but do not reference CONVENTIONS.md at all, and none include the required 'Applies:' rationale format specified by convention-applicability-rules.md. There is no evidence that convention-aware enrichment with file-type applicability validation was performed."

</details>

<details>
<summary>eval-5: 4 failing assertions</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "task-1-create-feature-branch.md (bookend create-branch) is missing 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. task-7-merge-feature-branch.md (bookend merge-branch) is missing 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. Intermediate tasks 2-6 all contain the required sections."

- **Assertion:** "The plan includes a workflow:feature-branch label decision to be applied to the feature issue"
  **Evidence:** "No output file contains any mention of applying a 'workflow:feature-branch' label to the feature issue. The impact-map.md mentions 'Workflow Mode: `feature-branch`' but does not reference applying a label. None of the task files mention a label either."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output file contains any reference to 'sha256', 'digest', '[sdlc-workflow]', or any description digest comment. No evidence of SHA-256 hash computation or posting of digest comments after task creation."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No output file contains any 'Applies: task modifies' rationale format or any reference to convention-applicability-rules.md. While task files reference docs/constraints.md sections (e.g., '§2 Commit Rules', '§5 Code Change Rules'), these are free-form prose references, not the prescribed 'Applies:' format. No evidence of systematic convention applicability validation."

</details>

**Pass rate:** 71% · **Tokens:** 52,132 · **Duration:** 228s

**Baseline** (`7160d2f`): 86% · 52,125 tokens · 178s

