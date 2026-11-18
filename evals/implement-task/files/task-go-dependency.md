<!-- SYNTHETIC TEST DATA — fictional Go-module CVE task for convention-driven implementation. -->

# Mock Jira Task

**Key**: TC-9340
**Summary**: Update netparser to the fixed version
**Status**: To Do
**Labels**: ai-generated-jira, Security, CVE-2026-77123

## Repository

trustify-go

## Target Branch

main

## Description

Remediate CVE-2026-77123 in `example.com/acme/netparser`. Versions below 2.4.6
are vulnerable; version 2.4.6 is fixed. Update the dependency resolution and
verify that no vulnerable path remains.

## Files to Modify

- `go.mod` — update the affected module selection if required by the approved strategy
- `go.sum` — update resolved checksums

## Files to Create

None.

## Implementation Notes

- Ecosystem: Go modules.
- Current resolved version: 2.3.1.
- Current graph has two paths to the vulnerable version: `service -> netparser` and
  `cli -> transport -> netparser`.
- The task does not authorize edits outside `go.mod` and `go.sum`.

## Acceptance Criteria

- [ ] Every relevant resolved path selects netparser 2.4.6 or later.
- [ ] No vulnerable netparser version remains in the resolved graph.
- [ ] Existing tests pass.

## Test Requirements

- [ ] Run the project-declared verification checks after graph verification.

## Dependencies

- Depends on: CVE-2026-77123 vulnerability issue.
