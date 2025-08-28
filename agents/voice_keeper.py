import subprocess

STYLE = """Rewrite the text in my voice:
- Short, cutting lines
- Clear, calm, slightly provocative
- Avoid corporate jargon
Output only the rewritten text.
Text:
"""

def rewrite_in_voice(text: str, model="mistral:7b") -> str:
    out = subprocess.run(
        ["ollama", "run", model],
        input=(STYLE + text).encode(),
        capture_output=True
    )
    return out.stdout.decode().strip()
