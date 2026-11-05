# Module 03 — Play the game

### Brief Overview

Learners play as customer participants before opening the instructor toolkit or answer vault. They use their CTFd player account, personal Gitea repository, Ansible Survival Kit Dev Spaces workspace, and AAP organization. The organizer has already loaded challenges and configured the AAP inventory and Machine credential.

### Audience and Time

- **Personas:** Solution Architects, TAMs, partner engineers
- **Prerequisites for this module:** Modules 1–2; organizer readiness checks complete; personal service credentials; basic Ansible knowledge
- **Estimated duration:** 50 minutes, including setup and debrief

### Learning Objectives

- Experience scoring, hints, and challenge progression as a participant
- Run selected CLI, Vault, and AAP exercises using the survival kit
- Recognize participant access and pacing issues relevant to facilitation
- Save gameplay observations before the later training-board reset

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Participant access and survival-kit workspace setup | 10 min |
| 2 | Scored play, including Warm Up | 35 min |
| 3 | Debrief and save results | 5 min |

### Detailed Steps

1. Sign in to CTFd as the player and verify personal Gitea, AAP, and Dev Spaces access
2. Open the personal survival-kit repository's main branch in Dev Spaces using its Ansible-enabled devfile; wait for startup and collection installation
3. Start one 35-minute scoring window after access is ready, including all Warm Up submissions
4. Receive the unlock key from the session facilitator; leave instructor toolkit and answer-vault setup until Module 4
5. Select challenges appropriate to experience and pace: discover versions, run local playbooks, decrypt a challenge vault with its documented passphrase, or create AAP projects and templates
6. For Apache, use the prepared Island Adventure inventory and Managed Node SSH credential, the challenge's AAP vault credential, and privilege escalation
7. After Apache succeeds, open the VM-specific HTTPS treasure URL; use SSH only on older deployments without that URL
8. Stop submissions at the end of scored play; completing every exercise is not required
9. Save final score, solved challenges/categories, hints, and blockers for Modules 4 and 6; keep credentials and tokens out of screenshots

### Key Takeaways

- Participant experience precedes event administration
- Instructor CLI login and answer-vault setup come later; challenge vaults use their documented passphrases
- Setup and debrief are outside the scored window
- Save gameplay notes before Module 4 clears board progress

### Infrastructure Notes

- Catalog provisioning and organizer post-deploy must finish before this module
- Learners have personal training boards; customer events normally use a shared board
- No catalog deployment or instructor playbook run occurs in this module
