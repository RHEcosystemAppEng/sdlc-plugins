# Repository Impact Map — TC-9002: Improve search experience

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. The search improvements (full-text indexing, relevance tuning, filters) are independent, incremental changes. Each task's PR can merge to `main` without breaking existing functionality — the search module already exists and these are additive improvements to it.

## trustify-backend

changes:
  - Add full-text search indexes to PostgreSQL for SBOM, advisory, and package entities to improve query performance
  - Refactor SearchService to use full-text search queries instead of LIKE/ILIKE patterns for improved relevance
  - Add filter parameters (entity type, severity, date range) to the search endpoint
  - Add integration tests for the improved search functionality

## Ambiguities Identified

The following ambiguities in the Feature description require clarification before implementation:

1. **No performance targets specified.** "Search should be faster" and "Should be fast enough" provide no quantitative benchmarks. **Assumption (pending clarification):** Target p95 response time of <500ms for search queries. This assumption is used for acceptance criteria but should be validated with stakeholders.

2. **No relevance criteria defined.** "Results should be more relevant" does not define what relevance means — keyword matching, fuzzy matching, ranking algorithm, field weighting. **Assumption (pending clarification):** Implement PostgreSQL full-text search (`tsvector`/`tsquery`) with field weighting (title > description > content) as the relevance improvement. Exact ranking weights need stakeholder input.

3. **Filter types not specified.** "Add filters — Some kind of filtering capability" does not enumerate which fields should be filterable. **Assumption (pending clarification):** Add filters for entity type (SBOM, advisory, package), severity (for advisories), and date range (created/modified). Additional filters may be needed after clarification.

4. **No definition of "don't break existing functionality."** The non-functional requirement is too vague to verify. **Assumption (pending clarification):** Existing search API contract (endpoint path, response shape) is preserved — new parameters are additive, not breaking.

5. **Missing search indexing scope.** The feature does not specify which entity fields should be indexed for full-text search. **Assumption (pending clarification):** Index name/title, description, and identifier fields for each entity type.

## Excluded Requirements

- **"Better UI" (Non-MVP):** Cannot be planned without design mockups or a frontend repository. The Repository Registry only includes `trustify-backend`. UI improvements require a Figma design and a frontend repository manifest to decompose into actionable tasks. This requirement is excluded from the current plan scope.

## Inherited Field Propagation

- **Priority:** Normal — will be propagated to all created tasks via `additional_fields.priority`
- **Fix Versions:** RHTPA 1.6.0 — will be propagated to all created tasks via `additional_fields.fixVersions` (fixVersion scope defaults to "both" since no `### Jira Field Defaults` section is configured)
