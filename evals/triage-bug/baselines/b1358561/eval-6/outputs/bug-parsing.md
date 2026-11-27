# Step 1 – Bug Parsing: ACME-500

## Step 0 – Configuration (from claude-md-bug-config.md)

| Field | Value |
|---|---|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md (mocked by bug-template-mock.md) |
| Bug-to-Task link type | Blocks |

Repository Registry, Jira Configuration, Code Intelligence and Bug Configuration sections are all present -> validation passed.

## Issue type validation

- Issue `issuetype.id` = **10020** (Bug); configured Bug issue type ID = **10020** -> match, proceed.

## Metadata

| Field | Value |
|---|---|
| Key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | **0.9.0** |
| affectsVersions already populated? | **Yes** — one value (`0.9.0`). Step 4.5 must offer keep / replace / augment instead of auto-setting. |

## Parsed sections (matched against template heading formats)

### Required Sections

| Section | Template heading | Found | Content |
|---|---|---|---|
| Description | `### **Issue Description**` | Yes | When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `), plan-feature's convention conformance analysis fails to match the heading and silently skips the convention. No warning is logged. The generated task description omits the convention that should have been included. |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes | 1. Create a `CONVENTIONS.md` with a heading that has trailing whitespace: `## Migration Patterns  ` followed by `Add Index::create() for all FK columns.` 2. Run `/plan-feature ACME-100` on a feature requiring a DB migration with foreign keys. 3. Inspect the generated task's Implementation Notes. |
| Expected Result | `### **Expected Result**` | Yes | Implementation Notes include: "Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns." |
| Actual Result | `### **Actual Result**` | Yes | Implementation Notes do NOT reference the Migration Patterns convention. No warning or error — the convention is silently dropped. |
| Environment / Version | `### **Environment / Version**` | **No heading in description** | Not present in the description body. The version information is instead carried by the issue's `Affects Version/s` field (`0.9.0`). |
| Attachments | `### **Attachments**` | Yes | None. |

### Optional Sections

| Section | Found | Content |
|---|---|---|
| Root Cause | No | — |
| Suggested Fix | No | — |

## Parsing note — Environment / Version

Strictly, the skill says a missing required section should stop triage. Here the version data the section is supposed to supply is already in the structured `Affects Version/s` field (0.9.0), and all behavioural sections (Description, Steps, Expected, Actual) are complete. Triage continues on that basis for this eval. In a live run the user would be told: "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md." They would then be asked to add the section, or to confirm that the Affects Version field is enough.
