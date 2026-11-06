# Criterion 2 — Check 6 verifies each new symbol has a documentation comment using the language's convention

**Verdict: MET (PASS)**

## Evidence (from the PR diff, `style-conventions.md`, `#### 6b — Check Documentation Comments`)

> For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition. Use the language's standard convention:
> - **Rust:** `///` or `//!` doc comments
> - **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
> - **Python:** `"""..."""` docstrings immediately inside the function/class body
> - **Go:** `//` comment immediately preceding the symbol declaration
> - **Markdown:** not applicable — skip Markdown files
>
> Record each symbol's documentation status (documented or undocumented).

## Reasoning

- It checks every symbol: "For each new symbol identified in 6a".
- It follows each language's convention. The list matches the task's Implementation Notes exactly (`///` Rust, `/** */` Java/TypeScript, `"""` Python, `//` Go). The Rust entry also accepts `//!`, which is the right call.
- It gets placement right. Python docstrings sit *inside* the body, while the other languages put the comment *before* the definition. The text states this correctly instead of applying "immediately precedes" to every language.
- It records each result ("documented or undocumented"), which feeds the verdict in 6c.
- It matches the existing Check 3 (Test Documentation), which uses the same list of conventions. This follows the Implementation Note to "Follow the structure of existing Checks 1-5".

## Related review feedback

Reviewer comment 50001 disputes the added rule "**Markdown:** not applicable — skip Markdown files". This repository defines skills in Markdown. The task did not ask for a Markdown rule, so the exclusion does not break this criterion, which covers languages that have a doc-comment convention. The reviewer's concern is handled separately as a code change request (see `review-50001.md` and `subtask-1.md`).
