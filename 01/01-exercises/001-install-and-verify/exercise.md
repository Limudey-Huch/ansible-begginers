# Exercise 001 — Install Ansible & Verify
**Lesson:** 01 — Introduction to Ansible & Architecture | **Level:** Beginner (start here)

---

## 🎯 Goal
Get Ansible installed on your control node and confirm it works, before touching any managed hosts.

---

## 📋 Instructions

### Step 1 — Install Ansible
On your control node (your laptop, a VM, or a container):
```bash
# Debian/Ubuntu
sudo apt update && sudo apt install -y ansible

# macOS (Homebrew)
brew install ansible

# Any OS via pip
python3 -m pip install --user ansible
```

### Step 2 — Verify the installation
```bash
ansible --version
```

### Step 3 — Inspect what got installed
```bash
ansible-doc -l | head -20     # list available modules
which ansible-playbook
```

---

## ✅ Checklist
- [ ] `ansible --version` prints a version number with no errors
- [ ] You can locate the `ansible.cfg` config file path printed by `ansible --version`
- [ ] `ansible-doc -l` lists available modules

---

## 💡 Hints
<details><summary>Hint 1 — command not found</summary>
Make sure the Python `bin` directory is on your `PATH` if you installed via `pip --user`.
</details>

<details><summary>Hint 2 — multiple Python versions</summary>
Use `python3 -m pip` explicitly rather than plain `pip` to avoid installing against the wrong Python interpreter.
</details>
