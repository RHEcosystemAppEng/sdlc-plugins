# Step 4 - Root Cause Analysis: ACME-500

## Root Cause Comment (to be posted on Bug ACME-500)

### Root Cause

The plan-feature skill's convention extraction in `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` parses `CONVENTIONS.md` headings using `line[3:]` without stripping trailing whitespace. When a heading line contains trailing spaces (e.g., `## Migration Patterns  `), the extracted section name becomes `"Migration Patterns  "` (with trailing spaces).

During task enrichment, the skill performs an exact-match lookup against convention names without trailing whitespace. The mismatch causes the lookup to fail silently, and the convention is omitted from the generated task description.

**What is broken**: Convention heading extraction does not normalize whitespace, causing exact-match lookups to fail for headings with trailing whitespace.

**Why it breaks**: `line[3:]` preserves trailing whitespace from the source file. The downstream lookup uses a clean (no trailing whitespace) key, so the dictionary lookup fails.

**Where it breaks**: `plugins/sdlc-workflow/skills/plan-feature/SKILL.md` -- the convention heading extraction loop, specifically the `section_name = line[3:]` assignment.

**How to fix**: Add `.strip()` to the heading extraction: `section_name = line[3:].strip()`. This normalizes the dictionary key at the source, ensuring downstream lookups succeed regardless of trailing whitespace in the source file.

**How to verify**:
1. Create a `CONVENTIONS.md` with trailing whitespace on a heading (e.g., `## Migration Patterns  `).
2. Run `/plan-feature` on a feature that should trigger that convention.
3. Confirm the generated task's Implementation Notes includes the convention reference.
4. Run existing plan-feature evals to confirm no regressions.
