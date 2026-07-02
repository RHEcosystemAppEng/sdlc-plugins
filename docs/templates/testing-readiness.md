# Testing Readiness Template

<!-- This template defines cross-cutting, feature-level test categories for your project.
     Place a copy of this file at docs/testing-readiness.md in your target repository.
     The plan-feature skill auto-discovers it at that path and generates one testing
     task per category for each feature.

     How it works:
     - Each ## heading defines a test category (e.g., Smoke Tests, Integration Tests).
     - Bullet points under each heading are acceptance criteria for that category.
     - plan-feature reads the headings and criteria, then creates a Jira testing task
       for each category. The task's Acceptance Criteria section is populated directly
       from the bullet points listed here.

     How to customize:
     - Add, remove, or rename ## headings to match your project's testing strategy.
     - Adjust the acceptance criteria under each heading to reflect your project's
       quality standards and infrastructure.
     - Categories are independent — you can have as few or as many as needed.

     Opt-out:
     - To disable testing task generation entirely, remove or do not create the
       docs/testing-readiness.md file in your repository. plan-feature skips testing
       task generation when the file is absent. -->

## Smoke Tests

<!-- Smoke tests validate the happy path for the feature end-to-end.
     Adjust these criteria to match your project's deployment and verification workflow. -->

- The feature's primary workflow completes successfully in a deployed environment
- No errors appear in application logs during the happy-path scenario
- The feature is accessible via its intended entry point (UI route, API endpoint, CLI command)

## Integration Tests

<!-- Integration tests verify cross-component or cross-service interactions introduced
     by the feature. Adjust these criteria based on the integration boundaries in your
     project (e.g., database, message queue, external API). -->

- Components modified by the feature interact correctly with their direct dependencies
- Data flows through the feature's full processing pipeline without corruption or loss
- Error responses from dependent services are handled gracefully (no silent failures, no crashes)

## Performance Benchmarks

<!-- Performance benchmarks ensure the feature meets response-time or throughput thresholds.
     Adjust the specific thresholds and measurement methods to match your project's SLAs
     and performance testing infrastructure. -->

- New API endpoints respond within the project's defined latency threshold under normal load
- Bulk operations or list endpoints handle the expected data volume without timeout or excessive memory use
- No measurable regression in existing endpoint response times after the feature is deployed
