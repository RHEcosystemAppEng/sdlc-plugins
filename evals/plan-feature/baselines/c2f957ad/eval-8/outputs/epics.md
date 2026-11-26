# Epics (by-sub-feature grouping)

Assumed level-1 type: `Epic` (Jira issue types could not be queried in this offline run). Each Epic is created with parent = TC-9007, labels `ai-generated-jira`, priority `Major`, and no fixVersions (the Feature has none).

## Epic A
- **Summary:** TC-9007: Owner group data model and onboarding
- **Description:** Adds the optional `ownerGroup` field and preserve-on-update semantics to the shared Service Catalog store, and collects `ownerGroup` during onboarding registration. Tasks: Task 1 (store schema), Task 2 (registration).

## Epic B
- **Summary:** TC-9007: Owner group display and documentation
- **Description:** Shows `ownerGroup` in the catalog summary API and the downloadable report, and documents the field. Tasks: Task 3 (summary API), Task 4 (report), Task 5 (documentation).

## Links
- Feature TC-9007 "incorporates" Epic A and Epic B
- Task 2 depends on Task 1; Task 3 depends on Task 1; Task 4 depends on Task 1; Task 5 depends on Tasks 1–4
