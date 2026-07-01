## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 15/16 | 1 | 94% |
| eval-2 | 13/14 | 1 | 93% |
| eval-3 | 10/15 | 5 | 67% |
| eval-4 | 6/11 | 5 | 55% |
| eval-5 | 11/15 | 4 | 73% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "The repo-backend.md fixture lists a CONVENTIONS.md file in the trustify-backend repo root, but no CONVENTIONS.md content was provided as an eval fixture. The task descriptions do not include any convention-aware enrichment (no 'Per CONVENTIONS.md' references or 'Applies:' rationale lines in Implementation Notes). Since the repo manifest indicates CONVENTIONS.md exists, convention enrichment should have been attempted. However, without the actual CONVENTIONS.md content being available as a fixture file, conventions could not be read or applied. The assertion requires validation of convention applicability, which was not performed."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "All 4 task files contain a Description Digest section but use placeholder text: 'sha256-md:&lt;computed-at-creation-time&gt;' instead of an actual 64 lowercase hex character hash. The impact map also shows an example with 'sha256-md:a1b2c3d4e5f6...' which is abbreviated, not a full 64-char hex string. The assertion requires exactly 64 lowercase hex characters, not a placeholder or abbreviated value. Since there is no actual Jira API to re-fetch from and no scripts/sha256-digest.py execution, actual digests could not be computed."

</details>

<details>
<summary>eval-3: 5 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No description digest comments were generated in the output files. The eval is a file-based simulation without actual Jira API access, so no sha256 digests were computed or posted. No task file contains '[sdlc-workflow] Description digest: sha256-md:' or 'sha256-adf:' markers."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No convention-aware enrichment was performed. The repo fixtures (repo-backend.md and repo-frontend.md) both mention CONVENTIONS.md files exist in their directory trees, but the actual CONVENTIONS.md content was not provided as a fixture file. No task Implementation Notes contain 'Per CONVENTIONS.md' references or applicability rationales. Since both repos list CONVENTIONS.md in their directory trees, convention enrichment should have been attempted."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature TC-9003 has Priority: Critical. However, no task file contains an 'additional_fields' section with 'priority' set to 'Critical'. The impact map mentions priority propagation ('Priority: Critical — inherited from TC-9003, propagated to all tasks via additional_fields.priority') but this is not reflected in the actual task files. The task description template does not define an additional_fields section, and no task includes one."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature TC-9003 has Fix Versions: RHTPA 1.5.0. The CLAUDE.md has no explicit fixVersion scope config, so it defaults to 'both'. However, no task file contains an 'additional_fields' section with 'fixVersions' set to 'RHTPA 1.5.0'. The impact map mentions fixVersion propagation but this is not reflected in the actual task files."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No summary comment was generated for the feature issue. The impact map documents field propagation intentions ('Priority: Critical — inherited from TC-9003' and 'Fix Versions: RHTPA 1.5.0 — inherited from TC-9003') but no Step 6c summary comment was produced as a separate output. This is an API-dependent step that was not simulated in the file-based eval."

</details>

<details>
<summary>eval-4: 5 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No description digest comments were generated. The eval is a file-based simulation without Jira API access, so no '[sdlc-workflow] Description digest: sha256-md:...' markers were posted for any task. None of the output files contain SHA-256 digest markers."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "The repo fixture (repo-backend.md) mentions that CONVENTIONS.md exists in the repository root, but its contents were not provided in the eval fixtures. Task 1 notes 'Per CONVENTIONS.md: conventions are not referenced here as no CONVENTIONS.md content was provided in the fixture beyond noting its existence.' No convention-aware enrichment with prescribed rationale format was performed on any task. The assertion requires validation against convention-applicability-rules.md, but without CONVENTIONS.md content, no conventions could be applied or excluded."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature TC-9004 has Priority: Major. However, none of the 5 task files contain an 'additional_fields' section with 'priority' set to 'Major'. This is a Jira API field that would be set when creating tasks programmatically, but the eval is file-based and no additional_fields section was included in the task markdown files."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature TC-9004 has Fix Versions: RHTPA 1.5.0. The CLAUDE.md does not contain a '### Jira Field Defaults' section, so the scope defaults to 'both', meaning fixVersions should be propagated to tasks. However, none of the 5 task files contain an 'additional_fields' section with 'fixVersions'. This is a Jira API field that would be set when creating tasks programmatically."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No summary comment was generated for the feature issue TC-9004. The eval is file-based without Jira API access, so no Step 6c summary comment was produced. Neither the impact map nor any task file contains a summary comment section noting inherited priority (Major) or fixVersion (RHTPA 1.5.0) propagation."

</details>

<details>
<summary>eval-5: 4 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "No task file or impact map contains a description digest comment with the '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' marker. This is a Jira API operation that was not performed since this is an eval producing local files, not interacting with Jira. No SHA-256 hashes appear in any output file."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "The repo-backend.md fixture lists CONVENTIONS.md in the repository directory tree, but no CONVENTIONS.md content was provided as an eval fixture file. The impact map notes this gap: 'The CONVENTIONS.md file is listed in the repository structure but its contents are not available; convention-aware enrichment cannot be applied without reviewing the actual convention definitions.' No convention-aware enrichment was applied to any task, and no 'Per CONVENTIONS.md' rationale lines appear. Since the assertion requires validation of file-type applicability, and no conventions content was available to validate against, this cannot be confirmed as PASS."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature TC-9005 has Priority: High. The impact map documents that priority 'High' was inherited and propagated to all tasks. However, no task file contains an 'additional_fields' section or JSON block with a 'priority' key. The assertion requires that each task's additional_fields includes 'priority' with the inherited value, which is a Jira API operation not reflected in the local markdown task files."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature TC-9005 has Fix Versions: RHTPA 2.0.0, and no ### Jira Field Defaults section exists in CLAUDE.md (defaulting to 'both'). The impact map documents propagation intent. However, no task file contains an 'additional_fields' section or JSON block with 'fixVersions'. This is a Jira API operation not reflected in local markdown task files."

</details>

**Pass rate:** 76% · **Tokens:** 47,235 · **Duration:** 217s

**Baseline** (`8b288dc2`): 78% · 70,380 tokens · 317s

