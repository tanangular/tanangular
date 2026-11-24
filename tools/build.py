"""Generates the animated SVGs for the tanangular profile README.
All text is converted to outlines so it renders the same everywhere (GitHub serves SVG as <img>, no web fonts)."""
import math, os
import textpath as T

THEMES = {
 "light": dict(bg="#f4f2e8", bg2="#ece7d8", ink="#0755b5", muted="#326daa", soft="#0755b5",
               pink="#a92a5c", green="#157a50", purple="#5b3db5", orange="#b8461a", teal="#0b6975",
               blob1="#0755b5", blob2="#a92a5c", blob3="#5b3db5", blobop=0.16, line=0.22),
 "dark":  dict(bg="#071431", bg2="#0b1d45", ink="#f4f2e8", muted="#9fb7e6", soft="#6f9bff",
               pink="#ff6fa3", green="#4fd39a", purple="#a08cff", orange="#ff8a4c", teal="#45c4d3",
               blob1="#1f5fff", blob2="#ff4f93", blob3="#7b5cff", blobop=0.30, line=0.28),
}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets"); os.makedirs(OUT, exist_ok=True)
EASE = "cubic-bezier(.2,.7,.2,1)"

BASE_CSS = f"""
.up{{animation:up .7s {EASE} both}}
.fade{{animation:fade 1s ease both}}
.draw{{stroke-dasharray:1;animation:draw 2.2s {EASE} both}}
.fillin{{animation:fillin 1s ease both}}
.pop{{transform-box:fill-box;transform-origin:center;animation:pop .6s {EASE} both}}
.blink{{animation:blink 1.05s steps(1) infinite}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-in-out infinite}}
.float{{animation:float 7s ease-in-out infinite alternate}}
@keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
@keyframes fillin{{from{{fill-opacity:0}}to{{fill-opacity:1}}}}
@keyframes pop{{0%{{opacity:0;transform:scale(.6)}}100%{{opacity:1;transform:none}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes pulse{{0%,100%{{transform:scale(1);opacity:1}}50%{{transform:scale(1.7);opacity:.35}}}}
@keyframes float{{from{{transform:translateY(-6px)}}to{{transform:translateY(6px)}}}}
@keyframes drift1{{from{{transform:translate(0,0)}}to{{transform:translate(260px,60px)}}}}
@keyframes drift2{{from{{transform:translate(0,0)}}to{{transform:translate(-220px,-50px)}}}}
@keyframes drift3{{from{{transform:translate(0,0)}}to{{transform:translate(120px,-80px)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""

def svg(w, h, body, css="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{title}"><title>{title}</title><style>{BASE_CSS}{css}</style>{body}</svg>\n')

def text_stagger(text, font, size, x, y, fill, start, step=0.03, wght=None, ls=0, anchor="start", cls="up"):
    """each glyph cluster gets its own delayed reveal"""
    gl, w = T.glyphs(text, font, size, x, y, wght=wght, ls=ls, anchor=anchor)
    parts = []
    for i, (d, c) in enumerate(gl):
        parts.append(f'<path class="{cls}" style="animation-delay:{start + c*step:.2f}s" d="{d}"/>')
    return f'<g fill="{fill}">{"".join(parts)}</g>', w

def text_plain(text, font, size, x, y, fill, wght=None, ls=0, anchor="start", extra=""):
    d, w = T.path(text, font, size, x, y, wght=wght, ls=ls, anchor=anchor)
    return f'<path fill="{fill}" {extra} d="{d}"/>', w

def blobs(t, w, h, p=""):
    return f"""<defs>
<radialGradient id="{p}b1"><stop offset="0" stop-color="{t['blob1']}" stop-opacity="{t['blobop']}"/><stop offset="1" stop-color="{t['blob1']}" stop-opacity="0"/></radialGradient>
<radialGradient id="{p}b2"><stop offset="0" stop-color="{t['blob2']}" stop-opacity="{t['blobop']*0.85}"/><stop offset="1" stop-color="{t['blob2']}" stop-opacity="0"/></radialGradient>
<radialGradient id="{p}b3"><stop offset="0" stop-color="{t['blob3']}" stop-opacity="{t['blobop']*0.8}"/><stop offset="1" stop-color="{t['blob3']}" stop-opacity="0"/></radialGradient>
<pattern id="{p}dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t['ink']}" fill-opacity=".13"/></pattern>
<clipPath id="{p}clip"><rect width="{w}" height="{h}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#{p}clip)">
<rect width="{w}" height="{h}" fill="{t['bg']}"/>
<ellipse cx="{w*0.15:.0f}" cy="{h*0.2:.0f}" rx="{w*0.35:.0f}" ry="{h*0.75:.0f}" fill="url(#{p}b1)" style="animation:drift1 19s ease-in-out infinite alternate"/>
<ellipse cx="{w*0.85:.0f}" cy="{h*0.85:.0f}" rx="{w*0.32:.0f}" ry="{h*0.7:.0f}" fill="url(#{p}b2)" style="animation:drift2 23s ease-in-out infinite alternate"/>
<ellipse cx="{w*0.55:.0f}" cy="{h*0.1:.0f}" rx="{w*0.25:.0f}" ry="{h*0.55:.0f}" fill="url(#{p}b3)" style="animation:drift3 29s ease-in-out infinite alternate"/>
<rect width="{w}" height="{h}" fill="url(#{p}dots)"/>
"""

def crop_marks(t, w, h, m=28, L=18, delay=0.0):
    s = []
    for (x, y, dx, dy) in [(m, m, -1, -1), (w-m, m, 1, -1), (m, h-m, -1, 1), (w-m, h-m, 1, 1)]:
        s.append(f'M{x+dx*6} {y}h{dx*L}M{x} {y+dy*6}v{dy*L}')
    return (f'<path class="fade" style="animation-delay:{delay}s" fill="none" stroke="{t["ink"]}" '
            f'stroke-opacity=".55" stroke-width="1" d="{"".join(s)}"/>')

def label(t, text, x, y, delay, anchor="start", color=None, size=12.5):
    g, _ = text_stagger(text, "mono", size, x, y, color or t["muted"], delay, step=0.015, wght=500, ls=1.6, anchor=anchor, cls="fade")
    return g

# ---------------- icosahedron (SMIL path morph, renders static frame 0 elsewhere) -------------
PHI = (1 + 5 ** 0.5) / 2
V = []
for a in (-1, 1):
    for b in (-PHI, PHI):
        V += [(0, a, b), (a, b, 0), (b, 0, a)]
E = [(i, j) for i in range(12) for j in range(i+1, 12)
     if abs(sum((V[i][k]-V[j][k])**2 for k in range(3)) - 4) < 1e-6]
assert len(E) == 30

def project(theta, cx, cy, r, tilt=0.42):
    pts = []
    for (x, y, z) in V:
        x1 = x*math.cos(theta) + z*math.sin(theta); z1 = -x*math.sin(theta) + z*math.cos(theta)
        y2 = y*math.cos(tilt) - z1*math.sin(tilt); z2 = y*math.sin(tilt) + z1*math.cos(tilt)
        s = r/1.902 * (1 + z2*0.07)
        pts.append((cx + x1*s, cy + y2*s, z2))
    return pts

def ico(t, cx, cy, r, frames=48, dur=36, delay=0.2):
    ths = [2*math.pi*i/frames for i in range(frames+1)]
    P = [project(th, cx, cy, r) for th in ths]
    def d(p): return "".join(f"M{p[i][0]:.1f} {p[i][1]:.1f}L{p[j][0]:.1f} {p[j][1]:.1f}" for i, j in E)
    vals = ";".join(d(p) for p in P)
    out = [f'<g class="float"><path class="draw" pathLength="1" style="animation-delay:{delay}s;animation-duration:3s" fill="none" stroke="{t["ink"]}" stroke-width="1.3" stroke-linecap="round" stroke-opacity=".9" d="{d(P[0])}">'
           f'<animate attributeName="d" dur="{dur}s" repeatCount="indefinite" values="{vals}"/></path>']
    # vertices: blender-ish select dots, one "active" in orange
    for k in range(12):
        xs = ";".join(f"{p[k][0]:.1f}" for p in P); ys = ";".join(f"{p[k][1]:.1f}" for p in P)
        col = t["orange"] if k == 4 else t["ink"]; rr = 5 if k == 4 else 2.6
        out.append(f'<circle class="pop" style="animation-delay:{delay+2.2+k*0.05:.2f}s" cx="{P[0][k][0]:.1f}" cy="{P[0][k][1]:.1f}" r="{rr}" fill="{col}">'
                   f'<animate attributeName="cx" dur="{dur}s" repeatCount="indefinite" values="{xs}"/>'
                   f'<animate attributeName="cy" dur="{dur}s" repeatCount="indefinite" values="{ys}"/></circle>')
    out.append('</g>')
    return "".join(out)

# ---------------- header ----------------
def header(theme):
    t = THEMES[theme]; W, H = 1200, 460
    b = [blobs(t, W, H), crop_marks(t, W, H)]
    # ruler ticks top
    ticks = "".join(f"M{x} 0v{10 if x % 100 == 0 else 5}" for x in range(40, W-30, 20))
    b.append(f'<path class="fade" fill="none" stroke="{t["ink"]}" stroke-opacity=".35" d="{ticks}"/>')
    b.append(label(t, "TANANGULAR  /  @COOLDEZIGN", 72, 86, 0.2))
    b.append(label(t, "ARTBOARD 01  ·  TH  ·  UTC+7", W-72, 86, 0.4, anchor="end"))
    # big name: outline draws, then fills
    d, wname = T.path("Tan", "serif_i", 236, 64, 300)
    b.append(f'<path class="draw" pathLength="1" style="animation-delay:.5s;animation-duration:2.4s" fill="none" stroke="{t["ink"]}" stroke-width="1.4" d="{d}"/>')
    b.append(f'<path class="fillin" style="animation-delay:2.1s" fill="{t["ink"]}" d="{d}"/>')
    dd, _ = T.path(".", "serif_i", 236, 64+wname-6, 300)
    b.append(f'<path class="pop" style="animation-delay:2.6s" fill="{t["pink"]}" d="{dd}"/>')
    # annotation next to the name (designer redline)
    ax = 64 + wname + 70
    b.append(f'<path class="draw" pathLength="1" style="animation-delay:2.8s;animation-duration:1s" fill="none" stroke="{t["pink"]}" stroke-width="1.2" d="M{ax} 214 h44 M{ax} 206 v16 M{ax+44} 206 v16"/>')
    g, _ = text_stagger("fig. 01, the human", "serif_i", 24, ax+58, 222, t["pink"], 3.0, step=0.025)
    b.append(g)
    g, _ = text_stagger("a dev with a design obsession.", "grotesk", 34, 70, 358, t["ink"], 2.9, step=0.022, wght=500, ls=-0.4)
    b.append(g)
    _, wtag = T.glyphs("a dev with a design obsession.", "grotesk", 34, 70, 358, wght=500, ls=-0.4)
    b.append(f'<rect style="animation:fade .2s 3.7s both,blink 1.05s 3.9s steps(1) infinite" x="{70+wtag+8:.0f}" y="330" width="3" height="34" fill="{t["orange"]}"/>')
    g, _ = text_stagger("สายโค้ดที่บ้าดีไซน์ เห็นของสวยของเท่แล้วอดไม่ได้", "thai_l", 21, 71, 398, t["muted"], 3.7, step=0.012)
    b.append(g)
    # right: wireframe + construction circle
    cx, cy, r = 930, 248, 134
    b.append(f'<circle class="draw" pathLength="1" style="animation-delay:.1s;animation-duration:2.6s" cx="{cx}" cy="{cy}" r="{r+22}" fill="none" stroke="{t["ink"]}" stroke-opacity=".25" stroke-dasharray="1" />')
    b.append(f'<path class="fade" style="animation-delay:1s" fill="none" stroke="{t["ink"]}" stroke-opacity=".22" stroke-dasharray="3 5" d="M{cx-r-60} {cy}H{cx+r+60}M{cx} {cy-r-34}V{cy+r+24}"/>')
    b.append(ico(t, cx, cy, r))
    b.append(label(t, "ICOSPHERE · SUBDIV 0", cx, cy+r+40, 2.4, anchor="middle", size=11))
    b.append("</g>")
    return svg(W, H, "".join(b), title="Tan, a dev with a design obsession")

# ---------------- divider ----------------
def divider(theme):
    t = THEMES[theme]; W, H = 1200, 56; mid = H/2
    def wave(ph, amp):
        pts = []
        for i in range(0, 161, 4):
            x = 520 + i; env = math.sin(math.pi*i/160)
            y = mid + amp*env*math.sin(i/9 + ph)
            pts.append(f"{x:.1f} {y:.1f}")
        return "M" + "L".join(pts)
    vals = ";".join(wave(2*math.pi*k/12, 14) for k in range(13))
    body = (f'<path fill="none" stroke="{t["ink"]}" stroke-opacity="{t["line"]}" d="M40 {mid}H510M690 {mid}H1160"/>'
            f'<path fill="none" stroke="{t["pink"]}" stroke-width="1.6" stroke-linecap="round" d="{wave(0,14)}"><animate attributeName="d" dur="1.6s" repeatCount="indefinite" values="{vals}"/></path>'
            f'<circle r="3.2" cy="{mid}" cx="40" fill="{t["orange"]}"><animate attributeName="cx" values="40;510" dur="5s" repeatCount="indefinite"/></circle>'
            f'<circle r="3.2" cy="{mid}" cx="1160" fill="{t["orange"]}"><animate attributeName="cx" values="1160;690" dur="5s" repeatCount="indefinite"/></circle>'
            f'<path fill="none" stroke="{t["ink"]}" stroke-opacity=".5" d="M40 {mid-6}v12M1160 {mid-6}v12"/>')
    return svg(W, H, body, title="divider")

def card_frame(t, W, H, num, name, p=""):
    return (blobs(t, W, H, p) +
            f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{t["ink"]}" stroke-opacity="{t["line"]}"/>'
            + label(t, f"{num}  /  {name}", 36, 46, 0.1))

# ---------------- toolbox ----------------
def toolbox(theme):
    t = THEMES[theme]; W, H = 1200, 320
    b = [card_frame(t, W, H, "02", "TOOLBOX")]
    g, _ = text_stagger("What I build with", "serif_i", 52, 36, 112, t["ink"], 0.3, step=0.025)
    b.append(g)
    chips = [("SolidJS", "blue"), ("Vue", "green"), ("Astro", "orange"), ("MedusaJS", "purple"),
             ("three.js", "ink"), ("Blender", "orange"), ("3D", "pink")]
    x, y = 36, 150; delay = 0.8
    for name, c in chips:
        col = t["ink"] if c in ("blue", "ink") else t[c]
        tg, tw = T.path(name, "grotesk", 24, 0, 0, wght=500)
        cw = tw + 66
        if x + cw > W - 36: x = 36; y += 70
        tg, _ = T.path(name, "grotesk", 24, x+44, y+35, wght=500)
        b.append(f'<g class="pop" style="animation-delay:{delay:.2f}s">'
                 f'<rect x="{x}" y="{y}" width="{cw:.0f}" height="52" rx="26" fill="{t["bg"]}" fill-opacity=".55" stroke="{t["ink"]}" stroke-opacity=".55"/>'
                 f'<circle cx="{x+25}" cy="{y+26}" r="6" fill="{col}"/>'
                 f'<path fill="{t["ink"]}" d="{tg}"/></g>')
        x += cw + 14; delay += 0.12
    # the react chip, crossed out, on its own row with a redline note
    name = "React"
    tg, tw = T.path(name, "grotesk", 24, 0, 0, wght=500); cw = tw + 44
    x = 36; y += 78
    tg, _ = T.path(name, "grotesk", 24, x+22, y+35, wght=500)
    b.append(f'<g class="pop" style="animation-delay:{delay+0.3:.2f}s">'
             f'<rect x="{x}" y="{y}" width="{cw:.0f}" height="52" rx="26" fill="none" stroke="{t["muted"]}" stroke-opacity=".7" stroke-dasharray="4 5"/>'
             f'<path fill="{t["muted"]}" fill-opacity=".75" d="{tg}"/></g>')
    b.append(f'<path class="draw" pathLength="1" style="animation-delay:{delay+0.9:.2f}s;animation-duration:.5s" fill="none" stroke="{t["pink"]}" stroke-width="3" stroke-linecap="round" d="M{x+12} {y+30} L{x+cw-12} {y+22}"/>')
    ax = x + cw + 14; ay = y + 26
    b.append(f'<path class="draw" pathLength="1" style="animation-delay:{delay+1.3:.2f}s;animation-duration:.8s" fill="none" stroke="{t["pink"]}" stroke-width="1.5" stroke-linecap="round" d="M{ax+86} {ay+4} C{ax+60} {ay+18} {ax+30} {ay+16} {ax+4} {ay+2} M{ax+14} {ay-6} L{ax+3} {ay+2} L{ax+15} {ay+9}"/>')
    g, _ = text_stagger("respectfully, no. the architecture and I disagree.", "serif_i", 27, ax+100, ay+10, t["pink"], delay+1.8, step=0.018)
    b.append(g)
    b.append("</g>")
    return svg(W, H, "".join(b), title="Toolbox: SolidJS, Vue, Astro, MedusaJS, three.js, Blender, 3D. React crossed out.")

# ---------------- currently into ----------------
def into(theme, body_only=False):
    t = THEMES[theme]; W, H = 590, 380
    b = [card_frame(t, W, H, "03", "CURRENTLY INTO", "i")]
    g, _ = text_stagger("On my mind lately", "serif_i", 44, 36, 104, t["ink"], 0.3, step=0.025)
    b.append(g)
    items = [("AI", t["ink"]), ("agent programming", t["green"]), ("fine-tuning models", t["purple"]), ("A2UI", t["orange"])]
    y = 154
    for i, (s, col) in enumerate(items):
        dl = 0.9 + i*0.25
        b.append(label(t, f"0{i+1}", 36, y+7, dl, size=12))
        b.append(f'<circle class="pop" style="animation-delay:{dl:.2f}s" cx="86" cy="{y}" r="5" fill="{col}"/>')
        b.append(f'<circle class="pulse" style="animation-delay:{i*0.6:.1f}s" cx="86" cy="{y}" r="5" fill="none" stroke="{col}" stroke-width="1.4"/>')
        g, w = text_stagger(s, "grotesk", 28, 106, y+10, t["ink"], dl+0.1, step=0.02, wght=500, ls=-0.3)
        b.append(g)
        b.append(f'<path class="draw" pathLength="1" style="animation-delay:{dl+0.2:.2f}s;animation-duration:1.2s" fill="none" stroke="{t["ink"]}" stroke-opacity="{t["line"]}" d="M36 {y+28}H{W-36}"/>')
        y += 48
    g, _ = text_stagger("ตอนนี้อินเรื่อง agent สุด ๆ", "thai_l", 18, 36, H-32, t["muted"], 2.2, step=0.015)
    b.append(g)
    b.append(f'<rect class="blink" x="{W-52}" y="{H-48}" width="12" height="3" fill="{t["orange"]}"/>')
    b.append("</g>")
    if body_only: return "".join(b)
    return svg(W, H, "".join(b), title="Currently into: AI, agent programming, fine-tuning models, A2UI")

# ---------------- fuel ----------------
def fuel(theme, body_only=False):
    t = THEMES[theme]; W, H = 590, 380
    b = [card_frame(t, W, H, "04", "FUEL", "f")]
    # two cups: coffee (left) + cocoa mug (right), line art, steam loops
    def cup(x, y, col, delay, mug=False):
        body = (f"M{x} {y} h70 v{46 if mug else 38} q0 22 -22 22 h-26 q-22 0 -22 -22 z" )
        handle = f"M{x+70} {y+10} q22 0 22 18 q0 18 -22 18"
        s = [f'<path class="draw" pathLength="1" style="animation-delay:{delay}s;animation-duration:1.6s" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" d="{body}{handle}"/>']
        if not mug:
            s.append(f'<path class="draw" pathLength="1" style="animation-delay:{delay+0.4}s;animation-duration:1.2s" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" d="M{x-14} {y+66} h98"/>')
        for k, dx in enumerate((18, 35, 52)):
            vals = []
            for ph in range(9):
                p = 2*math.pi*ph/8 + k
                vals.append(f"M{x+dx} {y-8} c{6*math.sin(p):.1f} -8 {-6*math.sin(p):.1f} -14 0 -22 c{6*math.sin(p+1):.1f} -8 {-6*math.sin(p+1):.1f} -14 0 -20")
            s.append(f'<path class="fade" style="animation-delay:{delay+1.2+k*0.2:.1f}s" fill="none" stroke="{col}" stroke-opacity=".6" stroke-width="1.5" stroke-linecap="round" d="{vals[0]}"><animate attributeName="d" dur="{2.2+k*0.4:.1f}s" repeatCount="indefinite" values="{";".join(vals)}"/></path>')
        return "".join(s)
    b.append(cup(W-250, 112, t["orange"], 0.4))
    b.append(cup(W-130, 104, t["pink"], 0.7, mug=True))
    b.append(label(t, "COFFEE", W-232, 214, 1.6, size=10.5))
    b.append(label(t, "COCOA", W-112, 214, 1.8, size=10.5))
    g, _ = text_stagger("Coffee boots me up.", "serif_i", 38, 36, 112, t["ink"], 0.4, step=0.022)
    b.append(g)
    g, _ = text_stagger("Cocoa keeps", "serif_i", 38, 36, 156, t["ink"], 0.9, step=0.022)
    b.append(g)
    g, _ = text_stagger("me running.", "serif_i", 38, 36, 200, t["ink"], 1.2, step=0.022)
    b.append(g)
    g, _ = text_stagger("กาแฟสตาร์ท โกโก้ลากยาว", "thai_l", 18, 36, 238, t["muted"], 1.8, step=0.015)
    b.append(g)
    # equalizer: trance on loop
    base = H - 40
    bars = []
    for i in range(22):
        x = 36 + i*9
        hs = [6 + abs(math.sin(i*0.7 + k*1.3))*30*(0.5+0.5*math.sin(i/3.5+k)) for k in range(6)]
        hv = ";".join(f"{h:.1f}" for h in hs + hs[:1]); yv = ";".join(f"{base-h:.1f}" for h in hs + hs[:1])
        col = t["pink"] if i % 5 == 0 else t["ink"]
        bars.append(f'<rect x="{x}" y="{base-hs[0]:.1f}" width="5" height="{hs[0]:.1f}" rx="1.5" fill="{col}" fill-opacity=".85">'
                    f'<animate attributeName="height" dur="{1.3+i%4*0.17:.2f}s" repeatCount="indefinite" values="{hv}"/>'
                    f'<animate attributeName="y" dur="{1.3+i%4*0.17:.2f}s" repeatCount="indefinite" values="{yv}"/></rect>')
    b.append(f'<g class="fade" style="animation-delay:2s">{"".join(bars)}</g>')
    b.append(label(t, "NOW PLAYING  ·  TRANCE, ON LOOP", 250, base-2, 2.2, size=11))
    b.append("</g>")
    if body_only: return "".join(b)
    return svg(W, H, "".join(b), title="Fuel: coffee boots me up, cocoa keeps me running. Trance on loop.")

def duo(theme):
    body = (f'<svg x="0" y="0" width="590" height="380" overflow="hidden">{into(theme, True)}</svg>'
            f'<svg x="610" y="0" width="590" height="380" overflow="hidden">{fuel(theme, True)}</svg>')
    return svg(1200, 380, body, title="Currently into: AI, agent programming, fine-tuning models, A2UI. Fuel: coffee boots me up, cocoa keeps me running. Trance on loop.")

if __name__ == "__main__":
    for th in THEMES:
        for name, fn in [("header", header), ("divider", divider), ("toolbox", toolbox), ("duo", duo)]:
            with open(f"{OUT}/{name}-{th}.svg", "w") as f:
                f.write(fn(th))
    print("ok")
