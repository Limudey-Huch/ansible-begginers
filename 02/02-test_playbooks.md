# Test — Playbooks & Practical Usage
**Course:** Ansible | **Lesson:** 02

---

## Part A — Multiple Choice

**1. What is the correct relationship between a playbook, a play, and a task?**
- a. A task contains plays, which contain playbooks
- b. A playbook contains one or more plays, each containing one or more tasks ✓
- c. A play contains playbooks, which contain tasks
- d. They are interchangeable terms for the same thing

**2. What does the `--check` flag do when running a playbook?**
- a. Validates YAML syntax only
- b. Simulates the run without making real changes ✓
- c. Checks the Ansible version
- d. Runs only the first task

**3. When does a handler execute?**
- a. Before every task
- b. Only when notified by a task that reported a change, and only once per play ✓
- c. On every run, regardless of changes
- d. Only when `--check` is used

**4. What is the highest-precedence way to set a variable?**
- a. `vars:` inside the playbook
- b. `group_vars/` files
- c. `-e` on the command line ✓
- d. `host_vars/` files

**5. What is the main purpose of Ansible Roles?**
- a. To replace inventory files
- b. To organize tasks, variables, templates, and handlers into reusable units ✓
- c. To install Ansible itself
- d. To manage SSH keys

**6. In a multi-tier playbook with a backend play and a frontend play, why does play order matter?**
- a. It doesn't — Ansible runs plays in parallel by default
- b. Later plays may depend on state established by earlier plays (e.g. backend must be running before frontend proxies to it) ✓
- c. YAML requires alphabetical ordering
- d. Only the first play in a file is executed

---

## Part B — Open Questions

**1.** Explain why `copy`/`template` modules are preferred over `command: echo ... > file` for writing configuration files, in terms of idempotency and handler notifications.
_Answer space:_

**2.** A task notifies a handler, but the handler never runs. List three possible causes and how you would debug each one.
_Answer space:_

**3.** Describe, step by step, what happens when `ansible-playbook` executes a playbook with two plays, each targeting a different host group.
_Answer space:_

---

## Part C — Practical Task

Write a playbook with two plays:
1. A **backend** play (`hosts: backend`) that installs `redis-server` and ensures the service is started and enabled.
2. A **frontend** play (`hosts: frontend`) that installs `nginx`, deploys a templated config file using a variable for the backend's address, and restarts nginx via a handler only when the config changes.

**Success criteria:**
- [ ] Two distinct plays, each targeting the correct host group
- [ ] Backend play is idempotent (`state: present` / `state: started`)
- [ ] Frontend play uses a Jinja2 template, not a static `copy`
- [ ] A handler is defined and notified only on config change
