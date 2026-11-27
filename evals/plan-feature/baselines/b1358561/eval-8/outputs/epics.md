# Epics — TC-9007 (by-sub-feature grouping)

Grouping strategy: `by-sub-feature`, the default in CLAUDE.md Hierarchy Configuration. Step 2.5 issue-type discovery could not run against Jira in this offline eval. This plan assumes the TC project has a level-1 "Epic" type. If it does not, the tasks are created directly under TC-9007 and these Epics are skipped.

Each Epic gets labels `ai-generated-jira`, parent TC-9007, priority Major (inherited) and no fixVersions (the Feature has none).

## Epic A — "TC-9007: Owner group onboarding"
Adds the `ownerGroup` field to the shared Service Catalog record schema with update-preservation semantics, and collects it during initial registration.
- Task 1: Add ownerGroup to the shared Service Catalog record schema
- Task 2: Collect ownerGroup during initial service registration

## Epic B — "TC-9007: Owner group display"
Exposes `ownerGroup` in the catalog summary API and the downloadable report, and documents the field.
- Task 3: Expose ownerGroup in the catalog summary API
- Task 4: Include ownerGroup in the downloadable catalog report
- Task 5: Document ownerGroup in the Service Catalog record contract

Links: TC-9007 "Incorporates" Epic A and Epic B. "Depend" links: Task 2 depends on Task 1; Tasks 3 and 4 each depend on Tasks 1 and 2; Task 5 depends on Tasks 1–4.
