# Module 05 — Customize and extend

### Brief Overview

Learners edit challenge definitions and apply a content update from the instructor workspace prepared in Module 4. They verify that the Warm Up solve created after the reset remains. Organizer ordering, post-deploy, and handout preparation are reference workflows for future events, outside the timed learner exercise.

### Audience and Time

- **Personas:** Solution Architects, TAMs, partner engineers
- **Prerequisites for this module:** Gameplay in Module 3; instructor workspace, CLI/vault setup, and one post-reset solve from Module 4
- **Estimated duration:** 20 minutes

### Learning Objectives

- Customize challenge definitions, points, categories, prerequisites, and hints
- Apply update-challenges.yml and verify an unchanged challenge's solve is retained
- Distinguish content updates, board resets, and organizer infrastructure provisioning
- Locate the reference workflow and handout generator for future customer events

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Review and edit challenge content | 7 min |
| 2 | Apply a content update and verify the retained solve | 8 min |
| 3 | Review organizer workflow and handout references | 5 min |

### Detailed Steps

1. Continue in aia-instructor and inspect roles/ctfd/vars/challenges.yml
2. Change Ansible Docs from 10 to 15 points; leave Write Your Name in the Sand unchanged for the preservation check
3. Review optional additions, encrypted flag edits, difficulty tiers, and verifier-dependent advanced challenges
4. Preview with ansible-playbook update-challenges.yml --check, then apply ansible-playbook update-challenges.yml
5. Verify new content and confirm the post-reset Warm Up solve remains
6. Explain that repricing can change scores, renaming creates a challenge, and removing hints removes associated purchases
7. Contrast the update with Module 4's deliberate deploy.yml reset; never reset during a customer competition
8. Review the organizer reference: leaderboard CI, linked student CIs, post-deploy configuration, and readiness checks before learners arrive
9. Review generate-handouts.yml, which creates Markdown service links and usernames; distribute passwords separately

### Key Takeaways

- Updates retain matching challenge IDs and solves; resets deliberately clear progress
- Accounts and infrastructure are retained by the learner toolkit
- Catalog provisioning and organizer post-deploy are preparation outside the two-hour training session

### Infrastructure Notes

- Use the personal OpenShift login and local lab-password vault file from Module 4
- Learners do not order or redeploy catalog items during this timed module
- Advanced verifier exercises require organizer deployment of the optional integration
