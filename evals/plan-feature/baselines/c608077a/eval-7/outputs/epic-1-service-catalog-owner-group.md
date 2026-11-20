# Epic E1 — TC-9007: Service Catalog ownerGroup

**Issue type**: Epic (assumed level-1 type; Step 2.5 discovery not possible offline)
**Parent**: TC-9007
**Labels**: ai-generated-jira
**Priority**: Major (inherited)
**fixVersions**: omitted (Feature has none)
**Grouping strategy**: by-sub-feature (from CLAUDE.md Hierarchy Configuration). The feature has a single sub-feature, so one Epic. The user's approval of this grouping is assumed.

## Description (plain text)

Adds an ownerGroup field to the shared Service Catalog record. The field is applied the same way across all four population paths (registration, scheduled sync, fallback import, on-demand refresh) and shown in the summary API and the downloadable report. The Epic contains two tasks:
- Task 1: the implementation across the store, the four writers, the two consumers, and their tests.
- Task 2: documentation of the population paths and the ownerGroup contract.
