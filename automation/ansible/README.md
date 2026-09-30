# rhpds.aia — Ansible Island Adventure Collection

This collection contains automation for deploying and configuring the Ansible Island Adventure CTF platform on OpenShift CNV.

## Roles

The primary automation lives in `ansible-testing/` and `collections/ansible_collections/rhpds/aia/` in the project root. This `automation/ansible/` directory is the publishing-house scaffolded placeholder.

For the actual deployment automation, see:

- `ansible-testing/deploy.yml` — Main deployment playbook
- `ansible-testing/roles/` — Deployment roles (cluster_setup, instructor, configure_ctfd, configure_gitea, configure_aap, shared_gitea)
- `collections/ansible_collections/rhpds/aia/` — Refactored collection with deploy_leaderboard and deploy_vms roles

## Usage

The deployment is triggered automatically by RHDP during environment provisioning. For manual runs:

```bash
cd ansible-testing
ansible-playbook deploy.yml --vault-password-file ../.vault-password
```

For tag-scoped updates (e.g., CTFd challenge changes only):

```bash
ansible-playbook deploy.yml --tags ctfd --vault-password-file ../.vault-password
```
