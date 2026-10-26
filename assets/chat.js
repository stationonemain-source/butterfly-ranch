/* "Ask the ranch" widget — PREVIEW, not yet connected to an AI (Circle 2026-10-25: "add it, but don't integrate it
   fully"). It answers the common questions from facts already published on this site, and says plainly that the full
   AI assistant switches on later. Nothing typed here leaves the visitor's browser. On the home page the bubble appears
   once the visitor scrolls past the film, so it never covers the hero's buttons. */
(function () {
  var root = document.documentElement, rel = (document.querySelector('link[rel=stylesheet][href*="assets/site.css"]') || {}).getAttribute
    ? document.querySelector('link[href*="assets/site.css"]').getAttribute('href').split('assets/')[0] : '';
  var PHONE = '(405) 922-0839', TEL = 'tel:+14059220839', CAMP = '(307) 250-7508', SMS = 'sms:+13072507508';
  var A = {
    donate: { q: 'How can I donate?', a: ['Every gift goes to hay, feed, farrier and vet care. You can give once or every month on the <a href="' + rel + 'donate/">Donate page</a>: pick an amount, then pay.',
      'Butterfly Rescue Ranch is a 501(c)(3), so gifts are tax-deductible as allowed by law. You can also mail a cheque to 7475 By Drive, Norman, OK 73072.'] },
    volunteer: { q: 'Can I volunteer?', a: ['Yes, and no horse experience is needed. Feeding, grooming, barn days and events all need willing hands.',
      'Tell the ranch what you’d like to do and when you’re free on the <a href="' + rel + 'volunteer/">Volunteer page</a>. It takes under a minute.'] },
    program: { q: 'Lessons and camps', a: ['Lessons: a half-hour ground lesson is $25, a one-hour horseback lesson $50. Camps run $250 to $600, and pony parties start at $300.',
      'To book, text Anna at <a href="' + SMS + '">' + CAMP + '</a>. All the details are on the <a href="' + rel + 'program/">Program page</a>.'] },
    visit: { q: 'Can I come visit?', a: ['The ranch is at 7475 By Drive, Norman, OK 73072. It’s a working barn, so please call before you come out: <a href="' + TEL + '">' + PHONE + '</a>.'] },
    sponsor: { q: 'Sponsor a horse', a: ['You can sponsor one horse by the month and get its updates. Businesses can sponsor too and have their logo on the horse’s page.',
      'See how it works on the <a href="' + rel + 'sponsor/">Sponsor page</a>.'] },
    horses: { q: 'Meet the horses', a: ['Each horse at the ranch has its own page with photos and how it’s doing. Start on <a href="' + rel + 'horses/">The horses</a>.'] }
  };
  var WORDS = [['donate', /donat|give|gift|money|tax|cheque|check|venmo|paypal|pay\b/], ['volunteer', /volunt|help out|muck|groom/],
               ['program', /lesson|camp|ride|riding|party|parties|pony|book|price|cost of|how much/], ['visit', /visit|address|where|direction|come out|location|hours|open/],
               ['sponsor', /sponsor|adopt|business|logo/], ['horses', /meet the|the herd|which horses|horses (here|at the ranch|do you have)|names? of/]];   // not bare "horse": "do you board horses?" must fall back
  var FALLBACK = ['This is a preview of the ranch’s assistant, so it can only answer the common questions for now. The full AI assistant switches on when the site goes live.',
                  'For anything else, call Braxton at <a href="' + TEL + '">' + PHONE + '</a>.'];

  var css = document.createElement('style');
  css.textContent = '' +
    '.ask-btn{position:fixed;right:18px;bottom:18px;z-index:60;display:flex;align-items:center;gap:10px;border:0;border-radius:999px;padding:12px 18px 12px 12px;background:var(--mag,#a71c5a);color:#fff;font:600 15.5px var(--fb,Georgia,serif);box-shadow:0 14px 30px -10px rgba(120,10,60,.55);cursor:pointer;transition:transform .35s cubic-bezier(.2,.7,.2,1),opacity .35s}' +
    '.ask-btn:hover{transform:translateY(-2px)}.ask-btn.off{opacity:0;transform:translateY(20px);pointer-events:none}' +
    '.ask-btn .av{width:32px;height:32px;border-radius:50%;background:#fff center/76% no-repeat;flex:none}' +
    '.ask{padding:0;margin:0;position:fixed;right:18px;bottom:18px;z-index:61;width:min(380px,calc(100vw - 24px));height:min(560px,calc(100svh - 36px));display:flex;flex-direction:column;background:var(--paper,#fbf8f6);border-radius:20px;overflow:hidden;box-shadow:0 30px 70px -20px rgba(43,32,38,.45),0 0 0 1px rgba(43,32,38,.06);transform-origin:100% 100%;animation:ask-in .35s cubic-bezier(.2,.7,.2,1)}' +
    '.ask[hidden]{display:none}@keyframes ask-in{from{opacity:0;transform:scale(.92) translateY(12px)}to{opacity:1;transform:none}}' +
    '.ask-h{flex:none;display:flex;align-items:center;gap:12px;padding:16px 16px 14px;background:var(--mag,#a71c5a);color:#fff}' +
    '.ask-h .av{width:40px;height:40px;border-radius:50%;background:#fff center/76% no-repeat;flex:none}' +
    '.ask-h b{display:block;font:400 19px var(--fd,Georgia,serif)}.ask-h small{display:block;font-size:12.5px;opacity:.85}' +
    '.ask-x{margin-left:auto;background:rgba(255,255,255,.16);border:0;color:#fff;width:34px;height:34px;border-radius:50%;font-size:20px;line-height:1;cursor:pointer}' +
    '.ask-b{flex:1 1 auto;min-height:0;overflow-y:auto;overscroll-behavior:contain;padding:16px 14px 8px;display:flex;flex-direction:column;gap:8px}' +
    '.ask-m{max-width:86%;padding:11px 14px;border-radius:16px;font-size:15.5px;line-height:1.45;animation:ask-m .3s ease both}' +
    '@keyframes ask-m{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}' +
    '.ask-m.bot{align-self:flex-start;background:#fff;color:var(--ink,#2b2026);border:1px solid var(--rule,#e7dde1);border-bottom-left-radius:6px}' +
    '.ask-m.me{align-self:flex-end;background:var(--mag,#a71c5a);color:#fff;border-bottom-right-radius:6px}' +
    '.ask-m a{color:var(--mag,#a71c5a);font-weight:600}.ask-m.me a{color:#fff}' +
    '.ask-dots{align-self:flex-start;display:flex;gap:4px;padding:14px;background:#fff;border:1px solid var(--rule,#e7dde1);border-radius:16px;border-bottom-left-radius:6px}' +
    '.ask-dots i{width:7px;height:7px;border-radius:50%;background:#c9a9b8;animation:ask-d 1.1s infinite}.ask-dots i:nth-child(2){animation-delay:.15s}.ask-dots i:nth-child(3){animation-delay:.3s}' +
    '@keyframes ask-d{0%,60%,100%{transform:none;opacity:.5}30%{transform:translateY(-3px);opacity:1}}' +
    '.ask-chips{flex:none;display:flex;gap:6px;padding:6px 14px 10px;overflow-x:auto;scrollbar-width:none}.ask-chips::-webkit-scrollbar{display:none}.ask-chips button{flex:none}' +
    '.ask-chips button{border:1.5px solid #e2c6d3;background:#fff;color:var(--mag-d,#86164a);border-radius:999px;padding:8px 13px;font:600 14px var(--fb,Georgia,serif);cursor:pointer}' +
    '.ask-chips button:hover{border-color:var(--mag,#a71c5a)}' +
    '.ask-f{flex:none;display:flex;gap:8px;padding:10px 12px 12px;border-top:1px solid var(--rule,#e7dde1);background:#fff}' +
    '.ask-f input{flex:1;min-width:0;border:1.5px solid #e2d6dc;border-radius:12px;padding:11px 13px;font:400 16px var(--fb,Georgia,serif);color:var(--ink,#2b2026)}' +
    '.ask-f input:focus{outline:none;border-color:var(--mag,#a71c5a)}' +
    '.ask-f button{border:0;border-radius:12px;background:var(--mag,#a71c5a);color:#fff;width:46px;font-size:18px;cursor:pointer}' +
    '.ask-note{margin:0;padding:0 14px 10px;font-size:12px;color:var(--mute,#8a7f85);background:#fff}' +
    '@media (max-width:600px){.ask{right:0;bottom:0;width:100vw;height:min(88svh,640px);border-radius:20px 20px 0 0}.ask-btn{right:14px;bottom:14px}}' +
    '@media (prefers-reduced-motion:reduce){.ask,.ask-m,.ask-btn{animation:none;transition:none}}';
  document.head.appendChild(css);

  var logo = 'url(' + rel + 'assets/logo.png)';
  var btn = document.createElement('button');
  btn.className = 'ask-btn'; btn.type = 'button'; btn.setAttribute('aria-haspopup', 'dialog');
  btn.innerHTML = '<span class="av" style="background-image:' + logo + '"></span>Ask the ranch';
  var box = document.createElement('div');   // not <section>: the site pads every section 72px
  box.className = 'ask'; box.hidden = true; box.setAttribute('role', 'dialog'); box.setAttribute('aria-label', 'Ask the ranch');
  box.innerHTML = '<div class="ask-h"><span class="av" style="background-image:' + logo + '"></span><div><b>Ask the ranch</b><small>Butterfly Rescue Ranch · preview</small></div><button class="ask-x" type="button" aria-label="Close">×</button></div>' +
    '<div class="ask-b" aria-live="polite"></div><div class="ask-chips"></div>' +
    '<form class="ask-f"><input type="text" name="q" placeholder="Ask a question…" autocomplete="off" aria-label="Your question"><button type="submit" aria-label="Send">↑</button></form>' +
    '<p class="ask-note">Preview: answers come from this site. The full AI assistant switches on at launch. Nothing you type is sent anywhere.</p>';
  document.body.appendChild(btn); document.body.appendChild(box);
  var body = box.querySelector('.ask-b'), chips = box.querySelector('.ask-chips'), input = box.querySelector('input'), started = false;

  function msg(html, who) { var d = document.createElement('div'); d.className = 'ask-m ' + who; d.innerHTML = html; body.appendChild(d); body.scrollTop = body.scrollHeight; return d; }
  function say(lines) {
    var i = 0;
    (function next() {
      if (i >= lines.length) { showChips(); return; }
      var t = document.createElement('div'); t.className = 'ask-dots'; t.innerHTML = '<i></i><i></i><i></i>'; body.appendChild(t); body.scrollTop = body.scrollHeight;
      setTimeout(function () { t.remove(); msg(lines[i++], 'bot'); setTimeout(next, 250); }, 500 + Math.min(900, lines[i].length * 6));
    })();
  }
  function showChips(skip) {
    chips.innerHTML = '';
    Object.keys(A).forEach(function (k) {
      if (k === skip) return;
      var b = document.createElement('button'); b.type = 'button'; b.textContent = A[k].q;
      b.addEventListener('click', function () { ask(A[k].q, k); }); chips.appendChild(b);
    });
    body.scrollTop = body.scrollHeight;   // the chips take room: keep the newest answer in view
  }
  function ask(text, key) {
    chips.innerHTML = '';
    msg(text.replace(/[<>&]/g, function (c) { return { '<': '&lt;', '>': '&gt;', '&': '&amp;' }[c]; }), 'me');
    if (!key) { var low = text.toLowerCase(); for (var i = 0; i < WORDS.length; i++) if (WORDS[i][1].test(low)) { key = WORDS[i][0]; break; } }
    say(key ? A[key].a : FALLBACK);
  }
  function open() {
    box.hidden = false; btn.classList.add('off');
    if (!started) { started = true; say(['Hi! I’m the ranch’s helper. What would you like to know?']); }
    setTimeout(function () { input.focus({ preventScroll: true }); }, 350);
  }
  function close() { box.hidden = true; btn.classList.remove('off'); btn.focus({ preventScroll: true }); }
  btn.addEventListener('click', open);
  box.querySelector('.ask-x').addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !box.hidden) close(); });
  box.querySelector('form').addEventListener('submit', function (e) { e.preventDefault(); var q = input.value.trim(); if (!q) return; input.value = ''; ask(q); });

  // gallery: step aside while the photo rope is on screen (its arrows sit where the bubble does)
  var rope = document.querySelector('[data-rope]');
  if (rope && window.IntersectionObserver) new IntersectionObserver(function (en) { if (box.hidden) btn.classList.toggle('off', en[0].isIntersecting); }, { threshold: 0.35 }).observe(rope);
  // home: wait until the visitor is past the film, so the bubble never sits on the hero's buttons
  var film = document.querySelector('.home .film');
  if (film) {
    var upd = function () { if (box.hidden) btn.classList.toggle('off', window.scrollY < film.offsetHeight * 0.6); };
    addEventListener('scroll', upd, { passive: true }); upd();
  }
})();
