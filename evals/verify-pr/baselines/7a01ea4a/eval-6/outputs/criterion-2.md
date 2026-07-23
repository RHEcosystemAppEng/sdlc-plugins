# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR adds step **6b -- Check Documentation Comments** to the new Check 6 section in `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. This step explicitly describes verifying documentation comments for each new symbol identified in step 6a:

> For each new symbol identified in 6a, check whether a documentation comment
> immediately precedes the definition. Use the language's standard convention:

The step provides language-specific doc comment patterns covering the major languages:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

The step also specifies recording each symbol's documentation status: "Record each symbol's documentation status (documented or undocumented)."

This satisfies the criterion: Check 6 verifies each new symbol has a documentation comment using language-specific conventions covering all the standard languages encountered in typical projects.
