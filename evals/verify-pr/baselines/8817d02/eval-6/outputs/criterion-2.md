# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR diff adds step "6b — Check Documentation Comments" which instructs the sub-agent to verify documentation comments for each new symbol. The step provides language-specific conventions:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable — skip Markdown files

The step records each symbol's documentation status (documented or undocumented).

This satisfies the criterion — Check 6 verifies each new symbol has a documentation comment using language-specific conventions.

## Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Lines added: Section "6b — Check Documentation Comments" (diff lines 25-36)
- Five language conventions are documented with specific doc comment patterns
