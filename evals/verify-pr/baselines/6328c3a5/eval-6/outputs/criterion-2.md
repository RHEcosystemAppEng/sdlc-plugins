## Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

**Verdict: PASS**

The diff adds section "6b -- Check Documentation Comments" which instructs: "For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition. Use the language's standard convention." It then enumerates language-specific patterns:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

The instruction to "Record each symbol's documentation status (documented or undocumented)" confirms that every new symbol is individually checked against the appropriate convention.

**Evidence:**
- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Diff lines 25-36 define sub-section 6b with per-language doc comment patterns
