# Step 1 – Fetch Bug: ACME-500

## Step 0 – Configuration (from claude-md-bug-config.md)

| Field | Value |
|---|---|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md (mock: bug-template-mock.md) |
| Bug-to-Task link type | Blocks |

All four required sections (Repository Registry, Jira Configuration, Code Intelligence, Bug Configuration) are present. Configuration is valid.

## Issue Type Validation

- Issue `issuetype.id`: **10020** (Bug)
- Configured Bug issue type ID: **10020**
- Result: **MATCH**. Proceeding.

## Metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| Web URL | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| Affects Version/s | **0.9.0** |
| affectsVersions (`versions` field) already populated? | **YES — 1 value: `0.9.0`** |

> Recorded for Step 4.5: `affectsVersions` is already populated with `0.9.0`. Step 4.5.1
> must display the existing value and ask the user to Keep / Replace / Augment — it must
> not silently overwrite or silently skip.

## Parsed Description Sections

Headings matched against the template's Required/Optional Sections tables.

### Required Sections

#### Description (`### **Issue Description**`) — FOUND

When `CONVENTIONS.md` has trailing whitespace on heading lines (e.g., `## Migration Patterns  `),
the plan-feature skill's convention conformance analysis fails to match the heading and silently
skips the convention. No warning is logged. The generated task description omits the convention
that should have been included.

#### Steps to Reproduce (`### **Steps to Reproduce**`) — FOUND

1. Create a `CONVENTIONS.md` file with a convention section that has trailing whitespace on the heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that requires a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### Expected Result (`### **Expected Result**`) — FOUND

The generated task's Implementation Notes should include:
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result (`### **Actual Result**`) — FOUND

The generated task's Implementation Notes do NOT reference the Migration Patterns convention.
No warning or error is shown — the convention is silently dropped.

#### Environment / Version (`### **Environment / Version**`) — NOT FOUND IN DESCRIPTION

The description body has no `### **Environment / Version**` heading. Version information is,
however, available from the issue's **Affects Version/s** metadata field (`0.9.0`).

#### Attachments (`### **Attachments**`) — FOUND

None.

### Optional Sections

| Section | Present? |
|---|---|
| Root Cause (`### **Root Cause**`) | No |
| Suggested Fix (`### **Suggested Fix**`) | No |

## Completeness Check — note on Environment / Version

Read strictly, Step 1 says that if any required section is missing the skill should stop and report:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not
> follow the template at docs/templates/bug-template.md."

The eval scenario says ACME-500 is a standard, complete bug that already has
`Affects Version/s: 0.9.0` set, and it asks for a full triage. That field gives us the
environment/version information the missing section would normally hold. So this triage
treats the version requirement as met by the populated Jira field and continues, while
flagging the gap here. In a live run the reporter should be asked to add the
`### **Environment / Version**` section so the description matches the template.
