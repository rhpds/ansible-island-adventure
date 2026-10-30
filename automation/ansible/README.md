# rhpds.aia — Ansible Island Adventure Collection

This collection contains automation for deploying and configuring the Ansible Island Adventure CTF platform on OpenShift CNV.

## Roles

Catalog workload roles live in this directory:

- `roles/instructor_config/` — Instructor services and access, including CTFd bootstrap, Gitea, AAP, and Keycloak integration
- `roles/keycloak_ocp_logout_fix/` — Keycloak/OpenShift logout configuration
- `roles/configure_devspaces/` — Shared leaderboard workspace limits and persistent storage policy, applied by post-deploy

The project root also retains `ansible-testing/` playbooks and the
`collections/ansible_collections/rhpds/aia/` collection for local role development.
The collection's `deploy_vms` role is currently a stub.

## Usage

Order the leaderboard CI first, wait for deployment, then order the student CI
using the leaderboard's five provision fields. Workload deployment runs through
RHDP provisioning. See the [root README](../../README.md#quick-start) for manual
ordering and the SSO-enabled `utils/dev-environment.py` CLI, which reuses the
leaderboard for subsequent student deployments.

Catalog provisioning deploys CTFd, waits for health, initializes the admin and
student accounts, completes setup, and publishes its URL and credentials. New
instances have an empty challenge board and a landing page linking to login.
Challenge definitions, archive generation/import, and challenge-count checks
are excluded from the default role path. Reprovisioning preserves existing
challenge data and event settings. The bootstrap command has its own timeout
and retry settings: `ctfd_bootstrap_timeout` (120 seconds),
`ctfd_bootstrap_retries` (2), and `ctfd_bootstrap_delay` (10 seconds).

Load content after the student CI succeeds, either from your event playbook or
with the standalone entry point (starting at the repository root):

```bash
cd automation/ansible
ansible-playbook configure_ctfd.yml \
  -e @/private/student-vars.yml -e @/private/event-challenges.yml \
  -e ansible_python_interpreter=/usr/bin/python3
```

Install `ansible-core`, the `kubernetes.core` and `community.general`
collections, Python `kubernetes`, `requests`, and `PyYAML`, and GNU coreutils `timeout` on
the control host. The playbook prepares `oc` using the role's existing CLI
installation/login tasks; the automatic installation requires sudo if `oc`
is missing. The interpreter override selects your local Python instead of
the role's provisioning-image default `/usr/bin/python3.11`.
Running from this directory also avoids the root `ansible.cfg`, which expects
the legacy `.vault-password` file. If your event vars are encrypted, pass your
vault password file explicitly with `--vault-password-file`.

The private student vars file supplies `guid` (the student's deployed GUID),
`openshift_api_server_url`, `openshift_cluster_ingress_domain`, and
`openshift_cluster_common_password`, matching the catalog workload inputs.
Use the GUID from `status.resourceHandle.name` (`guid-<guid>`) in a ResourceClaim.
The role derives the namespace as `instructor-<guid>-ctfd` unless you override
`instructor`. The event file supplies `ctfd_challenges` and optionally
`ctfd_challenges_advanced`, with real flags. Without an override, the loader uses
the bundled definitions, whose flags are `CHANGEME` placeholders.

To integrate with an existing post-deployment playbook, include
`instructor_config` with `tasks_from: ctfd_config` after authenticating `oc`;
use `ansible_island_adventure.automation.instructor_config` when installed as
a collection. This task entry point does not rerun Gitea, Keycloak, AAP, or
infrastructure deployment and does not require AgnosticD publication plugins.
The retained archive loader only imports into an empty challenge database; it
does not update challenges or reset scores on an existing populated instance.

The post-deployment challenge-count check allows 120 seconds per attempt and
two retries, with a 10-second delay between attempts. Override
`ctfd_challenge_check_timeout`, `ctfd_challenge_check_retries`, and
`ctfd_challenge_check_delay` when needed. Failed commands and missing or malformed
counts stop content loading before archive import; their command diagnostics are
retained in the Ansible output.

The check uses GNU coreutils `timeout` on the control host
instead of Ansible async polling. This avoids missing async result files when
the launch and polling processes resolve their job directories differently.
On timeout, it preserves partial output and reports the termination on stderr;
commands that ignore termination are killed after another five seconds.

## Configure deployed students

The deployment sequence has three responsibilities: the leaderboard CI creates
the shared cluster and Dev Spaces service; the student CI integrates with that
leaderboard and creates the requested student accounts and resources; this
post-deploy playbook applies iterated configuration to those existing resources.
No new CI orders or deployments are needed to change the workspace policy.

`post_deploy.yml` connects each already deployed student CI's CTFd instance and
Gitea account. It uses the real definitions in
[`ansible-testing/vars/challenges.yml`](../../ansible-testing/vars/challenges.yml)
and vault-encrypted answers in
[`ansible-testing/vars/flags.yml`](../../ansible-testing/vars/flags.yml).
The flags were aligned with the instructor toolkit at
[`6009a82`](https://github.com/l3acon/aia-instructor/tree/6009a828f76f4346a1d6b3c03ccdd3131ab0d278),
including corrected YAML quoting of regex answers and keys matched by challenge
name. The repository-name and main-branch Hello World answers were also corrected
to match the current student Gitea content. The vault password is supplied
separately; `.vault-password` is gitignored.

After validating all student mappings and flags, post-deploy configures Dev
Spaces once for the shared leaderboard cluster, before its serial student
configuration. Each instructor can run two simultaneous workspaces, with
`per-workspace` persistent storage. Separate PVCs prevent the cross-node
`Multi-Attach` failures caused by sharing a ReadWriteOnce per-user volume.
The exported inventory represents one leaderboard; do not combine students
from different leaderboard clusters into it.

`TODO(devspaces-ci-bootstrap)`: this Dev Spaces step is a temporary compatibility
workaround. Remove the automatic `configure_devspaces.yml` import from
`post_deploy.yml` after the shared `core_workloads` role exposes PVC strategy,
the leaderboard AgnosticV CI sets two running workspaces and `per-workspace`
storage, and a fresh leaderboard deployment is verified before post-deploy runs.
Verification must include two simultaneous workspaces for one instructor with
separate bound PVCs. Keep the standalone repair entry point while older
deployments still need it. The student CI does not need this cluster-wide setting.
To bypass the workaround during validation of the new CI defaults, use
`--skip-tags devspaces_ci_workaround` with `post_deploy.yml`.
Track the upstream feature in [core_workloads#197](https://github.com/rhpds/core_workloads/pull/197)
and the dependent leaderboard configuration in
[agnosticv#28869](https://github.com/rhpds/agnosticv/pull/28869).

From the repository root, using the development virtual environment:

```bash
.venv/bin/python -m pip install kubernetes
ansible-galaxy collection install -p ~/.ansible/collections kubernetes.core community.general
.venv/bin/python utils/dev-environment.py export-students --run <run-id>

cd automation/ansible
ansible-playbook -i ../../.aia-dev/runs/<run-id>.students.inventory.json \
  post_deploy.yml --vault-password-file ../../.vault-password
```

The exporter refreshes saved claim identities from the catalog, requires the
leaderboard and every student to be started and healthy, and validates the GUID,
CTFd URL, and Gitea owner before writing an inventory with mode `0600` under
`.aia-dev/`. It exports the actual published credentials, including different
CTFd and Gitea usernames, and records the Python interpreter used for export.
It places no orders. The generated kubeconfig is also kept under `.aia-dev/`.

To iterate on Dev Spaces alone, use the same exported inventory:

```bash
cd automation/ansible
ansible-playbook -i ../../.aia-dev/runs/<run-id>.students.inventory.json \
  configure_devspaces.yml
```

This entry point needs no event vault and does not configure Gitea or CTFd.
Override `aia_devspaces_running_workspaces_per_user` (default `2`) if needed;
the policy uses `aia_devspaces_pvc_strategy: per-workspace`. It patches the
existing CheCluster without recreating the service. The current cluster's
total saved-workspace limit is already two, so it accommodates both workspaces.

The storage default applies to newly created workspaces. Existing per-user
workspaces and their PVCs are left intact; save or back up uncommitted work and
recreate those workspaces with per-workspace storage when ready. Do not simply
change their storage attribute and assume files have moved. Each new workspace
has separate storage, including its own repository checkout and local files.

All students' event flags are resolved and checked before service changes.
Use `--tags preflight` to run just this validation. Override
`aia_event_flags_file` with an absolute path for a different event vault.
The default load includes 25 base challenges. Set `aia_enable_advanced=true`
only after deploying a verifier and supplying a valid `aia_student.verifier_url`;
the provisioned placeholder URL is not a verifier integration.

For each student, the playbook authenticates as their existing Gitea user,
checks or repairs missing forks, and verifies `main` and `treasurehunt` on
`ansible-survival-kit` plus `main` on `aia-instructor`. It creates or updates
only `aia-instructor/ISLAND_ACCESS.md`, with service links and account names.
Existing learner work is preserved. No passwords or answers are written to
Gitea. An unchanged guide produces no Git commit on rerun.

The playbook adds the student's repository link to relevant CTFd challenge
descriptions and invokes the retained empty-board content loader. It then
reconciles flag values through CTFd's API, patching existing flag IDs only when
values differ. The flag step plans all changes first and rejects missing or
ambiguous challenges and unexpected flag counts. It does not delete objects.
Use `--tags flags` for a flag-only update; preflight still runs. Populated
boards are preserved, including submissions and scores. Existing challenge
descriptions, points, hints, and prerequisites are not updated in place by this
entry point. It keeps the existing
`lab-user` CTFd account and `instructor-<guid>` Gitea account, and presents their
mapping in the access guide. It does not create AAP projects, job templates,
inventories, or credentials. Those resources remain separate from this CTFd/
Gitea configuration step.

Run the offline CTFd regression tests with `ansible-playbook`, GNU coreutils
`timeout`, PyYAML, and Jinja2 installed:

```bash
python3 -m unittest discover -s automation/ansible/tests -v
```

For legacy local playbook development, the following commands remain available;
they require the older `.cnv.env` layout and local Ansible dependencies:

```bash
cd ansible-testing
ansible-playbook deploy.yml --vault-password-file ../.vault-password
```

For tag-scoped updates (e.g., CTFd challenge changes only):

```bash
ansible-playbook deploy.yml --tags ctfd --vault-password-file ../.vault-password
```
