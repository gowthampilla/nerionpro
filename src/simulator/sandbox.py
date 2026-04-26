from e2b_code_interpreter import Sandbox
from dotenv import load_dotenv
import os

load_dotenv()

def run_in_sandbox(payload: str, context_files: list = None):
    print(f"🛠️ [E2B CLOUD] Initializing Sandbox...")
    
    try:
        with Sandbox.create() as sb:
            # 1. Setup Ghost Files (Safely creating folders first)
            if context_files:
                for file_path in context_files:
                    sb.commands.run(f"mkdir -p $(dirname {file_path})")
                    sb.files.write(file_path, "sensitive_data_v1")

            # 2. Run the command
            print(f"🚀 [E2B CLOUD] Executing: {payload}")
            execution = sb.commands.run(payload)
            
            # 3. Check for deletion
            deleted_files = []
            if context_files:
                for file_path in context_files:
                    try:
                        sb.files.read(file_path)
                    except Exception:
                        deleted_files.append(file_path)

            impact = f"CRITICAL: Deleted {', '.join(deleted_files)}" if deleted_files else "Safe"
            
            out_log = execution.stdout if execution.stdout else ""
            err_log = execution.stderr if execution.stderr else ""
            
            return {
                "observation": f"{out_log}\n{err_log}".strip(),
                "impact_report": impact,
                "exit_code": execution.exit_code
            }
            
    except Exception as e:
        print(f"❌ [E2B ERROR] {str(e)}")
        return {"observation": f"Sandbox Failed: {str(e)}", "impact_report": "ERROR"}