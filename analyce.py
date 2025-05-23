#!/usr/bin/env python3
import os
import anthropic

# 1) Carga la clave desde la variable de entorno
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise EnvironmentError("Define la variable ANTHROPIC_API_KEY en los Secrets del repo")

# Inicializa el cliente de Anthropic
client = anthropic.Anthropic(api_key=api_key)

# 2) Lee los prompts
with open("prompts.txt", encoding="utf-8") as f:
    prompts = [l.strip() for l in f if l.strip()]

# 3) Recoge contenido de los ficheros que quieras analizar
files = {}
for root, _, filenames in os.walk("."):
    for fn in filenames:
        if fn.endswith((".py", ".js", ".ts")):  # ajusta extensiones
            path = os.path.join(root, fn)
            with open(path, encoding="utf-8") as cf:
                files[path] = cf.read()

# 4) Para cada prompt, consulta a Claude y muestra el resultado
for prompt in prompts:
    message = prompt + "\n\nArchivos:\n" + "\n\n".join(f"--- {p}\n{c}" for p, c in files.items())
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            temperature=0,
            system="Eres un asistente experto en revisión de código.",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        
        print(f"\n\n=== Análisis ("{prompt}") ===\n")
        print(response.content[0].text)
        
    except Exception as e:
        print(f"\n\nError al procesar el prompt '{prompt}': {e}")
        continue