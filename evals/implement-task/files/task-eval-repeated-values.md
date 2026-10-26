<!-- SYNTHETIC TEST DATA — mock task, proposed eval assertion, and repeated image-row values for assertion/fixture consistency testing. -->

# Mock Jira Task

## Repository

sdlc-plugins

## Target Branch

main

## Description

Add eval coverage for the CPE requirement in a Container Images table.

## Files to Modify

- `evals/setup/evals.json` — add an assertion for the CPE requirement using the supplied fixture.

## Files to Create

None.

## API Changes

N/A.

## Acceptance Criteria

- Every image row includes a non-empty CPE value.

## Test Requirements

- Add the eval assertion: “Every image row has a CPE, and every CPE value is unique across all rows.”

## Supplied Fixture Values

| Product Version | Component | CPE |
|---|---|---|
| 2.1.0 | api-rhel9 | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
| 2.1.0 | api-rhel10 | `cpe:2.3:a:example:trustify_api:2.1.0:*:*:*:*:*:*:*` |
