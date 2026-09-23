# Newman dependency status

Registry audit checked on 2026-09-21. These are npm's counts of vulnerable
packages, including parent packages affected through dependencies, not counts
of independent vulnerabilities or proof of exploitability in this collection.

| State | Critical | High | Moderate | Total |
|---|---:|---:|---:|---:|
| Original lockfile | 1 | 12 | 7 | 20 |
| Patched dependency overrides | 0 | 5 | 4 | 9 |

Newman 6.2.2 was already the registry's latest version, but several dependencies
were pinned below patched versions. The overrides select same-major releases:

| Dependency | Selected version |
|---|---|
| handlebars | 4.7.9 |
| lodash | 4.18.1 |
| node-forge | 1.4.0 |
| qs | 6.16.0 |
| underscore | 1.13.8 |
| ip-address | 10.7.2 |
| flatted | 3.4.4 |
| jose | 4.15.9 |

The remaining advisories originate in `@faker-js/faker`, `csv-parse`, and `uuid`,
and propagate to their Newman/Postman parents. Fixing those requires additional
compatibility work across major versions or an upstream runtime update. No
major-version overrides or forced Newman downgrade were applied.

Reproduce with `npm ci`, `npm audit`, `npm run test:contracts`, and `npm test`.
The audit still returns nonzero because unresolved advisories remain. Do not
describe this dependency tree as vulnerability-free. The API collection and
failure probes exercise this project's usage; they do not cover all Newman
features, authentication schemes, dynamic variables, or untrusted collections.

CI uses `npm audit --audit-level=critical` to prevent a return of critical
findings while the documented high/moderate dependency migration remains open.

Recheck the pins when upgrading Newman and remove overrides once its supported
dependency tree provides the fixes. Counts can change as new advisories appear.
