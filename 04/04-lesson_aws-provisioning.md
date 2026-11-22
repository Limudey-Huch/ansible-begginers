# Lesson 04 — Ansible + AWS: Cloud Provisioning (Advanced)
**Course:** Ansible | **Duration:** ~3 hours | **Builds on:** Lesson 03 (Terraform + Ansible basics)

---

## 🎯 Learning Objectives
Lesson 03 kept infrastructure and configuration cleanly separate: Terraform created the
servers, Ansible only configured them. This lesson goes deeper into what Ansible itself can
do on the AWS side — provisioning the infrastructure too, not just configuring it — plus the
AWS-specific mechanics real teams rely on (dynamic inventory, SG-to-SG rules, tagging).

By the end of this lesson, students will be able to:
- Explain the difference between *configuration management* (Lessons 01-02) and *provisioning* (this lesson)
- Provision real EC2 instances from a playbook using the `amazon.aws.ec2_instance` module
- Create and manage an SSH key pair with Ansible
- Design Security Groups, including SG-to-SG rules (not just CIDR ranges)
- Use **dynamic inventory** (the `aws_ec2` plugin) instead of a hand-written `inventory.ini`
- Tag cloud resources for tracking and safely tear them all down when done

---

## 📋 Lesson Content

### 1. Configuration Management vs. Provisioning
Lessons 01-02 assumed the servers already existed — Ansible only *configured* them.
**Provisioning** is a step earlier: creating the servers themselves (and their
networking, security groups, storage, etc.) before any configuration happens.

**Key points:**
- Ansible can do both — the same tool, different modules (`amazon.aws.*` instead of `apt`/`service`)
- Other tools specialize in provisioning only (Terraform, CloudFormation, Pulumi) — many real
  teams use Terraform for provisioning and Ansible for configuration. Both approaches are valid;
  this lesson shows Ansible doing both so you understand the full picture.
- Provisioning cloud resources costs real money the moment they exist — **always tear down**
  what you created when you're done (Step 6 of every exercise here)

---

### 2. AWS Setup — What Ansible Needs
```bash
aws sts get-caller-identity     # confirms your AWS CLI credentials work
ansible-galaxy collection list | grep aws    # amazon.aws + community.aws must be installed
python3 -c "import boto3"       # the AWS collections call boto3/botocore under the hood
```

**Key points:**
- Ansible's AWS modules don't talk to AWS directly — they go through `boto3` (AWS's own Python SDK)
- Credentials are read the same way the AWS CLI reads them (`~/.aws/credentials`, env vars, or an IAM role) — you never put keys in a playbook
- `amazon.aws` = core modules (EC2, VPC, security groups...), `community.aws` = everything else AWS

---

### 3. Provisioning an EC2 Instance
```yaml
- name: Launch a web server
  amazon.aws.ec2_instance:
    name: "radar-web"
    key_name: "{{ key_name }}"
    instance_type: t3.micro
    image_id: ami-0848826c0bc5f2e6c
    region: eu-north-1
    tags:
      Project: ansible-course-radar
    security_group: "radar-web-sg"
    wait: true
  register: web_instance
```

**Key points:**
- `wait: true` makes Ansible wait until the instance is actually running before moving on
- This task is **idempotent** by `name` — running it again won't create a second instance,
  it'll recognize the existing one (the same principle from Lesson 01/02, now applied to infrastructure itself)
- `register` captures the result (including the new public IP) for later tasks to use

---

### 4. SSH Key Pairs, Managed by Ansible
```yaml
- name: Create an EC2 key pair
  amazon.aws.ec2_key:
    name: radar-course-key
    region: eu-north-1
  register: ec2_key

- name: Save the private key locally
  ansible.builtin.copy:
    content: "{{ ec2_key.key.private_key }}"
    dest: "./radar-course-key.pem"
    mode: '0400'
  when: ec2_key.key.private_key is defined
```

**Key points:**
- AWS only returns the private key material **once**, at creation time — the `when:` guard
  means this task only writes the file the first time (on later runs, `ec2_key.key.private_key` is undefined)
- `mode: '0400'` — SSH refuses keys that are readable by anyone but the owner

---

### 5. Security Groups: CIDR vs. SG-to-SG Rules
**(Dedicated architecture/comparison slide-equivalent — see diagram below)**

```yaml
- name: Web tier security group (public)
  amazon.aws.ec2_security_group:
    name: radar-web-sg
    rules:
      - proto: tcp
        ports: [22, 80]
        cidr_ip: "{{ my_ip }}/32"   # SSH only from your own IP
      - proto: tcp
        ports: [80]
        cidr_ip: 0.0.0.0/0          # HTTP open to everyone

- name: App tier security group (private)
  amazon.aws.ec2_security_group:
    name: radar-app-sg
    rules:
      - proto: tcp
        ports: [5000]
        group_name: radar-web-sg    # only the web tier can reach the app tier
```

**Key points:**
- A CIDR rule (`cidr_ip`) allows traffic from an IP *range* — fine for public-facing ports
- An SG-to-SG rule (`group_name`/`group_id`) allows traffic only from instances in *another
  security group* — this is how you keep your app and database tiers unreachable from the
  public internet, even though they're technically "in the cloud"

---

### 6. Static vs. Dynamic Inventory
**(Dedicated diagram slide)**

In Lessons 01-02 you wrote `inventory.ini` by hand, with fixed IPs. On AWS, IPs change every
time an instance is (re)launched — a static file would be stale immediately.

```yaml
# inventory.aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - eu-north-1
filters:
  tag:Project: ansible-course-radar
keyed_groups:
  - key: tags.Role
    prefix: role
```

```bash
ansible-inventory -i inventory.aws_ec2.yml --graph
ansible role_web -i inventory.aws_ec2.yml -m ping
```

**Key points:**
- The inventory is generated **live**, every run, by querying the AWS API — never goes stale
- `keyed_groups` auto-creates groups from EC2 tags (e.g. a `Role: web` tag creates a `role_web` group) — no manual `[web]` sections needed
- This is how real-world Ansible+cloud setups work — static `inventory.ini` was a teaching stepping stone

---

### 7. Tagging for Safe Teardown
Every resource this lesson creates gets `Project: ansible-course-radar`. That one tag is what
lets a single playbook find and delete *everything*, regardless of which exercise created it:
```bash
ansible-playbook teardown.yml
```
**Always run teardown when you're done for the day** — an EC2 instance left running bills you
for every hour, even if nobody is using it.

---

## 🔗 Links & Resources
- [amazon.aws collection docs](https://docs.ansible.com/ansible/latest/collections/amazon/aws/)
- [aws_ec2 inventory plugin](https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_ec2_inventory.html)

---

## 📝 Instructor Notes
- Say the cost warning out loud, more than once. A `t3.micro` is cheap, but "cheap and forgotten" is how bills happen.
- Live-demo the teardown playbook running successfully *before* letting students provision anything themselves — they should see it works and trust it.
- The radar capstone (Exercise 004) is the payoff for the whole course: real cloud infra, a self-contained live-moving simulation, a real multi-tier deploy. Budget extra time for it.
