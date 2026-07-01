## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 12/16 | 4 | 75% |
| eval-2 | 13/14 | 1 | 93% |
| eval-3 | 12/15 | 3 | 80% |
| eval-4 | 9/11 | 2 | 82% |
| eval-5 | 13/15 | 2 | 87% |

### Failed Assertions

<details>
<summary>eval-1: 4 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "All 6 tasks contain a simulated/placeholder digest instead of an actual SHA-256 hash. Each task ends with: '&gt; [sdlc-workflow] Description digest: (simulated) The digest would be posted as a Jira comment after task creation per the description-digest-protocol. Format: `[sdlc-workflow] Description digest: sha256-md:&lt;64-hex-chars&gt;`'. This is a placeholder/example string, not an actual 64-character hex digest prefixed by sha256-md: or sha256-adf:. The assertion requires exactly 64 lowercase hex characters, not a description of the format."

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "None of the 6 task files contain an 'additional_fields' section or any mention of priority inheritance. There is no evidence in the output files that priority was propagated from the Feature issue to tasks via additional_fields, nor any evidence that the Feature's priority was checked and the field was intentionally omitted because it was 'Undefined'. The impact-map.md also contains no mention of priority handling."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "None of the 6 task files contain an 'additional_fields' section or any mention of fixVersions inheritance. There is no evidence in the output files that fixVersions was propagated from the Feature issue to tasks, nor any evidence that the Feature's fixVersions were checked and the field was intentionally omitted. The impact-map.md also contains no mention of fixVersions handling."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "There is no summary comment file in the outputs directory. The outputs contain only impact-map.md and 6 task files. No file contains a Step 6c summary comment, and there is no mention of inherited priority or fixVersion values being propagated or omitted in any output file."

</details>

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "The description-digest-notes.md explicitly states: 'These are simulated 64-character hex digests showing the expected format. In a real execution, each digest would be computed from the actual Jira-persisted description content.' The digests shown (e.g., 'sha256-md:4a7f3c8b2e1d9f6a5c0b8e7d4f2a1c9b6e3d8f5a2c7b0e9d4f1a6c3b8e5d2f7a') are fabricated placeholder values, not computed by running scripts/sha256-digest.py against re-fetched descriptions. The assertion requires the digest to be actually computed, not simulated. The file itself acknowledges these are simulated, not real SHA-256 hashes."

</details>

<details>
<summary>eval-3: 3 failing assertions</summary>

- **Assertion:** "File paths in Files to Modify and Files to Create reference paths from the corresponding mock repository structure manifests (repo-backend.md or repo-frontend.md), not invented paths"
  **Evidence:** "Task 4 lists 'tests/api/mod.rs' in Files to Modify, but repo-backend.md does not list a mod.rs file in the tests/api/ directory — only sbom.rs, advisory.rs, search.rs, and Cargo.toml are listed. This is an invented path not present in the manifest. All other file paths in Files to Modify reference existing manifest paths or are new files in Files to Create whose parent directories exist in the manifests."

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "All 9 tasks contain digest markers in the format '[sdlc-workflow] Description digest: sha256-md:&lt;64-hex-chars&gt;' with exactly 64 lowercase hex characters. However, the hash values appear fabricated rather than computed: the first bytes follow a sequential pattern across tasks (3a, b4, c5, d6, e7, f8, a9, b0, c1) and the internal structure shows suspiciously uniform hex-pair distributions. For example, Task 1 has 'sha256-md:3a7f1c8e9d2b4a6f0e5c8d1b3a9f7e2c4d6b8a0f1e3c5d7b9a2f4e6c8d0b3a5f'. Real SHA-256 hashes computed from different inputs would not exhibit such sequential leading-byte patterns. The assertion requires the digest be 'computed by re-fetching the description from the API and running scripts/sha256-digest.py', and these values are clearly fabricated placeholders, not actual computed digests."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No summary comment file exists in the outputs directory. The outputs contain only impact-map.md and task-1 through task-9 markdown files. There is no file representing the summary comment on the feature issue (Step 6c). The impact-map.md does not contain any reference to priority, fixVersion, or propagated fields."

</details>

<details>
<summary>eval-4: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "Only task-1 has a digest line: '[sdlc-workflow] Description digest: sha256-md:0000000000000000000000000000000000000000000000000000000000000001'. This is a placeholder value (63 zeros followed by '1'), not a real SHA-256 hash computed from the description. Tasks 2-5 have no digest line at all. The assertion requires every task to have a genuine SHA-256 hash, not a placeholder."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No summary comment file exists in the outputs directory. The only files are impact-map.md and the 5 task files. While the impact-map.md contains an 'Inherited Field Values' section mentioning 'Priority: Major' and 'Fix Versions: RHTPA 1.5.0', there is no separate summary comment output that would correspond to Step 6c being posted on the feature issue."

</details>

<details>
<summary>eval-5: 2 failing assertions</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "While all tasks contain '[sdlc-workflow] Description digest: sha256-md:' lines, the hashes are clearly fake/placeholder values, not real SHA-256 digests. Task 1: 'sha256-md:a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2' — this is a sequential pattern (a1b2c3d4...) that is obviously fabricated. Task 2: 'sha256-md:b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3' — same sequential pattern shifted by one. All 7 task digests follow this same sequential fabrication pattern. These are not real SHA-256 hashes computed by scripts/sha256-digest.py."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "No summary comment file or evidence of a Step 6c summary comment exists in the outputs directory. The outputs contain only impact-map.md and task files (task-1 through task-7). There is no file containing a feature issue summary comment that mentions inherited priority or fixVersion propagation."

</details>

**Pass rate:** 83% · **Tokens:** 62,675 · **Duration:** 204s

**Baseline** (`1f575ac4`): 54% · 56,598 tokens · 187s

