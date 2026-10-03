"""Genera assets/telemetry.svg con datos reales de GitHub (sin dependencias).

Uso:  GITHUB_TOKEN=... python scripts/telemetry.py [usuario] [salida]

Con el GITHUB_TOKEN de Actions solo ve lo público; con un token personal de
solo lectura (secreto METRICS_TOKEN) suma los lenguajes de los repos privados.
Nunca escribe nombres de repositorios: solo totales.
"""

import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import date, datetime, timezone
from html import escape

USER = sys.argv[1] if len(sys.argv) > 1 else "sebastian0912"
OUT = sys.argv[2] if len(sys.argv) > 2 else "assets/telemetry.svg"

QUERY = """
query($login: String!, $after: String) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100, after: $after) {
      totalCount
      pageInfo { hasNextPage endCursor }
      nodes {
        languages(first: 12, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
  }
}
"""

# Paleta categórica validada (orden fijo, superficie oscura #0F172A).
CATEGORICAL = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300"]
OTHER = "#475569"
# Rampa secuencial de un solo tono (azul) para la intensidad semanal.
SEQ = ["#1e3a5f", "#24518a", "#2d6bb5", "#3987e5", "#6ea8f0", "#a8cbf7"]
# Marcado, estilos y archivos de build: GitHub los cuenta, pero no son lenguajes de programación.
IGNORED = {"HTML", "CSS", "SCSS", "Less", "Jupyter Notebook", "Batchfile", "Procfile", "Makefile", "Dockerfile"}


def gql(token, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "telemetry-svg"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if body.get("errors"):
        raise SystemExit(f"GraphQL: {body['errors']}")
    return body["data"]["user"]


def collect(token):
    langs, after, first = Counter(), None, None
    while True:
        user = gql(token, {"login": USER, "after": after})
        first = first or user
        repos = user["repositories"]
        for repo in repos["nodes"]:
            for edge in repo["languages"]["edges"]:
                if edge["node"]["name"] not in IGNORED:
                    langs[edge["node"]["name"]] += edge["size"]
        if not repos["pageInfo"]["hasNextPage"]:
            break
        after = repos["pageInfo"]["endCursor"]
    cc = first["contributionsCollection"]
    weeks = [sum(d["contributionCount"] for d in w["contributionDays"])
             for w in cc["contributionCalendar"]["weeks"]]
    week_starts = [w["contributionDays"][0]["date"] for w in cc["contributionCalendar"]["weeks"]]
    days = [x for w in cc["contributionCalendar"]["weeks"] for x in w["contributionDays"]]
    by_weekday = Counter()
    for x in days:
        by_weekday[date.fromisoformat(x["date"]).weekday()] += x["contributionCount"]
    return {
        "total": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        "active_days": sum(1 for x in days if x["contributionCount"]),
        "busiest_weekday": by_weekday.most_common(1)[0][0] if by_weekday else 0,
        "repos": first["repositories"]["totalCount"],
        "weeks": weeks,
        "week_starts": week_starts,
        "langs": langs,
    }


def fmt(n):
    return f"{n:,}".replace(",", ".")


WEEKDAYS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def render(d):
    W, H = 1000, 330
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-labelledby="t d"><title id="t">Telemetría de GitHub de {USER}</title>'
           f'<desc id="d">{fmt(d["total"])} contribuciones en los últimos 12 meses, {fmt(d["commits"])} commits, '
           f'{d["active_days"]} días activos, {d["repos"]} repositorios.</desc>']
    out.append("""<style>
.mono{font-family:'JetBrains Mono','SF Mono',Consolas,'Liberation Mono',monospace}
.sans{font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,Inter,Helvetica,Arial,sans-serif}
.k{fill:#64748b;font-size:11px;letter-spacing:1.5px}
.v{fill:#f1f5f9;font-size:30px;font-weight:600}
.lbl{fill:#94a3b8;font-size:12px}
.ax{fill:#64748b;font-size:10px}
.live{animation:pulse 2s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@media (prefers-reduced-motion:reduce){.live{animation:none}}
</style>""")
    out.append(f'<rect width="{W}" height="{H}" rx="16" fill="#0B1020"/>'
               f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="15.5" fill="none" stroke="#1E293B"/>')
    # Cabecera
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out.append(f'<circle class="live" cx="32" cy="32" r="4" fill="#34D399"/>'
               f'<text x="44" y="36" class="mono k" style="fill:#34D399">LIVE</text>'
               f'<text x="88" y="36" class="mono k">TELEMETRY · github.com/{USER}</text>'
               f'<text x="{W-28}" y="36" text-anchor="end" class="mono ax">actualizado {today}</text>'
               f'<line x1="24" y1="52" x2="{W-24}" y2="52" stroke="#1E293B"/>')
    # KPIs
    kpis = [("CONTRIBUCIONES·12M", fmt(d["total"])), ("COMMITS", fmt(d["commits"])),
            ("DÍAS ACTIVOS", fmt(d["active_days"])), ("REPOS", fmt(d["repos"]))]
    for (k, v), x in zip(kpis, (28, 168, 290, 412)):
        out.append(f'<text x="{x}" y="84" class="mono k" style="font-size:9.5px;letter-spacing:1px">{k}</text>'
                   f'<text x="{x}" y="118" class="sans v">{v}</text>')
    # Barras semanales (una serie: sin leyenda, el título la nombra)
    weeks = d["weeks"][-53:]
    starts = d["week_starts"][-53:]
    cx, cy, cw, ch = 28, 162, 470, 124
    peak = max(weeks) or 1
    step = cw / len(weeks)
    bw = max(step - 2, 2)  # 2px de separación entre barras
    out.append(f'<text x="{cx}" y="{cy-6}" class="sans lbl">Contribuciones por semana</text>')
    out.append(f'<line x1="{cx}" y1="{cy+ch}" x2="{cx+cw}" y2="{cy+ch}" stroke="#1E293B"/>')
    for i, n in enumerate(weeks):
        h = max(n / peak * (ch - 12), 2 if n else 0)
        if not h:
            continue
        tone = SEQ[min(int(n / peak * (len(SEQ) - 1) + .5), len(SEQ) - 1)]
        x = cx + i * step
        r = min(2, bw / 2)
        out.append(f'<path fill="{tone}" '
                   f'd="M{x:.1f},{cy+ch} v{-(h-r):.1f} q0,{-r} {r},{-r} h{bw-2*r:.1f} q{r},0 {r},{r} v{h-r:.1f} z">'
                   f'<title>Semana del {starts[i]}: {n}</title></path>')
    # Meses en el eje
    seen = set()
    for i, s in enumerate(starts):
        m = int(s[5:7])
        if m not in seen and int(s[8:10]) <= 7 and i < len(starts) - 2:
            seen.add(m)
            out.append(f'<text x="{cx + i*step:.1f}" y="{cy+ch+16}" class="mono ax">{MONTHS[m-1]}</text>')
    out.append(f'<text x="{cx+cw}" y="{cy-6}" text-anchor="end" class="mono ax">pico {peak}/sem</text>')

    # Lenguajes: barra apilada, 6 tonos en orden fijo + "Otros"
    total = sum(d["langs"].values()) or 1
    top = d["langs"].most_common(6)
    rest = total - sum(s for _, s in top)
    items = [(n, s, CATEGORICAL[i]) for i, (n, s) in enumerate(top)]
    if rest / total >= .005:
        items.append(("Otros", rest, OTHER))
    lx, ly, lw = 540, 84, 432
    out.append(f'<text x="{lx}" y="{ly}" class="mono k" style="font-size:9.5px;letter-spacing:1px">LENGUAJES DE PROGRAMACIÓN · POR VOLUMEN</text>')
    x = lx
    for i, (n, s, c) in enumerate(items):
        w = s / total * lw
        if w < 1:
            continue
        out.append(f'<rect x="{x:.1f}" y="{ly+14}" '
                   f'width="{max(w-2,1):.1f}" height="14" rx="3" fill="{c}"><title>{escape(n)} {s/total:.1%}</title></rect>')
        x += w
    # Leyenda en dos columnas: texto en tinta, el color va en la marca
    for i, (n, s, c) in enumerate(items):
        col, row = i % 2, i // 2
        x0, y0 = lx + col * 222, ly + 58 + row * 26
        out.append(f'<rect x="{x0}" y="{y0-10}" width="10" height="10" rx="2" fill="{c}"/>'
                   f'<text x="{x0+18}" y="{y0}" class="sans" style="fill:#e2e8f0;font-size:14px">{escape(n)}</text>'
                   f'<text x="{x0+200}" y="{y0}" text-anchor="end" class="mono" style="fill:#94a3b8;font-size:13px">{s/total:.1%}</text>')
    # Pie del panel derecho: lectura rápida del ritmo
    avg = d["total"] / max(len(d["weeks"]), 1)
    facts = [("PROMEDIO", f"{avg:.0f}/sem"), ("MEJOR SEMANA", fmt(peak)),
             ("DÍA MÁS ACTIVO", WEEKDAYS[d["busiest_weekday"]])]
    out.append(f'<line x1="{lx}" y1="244" x2="{lx+lw}" y2="244" stroke="#1E293B"/>')
    for i, (k, v) in enumerate(facts):
        x0 = lx + i * 150
        out.append(f'<text x="{x0}" y="266" class="mono k" style="font-size:9.5px;letter-spacing:1px">{k}</text>'
                   f'<text x="{x0}" y="290" class="sans" style="fill:#f1f5f9;font-size:18px;font-weight:600">{v}</text>')
    out.append("</svg>")
    return "".join(out)


def main():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("Falta GITHUB_TOKEN")
    svg = render(collect(token))
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{OUT} escrito ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
