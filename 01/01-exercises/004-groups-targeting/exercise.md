# Exercise 004 — Groups & Targeted Execution
**Lesson:** 01 — Introduction to Ansible & Architecture | **Level:** Intermediate (builds on 003)

---

## 🎯 Goal
Expand your inventory with multiple groups and practice targeting exactly the hosts you want — the foundation you'll need before writing playbooks in Lesson 02.

---

## 📋 Instructions

### Step 1 — Extend the inventory with two groups
Create `inventory_groups.ini` (starter provided):
```ini
[web]
web1 ansible_host=REPLACE_IP
web2 ansible_host=REPLACE_IP

[db]
db1 ansible_host=REPLACE_IP

[production:children]
web
db

[web:vars]
ansible_user=REPLACE_USER
role=frontend

[db:vars]
ansible_user=REPLACE_USER
role=backend
```

### Step 2 — Target each group independently
```bash
ansible web -i inventory_groups.ini -m ping
ansible db -i inventory_groups.ini -m ping
```

### Step 3 — Target the parent group (`production:children`)
```bash
ansible production -i inventory_groups.ini -m ping
```

### Step 4 — Use a host pattern to exclude a group
`!` is a special character in bash (history expansion) — wrap the pattern in **single**
quotes (double quotes won't protect it):
```bash
ansible 'all:!db' -i inventory_groups.ini -m ping
```

### Step 5 — Print the `role` variable per host
```bash
ansible all -i inventory_groups.ini -m debug -a "var=role"
```

---

## ✅ Checklist
- [ ] `production` successfully reaches both `web` and `db` hosts
- [ ] `all:!db` reaches only the web hosts
- [ ] The `role` variable prints correctly as `frontend` or `backend` per host

---

## 💡 Hints
<details><summary>Hint 1 — group of groups</summary>
`[production:children]` lists other *group names*, not hosts — this is how you build hierarchies.
</details>

<details><summary>Hint 2 — pattern syntax</summary>
`:` combines patterns (OR), `:!` excludes a group, `:&` intersects two groups.
</details>

<details><summary>Hint 3 — "event not found" error</summary>
That's bash, not Ansible — `!` triggers bash history expansion unless the whole pattern is
wrapped in single quotes: `'all:!db'`, not `"all:!db"` or `all:!db`.
</details>
