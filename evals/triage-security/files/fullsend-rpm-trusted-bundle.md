<!-- SYNTHETIC TEST DATA — schema-valid trusted RPM Fullsend evidence -->

# Trusted bundle facts

The mounted `triage-security-input.json` is already schema-valid for issue
`TC-8102`, with authorization `mutation_authorized: false`. Its trusted 2.2.x
matrix and `rpms.lock.yaml` evidence identify `openssl-libs` as an RPM package:

| Release | Lock version | Assessment |
| --- | --- | --- |
| 2.2.0 | 3.0.7-1 | vulnerable |
| 2.2.1 | 3.0.7-1 | vulnerable |
| 2.2.2 | 3.0.7-1 | vulnerable |
| 2.2.3 | 3.0.8-2 | patched |
| 2.2.4 | 3.0.8-2 | patched |

The same bundle includes an already retrieved SBOM record confirming the RPM
package classification. It supplies no local files, cosign access, Jira access,
git repository, or network access.
