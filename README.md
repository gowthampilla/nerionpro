# 🛡️ Evalshq: Nerion Decision Infrastructure

**The Enterprise Pre-Execution Risk Engine for Autonomous AI Agents.**

[![Live API](https://img.shields.io/badge/API-Live-success)](#) [![Architecture](https://img.shields.io/badge/Architecture-BYOK-blue)](#) [![Latency](https://img.shields.io/badge/Latency-~1200ms-orange)](#) [![Status](https://img.shields.io/badge/Status-Production_Ready-green)](#)

Evalshq operates the **Nerion Engine**—a platform designed to bring absolute clarity to complex autonomous decisions. 

As AI agents ship to production, they are granted access to file systems, databases, and critical APIs. But agents hallucinate. They make destructive choices. Evalshq acts as a "Digital Supreme Court," intercepting agent commands, analyzing their intent, and detonating high-risk payloads in ephemeral cloud micro-VMs to mathematically prove the blast radius—all before the code ever touches your actual environment.

---

## 🧠 The Nerion Philosophy
Nerion is built on the premise of **Trust through Adversarial Verification**. We do not trust the agent's internal logic. We force the agent to submit its proposed actions to an isolated, adversarial environment where state changes are monitored, logged, and audited in real-time.

### Core Capabilities
* **Adversarial Intent Analysis:** Before code runs, our LLM layer evaluates the semantic intent of the payload.
* **Ephemeral Micro-VM Sandboxing:** If a command is flagged as `MEDIUM` risk or higher, it is deployed to a sterile, isolated Linux cloud environment.
* **Forensic Impact Auditing:** We inject "Ghost Files" into the sandbox to mirror your production state, run the payload, and check if critical systems were altered or destroyed.
* **Zero-Friction BYOK:** Bring Your Own Key architecture ensures your proprietary prompts and LLM keys are never stored on our servers.

---

## 🏗️ Architecture & Execution Flow

When your agent proposes an action, the Nerion Engine executes a strict, 4-step protocol:

1. **The Intercept (API Gateway):** Your agent sends the proposed command (e.g., `rm -rf /app/db/prod.sql`) and your OpenAI API key to the `/evaluate` endpoint.
2. **Intent Evaluation (The Brain):** The engine uses your key to query an adversarial LLM, evaluating the command for destructive potential.
3. **Cloud Detonation (The Sandbox):** If deemed risky, the engine connects to our cloud infrastructure, boots a secure micro-VM in <1 second, replicates your specified file paths, and executes the command.
4. **The Verdict:** The engine audits the sandbox. If files were destroyed or state was altered unexpectedly, it returns a `BLOCKED` verdict with a full forensic log.

---

## 🚀 Quick Start Integration

You require zero local infrastructure. No Docker, no SSH keys. Just the standard `requests` library.

### Python Example

```python
import requests
import os

API_URL = "[https://nerionpro.onrender.com/api/v1/evaluate](https://nerionpro.onrender.com/api/v1/evaluate)"

payload = {
    "agent_id": "production-finance-agent",
    "action_type": "shell",
    "payload": "rm -rf /home/user/app/db/prod.sql",
    "context_files": [
        "/home/user/app/config/.env", 
        "/home/user/app/db/prod.sql"
    ],
    "user_api_key": os.getenv("OPENAI_API_KEY") # BYOK Auth
}

response = requests.post(API_URL, json=payload)
decision = response.json()

if decision["decision"] == "ALLOW":
    print("✅ Nerion Approved: Executing command...")
else:
    print(f"❌ Nerion Blocked: {decision['reason']}")
    print(f"🔍 Forensic Audit: {decision['simulation_result']['impact_report']}")
