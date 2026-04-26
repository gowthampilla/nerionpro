🛡️ Evalshq: Nerion Decision Infrastructure

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
📖 API ReferencePOST /api/v1/evaluateThe core evaluation endpoint for all agent proposals.Request Body (JSON)ParameterTypeRequiredDescriptionagent_idstringYesA unique identifier for the agent proposing the action.action_typestringYesThe type of execution (e.g., shell, python, sql).payloadstringYesThe exact command or code the agent intends to run.context_filesarrayNoA list of critical file paths (e.g., ["/app/.env"]) to inject into the sandbox to test for destructive impact.user_api_keystringYesYour OpenAI API key for processing the adversarial intent analysis (BYOK).Response Body (JSON)JSON{
  "risk_score": 95,
  "risk_level": "CRITICAL",
  "decision": "BLOCK",
  "reason": "🚨 CRITICAL: Deleted /home/user/app/db/prod.sql | This command permanently deletes a critical database file.",
  "simulation_result": {
    "observation": "(No console output)",
    "impact_report": "CRITICAL: Deleted /home/user/app/db/prod.sql",
    "exit_code": 0
  }
}
🔒 Security & Privacy (BYOK)Evalshq operates on a strict Bring Your Own Key (BYOK) model.Zero Logging: We do not log or store your user_api_key in our databases. It is used strictly in-memory during the lifecycle of the request.Ephemeral Environments: The micro-VMs spun up to test your agent's code are physically destroyed immediately after the exit code is returned. No residual data survives.No Training: We do not use your agent's commands, payloads, or architecture to train underlying models.💻 Local Development & Self-HostingIf you wish to run the Nerion Engine locally for development:Clone the Repository:Bashgit clone [https://github.com/yourusername/nerionpro.git](https://github.com/yourusername/nerionpro.git)
cd nerionpro
Install Dependencies:Bashpip install -r requirements.txt
Environment Setup:Create a .env file in the root directory:Code snippetE2B_API_KEY=your_sandbox_infrastructure_key
Run the API:Bashcd src
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
⚖️ LicenseApache License 2.0Copyright 2026 Evalshq (Nerionpro)Licensed under the Apache License, Version 2.0 (the "License");you may not use this file except in compliance with the License.You may obtain a copy of the License athttp://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, softwaredistributed under the License is distributed on an "AS IS" BASIS,WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.See the License for the specific language governing permissions andlimitations under the License.
