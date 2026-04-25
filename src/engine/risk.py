def calculate_risk(analysis_result: dict) -> tuple[int, str, str]:
    if analysis_result["is_dangerous"]:
        return 100, "CRITICAL", f"Matched destructive patterns: {', '.join(analysis_result['matches'])}"
    
    return 0, "LOW", "No destructive patterns detected"