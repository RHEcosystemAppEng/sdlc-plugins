# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The diff adds step "6b -- Check Documentation Comments" to `style-conventions.md`. This step instructs:

> For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition. Use the language's standard convention.

It then enumerates language-specific doc comment patterns:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

Each symbol's documentation status is recorded as "documented or undocumented."

This satisfies the criterion. The check verifies each new symbol has a documentation comment using the language's standard convention, with explicit per-language rules.
