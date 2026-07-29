## Repository
sdlc-plugins

## Target Branch
main

## Description
Root-cause: Document Markdown documentation coverage conventions in CONVENTIONS.md. A reviewer flagged that Check 6 (Documentation Coverage) skips Markdown files entirely, but this repository is documentation-heavy with skills defined in Markdown. The current CONVENTIONS.md describes the repository as "documentation-heavy" and notes that "skills are defined in Markdown (SKILL.md files)" but does not prescribe documentation coverage requirements for Markdown content. This gap caused the implementer to treat Markdown as "not applicable" without recognizing that Markdown is the primary content format requiring its own documentation coverage approach.

## Files to Modify
- `CONVENTIONS.md` -- add a convention documenting Markdown documentation coverage expectations, specifically: (1) new Markdown sections (headings) should have introductory/explanatory text, (2) when documentation coverage checks are applicable to Markdown files, and (3) what constitutes "documented" for Markdown content

## Implementation Notes
- Add the convention under the existing "Documentation" section or create a new subsection
- The convention should establish that in documentation-heavy repositories, Markdown headings introduced in PRs should be followed by explanatory prose before sub-sections or code blocks
- Reference the existing CONVENTIONS.md statement about Markdown being the primary format ("No source code: This is a documentation-heavy repository -- skills are defined in Markdown")
- The convention should be scoped to repositories where Markdown is a primary content format, not applied universally to all repos
- This is a convention gap (repo-specific knowledge), not a skill gap -- the knowledge about Markdown documentation expectations belongs in CONVENTIONS.md, not in general-purpose skills

## Acceptance Criteria
- [ ] CONVENTIONS.md includes a documented convention for Markdown documentation coverage
- [ ] The convention specifies when Markdown files need documentation coverage (e.g., new headings need explanatory text)
- [ ] The convention is scoped appropriately to documentation-heavy repositories
- [ ] The convention is discoverable by verify-pr's Check 1 (Convention Upgrade) for future convention-backed upgrades
