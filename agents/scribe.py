import subprocess
from outputs/formatters.md_formatter import apply_template
def ollama_generate(prompt, model="mistral:7b"):
    out = subprocess.run(["ollama","run",model], input=prompt.encode(), capture_output=True)
    return out.stdout.decode()
def draft(template_path, ctx, model="mistral:7b"):
    return ollama_generate(apply_template(template_path, ctx), model)
