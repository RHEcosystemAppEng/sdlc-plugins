# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR diff adds step **6b — Check Documentation Comments** to Check 6 in `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. This step specifies:

> For each new symbol identified in 6a, check whether a documentation comment
> immediately precedes the definition. Use the language's standard convention:
>
> - **Rust:** `///` or `//!` doc comments
> - **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
> - **Python:** `"""..."""` docstrings immediately inside the function/class body
> - **Go:** `//` comment immediately preceding the symbol declaration
> - **Markdown:** not applicable — skip Markdown files

This directly satisfies the criterion. The check verifies documentation presence using language-specific conventions for five language categories. Each convention pattern is specified concretely (e.g., `///` for Rust, `/** */` for Java/TypeScript), and the step records each symbol's documentation status.

## Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Diff lines adding step 6b (lines 25-36 of the diff hunk)
- Five language-specific doc comment patterns defined
- Per-symbol documentation status recording specified
