def enforce_policy(risk_level: str) -> str:
    if risk_level in ["HIGH", "CRITICAL"]:
        return "BLOCK"
    elif risk_level == "MEDIUM":
        return "REQUIRE_APPROVAL"
    return "ALLOW"