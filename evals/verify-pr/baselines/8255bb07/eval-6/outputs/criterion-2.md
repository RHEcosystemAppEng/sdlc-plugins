## Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

### Verdict: PASS

### Reasoning

The PR diff adds step **6b -- Check Documentation Comments** to the new Check 6
section in `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. This
step explicitly instructs the sub-agent to:

> For each new symbol identified in 6a, check whether a documentation comment
> immediately precedes the definition. Use the language's standard convention.

The step then enumerates language-specific doc comment patterns:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

The check correctly requires per-symbol verification using the appropriate
language convention, and records each symbol's documentation status (documented
or undocumented).

### Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Diff lines: the new step 6b section (lines 25-36 of the added block)
- Five language-specific patterns are defined, plus a Markdown exclusion rule
