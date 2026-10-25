"""The torn-poster footer for every page (port of the 21st.dev "Pushpin Tear Footer", dressed for Butterfly Ranch).
Markup only; the tear, the pin's drop, the flaps, the clock and the buttons are driven by assets/tear.js and styled by the
tear section of site.css. Disclosures stay in a strip under the poster."""
import html

SHEET = "#a71c5a"      # the ranch magenta
PAPER = "#fbf8f6"      # the site's paper
PAPER_INK = "#2b2026"  # the site's ink
SEED = 7


def e(s):
    return html.escape(str(s), quote=True)


def mix(a, b, t):
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join("%02x" % round(x + (y - x) * t) for x, y in zip(pa, pb))


P = 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'


def icon(name):
    body = {
        "up": '<path d="M5.5 14.5 12 8l6.5 6.5"/>',
        "arrow": '<path d="M5 12h13M13 6.5 18.5 12 13 17.5"/>',
        "check": '<path d="m5.5 12.5 4 4 9-9.5"/>',
        "copy": '<path d="M13.5 4.5H7A2.5 2.5 0 0 0 4.5 7v10A2.5 2.5 0 0 0 7 19.5h10a2.5 2.5 0 0 0 2.5-2.5v-6.5"/><circle cx="18.5" cy="5.5" r="2.3"/>',
        "squiggle": '<path d="M3.5 15c1.8-3.2 3.6-3.2 5.4 0s3.6 3.2 5.4 0 3.6-3.2 5.4 0"/>',
        "pin": '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
        "link": '<path d="M10.5 13.5a3.5 3.5 0 0 0 5 0l3-3a3.5 3.5 0 0 0-5-5l-1 1M13.5 10.5a3.5 3.5 0 0 0-5 0l-3 3a3.5 3.5 0 0 0 5 5l1-1"/>',
        "heart": '<path d="M12 19.5s-7.5-4.4-7.5-10A4.2 4.2 0 0 1 12 7a4.2 4.2 0 0 1 7.5 2.5c0 5.6-7.5 10-7.5 10z"/>',
        "phone": '<path d="M8.2 4.5H6A1.5 1.5 0 0 0 4.5 6c0 7.5 6 13.5 13.5 13.5a1.5 1.5 0 0 0 1.5-1.5v-2.2l-3.5-1.5-1.8 1.8a10.5 10.5 0 0 1-5.3-5.3L10.7 9 9.2 5.5z"/>',
    }[name]
    return f'<svg viewBox="0 0 24 24" class="tpf-ico" aria-hidden="true" {P}>{body}</svg>'


def pin_svg(base):
    hi, mid, lo, deep = mix(base, "#ffffff", 0.62), base, mix(base, "#000000", 0.42), mix(base, "#000000", 0.66)
    return f'''<svg viewBox="0 0 100 200" class="tpf-pin-svg" aria-hidden="true"><defs>
<linearGradient id="tpf-ps" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{lo}"/><stop offset=".24" stop-color="{mid}"/><stop offset=".4" stop-color="{hi}"/><stop offset=".58" stop-color="{mid}"/><stop offset="1" stop-color="{deep}"/></linearGradient>
<radialGradient id="tpf-pt" cx=".38" cy=".3" r=".8"><stop offset="0" stop-color="{hi}"/><stop offset=".55" stop-color="{mid}"/><stop offset="1" stop-color="{lo}"/></radialGradient>
<linearGradient id="tpf-pn" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#5b616b"/><stop offset=".4" stop-color="#f4f5f7"/><stop offset=".7" stop-color="#a3a9b2"/><stop offset="1" stop-color="#4a4f57"/></linearGradient>
<filter id="tpf-pb" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.4"/></filter></defs>
<path d="M48.3 112h3.4l-.7 76-1 4-1-4z" fill="url(#tpf-pn)"/><ellipse cx="50" cy="191.5" rx="3.2" ry="1.1" fill="#2b0b19" opacity=".35"/>
<path d="M28 103v6.5a22 7 0 0 0 44 0V103z" fill="url(#tpf-ps)"/><ellipse cx="50" cy="103" rx="22" ry="7" fill="url(#tpf-pt)"/>
<path d="M41.5 38c1.6 16 4.6 26 3 36-1.8 10-13 19-14.6 29h40.2c-1.6-10-12.8-19-14.6-29-1.6-10 1.4-20 3-36z" fill="url(#tpf-ps)"/>
<path d="M16 22v14a34 13 0 0 0 68 0V22z" fill="url(#tpf-ps)"/><ellipse cx="50" cy="22" rx="34" ry="13" fill="url(#tpf-pt)"/>
<ellipse cx="50" cy="22" rx="33" ry="12.3" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width=".8"/>
<ellipse cx="37" cy="17.5" rx="12" ry="4" fill="#fff" opacity=".7" filter="url(#tpf-pb)"/>
<path d="M22 38c4 4.5 9.5 6.4 15 7" stroke="#fff" stroke-opacity=".35" stroke-width="2" fill="none" stroke-linecap="round" filter="url(#tpf-pb)"/>
<path d="M45 50c.8 8 1.6 14 .8 22" stroke="#fff" stroke-opacity=".45" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>'''


def tear_footer(rel, O, credits):
    flap_base = mix(PAPER, "#ffffff", 0.35)
    rim = mix(flap_base, "#ffffff", 0.6)
    grads = "".join(f'<linearGradient id="tpf-fg{k}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{mix(flap_base, "#3a1528", 0.34)}"/>'
                    f'<stop offset=".5" stop-color="{mix(flap_base, "#3a1528", 0.08)}"/><stop offset="1" stop-color="#ffffff"/></linearGradient>' for k in range(12))
    flaps = "".join(f'<path id="tpf-f{k}" fill="url(#tpf-fg{k})"/>' for k in range(12))
    i = lambda n: f' style="--i:{n}"'
    home = rel if rel else "./"
    tel = f"tel:{O['phone_e164']}"

    def col(side, n, title, links, cta):
        lis = "".join(f'<li><a href="{h}">{e(t)}</a></li>' for t, h in links)
        # a div with role=navigation, not <nav>: the site styles (and hides on phones) every <nav> as its header menu
        return (f'<div role="navigation" class="tpf-z tpf-col tpf-h {side}"{i(n)} aria-label="{e(title)}"><h3>{e(title)}{icon("squiggle")}</h3>'
                f'<ul>{lis}</ul><a class="tpf-big" href="{cta[1]}">{e(cta[0])}</a></div>')

    return f'''<footer class="tpf" data-seed="{SEED}" style="--tpf-sheet:{SHEET};--tpf-paper:{PAPER};--tpf-on-sheet:#ffffff;--tpf-on-paper:{PAPER_INK};--tpf-word:{SHEET};--tpf-rim:{rim}">
<svg class="tpf-stage" aria-hidden="true"><defs>
<radialGradient id="tpf-v" cx=".5" cy=".78" r=".75"><stop offset=".45" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#2b0b19" stop-opacity=".07"/></radialGradient>
<linearGradient id="tpf-l" x1="0" y1="0" x2=".35" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".13"/><stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#2b0014" stop-opacity=".14"/></linearGradient>
<pattern id="tpf-g" width="160" height="160" patternUnits="userSpaceOnUse"><image id="tpf-grain-img" width="160" height="160"/></pattern>
<filter id="tpf-d" x="-5%" y="-5%" width="110%" height="120%"><feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#3a0b20" flood-opacity=".3"/></filter>
<filter id="tpf-fs" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="-2" dy="4" stdDeviation="4" flood-color="#3a0b20" flood-opacity=".26"/></filter>
{grads}<path id="tpf-s"/></defs>
<rect class="tpf-paper" width="100%" height="100%"/><rect width="100%" height="100%" fill="url(#tpf-v)" style="mix-blend-mode:multiply"/><rect width="100%" height="100%" fill="url(#tpf-g)" opacity=".32"/>
<g class="tpf-sheet-g" filter="url(#tpf-d)"><path class="tpf-rim"/><use href="#tpf-s" class="tpf-sheet"/></g>
<use href="#tpf-s" fill="url(#tpf-l)"/><use href="#tpf-s" fill="url(#tpf-g)" opacity=".5"/>
<g filter="url(#tpf-fs)">{flaps}</g></svg>

<div class="tpf-z tpf-top">
  <div class="tpf-row tpf-h"{i(0)}>
    <button type="button" class="tpf-ib tpf-up" aria-label="Back to top" title="Back to top">{icon("up")}</button>
    <a class="tpf-ib" href="{O['maps']}" target="_blank" rel="noopener" aria-label="Directions to the ranch" title="Directions">{icon("pin")}</a>
  </div>
  <a class="tpf-logo tpf-h" href="{home}"{i(1)} aria-label="{e(O['name'])}, home"><img src="{rel}assets/logo-white.png" alt="" width="900" height="313" loading="lazy"></a>
  <div class="tpf-h" style="--i:2;position:relative">
    <button type="button" class="tpf-mail" data-copy="{O['phone']}" aria-label="Copy the ranch's number, {O['phone']}" title="Copy number"><span>{O['phone']}</span>{icon("copy")}</button>
    <span class="tpf-toast" role="status" aria-live="polite"></span>
  </div>
</div>

<form class="tpf-z tpf-news tpf-h"{i(3)} novalidate>
  <label for="tpf-email">one email a month about the horses</label>
  <div class="tpf-pill" data-sent="false">
    <input id="tpf-email" type="email" placeholder="your@email" autocomplete="email">
    <span class="tpf-sent" aria-live="polite">{icon("check")} preview: not connected yet</span>
    <button type="submit" class="tpf-knob" aria-label="Sign up">{icon("arrow")}</button>
  </div>
</form>

<span class="tpf-z tpf-flank tpf-h" style="--i:4;left:24%">501(c)(3) · since {O['founded']}</span>
<span class="tpf-z tpf-flank tpf-h" style="--i:4;left:76%" title="Local time in {e(O['city'])}"><span class="tpf-clock" data-zone="America/Chicago">Norman <b class="h">--</b><i aria-hidden="true">:</i><b class="m">--</b></span></span>

<a class="tpf-z tpf-status tpf-h"{i(5)} href="{rel}volunteer/"><i class="tpf-live" aria-hidden="true"></i><span>volunteers welcome</span></a>

{col("l", 6, "the ranch", [("The horses", f"{rel}horses/"), ("Lessons and camps", f"{rel}program/"), ("Updates", f"{rel}updates/")], ("donate.", f"{rel}donate/"))}
{col("r", 7, "pitch in", [("Sponsor a horse", f"{rel}sponsor/"), ("Volunteer", f"{rel}volunteer/"), ("Visit", f"{rel}visit/")], ("call.", tel))}

<button type="button" class="tpf-pin" data-pin="idle" aria-label="Pull the nail: tear a new edge" title="Pull the nail">
  <span class="tpf-shadow" aria-hidden="true"></span>
  <span class="tpf-tilt"><span class="tpf-drop"><span class="tpf-body"><img class="tpf-nail" src="{rel}assets/nail.webp" alt="" width="200" height="600" draggable="false"><i class="tpf-hole" aria-hidden="true"></i></span></span></span>
</button>

<div class="tpf-z tpf-brand tpf-ink">
  <div class="tpf-brand-top tpf-p"{i(0)}>
    <span class="tpf-eye">Butterfly Rescue Ranch</span>
    <a class="tpf-bub" href="{tel}" aria-label="Call the ranch"><span class="tpf-dots" aria-hidden="true"><i></i><i></i><i></i></span><b>call us</b></a>
  </div>
  <a class="tpf-word" href="{home}" aria-label="{e(O['name'])}, home"><span>Butterfly.</span></a>
</div>

<a class="tpf-z tpf-side tpf-ink tpf-p l" style="--i:1;left:29.5%" href="{O['maps']}" target="_blank" rel="noopener"><span>directions</span>{icon("pin")}</a>
<a class="tpf-z tpf-side tpf-ink tpf-p r" style="--i:2;left:71.5%" href="{rel}links/"><span>all links</span>{icon("link")}</a>

<div class="tpf-z tpf-foot tpf-ink">
  <span class="tpf-p"{i(3)}>© 2026 {e(O['name'])}<span class="tpf-sep"> · </span><a class="tpf-by" href="https://station.solutions/" target="_blank" rel="noopener">site by Station</a></span>
  <span class="tpf-credit tpf-p"{i(4)}>{e(O['street'])}, {e(O['city'])}, {O['state']}</span>
  <a class="tpf-handle tpf-p"{i(5)} href="{rel}donate/">give a little →</a>
</div>
</footer>
<script src="{rel}assets/tear.js?v=1" defer></script>'''
