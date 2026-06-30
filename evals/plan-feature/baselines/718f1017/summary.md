## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 16/16 | 0 | 100% |
| eval-2 | 11/14 | 3 | 79% |
| eval-3 | 14/15 | 1 | 93% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 14/15 | 1 | 93% |

### Failed Assertions

<details>
<summary>eval-2: 3 failing assertions</summary>

- **Assertion:** "When the Feature issue has a priority set (not 'Undefined'), every created task's additional_fields includes 'priority' with the inherited priority name. When the Feature's priority is 'Undefined', the priority key is omitted entirely from additional_fields (not set to null or 'Undefined')"
  **Evidence:** "The feature TC-9002 has priority 'Normal'. The impact-map.md mentions priority propagation: 'Priority: Normal (from feature TC-9002) — will be propagated to all created tasks.' However, neither task-1 nor task-2 output files contain any 'additional_fields' section or explicit mention of priority being set in the task's Jira fields. The evidence only shows intent in the impact map, not actual task-level additional_fields with priority set. Since this is an eval with no real Jira, the task files themselves do not contain evidence of additional_fields with priority."

- **Assertion:** "When the Feature issue has a non-empty fixVersions array and the fixVersion scope config (from ### Jira Field Defaults in CLAUDE.md) is 'task' or 'both' (or absent, defaulting to 'both'), every created task's additional_fields includes 'fixVersions' with the inherited version(s). When fixVersion scope is 'feature' or the Feature has no fixVersions, the fixVersions key is omitted entirely from additional_fields"
  **Evidence:** "The feature TC-9002 has fixVersions 'RHTPA 1.6.0'. The CLAUDE.md has no fixVersion scope config, defaulting to 'both'. The impact-map.md states: 'fixVersions: RHTPA 1.6.0 (from feature TC-9002) — will be propagated to all created tasks.' However, neither task-1 nor task-2 output files contain any 'additional_fields' section or explicit mention of fixVersions being set in the task fields. The evidence only shows intent in the impact map, not actual task-level additional_fields with fixVersions."

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "There is no summary comment file in the outputs directory. The outputs contain only impact-map.md, task-1-search-indexes-migration.md, and task-2-search-fulltext-ranking.md. No file represents or contains a summary comment posted to the feature issue. The impact-map.md mentions priority and fixVersions propagation intent, but this is not a summary comment on the feature issue (Step 6c)."

</details>

<details>
<summary>eval-3: 1 failing assertion</summary>

- **Assertion:** "After each task is created, a description digest comment is posted with a format-tagged SHA-256 hash — exactly 64 lowercase hex characters prefixed by 'sha256-md:' or 'sha256-adf:', not a placeholder, abbreviated value, or example string. Marker format: '[sdlc-workflow] Description digest: sha256-md:&lt;64-char-hex&gt;' (or sha256-adf). The digest is computed by re-fetching the description from the API and running scripts/sha256-digest.py"
  **Evidence:** "Tasks 1-6 have valid digest comments with correct format and 64-char hex hashes: task-1 (sha256-md:d6733e781af5c10eaeb950a884d6e48bb5c620db8eac8d4a908570249da62562), task-2 (sha256-md:3cee5eafa9b6c24da656572dc23129aa45d8ebc2e3da6b27bbef313a4f1f07a2), task-3 (sha256-md:ec3a694b6575e8730228175aa4e2e3205454c23617715bb11979643ffe53fe5d), task-4 (sha256-md:218eb06f25ffc78d7b767d10dfd6ac4f7d281c35172f172ce16977093feccb0b), task-5 (sha256-md:9f29f5fbcfabf50a6c369c332112b7a0475f258bd474973b72edb44cbb8eddaa), task-6 (sha256-md:cb04b5b1f0af2c4bb22318ea0063407487b1565349454a7e217dc06c9bc67ceb). However, task-7 and task-8 are missing digest comments entirely. The assertion requires a digest 'after each task is created' — 2 of 8 tasks lack digests, so this fails."

</details>

<details>
<summary>eval-5: 1 failing assertion</summary>

- **Assertion:** "Convention-aware enrichment validates file-type applicability per shared/convention-applicability-rules.md before including a convention — inapplicable conventions are excluded entirely (not listed with 'Not applicable' annotations), and applicable ones include a rationale in the prescribed format ('Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;'), not free-form prose"
  **Evidence:** "No task file contains any convention-applicability rationale in the prescribed 'Applies: task modifies &lt;file&gt; matching the convention's &lt;scope&gt;' format. The repo-backend.md fixture shows CONVENTIONS.md exists in the repository root, indicating conventions should have been checked. Task Implementation Notes reference 'docs/constraints.md' sections but never reference CONVENTIONS.md conventions with the required applicability rationale format. There is no evidence of convention-aware enrichment per shared/convention-applicability-rules.md."

</details>

**Pass rate:** 93% · **Tokens:** 0 · **Duration:** 0s

**Baseline** (`7142c02`): 100% · 0 tokens · 0s

