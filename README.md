# Ansible Island Adventure

A "teach the teacher" lab that enables Red Hatters to deploy, facilitate, and customize
gamified Capture the Flag (CTF) competitions built on Red Hat Ansible Automation Platform.

Instructors receive a fully deployed environment — CTFd scoring platform, Gitea source
control, AAP controller, Dev Spaces IDE, and RHEL managed nodes — and learn how to
run customer-facing events, modify challenges, and generate pipeline.

## Quick Start

### Prerequisites

- RHDP catalog access through Red Hat SSO
- Python 3.10+ on Linux or macOS for the deployment CLI
- Access to the student CI development configuration so you can publish your changes
- Git with read access to the catalog's AgnosticV repository (currently through SSH)
  and push access to this content repository when using `publish-content`

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r utils/requirements-dev.txt
```

### Order the two catalog items

Deployment requires **two catalog items (CIs), ordered in sequence**:

1. Order the [Leaderboard CI](https://catalog.demo.redhat.com/catalog/all?search=island&item=babylon-catalog-dev%2Frh1-2027.lb1663-rh1-ans-island-leaderboard-cnv.dev).
   Select Activity **Asset Development**, Purpose **Developing a community demo**,
   leave other optional fields blank, check **Confirm that I understand above warnings**,
   and click **Order**. Wait until deployment completes.
2. Retrieve the leaderboard's ResourceClaim YAML and extract its provision fields:

   ```bash
   python utils/extract-provision-fields.py provision-data.yaml provision-fields.txt
   ```

   The output contains passwords. Keep it private. Missing or blank required values
   cause a nonzero exit without printing partial output.
3. Order the [Student CI](https://catalog.demo.redhat.com/catalog/all?search=island&item=babylon-catalog-dev%2Frh1-2027.lb1663-rh1-ans-island-student-cnv.dev).
   Use the same activity, purpose, and warning acknowledgement. Copy the five
   extracted values into the corresponding fields below, then click **Order**.
4. Wait for the student deployment to finish before beginning development.
5. Load event challenges with your post-deployment Ansible playbook. Catalog
   provisioning initializes CTFd service access and accounts; it leaves a new
   instance's challenge board empty. A standalone content loader is available at
   [`automation/ansible/configure_ctfd.yml`](automation/ansible/configure_ctfd.yml);
   see the [collection README](automation/ansible/README.md) for inputs and usage.

| Leaderboard provision-data key | Student form field / variable |
|-------------------------------|-------------------------------|
| `openshift_api_server_url` | OpenShift API Server URL / `openshift_api_server_url` |
| `openshift_cluster_ingress_domain` | OpenShift Cluster Ingress Domain / `openshift_cluster_ingress_domain` |
| `openshift_cluster_admin_password` | OpenShift Cluster Admin Password / `openshift_cluster_common_password` |
| `keycloak_admin_user` | Keycloak Admin Username / `keycloak_admin_user` |
| `keycloak_admin_password` | Keycloak Admin Password / `keycloak_admin_password` |

For machine-readable extraction, add `--format json`; the JSON uses the student
variable names. The password source and destination names differ deliberately.
The extractor calls this the common password; the current student form labels
the input **OpenShift Cluster Admin Password**.

### Automate catalog ordering

The CLI uses the [Babylon catalog API](https://github.com/redhat-cop/babylon/tree/main/catalog/api)
and its browser SSO handoff. Log in once:

```bash
python utils/dev-environment.py login
python utils/dev-environment.py whoami
python utils/dev-environment.py inspect
```

`login` opens the catalog's `/auth/cli-redirect` endpoint. Complete SSO in your
browser; an existing browser login can satisfy it. The catalog sends its proxy
cookies to a temporary localhost callback. The CLI validates them with
`/auth/session` and saves them privately. No SSO password is collected.
`inspect` reads both live catalog schemas, their resource versions, and warnings.

If the deployed catalog does not yet support the browser handoff, import an
exported cookie file for `catalog.demo.redhat.com`:

```bash
python utils/dev-environment.py login --cookies-file /private/path/catalog-cookies.json
```

Supported formats are a JSON cookie-name/value map, a browser cookie list,
Playwright storage-state JSON, and Netscape cookies.txt. Export the **catalog
host's OAuth proxy cookies**, including all chunks, after signing in; cookies
from the identity-provider host alone are insufficient. Cookie values belong
in the private file, not command arguments. The browser and CLI must be able to
reach the same loopback callback; for a remote terminal, forward the printed
callback port or use cookie import. `login --no-browser` only prints the login URL.

An existing `babylon login` session is also supported: if no local auth file
exists, the CLI reads `$XDG_CONFIG_HOME/babylon/config.yaml` (default
`~/.config/babylon/config.yaml`). To explicitly choose one:

```bash
python utils/dev-environment.py --babylon-config /private/path/config.yaml whoami
```

After reviewing the warnings, deploy both CIs:

```bash
python utils/dev-environment.py bootstrap --accept-warnings
```

This orders the leaderboard when none is saved, waits for it to reach `started`,
extracts and validates the five fields, then orders and waits for the student.
The flag records the same acknowledgement as the catalog checkbox; Babylon's
order API has no separate checkbox field. Default activity and purpose match
the manual procedure above.

To start with an existing leaderboard, use either its service identity or its YAML:

```bash
python utils/dev-environment.py bootstrap --leaderboard <namespace>/<claim-name> --accept-warnings
python utils/dev-environment.py bootstrap --leaderboard-file provision-data.yaml --accept-warnings
```

The YAML supplies the identity; credentials and readiness are refreshed from the
live API. For each subsequent student CI change:

```bash
# Commit the intended content first, then explicitly publish that revision.
python utils/dev-environment.py publish-content --commit <commit-sha>
python utils/dev-environment.py check-student
python utils/dev-environment.py new-student --accept-warnings
```

`publish-content` reads the student CI's effective Showroom repository/ref from
its AgnosticV `common.yaml` and stage override (for example, `dev.yaml`). The
current student CI overrides the common `main` ref with **`dev`**. Publishing
creates or advances that branch to the selected committed revision using the
local `origin` push remote. It verifies that the destination matches the CI's
content repository and that the commit contains the Showroom entrypoints.
`--remote <name>` selects a different local remote. It does not create commits,
include uncommitted changes, or force-push. A non-fast-forward update must be
reconciled in Git before retrying. Publishing content places no catalog orders.

`check-student` resolves the same configuration and verifies the published ref
without ordering anything. `bootstrap` and `new-student` perform this check
before saving a new run or submitting any orders; the student submission checks
again that the content commit has not moved. Runs record the verified content
commit and AgnosticV configuration commit. Configuration snapshots are cached
privately beneath `.aia-dev/source-cache/` and refreshed on the next source check.
These checks resolve literal Showroom repository/ref settings from the CI's
common and stage files; inherited or templated source settings require extending
the resolver rather than guessing a ref.

This prevents the failure where Showroom's `git-cloner` retries a missing `dev`
branch until the pod readiness task times out. A main branch in the content
repository does not satisfy a CI configured to clone `dev`. After a failed run,
use `abandon --run <run-id>` before ordering a fresh student; this only closes the
local run and does not clean up its catalog resources. The saved leaderboard
continues to be reused.

The `new-student` command reuses the saved leaderboard and creates a fresh student. Use
`bootstrap --new-leaderboard --accept-warnings` for a fresh pair. Each run records
the local Git revision, both catalog resource versions, and catalog spec hashes.
Local edits are not automatically published to RHDP. Use `publish-content` to
publish committed Showroom content and separately publish/sync changes to the
student CI configuration or workload automation. Verified source refs do not
prove which workload automation commit was deployed. To require an observed catalog version,
pass `--expected-student-version <resourceVersion>` from `inspect`.

To deploy independent student CIs through the workshop interface:

```bash
python utils/dev-environment.py new-student --workshop --workshop-user-count 2 \
  --keep-on-failure --accept-warnings
```

This creates a Babylon Workshop and WorkshopProvision using the catalog display
name, a generated eight-character access password, open registration, and an
empty description. The user count is the number of separate student CIs, all
using the saved leaderboard. Provision concurrency and start interval use the
form defaults of 10 and 30 seconds. Workshop ordering currently supports catalog
items with `workshopUserMode: none`; count limits and disabled interfaces are
checked before ordering.

`--keep-on-failure` selects **Keep instance if provision fails** by omitting the
auto-detach rule, so failed infrastructure remains available for inspection.
It also works for standalone orders. Auto-Stop and Auto-Destroy still apply.
Workshop passwords and exact requests are stored only in private `.aia-dev/`
files. `resume` recovers the same Workshop/WorkshopProvision after interruption,
then waits for and checks each student CI. `status` prints the workshop and
individual service links. The utility does not request replacement orders for
failed children; the workshop controller can apply its normal replacement policy.

To save a leaderboard that was ordered successfully in the browser without
ordering anything else:

```bash
python utils/dev-environment.py use-leaderboard <namespace>/<claim-name>
```

This checks the live catalog identity, deployment readiness, and all five student
fields before saving the claim's UID for reuse. Future `new-student` runs use it.
If an older run is incomplete, close that local run with `abandon --run <run-id>`
first. This leaves its catalog resources unchanged.

### Resume and verify

```bash
python utils/dev-environment.py status
python utils/dev-environment.py resume
# Select an older run explicitly:
python utils/dev-environment.py resume --run <run-id>
```

Order intent is saved before submission. Resume looks up the same claim name
and verifies its UID and catalog identity; it does not generate a replacement
order after an interrupted response. If a submission was attempted but the claim
is absent, inspect the catalog before using `resume --retry-submit`, which
retries that exact name. An incomplete run blocks another run in the same state
directory. Use `abandon` to close it locally; catalog resources remain allocated.

The CLI refreshes the API session token while the SSO cookies remain valid. If
SSO expires, run `login` again, then `resume`. Polling defaults to 30 seconds with
a two-hour timeout per CI; override with `--poll` and `--timeout` (seconds).
Read-only API calls retry transient network errors and HTTP 429/502/503/504 up
to three attempts. Ambiguous order submissions are recovered through `resume`.
The process can be interrupted with Ctrl-C and resumed later.

Provider validation errors stop polling immediately, including when the catalog
still displays **Waiting to Provision**. The latest ResourceClaim is saved
privately alongside the run for diagnosis. Activity and explanation are form
metadata stored in annotations; they are only sent as provider inputs if the
catalog explicitly declares them. Orders also follow the catalog's default
Auto-Stop runtime and, unless `--keep-on-failure` is selected, the browser's
failed-provisioning detachment behavior.

After deployment, reachability checks use the student's published `ctfd_url`,
`gitea_url`, and `aap_url` with TLS verification and without catalog credentials.
They check CTFd HTTP availability, Gitea's version endpoint, and the AAP entry
page (including its login redirect), retrying for up to five minutes. These are
smoke checks; they do not validate user login, challenge execution, or VM behavior.
If a check fails, the deployed environment is retained and `resume` retries.
`--skip-checks` explicitly bypasses these checks and records that choice.

State, credentials, exact request payloads, and exported ResourceClaims live in
the gitignored `.aia-dev/` directory. JSON files are written atomically with mode
`0600`, and newly created state directories use `0700`. Keep custom state
directories equally private. Global options such as `--state-dir` and `--server`
go **before** the command, and must be reused when resuming that environment.
The CLI has no resource deletion operation; manage cleanup and environment
lifespans in the catalog, taking shared leaderboard dependencies into account.

Run offline tests without SSO or catalog orders:

```bash
python -m unittest discover -s utils/tests -v
```

## Architecture

```
rhpds.aia collection (collections/ansible_collections/rhpds/aia/)
├── deploy_leaderboard    Local cluster-services deployment tooling
└── deploy_vms            VM provisioning role (stub)
```

The catalog ordering flow above is the deployment entry point. The repository
also retains local collection roles and test playbooks:

| Role | What it deploys | Cluster |
|------|----------------|---------|
| `rhpds.aia.deploy_leaderboard` | AAP orgs, CTFd (per instructor), Gitea, Dev Spaces | Leaderboard cluster (AAP + Dev Spaces pre-installed) |
| `rhpds.aia.deploy_vms` | Planned VM provisioning; currently a stub | VM cluster (CNV-enabled) |

Catalog workload automation is in `automation/ansible/roles/`, including
`instructor_config`. Legacy `qa-automation/` playbooks expect `.cnv.env` and must
be adapted before use with the current two-CI layout.

## Using as a Collection

For local role development, install `oc`, `ansible-core`, the `kubernetes.core`
and `community.general` collections, and Python packages `kubernetes`, `passlib`,
and `pyyaml`. These are separate from catalog ordering prerequisites. The roles
can be included directly in your own playbooks:

```yaml
- hosts: localhost
  roles:
    - role: rhpds.aia.deploy_leaderboard
      vars:
        aia_leaderboard_env: /path/to/.leaderboard.env
        aia_instructor_count: 10
```

Set `collections_path` in your `ansible.cfg` to point at the `collections/` directory,
or install the collection to `~/.ansible/collections`.

## Local Role Configuration

The following settings apply to the local collection role, independently of the
catalog ordering CLI. Defaults are in
`collections/ansible_collections/rhpds/aia/roles/deploy_leaderboard/defaults/main.yml`.

| Variable | Default | Description |
|----------|---------|-------------|
| `aia_leaderboard_env` | `""` | Path to ResourceClaim YAML (required) |
| `aia_instructor_count` | `4` | Number of instructors to create |
| `aia_instructors` | `[]` | Explicit instructor list (overrides count) |
| `aia_aap_manifest_path` | `""` | AAP manifest ZIP (if license not pre-applied) |
| `aia_ctfd_admin_password` | `supersecret123!` | CTFd admin password |
| `aia_gitea_admin_password` | `supersecret123!` | Gitea admin password |
| `aia_vm_ssh_user` | `student` | SSH user created on managed node VMs |

## Challenge Flags

Challenge flag values are vault-encrypted in `ansible-testing/vars/flags.yml`.
The vault password is in `.vault-password` (gitignored).

To edit flags:
```bash
ansible-vault edit ansible-testing/vars/flags.yml
```

Challenge definitions (descriptions, hints, categories) are plaintext in
`ansible-testing/vars/challenges.yml` and reference flags via `{{ ctfd_flags.<key> }}`.

## Capacity Planning

See [ansible-testing/CAPACITY.md](ansible-testing/CAPACITY.md) for production sizing.
A 5-worker cluster (64 vCPU / 128Gi each) supports ~140 instructors with 25% headroom.

## Repository Structure

```
.
├── ansible.cfg                        Ansible config (vault password, collections path)
├── collections/
│   └── ansible_collections/rhpds/aia/ The rhpds.aia Ansible collection
│       ├── galaxy.yml
│       └── roles/
│           ├── deploy_leaderboard/    Cluster services role
│           └── deploy_vms/            VM provisioning role (stub)
├── ansible-testing/                   Test playbooks and legacy roles
│   ├── deploy_leaderboard.yml         Test entrypoint for leaderboard deploy
│   ├── vars/
│   │   ├── flags.yml                  Challenge flags (vault-encrypted)
│   │   └── challenges.yml             Challenge definitions
│   ├── CAPACITY.md                    Production sizing guide
│   └── roles/                         Legacy pre-collection roles (reference only)
├── publishing-house/                  RHDP Publishing House spec and design docs
├── utils/                             Catalog deployment CLI and field extractor
│   ├── dev-environment.py             SSO login, ordering, status, and resume
│   ├── student_source.py              Showroom source checks and explicit publication
│   ├── extract-provision-fields.py    Manual extraction of student order fields
│   └── tests/                         Offline authentication and lifecycle tests
└── content/                           Showroom lab content (AsciiDoc)
```

## Publishing House

This project is managed through the [RHDP Publishing House](https://central-api-publishing-house.apps.ocpv-infra02.wdc07.infra.demo.redhat.com)
pipeline. Run `/rhdp-publishing-house` in Claude to check project status.
