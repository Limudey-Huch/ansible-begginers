# Exercise 003 — Ad-hoc Commands
**Lesson:** 01 — Introduction to Ansible & Architecture | **Level:** Intermediate (builds on 002)

---

## 🎯 Goal
Go beyond `ping` — use ad-hoc commands to gather information and make real changes on your managed hosts, using the inventory from Exercise 002.

---

## 📋 Instructions

This exercise has no inventory of its own — it reuses the one from Exercise 002.
Set this once per terminal session:
```bash
INV=../002-inventory-and-ping/inventory.ini
```

### Step 1 — Gather facts
```bash
ansible web -i $INV -m setup | less
```
Find the values for `ansible_distribution` and `ansible_memtotal_mb`.

### Step 2 — Run a raw shell command
```bash
ansible web -i $INV -m command -a "uptime"
```

### Step 3 — Check disk usage on every host
```bash
ansible web -i $INV -m shell -a "df -h /"
```

### Step 4 — Install a package (requires privilege escalation)
```bash
ansible web -i $INV -m apt -a "name=curl state=present" --become
```
(Use the `yum` or `dnf` module instead of `apt` if your hosts are RHEL/CentOS-based.)

### Step 5 — Copy a file to every host
```bash
echo "hello from ansible" > hello.txt
ansible web -i $INV -m copy -a "src=hello.txt dest=/tmp/hello.txt" --become
```

---

## ✅ Checklist
- [ ] You can extract at least one fact value from `setup` output
- [ ] `curl` is installed and verified on every host (`ansible web -i $INV -m command -a "curl --version"`)
- [ ] `/tmp/hello.txt` exists on every host with the correct content

---

## 💡 Hints
<details><summary>Hint 1 — command vs shell module</summary>
`command` does not support shell features like pipes (`|`) or redirects (`>`). Use `shell` when you need those.
</details>

<details><summary>Hint 2 — become fails silently</summary>
If `--become` doesn't prompt but also doesn't apply changes, check whether passwordless sudo is configured for your SSH user, or add `--ask-become-pass`.
</details>
