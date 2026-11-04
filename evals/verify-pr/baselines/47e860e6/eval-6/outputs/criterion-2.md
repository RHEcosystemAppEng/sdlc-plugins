# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

**Verdict: PASS**

## What was checked
Sub-step `#### 6b — Check Documentation Comments` in the added Check 6. I compared it with the task's Implementation Notes: "`///` for Rust, `/** */` for Java/TypeScript, `"""` for Python, `//` for Go".

## Evidence
6b says: "For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition. Use the language's standard convention:"
- **Rust:** `///` or `//!` doc comments. Matches the notes, and adds the inner-doc `//!` form.
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks. Matches.
- **Python:** `"""..."""` docstrings *inside* the function/class body. Matches, and correctly notes that Python docstrings follow the definition rather than precede it.
- **Go:** `//` comment immediately preceding the declaration. Matches.
- **Markdown:** "not applicable — skip Markdown files"

6b ends with "Record each symbol's documentation status (documented or undocumented)." Each symbol is checked one by one.

## Notes
- Every language in the Implementation Notes is covered, with the correct convention for each.
- Review comment **50001** (reviewer-b) objects to the Markdown exclusion in this sub-step. It argues that in this Markdown-first repository, new `###` sections should need introductory text. The task does not require Markdown handling, so the criterion is still met. The review comment is handled as a code change request in its own sub-task (see review-50001.md and subtask-1.md).
