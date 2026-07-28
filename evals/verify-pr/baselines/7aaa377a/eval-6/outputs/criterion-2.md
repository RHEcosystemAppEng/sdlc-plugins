# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR diff adds section "6b -- Check Documentation Comments" to `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. This section instructs the sub-agent to:

> For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition. Use the language's standard convention.

It then lists language-specific doc comment patterns:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

The section concludes with: "Record each symbol's documentation status (documented or undocumented)."

This directly satisfies the criterion. Each new symbol is checked for a documentation comment using the language's standard convention, with explicit per-language patterns defined.

## Evidence

Lines 25-37 of the added content in `style-conventions.md` define step 6b with language-specific doc comment conventions and verification instructions.
