# Exercise 001 — Your First EC2 Instance
**Lesson:** 04 — Ansible + AWS: Cloud Provisioning (Advanced) | **Level:** Advanced (start here)

---

## 🎯 Goal
Use Ansible — not the AWS Console, not Terraform — to create an SSH key pair, a security
group, and a real EC2 instance, then connect to it. This is *provisioning*, not
configuration: nothing exists yet until this playbook runs.

---

## ⚠️ Before you start
This creates **real, billable** AWS resources (a `t3.micro` instance is cheap, but not free
forever). **Always run Step 6 (teardown) when you're done** — don't leave it running overnight.

---

## 📋 Instructions

### Step 1 — Install the collections this lesson needs
Ansible core only ships generic modules (`apt`, `copy`, `service`...) — everything
AWS-specific comes from separate **collections** you install with `ansible-galaxy`,
the same way you'd `pip install` a Python package:
```bash
ansible-galaxy collection install amazon.aws community.aws community.postgresql
```
These also need `boto3`/`botocore` (AWS's own Python SDK — the collections call it
under the hood) available to the Python interpreter Ansible uses:
```bash
sudo apt install python3-boto3 python3-botocore
# or, if that's not available: python3 -m pip install --user boto3 botocore
```

### Step 2 — Sanity-check your AWS setup
```bash
aws sts get-caller-identity
ansible-galaxy collection list | grep aws
python3 -c "import boto3, botocore; print('ok')"
```
You should see your AWS account/user, both `amazon.aws` and `community.aws` listed, and `ok`.

### Step 3 — Provision
```bash
cd ~/00_devops_course_iccp/ansible/courses/ansible/04/04-exercises/001-first-ec2-instance
ansible-playbook provision.yml
```
Note the public IP in the final `debug` output.

### Step 4 — Connect
Give the instance ~30-60 seconds to finish booting (cloud-init), then:
```bash
ssh -i radar-course-key.pem ubuntu@<the-public-ip>
```

### Step 5 — Run it again (idempotency check)
```bash
ansible-playbook provision.yml
```
Check the AWS Console (or `aws ec2 describe-instances`) — confirm there's still only **one**
instance, not two. The `name` on `ec2_instance` is what Ansible uses to recognize "this already
exists."

### Step 6 — Tear down
```bash
ansible-playbook teardown.yml
```
Verify in the AWS Console that the instance is `terminated` and the security group/key pair are gone.

---

## ✅ Checklist
- [ ] `provision.yml` creates exactly one instance, one security group, one key pair
- [ ] You can SSH into the instance using the generated `.pem` file
- [ ] Running `provision.yml` a second time makes **zero** changes (idempotent)
- [ ] `teardown.yml` removes everything, leaving your AWS account clean

---

## 💡 Hints
<details><summary>Hint 1 — "UnauthorizedOperation" or permission errors</summary>
Your IAM user needs permissions for EC2 (RunInstances, CreateKeyPair, CreateSecurityGroup, etc.). If you hit this, check with whoever manages the AWS account about attaching an EC2-focused policy.
</details>

<details><summary>Hint 2 — SSH "Connection refused" right after provisioning</summary>
The instance is still booting. `wait: true` on `ec2_instance` only waits for the instance to reach "running" state — it does **not** wait for SSH/cloud-init to finish inside it. Give it a bit more time.
</details>

<details><summary>Hint 3 — teardown's security-group delete fails</summary>
AWS needs a few seconds after instance termination to fully detach the security group. Just rerun `teardown.yml` — the instance-termination part is already done, so it'll skip straight to the security group this time.
</details>
