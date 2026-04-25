import docker
import time

client = docker.from_env()

def run_in_sandbox(payload: str, context_files: list = None):
    container_name = f"nerion-sandbox-{int(time.time())}"
    
    # 1. SETUP: Create Ghost Files (using double quotes for internal echo)
    setup_cmd = ""
    if context_files:
        setup_parts = [f"mkdir -p $(dirname {f}) && touch {f}" for f in context_files]
        setup_cmd = " && ".join(setup_parts) + ' && echo "---GHOST_FILES_CREATED---" && '

    # 2. CHECK: Verify if files survived (using double quotes for internal echo)
    # 2. CHECK: Verify if files survived
    check_cmd = ""
    if context_files:
        check_parts = [f'([ -f {f} ] || echo "VERIFIED_DELETED:{f}")' for f in context_files]
        check_cmd = " && ".join(check_parts)
    
    # --- NEW: Clean the payload to prevent double semicolons ---
    clean_payload = payload.strip().rstrip(";")
    
    # 3. CONSTRUCT: The full shell script
    full_cmd = f'sh -c "{setup_cmd} {clean_payload} ; echo ---RESULT--- ; {check_cmd}"'

    print(f"🛠️ [SANDBOX] Executing Raw Script: {full_cmd}")

    try:
        container = client.containers.run(
            "alpine",
            command=full_cmd,
            name=container_name,
            detach=True,
            network_disabled=True,
            mem_limit="64m"
        )
        
        container.wait(timeout=5)
        raw_logs = container.logs().decode("utf-8").strip()
        
        print(f"📄 [RAW SANDBOX LOGS]:\n{raw_logs}\n{'-'*30}")
        
        container.remove(force=True)

        # Parse logic: Look for our specific VERIFIED_DELETED tag
        deleted = [line.split(":")[1] for line in raw_logs.split("\n") if "VERIFIED_DELETED:" in line]

        return {
            "status": "success",
            "observation": raw_logs.split("---RESULT---")[0].strip() if "---RESULT---" in raw_logs else raw_logs,
            "impact_report": f"DELETED: {', '.join(deleted)}" if deleted else "No files affected"
        }

    except Exception as e:
        return {"status": "error", "observation": str(e), "impact_report": "Sandbox Crash"}