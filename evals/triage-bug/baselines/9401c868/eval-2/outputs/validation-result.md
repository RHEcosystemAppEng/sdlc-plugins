# Validation Result: Bug Description Parsing (Step 1)

## Bug Issue: ACME-501

**Summary**: API returns 500 on malformed input
**Issue Type**: Bug (ID: 10020)
**Status**: New

## Step 0 -- Configuration Validation

Configuration validated successfully from CLAUDE.md:

- **Project key**: ACME
- **Cloud ID**: mock-cloud-id-for-eval
- **Bug issue type ID**: 10020
- **Bug template path**: docs/templates/bug-template.md
- **Bug-to-Task link type**: Blocks

## Step 1 -- Issue Type Validation

The issue's type ID (10020) matches the Bug issue type ID from Bug Configuration (10020). Validation passed.

## Step 1 -- Bug Description Parsing

### Template Analysis

The bug template defines the following **Required Sections** with their heading formats:

| Section | Heading Format |
|---------|----------------|
| Description | `### **Issue Description**` |
| Steps to reproduce | `### **Steps to Reproduce**` |
| Expected Result | `### **Expected Result**` |
| Actual Result | `### **Actual Result**` |
| Environment / Version | `### **Environment / Version**` |
| Attachments | `### **Attachments**` |

The skill (Step 1) explicitly enumerates five of these as required for triage:

1. Description (mapped from "Description" row)
2. Steps to Reproduce (mapped from "Steps to reproduce" row)
3. Expected Result (mapped from "Expected Result" row)
4. Actual Result (mapped from "Actual Result" row)
5. Environment / Version (mapped from "Environment / Version" row)

The template also defines **Optional Sections**:

| Section | Heading Format |
|---------|----------------|
| Root Cause | `### **Root Cause**` |
| Suggested Fix | `### **Suggested Fix**` |

### Sections Found in Bug ACME-501 Description

| Section | Heading | Present | Content |
|---------|---------|---------|---------|
| Description | `### **Issue Description**` | YES | "The API gateway returns HTTP 500 when receiving a malformed JSON payload instead of returning a 400 Bad Request with a descriptive error message." |
| Steps to Reproduce | `### **Steps to Reproduce**` | **NO** | -- |
| Expected Result | `### **Expected Result**` | **NO** | -- |
| Actual Result | `### **Actual Result**` | YES | "HTTP 500 Internal Server Error with a stack trace in the response body." |
| Environment / Version | `### **Environment / Version**` | **NO** | -- |
| Attachments | `### **Attachments**` | YES | "None." |

### Optional Sections Found

| Section | Heading | Present |
|---------|---------|---------|
| Root Cause | `### **Root Cause**` | NO |
| Suggested Fix | `### **Suggested Fix**` | NO |

### Missing Required Sections

Three of the five required sections are missing from the bug description:

1. **Steps to Reproduce** (`### **Steps to Reproduce**`)
2. **Expected Result** (`### **Expected Result**`)
3. **Environment / Version** (`### **Environment / Version**`)

## Outcome

Per the skill's Step 1 rule:

> "If any Required Section is missing from the Bug description, list the missing sections and inform the user."

The skill would stop execution immediately with the following message:

> "Bug ACME-501 is missing required sections: Steps to Reproduce, Expected Result, Environment / Version. The bug description does not follow the template at docs/templates/bug-template.md."

**Execution halted.** The skill does not attempt to investigate an incomplete bug report. No further steps (Steps 2-7) are executed.

## Summary

The bug description parsing in Step 1 detected that ACME-501 is an incomplete bug report. While the issue has a valid Description and Actual Result, it is missing three critical sections that the triage workflow requires to proceed: Steps to Reproduce (needed for reproduction in Step 2 and reproducer test generation in Step 5), Expected Result (needed for comparison against actual behavior), and Environment / Version (needed for Affects Version resolution in Step 4.5). The skill correctly enforces the template contract by halting before any investigation begins.
