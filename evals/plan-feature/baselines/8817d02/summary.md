## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/13 | 1 | 92% |
| eval-2 | 11/11 | 0 | 100% |
| eval-3 | 10/12 | 2 | 83% |
| eval-4 | 6/8 | 2 | 75% |
| eval-5 | 10/12 | 2 | 83% |

### Failed Assertions

<details>
<summary>eval-1: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task contains any convention applicability rationale in the prescribed format 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'. The Implementation Notes in all 6 tasks reference 'docs/constraints.md' sections (e.g., '§5.2', '§5.4', '§4.6', '§5.11') but never reference CONVENTIONS.md. The repo-backend.md manifest shows a CONVENTIONS.md file exists at the repository root (line 15), and the Key Conventions section lists multiple conventions (Framework: Axum, Module pattern, Error handling, Endpoint registration, Response types, Query helpers, Testing, Caching) that would be applicable to tasks modifying .rs files. Yet no convention enrichment with applicability rationale appears in any task output."

</details>

<details>
<summary>eval-3: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "All 10 task files contain sha256-md: digests with valid 64-character lowercase hex hashes (e.g., task-1: sha256-md:596764b370a18a174918ff88ce8d6852c0af3ca504efc105ba3546f58f61d9bf). However, the assertion requires the marker format '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;'. The actual format in the files is bare 'sha256-md:&lt;hex&gt;' without the '[sdlc-workflow] Description digest:' prefix. No file in the outputs directory contains the string '[sdlc-workflow]' or 'Description digest'. The digests appear as standalone lines at the end of each task file, not in the prescribed comment format."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task output contains the prescribed 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' rationale format. Searching all output files for 'Applies:' returns zero matches. The tasks reference docs/constraints.md sections (e.g., 'Per docs/constraints.md §4.6', 'Per docs/constraints.md §5.4') but these are constraint references, not CONVENTIONS.md convention enrichments with applicability rationales. No CONVENTIONS.md conventions are referenced with the required applicability format anywhere in the outputs."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "Each task file contains a sha256-md digest at the bottom (e.g., task-1: 'sha256-md:4297e7a4768664538f71438140415bff62f27da1b0a47b7e078dd85fdfd4d6e4', task-2: 'sha256-md:43c42be0671d33b3c883bd8f2bc1fa29dfe72f9afe0d69c6891281c9130bd6f2', etc.). All are 64 lowercase hex characters prefixed with 'sha256-md:'. However, the required marker format is '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' and none of the digests use this full marker format. The digests appear as bare 'sha256-md:&lt;hex&gt;' lines at the end of each file, missing the '[sdlc-workflow] Description digest:' prefix. There is no evidence that these were posted as Jira comments with the prescribed format."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the 5 task descriptions contain any references to CONVENTIONS.md or convention applicability rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'). The tasks reference 'docs/constraints.md' sections (e.g., 'Per docs/constraints.md section 5 (Code Change Rules)') but these are constraint references, not convention enrichment. There is no evidence that convention-aware enrichment with file-type applicability validation was performed. No 'Per CONVENTIONS.md §...' entries appear in any Implementation Notes section. Without any evidence that the convention applicability check was executed, the assertion cannot be verified as PASS."

</details>

<details>
<summary>eval-5: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "Each task file contains a sha256-md: hash at the end (e.g., task-1: 'sha256-md:9c5e8bfb9a81a70709c9f6d9adffe1c67ecfa0aae08c61007d5a0878c65d8ae6'). All hashes are 64 lowercase hex characters prefixed with sha256-md:. However, the required marker format is '[sdlc-workflow] Description digest: sha256-md:&lt;hash&gt;' and none of the task files use this full marker format — they contain only the bare 'sha256-md:&lt;hash&gt;' without the '[sdlc-workflow] Description digest:' prefix. The impact-map.md also has a bare hash. No evidence of the prescribed comment format being used."

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "None of the 8 task files or the impact-map.md contain any convention sections, convention applicability rationale, or 'Applies: task modifies' text. There is no evidence of convention-aware enrichment having been performed. A grep for 'convention', 'Convention', and 'applicab' across all output files found only incidental references to project conventions (e.g., 'per the project convention') but no structured convention applicability sections with the prescribed rationale format."

</details>

**Pass rate:** 87% · **Tokens:** 57,050 · **Duration:** 175s

**Baseline** (`4f620b9`): 92% · 61,140 tokens · 226s

