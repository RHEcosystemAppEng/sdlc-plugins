# Root Cause Analysis — ACME-500

This is the comment that would be posted on Bug ACME-500.

---

## Root Cause

**What is broken**: The plan-feature skill's convention conformance analysis silently drops conventions when `CONVENTIONS.md` heading lines contain trailing whitespace. The heading extraction code uses `line[3:]` to extract the section name, which preserves any trailing whitespace. The downstream convention match then performs an exact string comparison, which fails because the extracted key (e.g., `"Migration Patterns  "`) does not equal the expected key (`"Migration Patterns"`).

**Where it is broken**: The plan-feature convention lookup in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md`, specifically the heading extraction logic:

```python
section_name = line[3:]  # Does not strip trailing whitespace
```

This causes the exact-match lookup in the convention-aware task enrichment step to fail silently.

**How to verify the fix**: Create a reproducer test that includes trailing whitespace on a `CONVENTIONS.md` heading. The test should:

1. Use a `CONVENTIONS.md` fixture with trailing whitespace on the heading (e.g., `## Migration Patterns  ` with trailing spaces).
2. Run the convention lookup against this fixture.
3. Assert that the convention is correctly extracted and matched despite the trailing whitespace.
4. Verify that the generated task's Implementation Notes include the expected convention reference (e.g., `Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.`).

A passing reproducer confirms the fix handles the edge case correctly.
