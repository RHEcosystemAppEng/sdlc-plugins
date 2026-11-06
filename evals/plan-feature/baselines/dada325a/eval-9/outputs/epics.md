# Epics (by-sub-feature, from CLAUDE.md Hierarchy Configuration)

Labels: ai-generated-jira · Priority: Major (inherited) · fixVersions: omitted (Feature has none) · Parent: TC-9008

## Epic A — TC-9008: Tracker service-account authentication
Switches tracker access to the service-account token sent through the tracker API gateway and adds a positive authentication proof to the tracker client. Tasks: Task 1.

## Epic B — TC-9008: Fail-closed verification gate
Gates verification on linked issues in "Ready for Verification" state and makes the gate and pre-verify wrapper fail closed when tracker authentication is not proven, instead of treating an empty search as a skip. Tasks: Task 2, Task 3.

## Links
- TC-9008 incorporates Epic A, Epic B
- Task 2 depends on Task 1
- Task 3 depends on Task 2
