# Repository Structure: trustify-ui

> **Eval fixture — synthetic data.** This is a representative repository structure for eval testing, not an exact mirror of any specific repository.

A React/TypeScript frontend for advisory and SBOM views, built with PatternFly.

## Directory Tree

```
trustify-ui/
├── package.json
├── tsconfig.json
├── CONVENTIONS.md
├── src/
│   ├── api/
│   │   ├── advisories.ts        # Advisory fetch helpers (paged)
│   │   └── sboms.ts
│   ├── pages/
│   │   ├── advisories/
│   │   │   ├── AdvisoryTable.tsx    # Advisory table component
│   │   │   └── __tests__/
│   │   │       ├── AdvisoryTable.test.tsx
│   │   │       └── AdvisoryTable.sorting.test.tsx  # Added by this PR
│   │   └── sboms/
│   └── App.tsx
└── tests/
    └── setup.ts
```
