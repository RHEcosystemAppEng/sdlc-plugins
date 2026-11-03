# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

**Verdict: PASS**

## Evidence

Sub-step `#### 6b — Check Documentation Comments`:

> For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition. Use the language's standard convention:
> - **Rust:** `///` or `//!` doc comments
> - **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
> - **Python:** `"""..."""` docstrings immediately inside the function/class body
> - **Go:** `//` comment immediately preceding the symbol declaration
> - **Markdown:** not applicable — skip Markdown files
>
> Record each symbol's documentation status (documented or undocumented).

## Reasoning

- The check runs per symbol ("For each new symbol identified in 6a").
- Every language pattern required by the task's Implementation Notes (`///` Rust, `/** */` Java/TypeScript, `"""` Python, `//` Go) is listed. Rust's `//!` is added correctly.
- Python placement is right: the docstring sits inside the body, not before the definition, even though the 6b lead sentence says "immediately precedes".
- Each symbol's status is recorded, which feeds the verdict in 6c.

## Related review feedback

Reviewer-b's comment 50001 disputes the "Markdown: not applicable" exclusion. That is a request to extend the check beyond the criterion, and it is tracked as a separate review-feedback sub-task. It does not make this criterion fail, because the criterion asks only for "the language's convention" for doc comments, and Markdown has no doc-comment convention.
