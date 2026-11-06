# Step 1 – Fetch Bug: ACME-500

## Step 0 – Configuration (from claude-md-bug-config.md)

| Item | Value |
|---|---|
| Project key | ACME |
| Cloud ID | mock-cloud-id-for-eval |
| Bug issue type ID | 10020 |
| Bug template path | docs/templates/bug-template.md (eval: bug-template-mock.md) |
| Bug-to-Task link type | Blocks |
| Repository Registry | acme-backend (Serena instance `serena_backend`, path `/home/dev/repos/acme-backend`) |
| Code Intelligence | No Serena MCP servers configured, so the fallback is Read/Grep/Glob |

All required configuration sections exist, so the skill continues.

## Issue Type Validation

- Issue `issuetype.id`: **10020** (Bug)
- Configured Bug issue type ID: **10020**
- Result: **MATCH**. ACME-500 is a Bug, so triage continues.

## Extracted Metadata

| Field | Value |
|---|---|
| Issue key | ACME-500 |
| webUrl | https://mock-jira.example.com/browse/ACME-500 |
| Summary | plan-feature silently drops conventions when CONVENTIONS.md has trailing whitespace |
| Status | New |
| Labels | reported-by-user |
| Component | sdlc-workflow |
| **Affects Version/s** | **0.9.0** |
| **affectsVersions already populated?** | **YES**: the `versions` field holds 1 value (`0.9.0`). Step 4.5.1 must show this value and ask the user whether to Keep, Replace, or Augment it. The skill must not overwrite it silently. |

## Parsed Description Sections (heading formats from bug-template-mock.md)

### Required Sections

| Section | Template heading | Found? |
|---|---|---|
| Description | `### **Issue Description**` | Yes |
| Steps to Reproduce | `### **Steps to Reproduce**` | Yes |
| Expected Result | `### **Expected Result**` | Yes |
| Actual Result | `### **Actual Result**` | Yes |
| Environment / Version | `### **Environment / Version**` | **No** (no heading in the description) |
| Attachments | `### **Attachments**` | Yes ("None.") |

#### Description
When `CONVENTIONS.md` has trailing whitespace on heading lines (for example, `## Migration Patterns  `), the plan-feature skill's convention conformance analysis does not match the heading and skips the convention without notice. No warning is logged. The generated task description leaves out the convention that should have been included.

#### Steps to Reproduce
1. Create a `CONVENTIONS.md` file with a convention section whose heading has trailing whitespace:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
2. Run `/plan-feature ACME-100` on a feature that needs a database migration with foreign keys.
3. Inspect the generated task's Implementation Notes.

#### Expected Result
The generated task's Implementation Notes should include:
> Per CONVENTIONS.md §Migration Patterns: add `Index::create()` for all FK columns.

#### Actual Result
The generated task's Implementation Notes do NOT reference the Migration Patterns convention. No warning or error appears; the convention is dropped without notice.

#### Environment / Version
*(Section not present in the description.)* The only version information is the Jira **Affects Version/s** field: `0.9.0`.

#### Attachments
None.

### Optional Sections

| Section | Present? |
|---|---|
| Root Cause | No |
| Suggested Fix | No |

## Validation Note: Environment / Version Section

The template lists `### **Environment / Version**` as a Required Section, and the ACME-500 description has no such heading. Read literally, Step 1's stop rule would halt triage with:

> "Bug ACME-500 is missing required sections: Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

For this eval run, triage continued for these reasons:
- The four core sections that drive investigation (Description, Steps to Reproduce, Expected Result, Actual Result) are all present and complete.
- The version information that section would hold is already on the issue as the structured **Affects Version/s = 0.9.0** field. This is the case Step 4.5.1 is designed to handle.
- The eval scenario explicitly asks for the Step 4.5 existing-value handling and the downstream outputs.

In a live run, the agent should tell the user about the missing section, for example by asking the reporter to add an `### **Environment / Version**` section. It would then proceed only with user agreement.
