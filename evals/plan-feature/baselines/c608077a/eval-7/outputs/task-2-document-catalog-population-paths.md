# Task 2 — Document Service Catalog population paths and the ownerGroup contract

**Summary**: TC-9007: Document Service Catalog population paths and the ownerGroup contract
**Issue type**: Task
**Parent (Epic)**: E1 — TC-9007: Service Catalog ownerGroup
**Labels**: ai-generated-jira
**Priority**: Major (inherited from TC-9007)
**fixVersions**: omitted (TC-9007 has none)

---

## Repository
catalog-service

## Target Branch
main

## Description
Update the existing documentation to reflect the `ownerGroup` field added to Service Catalog records in TC-9007.

- **Doc impact type**: Updates to existing content.
- **What changed**: Service Catalog records now carry an `ownerGroup`. The summary API and the downloadable report show it. The same `ownerGroup` contract applies whichever workflow populates the record:
  - A supplied value is used.
  - On update, the existing value is kept unless a new one is supplied.
  - A newly created record with no supplied value gets the documented default (`unassigned`, pending stakeholder confirmation).
- **Population paths to document**: initial registration (onboarding), scheduled provider synchronization, fallback import of previously exported data (used when provider sync is unavailable), and operator-requested on-demand refresh (`POST /api/catalog/refresh`, which accepts an optional `ownerGroup`).
- **Audience and purpose**: operators and API consumers need to know that all four paths use the same catalog contract. They also need to know that `ownerGroup` is shown for every record whichever path populated it.
- **Reference**: Feature TC-9007, "Documentation Considerations" section.

## Acceptance Criteria
- [ ] The documentation lists all four population paths: registration, scheduled sync, fallback import, and on-demand refresh.
- [ ] The documentation states that all paths share one catalog record contract, including the `ownerGroup` rules (supplied value, preserve-on-update, default on create).
- [ ] The documentation describes `ownerGroup` in the summary API response and in the downloadable report.
- [ ] The documentation describes the optional `ownerGroup` parameter on `POST /api/catalog/refresh`.

## Test Requirements
- [ ] Check each documented population path and `ownerGroup` rule against the behavior merged in Task 1, including the final default value the stakeholder confirmed.
- [ ] Check that the documented summary API field and report column match the implemented names and formats.

## Dependencies
- Depends on: Task 1 — Add ownerGroup to the shared Service Catalog record across all population paths and consumers
