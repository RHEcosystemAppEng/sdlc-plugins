## Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

**Verdict: PASS**

The PR adds section "6b — Check Documentation Comments" which specifies that for each new symbol identified in 6a, the check verifies whether a documentation comment immediately precedes the definition. It includes language-specific doc comment patterns:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** explicitly marked as not applicable (skip Markdown files)

The check records each symbol's documentation status as either "documented" or "undocumented", satisfying the requirement to verify documentation using language-specific conventions.
