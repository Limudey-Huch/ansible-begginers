# Lesson 01 — Introduction to Ansible & Architecture
**Course:** Ansible | **Duration:** ~3 hours

---

## 🎯 Learning Objectives
By the end of this lesson, students will be able to:
- Explain what Configuration Management is and why it matters
- Describe Ansible's agentless architecture (Control Node, Managed Nodes, SSH)
- Read and write a basic Ansible inventory file
- Run ad-hoc commands against one or more managed hosts
- Explain the role of YAML in Ansible

---

## 📋 Lesson Content

### 1. Why Configuration Management?
Before automation, servers were configured by hand — one SSH session at a time. As the number of servers grows, this becomes slow, inconsistent, and error-prone (the "snowflake server" problem).

**Key points:**
- Manual configuration doesn't scale and isn't repeatable
- Configuration Management tools describe the *desired state* of a system, then enforce it
- Ansible, Puppet, Chef, and SaltStack solve this problem, each with different trade-offs

**Comparison (visual slide):**
| Tool | Agent required? | Language |
|------|------------------|----------|
| Ansible | No (agentless) | YAML |
| Puppet | Yes | Puppet DSL |
| Chef | Yes | Ruby DSL |

---

### 2. What Is Ansible?
Ansible is an open-source automation tool for configuration management, application deployment, and orchestration. It connects to remote machines over SSH and executes tasks — no agent software needs to be installed on managed hosts.

**Key points:**
- Agentless: only SSH + Python are required on managed nodes
- Declarative: you describe *what* you want, not *how* to do it step by step
- Idempotent: running the same playbook twice produces the same result, with no unwanted side effects

---

### 3. Advantages & Disadvantages
**(Pros/cons slide)**

**Advantages:**
- Agentless — nothing to install or maintain on managed nodes
- Low learning curve — YAML is readable, even for non-programmers
- Push-based — you control exactly when changes happen
- Huge module ecosystem and active community

**Disadvantages:**
- Push-based also means it doesn't *continuously* enforce state like agent-based tools can (no built-in drift auto-correction without re-running)
- Performance over SSH is slower at very large scale (thousands of nodes) compared to agent-based pull models
- Windows support (WinRM) is less mature than Linux/SSH support
- Large, complex playbooks can become hard to maintain without discipline (roles, structure)

---

### 4. Where (and When) to Use Ansible
**(Concept slide)**

**Good fit:**
- Small to mid-size infrastructure (tens to low thousands of servers)
- Teams that want to get started quickly without agent rollout
- Provisioning, configuration management, and app deployment combined
- Environments with mixed OS (Linux servers + occasional Windows/network devices)

**Less ideal fit:**
- Massive, highly dynamic fleets needing constant self-healing (pure pull-based tools may fit better)
- Real-time/continuous enforcement requirements (pair Ansible with a scheduler/CI pipeline, or consider agent-based alternatives)

---

### 5. Architecture: Control Node & Managed Nodes
**(Dedicated architecture diagram slide)**

- **Control Node** — the machine where Ansible is installed and playbooks are run from
- **Managed Nodes** — the target servers being configured (no Ansible installation needed)
- **Connection** — SSH (Linux) or WinRM (Windows)
- **Inventory** — the file that tells Ansible which hosts exist and how to group them

```
Control Node  --SSH-->  Managed Node 1
              --SSH-->  Managed Node 2
              --SSH-->  Managed Node 3
```

---

### 6. The Inventory File
The inventory lists the hosts Ansible manages, optionally grouped by role or environment.

**Example (`inventory.ini`):**
```ini
[web]
web1.example.com
web2.example.com

[db]
db1.example.com

[web:vars]
ansible_user=ubuntu
```

**Key points:**
- Default format is INI, but YAML is also supported
- Groups let you target multiple hosts at once (`[web]`, `[db]`)
- Variables can be attached per host or per group

---

### 7. Ad-hoc Commands
Ad-hoc commands run a single task against one or more hosts without writing a full playbook — useful for quick checks and one-off operations.

**Example:**
```bash
# Check connectivity
ansible web -i inventory.ini -m ping

# Run a shell command
ansible web -i inventory.ini -m command -a "uptime"

# Install a package (requires privilege escalation)
ansible web -i inventory.ini -m apt -a "name=curl state=present" --become
```

**Key points:**
- `-m` selects the module (e.g. `ping`, `command`, `apt`)
- `-a` passes arguments to the module
- `--become` elevates privileges (like `sudo`)

---

### 8. YAML Basics
Ansible playbooks (covered in Lesson 02) are written in YAML. A quick primer:

```yaml
name: Example structure
items:
  - first
  - second
settings:
  key: value
  nested:
    another_key: another_value
```

**Key points:**
- Indentation (spaces, not tabs) defines structure
- Lists use `-`, mappings use `key: value`

---

## 🔗 Links & Resources
- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Inventory Guide](https://docs.ansible.com/ansible/latest/inventory_guide/index.html)

---

## 📝 Instructor Notes
- Emphasize "agentless" as Ansible's key differentiator early — it explains why SSH/Python are the only requirements.
- Live-demo the architecture diagram: SSH into 2-3 local VMs or containers if possible.
- Keep ad-hoc commands hands-on — students should run `ansible ... -m ping` themselves before moving to Lesson 02.
