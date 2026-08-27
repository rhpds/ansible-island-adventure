# Module 05 — Customize and extend

### Brief Overview

This module teaches students how to modify Ansible Island Adventure for their specific customer or partner engagements. Students edit challenge definitions, adjust difficulty tiers, and re-run the idempotent deployer to apply changes to the live environment. The module covers state coordination — what the deployer manages vs. what accumulates at runtime — and how to take the deployment artifacts to a fresh RHDP-ordered environment for independent delivery.

### Audience and Time

- **Personas:** Solution Architects, TAMs, partner engineers
- **Prerequisites for this module:** Completion of Module 4 (firsthand experience with the challenges); understanding of the playbook structure from Module 3
- **Estimated duration:** 20 minutes

### Learning Objectives

- Configure challenge definitions, difficulty tiers, and content in the challenge variables files to tailor Ansible Island Adventure for a specific audience
- Re-deploy changes to the pre-deployed environment using the idempotent Ansible playbook, verifying that only modified components update while cached credentials and runtime state are preserved
- Distinguish deployer-managed state (challenges, configuration, player accounts) from runtime state (scores, submissions, leaderboard data) and explain the implications for re-deployment
- Demonstrate the artifact handoff workflow: ordering a fresh RHDP environment and deploying from scratch using the provided playbook and roles

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Modify challenge content | 7 min |
| 2 | Re-run the idempotent deployer | 6 min |
| 3 | State coordination and artifact handoff | 7 min |

### Detailed Steps

1. Open `roles/ctfd/vars/challenges.yml` and review the challenge definition structure: categories, point values, flags, hints, and difficulty assignments
2. Add a new challenge or modify an existing challenge's point value and hint text
3. Review `roles/ctfd/vars/challenges_advanced.yml` for advanced challenge definitions and understand how difficulty tiers are structured
4. Re-run the deployer with `ansible-playbook deploy.yml --tags ctfd` to apply only the CTFd changes
5. Observe that the playbook loads cached credentials from `player.creds` (no regeneration) and only updates CTFd configuration
6. Verify the changes in CTFd: confirm the new or modified challenge appears with the correct point value and hints
7. Confirm that existing runtime state — player scores, flag submissions, leaderboard positions — is unaffected by the re-deployment
8. Review what happens when running the full playbook (`ansible-playbook deploy.yml` without tags): all roles execute but converge to existing state except for the modified components
9. Discuss the fresh-environment workflow: ordering a new ROSA open environment from RHDP, receiving a fresh `rosa.creds`, and running `deploy.yml` from scratch — with no cached `player.creds`, the deployer generates new credentials automatically
10. Review the handout generation workflow (`generate-handouts.yml`) and how it uses player credentials to produce PDF handouts for distribution at customer events

### Key Takeaways

- Challenge content is defined in YAML variables files and can be customized per engagement without modifying the playbook or roles
- The deployer is idempotent: re-running it loads cached credentials and converges to the desired state — only changes are applied
- Runtime state (scores, submissions) lives in the CTFd database and is independent of the deployer — re-deploying does not reset player progress
- For customer events, the workflow is: order from RHDP → receive pre-deployed environment → customize challenges → distribute credentials and handouts

### Infrastructure Notes

- Re-running the deployer requires the same cluster access used during the initial deployment (credentials from rosa.creds)
- Tag-scoped runs (`--tags ctfd`) limit the blast radius to specific roles, reducing re-deployment time
- The `player.creds` cache-or-generate pattern ensures credential stability across re-runs
