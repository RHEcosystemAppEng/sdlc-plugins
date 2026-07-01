# Investigation: ACME-502 — Malformed skill output and wrong issue type

## Summary

Bug ACME-502 reports two distinct problems when running `/plan-feature`:

1. Convention references in generated task Implementation Notes use kebab-case instead of preserving the original heading case.
2. Created tasks use the Feature issue type (ID 10142) instead of the Task issue type (ID 10050).

Investigation reveals these are caused by **two independent root causes** in **different modules** affecting **independent code paths**.

---

## Root Cause 1: Malformed convention references

**Affected module:** `shared/convention-utils.md`
**Affected code path:** Convention reference formatting

The convention reference formatter in `shared/convention-utils.md` applies an incorrect case transform when generating section references from CONVENTIONS.md headings. When it encounters a heading like `## Migration Patterns`, it lowercases the text and converts spaces to hyphens, producing `migration-patterns`. The resulting Implementation Notes reference becomes `§migration-patterns` instead of the correct `§Migration Patterns`.

**Root cause:** The formatter applies a slug/kebab-case normalization (lowercase + hyphenation) to heading names. This transform is appropriate for generating URL anchors but is incorrect for producing human-readable convention references in Implementation Notes. The formatter should preserve the original heading text as-is when constructing `§`-prefixed references.

**Example:**
- Input heading: `## Migration Patterns`
- Actual output: `§migration-patterns`
- Expected output: `§Migration Patterns`

---

## Root Cause 2: Wrong issue type in task creation

**Affected module:** `plan-feature/SKILL.md` Step 6a
**Affected code path:** Jira issue creation

The task creation logic in `plan-feature/SKILL.md` Step 6a reads the **Feature issue type ID** (10142) from the project's Jira Configuration when creating task issues. It does not look up or use a Task-specific issue type ID. When the project has a custom issue type scheme where Task has its own ID (10050), the created issue is incorrectly assigned the Feature type.

**Root cause:** Step 6a hardcodes or defaults to reading the `Feature issue type ID` field from the Jira Configuration section of the project CLAUDE.md. There is no `Task issue type ID` field configured, and the logic does not distinguish between Feature and Task issue types. It should either:
- Read a dedicated `Task issue type ID` from the Jira Configuration, or
- Accept the correct issue type ID as a parameter rather than assuming the Feature ID applies to all created issues.

**Example:**
- Jira Configuration has: `Feature issue type ID: 10142`
- Project's custom scheme has: Task ID = 10050
- Actual issue type used: Feature (10142)
- Expected issue type: Task (10050)

---

## Independence of Root Causes

These two root causes are **fully independent**:

| Dimension | Root Cause 1 | Root Cause 2 |
|-----------|-------------|-------------|
| **Module** | `shared/convention-utils.md` | `plan-feature/SKILL.md` Step 6a |
| **Code path** | Convention reference formatting | Jira issue creation |
| **Symptom** | Malformed `§` references in text | Wrong issue type on created Jira issue |
| **Fix scope** | Change case transform logic | Change issue type ID lookup |
| **Can be fixed independently** | Yes | Yes |

Fixing one root cause has no effect on the other. They share no common code path, no shared state, and no causal relationship. The only connection is that both symptoms are observable in the output of a single `/plan-feature` invocation.
