## Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

### Verdict: PASS

### Reasoning

The PR diff adds step "6b -- Check Documentation Comments" to `style-conventions.md`, which describes checking for documentation comments using language-specific conventions:

> For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition. Use the language's standard convention:
> - Rust: `///` or `//!` doc comments
> - TypeScript/Java: `/** ... */` JSDoc/Javadoc blocks
> - Python: `"""..."""` docstrings immediately inside the function/class body
> - Go: `//` comment immediately preceding the symbol declaration
> - Markdown: not applicable -- skip Markdown files

This covers the major languages with their standard doc comment patterns. Each symbol's documentation status is recorded as documented or undocumented.

### Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Added lines: Step 6b lists 5 language-specific doc comment conventions
- The check operates per-symbol, verifying each one individually
