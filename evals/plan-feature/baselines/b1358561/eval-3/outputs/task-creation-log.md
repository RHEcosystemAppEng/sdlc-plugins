# Task creation log — TC-9003 (simulated; no Jira calls made)

Placeholder keys `TC-E1..E4` (Epics) and `TC-T1..T9` (Tasks) stand for keys Jira would assign.

## Inherited fields
| Field | Feature value | Decision |
|---|---|---|
| priority | Critical | Propagated (set, not "Undefined") |
| fixVersions | RHTPA 1.5.0 | Propagated (non-empty; `fixVersion scope: both`) |
| labels | — | `ai-generated-jira` on every created issue |

`additional_fields` used on **every** Epic and Task:
```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Critical"},
  "fixVersions": [{"name": "RHTPA 1.5.0"}]
}
```

## 6a.0 — Epics (issueTypeName = Epic, parent = TC-9003)
| Placeholder | Summary | Description file |
|---|---|---|
| TC-E1 | TC-9003: SBOM comparison diff API | epic-1-diff-api.md |
| TC-E2 | TC-9003: SBOM comparison UI | epic-2-comparison-ui.md |
| TC-E3 | TC-9003: Comparison export | epic-3-comparison-export.md |
| TC-E4 | TC-9003: Documentation | epic-4-documentation.md |

## 6a — Tasks (issueTypeName = Task)
| Placeholder | Summary | Parent | Description file | Digest comment |
|---|---|---|---|---|
| TC-T1 | TC-9003: Add SBOM comparison model and diff computation service | TC-E1 | task-1-sbom-diff-model-and-service.md | task-1-digest.md |
| TC-T2 | TC-9003: Add GET /api/v2/sbom/compare endpoint | TC-E1 | task-2-sbom-compare-endpoint.md | task-2-digest.md |
| TC-T3 | TC-9003: Add SBOM comparison API client and useSbomComparison hook | TC-E2 | task-3-frontend-compare-api-client.md | task-3-digest.md |
| TC-T4 | TC-9003: Add /sbom/compare page with SBOM selectors and URL-shareable state | TC-E2 | task-4-frontend-compare-page.md | task-4-digest.md |
| TC-T5 | TC-9003: Render collapsible diff sections, count badges and critical highlighting | TC-E2 | task-5-frontend-diff-sections.md | task-5-digest.md |
| TC-T6 | TC-9003: Add SBOM multi-select and "Compare selected" action to SBOM list | TC-E2 | task-6-frontend-sbom-list-compare-selected.md | task-6-digest.md |
| TC-T7 | TC-9003: Export SBOM comparison as JSON or CSV | TC-E3 | task-7-frontend-export-diff.md | task-7-digest.md |
| TC-T8 | TC-9003: Document GET /api/v2/sbom/compare endpoint | TC-E4 | task-8-docs-compare-endpoint.md | task-8-digest.md |
| TC-T9 | TC-9003: Document the SBOM comparison UI workflow | TC-E4 | task-9-docs-comparison-ui-guide.md | task-9-digest.md |

Each digest comment is posted immediately after the task is created, before links/other comments, as a standalone comment without footnote.

Feature label: workflow mode is `direct-to-main` → `workflow:feature-branch` NOT added to TC-9003.

## 6b — Links
**Incorporates (Feature → Epic):** TC-9003 → TC-E1, TC-E2, TC-E3, TC-E4

**Depend (inward = dependent, outward = dependency):**
| Dependent | Depends on |
|---|---|
| TC-T2 | TC-T1 |
| TC-T3 | TC-T2 |
| TC-T4 | TC-T3 |
| TC-T5 | TC-T4 |
| TC-T6 | TC-T4 |
| TC-T7 | TC-T5 |
| TC-T8 | TC-T1 |
| TC-T8 | TC-T2 |
| TC-T9 | TC-T4 |
| TC-T9 | TC-T5 |
| TC-T9 | TC-T6 |
| TC-T9 | TC-T7 |

## Choices made in place of interactive prompts
- Step 0.5 REST fallback prompt: not applicable (eval writes to files instead of Jira).
- Step 1.5 parent link prompt: skipped (no parent).
- Step 2.5 issue types: assumed Epic exists at level 1 (Feature is level 2 in TC).
- Step 4 impact map approval: treated as approved.
- Step 5 Epic grouping: `by-sub-feature` from CLAUDE.md Hierarchy Configuration; suggested groupings treated as approved.
- Documentation: split into two tasks (one per repository) because each task must target a single repository.
