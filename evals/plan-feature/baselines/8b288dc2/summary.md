## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 16/16 | 0 | 100% |
| eval-2 | 10/14 | 4 | 71% |
| eval-3 | 11/15 | 4 | 73% |
| eval-4 | 7/11 | 4 | 64% |
| eval-5 | 12/15 | 3 | 80% |

### Failed Assertions

<details>
<summary>eval-2: 4 failing assertions</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment is present in any task description. The Implementation Notes reference docs/constraints.md sections (e.g., 'Per docs/constraints.md §5.2', 'Per docs/constraints.md §5.4', 'Per docs/constraints.md §5.11') but do not reference CONVENTIONS.md at all. The repo-backend.md fixture lists a CONVENTIONS.md file, and the convention-applicability-rules.md requires that applicable conventions include the prescribed rationale format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. No such rationale appears in any task. Convention-aware enrichment was not performed."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature fixture (feature-ambiguous.md) has Priority: Normal. The impact-map.md correctly notes 'Priority: Normal (inherited from TC-9002, will be propagated to all tasks)'. However, none of the 4 task description files contain an 'additional_fields' section or any mention of priority. The tasks only have the standard template sections. The priority inheritance is documented as intent in the impact map but not actually present in the task output files."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature fixture has Fix Versions: RHTPA 1.6.0, and CLAUDE.md has no ### Jira Field Defaults section so the scope defaults to 'both'. The impact-map.md correctly identifies this: 'Fix Versions: RHTPA 1.6.0 (inherited from TC-9002, will be propagated to all tasks — fixVersion scope defaults to "both")'. However, none of the 4 task files contain an 'additional_fields' section or any mention of fixVersions. The fixVersions inheritance is stated as intent but not actually present in the task outputs."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "There is no separate summary comment file in the outputs directory. The impact-map.md contains a 'Priority and Fix Version Propagation' section at the bottom (lines 51-53) stating 'Priority: Normal (inherited from TC-9002, will be propagated to all tasks)' and 'Fix Versions: RHTPA 1.6.0 (inherited from TC-9002, will be propagated to all tasks)'. However, this is in the impact map, not a summary comment posted on the feature issue (Step 6c). No output file represents the summary comment that would be posted to the feature issue, so the assertion cannot be confirmed as satisfied."

</details>

<details>
<summary>eval-3: 4 failing assertions</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the 9 task descriptions contain any convention applicability rationale in the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. There is no evidence of convention-aware enrichment in any task output. No conventions are listed with applicability rationale anywhere in the output files."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature issue (feature-multi-repo.md) has Priority: Critical. However, none of the 9 task descriptions contain an 'additional_fields' section or any mention of priority inheritance. There is no evidence that priority was propagated to created tasks."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature issue has Fix Versions: RHTPA 1.5.0 and the CLAUDE.md does not contain a '### Jira Field Defaults' section, so the default scope 'both' should apply. However, none of the 9 task descriptions contain an 'additional_fields' section or any mention of fixVersions inheritance. There is no evidence that fixVersions was propagated to created tasks."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No summary comment file was found in the outputs directory. The outputs contain only impact-map.md and task-1 through task-9 files. There is no evidence of a summary comment mentioning priority (Critical) or fixVersion (RHTPA 1.5.0) propagation."

</details>

<details>
<summary>eval-4: 4 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "Each task file contains a '## Description Digest' section with a sha256-md: prefixed 64-character lowercase hex hash (e.g., task-1: sha256-md:cc0ce990c78f95c2469b66d18dd866684f646f421e50a26652004ca55f6894df). However, the assertion requires the specific marker format '[sdlc-workflow] Description digest: sha256-md:&lt;hash&gt;' which represents a comment posted on the Jira task. The digests in the output files appear as bare 'sha256-md:&lt;hash&gt;' values under a '## Description Digest' heading, not in the prescribed '[sdlc-workflow] Description digest:' comment format. There is no evidence of a separate comment being posted — no comment output files exist, and the digest lines in task descriptions do not use the required marker format."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature fixture TC-9004 has Priority: Major (not 'Undefined'). The impact map states 'Priority: Major (propagated to tasks)'. However, none of the 5 task description files contain 'priority', 'additional_fields', or any field indicating the inherited priority. Searched all task files for 'priority' and 'additional_fields' with zero matches. The assertion requires every created task's additional_fields to include 'priority' with 'Major', but this is absent from all task outputs."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature fixture TC-9004 has Fix Versions: RHTPA 1.5.0 (non-empty). The CLAUDE.md has no '### Jira Field Defaults' section, so fixVersion scope defaults to 'both'. The impact map states 'Fix Versions: RHTPA 1.5.0 (propagated to tasks -- fixVersion scope defaults to both)'. However, none of the 5 task description files contain 'fixVersions', 'fixVersion', 'RHTPA', or 'additional_fields'. Searched all task files with zero matches. The assertion requires every created task's additional_fields to include 'fixVersions' with the inherited version, but this is absent from all task outputs."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No summary comment output file exists in the outputs directory. The only files are impact-map.md and 5 task description files. While the impact-map.md header mentions 'Priority: Major (propagated to tasks)' and 'Fix Versions: RHTPA 1.5.0 (propagated to tasks)', there is no dedicated summary comment file that would represent the Step 6c comment posted to the feature issue. The impact map is not a summary comment — it is a separate artifact. No evidence of a summary comment being generated or posted."

</details>

<details>
<summary>eval-5: 3 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "Each task file contains a digest line at the bottom (e.g., task-1: 'Description Digest: sha256-md:3d7e8e3b5193b60dddc401b12dd7b1d35bda5f0a76e4e73b52951172f3a6d376'), but the format does not match the required marker format '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;'. The actual format is 'Description Digest: sha256-md:...' without the '[sdlc-workflow]' prefix. Additionally, there is no evidence these were posted as comments on the Jira issues — they appear only as metadata lines within the task files themselves."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "The repo-backend.md fixture lists a CONVENTIONS.md file in the repository tree. However, none of the intermediate task files (tasks 2-6) contain any convention references, 'Per CONVENTIONS.md' citations, or applicability rationales in their Implementation Notes sections. There is no evidence of convention-aware enrichment being performed at all — no conventions are referenced with the prescribed 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' format."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No output file contains a summary comment for the feature issue that mentions inherited priority and fixVersion propagation. The impact-map.md discusses workflow mode and label decisions but does not mention priority or fixVersion inheritance. There is no separate summary comment file in the outputs directory."

</details>

**Pass rate:** 78% · **Tokens:** 70,380 · **Duration:** 317s

**Baseline** (`1f575ac4`): 54% · 56,598 tokens · 187s

