"""Genera los SVG estáticos del perfil en assets/.

Uso:  python scripts/build_assets.py

El contenido (sistemas, radar, nube) vive en las listas de abajo: para agregar
un proyecto o mover una tecnología de anillo se edita aquí y se vuelve a correr.
La telemetría en vivo la genera scripts/telemetry.py desde Actions.
"""

import math
import os
import textwrap
from html import escape

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")

# Tokens de diseño (superficie oscura propia: se ve igual en tema claro y oscuro)
BG, PANEL, LINE = "#0B1020", "#0F172A", "#1E293B"
INK, INK2, MUTED, FAINT = "#F1F5F9", "#CBD5E1", "#94A3B8", "#64748B"
CYAN, VIOLET, GREEN = "#22D3EE", "#A78BFA", "#34D399"
AWS, AZURE = "#FF9900", "#3B9CFF"
# Paleta categórica validada para superficie oscura (orden fijo)
CAT = ["#3987e5", "#d95926", "#199e70", "#c98500"]

SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,Inter,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono',Consolas,'Liberation Mono',monospace"

BASE_CSS = f"""
.s{{font-family:{SANS}}} .m{{font-family:{MONO}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""


def e(t):
    return escape(t, quote=True)


def svg(w, h, title, desc, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d"><title id="t">{e(title)}</title><desc id="d">{e(desc)}</desc>'
            f'<style>{BASE_CSS}{css}</style>{body}</svg>')


def frame(w, h, grid=True):
    out = [f'<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse">'
           f'<path d="M24 0H0V24" fill="none" stroke="{LINE}" stroke-width=".6" opacity=".55"/></pattern>'
           f'<radialGradient id="glowA" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" '
           f'gradientTransform="translate(120 40) scale(520 360)"><stop stop-color="{CYAN}" stop-opacity=".16"/>'
           f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>'
           f'<radialGradient id="glowB" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" '
           f'gradientTransform="translate({w-140} {h-60}) scale(520 380)"><stop stop-color="{VIOLET}" stop-opacity=".16"/>'
           f'<stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>'
           f'<clipPath id="clip"><rect width="{w}" height="{h}" rx="16"/></clipPath></defs>'
           f'<g clip-path="url(#clip)"><rect width="{w}" height="{h}" fill="{BG}"/>']
    if grid:
        out.append(f'<rect width="{w}" height="{h}" fill="url(#g)"/>')
    out.append(f'<rect width="{w}" height="{h}" fill="url(#glowA)"/><rect width="{w}" height="{h}" fill="url(#glowB)"/></g>'
               f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="15.5" fill="none" stroke="{LINE}"/>')
    return "".join(out)


def header(x, y, kicker, title, w=None, right=None):
    out = (f'<text x="{x}" y="{y}" class="m" fill="{CYAN}" font-size="11" letter-spacing="2">{e(kicker)}</text>'
           f'<text x="{x}" y="{y+30}" class="s" fill="{INK}" font-size="24" font-weight="650">{e(title)}</text>')
    if right and w:
        out += f'<text x="{w-x}" y="{y}" text-anchor="end" class="m" fill="{FAINT}" font-size="11">{e(right)}</text>'
    return out


def chip(x, y, label, color=MUTED, fill="none", size=11, pad=9, h=22):
    w = len(label) * size * 0.62 + pad * 2
    return (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{color}" '
            f'stroke-opacity=".55"/><text x="{x + w/2:.1f}" y="{y + h/2 + size*0.36:.1f}" text-anchor="middle" '
            f'class="m" fill="{color}" font-size="{size}">{e(label)}</text>'), w


# --------------------------------------------------------------------- hero
def hero():
    W, H = 1000, 440
    b = [frame(W, H)]
    # barra de ventana
    b.append(f'<g>{"".join(f'<circle cx="{24 + i*18}" cy="24" r="5" fill="{c}"/>' for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]))}'
             f'<text x="86" y="28" class="m" fill="{FAINT}" font-size="12">~/sebastian0912 › architecture.yaml</text>'
             f'<rect x="{W-214}" y="12" width="190" height="24" rx="12" fill="{GREEN}" fill-opacity=".08" stroke="{GREEN}" stroke-opacity=".4"/>'
             f'<circle class="pulse" cx="{W-198}" cy="24" r="4" fill="{GREEN}"/>'
             f'<text x="{W-186}" y="28" class="m" fill="{GREEN}" font-size="11">disponible para retos</text>'
             f'<line x1="0" y1="48" x2="{W}" y2="48" stroke="{LINE}"/></g>')
    # columna izquierda
    b.append(f'<defs><linearGradient id="nameG" x1="0" x2="1"><stop stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient></defs>')
    b.append(f'<text x="48" y="98" class="m" fill="{CYAN}" font-size="12" letter-spacing="2.5">SOFTWARE ARCHITECT · CLOUD ARCHITECT</text>'
             f'<text x="46" y="160" class="s" fill="{INK}" font-size="56" font-weight="700" letter-spacing="-1.5">Sebastian</text>'
             f'<text x="46" y="220" class="s" fill="url(#nameG)" font-size="56" font-weight="700" letter-spacing="-1.5">Guarnizo Campos</text>'
             f'<text x="48" y="262" class="s" fill="{INK2}" font-size="18">Senior Software Engineer que diseña plataformas</text>'
             f'<text x="48" y="288" class="s" fill="{INK2}" font-size="18">que escalan, se auditan y se sostienen años.</text>'
             f'<rect class="caret" x="404" y="273" width="9" height="19" fill="{CYAN}"/>')
    x = 48
    for label, color in [("AWS", AWS), ("Azure", AZURE), ("Kubernetes", CYAN), ("Spring Cloud", GREEN), ("Kafka · NATS", VIOLET)]:
        c, w = chip(x, 318, label, color, fill=color + "14", size=12, h=26)
        b.append(c)
        x += w + 10
    b.append(f'<text x="48" y="384" class="m" fill="{FAINT}" font-size="12">◉ Bogotá, Colombia · UTC−5   ·   microservicios · event-driven · multi-tenant · GPU</text>')

    # topología multinube animada (columna derecha)
    cx = 790

    def node(x, y, w, h, label, color=INK2, stroke=LINE, sub=None):
        t = (f'<rect x="{x - w/2}" y="{y - h/2}" width="{w}" height="{h}" rx="8" fill="{PANEL}" stroke="{stroke}"/>'
             f'<text x="{x}" y="{y + (4 if not sub else -1)}" text-anchor="middle" class="m" fill="{color}" font-size="11">{e(label)}</text>')
        if sub:
            t += f'<text x="{x}" y="{y + 12}" text-anchor="middle" class="m" fill="{FAINT}" font-size="9">{e(sub)}</text>'
        return t

    def hexa(x, y, r, label, color):
        pts = " ".join(f"{x + r*math.cos(math.radians(60*i)):.1f},{y + r*math.sin(math.radians(60*i)):.1f}" for i in range(6))
        return (f'<polygon points="{pts}" fill="{PANEL}" stroke="{color}" stroke-opacity=".8"/>'
                f'<text x="{x}" y="{y+3.5}" text-anchor="middle" class="m" fill="{INK2}" font-size="9.5">{e(label)}</text>')

    paths = {
        "p1": f"M{cx},92 V176",
        "p2": f"M{cx},198 C{cx},222 696,214 696,250",
        "p3": f"M{cx},198 C{cx},222 884,214 884,250",
        "p4": f"M696,330 C696,350 {cx},340 {cx},358",
        "p5": f"M884,330 C884,350 {cx},340 {cx},358",
        "p6": f"M{cx},380 V402",
    }
    b.append(f'<g fill="none" stroke="{LINE}" stroke-width="1.5">' +
             "".join(f'<path id="{k}" d="{d}"/>' for k, d in paths.items()) + '</g>')
    b.append(f'<g fill="none" stroke="{CYAN}" stroke-width="1.5" stroke-opacity=".5" class="flow">' +
             "".join(f'<path d="{d}"/>' for d in paths.values()) + '</g>')
    # regiones
    b.append(f'<rect x="606" y="242" width="180" height="96" rx="12" fill="{AWS}" fill-opacity=".05" stroke="{AWS}" stroke-opacity=".55" stroke-dasharray="4 4"/>'
             f'<text x="618" y="260" class="m" fill="{AWS}" font-size="10" letter-spacing="1">AWS · EKS</text>'
             f'<rect x="794" y="242" width="180" height="96" rx="12" fill="{AZURE}" fill-opacity=".05" stroke="{AZURE}" stroke-opacity=".55" stroke-dasharray="4 4"/>'
             f'<text x="806" y="260" class="m" fill="{AZURE}" font-size="10" letter-spacing="1">AZURE · AKS</text>')
    b.append(hexa(660, 298, 24, "auth", AWS) + hexa(730, 298, 24, "core", AWS) +
             hexa(848, 298, 24, "docs", AZURE) + hexa(918, 298, 24, "ai", AZURE))
    b.append(node(cx, 78, 170, 28, "clients · web · desktop") +
             node(cx, 136, 170, 28, "edge · CDN · WAF") +
             node(cx, 188, 170, 28, "API gateway · OIDC", INK, CYAN) +
             node(cx, 370, 250, 26, "event bus · Kafka / NATS", INK, VIOLET) +
             node(cx, 414, 250, 22, "PostgreSQL · pgvector · object storage", MUTED))
    b.append(f'<text x="{cx}" y="161" text-anchor="middle" class="m" fill="{FAINT}" font-size="9">TLS · rate limit</text>')
    # paquetes viajando por la topología
    packets = [("p1", 0, CYAN), ("p1", 1.2, CYAN), ("p2", .6, AWS), ("p3", 1.5, AZURE), ("p2", 2.4, AWS),
               ("p3", 3.0, AZURE), ("p4", 1.1, VIOLET), ("p5", 2.0, VIOLET), ("p6", 1.6, GREEN), ("p6", 3.1, GREEN)]
    for pid, begin, color in packets:
        b.append(f'<circle r="3.2" fill="{color}" filter="url(#glow)"><animateMotion dur="2.4s" begin="{begin}s" '
                 f'repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="linear"><mpath href="#{pid}"/></animateMotion></circle>')
    b.insert(1, '<defs><filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.2" result="b"/>'
                '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
    # línea de escaneo
    b.append(f'<rect class="scan" x="596" y="56" width="392" height="2" fill="{CYAN}" opacity=".0"/>')
    css = """
.pulse{animation:pulse 2s ease-in-out infinite}
.caret{animation:blink 1.05s steps(1) infinite}
.flow path{stroke-dasharray:4 10;animation:dash 1.6s linear infinite}
.scan{animation:scan 6s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
@keyframes dash{to{stroke-dashoffset:-28}}
@keyframes scan{0%{transform:translateY(0);opacity:0}10%{opacity:.35}90%{opacity:.35}100%{transform:translateY(370px);opacity:0}}
"""
    return svg(W, H, "Sebastian Guarnizo Campos — Software & Cloud Architect",
               "Arquitecto de software y nube (AWS y Azure), Senior Software Engineer en Bogotá. "
               "Diagrama animado de una topología multinube: clientes, edge, API gateway, servicios en EKS y AKS, bus de eventos y datos.",
               "".join(b), css)


# ------------------------------------------------------------------ catálogo
PROJECTS = [  # (título, contexto, patrón, descripción, etiquetas)
    ("Plataforma de gestión ganadera", "PROYECTO DE GRADO", "microservicios",
     "Diseñé una plataforma para administrar fincas —salud animal, producción, ventas y "
     "finanzas— con servicios independientes que se comunican por eventos.",
     ["Microservicios", "Eventos", "Java"]),
    ("Modernización empresarial", "RR. HH. Y NÓMINA", "strangler fig",
     "Migración gradual de un monolito a servicios por dominio (nómina, contratación, "
     "documentos, automatización) sin detener la operación diaria de la empresa.",
     ["Java", "Python", "Eventos"]),
    ("Analítica de video con IA", "VIDEOVIGILANCIA", "tiempo real",
     "Participé en una plataforma que analiza cámaras de seguridad en tiempo real para "
     "detectar eventos y generar alertas, desplegada sobre infraestructura con GPU.",
     ["Visión por computador", "Python", "Kubernetes"]),
    ("Gestión ágil para equipos", "PRODUCTO SAAS", "multi-tenant",
     "Herramienta Scrum y Kanban multiempresa para compañías, universidades y equipos "
     "pequeños; funciona en la nube o instalada en el equipo.",
     ["Spring Boot", "Angular", "Electron"]),
    ("Gestión documental", "PRODUCTO", "hexagonal",
     "Organiza, indexa y encuentra documentos con OCR desde web, escritorio y móvil, "
     "compartiendo un mismo núcleo de negocio.",
     ["Java", "Angular", "OCR"]),
    ("Verificación de antecedentes", "CUMPLIMIENTO", "privacy by design",
     "Automatiza consultas a fuentes oficiales y entrega reportes con evidencias. Diseñado "
     "desde la privacidad: no conserva datos más allá de lo necesario.",
     ["Java", "Angular", "Automatización"]),
    ("Hábitos y finanzas personales", "APP PERSONAL", "local-first",
     "Cruza hábitos y gastos personales. Los datos viven en el dispositivo y la app "
     "funciona completa sin conexión, en escritorio y Android.",
     ["Angular", "Electron", "Android"]),
    ("Agentes de IA para desarrollo", "IA EN EL SDLC", "plataforma interna",
     "Orquesta agentes de IA que trabajan sobre copias aisladas del código, con cola de "
     "tareas y permisos controlados desde la plataforma.",
     ["Node.js", "IA", "Linux"]),
]


def catalog():
    W = 1000
    cw, chh, gap, top = 466, 186, 20, 96
    rows = math.ceil(len(PROJECTS) / 2)
    H = top + rows * chh + (rows - 1) * 16 + 28
    b = [frame(W, H, grid=False),
         header(28, 44, "SERVICE CATALOG", "Sistemas que he diseñado o en los que he participado", W, f"{len(PROJECTS)} sistemas")]
    for i, (name, kind, pattern, desc, tags) in enumerate(PROJECTS):
        col, row = i % 2, i // 2
        x, y = 28 + col * (cw + gap), top + row * (chh + 16)
        accent = CAT[i % 4]
        b.append(f'<g>'
                 f'<rect x="{x}" y="{y}" width="{cw}" height="{chh}" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
                 f'<rect x="{x}" y="{y+18}" width="3" height="34" rx="1.5" fill="{accent}"/>'
                 f'<text x="{x+22}" y="{y+30}" class="m" fill="{FAINT}" font-size="10" letter-spacing="1.5">{i+1:02d} · {e(kind)}</text>'
                 f'<text x="{x+22}" y="{y+56}" class="s" fill="{INK}" font-size="21" font-weight="650">{e(name)}</text>')
        pc, pw = chip(0, 0, pattern, VIOLET, fill=VIOLET + "14", size=10, pad=8, h=20)
        b.append(f'<g transform="translate({x + cw - 20 - pw:.1f} {y+16})">{pc}</g>')
        for j, line in enumerate(textwrap.wrap(desc, 66)[:3]):
            b.append(f'<text x="{x+22}" y="{y+84 + j*19}" class="s" fill="{MUTED}" font-size="13.5">{e(line)}</text>')
        tx = x + 22
        for t in tags:
            c, w = chip(tx, y + chh - 38, t, INK2, fill="#ffffff08", size=10.5, pad=8, h=22)
            b.append(c)
            tx += w + 8
        b.append('</g>')
    css = ""
    return svg(W, H, "Catálogo de sistemas",
               "Sistemas en los que ha trabajado Sebastian Guarnizo: " + "; ".join(f"{p[0]} ({p[1].lower()})" for p in PROJECTS),
               "".join(b), css)


# ---------------------------------------------------------------- multinube
CLOUD = [
    ("Contenedores", "ECS · EKS · ECR", "Container Apps · AKS · ACR"),
    ("Serverless", "Lambda · Step Functions", "Functions · Durable Functions"),
    ("Edge & APIs", "CloudFront · API Gateway · WAF", "Front Door · API Management"),
    ("Eventos", "SQS · SNS · EventBridge · MSK", "Service Bus · Event Grid · Event Hubs"),
    ("Datos", "RDS · Aurora PostgreSQL", "Database for PostgreSQL · Azure SQL"),
    ("Objetos", "S3 · S3 Glacier", "Blob Storage · Archive tier"),
    ("Identidad", "IAM · Cognito", "Entra ID · External ID"),
    ("Secretos", "Secrets Manager · KMS", "Key Vault"),
    ("Observabilidad", "CloudWatch · X-Ray", "Monitor · Application Insights"),
    ("IaC & entrega", "CloudFormation · CDK", "Bicep · ARM"),
]


def multicloud():
    W = 1000
    top, rh = 132, 38
    H = top + len(CLOUD) * rh + 74
    b = [frame(W, H),
         header(28, 44, "MULTI-CLOUD", "Un diseño, dos proveedores", W, "Terraform · GitHub Actions · OpenTelemetry")]
    mid = W / 2
    b.append(f'<text x="{mid - 110}" y="{top - 16}" text-anchor="end" class="m" fill="{AWS}" font-size="13" font-weight="700" letter-spacing="2">AWS</text>'
             f'<text x="{mid + 110}" y="{top - 16}" class="m" fill="{AZURE}" font-size="13" font-weight="700" letter-spacing="2">AZURE</text>'
             f'<text x="{mid}" y="{top - 16}" text-anchor="middle" class="m" fill="{FAINT}" font-size="10" letter-spacing="2">CAPACIDAD</text>')
    for i, (cap, aws, az) in enumerate(CLOUD):
        y = top + i * rh
        if i % 2 == 0:
            b.append(f'<rect x="20" y="{y}" width="{W-40}" height="{rh}" rx="8" fill="#ffffff05"/>')
        cy = y + rh / 2
        b.append(f'<g>'
                 f'<text x="{mid - 110}" y="{cy + 5}" text-anchor="end" class="s" fill="{INK2}" font-size="14">{e(aws)}</text>'
                 f'<line x1="{mid - 98}" y1="{cy}" x2="{mid - 78}" y2="{cy}" stroke="{AWS}" stroke-opacity=".6"/>'
                 f'<rect x="{mid - 74}" y="{cy - 12}" width="148" height="24" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
                 f'<text x="{mid}" y="{cy + 4}" text-anchor="middle" class="m" fill="{INK}" font-size="11">{e(cap)}</text>'
                 f'<line x1="{mid + 78}" y1="{cy}" x2="{mid + 98}" y2="{cy}" stroke="{AZURE}" stroke-opacity=".6"/>'
                 f'<text x="{mid + 110}" y="{cy + 5}" class="s" fill="{INK2}" font-size="14">{e(az)}</text></g>')
    fy = top + len(CLOUD) * rh + 36
    b.append(f'<line x1="28" y1="{fy - 18}" x2="{W-28}" y2="{fy - 18}" stroke="{LINE}"/>'
             f'<text x="28" y="{fy + 4}" class="s" fill="{MUTED}" font-size="13.5">'
             f'Decido por requisitos, costo y operación — no por marca. Cada elección queda en un ADR y en código.</text>')
    css = ""
    return svg(W, H, "Mapa multinube AWS y Azure",
               "Equivalencias entre servicios de AWS y Azure por capacidad: " +
               "; ".join(f"{c}: {a} / {z}" for c, a, z in CLOUD), "".join(b), css)


# ---------------------------------------------------------------- tech radar
RADAR = {  # cuadrante -> [(nombre, anillo 0=adopt 1=trial 2=assess)]
    "Lenguajes & frameworks": [("Java 21 · Spring Boot", 0), ("TypeScript · Angular", 0), ("Python · FastAPI", 0),
                               ("Electron · Capacitor", 1), (".NET · gRPC", 1), ("Kotlin", 2)],
    "Plataformas & nube": [("AWS", 0), ("Azure", 0), ("Docker", 0), ("GitHub Actions", 0),
                           ("Kubernetes", 1), ("Serverless", 2)],
    "Datos & mensajería": [("PostgreSQL", 0), ("Apache Kafka", 0), ("MySQL", 0),
                           ("NATS", 1), ("IndexedDB · local-first", 1), ("Bases vectoriales", 2)],
    "Arquitectura & prácticas": [("Hexagonal", 0), ("ADRs", 0), ("Microservicios", 0), ("Event-driven", 0),
                                 ("Agentes IA en el SDLC", 1), ("Multi-tenant", 1), ("Visión por computador", 2), ("Platform engineering", 2)],
}


def radar():
    W, H = 1000, 600
    cx, cy, R = 500, 330, 230
    rings = [(0.5, "ADOPT"), (0.78, "TRIAL"), (1.0, "ASSESS")]
    b = [frame(W, H, grid=False),
         header(28, 44, "TECH RADAR", "Con qué construyo hoy", W, "adopt · trial · assess")]
    for k, (f, _) in enumerate(reversed(rings)):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{R*f}" fill="{["#ffffff04", "#ffffff06", "#ffffff09"][k]}" stroke="{LINE}"/>')
    b.append(f'<line x1="{cx-R}" y1="{cy}" x2="{cx+R}" y2="{cy}" stroke="{LINE}"/><line x1="{cx}" y1="{cy-R}" x2="{cx}" y2="{cy+R}" stroke="{LINE}"/>')
    for f, name in rings:
        b.append(f'<text x="{cx + 6}" y="{cy - R*f + 14}" class="m" fill="{FAINT}" font-size="9" letter-spacing="1.5">{name}</text>')
    b.append(f'<circle class="sweep-dot" cx="{cx}" cy="{cy}" r="3" fill="{CYAN}"/>'
             f'<g class="sweep" style="transform-origin:{cx}px {cy}px"><path d="M{cx},{cy} L{cx},{cy-R} A{R},{R} 0 0,1 {cx + R*math.sin(math.radians(28)):.1f},{cy - R*math.cos(math.radians(28)):.1f} Z" fill="url(#sw)"/></g>'
             f'<defs><linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".18"/></linearGradient></defs>')
    # cuadrantes: 0 arriba-izq, 1 arriba-der, 2 abajo-izq, 3 abajo-der
    angle_ranges = [(180, 270), (270, 360), (90, 180), (0, 90)]  # grados, eje y hacia abajo
    n = 1
    legends = []
    for q, (qname, items) in enumerate(RADAR.items()):
        color = CAT[q]
        a0, a1 = angle_ranges[q]
        for ring in range(3):
            ring_items = [it for it in items if it[1] == ring]
            r_in = 0 if ring == 0 else R * rings[ring - 1][0]
            r_out = R * rings[ring][0]
            for k, (name, _) in enumerate(ring_items):
                t = (k + 1) / (len(ring_items) + 1)
                ang = math.radians(a0 + 10 + t * (a1 - a0 - 20))
                if ring == 0:
                    rr = (48, 90)[k % 2]
                else:
                    rr = r_in + (r_out - r_in) * (0.5 + (0.2 if k % 2 else -0.2))
                bx, by = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
                b.append(f'<g><circle cx="{bx:.1f}" cy="{by:.1f}" r="10" fill="{color}" stroke="{BG}" stroke-width="2"/>'
                         f'<text x="{bx:.1f}" y="{by + 3.5:.1f}" text-anchor="middle" class="m" fill="#fff" font-size="9.5" font-weight="700">{n}</text>'
                         f'<title>{e(name)} · {rings[ring][1].lower()}</title></g>')
                legends.append((q, n, name, ring))
                n += 1
    # leyendas: izquierda (0 arriba, 2 abajo), derecha (1 arriba, 3 abajo)
    pos = {0: (28, 104), 1: (W - 228, 104), 2: (28, 368), 3: (W - 228, 368)}
    for q, qname in enumerate(RADAR):
        x, y = pos[q]
        b.append(f'<rect x="{x}" y="{y - 10}" width="10" height="10" rx="2" fill="{CAT[q]}"/>'
                 f'<text x="{x + 18}" y="{y}" class="s" fill="{INK}" font-size="13.5" font-weight="650">{e(qname)}</text>')
        for k, (_, num, name, ring) in enumerate([l for l in legends if l[0] == q]):
            yy = y + 26 + k * 21
            b.append(f'<text x="{x + 2}" y="{yy}" class="m" fill="{FAINT}" font-size="11">{num:>2}</text>'
                     f'<text x="{x + 26}" y="{yy}" class="s" fill="{INK2 if ring == 0 else MUTED}" font-size="13">{e(name)}</text>')
    css = ".sweep{animation:spin 8s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}"
    desc = "; ".join(f"{q}: " + ", ".join(f"{n} ({rings[r][1].lower()})" for n, r in items) for q, items in RADAR.items())
    return svg(W, H, "Tech radar", desc, "".join(b), css)


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("hero", hero), ("catalog", catalog),
                     ("multicloud", multicloud), ("radar", radar)]:
        path = os.path.join(OUT, f"{name}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(fn())
        print(f"assets/{name}.svg")


if __name__ == "__main__":
    main()
