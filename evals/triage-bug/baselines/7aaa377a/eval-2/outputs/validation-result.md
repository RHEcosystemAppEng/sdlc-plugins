# Triage-Bug Skill Execution: ACME-501

## Step 0 – Configuration Validation

Read `claude-md-bug-config.md` (the project CLAUDE.md). All required sections under
`# Project Configuration` are present:

| Section | Status |
|---------|--------|
| Repository Registry | PRESENT — one entry: `acme-backend` |
| Jira Configuration | PRESENT — Project key: ACME, Cloud ID: mock-cloud-id-for-eval |
| Code Intelligence | PRESENT |
| Bug Configuration | PRESENT — Bug issue type ID: 10020, Bug template path: docs/templates/bug-template.md, Bug-to-Task link type: Blocks |

Extracted values:
- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

Configuration is valid. Proceeding to Step 1.

---

## Step 1 – Fetch Bug: Bug Description Parsing

### Issue Metadata

| Field | Value |
|-------|-------|
| Key | ACME-501 |
| Summary | API returns 500 on malformed input |
| Issue Type ID | 10020 |
| Status | New |
| Labels | production-incident |
| Component | api-gateway |
| Web URL | https://mock-jira.example.com/browse/ACME-501 |
| Affects Versions | (none set) |

### Issue Type Validation

Configured Bug issue type ID: `10020`
Issue's `issuetype.id`: `10020`

**Result: MATCH** — issue is confirmed to be a Bug. Proceeding to description parsing.

### Bug Template: Required Sections

Read `bug-template-mock.md`. The template defines the following **Required Sections** and their expected heading formats:

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Environment / Version | `### **Environment / Version**` |

(Note: the template also lists `Attachments` as a Required Section, but the skill's
Step 1 maps only the five sections above as required for extraction. The `Attachments`
section is not part of the skill's required extraction list.)

### Parsing the Bug Description

The bug issue (`bug-issue-missing-sections.md`) contains the following headings:

| Heading Present in Issue | Maps To |
|--------------------------|---------|
| `### **Issue Description**` | Description (Required) |
| `### **Actual Result**` | Actual Result (Required) |
| `### **Attachments**` | Attachments (not a required extraction target) |

### Missing Required Sections

Comparing the template's required headings against the headings found in the bug
description:

| Required Section | Heading Format | Found in Issue |
|------------------|----------------|----------------|
| Description | `### **Issue Description**` | YES |
| Steps to reproduce | `### **Steps to Reproduce**` | **NO** |
| Expected Result | `### **Expected Result**` | **NO** |
| Actual Result | `### **Actual Result**` | YES |
| Environment / Version | `### **Environment / Version**` | **NO** |

**Three required sections are missing:**
1. Steps to Reproduce
2. Expected Result
3. Environment / Version

---

## Outcome: Execution Halted at Step 1

Per the skill's Step 1 guard:

> "Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result,
> Environment / Version. The bug description does not follow the template at
> docs/templates/bug-template.md."

**Execution stops immediately.** The skill does not proceed to Step 2
(Reproduce/Trace), Step 3 (Codebase Investigation), or any subsequent steps.

### Rationale

The triage-bug skill requires all five structured sections to be present before
investigation begins. Without **Steps to Reproduce**, there is no reproducible
scenario to trace. Without **Expected Result** and **Actual Result** (the latter
is present but the former is missing), the divergence between correct and incorrect
behavior cannot be formally characterized. Without **Environment / Version**, the
scope of the bug cannot be tied to a specific release.

Attempting to investigate an incomplete bug report risks producing an inaccurate
root cause analysis and a fix task with unreliable acceptance criteria. The skill's
guardrail correctly prevents this.

### Recommended Action for Reporter

The reporter of ACME-501 should update the bug description to include the three
missing sections using the required heading formats from the template at
`docs/templates/bug-template.md`:

```
### **Steps to Reproduce**
1. <step one>
2. <step two>
...

### **Expected Result**
<what should happen>

### **Environment / Version**
<product version, environment details>
```

Once all required sections are populated, re-run `/triage-bug ACME-501`.
