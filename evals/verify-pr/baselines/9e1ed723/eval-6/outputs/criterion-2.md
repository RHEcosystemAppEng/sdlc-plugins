# Criterion 2: Check 6 checks each new symbol for a doc comment in the language's convention

**Verdict: PASS**

## Evidence (PR diff, `style-conventions.md`, 6b)

- `+For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition. Use the language's standard convention:`
- `+- **Rust:** `///` or `//!` doc comments`
- `+- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks`
- `+- **Python:** `"""..."""` docstrings immediately inside the function/class body`
- `+- **Go:** `//` comment immediately preceding the symbol declaration`
- `+- **Markdown:** not applicable — skip Markdown files`
- `+Record each symbol's documentation status (documented or undocumented).`

## Reasoning

6b runs over each symbol found in 6a and lists a doc-comment convention per language. The list matches the Implementation Notes exactly (`///` Rust, `/** */` Java/TypeScript, `"""` Python, `//` Go). It also correctly places Python docstrings inside the body, not before the definition. The lead sentence says "immediately precedes", which is slightly inconsistent with the Python bullet, but the bullet settles which rule applies to Python.

The Markdown exclusion is what reviewer comment 50001 and review body 40002 object to. Markdown files have no function, method, struct or class definitions, and neither the task's Acceptance Criteria nor its Implementation Notes mention Markdown. Skipping Markdown therefore does not break this criterion. The reviewer's proposed heading rule would add new scope (see review-50001.md).
