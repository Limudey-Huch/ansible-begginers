# Exercise 002 — Variables & Multiple Tasks
**Lesson:** 02 — Playbooks & Practical Usage | **Level:** Beginner-Intermediate (builds on 001)

---

## 🎯 Goal
Extend your first playbook: install and start a package whose name comes from a variable, and chain multiple tasks together.

---

## 📋 Instructions

This exercise has no inventory of its own — the playbook targets `hosts: web`, the
same `[web]` group from Lesson 01's inventory. Set this once per terminal session:
```bash
INV=../../../01/01-exercises/002-inventory-and-ping/inventory.ini
```

### Step 1 — Add variables and a second task
A starter file is provided (`playbook.yml`):
```yaml
---
- name: Install and start a web server
  hosts: web
  become: true
  vars:
    package_name: nginx
    service_name: nginx
  tasks:
    - name: Install package
      apt:
        name: "{{ package_name }}"
        state: present
        update_cache: true

    - name: Ensure service is running and enabled
      service:
        name: "{{ service_name }}"
        state: started
        enabled: true
```

### Step 2 — Override a variable from the command line
Overriding with the *same* value (`nginx`) wouldn't prove anything — you need a
**different** value to actually see the override take effect. Use `vsftpd` (an FTP
server, on a different port, so it won't conflict with the nginx you just started):
```bash
ansible-playbook -i $INV playbook.yml -e "package_name=vsftpd service_name=vsftpd"
```
Note both variables are overridden together — if you only overrode `package_name`,
the second task would still try to manage the `nginx` service (from the unchanged
default), which isn't what you installed.

### Step 3 — Verify the result
```bash
ansible web -i $INV -m command -a "systemctl is-active nginx"
ansible web -i $INV -m command -a "systemctl is-active vsftpd"
```
Both should report `active` — nginx from Step 1's default run, vsftpd from Step 2's override.

---

## ✅ Checklist
- [ ] Playbook runs successfully using the `vars` block (installs & starts nginx)
- [ ] `-e` on the command line successfully overrides **both** variables (installs & starts vsftpd instead)
- [ ] `systemctl is-active nginx` **and** `systemctl is-active vsftpd` both report `active`

---

## 💡 Hints
<details><summary>Hint 1 — variable not substituted</summary>
Jinja2 expressions need to be quoted when they are the entire value: `name: "{{ package_name }}"`, not `name: {{ package_name }}`.
</details>

<details><summary>Hint 2 — precedence</summary>
Command-line `-e` variables have the highest precedence — they always win over `vars:` in the playbook.
</details>
