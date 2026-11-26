#!/usr/bin/env python3
"""Génère terminal.svg : fenêtre de terminal animée (frappe au clavier), 100% décorative."""
from xml.sax.saxutils import escape

W, H = 1000, 310
FS, CW = 15, 9                      # taille police / largeur d'un caractère (monospace)
X0, Y0, DY = 34, 92, 26
BG, BAR, BLUE = "#0d1730", "#162447", "#3b6fe0"
GREEN, WHITE, SOFT, YEL = "#39d353", "#e6edf3", "#8aa4e8", "#ffd400"

# (type, texte)  cmd = commande tapée lentement ; out = résultat affiché vite
LINES = [
    ("cmd", "whoami"),
    ("out", "Mayssa Abdouli — étudiante ingénieure en informatique"),
    ("cmd", "cat focus.txt"),
    ("out", "IA Générative  ·  Systèmes Multi-Agents "),
    ("cmd", "./status --pfe"),
    ("out", "● disponible  →  PFE février 2027"),
    ("cmd", ""),
]

# --- Calcul de la chronologie ---
t = 0.6
plan = []                            # (index, début, secondes/caractère, nb caractères)
for i, (kind, txt) in enumerate(LINES):
    n = len(txt) + (2 if kind == "cmd" else 0)         # "$ " pour les commandes
    cps = 0.07 if kind == "cmd" else 0.012
    plan.append((i, t, cps, n))
    t += n * cps + (0.45 if kind == "cmd" else 0.7)
HOLD = 5.0
D = t + HOLD
cursor_start = plan[-1][1]

o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  "font-family=\"'Fira Code', 'DejaVu Sans Mono', 'Courier New', monospace\">")

# clipPaths animés (effet machine à écrire, par paliers)
a('<defs>')
for i, start, cps, n in plan:
    ev = [(0.0, 0)]
    for j in range(1, n + 1):
        ev.append((start + j * cps, j * CW))
    ev.append((D - 0.2, 0))
    kt = ";".join(f"{min(e[0] / D, 1):.5f}" for e in ev)
    vals = ";".join(str(e[1]) for e in ev)
    y = Y0 + i * DY - FS
    a(f'<clipPath id="c{i}"><rect x="{X0}" y="{y}" height="{DY}" width="0">'
      f'<animate attributeName="width" calcMode="discrete" keyTimes="{kt}" values="{vals}" '
      f'dur="{D:.2f}s" repeatCount="indefinite"/></rect></clipPath>')
a('<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
  f'<stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="#0a1126"/></linearGradient>')
a('</defs>')

# fenêtre
a(f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)" stroke="{BLUE}" stroke-width="1.5"/>')
a(f'<path d="M0,12 Q0,0 12,0 H{W - 12} Q{W},0 {W},12 V40 H0 Z" fill="{BAR}"/>')
for k, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
    a(f'<circle cx="{26 + k * 22}" cy="20" r="6" fill="{c}"/>')
a(f'<text x="{W / 2}" y="25" text-anchor="middle" fill="{SOFT}" font-size="13">mayssa@abdouli: ~/profile</text>')

# lignes de texte
for i, (kind, txt) in enumerate(LINES):
    y = Y0 + i * DY
    if kind == "cmd":
        n = len(txt) + 2
        a(f'<g clip-path="url(#c{i})"><text x="{X0}" y="{y}" font-size="{FS}" '
          f'textLength="{n * CW}" lengthAdjust="spacing" xml:space="preserve">'
          f'<tspan fill="{GREEN}">$ </tspan><tspan fill="{WHITE}">{escape(txt)}</tspan></text></g>')
    else:
        col = YEL if txt.startswith("●") else SOFT
        a(f'<g clip-path="url(#c{i})"><text x="{X0}" y="{y}" font-size="{FS}" fill="{col}" '
          f'textLength="{len(txt) * CW}" lengthAdjust="spacing" xml:space="preserve">{escape(txt)}</text></g>')

# curseur clignotant sur la dernière ligne
cy = Y0 + (len(LINES) - 1) * DY - FS + 2
a(f'<g opacity="0"><animate attributeName="opacity" calcMode="discrete" '
  f'keyTimes="0;{cursor_start / D:.5f};{(D - 0.2) / D:.5f}" values="0;1;0" dur="{D:.2f}s" repeatCount="indefinite"/>'
  f'<rect x="{X0 + 2 * CW + 2}" y="{cy}" width="9" height="18" fill="{WHITE}">'
  '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/>'
  '</rect></g>')

a('</svg>')
open("terminal.svg", "w", encoding="utf-8").write("\n".join(o))
print(f"terminal.svg généré (boucle de {D:.0f}s)")
