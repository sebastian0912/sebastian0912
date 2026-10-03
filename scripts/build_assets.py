"""Genera los SVG estáticos del perfil en assets/.

Uso:  python scripts/build_assets.py

El contenido (estilos, radar, nube) vive en las listas de abajo: para agregar
un estilo o mover una tecnología de anillo se edita aquí y se vuelve a correr.
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


# ------------------------------------------------------ estilos de arquitectura
STYLES = [  # (nombre, cuándo, dónde lo he aplicado)
    ("Monolito", "Un despliegue y un equipo: velocidad máxima mientras se descubre el dominio.",
     "Plataforma empresarial de RR. HH. y nómina."),
    ("Monolito modular", "Módulos con fronteras claras (hexagonal) dentro de un solo artefacto fácil de operar.",
     "Productos SaaS, gestión documental y verificación."),
    ("Híbrido", "Núcleo modular y procesos aparte solo donde la carga o el aislamiento lo exigen.",
     "Analítica de video con IA y motores de automatización."),
    ("Microservicios", "Despliegues y datos independientes por dominio, comunicados por API y eventos.",
     "Plataforma ganadera y modernización empresarial."),
]


def styles():
    W, H = 1000, 466
    b = [frame(W, H),
         header(28, 44, "ARCHITECTURE STYLES", "Elijo el estilo según el problema, no según la moda", W, "monolito → microservicios")]
    b.append(f'<defs><linearGradient id="spec" gradientUnits="userSpaceOnUse" x1="40" y1="0" x2="{W-44}" y2="0"><stop stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
             f'<marker id="tip" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{VIOLET}"/></marker></defs>'
             f'<line x1="40" y1="98" x2="{W-44}" y2="98" stroke="url(#spec)" stroke-width="2" marker-end="url(#tip)"/>'
             f'<text x="40" y="118" class="m" fill="{FAINT}" font-size="10" letter-spacing="1">MENOS PIEZAS · OPERACIÓN SIMPLE</text>'
             f'<text x="{W-40}" y="118" text-anchor="end" class="m" fill="{FAINT}" font-size="10" letter-spacing="1">AUTONOMÍA · ESCALA INDEPENDIENTE</text>')
    cw, gap, x0, y0 = 226, 14, 27, 134

    def cyl(x, y, w=26, color=MUTED):
        return (f'<path d="M{x-w/2},{y} v12 a{w/2},4 0 0,0 {w},0 v-12" fill="{PANEL}" stroke="{color}"/>'
                f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="4" fill="{PANEL}" stroke="{color}"/>')

    def hexa(x, y, r, color):
        pts = " ".join(f"{x + r*math.cos(math.radians(60*i+30)):.1f},{y + r*math.sin(math.radians(60*i+30)):.1f}" for i in range(6))
        return f'<polygon points="{pts}" fill="{PANEL}" stroke="{color}"/>'

    def block(cx, top, w, c):
        return f'<rect x="{cx-w/2}" y="{top}" width="{w}" height="62" rx="8" fill="{c}" fill-opacity=".10" stroke="{c}"/>'

    def db_under(x, top):
        return f'<line x1="{x}" y1="{top+62}" x2="{x}" y2="{top+74}" stroke="{LINE}"/>' + cyl(x, top + 78)

    def diagram(i, cx, top):
        c = CAT[i]
        if i == 0:  # un bloque en capas
            return (block(cx, top, 120, c)
                    + "".join(f'<line x1="{cx-48}" y1="{top+18+k*14}" x2="{cx+48}" y2="{top+18+k*14}" stroke="{c}" stroke-opacity=".6"/>' for k in range(3))
                    + db_under(cx, top))
        if i == 1:  # bloque con módulos
            mods = "".join(f'<rect x="{cx-50 + (k%2)*52}" y="{top+8 + (k//2)*25}" width="48" height="21" rx="4" fill="{PANEL}" stroke="{c}" stroke-dasharray="3 3"/>' for k in range(4))
            return block(cx, top, 120, c) + mods + db_under(cx, top)
        if i == 2:  # núcleo modular + workers aparte
            mods = "".join(f'<rect x="{cx-76 + (k%2)*40}" y="{top+8 + (k//2)*25}" width="36" height="21" rx="4" fill="{PANEL}" stroke="{c}" stroke-dasharray="3 3"/>' for k in range(4))
            return (block(cx - 38, top, 92, c) + mods
                    + f'<path d="M{cx+8},{top+31} H{cx+38}" stroke="{c}" stroke-opacity=".7" class="flow" fill="none"/>'
                    + f'<path d="M{cx+38},{top+16} V{top+50}" stroke="{c}" stroke-opacity=".7" fill="none"/>'
                    + hexa(cx + 54, top + 16, 15, c) + hexa(cx + 54, top + 50, 15, c)
                    + db_under(cx - 38, top))
        # microservicios: cada servicio con su base, unidos por un bus de eventos
        out = f'<line x1="{cx-84}" y1="{top+44}" x2="{cx+84}" y2="{top+44}" stroke="{VIOLET}" stroke-width="2" class="flow"/>'
        for k in range(4):
            hx = cx - 63 + k * 42
            out += (f'<line x1="{hx}" y1="{top+18}" x2="{hx}" y2="{top+44}" stroke="{c}" stroke-opacity=".6"/>' + hexa(hx, top + 14, 15, c)
                    + f'<line x1="{hx}" y1="{top+44}" x2="{hx}" y2="{top+68}" stroke="{LINE}"/>' + cyl(hx, top + 72, 18))
        return out

    for i, (name, when, where) in enumerate(STYLES):
        x = x0 + i * (cw + gap)
        cx = x + cw / 2
        b.append(f'<rect x="{x}" y="{y0}" width="{cw}" height="304" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
                 f'<text x="{x+18}" y="{y0+26}" class="m" fill="{FAINT}" font-size="10" letter-spacing="1.5">{i+1:02d}</text>'
                 f'<circle cx="{x+cw-22}" cy="{y0+22}" r="4" fill="{CAT[i]}"/>')
        b.append(diagram(i, cx, y0 + 40))
        b.append(f'<text x="{x+18}" y="{y0+164}" class="s" fill="{INK}" font-size="18" font-weight="650">{e(name)}</text>')
        for j, line in enumerate(textwrap.wrap(when, 30)):
            b.append(f'<text x="{x+18}" y="{y0+188 + j*18}" class="s" fill="{MUTED}" font-size="13">{e(line)}</text>')
        b.append(f'<line x1="{x+18}" y1="{y0+240}" x2="{x+cw-18}" y2="{y0+240}" stroke="{LINE}"/>'
                 f'<text x="{x+18}" y="{y0+257}" class="m" fill="{CYAN}" font-size="9.5" letter-spacing="1">LO HE APLICADO EN</text>')
        for j, line in enumerate(textwrap.wrap(where, 32)[:2]):
            b.append(f'<text x="{x+18}" y="{y0+274 + j*15}" class="s" fill="{INK2}" font-size="12">{e(line)}</text>')
    css = ".flow{stroke-dasharray:3 6;animation:dash 1.2s linear infinite}@keyframes dash{to{stroke-dashoffset:-18}}"
    return svg(W, H, "Estilos de arquitectura",
               "Monolito, monolito modular, híbrido y microservicios: cuándo conviene cada uno y dónde los ha aplicado. " +
               " ".join(f"{n}: {w} Aplicado en: {d}" for n, w, d in STYLES), "".join(b), css)


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
    for name, fn in [("hero", hero), ("styles", styles),
                     ("multicloud", multicloud), ("radar", radar)]:
        path = os.path.join(OUT, f"{name}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(fn())
        print(f"assets/{name}.svg")


if __name__ == "__main__":
    main()
