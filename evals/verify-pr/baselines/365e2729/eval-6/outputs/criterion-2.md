# Criterion 2 — Check 6 verifies each new symbol has a documentation comment using the language's convention

**Verdict: PASS**

## What the PR implements
`#### 6b — Check Documentation Comments` checks that a documentation comment comes immediately before each symbol found in 6a. It uses each language's standard convention:
- Rust: `///` or `//!`
- TypeScript/Java: `/** ... */` (JSDoc/Javadoc)
- Python: `"""..."""` docstring immediately inside the function/class body
- Go: a `//` comment immediately before the declaration
- Markdown: not applicable, skipped

It also records whether each symbol is documented or undocumented.

## Reasoning
- The list covers every language named in the task's Implementation Notes (`///` Rust, `/** */` Java/TypeScript, `"""` Python, `//` Go) and adds `//!` for Rust. The check applies to each symbol from 6a, so "each new symbol" is satisfied.
- Minor wording problem: the 6b lead-in says the comment "immediately precedes the definition", but the Python rule correctly says the docstring is *inside* the body. The Python bullet is correct and makes the intent clear, so this is a nit, not a failure.
- The Markdown exclusion is the subject of review comment 50001. That comment asks to extend the check beyond what the criteria require (sub-task 1). It does not mean this criterion is unmet.

## Evidence
- PR diff, `style-conventions.md`, 6b bullet list.
