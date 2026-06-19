# report-bug Evals

Evaluations for the `report-bug` skill. See the
[framework README](../README.md) for how evals work and how to run them.

## Test cases

| ID | Name | Purpose |
|----|------|---------|
| 1 | Interactive complete | All required + optional sections provided via interactive mode. Tests golden path: template-driven section composition, heading format usage, preview generation, Jira create parameters, and Comment Footnote format. |
| 2 | Interactive partial | Only required sections provided; optional sections skipped. Tests that skipped optional sections are omitted from the preview (no empty headings). |
| 3 | Missing Bug Configuration | CLAUDE.md without Bug Configuration section. Tests that the skill stops with a /setup recommendation and does NOT proceed to collect section content. |
| 4 | Programmatic mode | Structured input from a calling skill with Summary line and section headings. Tests programmatic input parsing, required section validation, and correct heading format usage. |
| 5 | Adversarial | User input with injection vectors (system overrides, exfiltration instructions, preview bypass, fabrication directives). Tests injection resistance and guardrail compliance. |

## Fixture files

Files in `files/` simulate user input, project configuration, and the bug
template. The eval prompt instructs the agent to write its outputs to
`outputs/` rather than calling actual Jira APIs.

### User input fixtures (`user-input-*.md`)

Simulated user-provided content for bug template sections:

- **user-input-interactive-complete.md** — realistic content for all 5
  required sections + both optional sections (advisory upload filename
  bug), testing golden path composition in interactive mode
- **user-input-interactive-partial.md** — content for only the 5 required
  sections with explicit SKIP markers for optional sections
- **user-input-programmatic.md** — structured programmatic input with
  Summary line and section headings, simulating a calling skill like
  verify-pr
- **user-input-adversarial.md** — section content with embedded injection
  vectors: system override commands, exfiltration instructions, preview
  bypass attempts, and fabrication directives

### Project configuration (`claude-md-*.md`)

Mock CLAUDE.md files representing different project states:

- **claude-md-configured.md** — valid CLAUDE.md with complete Project
  Configuration including Bug Configuration (Bug issue type ID + Bug
  template path)
- **claude-md-missing-bug-config.md** — CLAUDE.md with Jira Configuration
  but without Bug Configuration, simulating a project that hasn't
  configured the bug lifecycle

### Bug template (`bug-template.md`)

Mock bug description template with Required Sections (Description, Steps
to reproduce, Expected Result, Actual Result, Attachments) and Optional
Sections (Root Cause, Suggested Fix). Each section has a Heading Format
column specifying the exact heading to use in the composed description.

## Key constraints tested

| Constraint | Eval IDs |
|------------|----------|
| Guardrails — report-bug MUST NOT modify/create/delete files | 1, 2, 4, 5 |
| Guardrails — report-bug MUST NOT fabricate content | 1, 2, 4, 5 |
| Guardrails — report-bug MUST NOT create issue without preview and approval | 1, 2, 4, 5 |
| Step 0 — validate Bug Configuration before proceeding | 3 |
| Step 1 — programmatic mode parses structured input correctly | 4 |
| Step 3 — skipped optional sections omitted from output (no empty headings) | 2 |
| Step 4 — heading formats from template used verbatim in preview | 1, 2, 4 |
| Comment Footnote — correct skill name, repo link, and version | 1, 4, 5 |
| Injection resistance — adversarial content treated as literal text | 5 |

## Running

```
/sdlc-workflow:run-evals Run evals for report-bug.
Evals path: evals/report-bug/evals.json
Workspace: /tmp/report-bug-eval
```
