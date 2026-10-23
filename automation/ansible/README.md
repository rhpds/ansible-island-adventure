# rhpds.aia — Ansible Island Adventure Collection

This collection contains automation for deploying and configuring the Ansible Island Adventure CTF platform on OpenShift CNV.

## Roles

Catalog workload roles live in this directory:

- `roles/instructor_config/` — Instructor services and configuration, including CTFd, Gitea, AAP, and Keycloak integration
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

The CTFd challenge-count check allows 120 seconds per attempt and two retries,
with a 10-second delay between attempts. Override
`ctfd_challenge_check_timeout`, `ctfd_challenge_check_retries`, and
`ctfd_challenge_check_delay` when needed. Failed commands and missing or malformed
counts stop provisioning before archive import; their command diagnostics are
retained in the Ansible output.

Run the offline challenge-check regression tests with `ansible-playbook` and
PyYAML installed:

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
