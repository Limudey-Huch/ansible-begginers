# Test — Ansible + AWS: Cloud Provisioning
**Course:** Ansible | **Lesson:** 04

---

## Part A — Multiple Choice

**1. What is the key difference between "provisioning" and "configuration management"?**
- a. They are the same thing
- b. Provisioning creates the infrastructure itself (servers, networking); configuration management sets up software on servers that already exist ✓
- c. Configuration management is only for AWS
- d. Provisioning cannot be done with Ansible

**2. Why does `ec2_key` only return the private key material the first time it runs?**
- a. It's a bug
- b. AWS never stores the private key — it hands it to you once at creation, then forgets it ✓
- c. Ansible deletes it automatically
- d. It returns it every time

**3. What's the main advantage of an SG-to-SG rule (`group_name`/`group_id`) over a CIDR rule?**
- a. It's faster
- b. It allows traffic only from instances that are members of a specific security group, regardless of their changing IPs ✓
- c. It works across AWS accounts automatically
- d. It removes the need for a VPC

**4. Why does AWS SG-to-SG rule matching only work over an instance's private IP, not its public IP?**
- a. It doesn't — both work identically
- b. Public IP traffic effectively leaves and re-enters the VPC boundary, so AWS can no longer attribute it to a specific security group ✓
- c. Public IPs are always blocked by default
- d. Security groups only exist for private IPs

**5. What problem does dynamic inventory (`aws_ec2` plugin) solve that a static `inventory.ini` can't?**
- a. It's required for Ansible to work at all
- b. Static files go stale the moment an instance is recreated with a new IP — dynamic inventory queries AWS live, every run ✓
- c. Dynamic inventory is faster to type
- d. Static inventory can't use SSH

**6. Why tag every resource with the same `Project` value in this lesson?**
- a. AWS requires it
- b. It lets one teardown playbook find and delete everything this lesson created, regardless of which exercise created it ✓
- c. Tags make instances boot faster
- d. It's required for billing

---

## Part B — Open Questions

**1.** Explain why the radar app's `app.py` (API) and `poller.py` (data refresh) are two separate
processes instead of one Flask app that polls OpenSky on every request.
_Answer space:_

**2.** In the 3-tier radar deployment, trace the exact network path of one browser request for
`/api/aircraft`, naming every tier and protocol/port involved.
_Answer space:_

**3.** Why is a plaintext `radar_db_password` variable in a playbook a shortcut, not a real-world
practice? What would you use instead?
_Answer space:_

---

## Part C — Practical Task

Using what you learned in this lesson:

1. Write an `ec2_security_group` task for a new "cache" tier that should be reachable, on port
   6379, **only** from the existing app tier — not from the public internet, not from the db tier.
2. Write the one-line addition to a dynamic inventory's `keyed_groups` that would be needed if
   this new tier is tagged `Role: cache`.
3. Explain, in one or two sentences, why this new tier's security group rule should reference
   `radar-app-sg` by `group_name`, not by writing out the app instance's IP address directly.

**Success criteria:**
- [ ] Security group rule correctly scoped to port 6379 and the app tier's SG only
- [ ] Correctly identifies that `keyed_groups` already handles this automatically (no new line needed) — or if changes are proposed, they're accurate
- [ ] Explanation correctly identifies that IPs change on instance replacement, while the SG membership does not
