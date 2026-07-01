# Unsupported Ecosystem Notification

## Step 5.3 -- Unsupported Ecosystem Handling

After Step 1 Ecosystem detection resolved the vulnerable library's ecosystem to **Go modules**, the skill checked the Ecosystem Mappings tables in the security-matrix.md for all configured version streams.

### Ecosystem Mappings (from security-matrix.md)

**Stream 2.1.x (rhtpa-release.0.3.z):**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Stream 2.2.x (rhtpa-release.0.4.z):**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Supported ecosystems**: Cargo, RPM

**Detected ecosystem**: Go modules

### Notification Presented to User

> **Unsupported ecosystem**: Go modules is not yet supported for automated triage. Manual assessment is required.

The detected ecosystem name ("Go modules") is substituted into the notification template's `<ecosystem>` placeholder, following the angle-bracket placeholder convention used by other user-facing messages in the skill. The notification is not hard-coded to any specific ecosystem name -- it dynamically uses whatever ecosystem was detected in Step 1.

### Triage Halted

Automated triage stops at this point. The following steps are **not performed** for the unsupported ecosystem:

- **Step 2 (Version Impact Analysis)** -- skipped. No lock file inspection or version impact table is generated.
- **Step 3 (Affects Versions Correction)** -- skipped. No Jira version corrections are proposed.
- **Step 4 (Duplicate/Sibling/Overlap Check)** -- skipped. No sibling or overlap analysis is performed.
- **Step 5 (Version Lifecycle Check)** -- skipped.
- **Step 6 (Already Fixed Check)** -- skipped.
- **Step 7 (Concurrent Triage Detection)** -- skipped.
- **Step 8 (Remediation)** -- skipped. No remediation tasks are created, and no close recommendation is issued.

The engineer must perform manual assessment for Go modules vulnerabilities, including:
- Manually inspecting the relevant go.sum or go.mod files at each pinned commit
- Determining version impact by hand
- Creating remediation tasks manually if the vulnerability affects supported versions
