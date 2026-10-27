# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Analysis

The PR diff adds step 6b ("Check Documentation Comments") which defines language-specific doc comment patterns:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable — skip Markdown files

For each new symbol identified in 6a, the check verifies whether a documentation comment immediately precedes the definition using the appropriate language convention.

## Evidence

- **File:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- **Lines added:** Step 6b section with language-specific doc comment patterns
- **Verification method:** Checks for documentation comment immediately preceding the definition
- **Languages covered:** Rust, TypeScript, Java, Python, Go, with Markdown exclusion
