#!/usr/bin/env python3
"""Ananda Labs site — zero-dep static build. The Creations registry (index.json) is the CMS.
Run: python3 build.py   → writes index.html, projects.html, research.html, doctrine.html next to this file."""
import json, os, html, datetime
ROOT=os.path.dirname(os.path.abspath(__file__))
REG=json.load(open(os.path.expanduser("~/Creations/index.json")))["creations"]
TODAY=datetime.date.today().isoformat()
PUB=[c for c in REG if c.get("visibility")=="public" and c.get("publish")=="published"]
KIND_LABEL={"project":"Project","tool":"Tool","skill":"Skill","doc":"Book","experiment":"Experiment"}
DOCTRINE=[c for c in PUB if c["kind"]=="doc"]
SITES={"humming-bird":"https://hummingbird.akeyo.io/","tesseract-logo":"https://tesseract.akeyo.io/","p2p":"https://p2p.akeyo.io/",
       "agentworkatlas":"https://atlas.akeyo.io","honestporn":"https://iris.akeyo.io","airsec-static-warroom":"https://airsec.akeyo.io/warroom/","xo":"https://akeyo.io/xo/"}

ONE_SENTENCE="A one-person research lab building the harness for minds — agents, control planes, doctrine, and the tools that make a frontier model operate."
def shell(title, body, active="", desc=ONE_SENTENCE, path="index.html"):
    nav="".join(f'<a href="{h}"{" class=on" if k==active else ""}>{t}</a>' for k,h,t in
        [("research","research.html","Research"),("projects","projects.html","Projects"),("doctrine","doctrine.html","Doctrine"),("brand","brand.html","Brand"),("github","https://github.com/fire17","GitHub")])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://ananda.akeyo.io/{path if path!="index.html" else ""}"><meta name="theme-color" content="#0b0b0d"><link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="Ananda Labs"><meta property="og:url" content="https://ananda.akeyo.io/{path if path!="index.html" else ""}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="https://ananda.akeyo.io/assets/og.png"><meta property="og:image:width" content="1280"><meta property="og:image:height" content="640"><meta property="og:image:alt" content="The Ananda Labs tesseract mark"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}"><meta name="twitter:description" content="{html.escape(desc)}"><meta name="twitter:image" content="https://ananda.akeyo.io/assets/og.png">
<link rel="icon" href="assets/favicon.svg"><link rel="alternate" type="application/rss+xml" title="Ananda Labs" href="https://ananda.akeyo.io/feed.xml"><link rel="stylesheet" href="style.css"></head>
<body><header class="top"><a class="brand" href="index.html"><img src="assets/tesseract-solid-inverted.svg" alt="" width="28" height="28"><span class="wm">ANANDA<small>LABS</small></span></a><nav>{nav}</nav></header>
<main>{body}</main>
<footer><div><img src="assets/tesseract-outlined-inverted.svg" alt="" width="40" height="40"></div><div>Ananda Labs · fire17 · <a href="https://github.com/fire17">github.com/fire17</a> · <a href="https://tesseract.akeyo.io/">the mark</a><br><span class="faint">Built {TODAY} from the living registry · {len(PUB)} public creations</span></div></footer>
</body></html>"""

def card(c):
    repo=c.get("repo") or ""
    live=SITES.get(c["slug"])
    links=[]
    if live: links.append(f'<a href="{live}">live ↗</a>')
    if repo.startswith("http"): links.append(f'<a href="{repo}">code ↗</a>')
    tags="".join(f"<i>{html.escape(t)}</i>" for t in (c.get("tags") or [])[:4])
    return f"""<article class="card"><div class="k">{KIND_LABEL.get(c["kind"],c["kind"])}</div><h3>{html.escape(c["name"])}</h3><p>{html.escape(c.get("summary") or "")}</p><div class="tags">{tags}</div><div class="links">{" ".join(links)}</div></article>"""

# ---------- index
featured=[s for s in ["tesseract-logo","fable-a-fable","livemind","p2p","humming-bird","pyramid"] if any(c["slug"]==s for c in PUB)]
feat_cards="".join(card(next(c for c in PUB if c["slug"]==s)) for s in featured)
index_body=f"""
<section class="hero">
  <div class="stage">
    <video class="fallback" src="assets/petrie.mp4" muted loop autoplay playsinline poster="assets/tesseract-outlined-inverted.svg"></video>
    <iframe src="https://tesseract.akeyo.io/4d.html?hero=1" title="The tesseract, turning through the fourth dimension" loading="eager" allow="autoplay" onload="setTimeout(()=>this.classList.add('live'),1200)"></iframe>
  </div>
  <div class="copy">
    <h1><span class="wm big">ANANDA<small>LABS</small></span></h1>
    <p class="one">{ONE_SENTENCE.replace("harness","<em>harness</em>",1)}</p>
    <p class="doors"><a class="btn" href="research.html">Research</a><a class="btn ghost" href="projects.html">{len(PUB)} public projects</a><a class="btn ghost" href="doctrine.html">Doctrine</a></p>
  </div>
</section>
<section class="strip"><div><b>{len(PUB)}</b><span>published</span></div><div><b>{len(REG)}</b><span>creations in the registry</span></div><div><b>{len(DOCTRINE)}</b><span>books</span></div><div><b>4D</b><span>the mark is a theorem</span></div></section>
<section><h2>Featured</h2><div class="grid">{feat_cards}</div></section>
<section class="who"><h2>Who</h2><p>One person: <a href="https://github.com/fire17">fire17</a> (Tami Bar), building with frontier models as colleagues. The lab began as a <a href="https://github.com/fire17">registry of everything made</a> and became a place to publish it. Every claim on this site links to a thing that exists; where it doesn't yet, the page says so.</p><p class="faint">Public since 2026-09-22 · {len(PUB)} public creations · the registry is the CMS, so these numbers are generated, not typed.</p></section>
<section class="thesis"><h2>The thesis</h2><p>AGI is an <em>operations</em> problem. The ship — raw capability — is nearly solved. The harbor — control planes, introspection, economics, ledgers, arenas, conscience — is what turns a mind into a power. We build harbors.</p><p class="faint">— <a href="doctrine.html">Fable: A Fable</a>, ch. XIV</p></section>
"""
open(os.path.join(ROOT,"index.html"),"w").write(shell("Ananda Labs", index_body, path="index.html"))

# ---------- projects
by_kind={}
for c in sorted(PUB,key=lambda c:c["name"].lower()): by_kind.setdefault(c["kind"],[]).append(c)
sections="".join(f'<h2 id="{k}">{KIND_LABEL.get(k,k)}s <span class="faint">{len(v)}</span></h2><div class="grid">{"".join(card(c) for c in v)}</div>' for k,v in sorted(by_kind.items(),key=lambda kv:-len(kv[1])))
open(os.path.join(ROOT,"projects.html"),"w").write(shell("Projects — Ananda Labs", f'<section><h1>Projects</h1><p class="lede">Everything public, straight from the living registry. Each has code; most have a demo.</p>{sections}</section>', "projects", path="projects.html"))

# ---------- research (honest empty state)
open(os.path.join(ROOT,"research.html"),"w").write(shell("Research — Ananda Labs", """<section><h1>Research</h1><p class="lede">Posts with a claim, a number, a plot, and a reproduction command. Nothing ships without all four.</p>
<div class="empty"><img src="assets/tesseract-outlined-inverted.svg" alt="" width="72" height="72"><p>No posts yet. Three are in preparation:</p><ol><li><b>The logo is a theorem</b> — a Petrie projection of a tesseract, and what its motion lab shows about the fourth dimension.</li><li><b>A frontier model wrote a book about itself</b> — <i>Fable: A Fable</i> and its self-audit.</li><li><b>One engineering post with a number</b> — p2p, humming-bird, or CCVoiceGlobal latency.</li></ol></div></section>""", "research", path="research.html"))

# ---------- doctrine
doc_cards="".join(card(c) for c in DOCTRINE)
open(os.path.join(ROOT,"doctrine.html"),"w").write(shell("Doctrine — Ananda Labs", f"""<section><h1>Doctrine</h1><p class="lede">A lab has a worldview. Ours is written down, by the minds that hold it.</p><div class="grid">{doc_cards}</div>
<h2>Principles we operate by</h2><ul class="creed"><li><b>Ground truth beats memory.</b> Re-derive before acting.</li><li><b>Verification is the work,</b> not the epilogue.</li><li><b>Cheap gates before expensive work.</b></li><li><b>The user's words are sacred data.</b> Verbatim first, derivation second.</li><li><b>Claims fight or they retire.</b> Identical tasks, fresh sessions, measured.</li><li><b>Polish over accretion.</b></li></ul></section>""", "doctrine", path="doctrine.html"))
# ---------- feed.xml (research posts; empty-but-valid until the first post)
POSTS=[]  # [{"title","url","date","summary"}] — filled by the research build when posts exist
items="".join(f"<item><title>{html.escape(p['title'])}</title><link>{p['url']}</link><guid>{p['url']}</guid><pubDate>{p['date']}</pubDate><description>{html.escape(p['summary'])}</description></item>" for p in POSTS)
open(os.path.join(ROOT,"feed.xml"),"w").write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Ananda Labs</title><link>https://ananda.akeyo.io/</link><description>Research posts from Ananda Labs — a claim, a number, a plot, a reproduction command.</description><language>en</language><lastBuildDate>{datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>{items}</channel></rss>')

# ---------- robots / sitemap / 404
open(os.path.join(ROOT,"robots.txt"),"w").write("User-agent: *\nAllow: /\nSitemap: https://ananda.akeyo.io/sitemap.xml\n")
pages=["","projects.html","research.html","doctrine.html","brand.html"]
open(os.path.join(ROOT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>https://ananda.akeyo.io/{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in pages)+"</urlset>")
open(os.path.join(ROOT,"404.html"),"w").write(shell("Not found — Ananda Labs", '<section class="empty" style="margin-top:48px"><img src="/assets/tesseract-outlined-inverted.svg" alt="" width="72" height="72"><h1>Not on this projection</h1><p>That page is not one of our 16 vertices. <a href="/">Back to the front</a>.</p></section>', path="404.html").replace('href="assets/','href="/assets/').replace('src="assets/','src="/assets/').replace('href="style.css"','href="/style.css"'))

# ---------- registry export for brand.html V1 (names only for public entries)
# DISCLOSURE GUARD (oracle INV-3/INV-6): non-public entries export ONLY their four binary axes — no slug, no name, no exact status/visibility/publish vocab.
def _axes(c): return {"x":1 if c["kind"] in("project","tool") else -1,"y":1 if c["status"] in("working","shipped","archived") else -1,"z":-1 if c["visibility"]=="private" else 1,"w":1 if c["publish"]=="published" else -1}
_pub=lambda c: c.get("visibility")=="public" and c.get("publish")=="published"
json.dump([dict(_axes(c),**({"slug":c["slug"],"name":c["name"],"kind":c["kind"]} if _pub(c) else {})) for c in REG],open(os.path.join(ROOT,"assets","registry.json"),"w"))
print("built:", len(PUB), "public →", ROOT)
