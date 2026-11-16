# Exercise 003 — Handlers
**Lesson:** 02 — Playbooks & Practical Usage | **Level:** Intermediate (builds on 002)

---

## 🎯 Goal
Deploy a config file and have the service automatically restart only when that file actually changes — the classic handler pattern.

---

## 📋 Instructions

This exercise has no inventory of its own — the playbook targets `hosts: web`, the
same `[web]` group from Lesson 01's inventory. Set this once per terminal session:
```bash
INV=../../../01/01-exercises/002-inventory-and-ping/inventory.ini
```

### Step 1 — Create a config file to deploy
`nginx_custom.conf` (starter provided) — a minimal custom nginx config.

### Step 2 — Write the playbook with a handler
Starter provided (`playbook.yml`):
```yaml
---
- name: Deploy custom nginx config
  hosts: web
  become: true
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
        update_cache: true

    - name: Deploy custom config
      copy:
        src: nginx_custom.conf
        dest: /etc/nginx/conf.d/custom.conf
      notify: Restart nginx

  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted
```

### Step 3 — Run it twice
```bash
ansible-playbook -i $INV playbook.yml
ansible-playbook -i $INV playbook.yml
```
Observe: the handler fires on the first run (file changed) but not the second (file unchanged).

### Step 4 — Change the config and re-run
Edit `nginx_custom.conf`, then run the playbook again — confirm the handler fires again.

---

## ✅ Checklist
- [ ] First run: `copy` task shows `changed`, handler runs, nginx restarts
- [ ] Second run (no edits): `copy` task shows `ok`, handler does **not** run
- [ ] After editing the file: handler runs again on the next execution

---

## 💡 Hints
<details><summary>Hint 1 — handler never runs</summary>
Check indentation — `handlers:` must be a sibling of `tasks:` under the same play, and the handler `name:` must exactly match the string passed to `notify:`.
</details>

<details><summary>Hint 2 — handler runs even with no changes</summary>
Handlers queue only when a task reports `changed`. If it fires every time, something in your task is not idempotent (e.g. using `command` to write the file instead of `copy`/`template`).
</details>
