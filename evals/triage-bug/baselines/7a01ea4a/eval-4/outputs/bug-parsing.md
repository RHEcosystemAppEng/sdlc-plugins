# Step 1 -- Bug Parsing

## Configuration Validation (Step 0)

Extracted from CLAUDE.md (`claude-md-bug-config.md`):

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Issue Type Validation

Issue type ID on ACME-510 is `10020` (Bug), which matches the Bug issue type ID `10020` from Bug Configuration. Validation passes.

## Metadata

- **Issue key**: ACME-510
- **Web URL**: https://mock-jira.example.com/browse/ACME-510
- **Summary**: API response missing pagination headers when filtering by date range
- **Status**: New
- **Labels**: reported-by-user
- **Component**: sdlc-workflow
- **Affects Version/s**: (none) -- field is empty, not populated with any values

## Parsed Description Sections

### Required Sections

All required sections are present per the bug template (`docs/templates/bug-template.md`).

#### Issue Description

When calling the `/api/v2/advisories` endpoint with `filterDateRange` query parameters,
the response is missing the `X-Total-Count` and `Link` pagination headers. The response
body contains the correct filtered results, but clients relying on pagination headers
cannot determine total pages.

#### Steps to Reproduce

1. Start the backend service locally.
2. Call `GET /api/v2/advisories?publishedAfter=2025-01-01&publishedBefore=2025-06-30&limit=10`.
3. Inspect the response headers.

#### Expected Result

The response should include:
- `X-Total-Count: <n>` header with the total number of matching advisories
- `Link: <url>; rel="next"` header when more pages exist

#### Actual Result

The response body contains the correct filtered advisories, but the `X-Total-Count`
and `Link` headers are absent. Non-filtered requests (without `publishedAfter`/`publishedBefore`)
return pagination headers correctly.

#### Environment / Version

Product version: 0.9.0
OS: RHEL 9.2
Deployment: OpenShift 4.14

### Optional Sections

#### Root Cause

Not present in the bug description.

#### Suggested Fix

Not present in the bug description.

#### Attachments

None.
