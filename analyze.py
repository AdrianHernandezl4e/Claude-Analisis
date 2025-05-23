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
try:
    with open("prompts.txt", encoding="utf-8") as f:
        prompts = [l.strip() for l in f if l.strip()]
    if not prompts:
        print("Error: El archivo prompts.txt está vacío o no contiene prompts válidos")
        exit(1)
except FileNotFoundError:
    print("Error: No se encontró el archivo prompts.txt")
    exit(1)
print(f"Se encontraron {len(prompts)} prompts para procesar")

# 3) Recoge contenido de los ficheros que quieras analizar
files = {}
for root, _, filenames in os.walk("."):
    for fn in filenames:
        if fn.endswith((".py", ".js", ".ts")):  # ajusta extensiones
            path = os.path.join(root, fn)
            # Excluir el propio script de análisis
            if fn == "analyze.py":
                continue
            try:
                with open(path, encoding="utf-8") as cf:
                    files[path] = cf.read()
            except Exception as e:
                print(f"Error leyendo archivo {path}: {e}")
                continue

print(f"Se encontraron {len(files)} archivos para analizar")

# 4) Para cada prompt, consulta a Claude y muestra el resultado
for i, prompt in enumerate(prompts, 1):
    print(f"\n\n=== Procesando prompt {i}/{len(prompts)}: '{prompt[:50]}...' ===")
    
    if not files:
        print("No hay archivos para analizar")
        continue
        
    message = prompt + "\n\nArchivos:\n" + "\n\n".join(f"--- {p}\n{c}" for p, c in files.items())
    
    # Verificar que el mensaje no sea demasiado largo
    if len(message) > 100000:  # Límite aproximado
        print(f"Advertencia: El mensaje es muy largo ({len(message)} caracteres), podría truncarse")
    
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
        
        print(f"\n=== Análisis ('{prompt}') ===\n")
        print(response.content[0].text)
        
    except Exception as e:
        print(f"\nError al procesar el prompt '{prompt}': {e}")
        print(f"Tipo de error: {type(e).__name__}")
        continue