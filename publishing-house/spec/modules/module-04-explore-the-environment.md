# Module 04 — Explore the environment

### Brief Overview

After playing, learners explore the architecture and switch to their instructor toolkit. They configure a personal OpenShift CLI login and lab-password vault file, inspect the board-management playbooks, and deliberately reset their own CTFd progress. The before/after comparison distinguishes a board reset from infrastructure redeployment.

### Audience and Time

- **Personas:** Solution Architects, TAMs, partner engineers
- **Prerequisites for this module:** Modules 1–3; saved gameplay results; personal service credentials
- **Estimated duration:** 20 minutes

### Learning Objectives

- Identify shared services, the personal CTFd namespace, and separately provisioned managed node
- Open the instructor workspace alongside the survival-kit workspace
- Configure personal oc login and a local vault-password file with the lab password
- Demonstrate what the board reset clears and what it preserves

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Architecture tour and administration access | 5 min |
| 2 | Instructor workspace, CLI login, and vault setup | 7 min |
| 3 | Playbook walkthrough, reset, and verification | 8 min |

### Detailed Steps

1. Keep the player session available and use a private browser window for CTFd administration
2. Inspect the personal CTFd namespace and service URLs; shared platform namespaces may be restricted
3. Copy the personal OpenShift login command without exposing its token
4. Open the personal aia-instructor Gitea repository in a second persistent Dev Spaces workspace using its devfile
5. Log in with oc and verify the instructor identity
6. Create the local .vault-password with the lab password, set mode 0600, and verify the encrypted instructor flags file
7. Inspect root deploy.yml, update-challenges.yml, shared discovery/content tasks, and challenge definitions
8. Run syntax and check mode and confirm that discovery selects the learner's own board
9. Apply deploy.yml for the deliberate post-game training reset; compare cleared solves, submissions, awards, and purchased hints with saved results
10. Verify retained accounts, profile changes, settings, challenge IDs, workspaces, VM, and AAP resources; resetting the board does not undo Apache deployment
11. As the player, submit DONE to Write Your Name in the Sand again, creating a solve for Module 5's preservation check

### Key Takeaways

- The toolkit manages personal board content rather than recreating catalog infrastructure
- Reset customer boards before a new session, never during scoring; the after-game reset here is an explicit training exercise
- Content updates retain progress; board resets clear it
- Use saved Module 3 results for later analysis, not the reset board

### Infrastructure Notes

- Two simultaneous workspaces use separate persistent storage
- Learners use personal identity and lab password; organizer cluster-admin credentials remain private
- Organizer post-deploy is separate from the learner toolkit's reset
