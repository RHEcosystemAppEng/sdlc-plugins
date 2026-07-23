## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 18/19 | 1 | 95% |
| eval-2 | 15/16 | 1 | 94% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 9/11 | 2 | 82% |
| eval-5 | 13/15 | 2 | 87% |
| eval-6 | 12/14 | 2 | 86% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "All 8 digest files (task-1-digest.md through task-8-digest.md) contain '[sdlc-workflow] Description digest: sha256-md:&lt;computed-after-jira-creation&gt;' — the value '&lt;computed-after-jira-creation&gt;' is a placeholder string, NOT 64 lowercase hex characters. The assertion requires exactly 64 lowercase hex characters after the 'sha256-md:' prefix, not a placeholder. No actual SHA-256 hash is present in any digest file."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Digest files exist for all three tasks (task-1-digest.md, task-2-digest.md, task-3-digest.md), but each contains a placeholder instead of an actual hash: 'sha256-adf:&lt;64-char-hex-digest-computed-at-creation-time&gt;'. The files explicitly state 'The actual hex digest cannot be computed in this eval because the description is not posted to Jira.' The assertion requires 'exactly 64 lowercase hex characters', not a placeholder."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "UI-facing frontend tasks (pages, components) reference Figma design context mentioning specific PatternFly components and visual specifications — API-layer frontend tasks (API types, client functions, hooks) are exempt from this requirement"
  **Evidence:** "Task 5 (SbomComparePage) references Figma design context with a 'Figma component mapping' table listing PatternFly components (Select, ExpandableSection, Badge, Table, SeverityBadge, EmptyState, Dropdown) with visual specifications. However, Task 6 (SbomListPage compare selection) is a UI-facing task (adds checkboxes, toolbar button to a page) and does NOT reference Figma design context at all. It mentions 'PatternFly 5 components' and 'PatternFly Td with select prop' but has no Figma reference."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Separate digest files exist for all 6 tasks (task-1-digest.md through task-6-digest.md). However, every digest file contains the placeholder string 'sha256-adf:&lt;computed-64-char-hex-digest&gt;' instead of an actual 64-character hex hash. Each file explicitly states 'The actual hex digest would be computed at runtime from the Jira-persisted description content. It is not pre-computed here because Jira normalizes content during storage.' The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:, not a placeholder, abbreviated value, or example string.' The placeholder '&lt;computed-64-char-hex-digest&gt;' fails this requirement."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No output file contains any reference to conventions, CONVENTIONS.md, or convention applicability rationales. None of the 6 task descriptions contain 'Per CONVENTIONS.md' references, 'Applies: task modifies' rationales, or any convention-related content. The impact map also contains no mention of convention validation. There is no evidence that convention-aware enrichment was performed — no conventions are included with rationales, and no documentation explains that conventions were checked and found inapplicable. Burden of proof is on PASS and no evidence of the process exists."

</details>

<details>
<summary>eval-5: 2 failing assertions</summary>

- **Assertion:** "Each non-documentation task file contains all required template sections: Repository, Target Branch, Description, at least one of Files to Modify or Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements. Documentation tasks are exempt from requiring Files to Modify, Files to Create, and Implementation Notes — they must still include Repository, Target Branch, Description, Acceptance Criteria, and Test Requirements"
  **Evidence:** "Bookend tasks (Task 1 and Task 8) are non-documentation tasks but are missing required sections. Task 1 (task-1-create-feature-branch.md) has Repository, Target Branch, Description, Acceptance Criteria, Test Requirements but is missing Files to Modify/Create and Implementation Notes. Task 8 (task-8-merge-feature-branch.md) similarly has Repository, Target Branch, Description, Acceptance Criteria, Test Requirements but is missing Files to Modify/Create and Implementation Notes. Intermediate non-documentation tasks 2-6 all contain the required sections. Documentation task 7 correctly includes Repository, Target Branch, Description, Acceptance Criteria, Test Requirements (exempt from Files to Modify/Create and Implementation Notes)."

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "Separate digest files exist for all 8 tasks (task-1-digest.md through task-8-digest.md). However, every digest file contains the placeholder string 'sha256-adf:&lt;64-char-hex-digest&gt;' instead of an actual 64-character hexadecimal hash. For example, task-1-digest.md line 27: '[sdlc-workflow] Description digest: sha256-adf:&lt;64-char-hex-digest&gt;'. The assertion explicitly requires 'exactly 64 lowercase hex characters' and 'not a placeholder, abbreviated value, or example string'. The '&lt;64-char-hex-digest&gt;' text is a placeholder, not a real hash."

</details>

<details>
<summary>eval-6: 2 failing assertions</summary>

- **Assertion:** "For each task created, a description digest is produced — evidenced by a separate digest file (e.g., task-N-digest.md), a digest entry in the impact map, or a '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker in any output file. The digest must contain a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string"
  **Evidence:** "All 7 digest files (task-1-digest.md through task-7-digest.md) exist but contain the placeholder '[sdlc-workflow] Description digest: sha256-md:&lt;computed-after-jira-creation&gt;' instead of an actual 64-character hex hash. The assertion requires 'exactly 64 lowercase hex characters prefixed by sha256-md: or sha256-adf:, not a placeholder, abbreviated value, or example string'. '&lt;computed-after-jira-creation&gt;' is a placeholder, not a valid hash."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any convention-aware enrichment section, no 'Applies:' rationale markers, and no references to convention-applicability-rules.md. Searched all 7 task description files and the impact-map.md — no evidence of convention validation or applicability rationale in any output file."

</details>

**Pass rate:** 89% · **Tokens:** 79,139 · **Duration:** 409s

**Baseline** (`7a01ea4a`): 89% · 77,107 tokens · 378s

---
*Generated by [sdlc-workflow/run-evals](https://github.com/RHEcosystemAppEng/sdlc-plugins) v0.13.4*

