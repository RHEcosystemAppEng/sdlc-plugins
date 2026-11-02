# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

The diff adds section "6b — Check Documentation Comments" which lists language-specific doc comment patterns:
- Rust: `///` or `//!` doc comments
- TypeScript/Java: `/** ... */` JSDoc/Javadoc blocks
- Python: `"""..."""` docstrings immediately inside the function/class body
- Go: `//` comment immediately preceding the symbol declaration
- Markdown: not applicable — skip Markdown files

The check verifies that a documentation comment immediately precedes each new symbol definition.

**Evidence:**
- Lines 23-37 of the diff add the complete "6b — Check Documentation Comments" subsection
- Five language conventions are listed with specific syntax patterns
- Each new symbol is checked for a doc comment immediately preceding its definition
