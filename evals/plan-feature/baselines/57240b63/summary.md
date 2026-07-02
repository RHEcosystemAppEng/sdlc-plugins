## Eval Results: plan-feature

| Eval | Passed | Failed | Pass Rate |
|------|--------|--------|-----------|
| eval-1 | 16/16 | 0 | 100% |
| eval-2 | 13/14 | 1 | 93% |
| eval-3 | 15/15 | 0 | 100% |
| eval-4 | 11/11 | 0 | 100% |
| eval-5 | 15/15 | 0 | 100% |
| eval-6 | 12/14 | 2 | 86% |

### Failed Assertions

<details>
<summary>eval-2: 1 failing assertion</summary>

- **Assertion:** "The summary comment on the feature issue (Step 6c) includes the inherited priority and fixVersion values that were propagated to tasks, or states they were omitted and why"
  **Evidence:** "The impact map (impact-map.md) does not contain any mention of inherited priority or fixVersion values. It covers ambiguities (lines 3-76), workflow mode (lines 78-89), and impact map structure (lines 91-103), but has no summary comment documenting field inheritance. No other output file contains a summary comment about propagated priority ('Normal') or fixVersion ('RHTPA 1.6.0') values. The only evidence of these fields is in each task's additional_fields section, but no summary comment documents what was propagated."

</details>

<details>
<summary>eval-6: 2 failing assertions</summary>

- **Assertion:** "Incorporates links are created from the Feature to each Epic (not from Feature to individual Tasks)"
  **Evidence:** "No mention of 'Incorporates' links anywhere in the outputs. The impact-map.md documents Epic Grouping and Inherited Fields but does not reference the Incorporates link type or any link creation from the Feature to the Epics."

- **Assertion:** "Epics are created with the level-1 issue type name ('Epic') and parent set to the feature issue key"
  **Evidence:** "The epic-*.md files contain only paragraph descriptions without structured fields. Neither epic-1-trustify-backend.md nor epic-2-trustify-ui.md contains an explicit issue type field set to 'Epic' or a parent field set to the feature issue key (TC-9006). The impact-map.md labels them as 'Epic 1' and 'Epic 2' in a table but does not explicitly specify the issue type name or parent field configuration."

</details>

**Pass rate:** 96% · **Tokens:** 80,983 · **Duration:** 398s

**Baseline** (`d573976e`): 56% · 60,925 tokens · 210s
