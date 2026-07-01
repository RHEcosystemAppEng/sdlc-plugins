# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR diff adds step "6b -- Check Documentation Comments" which explicitly instructs checking whether a documentation comment immediately precedes each new symbol definition. It provides language-specific doc comment patterns:

- Rust: `///` or `//!` doc comments
- TypeScript/Java: `/** ... */` JSDoc/Javadoc blocks
- Python: `"""..."""` docstrings immediately inside the function/class body
- Go: `//` comment immediately preceding the symbol declaration
- Markdown: not applicable -- skip Markdown files

This satisfies the criterion of verifying each new symbol has a documentation comment using the language's convention.

## Evidence

From the PR diff, step "6b -- Check Documentation Comments" lists all five language-specific conventions and instructs recording each symbol's documentation status (documented or undocumented).
