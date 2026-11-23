# Criterion 4: Check 6 produces WARN when any new symbol lacks documentation

**Verdict: PASS**

## Evidence (PR diff, `style-conventions.md`, 6c)

- `+- **WARN** — at least one new symbol lacks a documentation comment`
- `+Evidence: list of undocumented symbols with file path and line number.`

## Reasoning

WARN fires when at least one new symbol is undocumented ("any"), as the criterion requires. The evidence rule makes the check list each undocumented symbol with its file and line. That covers the Test Requirement "correctly identifies undocumented new symbols in a diff".
