# Unsupported Ecosystem Notification

## Notification Presented to User

**Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

## Context

- **CVE**: CVE-2026-31812
- **Vulnerability issue**: TC-8040
- **Vulnerable library**: quinn-proto
- **Detected ecosystem**: Go modules
- **Configured ecosystems (stream 2.2.x)**: Cargo, RPM
- **Configured ecosystems (stream 2.1.x)**: Cargo, RPM

The ecosystem detection resolved to "Go modules," which does not appear in any stream's Ecosystem Mappings table in security-matrix.md. The Ecosystem Mappings tables define the set of ecosystems supported for automated triage -- any ecosystem not listed requires manual assessment by the engineer.

## What This Means

The triage-security skill reads available ecosystems from the Ecosystem Mappings configuration in each stream's security-matrix.md rather than assuming a fixed set. Since "Go modules" is not listed:

1. No lock file path or check command is configured for Go modules
2. No version impact analysis can be performed (Step 2 requires ecosystem-specific lock file inspection)
3. No remediation tasks can be created (Step 8 task structure depends on ecosystem classification -- source dependency vs. system package)

## Automated Triage Stopped

The following steps are **not performed** for this unsupported ecosystem:

- Step 1.5 -- External CVE Data Enrichment (skipped)
- Step 1.7 -- Embargo Check (skipped)
- Step 2 -- Version Impact Analysis (skipped -- no lock file or check command configured)
- Step 3 -- Affects Versions Correction (skipped -- no version impact data)
- Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check (skipped)
- Step 5 -- Version Lifecycle Check (skipped)
- Step 6 -- Already Fixed Check (skipped)
- Step 7 -- Concurrent Triage Detection (skipped)
- Step 8 -- Remediation Task Creation (skipped -- no ecosystem classification available)

## Recommended Manual Actions

The engineer should:

1. Manually inspect the Go modules dependency tree for the affected versions
2. Determine whether quinn-proto (or its Go equivalent) is present and at what version
3. Assess version impact manually against the supportability matrix
4. Create remediation tasks manually if needed
5. Consider adding Go modules to the Ecosystem Mappings table in security-matrix.md if Go dependencies are expected in this product, so that future triages for Go ecosystem vulnerabilities can be automated
