"""Builds the Butterfly Rescue Ranch concept site from data.json. One page per URL, shared chrome, JSON-LD on every page.
Run from anywhere: python _src/build.py. Output lands next to _src (the git root). Never hand-edit the generated HTML."""
import json, os, html, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tear_footer import tear_footer
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "_src", "data.json"), encoding="utf-8"))
O = D["org"]; BASE = O["url"]
TODAY = datetime.date.today().isoformat()
def e(s): return html.escape(str(s), quote=True)

NAV = [("The horses", "horses/"), ("Sponsor", "sponsor/"), ("Volunteer", "volunteer/"), ("Program", "program/"), ("About", "about/"), ("Visit", "visit/")]

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
<link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}assets/hero-poster.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Marcellus+SC&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/site.css?v={TODAY}">
{lds}
</head>
<body{BODYCLS}>
<a class="skip" href="#main">Skip to content</a>
<header>
  <div class="wrap">
    <a class="logo" href="{rel if rel else './'}" aria-label="{e(O['name'])}, home"><img class="dark-logo" src="{rel}assets/logo.png" alt="{e(O['short'])}" width="900" height="313"><img class="light-logo" src="{rel}assets/logo-white.png" alt="" width="900" height="313" aria-hidden="true"></a>
    <button class="menu" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav id="nav">{links}</nav>
    <button class="how-btn" type="button" aria-pressed="false" hidden title="Show which Station product runs each part of this page"><span class="how-sw" aria-hidden="true"></span>How it works</button>
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
    function label(){{var a=amt();btn.textContent=a?('Give $'+a+(freq()==='monthly'?' a month':'')):'Choose an amount'}}
    g.addEventListener('change',label); other.addEventListener('input',function(){{tiles.forEach(function(x){{x.checked=false}});label()}}); label();
    g.addEventListener('submit',function(ev){{ev.preventDefault();var a=amt();if(!a){{other.focus();return}}
      out.textContent='Preview: $'+a+(freq()==='monthly'?' a month':'')+' would go to checkout here. Payments switch on when the ranch connects its Givebutter account; nothing was charged.';out.classList.add('on')}});
  }}
}})();
</script>
<script src="{rel}assets/forms.js?v=1" defer></script><script src="{rel}assets/chat.js?v=4" defer></script><script src="{rel}assets/how.js?v={TODAY}" defer></script>
</body>
</html>"""

def write(path, content):
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

def updates(rel, what="the horses"):
    return f'''<section class="updates"><div class="wrap"><div class="upd"><div><span class="label">Updates from the barn</span><h2>Hear how {what} are doing</h2><p>One email a month, with the horse you helped and what it cost. No more than that.</p></div>
<form class="join" data-preview data-how="join" data-how-at="end" novalidate aria-label="Email updates"><div class="join-row"><label class="vh" for="join-email">Email</label><input id="join-email" type="email" name="email" autocomplete="email" inputmode="email" placeholder="you@example.com" required><button class="btn fill" type="submit">Get the updates</button></div><p class="join-fine">One email a month. Unsubscribe in one click.</p><p class="sent" role="status">This is a preview, so the sign-up isn't connected yet and nothing was sent.</p></form></div></div></section>'''

PHONE = f'<a href="tel:{O["phone_e164"]}">{O["phone"]}</a>'

# ---------- HOME ----------
def home():
    rel = ""
    herd = "".join(f'<a href="horses/{h["slug"]}/"><img src="assets/photos/horse-{h["slug"]}.jpg" alt="{e(h["alt"])}" width="1200" height="1500" loading="lazy"><h3>{e(h["title"])}</h3><p class="coat">{e(h["coat"])}</p></a>' for h in D["horses"][:8])
    body = f'''
<div class="film">
  <picture class="still"><source media="(max-aspect-ratio: 4/5)" srcset="assets/hero-poster-m.jpg"><img src="assets/hero-poster.jpg" alt="Horses at Butterfly Ranch look straight at the camera over the fence"></picture>
  <video autoplay muted loop playsinline preload="auto" aria-label="The horses of Butterfly Ranch coming to the fence, filmed at the ranch in October 2026; some shots are animated from photos"><source src="assets/hero-m.mp4" type="video/mp4" media="(max-aspect-ratio: 4/5)"><source src="assets/hero.mp4" type="video/mp4"></video>
  <div class="wrap">
    <span class="label">Horse rescue · Norman, Oklahoma</span>
    <h1>Every horse here has a story.</h1>
    <p class="lede">Rescued from kill pens and hard homes, brought back to health, and every step shown.</p>
    <div class="acts"><a class="btn fill" href="donate/">Donate</a><a class="btn ghost" href="horses/">Meet the horses</a></div>
  </div>
  <span class="credit">Filmed at the ranch by OU students, October 2026 · some shots animated from their photos</span>
</div>

<section class="state"><div class="wrap"><p>A horse that nobody wanted gets fed, shod, doctored and worked, slowly, <b>and every step of it is here for you to see.</b> That's the whole idea.</p></div></section>

<section>
  <div class="wrap">
    {head("The herd", "The horses at the ranch right now", "Every horse here has its own page, updated as it recovers, with what was spent and who helped.", '<a href="horses/">See all the horses →</a>')}
    <div class="herd" data-how="herd">{herd}</div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    {head("How a horse comes through", "Rescue, rehab, and every step in the open")}
    <div class="path">
      <ol class="steps">
        <li><span class="n">1</span><div><h3>Rescue</h3><p>Horses come to us from dangerous places: kill pens, abusive homes, and owners who can no longer keep them.</p></div></li>
        <li><span class="n">2</span><div><h3>Rehabilitation</h3><p>Feed, supplements, farrier, vet care and time. The work goes at the horse's pace, not ours.</p></div></li>
        <li><span class="n">3</span><div><h3>Followed, in public</h3><p>Every step goes on the horse's page: what was done, what it cost and who helped. Donors see exactly where their gift went.</p></div></li>
      </ol>
      <figure><img src="assets/photos/student-bucket.jpg" alt="A student in a maroon shirt and cap, seen from behind, brushes a chestnut horse beside a pink feed bucket, the ranch sign behind them" width="1200" height="1600" loading="lazy"><figcaption>Grooming by the pens, with the sign behind.</figcaption></figure>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    {head("In numbers", "What the ranch is, in plain figures", "The dashes are deliberate. The ranch fills these in from its own records rather than publishing a guess.")}
    <div class="stats">
      <div><span class="n">{len(D["horses"])}</span><p>horses photographed at the ranch on 23 October 2026</p></div>
      <div><span class="n">{O["founded"]}</span><p>the year Braxton started the ranch</p></div>
      <div><span class="n"><i>—</i></span><p>horses rescued so far <span class="tbc">(to confirm)</span></p></div>
      <div><span class="n">$<i>—</i></span><p>what one horse costs each month <a href="donate/#costs">see where it goes</a></p></div>
    </div>
  </div>
</section>

{band(rel)}

<section>
  <div class="wrap">
    {head("The program", "Lessons, camps and pony parties", "Kids and adults come out to ride, learn horsemanship and get away from city life. Lessons and camps help keep the rescue fed.", '<a href="program/">Camps, lessons and pony parties →</a>')}
    <div class="gallery">
      <div class="wide"><img src="assets/photos/friends.jpg" alt="Two horses, a bay with a wide blaze and a chestnut, stand head to head at a wooden feeder" width="1600" height="1000" loading="lazy"></div>
      <div><img src="assets/photos/goofy.jpg" alt="A bay horse lifts its head high over the fence, lip curled, showing off" width="1200" height="1600" loading="lazy"></div>
      <div><img src="assets/photos/saddles.jpg" alt="Western saddles and a striped saddle blanket racked against the barn wall" width="1200" height="1600" loading="lazy"></div>
      <div><img src="assets/photos/trough.jpg" alt="A bay horse stands by a full water trough with wildflowers along the fence" width="1200" height="1600" loading="lazy"></div>
      <div><img src="assets/photos/goat.jpg" alt="A brown and white goat with long ears looks at the camera beside a horse trailer" width="1200" height="1600" loading="lazy"></div>
    </div>
  </div>
</section>

{updates(rel)}'''
    write("", page("", f"{O['name']} · Horse rescue in Norman, Oklahoma", "Butterfly Rescue Ranch is a 501(c)(3) horse rescue in Norman, Oklahoma. Horses from kill pens, abusive homes and surrenders are rehabilitated in the open: follow every horse, donate, sponsor or volunteer.", body, home=True))

# ---------- HORSES ----------
def horses():
    rel = "../"
    herd = "".join(f'<a href="{h["slug"]}/"><img src="{rel}assets/photos/horse-{h["slug"]}.jpg" alt="{e(h["alt"])}" width="1200" height="1500" loading="lazy"><h3>{e(h["title"])}</h3><p class="coat">{e(h["coat"])}</p></a>' for h in D["horses"])
    body = ph("The herd", "The horses at the ranch", f"Every one of them has a page that follows it from the day it arrived. <span class=\"tbc\">Names and stories are Braxton's to add; the photos are from the ranch on 23 October 2026.</span>", crumbs=[("Home", ""), ("The horses", None)], rel=rel)
    body += f'<section><div class="wrap"><div class="herd" data-how="herd">{herd}</div></div></section>{band(rel)}{updates(rel)}'
    ld = [crumbs_ld([("Home", ""), ("The horses", "horses/")]),
          {"@context": "https://schema.org", "@type": "ItemList", "name": "Horses at Butterfly Rescue Ranch", "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "name": h["title"], "url": f"{BASE}horses/{h['slug']}/"} for i, h in enumerate(D["horses"])]}]
    write("horses/", page("horses/", f"The horses · {O['name']}", "Meet the rescue horses at Butterfly Rescue Ranch in Norman, Oklahoma. Each horse has its own page, updated as it recovers.", body, ld, current="horses/"))
    for h in D["horses"]:
        horse(h)

def horse(h):
    rel = "../../"
    others = [x for x in D["horses"] if x["slug"] != h["slug"]][:4]
    more = "".join(f'<a href="../{x["slug"]}/"><img src="{rel}assets/photos/horse-{x["slug"]}.jpg" alt="{e(x["alt"])}" width="1200" height="1500" loading="lazy"><h3>{e(x["title"])}</h3><p class="coat">{e(x["coat"])}</p></a>' for x in others)
    body = f'''
<div class="ph"><div class="wrap">
  <div><p class="crumbs"><a href="{rel}">Home</a> › <a href="../">The horses</a> › {e(h["title"])}</p><span class="label">{e(h["status"])}</span><h1>{e(h["title"])}</h1>
  <p class="lede">{e(h["coat"])}. <span class="tbc">Name, age, where it came from and its story are Braxton's to add. This page shows the layout every horse will get.</span></p>
  <div class="acts" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn fill" href="{rel}sponsor/">Sponsor this horse</a><a class="btn line" href="{rel}donate/">Give toward its care</a></div></div>
  <img src="{rel}assets/photos/horse-{h["slug"]}.jpg" alt="{e(h["alt"])}" width="1200" height="1500" style="aspect-ratio:4/5">
</div></div>

<section class="dark">
  <div class="wrap">
    {head("The journal", "From the day it arrived", "Updated as the horse recovers, with what was spent and who helped, so donors can see what their gift did.")}
    <div class="journal" data-how="journal">
      <aside class="card-id" aria-label="Horse details">
        <span class="label">{e(h["status"])}</span>
        <div class="name">{e(h["title"])}</div>
        <dl><dt>Coat</dt><dd>{e(h["coat"])}</dd><dt>Came from</dt><dd class="tbc">Kill pen, auction or surrender</dd><dt>Arrived</dt><dd class="tbc">Month, year</dd><dt>Breed, age</dt><dd class="dash">—</dd><dt>Spent so far</dt><dd class="dash">$ —</dd><dt>Sponsored by</dt><dd class="tbc">Open</dd></dl>
        <a class="btn fill" href="{rel}sponsor/">Sponsor this horse</a>
      </aside>
      <ol class="log">
        <li><time>Day 1</time><div><h3>Arrival</h3><p>Where the horse came from, its weight and condition, and the first vet check. Intake photo here.</p></div><span class="cost">Intake vet · $ —</span></li>
        <li><time>Week 2</time><div><h3>Feet and teeth</h3><p>First farrier visit and dental float. What the farrier found, in plain words.</p></div><span class="cost">Farrier and dental · $ —</span></li>
        <li><time>Month 2</time><div><h3>Putting weight back on</h3><p>Feed plan, weight change, and the first time the horse comes to the gate on its own.</p></div><span class="cost">Feed · $ — a month</span></li>
        <li><time>Month 4</time><div><h3>Back to work</h3><p>Groundwork, then saddle time when the horse is sound. Photos as it fills out.</p></div></li>
        <li><time>Recovered</time><div><h3>Well</h3><p>Sound, at weight, and settled. A thank-you to every donor who helped get it here, and what the whole journey cost.</p></div><span class="cost">Total · $ —</span></li>
      </ol>
    </div>
  </div>
</section>

<section><div class="wrap">{head("Also at the ranch", "More of the herd", more=f'<a href="../">All the horses →</a>')}<div class="herd">{more}</div></div></section>
{band(rel, "Help this horse", "Sponsor it by the month, or give once toward its feed, farrier and vet care. Either way you'll hear how it's doing.")}
{updates(rel, "this horse and the others")}'''
    ld = [crumbs_ld([("Home", ""), ("The horses", "horses/"), (h["title"], f"horses/{h['slug']}/")]),
          {"@context": "https://schema.org", "@type": "Animal" if False else "Thing", "name": h["title"], "description": f"A rescue horse at {O['name']}, {O['city']}, Oklahoma. {h['coat']}.", "image": f"{BASE}assets/photos/horse-{h['slug']}.jpg", "url": f"{BASE}horses/{h['slug']}/"}]
    write(f"horses/{h['slug']}/", page(f"horses/{h['slug']}/", f"{h['title']} · The horses · {O['name']}", f"{h['title']} is a rescue horse at Butterfly Rescue Ranch in Norman, Oklahoma. Follow its journal, sponsor it, or give toward its care.", body, ld, current="horses/"))

# ---------- DONATE ----------
def donate():
    rel = "../"
    tiles = "".join(f'<label><input type="radio" name="amt" value="{t["amt"]}"{" checked" if i == 1 else ""}><span class="a">${t["amt"]}</span><span class="f">{e(t["for"])}</span></label>' for i, t in enumerate(D["tiers"]))
    qa = [("Is my gift tax-deductible?", f"{O['name']} is a registered 501(c)(3) nonprofit, so gifts are tax-deductible to the extent the law allows. You'll get a receipt by email for every gift. <span class=\"tbc\">The ranch's EIN will be shown here.</span>"),
          ("Where does the money go?", "Hay, feed and supplements, farrier work, vet care, vaccines and dental. The monthly cost of one horse is published on this page as the ranch fills in its figures, and every horse's page shows what was spent on it."),
          ("Can I give monthly?", "Yes. Choose <b>Monthly</b> above. Monthly gifts are what let the ranch plan feed and farrier visits ahead instead of month to month. You can stop at any time from the receipt email."),
          ("Can I give to one particular horse?", f"Yes. <a href=\"{rel}sponsor/\">Sponsor a horse</a> covers one horse's care by the month, and you'll get its updates. A one-time gift here goes wherever the need is that month."),
          ("Can I give supplies instead of money?", "Please do. Hay, feed, fly spray, wormer, hoof care, halters, lead ropes and brushes are all used daily. Call ahead before dropping anything off. A wish list is on its way."),
          ("Does my employer match gifts?", "Many do. Ask your HR team for their matching-gift form and send it to the ranch with your receipt; the ranch will complete its part.")]
    body = ph("Donate", "Give to the horses", "Every dollar goes to hay, feed and care, and you'll hear back about the horse it helped. Three steps: pick an amount, choose once or monthly, pay.", crumbs=[("Home", ""), ("Donate", None)], rel=rel)
    body += f'''
<section>
  <div class="wrap">
    <div class="give">
      <form class="giver" id="giver" data-how="giver" data-how-at="end" novalidate aria-label="Donation form">
        <div class="seg" role="radiogroup" aria-label="How often"><label><input type="radio" name="freq" value="once" checked><span>One time</span></label><label><input type="radio" name="freq" value="monthly"><span>Monthly</span></label></div>
        <div class="tiles">{tiles}</div>
        <div class="other"><span>Or another amount</span><input type="number" name="other" min="1" inputmode="numeric" placeholder="$" aria-label="Other amount in dollars"></div>
        <p class="impact" aria-live="polite"></p><button class="btn fill" type="submit">Give $50</button>
        <p class="fine">{e(O["name"])} is a 501(c)(3). Gifts are tax-deductible as allowed by law. Card, Venmo and PayPal at checkout. <span class="tbc">Checkout switches on when the ranch connects its Givebutter account.</span></p>
        <p class="sent" role="status"></p>
      </form>
      <div>
        <h2 style="margin-bottom:22px">Other ways to give</h2>
        <ul class="ways">
          <li><b>Venmo</b><p><span class="tbc">The ranch's Venmo handle will be here, with a QR code.</span></p></li>
          <li><b>By mail</b><p>Cheques to {e(O["name"])}, {e(O["street"])}, {e(O["city"])}, {O["state"]} {O["zip"]}.</p></li>
          <li><b>Supplies</b><p>Hay, feed, fly spray, wormer, hoof care, halters, lead ropes, brushes. <span class="tbc">Wish list to come.</span> Call first: {PHONE}.</p></li>
          <li><b>Employer match</b><p>Many employers double a gift. Ask HR for the form; the ranch will complete its part.</p></li>
          <li><b>Sponsor a horse</b><p>One horse, by the month, with its updates. <a href="{rel}sponsor/">How sponsoring works →</a></p></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section id="costs" class="dark">
  <div class="wrap">
    {head("Where it goes", "What one horse costs us each month", "Hay isn't free, and neither is a farrier. Here is the real monthly cost of keeping one rescue horse at the ranch, so you know what a gift covers.")}
    <div class="ledger-grid">
      <div>
        <div class="big"><span class="amt">$<i>—</i></span><span class="per soft">a month, for one rescue horse at the ranch</span></div>
        <table>
          <caption>One horse · one month</caption>
          <thead><tr><th>Item</th><th class="amt">Cost</th></tr></thead>
          <tbody>
            <tr><td>Hay<small>Shared across the herd</small></td><td class="amt dash">—</td></tr>
            <tr><td>Feed and supplements<small>Grain, minerals and supplements</small></td><td class="amt dash">—</td></tr>
            <tr><td>Farrier<small>Trim or shoes every 6 to 8 weeks, spread monthly</small></td><td class="amt dash">—</td></tr>
            <tr><td>Vet, vaccines and deworming<small>Routine care, spread monthly</small></td><td class="amt dash">—</td></tr>
            <tr><td>Dental<small>Yearly float, spread monthly</small></td><td class="amt dash">—</td></tr>
          </tbody>
          <tfoot><tr><td>One horse, one month</td><td class="amt dash">$ —</td></tr></tfoot>
        </table>
        <p class="note">The dashes are deliberate. The ranch fills these in from its own records rather than publishing a guess.</p>
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
    write("donate/", page("donate/", f"Donate · {O['name']}", "Give to the rescue horses at Butterfly Rescue Ranch, Norman, Oklahoma. One-time or monthly, card, Venmo or PayPal. A 501(c)(3); gifts are tax-deductible.", body, ld, current="donate/"))

# ---------- SPONSOR ----------
def sponsor():
    rel = "../"
    qa = [("What does a sponsor get?", "A photo and a short note each month on the horse you sponsor, your name (or your business's) on its page if you want it there, and an invitation to come out and meet it. Businesses get a logo on this page and a thank-you on the ranch's social channels."),
          ("How long does it last?", "Month to month. Stop whenever you need to; the horse stays."),
          ("Can two people sponsor the same horse?", "Yes. Care for one horse costs more than most single sponsorships, so several sponsors on one horse is normal and welcome."),
          ("Is it tax-deductible?", f"{O['name']} is a 501(c)(3), so yes, to the extent the law allows. You'll get a receipt for each payment.")]
    levels = f'''<div class="levels" data-how="levels">
<div><span class="label">Friend</span><div class="a">$<i style="font-style:normal;opacity:.35">—</i></div><p class="per">a month</p><ul><li>Monthly photo and note on your horse</li><li>Your first name on its page, if you like</li><li>A receipt for every payment</li></ul></div>
<div><span class="label">Sponsor</span><div class="a">$<i style="font-style:normal;opacity:.35">—</i></div><p class="per">a month</p><ul><li>Everything above</li><li>Come out and meet your horse</li><li>Named in the monthly email</li></ul></div>
<div><span class="label">Business</span><div class="a">$<i style="font-style:normal;opacity:.35">—</i></div><p class="per">a month</p><ul><li>Everything above</li><li>Your logo on this page and on the horse's page</li><li>A thank-you post on the ranch's channels</li></ul></div></div>
<p class="note">Levels and prices are the ranch's to set from its real monthly costs; the dashes stay until it does.</p>'''
    body = ph("Sponsor a horse", "One horse. Your name on its story.", "Pick a horse, cover part of its care each month, and follow it from the day it arrived to the day it's well.", img="horse-sign", alt="A bay horse at the fence in front of the pink Butterfly Ranch sign", crumbs=[("Home", ""), ("Sponsor a horse", None)], rel=rel)
    body += f'''
<section><div class="wrap">{head("Levels", "Three ways to sponsor")}{levels}</div></section>
<section class="dark"><div class="wrap">{head("Pick a horse", "Who needs a sponsor", "Every horse at the ranch is open for sponsorship right now.", f'<a href="{rel}horses/">All the horses →</a>')}
<div class="herd">{"".join(f'<a href="{rel}horses/{h["slug"]}/"><img src="{rel}assets/photos/horse-{h["slug"]}.jpg" alt="{e(h["alt"])}" width="1200" height="1500" loading="lazy"><h3 style="color:#f4ecef">{e(h["title"])}</h3><p class="coat" style="color:#b9aab1">{e(h["coat"])}</p></a>' for h in D["horses"][:8])}</div></div></section>
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
    qa = [("Do I need horse experience?", "No. Feeding, filling water, mucking and barn days need willing hands, not experience. Anyone working directly with a horse is shown how first."),
          ("How old do volunteers have to be?", "<span class=\"tbc\">The ranch's minimum age and the rule for under-18s with a parent will be stated here.</span>"),
          ("When are volunteer days?", "<span class=\"tbc\">Regular days and times will be listed here once the ranch sets them.</span> Tell us when you're free in the form and we'll match you to one."),
          ("Can a group or a class come out?", f"Yes. Call {O['phone']} and we'll plan a barn day around your group.")]
    body = ph("Volunteer", "Hands on. Horses first.", "Feeding, grooming, mucking, barn days. Tell us when you're free and the ranch will be in touch.", img="hand-nose", alt="A hand reaches up to a dark bay horse's nose over a wire fence", crumbs=[("Home", ""), ("Volunteer", None)], rel=rel, pos="50% 38%")
    body += f'''
<section><div class="wrap"><div class="two">
<div>{head("Sign up", "Tell us about you")}
<form class="steps-form" data-preview data-steps data-how="volunteer" novalidate aria-label="Volunteer sign-up">
  <div class="sf-bar" aria-hidden="true"><i></i></div>
  <fieldset class="sf-step" data-step="1"><legend class="sf-q">What would you like to help with?</legend><p class="sf-hint">Pick any. No horse experience needed.</p>
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
<li><span class="n">4</span><div><h3>Events and camps</h3><p>Extra hands for pony parties, camps and open days.</p></div></li>
</ol></div>
</div></div></section>
<section class="dark"><div class="wrap">{head("Questions", "Volunteering, answered")}{faq_html(qa)}</div></section>
{band(rel)}'''
    ld = [crumbs_ld([("Home", ""), ("Volunteer", "volunteer/")]), faq_ld([(q, a) for q, a in qa if "tbc" not in a])]
    write("volunteer/", page("volunteer/", f"Volunteer · {O['name']}", "Volunteer at Butterfly Rescue Ranch in Norman, Oklahoma: feeding, grooming, barn days and events. No horse experience needed.", body, ld, current="volunteer/"))

# ---------- PROGRAM ----------
def program():
    rel = "../"
    def rows(items): return "".join(f'<div class="row"><span class="what">{e(w)}</span><span class="dots"></span><span class="price">{e(p)}</span>{f"<small class=meta>{e(m)}</small>" if m else ""}</div>' for w, p, m in items)
    body = ph("The program", "Lessons, camps and pony parties", "Kids and adults come out to ride, learn horsemanship and get away from city life. Lessons and camps help keep the rescue fed.", img="friends", alt="Two horses, a bay with a wide blaze and a chestnut, stand head to head at a wooden feeder", crumbs=[("Home", ""), ("Program", None)], rel=rel)
    body += f'''
<section class="dark"><div class="wrap"><div class="prog">
<figure><img src="{rel}assets/photos/chestnut-sky.jpg" alt="A chestnut horse with a white blaze stands in the pen under a wide blue sky" width="1200" height="1600" loading="lazy"><figcaption>In the pens, between lessons.</figcaption></figure>
<div class="flyer" data-how="flyer" data-how-at="end">
  <h3>Summer camps</h3><p class="soft" style="font-size:15.5px;margin:0 0 6px">Last summer's camps. <span class="tbc">2026 dates to come.</span></p>{rows(D["camps"])}
  <h3>Breakaway lessons</h3>{rows(D["lessons"])}
  <h3>Pony parties</h3>{rows(D["parties"])}
  <p class="soft" style="font-size:15.5px;margin-top:18px">Camps hold a spot with a $100 non-refundable deposit. To book, text Anna at <a href="sms:{O["camp_phone_e164"]}">{O["camp_phone"]}</a>.</p>
</div></div></div></section>
<section><div class="wrap">{head("Why it matters", "Lessons that feed the rescue", "Every lesson, camp and pony party helps pay for hay, farrier and vet care for the rescue horses. Come ride, and you're part of it.")}
<div class="gallery pair"><div><img src="{rel}assets/photos/student-bucket.jpg" alt="A student seen from behind brushes a chestnut horse beside a pink bucket" width="1200" height="1600" loading="lazy"></div><div><img src="{rel}assets/photos/braids.jpg" alt="A horse's mane in neat braids" width="1200" height="1600" loading="lazy"></div></div></div></section>
{band(rel)}'''
    ld = [crumbs_ld([("Home", ""), ("Program", "program/")])]
    write("program/", page("program/", f"Lessons, camps and pony parties · {O['name']}", "Riding lessons, summer horse camps and pony parties at Butterfly Rescue Ranch in Norman, Oklahoma. Every lesson helps feed the rescue horses.", body, ld, current="program/"))

# ---------- ABOUT ----------
def about():
    rel = "../"
    people = "".join(f'<div><img src="{rel}assets/{p["img"]}" alt="{e(p["alt"])}" width="900" height="1000" loading="lazy"><h3>{e(p["name"])}</h3><div class="role">{e(p["role"])}</div><p>{e(p["bio"])}</p></div>' for p in D["people"])
    body = ph("About", "Started in 2022, for the horses", "Braxton started Butterfly Ranch because the community needed a place where kids and adults could spend time with horses and get away from city life. The rescue grew out of that, and it is now the heart of it.", img="sign-sky", alt="The pink Butterfly Ranch sign on a dark block wall under a big Oklahoma sky", crumbs=[("Home", ""), ("About", None)], rel=rel)
    body += f'''
<section><div class="wrap">{head("The people", "The people at the barn")}<div class="people">{people}</div>
</div></section>
<section class="dark"><div class="wrap">{head("What we believe", "Hopeful, not heartbreaking")}
<div class="two"><div><p class="soft">We don't lead with the worst photo of a horse's life. We show the recovery: weight coming back, feet fixed, the first day a horse walks to the gate on its own. Where a horse came from is part of its story, told plainly, once.</p></div>
<div><p class="soft">We publish what things cost and where gifts went. Every horse has a page that is updated as it recovers, and every donor hears back about the horse they helped. Your name stays private unless you ask to be thanked by name.</p></div></div></div></section>
<section><div class="wrap">{head("The facts", "On the record")}
<table data-how="facts"><tbody><tr><td>Legal name</td><td>{e(O["name"])}</td></tr><tr><td>Status</td><td>501(c)(3) nonprofit <span class="tbc">(EIN to be shown)</span></td></tr><tr><td>Founded</td><td>{O["founded"]}, by Braxton Brackin</td></tr><tr><td>Where</td><td>{e(O["street"])}, {e(O["city"])}, Oklahoma {O["zip"]}</td></tr><tr><td>Phone</td><td>{PHONE}</td></tr><tr><td>What we do</td><td>Rescue and rehabilitate horses, in the open; riding lessons, camps and pony parties</td></tr><tr><td>Photos and film</td><td>{e(D["credits"])}</td></tr><tr><td>This site</td><td>A concept by <a href="https://station.solutions/" target="_blank" rel="noopener">Station</a>, not yet the ranch's official website</td></tr></tbody></table></div></section>
{band(rel)}'''
    ld = [crumbs_ld([("Home", ""), ("About", "about/")]),
          {"@context": "https://schema.org", "@type": "Person", "name": "Braxton Brackin", "jobTitle": "Founder & CEO", "worksFor": {"@type": "NGO", "name": O["name"]}, "url": BASE + "about/"}]
    write("about/", page("about/", f"About · {O['name']}", "Butterfly Rescue Ranch is a 501(c)(3) horse rescue founded in 2022 by Braxton Brackin in Norman, Oklahoma. Meet the team and read what the ranch stands for.", body, ld, current="about/"))

# ---------- VISIT ----------
def visit():
    rel = "../"
    body = ph("Visit", "Come meet the herd", "We're a working barn, so please call before you come out. Lessons, camps and pony parties are booked by text.", img="gate", alt="The red pipe entrance gate of the ranch with the sign beyond", crumbs=[("Home", ""), ("Visit", None)], rel=rel)
    body += f'''
<section><div class="wrap"><div class="visit">
<div data-how="where" data-how-at="end"><h3>Where</h3><p>{e(O["street"])}<br>{e(O["city"])}, Oklahoma {O["zip"]}<br><a href="{O["maps"]}" target="_blank" rel="noopener">Open in Maps</a></p></div>
<div data-how="call" data-how-at="end"><h3>Call first</h3><p>We're a working barn, so please call before you come out.<br>{PHONE}</p></div>
<div><h3>Camps and lessons</h3><p>Text Anna at <a href="sms:{O["camp_phone_e164"]}">{O["camp_phone"]}</a>.</p></div>
</div>
<div class="gallery pair" style="margin-top:64px"><div><img src="{rel}assets/photos/sign-flowers.jpg" alt="The Butterfly Ranch sign behind yellow wildflowers" width="1200" height="1600" loading="lazy"></div><div><img src="{rel}assets/photos/trough.jpg" alt="A bay horse stands by a full water trough with wildflowers along the fence" width="1200" height="1600" loading="lazy"></div></div></div></section>
{band(rel)}'''
    ld = [crumbs_ld([("Home", ""), ("Visit", "visit/")])]
    write("visit/", page("visit/", f"Visit · {O['name']}", "Visit Butterfly Rescue Ranch at 7475 By Drive, Norman, Oklahoma 73072. Call (405) 922-0839 before you come out.", body, ld, current="visit/"))

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
<a class="btn line" style="text-align:center;padding:18px" href="{rel}program/">Camps, lessons and pony parties</a>
<a class="btn line" style="text-align:center;padding:18px" href="{rel}updates/">Get the monthly update</a>
<a class="btn line" style="text-align:center;padding:18px" href="tel:{O["phone_e164"]}">Call the ranch · {O["phone"]}</a>
</div></div></section>'''
    write("links/", page("links/", f"Links · {O['name']}", "Butterfly Rescue Ranch: donate, sponsor a horse, meet the horses, volunteer, camps and lessons.", body))

def sitemap_and_llms():
    urls = ["", "horses/", "donate/", "sponsor/", "volunteer/", "program/", "about/", "visit/", "updates/", "links/"] + [f"horses/{h['slug']}/" for h in D["horses"]]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write(sm)
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(f"User-agent: *\nDisallow: /\n\n# Concept site, not yet the ranch's official website. Sitemap kept for when it goes live.\nSitemap: {BASE}sitemap.xml\n")
    llms = f"""# {O['name']}

> A 501(c)(3) horse rescue in {O['city']}, Oklahoma, founded in {O['founded']} by Braxton Brackin. Horses from kill pens, abusive homes and surrenders are rehabilitated, and every horse's recovery and costs are published on its own page. The ranch also runs riding lessons, summer camps and pony parties.

Address: {O['street']}, {O['city']}, {O['state']} {O['zip']}. Phone: {O['phone']}. Camps and lessons: text Anna at {O['camp_phone']}.

## Pages
- [Home]({BASE}): what the ranch does and the horses there now
- [The horses]({BASE}horses/): one page per horse, each with a journal of its recovery and costs
- [Donate]({BASE}donate/): one-time or monthly gifts; card, Venmo, PayPal, mail, supplies, employer match
- [Sponsor a horse]({BASE}sponsor/): monthly sponsorship of one horse, with updates; business logos welcome
- [Volunteer]({BASE}volunteer/): feeding, grooming, barn days, events; no experience needed
- [Program]({BASE}program/): lessons, summer camps and pony parties, with prices
- [About]({BASE}about/): the founder and team, what the ranch stands for, legal facts
- [Visit]({BASE}visit/): address, map, call first
- [Updates]({BASE}updates/): news from the barn

## Facts
- Status: 501(c)(3) nonprofit; gifts are tax-deductible as allowed by law
- Founded: {O['founded']}
- Founder: Braxton Brackin, Founder & CEO
- Barn manager and instructor: Anna Foote; instructor: Chloe Bjornberg
- Camps (last summer): Overnight Barrel Camp $600; Barrel Day Camp $375; Overnight Camp $500; River Day Camp $250–$325; Playday Camp $250. $100 deposit holds a spot.
- Lessons: ground lesson (half hour) $25; horseback lesson (one hour) $50. Pony parties from $300.
- Monthly cost per horse and total horses rescued: to be published by the ranch.

This is a concept site built by Station (station.solutions) with the University of Oklahoma MKT 4970 class, October 2026. It is not yet the ranch's official website.
"""
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8", newline="\n").write(llms)

if __name__ == "__main__":
    import shutil
    css = open(os.path.join(ROOT, "_src", "site.css"), encoding="utf-8").read() + "\n" + open(os.path.join(ROOT, "_src", "tear.css"), encoding="utf-8").read() + "\n" + open(os.path.join(ROOT, "_src", "forms.css"), encoding="utf-8").read() + "\n" + open(os.path.join(ROOT, "_src", "how.css"), encoding="utf-8").read()
    open(os.path.join(ROOT, "assets", "site.css"), "w", encoding="utf-8", newline="\n").write(css)
    shutil.copy(os.path.join(ROOT, "_src", "tear.js"), os.path.join(ROOT, "assets", "tear.js"))
    shutil.copy(os.path.join(ROOT, "_src", "forms.js"), os.path.join(ROOT, "assets", "forms.js"))
    shutil.copy(os.path.join(ROOT, "_src", "chat.js"), os.path.join(ROOT, "assets", "chat.js"))
    # the "How it works" switch: its copy lives in data.json ("how") and is written into the script
    how = open(os.path.join(ROOT, "_src", "how.js"), encoding="utf-8").read()
    assert "/*HOW_DATA*/null" in how
    how_data = {k: v for k, v in D["how"].items() if not k.startswith("_")}
    open(os.path.join(ROOT, "assets", "how.js"), "w", encoding="utf-8", newline="\n").write(how.replace("/*HOW_DATA*/null", json.dumps(how_data, ensure_ascii=False)))
    home(); horses(); donate(); sponsor(); volunteer(); program(); about(); visit(); updates_page(); links(); sitemap_and_llms()
    print("built", 10 + len(D["horses"]), "pages")
