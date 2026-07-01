# Step 4: Root Cause Analysis

## Root Cause

The plan-feature skill's convention conformance analysis extracts `CONVENTIONS.md` section headings using `line[3:]`, which does not strip trailing whitespace. When a heading line contains trailing spaces (e.g., `## Migration Patterns  `), the extracted section name retains those spaces (`"Migration Patterns  "`). The downstream convention-aware task enrichment step performs an exact-match dictionary lookup using the clean convention name (`"Migration Patterns"`), which fails against the whitespace-polluted key. The convention is silently dropped with no warning logged.

## Affected Files

- **`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`** -- Convention conformance analysis section: the heading extraction logic at `section_name = line[3:]` does not call `.strip()` on the extracted text.
- **`plugins/sdlc-workflow/skills/plan-feature/SKILL.md`** -- Convention-aware task enrichment section: the exact-match lookup `if convention_name in discovered_conventions` has no fallback or fuzzy matching and no warning on miss.

## Suggested Approach

1. **Primary fix:** Strip trailing whitespace from extracted heading names during convention parsing. Change:
   ```python
   section_name = line[3:]
   ```
   to:
   ```python
   section_name = line[3:].strip()
   ```
   This normalizes the dictionary key so that downstream exact-match lookups succeed regardless of trailing whitespace in the source file.

2. **Defensive enhancement (optional):** Add a warning log when a convention name expected by the task enrichment step is not found in the discovered conventions dictionary. This prevents future silent-drop scenarios for other edge cases.

## Reproducer Strategy

1. Create a `CONVENTIONS.md` fixture file with trailing whitespace on at least one section heading:
   ```
   ## Migration Patterns  
   Add Index::create() for all FK columns.
   ```
   (Two trailing spaces after "Patterns" before the newline.)

2. Run the plan-feature skill against a feature issue that should trigger the "Migration Patterns" convention (e.g., a feature requiring a database migration with foreign keys).

3. **Assert** that the generated task's Implementation Notes contain:
   ```
   Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.
   ```

4. Before the fix, this assertion fails (the convention is silently dropped). After the fix, the assertion passes.

5. Additionally, add the trailing-whitespace fixture to the existing eval suite at `evals/plan-feature/files/conventions-mock.md` to ensure this edge case is covered by CI going forward.
