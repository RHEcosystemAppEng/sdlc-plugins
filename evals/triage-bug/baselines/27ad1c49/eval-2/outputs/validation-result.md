# Validation Result -- Step 1: Bug Description Parsing

## Issue

**Key**: ACME-501
**Summary**: API returns 500 on malformed input

## Bug Template Reference

Bug template path (from Bug Configuration): `docs/templates/bug-template.md`

## Required Sections Check

The bug description was parsed against the required section headings defined in the bug template. The five required sections per the triage-bug skill (Step 1) are:

| # | Required Section       | Template Heading Format          | Present in ACME-501? |
|---|------------------------|----------------------------------|----------------------|
| 1 | Description            | `### **Issue Description**`      | Yes                  |
| 2 | Steps to Reproduce     | `### **Steps to Reproduce**`     | **No -- MISSING**    |
| 3 | Expected Result        | `### **Expected Result**`        | **No -- MISSING**    |
| 4 | Actual Result          | `### **Actual Result**`          | Yes                  |
| 5 | Environment / Version  | `### **Environment / Version**`  | **No -- MISSING**    |

## Sections Present (2 of 5)

1. **Description** (`### **Issue Description**`): Contains content describing the API gateway returning HTTP 500 on malformed JSON payloads.
2. **Actual Result** (`### **Actual Result**`): Contains content stating "HTTP 500 Internal Server Error with a stack trace in the response body."

## Sections Missing (3 of 5)

1. **Steps to Reproduce** -- No `### **Steps to Reproduce**` heading found in the bug description. There are no instructions for how to trigger the bug.
2. **Expected Result** -- No `### **Expected Result**` heading found in the bug description. There is no statement of what the correct behavior should be.
3. **Environment / Version** -- No `### **Environment / Version**` heading found in the bug description. There is no information about the environment or software version where the bug was observed.

## Outcome

**STOP -- Validation failed.** Three required sections are missing.

Per the triage-bug skill Step 1 rule: "If any Required Section is missing from the Bug description, list the missing sections and inform the user... Stop execution immediately. Do not attempt to investigate an incomplete bug report."

The skill would output the following message and halt:

> Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result, Environment / Version. The bug description does not follow the template at `docs/templates/bug-template.md`.

No further steps (investigation, root cause analysis, task creation) are performed. The skill stops at Step 1.
