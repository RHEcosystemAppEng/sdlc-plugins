# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR diff adds step 6b ("Check Documentation Comments") to `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. This step explicitly instructs:

> "For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition."

It provides language-specific doc comment conventions:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable — skip Markdown files

The step concludes with: "Record each symbol's documentation status (documented or undocumented)."

This satisfies the criterion — Check 6 verifies documentation comments using language-appropriate conventions.
