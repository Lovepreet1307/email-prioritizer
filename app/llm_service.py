import subprocess
import json

# Ollama model to use
MODEL_NAME = "llama2"  # Change to your installed model

CLASSIFY_PROMPT = """
You are an assistant that classifies emails into one of three categories: Urgent, Important, FYI.
Rules:
- If the email asks for immediate action or mentions deadlines within 48 hours -> Urgent.
- If it's work-related or needs attention but not immediate -> Important.
- If it's a newsletter, notification or just FYI -> FYI.
Return JSON with keys: priority, reason (one sentence).
Email:
\"\"\"\n{email}\n\"\"\"
"""

SUMMARIZE_PROMPT = """
Summarize the following email in 1-2 sentences:
\"\"\"\n{email}\n\"\"\"
"""

REPLY_PROMPT = """
Write a short, polite reply (2-4 sentences) appropriate for the following email. If no reply is required, output an empty string.
Email:
\"\"\"\n{email}\n\"\"\"
"""

# Timeout in seconds for each Ollama call
OLLAMA_TIMEOUT = 15

def run_ollama(prompt: str) -> str:
    """Call Ollama CLI with timeout and return generated text."""
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME, "--text", prompt],
            capture_output=True,
            text=True,
            timeout=OLLAMA_TIMEOUT
        )
        # Ollama output may be JSON or plain text
        try:
            output = json.loads(result.stdout)
            return output.get("content", "").strip()
        except json.JSONDecodeError:
            return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"Ollama call timed out after {OLLAMA_TIMEOUT} seconds")
        return ""
    except subprocess.CalledProcessError as e:
        print("Ollama CLI error:", e.stderr)
        return ""

def classify_email(email_text: str) -> dict:
    prompt = CLASSIFY_PROMPT.format(email=email_text)
    out = run_ollama(prompt)
    priority = None
    reason = ""

    for line in out.splitlines():
        if 'Urgent' in line:
            priority = 'Urgent'
            reason = line
            break
        if 'Important' in line:
            priority = 'Important'
            reason = line
            break
        if 'FYI' in line:
            priority = 'FYI'
            reason = line
            break

    if not priority:
        if 'deadline' in email_text.lower() or 'asap' in email_text.lower():
            priority = 'Urgent'
        else:
            priority = 'Important'

    return {"priority": priority, "reason": reason or out}

def summarize_email(email_text: str) -> str:
    prompt = SUMMARIZE_PROMPT.format(email=email_text)
    return run_ollama(prompt)

def suggest_reply(email_text: str) -> str:
    prompt = REPLY_PROMPT.format(email=email_text)
    return run_ollama(prompt)
