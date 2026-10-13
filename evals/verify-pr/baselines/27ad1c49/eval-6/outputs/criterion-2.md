# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR diff adds step **6b -- Check Documentation Comments** to `style-conventions.md`. This step instructs the check to verify each new symbol (identified in 6a) has a documentation comment using language-specific conventions:

> For each new symbol identified in 6a, check whether a documentation comment
> immediately precedes the definition. Use the language's standard convention:
>
> - **Rust:** `///` or `//!` doc comments
> - **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
> - **Python:** `"""..."""` docstrings immediately inside the function/class body
> - **Go:** `//` comment immediately preceding the symbol declaration
> - **Markdown:** not applicable -- skip Markdown files

The step explicitly requires checking "whether a documentation comment immediately precedes the definition" and provides the specific doc comment syntax for five major language ecosystems. It also records each symbol's documentation status (documented or undocumented).

## Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Diff lines 25-36: Step 6b "Check Documentation Comments" with per-language conventions
