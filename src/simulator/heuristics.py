import re

DANGEROUS_PATTERNS = {
    "shell": [r"rm\s+-rf", r"chmod\s+777", r"mkfs", r"reboot", r"shutdown"],
    "sql": [r"DROP\s+TABLE", r"DELETE\s+FROM", r"TRUNCATE", r"ALTER\s+TABLE"],
    "infra": [r"terraform\s+destroy", r"kubectl\s+delete", r"aws\s+.*\s+delete"]
}

def analyze_payload(action_type: str, payload: str) -> dict:
    patterns = DANGEROUS_PATTERNS.get(action_type.lower(), [])
    
    matched_patterns = []
    for pattern in patterns:
        if re.search(pattern, payload, re.IGNORECASE):
            matched_patterns.append(pattern)
            
    if matched_patterns:
        return {"is_dangerous": True, "matches": matched_patterns}
    return {"is_dangerous": False, "matches": []}