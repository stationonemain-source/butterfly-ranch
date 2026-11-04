"""Builds the Butterfly Rescue Ranch concept site from data.json. One page per URL, shared chrome, JSON-LD on every page.
Run from anywhere: python _src/build.py. Output lands next to _src (the git root). Never hand-edit the generated HTML."""
import json, os, html, datetime, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tear_footer import tear_footer
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "_src", "data.json"), encoding="utf-8"))
O = D["org"]; BASE = O["url"]
TODAY = datetime.date.today().isoformat()
# cache-bust token that changes whenever any shipped CSS/JS source changes (a date alone served stale CSS to phones)
import hashlib as _hl, glob as _gl, os as _os
ASSETV = _hl.sha1(b"".join(open(f, "rb").read() for f in sorted(_gl.glob(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "*.css")) + _gl.glob(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "*.js"))))).hexdigest()[:10]
def status_label(h):
    return f'<span class="label">{e(h["status"])}</span>' if h.get("status") else ""

def e(s): return html.escape(str(s), quote=True)

NAV = [("The horses", "horses/"), ("Gallery", "gallery/"), ("Sponsor", "sponsor/"), ("Volunteer", "volunteer/"), ("Program", "program/"), ("About", "about/"), ("Visit", "visit/")]

def org_ld():
    return {"@context": "https://schema.org", "@type": "NGO", "name": O["name"], "alternateName": O["short"], "url": BASE,
            "logo": BASE + "assets/logo.png", "foundingDate": O["founded"], "nonprofitStatus": "Nonprofit501c3",
            "telephone": O["phone_e164"], "slogan": O["tagline"],
            "address": {"@type": "PostalAddress", "streetAddress": O["street"], "addressLocality": O["city"], "addressRegion": O["state"], "postalCode": O["zip"], "addressCountry": "US"},
            "areaServed": "Norman, Oklahoma", "knowsAbout": ["horse rescue", "equine rehabilitation", "riding lessons", "summer horse camps"],
            "potentialAction": {"@type": "DonateAction", "target": BASE + "donate/"}}

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(items)]}

def faq_ld(qa):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}

def faq_html(qa):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{a}</p></details>" for q, a in qa) + "</div>"

def page(path, title, desc, body, ld=(), current=None, depth=None, home=False):
    """path: '' for home, 'donate/' etc. All asset/link URLs are root-relative to the Pages project path."""
    rel = "../" * path.count("/")
    CUR = ' aria-current="page"'
    BODYCLS = ' class="home"' if home else ""
    links = "".join(f'<a href="{rel}{u}"{CUR if current == u else ""}>{n}</a>' for n, u in NAV)
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ((org_ld(),) + tuple(ld)))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex, nofollow">
<meta name="give-api" content="https://give.srv1748596.hstgr.cloud/api/butterfly-ranch">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}assets/hero-poster.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Allura&family=Cinzel:wght@400;600&family=Josefin+Slab:wght@400;600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/site.css?v={ASSETV}">
{lds}
</head>
<body{BODYCLS}>
<a class="skip" href="#main">Skip to content</a>
<header>
  <div class="wrap">
    <a class="logo" href="{rel if rel else './'}" aria-label="{e(O['name'])}, home"><img class="dark-logo" src="{rel}assets/logo.png" alt="{e(O['short'])}" width="900" height="313"><img class="light-logo" src="{rel}assets/logo-white.png" alt="" width="900" height="313" aria-hidden="true"></a>
    <button class="menu" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav id="nav">{links}</nav>
    <a class="btn fill" href="{rel}donate/">Donate</a>
  </div>
</header>
<main id="main">
{body}
</main>
{tear_footer(rel, O, D["credits"])}
<script>
(function(){{
  var b=document.querySelector('.menu'), n=document.getElementById('nav'), h=document.querySelector('header');
  if(document.body.classList.contains('home')){{var film=document.querySelector('.film');var v=film.querySelector('video');if(v){{if(matchMedia('(max-aspect-ratio: 4/5)').matches&&!/hero-m\.mp4/.test(v.currentSrc||'')){{v.src='assets/hero-m.mp4';v.load()}}v.addEventListener('playing',function(){{v.classList.add('on')}});var tryPlay=function(){{var pp=v.play();if(pp&&pp.catch)pp.catch(function(){{}})}};tryPlay();var kick=function(){{if(v.paused)tryPlay();['touchstart','pointerdown','scroll','keydown'].forEach(function(t){{removeEventListener(t,kick,true)}})}};['touchstart','pointerdown','scroll','keydown'].forEach(function(t){{addEventListener(t,kick,{{capture:true,passive:true}})}})}}function sol(){{h.classList.toggle('solid',window.scrollY>film.offsetHeight-h.offsetHeight-8)}}addEventListener('scroll',sol,{{passive:true}});sol()}}
  b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)}});
  document.querySelectorAll('form[data-preview]:not([data-steps])').forEach(function(f){{f.addEventListener('submit',function(ev){{ev.preventDefault();f.querySelector('.sent').classList.add('on')}})}});
  var g=document.getElementById('giver');
  if(g){{
    var other=g.querySelector('input[name=other]'), tiles=g.querySelectorAll('input[name=amt]'), out=g.querySelector('.sent'), btn=g.querySelector('button');
    function amt(){{var t=[].filter.call(tiles,function(x){{return x.checked}})[0];return other.value?Number(other.value):(t?Number(t.value):0)}}
    function freq(){{return g.querySelector('input[name=freq]:checked').value}}
    function label(){{var a=amt();btn.textContent=a?('Give $'+a+(freq()==='monthly'?' a month':' once')):'Choose an amount'}}
    var want=new URLSearchParams(location.search).get('amt');if(want){{var hit=[].filter.call(tiles,function(x){{return x.value===want}})[0];if(hit)hit.checked=true;else other.value=want}}
    g.addEventListener('change',label); other.addEventListener('input',function(){{tiles.forEach(function(x){{x.checked=false}});label()}}); label();
  }}
}})();
</script>
<script src="{rel}assets/forms.js?v=1" defer></script><script src="{rel}assets/give.js?v={ASSETV}" defer></script><script src="{rel}assets/chat.js?v=5" defer></script>
</body>
</html>"""

# A small caps label above a heading is a template slot (slop-war: eyebrows). Keep it only where it states a fact.
EYEBROW_KEEP = {"Helping new riders", "Here for good", "Riding with advanced kids", "7475 By Drive · Norman, Oklahoma", "The January goal"}
EYEBROW_RE = re.compile(r'<span class="label">([^<]*)</span>(?=\s*(?:<div[^>]*>\s*)?<h[1-3]\b)')

def drop_eyebrows(content):
    return EYEBROW_RE.sub(lambda m: m.group(0) if html.unescape(m.group(1)) in EYEBROW_KEEP else "", content)

def write(path, content):
    content = drop_eyebrows(content)
    out = os.path.join(ROOT, path, "index.html") if path else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8", newline="\n").write(content)

def head(label, h2, p=None, more=None):
    return f'<div class="head"><span class="label">{e(label)}</span><div><h2>{h2}</h2>{f"<p>{p}</p>" if p else ""}{f"<p class=more>{more}</p>" if more else ""}</div></div>'

def ph(label, h1, lede, img=None, alt="", crumbs=None, rel="", pos=None):
    c = ""
    if crumbs:
        parts = [f'<a href="{rel}{u}">{e(n)}</a>' if u is not None else e(n) for n, u in crumbs]
        c = '<p class="crumbs">' + " › ".join(parts) + "</p>"
    st = f' style="object-position:{pos}"' if pos else ""
    pic = f'<img src="{rel}assets/photos/{img}.jpg" alt="{e(alt)}" width="1600" height="1200"{st}>' if img else ""
    return f'<div class="ph{"" if img else " plain"}"><div class="wrap"><div>{c}<span class="label">{e(label)}</span><h1>{h1}</h1><p class="lede">{lede}</p></div>{pic}</div></div>'

def band(rel, h="Give once, or a little every month", p="Every gift goes to hay, feed and care, and you'll hear back about the horse it helped."):
    return f'<section class="band"><div class="wrap"><div><span class="label">Help a horse</span><h2>{h}</h2><p>{p}</p></div><div class="acts"><a class="btn fill" href="{rel}donate/">Donate</a><a class="btn line" href="{rel}sponsor/">Sponsor a horse</a><a class="btn line" href="{rel}volunteer/">Volunteer</a></div></div></section>'

def goal(rel):
    lo, hi = O["goal_low"], O["goal_high"]
    mark = round(lo / hi * 100)
    return f'''<section class="goal" id="goal"><div class="wrap">
  {head("The January goal", f"${lo:,} to ${hi:,} for the horses by January", "The first goal the ranch has ever set: enough to stop paying for hay out of pocket this winter. The bar fills itself from every gift.")}
  <div class="goal-grid">
    <div>
      <div class="gbar" role="img" aria-label="$0 raised of a ${hi:,} goal"><i style="width:0%"></i><b style="left:{mark}%"><span>${lo:,}</span></b></div>
      <div class="gnums"><span><strong>$0</strong> raised so far</span><span>Goal <strong>${hi:,}</strong></span></div>
      <p class="note">Giving opens when the ranch's donations go live. Until then the bar stays at zero rather than showing a made-up number.</p>
      <div class="acts"><a class="btn fill" href="{rel}donate/">Give toward the goal</a><a class="btn line" href="{rel}donate/#ways">Give supplies instead</a></div>
    </div>
    <div class="need"><h3>Still needed</h3><ul>
      <li><b>Money</b><span>First and foremost. Hay and feed are $9 a day for every horse.</span></li>
      <li><b>Hay and feed</b><span>Bales and bags, dropped off. Call first.</span></li>
      <li><b>Horse supplies</b><span>Fly spray, wormer, hoof care, halters, lead ropes, brushes.</span></li>
      <li><b>Volunteer time</b><span>Feeding, grooming and barn days. <a href="{rel}volunteer/">Sign up</a></span></li>
    </ul></div>
  </div>
</div></section>'''

def updates(rel, what="the horses"):
    return f'''<section class="updates"><div class="wrap"><div class="upd"><div><span class="label">Updates from the barn</span><h2>Hear how {what} are doing</h2><p>One email a month, with the horse you helped and what it cost. No more than that.</p></div>
<form class="join" data-signup data-how="join" data-how-at="end" novalidate aria-label="Email updates"><div class="join-row"><label class="vh" for="join-email">Email</label><input id="join-email" type="email" name="email" autocomplete="email" inputmode="email" placeholder="you@example.com" required><button class="btn fill" type="submit">Get the updates</button></div><p class="join-fine">One email a month. Unsubscribe in one click.</p><p class="sent" role="status"></p></form></div></div></section>'''

PHONE = f'<a href="tel:{O["phone_e164"]}">{O["phone"]}</a>'
# buy-out up to $2,000 + a year at $9 a day hay and feed, $50 a month supplements, $50 every six weeks farrier
NEXT_HORSE = 6300

# ---------- HOME ----------
def home():
    rel = ""
    herd = "".join(f'<a href="horses/{h["slug"]}/"><img src="assets/photos/horse-{h["slug"]}.jpg" alt="{e(h["alt"])}" width="1200" height="1500" loading="lazy"><h3>{e(h["title"])}</h3><p class="coat">{e(h["coat"])}</p></a>' for h in D["horses"][:8])
    body = f'''
<div class="film">
  <picture class="still"><source media="(max-aspect-ratio: 4/5)" srcset="assets/hero-poster-m.jpg"><img src="assets/hero-poster.jpg" alt="Horses at Butterfly Ranch look straight at the camera over the fence"></picture>
  <video autoplay muted loop playsinline preload="auto" aria-label="The horses of Butterfly Ranch coming to the fence, filmed at the ranch in October 2026; some shots are animated from photos"><source src="assets/hero-m.mp4" type="video/mp4" media="(max-aspect-ratio: 4/5)"><source src="assets/hero.mp4" type="video/mp4"></video>
  <div class="wrap">
    <span class="label">{e(O["street"])} · {e(O["city"])}, Oklahoma</span>
    <h1>Every horse here has a story.</h1>
    <p class="script">Every loving heart deserves to see it.</p>
    <div class="acts"><a class="btn fill cta" href="donate/">Donate</a><a class="btn ghost" href="horses/">Meet the herd</a></div>
  </div>
  <span class="credit">Filmed at the ranch by OU students, October 2026 · some shots animated from their photos</span>
</div>

<section class="state said-home"><div class="wrap"><blockquote class="said"><p>“Once she had a little bit of love and a little bit of time to realize that nobody was going to hurt her anymore, she was able to be put into the riding lessons.”</p><cite>Ranch staff, on <a href="horses/dandelion/">Dandelion</a></cite></blockquote></div></section>

{band(rel)}
{goal(rel)}

<section class="dark">
  <div class="wrap">
    {head("The journey to a second chance", "Every horse deserves a chance to heal")}
    <div class="path">
      <ol class="steps">
        <li><span class="n">01</span><div><h3>A new beginning</h3><p>Every horse arrives with a story. Some have known neglect or abuse; others come from owners who can no longer care for them. Whatever the past, each horse is welcomed with compassion, patience and the promise of a brighter future.</p></div></li>
        <li><span class="n">02</span><div><h3>Healing takes time</h3><p>Recovery is about more than food and medical care. It's rebuilding trust, finding comfort and learning to feel safe again. With proper nutrition, vet care, gentle attention and plenty of patience, each horse heals at its own pace.</p></div></li>
        <li><span class="n">03</span><div><h3>Be part of their story</h3><p>Every small step forward is worth celebrating, and none of it happens alone. We share each horse's journey so supporters can see the difference their kindness makes. Every donation helps write a new chapter.</p></div></li>
        <li><span class="n">04</span><div><h3>A home</h3><p>When a horse is ready, Braxton finds it the right home. Some stay for good, like <a href="horses/rico/" style="color:inherit">Rico</a>.</p></div></li>
      </ol>
      <figure class="ba-rico"><div class="ba2"><div><span class="tag">Arriving</span><img src="assets/photos/rico-before.jpg" alt="Rico when he came back to the ranch: a white horse so thin his ribs and hip bones show, eating from a black tub" width="1600" height="1200" loading="lazy"></div><div><span class="tag">Today</span><img src="assets/photos/rico-now.jpg" alt="Rico today: a white horse at a healthy weight standing by the red pipe gate" width="1600" height="1200" loading="lazy"></div></div>
      <figcaption><b>Rico's journey.</b> These photos show Rico when he arrived at Butterfly Ranch and where he is today: a reminder of what love, patience and proper care can do. Every horse deserves a second chance, and Rico is living proof.</figcaption></figure>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    {head("Meet the herd", "The four horses in the rescue", "Rescued from kill pens and hard homes, brought back to health, and every step shown.", '<a href="horses/">Meet the herd →</a>')}
    <div class="herd" data-how="herd">{herd}</div>
  </div>
</section>
{gallery_strip()}

{updates(rel)}'''
    write("", page("", f"{O['name']} · Horse rescue in Norman, Oklahoma", "Butterfly Rescue Ranch is a 501(c)(3) horse rescue in Norman, Oklahoma. Horses from kill pens, abusive homes and surrenders are rehabilitated in the open: follow every horse, donate, sponsor or volunteer.", body, home=True))

# ---------- HORSES ----------
def horses():
    rel = "../"
    herd = "".join(f'<a href="{h["slug"]}/"><img src="{rel}assets/photos/horse-{h["slug"]}.jpg" alt="{e(h["alt"])}" width="1200" height="1500" loading="lazy"><h3>{e(h["title"])}</h3><p class="coat">{e(h["coat"])}</p></a>' for h in D["horses"])
    body = ph("Meet the herd", "The four horses in the rescue", "Rico, Reba, Dandelion and Daisy are the horses in the rescue program right now. Each has a page that follows it from the day it arrived. The other horses at the ranch are Braxton's own.", crumbs=[("Home", ""), ("The horses", None)], rel=rel)
    body += f'<section><div class="wrap"><div class="herd" data-how="herd">{herd}</div></div></section>{band(rel)}{updates(rel)}'
    ld = [crumbs_ld([("Home", ""), ("The horses", "horses/")]),
          {"@context": "https://schema.org", "@type": "ItemList", "name": "Horses at Butterfly Rescue Ranch", "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "name": h["title"], "url": f"{BASE}horses/{h['slug']}/"} for i, h in enumerate(D["horses"])]}]
    write("horses/", page("horses/", f"The horses · {O['name']}", "Meet the rescue horses at Butterfly Rescue Ranch in Norman, Oklahoma. Each horse has its own page, updated as it recovers.", body, ld, current="horses/"))
    for h in D["horses"]:
        horse(h)

def horse_log(h):
    if h.get("log"):
        return "".join(f'<li><time>{e(w)}</time><div><h3>{e(t_)}</h3><p>{e(p)}</p></div>{f"<span class=cost>{e(c)}</span>" if c else ""}</li>' for w, t_, p, c in h["log"])
    return """<li><time>Day 1</time><div><h3>Arrival</h3><p>Where the horse came from, its weight and condition, and the first vet check. Intake photo here.</p></div><span class="cost">Intake vet · $ —</span></li>
        <li><time>Week 2</time><div><h3>Feet and teeth</h3><p>First farrier visit and dental float. What the farrier found, in plain words.</p></div><span class="cost">Farrier, every 6 weeks · $50</span></li>
        <li><time>Month 2</time><div><h3>Putting weight back on</h3><p>Feed plan, weight change, and the first time the horse comes to the gate on its own.</p></div><span class="cost">Hay, feed and supplements · about $324 a month</span></li>
        <li><time>Month 4</time><div><h3>Back to work</h3><p>Groundwork, then saddle time when the horse is sound. Photos as it fills out.</p></div></li>
        <li><time>Recovered</time><div><h3>Well</h3><p>Sound, at weight, and settled. A thank-you to every donor who helped get it here, and what the whole journey cost.</p></div><span class="cost">Total · $ —</span></li>"""

def horse(h):
    rel = "../../"
    named = bool(h.get("lede"))
    who = h["title"] if named else "this horse"
    she = h.get("pron") == "she"
    his, him, he_is = ("her", "her", "she is") if she else ("his", "him", "he is")
    if named:
        lede = e(h["lede"])
    else:
        lede = f'{e(h["coat"])}. <span class="tbc">Name, age, where it came from and its story are Braxton\'s to add. This page shows the layout every horse will get.</span>'
    card = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in h["card"]) if h.get("card") else '<dt>Came from</dt><dd class="tbc">Kill pen, auction or surrender</dd><dt>Arrived</dt><dd class="tbc">Month, year</dd><dt>Breed, age</dt><dd class="dash">—</dd>'

    others = [x for x in D["horses"] if x["slug"] != h["slug"]][:4]
    more = "".join(f'<a href="../{x["slug"]}/"><img src="{rel}assets/photos/horse-{x["slug"]}.jpg" alt="{e(x["alt"])}" width="1200" height="1500" loading="lazy"><h3>{e(x["title"])}</h3><p class="coat">{e(x["coat"])}</p></a>' for x in others)
    body = f'''
<div class="ph horse"><div class="wrap">
  <div><p class="crumbs"><a href="{rel}">Home</a> › <a href="../">The horses</a> › {e(h["title"])}</p>{status_label(h)}<h1>{e(h["title"])}</h1>
  <p class="lede">{lede}</p>
  <div class="acts" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn fill" href="{rel}sponsor/?horse={h["slug"]}#start">Sponsor {e(who)}</a><a class="btn line" href="{rel}donate/?horse={h["slug"]}">Give toward {his if named else "its"} care</a></div>
  <a class="feed" href="{rel}donate/?horse={h["slug"]}&amp;amt=9"><b>$9</b><span>feeds {e(who)} for a day: hay and feed</span><em>Give $9 →</em></a></div>
  <img src="{rel}assets/photos/horse-{h["slug"]}.jpg" alt="{e(h["alt"])}" width="1200" height="1500" style="aspect-ratio:4/5">
</div></div>

<section class="dark">
  <div class="wrap">
    {f'<blockquote class="said"><p>“{e(h["quote"][0])}”</p><cite>{e(h["quote"][1])}</cite></blockquote>' if h.get("quote") else ""}
    {head("The journal", f"From the day {'she' if she else 'he'} arrived" if named else "From the day it arrived", "Updated as the horse recovers, with what was spent and who helped, so donors can see what their gift did.")}
    <div class="journal" data-how="journal">
      <aside class="card-id" aria-label="Horse details">
        {status_label(h)}
        <div class="name">{e(h["title"])}</div>
        <dl><dt>Coat</dt><dd>{e(h["coat"])}</dd>{card}<dt>Costs a month</dt><dd>About ${O["cost_month"]}</dd><dt>Sponsored by</dt><dd class="tbc">Open</dd></dl>
        <a class="btn fill" href="{rel}sponsor/?horse={h["slug"]}#start">Sponsor {e(who)}</a>
      </aside>
      <ol class="log">
        {horse_log(h)}
      </ol>
    </div>
  </div>
</section>

<section><div class="wrap">{head("Also in the rescue", "The rest of the herd", more=f'<a href="../">All four horses →</a>')}<div class="herd">{more}</div></div></section>
{band(rel, f"Help {who}", f"Sponsor {him if named else 'it'} by the month, or give once toward feed, farrier and vet care. Either way you'll hear how {he_is if named else 'it is'} doing.")}
{updates(rel, "this horse and the others")}'''
    ld = [crumbs_ld([("Home", ""), ("The horses", "horses/"), (h["title"], f"horses/{h['slug']}/")]),
          {"@context": "https://schema.org", "@type": "Animal" if False else "Thing", "name": h["title"], "description": f"A rescue horse at {O['name']}, {O['city']}, Oklahoma. {h['coat']}.", "image": f"{BASE}assets/photos/horse-{h['slug']}.jpg", "url": f"{BASE}horses/{h['slug']}/"}]
    write(f"horses/{h['slug']}/", page(f"horses/{h['slug']}/", f"{h['title']} · The horses · {O['name']}", f"{h['title']} is a rescue horse at Butterfly Rescue Ranch in Norman, Oklahoma. Follow its journal, sponsor it, or give toward its care.", body, ld, current="horses/"))

# ---------- DONATE ----------
def donate():
    rel = "../"
    tiles = "".join(f'<label><input type="radio" name="amt" value="{t["amt"]}"{" checked" if i == 1 else ""}><span class="a">${t["amt"]}</span><span class="f">{e(t["for"])}</span></label>' for i, t in enumerate(D["tiers"]))
    qa = [("Is my gift tax-deductible?", f"{O['name']} is a registered 501(c)(3) nonprofit, so gifts are tax-deductible to the extent the law allows. You'll get a receipt by email for every gift. <span class=\"tbc\">The ranch's EIN will be shown here.</span>"),
          ("Where does the money go?", "Hay and feed ($9 a day for each horse), supplements ($50 a month), the farrier ($50 every six weeks) and the vet when a horse needs one. That comes to about $360 a month for one horse before the vet, and every horse's page shows what was spent on it."),
          ("Can I give monthly?", "Yes. Choose <b>Monthly</b> above. Monthly gifts are what let the ranch plan feed and farrier visits ahead instead of month to month. You can stop at any time from the receipt email."),
          ("Can I give to one particular horse?", f"Yes. <a href=\"{rel}sponsor/\">Sponsor a horse</a> covers one horse's care by the month, and you'll get its updates. A one-time gift here goes wherever the need is that month."),
          ("Can I give supplies instead of money?", "Please do. Feed, hay and horse supplies are used every day, and the list of what's needed most is above. Call ahead before dropping anything off."),
          ("Does my employer match gifts?", "Many do. Ask your HR team for their matching-gift form and send it to the ranch with your receipt; the ranch will complete its part.")]
    body = ph("Donate", "Transparency you can trust, impact you can see", "Be part of every horse's story. Every dollar you give goes to a horse's journey, from rescue to rehabilitation and, in time, a new home. Three steps: pick an amount, choose once or monthly, and pay.", img="donate-sign", alt="A bay horse grazes beside the pink Butterfly Ranch sign on the block wall", crumbs=[("Home", ""), ("Donate", None)], rel=rel)
    body += f'''
<section>
  <div class="wrap">
    <div class="give">
      <form class="giver" id="giver" data-horses='{e(json.dumps({h["slug"]: (h["title"][0].lower() + h["title"][1:]) if h["title"].startswith("The ") else h["title"] for h in D["horses"]}))}' data-how="giver" data-how-at="end" novalidate aria-label="Donation form">
        <div class="seg" role="radiogroup" aria-label="How often"><label><input type="radio" name="freq" value="once" checked><span>One time</span></label><label><input type="radio" name="freq" value="monthly"><span>Monthly</span></label></div>
        <div class="tiles">{tiles}</div>
        <div class="other"><span>Or another amount</span><input type="number" name="other" min="1" inputmode="numeric" placeholder="$" aria-label="Other amount in dollars"></div>
        <p class="for-horse" hidden></p><p class="impact" aria-live="polite"></p>
        <div class="give-progress" data-give-progress hidden><div class="bar"><i></i></div><span></span></div>
        <button class="btn fill" type="submit">Give $50</button>
        <p class="fine">{e(O["name"])} is a 501(c)(3). Gifts are tax-deductible as allowed by law. Pay by card, Apple Pay, Google Pay or bank in a secure form on this page; the money goes straight to the ranch's own Stripe account. For Venmo, see below.</p>
        <p class="sent" role="status"></p>
      </form>
      <div>
        <h2 style="margin-bottom:22px" id="ways">Other ways to give</h2>
        <ul class="ways">
          <li><b>Venmo</b><p><span class="tbc">The ranch's Venmo handle will be here, with a QR code.</span></p></li>
          <li><b>By mail</b><p>Checks to {e(O["name"])}, {e(O["street"])}, {e(O["city"])}, {O["state"]} {O["zip"]}. <span class="tbc">A PO Box is being set up.</span></p></li>
          <li><b>Supplies</b><p>Feed, hay and tack. <a href="#supplies">See what's needed most →</a></p></li>
          <li><b>Employer match</b><p>Many employers double a gift. Ask HR for the form; the ranch will complete its part.</p></li>
          <li><b>Sponsor a horse</b><p>One horse, by the month, with its updates. <a href="{rel}sponsor/">How sponsoring works →</a></p></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="next-horse"><div class="wrap">
  {head("The next horse", f"We are ${NEXT_HORSE:,} away from saving our next horse this year", "That's what it takes to bring one more horse in: up to $2,000 to buy it out of a kill pen, and about $4,300 for its first year of hay, feed, supplements and the farrier. Braxton's goal is four horses a year without paying out of her own pocket.")}
  <div class="gbar" role="img" aria-label="$0 raised of ${NEXT_HORSE:,} for the next horse"><i style="width:0%"></i></div>
  <div class="gnums"><span><strong>$0</strong> toward the next horse</span><span><strong>${NEXT_HORSE:,}</strong> saves one</span></div>
  <p class="note">The bar fills from every gift once the ranch's donations go live. Until then it stays at zero.</p>
</div></section>

<section class="why"><div class="wrap">
  {head("Why your support is critical", "Every dollar goes to the horses")}
  <div class="two"><p class="soft">At Butterfly Ranch, every dollar spent goes directly to changing the lives of the horses in our care. We take in horses from dangerous situations and give them the safe place, the resources and the love they need to thrive.</p>
  <p class="soft">Rescued horses need intensive daily care, from proper nutrition and hay to vet checks and rehabilitation supplies. Your gift makes sure these horses never go without what they need. Become part of their recovery today.</p></div>
</div></section>

<section class="supplies" id="supplies"><div class="wrap">
  <img class="banner" src="{rel}assets/photos/tack-banner.jpg" alt="Saddles, halters and lead ropes in pink, green and purple hanging in the tack room" width="1600" height="640" loading="lazy">
  {head("A gift more than money", "Give supplies the ranch uses every day", f"Have equipment or supplies to give? Physical gifts keep the ranch running. Call first so someone is there: {PHONE}.")}
  <div class="two"><div><h3>Needed most</h3><ul class="needs"><li>Feed</li><li>Hay</li><li>Horse supplies: fly spray, wormer, hoof care, brushes</li><li>Children's saddles</li><li>Saddle pads</li><li>Riding helmets</li></ul><p class="note"><span class="tbc">The order of this list is Braxton's to confirm.</span></p></div>
  <div><h3>Amazon wish list</h3><p class="soft">Order something the horses need and it ships straight to the ranch. <span class="tbc">Braxton is setting the list up; the link goes here.</span></p></div></div>
</div></section>

<section id="costs" class="dark">
  <div class="wrap">
    {head("Where it goes", "What one horse costs us each month", "You deserve to see exactly where your money goes. A gift isn't lost in an anonymous fund: you become part of a horse's journey, with updates from arrival to recovery.")}
    <div class="ledger-grid">
      <div>
        <div class="big"><span class="amt">${O["cost_month"]}</span><span class="per soft">a month in set costs, for one rescue horse at the ranch</span></div>
        <table>
          <caption>One horse · one month</caption>
          <thead><tr><th>Item</th><th class="amt">Cost</th></tr></thead>
          <tbody>
            <tr><td>Hay and feed<small>$9 a day, every day</small></td><td class="amt">$274</td></tr>
            <tr><td>Supplements<small>Every month</small></td><td class="amt">$50</td></tr>
            <tr><td>Farrier<small>$50 every 6 weeks, spread monthly</small></td><td class="amt">$36</td></tr>
            <tr><td>Vet<small>When a horse needs it, on top of the set costs</small></td><td class="amt dash">as needed</td></tr>
          </tbody>
          <tfoot><tr><td>One horse, one month</td><td class="amt">$360</td></tr></tfoot>
        </table>
        <p class="note">Bringing a new horse in costs more: $1,000 to $2,000 to buy it out of a kill pen. Four rescue horses at the ranch now is about $1,440 a month.</p>
      </div>
      <div class="promise" data-how="promise" data-how-at="end">
        <h3>What we promise donors</h3>
        <ul><li><b>A thank-you from us, personally,</b> after every gift.</li><li><b>An update on the horse you helped,</b> with photos, as it recovers.</li><li><b>The numbers, in public.</b> This table is updated as costs change.</li><li><b>Your name stays private</b> unless you tell us you'd like to be thanked by name.</li></ul>
      </div>
    </div>
  </div>
</section>

<section><div class="wrap">{head("Questions", "Giving, answered")}{faq_html(qa)}</div></section>
{updates(rel)}'''
    ld = [crumbs_ld([("Home", ""), ("Donate", "donate/")]), faq_ld([(q, a.replace('<span class="tbc">', '').replace('</span>', '').replace('<b>', '').replace('</b>', '')) for q, a in qa if "<a" not in a])]
    write("donate/", page("donate/", f"Donate · {O['name']}", "Give to the rescue horses at Butterfly Rescue Ranch, Norman, Oklahoma. One-time or monthly, by card, Apple Pay, Google Pay or bank. A 501(c)(3); gifts are tax-deductible.", body, ld, current="donate/"))

# ---------- THANKS (Stripe returns here) ----------
def thanks():
    rel = "../../"
    body = ph("Thank you", "Thank you for the horses", "Your gift goes to hay, feed and care.", crumbs=[("Home", ""), ("Donate", "donate/"), ("Thank you", None)], rel=rel)
    body += f'''<section><div class="wrap"><div id="give-thanks"><p class="gt-msg lede" role="status">Checking your gift…</p>
<p class="gt-ok" hidden>A tax receipt is on its way by email, and Braxton will write to say thank you. If you gave for a horse, you'll hear how it's doing.</p>
<p style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px"><a class="btn fill" href="{rel}horses/">Meet the horses</a><a class="btn line" href="{rel}">Back to the ranch</a></p></div></div></section>'''
    write("donate/thanks/", page("donate/thanks/", f"Thank you · {O['name']}", "Thank you for your gift to Butterfly Rescue Ranch.", body, [], current="donate/"))

# ---------- SPONSOR ----------
def sponsor():
    rel = "../"
    qa = [("What does a sponsor get?", "A photo and a short note each month on the horse you sponsor, your name (or your business's) on its page if you want it there, and an invitation to come out and meet it. Businesses get a logo on this page and a thank-you on the ranch's social channels."),
          ("How long does it last?", "Month to month. Stop whenever you need to; the horse stays."),
          ("Can two people sponsor the same horse?", "Yes. Care for one horse costs more than most single sponsorships, so several sponsors on one horse is normal and welcome."),
          ("Is it tax-deductible?", f"{O['name']} is a 501(c)(3), so yes, to the extent the law allows. You'll get a receipt for each payment.")]
    levels = f'''<div class="levels" data-how="levels">
<div><span class="label">Friend</span><div class="a">$27</div><p class="per">a month · three days of hay and feed</p><ul><li>Monthly photo and note on your horse</li><li>Your first name on its page, if you like</li><li>A receipt for every payment</li></ul></div>
<div><span class="label">Sponsor</span><div class="a">$90</div><p class="per">a month · a quarter of one horse's month</p><ul><li>Everything above</li><li>Come out and meet your horse</li><li>Named in the monthly email</li></ul></div>
<div><span class="label">Business</span><div class="a">$360</div><p class="per">a month · one horse's whole month</p><ul><li>Everything above</li><li>Your logo on this page and on the horse's page</li><li>A thank-you post on the ranch's channels</li></ul></div></div>
<p class="note">Suggested from Braxton's own costs: $9 a day for hay and feed, about $360 a month for one horse. The ranch sets the final levels.</p>'''
    cards = "".join(f'''<article><a href="{rel}horses/{h["slug"]}/"><img src="{rel}assets/photos/horse-{h["slug"]}.jpg" alt="{e(h["alt"])}" width="1200" height="1500" loading="lazy"></a><div>{status_label(h)}<h3>{e(h["title"])}</h3><p>{e(h["lede"])}</p><p class="how-sp">Sponsoring {e(h["title"])} pays for the feed, care and farrier {"she needs" if h.get("pron") == "she" else "he needs"}, and you'll get {"her" if h.get("pron") == "she" else "his"} updates every month.</p><a class="btn fill" href="?horse={h["slug"]}#start">Sponsor {e(h["title"])}</a></div></article>''' for h in D["horses"])
    body = ph("Sponsor a horse", "One horse. Your name on its story.", "Pick a horse, cover part of its care each month, and follow it from the day it arrived to the day it's well.", img="horse-sign", alt="A bay horse at the fence in front of the pink Butterfly Ranch sign", crumbs=[("Home", ""), ("Sponsor a horse", None)], rel=rel)
    body += f'''
<section class="dark"><div class="wrap">{head("Pick a horse", "The four horses you can sponsor", "Only the horses in the rescue program are open for sponsorship. The other horses at the ranch are Braxton's own.", f'<a href="{rel}horses/">Meet the herd →</a>')}
<div class="sp-horses">{cards}</div></div></section>
<section><div class="wrap">{head("Levels", "Three ways to sponsor")}{levels}</div></section>
<section id="start"><div class="wrap">{head("Start", "Sponsor a horse today", "Choose the horse and what you'd like to give each month. Stop any time from your receipt.")}
<form class="giver sponsor-form" data-sponsor-form data-how="giver" novalidate aria-label="Start a sponsorship">
  <label class="field">Horse<select name="horse">{"".join(f'<option value="{h["slug"]}">{e(h["title"])}</option>' for h in D["horses"])}</select></label>
  <div class="other"><span>Each month</span><input type="number" name="amount" min="5" inputmode="numeric" placeholder="$" aria-label="Monthly amount in dollars"></div>
  <label class="check"><input type="checkbox" name="name_on_page"> Show my first name on the horse's page</label>
  <button class="btn fill" type="submit">Sponsor monthly</button>
  <p class="fine">A monthly gift on the ranch's own Stripe account, with a receipt for every payment.</p>
  <p class="sent" role="status"></p>
</form></div></section>

<section><div class="wrap">{head("Business sponsors", "Norman businesses behind the herd", "Sponsor a horse as a business and your logo sits here and on the horse's page.")}
<div class="logos" data-how="logos"><div>Your business here</div><div>Your business here</div><div>Your business here</div><div>Your business here</div></div>
<p style="margin-top:28px"><a class="btn fill" href="mailto:?subject=Sponsoring%20a%20horse%20at%20Butterfly%20Ranch">Ask about sponsoring</a> <span class="tbc" style="margin-left:12px">Email address to be added.</span></p></div></section>
<section class="dark"><div class="wrap">{head("Questions", "Sponsoring, answered")}{faq_html(qa)}</div></section>
{updates(rel)}'''
    ld = [crumbs_ld([("Home", ""), ("Sponsor a horse", "sponsor/")]), faq_ld(qa)]
    write("sponsor/", page("sponsor/", f"Sponsor a horse · {O['name']}", "Sponsor one rescue horse at Butterfly Rescue Ranch in Norman, Oklahoma, by the month. Monthly updates, your name on its page, business logos welcome.", body, ld, current="sponsor/"))

# ---------- VOLUNTEER ----------
def volunteer():
    rel = "../"
    qa = [("Who can volunteer?", "Anyone who wants to help the ranch and its rescued horses: individuals, students looking for service hours, groups, or someone who simply loves horses."),
          ("What will I do?", "Help with what the ranch needs that week and with the care of the rescued horses, guided by the staff."),
          ("Do I need horse experience?", "<span class=\"tbc\">Braxton will confirm.</span> Tell the ranch what you've done before and it will match you to work that fits. Anyone working directly with a horse is shown how first."),
          ("How old do volunteers have to be?", "<span class=\"tbc\">The ranch's minimum age and the rule for under-18s with a parent will be stated here.</span>"),
          ("When are volunteer days?", "<span class=\"tbc\">Regular days and times will be listed here once the ranch sets them.</span> Tell us when you're free in the form and we'll match you to one."),
          ("Can a group or a class come out?", f"Yes. Call {O['phone']} and we'll plan a barn day around your group.")]
    body = ph("Volunteer", "Make a difference, one horse at a time", "Every horse deserves care, patience and a chance at a better life. Volunteers make that possible here. With horse experience or without, there's a place for you at Butterfly Ranch.", img="vol-grooming", alt="A ranch hand in a cap, her face turned away, brushes the leg of a white horse tied at the red gate", crumbs=[("Home", ""), ("Volunteer", None)], rel=rel, pos="50% 42%")
    body += f'''
<section class="state"><div class="wrap"><p><b>Give your time. Change a horse's story.</b> Volunteers keep the ranch a safe, steady place for rescued horses, from everyday chores to supporting the people who make the mission possible. A willingness to learn, lend a hand and care for these animals is a great place to start.</p></div></section>
<section><div class="wrap"><div class="two">
<div>{head("Sign up", "Tell us about you")}
<form class="steps-form" data-preview data-steps data-how="volunteer" novalidate aria-label="Volunteer sign-up">
  <div class="sf-bar" aria-hidden="true"><i></i></div>
  <fieldset class="sf-step" data-step="1"><legend class="sf-q">What would you like to help with?</legend><p class="sf-hint">Pick any.</p>
    <div class="picks">
      <label class="pick"><input type="checkbox" name="i" value="feeding"><span><b>Feeding</b><small>Hay, water, supplements</small></span></label>
      <label class="pick"><input type="checkbox" name="i" value="grooming"><span><b>Grooming</b><small>Brushing, feet, leading</small></span></label>
      <label class="pick"><input type="checkbox" name="i" value="barn"><span><b>Barn days</b><small>Mucking, fences, hay</small></span></label>
      <label class="pick"><input type="checkbox" name="i" value="events"><span><b>Events and camps</b><small>Extra hands on busy days</small></span></label>
      <label class="pick"><input type="checkbox" name="i" value="skills"><span><b>A skill</b><small>Photos, fencing, vet, farrier</small></span></label>
    </div>
    <div class="sf-nav"><button class="btn fill sf-next" type="button">Next</button></div>
  </fieldset>
  <fieldset class="sf-step" data-step="2"><legend class="sf-q">When are you usually free?</legend><p class="sf-hint">Pick any that fit.</p>
    <div class="picks two">
      <label class="pick"><input type="checkbox" name="when" value="weekday-am"><span><b>Weekday mornings</b></span></label>
      <label class="pick"><input type="checkbox" name="when" value="weekday-pm"><span><b>Weekday evenings</b></span></label>
      <label class="pick"><input type="checkbox" name="when" value="weekends"><span><b>Weekends</b></span></label>
      <label class="pick"><input type="checkbox" name="when" value="any"><span><b>Whenever you need me</b></span></label>
    </div>
    <div class="sf-nav"><button class="sf-back" type="button">Back</button><button class="btn fill sf-next" type="button">Next</button></div>
  </fieldset>
  <fieldset class="sf-step" data-step="3"><legend class="sf-q">How should the ranch reach you?</legend>
    <label class="field">Your name<input name="name" autocomplete="name" required></label>
    <label class="field">Email<input type="email" name="email" autocomplete="email" inputmode="email" required></label>
    <label class="field">Phone <span class="opt">optional</span><input type="tel" name="phone" autocomplete="tel" inputmode="tel"></label>
    <label class="field">Anything else? <span class="opt">optional</span><textarea name="note" rows="2"></textarea></label>
    <div class="sf-nav"><button class="sf-back" type="button">Back</button><button class="btn fill" type="submit">Count me in</button></div>
    <p class="sf-err" role="alert" hidden></p>
  </fieldset>
  <div class="sf-done" hidden tabindex="-1"><h3>Thank you, <span data-first></span>.</h3><p>Braxton or Anna will get in touch about a first barn day.</p><p class="sf-note">This is a preview site, so the form isn't connected yet and nothing was sent. On the live site this goes straight to the ranch.</p></div>
</form></div>
<div>{head("What the work is", "A day at the barn")}
<ol class="steps">
<li><span class="n">1</span><div><h3>Feed and water</h3><p>Morning and evening. Hay out, buckets filled, supplements measured by the labels on the jugs.</p></div></li>
<li><span class="n">2</span><div><h3>Grooming and groundwork</h3><p>Brushing, picking feet, leading. This is where a shy horse learns people are all right.</p></div></li>
<li><span class="n">3</span><div><h3>Barn days</h3><p>Mucking, fence repair, hay stacking, tack cleaning. Bring gloves.</p></div></li>
<li><span class="n">4</span><div><h3>Events and camps</h3><p>Extra hands for camps and open days.</p></div></li>
</ol></div>
</div></div></section>
<section class="events" id="dates"><div class="wrap">{head("Coming up", "Dates at the ranch", "Pick a date and you'll get a reminder the day before. Braxton sets the dates; they appear here as she does.")}
<div class="cal">
  <div><span class="label">Every week</span><h3>Barn day</h3><p>Feeding, mucking, fences and hay. No experience needed; bring gloves.</p><span class="when tbc">Day and time to be set</span></div>
  <div><span class="label">Before your first barn day</span><h3>Volunteer orientation</h3><p>A walk round the barn, the safety rules, and the horses you'll work around.</p><span class="when tbc">Dates to be set</span></div>
  <div><span class="label">Open to everyone</span><h3>Meet the horses</h3><p>Come out, meet Rico and the herd, and hear their stories from Braxton.</p><span class="when tbc">Dates to be set</span></div>
</div>
<p class="note" style="margin-top:18px">On the live site each date has a booking button, with a text and email reminder before it.</p></div></section>
<section class="dark"><div class="wrap">{head("Questions", "Volunteering, answered")}{faq_html(qa)}</div></section>
{band(rel, "Be part of their story", "Take the first step toward helping rescued horses: sign up above, or give once or monthly.")}'''
    ld = [crumbs_ld([("Home", ""), ("Volunteer", "volunteer/")]), faq_ld([(q, a) for q, a in qa if "tbc" not in a])]
    write("volunteer/", page("volunteer/", f"Volunteer · {O['name']}", "Volunteer at Butterfly Rescue Ranch in Norman, Oklahoma: feeding, grooming, barn days and events. No horse experience needed.", body, ld, current="volunteer/"))

# ---------- PROGRAM ----------
def program():
    rel = "../"
    def rows(items): return "".join(f'<div class="row"><span class="what">{e(w)}</span><span class="dots"></span><span class="price">{e(p)}</span>{f"<small class=meta>{e(m)}</small>" if m else ""}</div>' for w, p, m in items)
    body = ph("The program", "Lessons and camps", "Kids and adults come out to ride, learn horsemanship and get away from city life. Rico, Reba and Dandelion all carry riders, and lessons and camps help keep the rescue fed.", img="friends", alt="Two horses, a bay with a wide blaze and a chestnut, stand head to head at a wooden feeder", crumbs=[("Home", ""), ("Program", None)], rel=rel)
    body += f'''
<section class="dark"><div class="wrap"><div class="prog">
<figure><img src="{rel}assets/photos/chestnut-sky.jpg" alt="A chestnut horse with a white blaze stands in the pen under a wide blue sky" width="1200" height="1600" loading="lazy"><figcaption>In the pens, between lessons.</figcaption></figure>
<div class="flyer" data-how="flyer" data-how-at="end">
  <h3>Summer camps</h3><p class="soft" style="font-size:15.5px;margin:0 0 6px">Last summer's camps. <span class="tbc">2026 dates to come.</span></p>{rows(D["camps"])}
  <h3>Breakaway lessons</h3>{rows(D["lessons"])}
  <p class="soft" style="font-size:15.5px;margin-top:18px">Camps hold a spot with a $100 non-refundable deposit. To book, text Anna at <a href="sms:{O["camp_phone_e164"]}">{O["camp_phone"]}</a>.</p>
</div></div></div></section>
<section><div class="wrap">{head("Why it matters", "Lessons that feed the rescue", "Every lesson and camp helps pay for hay, farrier and vet care for the rescue horses. Come ride, and you're part of it.")}
<div class="gallery pair"><div><img src="{rel}assets/photos/student-bucket.jpg" alt="A student seen from behind brushes a chestnut horse beside a pink bucket" width="1200" height="1600" loading="lazy"></div><div><img src="{rel}assets/photos/braids.jpg" alt="A horse's mane in neat braids" width="1200" height="1600" loading="lazy"></div></div></div></section>
{band(rel)}'''
    ld = [crumbs_ld([("Home", ""), ("Program", "program/")])]
    write("program/", page("program/", f"Lessons and camps · {O['name']}", "Riding lessons and summer horse camps at Butterfly Rescue Ranch in Norman, Oklahoma. Every lesson helps feed the rescue horses.", body, ld, current="program/"))

# ---------- ABOUT ----------
def about():
    rel = "../"
    people = "".join(f'<div><img src="{rel}assets/{p["img"]}" alt="{e(p["alt"])}" width="900" height="1000" loading="lazy"><h3>{e(p["name"])}</h3><div class="role">{e(p["role"])}</div><p>{e(p["bio"])}</p></div>' for p in D["people"])
    body = ph("About", "Started in 2022, for the horses", "Braxton started Butterfly Ranch because the community needed a place where kids and adults could spend time with horses and get away from city life. The rescue grew out of that, and it is now the heart of it.", img="sign-sky", alt="The pink Butterfly Ranch sign on a dark block wall under a big Oklahoma sky", crumbs=[("Home", ""), ("About", None)], rel=rel)
    body += f'''
<section><div class="wrap">{head("The people", "The people at the barn")}<div class="people">{people}</div>
</div></section>
<section>
  <div class="wrap">
    {head("In numbers", "What the ranch is, in plain figures", "From Braxton's own answers to the class, October 2026.")}
    <div class="stats">
      <div><span class="n">{O["rescued"]}</span><p>horses rescued since {O["founded"]}</p></div>
      <div><span class="n">{O["rescues_now"]}</span><p>rescue horses at the ranch right now: <a href="{rel}horses/">meet them</a></p></div>
      <div><span class="n">${O["cost_month"]}</span><p>what one horse's set costs come to each month <a href="{rel}donate/#costs">see where it goes</a></p></div>
      <div><span class="n">$9</span><p>a day of hay and feed for one horse <a href="{rel}donate/?amt=9">give a day</a></p></div>
    </div>
  </div>
</section>
<section class="dark"><div class="wrap">{head("What we believe", "Hopeful, not heartbreaking")}
<div class="two"><div><p class="soft">We don't lead with the worst photo of a horse's life. We show the recovery: weight coming back, feet fixed, the first day a horse walks to the gate on its own. Where a horse came from is part of its story, told plainly, once.</p></div>
<div><p class="soft">We publish what things cost and where gifts went. Every horse has a page that is updated as it recovers, and every donor hears back about the horse they helped. Your name stays private unless you ask to be thanked by name.</p></div></div></div></section>
<section><div class="wrap">{head("The facts", "On the record")}
<table data-how="facts"><tbody><tr><td>Legal name</td><td>{e(O["name"])}</td></tr><tr><td>Status</td><td>501(c)(3) nonprofit <span class="tbc">(EIN to be shown)</span></td></tr><tr><td>Founded</td><td>{O["founded"]}, by Braxton Brackin</td></tr><tr><td>Where</td><td>{e(O["street"])}, {e(O["city"])}, Oklahoma {O["zip"]}</td></tr><tr><td>Phone</td><td>{PHONE}</td></tr><tr><td>What we do</td><td>Rescue and rehabilitate horses, in the open; riding lessons and camps</td></tr><tr><td>Photos and film</td><td>{e(D["credits"])}</td></tr><tr><td>This site</td><td>A concept by <a href="https://station.solutions/" target="_blank" rel="noopener">Station</a>, not yet the ranch's official website</td></tr></tbody></table></div></section>
{band(rel)}'''
    ld = [crumbs_ld([("Home", ""), ("About", "about/")]),
          {"@context": "https://schema.org", "@type": "Person", "name": "Braxton Brackin", "jobTitle": "Founder & CEO", "worksFor": {"@type": "NGO", "name": O["name"]}, "url": BASE + "about/"}]
    write("about/", page("about/", f"About · {O['name']}", "Butterfly Rescue Ranch is a 501(c)(3) horse rescue founded in 2022 by Braxton Brackin in Norman, Oklahoma. Meet the team and read what the ranch stands for.", body, ld, current="about/"))

# ---------- VISIT ----------
def visit():
    rel = "../"
    body = ph("Visit", "Come meet the herd", "We're a working barn, so please call before you come out. Lessons and camps are booked by text.", img="gate", alt="The red pipe entrance gate of the ranch with the sign beyond", crumbs=[("Home", ""), ("Visit", None)], rel=rel)
    body += f'''
<section><div class="wrap"><div class="visit">
<div data-how="where" data-how-at="end"><h3>Where</h3><p>{e(O["street"])}<br>{e(O["city"])}, Oklahoma {O["zip"]}<br><a href="{O["maps"]}" target="_blank" rel="noopener">Open in Maps</a></p></div>
<div data-how="call" data-how-at="end"><h3>Call first</h3><p>We're a working barn, so please call before you come out.<br>{PHONE}</p></div>
<div><h3>Camps and lessons</h3><p>Text Anna at <a href="sms:{O["camp_phone_e164"]}">{O["camp_phone"]}</a>.</p></div>
</div>
<div class="trouble" id="trouble"><span class="label">Found a horse in trouble?</span><h2>A horse loose, hurt or going hungry</h2>
<ol class="steps">
<li><span class="n">1</span><div><h3>Keep yourself safe</h3><p>If a horse is loose on a road, call 911 first. Don't try to catch a horse you don't know.</p></div></li>
<li><span class="n">2</span><div><h3>Note where it is</h3><p>The road or address, what you can see, and a photo if you can take one safely.</p></div></li>
<li><span class="n">3</span><div><h3>Call the ranch</h3><p>{PHONE}. The ranch can't take every horse, but Braxton will tell you what to do next. Owners who can no longer keep a horse can call the same number.</p></div></li>
</ol></div>
<div class="gallery pair" style="margin-top:64px"><div><img src="{rel}assets/photos/sign-flowers.jpg" alt="The Butterfly Ranch sign behind yellow wildflowers" width="1200" height="1600" loading="lazy"></div><div><img src="{rel}assets/photos/trough.jpg" alt="A bay horse stands by a full water trough with wildflowers along the fence" width="1200" height="1600" loading="lazy"></div></div></div></section>
{band(rel)}'''
    ld = [crumbs_ld([("Home", ""), ("Visit", "visit/")])]
    write("visit/", page("visit/", f"Visit · {O['name']}", "Visit Butterfly Rescue Ranch at 7475 By Drive, Norman, Oklahoma 73072. Call (405) 922-0839 before you come out.", body, ld, current="visit/"))


# ---------- GALLERY ----------
def _gallery():
    return json.load(open(os.path.join(ROOT, "assets", "gallery", "gallery.json"), encoding="utf-8"))

def gallery_strip():
    G = _gallery(); picks = G["rope"][:6]; n = sum(len(c["photos"]) for c in G["cats"])
    tiles = "".join(f'<a href="gallery/#{r["cat"]}"><img src="{r["thumb"]}" alt="{e(r["alt"])}" loading="lazy" width="560" height="560"></a>' for r in picks)
    return f'<section><div class="wrap">{head("The gallery", "See the whole ranch", f"{n} photos from the class visit: the horses, the barn and the work.", "<a href=gallery/>Open the gallery &rarr;</a>")}<div class="gstrip">{tiles}</div></div></section>'

def gallery():
    rel = "../"; G = _gallery(); n = sum(len(c["photos"]) for c in G["cats"])
    body = ph("Gallery", "The ranch, up close", f"{n} photos from the class's visit on 23 October 2026. Drag the rope, or pick a set below.", crumbs=[("Home", ""), ("Gallery", None)], rel=rel)
    body += f"""
<div data-gallery data-base="{rel}">
<div class="rope" data-rope tabindex="0" role="region" aria-roledescription="carousel" aria-label="Favourite photos on a rope">
  <svg class="rp-line" aria-hidden="true"><path d=""/></svg>
  <span class="rp-hint">Drag the rope &middot; tap the front photo to see its set</span>
  <div class="rp-cards"></div>
  <div class="rp-bar"><div class="rp-cap" aria-live="polite"></div><span class="rp-count"></span><button class="rp-btn rp-prev" type="button" aria-label="Previous photo">&lsaquo;</button><button class="rp-btn rp-next" type="button" aria-label="Next photo">&rsaquo;</button></div>
</div>
<section><div class="wrap">
  <div data-wall-head><span class="label">Every photo</span><h2 style="margin:8px 0 18px">Pick a set</h2></div>
  <div class="gtabs" role="tablist" aria-label="Photo sets"></div>
  <p class="g-lede" data-cat-lede></p>
  <div class="gwall"></div>
  <noscript><p>The gallery needs JavaScript to show the photos.</p></noscript>
</div></section>
</div>
<script src="{rel}assets/gallery.js?v=3" defer></script>
{band(rel)}"""
    ld = [crumbs_ld([("Home", ""), ("Gallery", "gallery/")]),
          {"@context": "https://schema.org", "@type": "ImageGallery", "name": "Butterfly Rescue Ranch gallery", "url": BASE + "gallery/", "about": O["name"], "numberOfItems": n}]
    write("gallery/", page("gallery/", f"Gallery · {O['name']}", f"{n} photos of Butterfly Rescue Ranch in Norman, Oklahoma: the horses, the ranch and the daily work.", body, ld, current="gallery/"))

# ---------- UPDATES ----------
def updates_page():
    rel = "../"
    body = ph("Updates", "News from the barn", "Short posts as horses arrive and recover. The first post goes up when the ranch is ready.", crumbs=[("Home", ""), ("Updates", None)], rel=rel)
    body += f'''<section style="padding-top:48px"><div class="wrap"><ol class="log" data-how="news">
<li><time>Oct 2026</time><div><h3>The OU class came out</h3><p>Students from the University of Oklahoma's marketing program spent a day at the ranch photographing and filming the horses for this site and the ranch's channels.</p></div></li>
<li><time>Soon</time><div><h3 class="tbc">The first horse's story</h3><p class="tbc">Braxton picks the horse; the ranch writes it.</p></div></li>
</ol></div></section>{updates(rel)}'''
    write("updates/", page("updates/", f"Updates · {O['name']}", "News from Butterfly Rescue Ranch in Norman, Oklahoma: horses arriving and recovering.", body, [crumbs_ld([("Home", ""), ("Updates", "updates/")])]))

# ---------- LINKS (bio page) ----------
def links():
    rel = "../"
    body = f'''<div class="ph plain"><div class="wrap" style="text-align:center;padding-top:48px"><div><span class="label">Butterfly Ranch</span><h1 style="margin:12px auto 10px;max-width:none">Every horse has a story.</h1><p class="lede" style="margin:0 auto">Norman, Oklahoma · 501(c)(3) horse rescue</p></div></div></div>
<section style="padding-top:40px"><div class="wrap" style="max-width:520px"><div style="display:grid;gap:12px" data-how="links">
<a class="btn fill" style="text-align:center;padding:18px" href="{rel}donate/">Donate</a>
<a class="btn line" style="text-align:center;padding:18px" href="{rel}sponsor/">Sponsor a horse</a>
<a class="btn line" style="text-align:center;padding:18px" href="{rel}horses/">Meet the horses</a>
<a class="btn line" style="text-align:center;padding:18px" href="{rel}volunteer/">Volunteer</a>
<a class="btn line" style="text-align:center;padding:18px" href="{rel}program/">Camps and lessons</a>
<a class="btn line" style="text-align:center;padding:18px" href="{rel}updates/">Get the monthly update</a>
<a class="btn line" style="text-align:center;padding:18px" href="tel:{O["phone_e164"]}">Call the ranch · {O["phone"]}</a>
</div></div></section>'''
    write("links/", page("links/", f"Links · {O['name']}", "Butterfly Rescue Ranch: donate, sponsor a horse, meet the horses, volunteer, camps and lessons.", body))

def redirects():
    moved = [("gray", "rico"), ("cream", "daisy"), ("buckskin", "dandelion"), ("chestnut-blaze", "reba")]
    moved += [(x, "") for x in ("bay-lightning", "bay-star", "dark-bay", "paint", "palomino-pony", "little-pinto", "chestnut-braids")]
    for old, new in moved:
        to = f"../{new}/" if new else "../"
        write(f"horses/{old}/", f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{BASE}horses/{new + "/" if new else ""}"><title>The horses</title><a href="{to}">This page has moved</a>')

def sitemap_and_llms():
    urls = ["", "horses/", "gallery/", "donate/", "sponsor/", "volunteer/", "program/", "about/", "visit/", "updates/", "links/"] + [f"horses/{h['slug']}/" for h in D["horses"]]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write(sm)
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(f"User-agent: *\nDisallow: /\n\n# Concept site, not yet the ranch's official website. Sitemap kept for when it goes live.\nSitemap: {BASE}sitemap.xml\n")
    llms = f"""# {O['name']}

> A 501(c)(3) horse rescue in {O['city']}, Oklahoma, founded in {O['founded']} by Braxton Brackin. Horses from kill pens, abusive homes and surrenders are rehabilitated, and every horse's recovery and costs are published on its own page. The ranch also runs riding lessons, summer camps and pony parties.

Address: {O['street']}, {O['city']}, {O['state']} {O['zip']}. Phone: {O['phone']}. Camps and lessons: text Anna at {O['camp_phone']}.

## Pages
- [Home]({BASE}): what the ranch does and the horses there now
- [The horses]({BASE}horses/): one page per horse, each with a journal of its recovery and costs
- [Donate]({BASE}donate/): one-time or monthly gifts by card, Apple Pay, Google Pay or bank; Venmo, mail, supplies, employer match
- [Sponsor a horse]({BASE}sponsor/): monthly sponsorship of one horse, with updates; business logos welcome
- [Volunteer]({BASE}volunteer/): feeding, grooming, barn days, events; no experience needed
- [Program]({BASE}program/): lessons and summer camps, with prices
- [About]({BASE}about/): the founder and team, what the ranch stands for, legal facts
- [Visit]({BASE}visit/): address, map, call first
- [Updates]({BASE}updates/): news from the barn

## Facts
- Status: 501(c)(3) nonprofit; gifts are tax-deductible as allowed by law
- Founded: {O['founded']}
- Founder: Braxton Brackin, Founder & CEO
- Barn manager and instructor: Anna Foote; instructor: Chloe Bjornberg
- Camps (last summer): Overnight Barrel Camp $600; Barrel Day Camp $375; Overnight Camp $500; River Day Camp $250–$325; Playday Camp $250. $100 deposit holds a spot.
- Lessons: ground lesson (half hour) $25; horseback lesson (one hour) $50.
- About $360 a month in set costs per horse: hay and feed $9 a day, supplements $50 a month, farrier $50 every six weeks; vet on top. Roughly 20 horses rescued since 2022; 4 rescue horses at the ranch now, including Rico, who stays for good.
- January 2027 goal: $2,000 to $3,000.

This is a concept site built by Station (station.solutions) with the University of Oklahoma MKT 4970 class, October 2026. It is not yet the ranch's official website.
"""
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8", newline="\n").write(llms)

if __name__ == "__main__":
    import shutil
    css = open(os.path.join(ROOT, "_src", "site.css"), encoding="utf-8").read() + "\n" + open(os.path.join(ROOT, "_src", "tear.css"), encoding="utf-8").read() + "\n" + open(os.path.join(ROOT, "_src", "forms.css"), encoding="utf-8").read() + "\n" + open(os.path.join(ROOT, "_src", "how.css"), encoding="utf-8").read() + "\n" + open(os.path.join(ROOT, "_src", "give.css"), encoding="utf-8").read() + "\n" + open(os.path.join(ROOT, "_src", "gallery.css"), encoding="utf-8").read()
    open(os.path.join(ROOT, "assets", "site.css"), "w", encoding="utf-8", newline="\n").write(css)
    shutil.copy(os.path.join(ROOT, "_src", "tear.js"), os.path.join(ROOT, "assets", "tear.js"))
    shutil.copy(os.path.join(ROOT, "_src", "forms.js"), os.path.join(ROOT, "assets", "forms.js"))
    shutil.copy(os.path.join(ROOT, "_src", "give.js"), os.path.join(ROOT, "assets", "give.js"))
    shutil.copy(os.path.join(ROOT, "_src", "chat.js"), os.path.join(ROOT, "assets", "chat.js"))
    shutil.copy(os.path.join(ROOT, "_src", "gallery.js"), os.path.join(ROOT, "assets", "gallery.js"))
    # the "How it works" switch: its copy lives in data.json ("how") and is written into the script
    how = open(os.path.join(ROOT, "_src", "how.js"), encoding="utf-8").read()
    assert "/*HOW_DATA*/null" in how
    how_data = {k: v for k, v in D["how"].items() if not k.startswith("_")}
    open(os.path.join(ROOT, "assets", "how.js"), "w", encoding="utf-8", newline="\n").write(how.replace("/*HOW_DATA*/null", json.dumps(how_data, ensure_ascii=False)))
    home(); horses(); gallery(); donate(); thanks(); sponsor(); volunteer(); program(); about(); visit(); updates_page(); links(); sitemap_and_llms(); redirects()
    print("built", 10 + len(D["horses"]), "pages")
