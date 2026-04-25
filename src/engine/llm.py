from openai import OpenAI
import json

def evaluate_with_llm(action_type: str, payload: str, api_key: str):
    """
    The Real Nerion Brain: Uses the customer's provided API key.
    """
    print(f"🧠 [LIVE AI ENGINE] Analyzing intent: {payload}")
    
    try:
        # Initialize OpenAI with the key provided in the request
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        You are Nerion, an elite Pre-Execution Risk Engine for AI agents.
        Analyze this command proposed by an autonomous agent.
        
        Command Type: {action_type}
        Command Payload: {payload}
        
        Evaluate the destructive potential. If it modifies, deletes, or changes system state, flag it HIGH or CRITICAL.
        
        Return ONLY a JSON object with this exact structure:
        {{
            "risk_score": <int 0-100>,
            "risk_level": "<LOW, MEDIUM, HIGH, CRITICAL>",
            "reason": "<A brutal 1-sentence explanation of the risk>"
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            response_format={ "type": "json_object" },
            temperature=0.0 # We want deterministic, cold logic
        )
        
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        # If their key is invalid or out of money, we auto-block the action
        print(f"⚠️ [ENGINE FAILURE] {str(e)}")
        return {
            "risk_score": 99,
            "risk_level": "CRITICAL",
            "reason": f"API Key Validation Failed: {str(e)}"
        }