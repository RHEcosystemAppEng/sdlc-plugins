# Repository Impact Map — TC-9006: Add vulnerability remediation tracking dashboard

## Inputs and run decisions (non-interactive)

- **Feature:** TC-9006, priority **Major**, fixVersions **[RHTPA 1.5.0]**
- **Figma:** no Figma URL supplied or present in the description, so Figma steps were skipped. UI is built from the textual requirements with standard PatternFly 5 components.
- **Step 1.5 (parent link):** the Feature has no parent. The prompt was skipped by default and no parent link was set.
- **Step 2.5 (issue types):** level-1 type discovered → `Epic` (hierarchyLevel 1). Type-to-role mapping:
  - Feature: Feature (ID 10142, level 2)
  - Epic: Epic (level 1)
  - Task: Task (level 0)
- **Epic grouping strategy:** `by-repository` (from Hierarchy Configuration default, as specified for this run). No prompt was shown.
- **Repository analysis:** no Serena instances are configured, so analysis used the repository structure fixtures (`repo-backend.md`, `repo-frontend.md`). Both repos have a `CONVENTIONS.md`; its documented conventions (the "Key Conventions" in the fixtures) were used for enrichment.
- **Testing readiness template:** `docs/testing-readiness.md` is not present in either repo, so no testing tasks were generated.
- **Documentation signals:** Doc Impact = **New Content**, so one documentation task was generated (Task 8).

## Impact map

```
trustify-backend:
  changes:
    - Add a `remediation` domain module (model + service) that computes severity x status counts and per-product breakdowns from existing advisory / SBOM-advisory data (no new tables)
    - Expose GET /api/v2/remediation/summary (optional product filter) and GET /api/v2/remediation/by-product (paginated)
    - Expose GET /api/v2/remediation/vulnerabilities — filterable (severity, product, status), sortable, paginated list backing the dashboard table
    - Expose GET /api/v2/remediation/trend — daily Open/In Progress/Resolved counts over a window (default 30 days) backing the progress chart
    - Mount remediation routes in server/src/main.rs; add integration tests in tests/api/remediation.rs; list endpoints in README.md

trustify-ui:
  changes:
    - Add remediation response types, REST client functions, React Query hooks, and MSW mocks/fixtures
    - Add /remediation dashboard page with product filter, summary cards (Open / In Progress / Resolved), and 30-day trend chart
    - Add filterable/sortable/paginated outstanding-vulnerability table to the dashboard, plus a Playwright E2E for UC-1/UC-2
    - Add a user guide and API reference for the dashboard and endpoints (documentation task)
```

## Excluded requirements

| Requirement | Reason |
|---|---|
| Export remediation report as CSV (Is MVP? **No**) | Deferred as non-MVP: there is no export format specification (columns, filter scoping, sync vs async for 10k rows) and no UI placement design. To plan it, the engineer needs the CSV column definition and to say whether the export should honor the active dashboard filters. It can be added as a follow-up task under the backend and UI Epics. |

## Open questions and assumptions (recorded for engineer review)

- **Remediation status source:** Open/In Progress/Resolved is assumed to come from existing SBOM-advisory correlation data (`entity/sbom_advisory.rs`). If no status column exists, Task 1 tells the implementer to stop and raise it on TC-9006 rather than add a table, because the Feature forbids new tables.
- **Trend history:** the 30-day trend (Task 4) needs historical timestamps on existing entities. If they are missing, Task 4 tells the implementer to fail explicitly and escalate rather than return a misleading flat series.
- **"Product" dimension:** assumed to come from SBOM identity in `entity/sbom.rs`.

## Workflow mode

**direct-to-main**. See `workflow-mode-decision.md`.

## Hierarchy and Epic creation (Step 6a.0)

| Epic group | Summary | Issue type | Parent | Simulated key | Tasks |
|---|---|---|---|---|---|
| trustify-backend | `TC-9006: trustify-backend` | Epic (level 1) | TC-9006 | TC-9101 | Tasks 1, 2, 3, 4 |
| trustify-ui | `TC-9006: trustify-ui` | Epic (level 1) | TC-9006 | TC-9102 | Tasks 5, 6, 7, 8 |

Epic `additional_fields` (both Epics):
```json
{ "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```

## Tasks

| # | Summary | Repository | Parent Epic | Simulated key | Depends on |
|---|---|---|---|---|---|
| 1 | Remediation aggregation model and service | trustify-backend | TC-9101 (TC-9006: trustify-backend) | TC-9103 | — |
| 2 | Remediation summary and by-product endpoints | trustify-backend | TC-9101 (TC-9006: trustify-backend) | TC-9104 | 1 |
| 3 | Remediation vulnerability list endpoint | trustify-backend | TC-9101 (TC-9006: trustify-backend) | TC-9105 | 1, 2 |
| 4 | Remediation trend endpoint | trustify-backend | TC-9101 (TC-9006: trustify-backend) | TC-9106 | 1, 2 |
| 5 | Remediation API client and hooks | trustify-ui | TC-9102 (TC-9006: trustify-ui) | TC-9107 | 2, 3, 4 |
| 6 | Remediation dashboard page | trustify-ui | TC-9102 (TC-9006: trustify-ui) | TC-9108 | 5 |
| 7 | Remediation vulnerability table | trustify-ui | TC-9102 (TC-9006: trustify-ui) | TC-9109 | 5, 6 |
| 8 | Remediation dashboard documentation | trustify-ui | TC-9102 (TC-9006: trustify-ui) | TC-9110 | 2, 3, 4, 6, 7 |

Backend tasks (1–4) are numbered before the frontend tasks (5–8) that depend on them.

Task `additional_fields` (all 8 tasks), with `parent` set to the Epic key listed above:
```json
{ "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```
- priority: **Major** is inherited from the Feature (it is set and not "Undefined").
- fixVersions: **RHTPA 1.5.0** is inherited, because the Feature's fixVersions is non-empty and `fixVersion scope: both`.

## Links (Step 6b)

**Incorporates** links go from the Feature to each Epic only, not to individual Tasks. Tasks inherit the hierarchy through their Epic parent:
- TC-9006 incorporates TC-9101 (TC-9006: trustify-backend)
- TC-9006 incorporates TC-9102 (TC-9006: trustify-ui)

**Depend** links (inward = dependent, outward = dependency):
- TC-9104 → TC-9103
- TC-9105 → TC-9103, TC-9104
- TC-9106 → TC-9103, TC-9104
- TC-9107 → TC-9104, TC-9105, TC-9106
- TC-9108 → TC-9107
- TC-9109 → TC-9107, TC-9108
- TC-9110 → TC-9104, TC-9105, TC-9106, TC-9108, TC-9109

## Description digests

| Task | Digest |
|---|---|
| 1 | sha256-md:6071aa1f100b6f95cce1f0999396644dc439049695b5b149ecbdb7aa83a77ec2 |
| 2 | sha256-md:54a9a76ccf7874358f40d19c9f4913e02bc6725b9b0ab6f8b3db7757ae831234 |
| 3 | sha256-md:ec35efd71c6a6c536c00bb5a8c88849f6069a0dbec27ee150bdeabc09400ee5b |
| 4 | sha256-md:8a31421037e11f0a896ca0ed7905c3948a3ab38ddf6ccf132a29150cde5aac1a |
| 5 | sha256-md:d3971443467c4f6034c1a5faaf6336ab5ee33032eb7aea11af4a3b500b8b5cc4 |
| 6 | sha256-md:a599b53e4e84a33a403b93cc3ac86ecd49ed8bfe2bcb472c412d7d1d0660df91 |
| 7 | sha256-md:a617b47ebf2caa11b9cd87bd1f488e27fa74310cb42ff4154e026e479582a731 |
| 8 | sha256-md:a0491e3b95c38970a86ea8918e63cfc600cb1842a8470391dcae4ed6b463b647 |

Digests were computed with `scripts/sha256-digest.py` over the markdown task description files. In a live run they would be computed from the description re-fetched from Jira.
