# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR diff adds section "6b -- Check Documentation Comments" to `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. This section instructs:

> For each new symbol identified in 6a, check whether a documentation comment
> immediately precedes the definition. Use the language's standard convention:

It then lists language-specific doc comment patterns:
- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

Each new symbol's documentation status (documented or undocumented) is recorded.

This satisfies the criterion. The check verifies documentation comments per-symbol using language-appropriate conventions, covering four major languages plus an explicit Markdown exclusion.

## Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Diff lines: the `#### 6b -- Check Documentation Comments` section (diff lines 25-36)
- Languages covered: Rust, TypeScript/Java, Python, Go
- Per-symbol recording: "Record each symbol's documentation status (documented or undocumented)"
