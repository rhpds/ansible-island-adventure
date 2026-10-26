# rhpds.aia — Ansible Island Adventure Collection

This collection contains automation for deploying and configuring the Ansible Island Adventure CTF platform on OpenShift CNV.

## Roles

Catalog workload roles live in this directory:

- `roles/instructor_config/` — Instructor services and access, including CTFd bootstrap, Gitea, AAP, and Keycloak integration
- `roles/keycloak_ocp_logout_fix/` — Keycloak/OpenShift logout configuration

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
collections, Python `kubernetes` and `PyYAML`, and GNU coreutils `timeout` on
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
