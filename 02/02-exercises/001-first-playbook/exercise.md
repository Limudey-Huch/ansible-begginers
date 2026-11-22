# Exercise 001 — Your First Playbook
**Lesson:** 02 — Playbooks & Practical Usage | **Level:** Beginner (start here)

---

## 🎯 Goal
Write and run the simplest possible playbook: one play, one task, against the inventory you already built in Lesson 01.

---

## 📋 Instructions

Run every command below from inside this exercise's own folder — `playbook.yml` is
referenced by a relative path, so the wrong working directory means "file not found":
```bash
cd .../ansible/courses/ansible/02/02-exercises/001-first-playbook   # the prefix depends on where you placed the course
```

This exercise has no inventory of its own — the playbook targets `hosts: web`, which is
the same `[web]` group you already built in Lesson 01's inventory. Set this once per
terminal session:
```bash
INV=../../../01/01-exercises/002-inventory-and-ping/inventory.ini
```

### Step 1 — Create `playbook.yml` (starter provided)
```yaml
---
- name: Install curl on web servers
  hosts: web
  become: true
  tasks:
    - name: Install curl
      apt:
        name: curl
        state: present
        update_cache: true
```

### Step 2 — Dry-run it first
```bash
ansible-playbook -i $INV playbook.yml --check
```

### Step 3 — Run it for real
```bash
ansible-playbook -i $INV playbook.yml
```

### Step 4 — Run it again
Notice the task now reports `ok` instead of `changed` — this is idempotency in action.

---

## ✅ Checklist
- [ ] `--check` run completes with no errors
- [ ] Real run shows `changed=1` the first time
- [ ] Second run shows `changed=0` (nothing to do)

---

## 💡 Hints
<details><summary>Hint 1 — "changed" every time</summary>
If a task reports `changed` on every run, the module isn't being used idempotently — double check you're using `state: present`, not re-running an imperative command.
</details>
