# Test — Introduction to Ansible & Architecture
**Course:** Ansible | **Lesson:** 01

---

## Part A — Multiple Choice

**1. What makes Ansible "agentless"?**
- a. It requires no network connection
- b. It needs no agent software installed on managed nodes, only SSH and Python ✓
- c. It only works on a single machine
- d. It has no command-line interface

**2. Which component initiates connections to managed nodes?**
- a. The Managed Node
- b. The Control Node ✓
- c. The Inventory file
- d. The YAML parser

**3. What protocol does Ansible use to connect to Linux managed nodes by default?**
- a. HTTP
- b. FTP
- c. SSH ✓
- d. RDP

**4. What is the purpose of the inventory file?**
- a. To store playbook variables only
- b. To list managed hosts and optionally group them ✓
- c. To define YAML syntax rules
- d. To install Ansible itself

**5. What does "idempotent" mean in the context of Ansible?**
- a. Tasks run faster each time
- b. Running the same playbook multiple times produces the same end state without unwanted side effects ✓
- c. Tasks can only run once
- d. Tasks require manual confirmation every time

**6. Which flag elevates privileges (like `sudo`) in an ad-hoc command?**
- a. `-m`
- b. `-a`
- c. `--become` ✓
- d. `-i`

---

## Part B — Open Questions

**1.** Explain, in your own words, the difference between Ansible and an agent-based tool like Puppet or Chef. What trade-off does agentless architecture bring?
_Answer space:_

**2.** Describe what happens when you run:
```bash
ansible web -i inventory.ini -m ping
```
What does Ansible actually do, step by step, from the Control Node's perspective?
_Answer space:_

**3.** Why is YAML indentation important in Ansible, and what commonly goes wrong because of it?
_Answer space:_

---

## Part C — Practical Task

Given three managed hosts (`app1`, `app2`, `db1`):

1. Write an inventory file with two groups: `app` (containing `app1`, `app2`) and `database` (containing `db1`).
2. Write the ad-hoc command to verify SSH connectivity to all hosts at once.
3. Write the ad-hoc command to install the `htop` package only on the `app` group, using privilege escalation.

**Success criteria:**
- [ ] Inventory correctly defines both groups
- [ ] Connectivity command targets `all` hosts
- [ ] Install command targets only `app`, uses the correct module and `--become`
