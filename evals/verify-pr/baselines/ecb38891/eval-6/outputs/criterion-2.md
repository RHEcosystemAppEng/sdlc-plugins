# Acceptance Criterion 2

## Criterion

> Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR diff adds Step 6b ("Check Documentation Comments") to Check 6, which explicitly instructs the sub-agent to verify documentation comments for each new symbol identified in 6a. The step specifies language-specific doc comment conventions:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

The check records each symbol's documentation status (documented or undocumented), providing a per-symbol assessment rather than just an aggregate result.

This criterion is satisfied: the check verifies doc comments using language-specific conventions for five major languages.

## Evidence

From the PR diff in style-conventions.md:

```
#### 6b — Check Documentation Comments

For each new symbol identified in 6a, check whether a documentation comment
immediately precedes the definition. Use the language's standard convention:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable — skip Markdown files

Record each symbol's documentation status (documented or undocumented).
```
