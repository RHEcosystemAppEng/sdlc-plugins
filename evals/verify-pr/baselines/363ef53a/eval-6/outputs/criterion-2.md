# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR diff adds step "#### 6b -- Check Documentation Comments" to
`plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. This step
instructs the sub-agent to:

> For each new symbol identified in 6a, check whether a documentation comment
> immediately precedes the definition. Use the language's standard convention:

The step then lists language-specific doc comment patterns:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

The check records each symbol's documentation status (documented or
undocumented), providing per-symbol tracking that feeds into the verdict.

This satisfies the criterion: the check verifies documentation comments for
each new symbol using language-specific conventions. The coverage spans the
major languages relevant to the repository ecosystem (Rust, TypeScript, Java,
Python, Go).
