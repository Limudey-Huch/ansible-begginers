# Lesson 02 — Playbooks & Practical Usage
**Course:** Ansible | **Duration:** ~3 hours

---

## 🎯 Learning Objectives
By the end of this lesson, students will be able to:
- Explain the structure of an Ansible Playbook (plays, tasks, modules)
- Write and run a playbook using `ansible-playbook`
- Use variables to make playbooks reusable
- Use handlers to react to changes (e.g. restart a service)
- Describe what Roles are and when to use them
- Build a small multi-tier deployment (frontend + backend)

---

## 📋 Lesson Content

### 1. From Ad-hoc to Playbooks
Ad-hoc commands (Lesson 01) are great for one-off tasks, but real automation needs repeatable, version-controlled definitions. That's what Playbooks are for.

**Key points:**
- A playbook is a YAML file describing one or more **plays**
- A play maps a group of hosts to a list of **tasks**
- Each task calls one **module** (e.g. `apt`, `copy`, `service`)

---

### 2. Anatomy of a Playbook
```yaml
---
- name: Configure web servers
  hosts: web
  become: true
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present

    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: true
```

**Key points:**
- `hosts` — which inventory group this play targets
- `become` — whether to escalate privileges for this play
- `tasks` — an ordered list, executed top to bottom
- Each task should have a descriptive `name`

---

### 3. Running a Playbook
```bash
ansible-playbook -i inventory.ini site.yml

# Dry run (no changes made)
ansible-playbook -i inventory.ini site.yml --check

# Limit to one host or group
ansible-playbook -i inventory.ini site.yml --limit web1
```

**Key points:**
- `--check` simulates the run — essential before touching production
- `--limit` restricts execution without editing the playbook

---

### 4. Variables
Variables let the same playbook adapt to different environments.

```yaml
- name: Install a specific package version
  hosts: web
  vars:
    package_name: nginx
    package_state: present
  tasks:
    - name: Install package
      apt:
        name: "{{ package_name }}"
        state: "{{ package_state }}"
```

**Key points:**
- Variables can live in the playbook, in `group_vars/`, or in `host_vars/`
- `{{ }}` is Jinja2 templating syntax

---

### 5. Handlers
Handlers run only when **notified** by a task that reported a change — commonly used to restart a service after its config file changes.

```yaml
tasks:
  - name: Deploy nginx config
    copy:
      src: nginx.conf
      dest: /etc/nginx/nginx.conf
    notify: Restart nginx

handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
```

**Key points:**
- Handlers run once, at the end of the play, even if notified multiple times
- They only run if the notifying task actually changed something

---

### 6. Playbook Execution Flow
**(Dedicated flow-diagram slide)**

```
Parse playbook → For each play:
  Gather facts → Run tasks in order →
  Task changes something? → Queue notified handler →
  All tasks done → Run queued handlers → Report results
```

---

### 7. A Glimpse at Roles
As playbooks grow, Roles organize tasks, variables, templates, and handlers into reusable, shareable units with a standard directory layout (`roles/webserver/tasks/main.yml`, etc.). Full Role authoring is a natural next topic beyond this course.

---

### 8. Multi-Tier Example: Frontend + Backend
**(Dedicated architecture/comparison visual slide)**

A realistic playbook often targets more than one tier:
```yaml
- name: Configure backend app
  hosts: backend
  become: true
  tasks:
    - name: Install Node.js
      apt:
        name: nodejs
        state: present
    - name: Start app service
      service:
        name: myapp
        state: started
        enabled: true

- name: Configure frontend reverse proxy
  hosts: frontend
  become: true
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    - name: Deploy reverse proxy config
      template:
        src: reverse_proxy.conf.j2
        dest: /etc/nginx/sites-enabled/default
      notify: Restart nginx

handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
```

**Key points:**
- One playbook, two plays, two different host groups
- The frontend play depends logically on the backend already running (order matters)

---

## 🔗 Links & Resources
- [Ansible Playbooks Guide](https://docs.ansible.com/ansible/latest/playbook_guide/index.html)
- [Ansible Handlers](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html)
- [Ansible Roles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)

---

## 📝 Instructor Notes
- Build the playbook live, incrementally: start with one task, run it, then add the next — mirrors how students should work too.
- Always demo `--check` before a real run to build the habit of dry-running changes.
- Save the multi-tier example for last — it's the capstone that ties Lesson 01 (groups) and Lesson 02 (playbooks) together.
