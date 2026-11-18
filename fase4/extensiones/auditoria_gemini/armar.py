"""armar.py EXT p1files p2files encargo -- arma los trozos de auditoria de una extension."""
import sys, os, html
B = os.path.dirname(os.path.abspath(__file__))
ext, carpeta = sys.argv[1], sys.argv[2]
p1 = sys.argv[3].split(","); p2 = sys.argv[4].split(","); enc = sys.argv[5]
E = os.path.join(os.path.dirname(B), carpeta)
D = os.path.join(B, ext); os.makedirs(D + "/trozos", exist_ok=True); os.makedirs(D + "/conversaciones", exist_ok=True); os.makedirs(D + "/respuestas", exist_ok=True)
def bloque(f):
    t = open(os.path.join(E, f)).read()
    return f"## {f}\n\n" + (f"```python\n{t}\n```\n" if f.endswith(".py") else t + "\n")
ctx = ("Proyecto de física teórica (curso universitario de integrales de camino). Potencial de Yukawa V(r) = −e^{−δr}/r "
       "en unidades ħ = m = g = 1, δ = μħ²/(mg); el estado 1s deja de existir en δ_c = 1.1906124210606.")
t1 = f"# Material para auditoría (parte 1 de 3)\n\nResponde solo \"Recibido\" hasta la parte 3, que trae el encargo.\n\n## Contexto\n\n{ctx}\n\n" + "\n".join(bloque(f) for f in p1)
t2 = "# Material para auditoría (parte 2 de 3)\n\nResponde solo \"Recibido\".\n\n" + "\n".join(bloque(f) for f in p2)
t3 = open(enc).read()
for i, t in enumerate((t1, t2, t3), 1):
    open(f"{D}/trozos/{ext}_parte{i}.md", "w").write(t)
    print(i, len(t))
