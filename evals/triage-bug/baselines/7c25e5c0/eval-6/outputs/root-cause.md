# Step 4 -- Root Cause Analysis

## Root Cause

The plan-feature skill's convention heading extraction does not strip trailing whitespace from `CONVENTIONS.md` heading lines.

### Mechanism

1. The convention parser iterates over lines in `CONVENTIONS.md` and identifies headings by the `## ` prefix.
2. It extracts the heading text using `line[3:]`, which captures everything after the `## ` prefix -- including any trailing whitespace characters.
3. When a heading line has trailing spaces (e.g., `## Migration Patterns  `), the extracted key becomes `"Migration Patterns  "` (with trailing spaces).
4. Later, the task enrichment step looks up conventions by their expected clean name (e.g., `"Migration Patterns"`). This exact-match comparison fails because the stored key has trailing whitespace.
5. The failed match is not logged or warned about -- the convention is silently dropped from the generated task description.

### Why It Is Silent

The code path that matches `convention_name in discovered_conventions` simply evaluates to `False` when trailing whitespace causes a mismatch. There is no `else` branch or warning log for unmatched conventions, so the failure is completely silent.

## Fix Approach

1. **Primary fix**: Strip trailing whitespace from the extracted heading name:
   ```python
   section_name = line[3:].strip()
   ```
   This normalizes headings regardless of trailing whitespace.

2. **Secondary fix**: Add a warning log when an expected convention name is not found in the discovered conventions, so that similar mismatches do not go undetected in the future.

3. **Test coverage**: Add an eval fixture that includes trailing whitespace on a `CONVENTIONS.md` heading to prevent regression.

## Severity Assessment

- **Impact**: Convention conformance guidance is silently dropped from generated tasks, which may lead to implementation that violates repository conventions.
- **Scope**: Affects any repository where `CONVENTIONS.md` headings happen to have trailing whitespace -- a common occurrence with editor auto-formatting or copy-paste.
- **Workaround**: Manually remove trailing whitespace from all `CONVENTIONS.md` headings.
