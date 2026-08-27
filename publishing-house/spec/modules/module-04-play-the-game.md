# Module 04 — Play the game

### Brief Overview

This is the core hands-on module. Attendees receive handouts and play through Ansible Island Adventure as participants would at a customer event. They work through challenges across six categories of increasing complexity, experience the scoring and hint system firsthand, and debrief on which challenges resonate with different audiences. Instructors circulate to assist, modeling the facilitation experience.

### Audience and Time

- **Personas:** Solution Architects, TAMs, partner engineers
- **Prerequisites for this module:** Completion of Module 3 (environment explored and verified); working knowledge of Ansible playbooks, roles, and inventories; basic familiarity with the Ansible Automation Platform controller
- **Estimated duration:** 45 minutes

### Learning Objectives

- Demonstrate proficiency with the Ansible Island Adventure challenge progression by completing challenges across all six categories: Warm Up, Let's get started, At the Beach, Treasure Hunt, Side Quest, and Trivia
- Explore the CTFd scoring platform from the participant perspective, including flag submission, hint usage, and leaderboard tracking
- Build hands-on experience with Ansible Automation Platform capabilities exercised by the challenges: CLI operations, Vault decryption, controller project and job template creation, and web application deployment
- Analyze the scoring methodology and identify which challenge types and difficulty levels resonate with different audience profiles

### Lab Structure

| Section | Title | Duration |
|---------|-------|----------|
| 1 | Receive handouts and orientation | 3 min |
| 2 | Warm Up challenges | 5 min |
| 3 | Let's get started challenges | 5 min |
| 4 | At the Beach challenges | 7 min |
| 5 | Treasure Hunt challenges | 12 min |
| 6 | Side Quest and Trivia | 8 min |
| 7 | Debrief and discussion | 5 min |

### Detailed Steps

1. Receive the player handout with credentials, shortened URLs, and challenge instructions
2. Log into CTFd with the assigned player credentials
3. Complete the **Warm Up** challenges: set up your account, find Ansible documentation, and locate collections on Ansible Galaxy or Automation Hub
4. Complete the **Let's get started** challenges: log into VSCode Server, discover the installed Ansible core version, and identify the Ansible Automation Platform version
5. Complete the **At the Beach** challenges: clone repositories from Gitea, run playbooks from the CLI, and decrypt Ansible Vault secrets to retrieve flags
6. Complete the **Treasure Hunt** challenges: create projects in the Ansible Automation Platform controller, configure vault credentials, build job templates, and deploy a web application
7. Explore the **Side Quest**: launch and interact with the Ansible Quest interactive video game
8. Answer the **Trivia** challenges: test knowledge of Ansible history and ecosystem
9. Submit flags in CTFd after each completed challenge and observe score updates on the leaderboard
10. Review the scoring methodology with the group: how points are assigned, how hints affect scores, and how the leaderboard drives competition
11. Discuss as a group which challenges resonated most and why, and how different customer audiences might respond to different challenge categories

### Key Takeaways

- Playing through the event as a participant is essential for effective facilitation — instructors must know the challenges firsthand
- The challenge progression moves from basic Ansible awareness through CLI proficiency to controller orchestration, covering a wide skill spectrum
- The scoring and hint system balances challenge difficulty with accessibility, keeping all skill levels engaged
- Understanding which challenges resonate with different audiences helps facilitators customize and pace future customer events

### Infrastructure Notes

- Each participant uses their own player credentials provided by the pre-deployed environment
- Challenges interact with CTFd (flag submission and scoring), Gitea (repository cloning), VSCode Server (CLI work), and the Ansible Automation Platform controller (projects, templates, credentials)
- The Side Quest (Ansible Quest video game) runs as a separate application accessible via an OpenShift route
- All challenge infrastructure is pre-deployed by RHDP and should be fully operational
