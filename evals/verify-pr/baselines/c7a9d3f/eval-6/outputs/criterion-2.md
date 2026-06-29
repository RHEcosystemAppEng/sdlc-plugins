## Acceptance Criterion 2

**Criterion:** Check 6 verifies each new symbol has a documentation comment using the language's convention

**Verdict:** PASS

**Reasoning:**

The PR adds step 6b ("Check Documentation Comments") to Check 6, which explicitly specifies:

> For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition. Use the language's standard convention:

The step then enumerates language-specific doc comment conventions:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

This satisfies the criterion because:

1. It verifies "each new symbol" (iterates over all symbols from step 6a)
2. It checks for "a documentation comment" (specifically doc comments, not any comment)
3. It uses "the language's convention" (provides language-specific patterns for Rust, TypeScript/Java, Python, and Go)
4. It records each symbol's documentation status (documented or undocumented)

The language coverage is appropriate for a general-purpose check, covering the most common languages with standard doc comment conventions.
