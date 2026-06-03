## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 11/13 | 2 | 85% |
| eval-2 | 7/11 | 4 | 64% |
| eval-3 | 10/12 | 2 | 83% |
| eval-4 | 6/8 | 2 | 75% |
| eval-5 | 8/12 | 4 | 67% |

### Failed Assertions

<details>
<summary>eval-1: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "None of the 6 task files or any other file in the outputs directory contains any reference to 'sha256', 'digest', '[sdlc-workflow]', or any hash values. There are no digest comment files or logs in the outputs directory. The only files present are impact-map.md and the 6 task description files. No evidence of description digest comments being posted."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the 6 task files contain convention applicability rationale in the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The Implementation Notes sections reference docs/constraints.md (e.g., 'Per docs/constraints.md Section 5 (Code Change Rules)') but do not reference CONVENTIONS.md conventions with applicability rationale. No task contains the prescribed 'Applies:' format. Convention-aware enrichment with applicability validation is absent from all outputs."

</details>

<details>
<summary>eval-2: 4 failing assertions</summary>

- **Assertion:** "Plan acknowledges that 'Better UI' (non-MVP) cannot be planned without design mockups or frontend repository and excludes it from scope"
  **Evidence:** "No mention of 'Better UI' appears anywhere in the impact-map.md or any of the four task files. The feature description (feature-ambiguous.md) lists 'Better UI | Make it look nicer | No' as a non-MVP requirement, but the plan simply omits it without any explicit acknowledgment that it cannot be planned due to missing design mockups or frontend repository. The assertion requires explicit acknowledgment, not silent omission."

- **Assertion:** "Tasks document assumptions where they fill in missing details, labeled as assumptions pending clarification"
  **Evidence:** "The impact-map.md uses 'Interpreted as:' language for each ambiguity and states 'These should be confirmed with the product owner before implementation begins,' but the individual task files (task-1 through task-4) do not label any assumptions as 'assumptions pending clarification.' Task descriptions present implementation details as definitive decisions (e.g., task-1 states 'adds tsvector columns and GIN indexes' without labeling this as an assumption). The assertion requires assumptions to be documented in the tasks and labeled as assumptions pending clarification, which is not done."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "None of the 5 output files (impact-map.md, task-1 through task-4) contain any '[sdlc-workflow] Description digest:' marker, 'sha256-md:', 'sha256-adf:', or any SHA-256 hash string. No evidence of digest comments being posted anywhere in the outputs."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the 4 task files contain any 'Per CONVENTIONS.md' references, 'Applies:' rationale lines, or any evidence of convention-aware enrichment. The Implementation Notes reference 'docs/constraints.md §2' and 'docs/constraints.md §5' (which are project constraints, not CONVENTIONS.md conventions), but no convention applicability validation was performed. The prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' appears nowhere in the outputs."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No sha256 digest comments were found in any of the output files. Searched all 11 files for 'sha256', 'digest', and '[sdlc-workflow]' — no matches. The outputs contain only task description markdown files and an impact map, with no evidence of digest comments being posted."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention applicability rationales were found in any task's Implementation Notes. Searched all output files for 'Applies:', 'CONVENTIONS.md', and 'convention' — no matches in the prescribed format. The word 'convention' appears only in generic context (e.g., 'TypeScript convention in this codebase', 'struct definition conventions', 'naming conventions') but never in the 'Per CONVENTIONS.md §...' format with an 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale. No evidence of convention-aware enrichment being performed."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No sha256 digest or '[sdlc-workflow] Description digest:' marker found anywhere in the output files. Searched all files in /tmp/plan-feature-eval-baseline/eval-4/outputs/ for 'sha256' and 'digest' — zero matches. No evidence of digest comments being posted for any of the 6 tasks."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-related content found anywhere in the output files. Searched all files for 'convention', 'Convention', and 'applicab' — zero matches. No 'Per CONVENTIONS.md' references, no 'Applies:' rationale lines, and no convention enrichment of any kind appears in any task description's Implementation Notes or elsewhere. Convention-aware enrichment was not performed."

</details>

<details>
<summary>eval-5: 4 failing assertions</summary>

- **Assertion:** "Each task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements"
  **Evidence:** "Bookend tasks (task-1-create-feature-branch.md and task-7-merge-feature-branch.md) are missing 'Files to Modify', 'Files to Create', and 'Implementation Notes' sections. Task 1 headers: Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements, Dependencies. Task 7 headers: Repository, Target Branch, Bookend Type, Description, Acceptance Criteria, Test Requirements, Dependencies. Neither has any Files to Modify/Create or Implementation Notes. Intermediate tasks 2-6 all have the required sections."

- **Assertion:** "The plan includes a workflow:feature-branch label decision to be applied to the feature issue"
  **Evidence:** "No mention of 'workflow:feature-branch' label or any label decision appears in any output file. Searched all files for 'label', 'workflow:feature-branch' -- no matches found. The impact-map.md mentions the feature-branch mode selection but does not include a label decision."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No output file contains any reference to 'sha256', 'digest', '[sdlc-workflow]', or any hash values. Searched all output files -- zero matches. No description digest comments are present in any task file."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No output file contains any 'Per CONVENTIONS.md', 'Applies:', or convention applicability rationale text. Searched all files for 'convention', 'Applies:', 'CONVENTIONS' -- only match was task-6-update-integration-tests.md line 21 referencing 'project conventions' in general prose, not a structured convention enrichment. No evidence of convention-aware enrichment or applicability validation."

</details>

**Pass rate:** 75% · **Tokens:** 47,086 · **Duration:** 187s

**Baseline** (`43d89b3`): 97% · 52,427 tokens · 174s

