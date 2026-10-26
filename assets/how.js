/* "How it works" switch (2026-10-25). A showcase for Braxton and the OU class: with the switch on, every feature a
   Station product runs gets a thin magenta outline and a small note naming the product and what it does ON THE LIVE
   SITE. Nothing on this preview is connected; the notes never say otherwise. Copy lives in _src/data.json ("how");
   build.py writes it into assets/how.js in place of the HOW_DATA marker. Off by default; the choice is a view
   preference, so it may sit in localStorage. */
(function () {
  var DATA = {"legend": "Each outlined part of this page is run by a Station product, named in the note beside it. This site is a preview. Email sign-ups already go to the ranch’s own list; donations, the chat and texts switch on when the site goes live. The notes say what happens then.", "notes": {"herd": [["Custom website", "Every horse gets its own page, following it from the day it arrived to the day it is well."], ["Marquee", "The same story goes out as the ranch’s two-a-week horse series on Instagram and Facebook, scheduled from one calendar."]], "journal": [["Custom website", "Each step of the horse’s recovery, and what it cost, is added to this page as it happens."], ["Marquee", "The same updates go out as the two-a-week horse series on Instagram and Facebook, scheduled from one calendar."], ["Dispatch", "The monthly email tells donors which horses moved forward and what their gifts paid for."]], "news": [["Marquee", "Each post here also goes out on Instagram and Facebook, scheduled from one calendar."], ["Dispatch", "Once a month the news goes to everyone on the ranch’s email list."]], "join": [["Dispatch", "The address joins the ranch’s own email list. Once a month, everyone on it hears how the horses are doing."]], "giver": [["Tap", "Secure checkout on the ranch’s own Stripe account: card, Apple Pay, Google Pay or bank. The money goes straight to the ranch, and a tax receipt arrives by email at once."], ["Tap · monthly gifts", "Monthly donors update their card or stop their gift from the link in their receipt. A card that fails is retried automatically."]], "promise": [["Pursuit", "Every donor gets a thank-you from Braxton within the hour. A gift of $250 or more also alerts Braxton to call the donor personally."], ["Dispatch", "Donors get the horse updates, a summary of their giving each January, and the Giving Tuesday appeal."], ["Revive", "A donor who has not given for 12 months gets a short note from the ranch inviting them back."]], "levels": [["Tap", "A sponsorship is a monthly gift through secure checkout on the ranch’s own Stripe account, with a tax receipt by email. Sponsors update their card or stop it from their receipt link, and a failed card is retried automatically."], ["Pursuit", "Each new sponsor gets a thank-you from Braxton within the hour."], ["Dispatch", "The monthly note on the horse, the January giving summary and Giving Tuesday all go out by email."]], "logos": [["Radar", "Radar finds local businesses that fit, like feed and tack stores, vet clinics and riding programs, and lines them up in the ranch’s sponsor pipeline for the ask."], ["Tap", "A business sponsors through the same secure monthly checkout, with a receipt for every payment."]], "volunteer": [["Pursuit", "Every sign-up gets a welcome by text and email the same day, and follow-ups until the volunteer replies."], ["Slate", "The welcome links to the ranch’s booking page, where a new volunteer picks a first barn day and gets a reminder before it."]], "flyer": [["Slate", "Families pick a lesson, camp or pony party and book it themselves, and reminders by text and email make sure they turn up."]], "where": [["Echo", "The ranch’s Google listing is kept to one name, one address and one set of hours, with the donate and volunteer links and a horse update each week."], ["Repute", "After a visit or a volunteer day, everyone who came is asked for a Google review, not only the happy ones. Braxton approves a drafted reply to each review."]], "call": [["Lineback", "When nobody can get to the phone, a missed call gets a text back within seconds."], ["Frontdesk", "An AI receptionist answers the ranch’s number, takes a message on surrender and welfare calls, and passes urgent ones straight to Braxton."]], "facts": [["Custom website", "Built by Station on the ranch’s own photos and words, and the ranch’s to keep."], ["Echo", "The same name, address and phone are kept on the ranch’s Google listing, so the two never disagree."]], "links": [["Custom website", "Every social bio points here instead of Linktree, so a follower is one tap from Donate."], ["Dispatch", "“Get the monthly update” turns a follower into someone on the ranch’s own email list."]], "greet": [["Greet", "An AI assistant answers from the ranch’s own facts at any hour, and takes the visitor’s details so the ranch can follow up."]], "footer": [["Dispatch", "The sign-up on the magenta sheet below joins the same monthly email list."], ["Lineback, Frontdesk", "The ranch’s number gets missed-call text-back and the AI receptionist."], ["Tap", "“donate.” goes to the same secure checkout on the ranch’s own Stripe account."]]}, "spots": [{"sel": ".ask-btn", "note": "greet", "at": "fly"}, {"sel": "footer.tpf", "note": "footer", "at": "before", "mark": ".tpf-news .tpf-pill, .tpf-mail, .tpf-big"}]};
  var btn = document.querySelector('.how-btn'), root = document.documentElement, KEY = 'br-how', built = false;
  if (!btn || !DATA) return;
  btn.hidden = false;

  function el(tag, cls, text) { var d = document.createElement(tag); if (cls) d.className = cls; if (text != null) d.textContent = text; return d; }
  function note(key, extra) {
    var rows = DATA.notes[key]; if (!rows) return null;
    var n = el('div', 'how-note' + (extra ? ' ' + extra : ''));
    n.setAttribute('role', 'note');
    n.setAttribute('aria-label', 'How it works: ' + rows.map(function (r) { return r[0]; }).join(', '));
    n.appendChild(el('p', 'how-eye', 'On the live site:'));
    var list = el('div', 'how-rows');
    rows.forEach(function (r) { var row = el('div', 'how-row'); row.appendChild(el('b', 'how-p', r[0])); row.appendChild(el('p', null, r[1])); list.appendChild(row); });
    n.appendChild(list);
    return n;
  }
  function place(target, n, at) {
    if (at === 'before') target.parentNode.insertBefore(n, target);
    else if (at === 'start') target.insertBefore(n, target.firstChild);
    else if (at === 'end') target.appendChild(n);
    else target.parentNode.insertBefore(n, target.nextSibling);   // 'after'
  }
  function build() {
    built = true;
    // the legend: under the film on home, at the top of the page everywhere else
    var lg = el('div', 'how-legend'), w = el('div', 'wrap');
    w.appendChild(el('b', 'how-p', 'How it works')); w.appendChild(el('p', null, DATA.legend)); lg.appendChild(w);
    var film = document.querySelector('.home .film'), main = document.getElementById('main');
    if (film) film.parentNode.insertBefore(lg, film.nextSibling); else if (main) main.insertBefore(lg, main.firstChild);

    document.querySelectorAll('[data-how]').forEach(function (f) {
      var n = note(f.getAttribute('data-how')); if (n) place(f, n, f.getAttribute('data-how-at') || 'after');
    });
    (DATA.spots || []).forEach(function (s) {
      var t = document.querySelector(s.sel); if (!t) return;
      var n = note(s.note); if (!n) return;
      t.setAttribute('data-how-mark', '');
      if (s.mark) t.querySelectorAll(s.mark).forEach(function (m) { m.setAttribute('data-how-mark', ''); });
      if (s.at === 'fly') {
        // the chat bubble is fixed to the corner, so its note can't sit in the page without covering it. A small tab
        // floats above the bubble (and hides with it); the note opens from the tab, so nothing is covered by default.
        var fly = el('div', 'how-fly'), id = 'how-' + s.note;
        var tab = el('button', 'how-tab', DATA.notes[s.note].map(function (r) { return r[0]; }).join(', ') + ' · how the chat works');
        tab.type = 'button'; tab.setAttribute('aria-expanded', 'false'); tab.setAttribute('aria-controls', id);
        var x = el('button', 'how-x', '×'); x.type = 'button'; x.setAttribute('aria-label', 'Close this note');
        n.id = id; n.hidden = true; n.insertBefore(x, n.firstChild);
        function show(o) { n.hidden = !o; tab.hidden = o; tab.setAttribute('aria-expanded', o ? 'true' : 'false'); (o ? x : tab).focus({ preventScroll: true }); }
        tab.addEventListener('click', function () { show(true); });
        x.addEventListener('click', function () { show(false); });
        fly.appendChild(tab); fly.appendChild(n);
        t.parentNode.insertBefore(fly, t.nextSibling);
      } else if (s.at === 'before') {
        var wrap = el('div', 'wrap how-out'); wrap.appendChild(n); t.parentNode.insertBefore(wrap, t);
      } else place(t, n, s.at);
    });
  }
  function set(on, save) {
    if (on && !built) build();
    root.classList.toggle('how-on', on);
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    if (save) { try { localStorage.setItem(KEY, on ? '1' : '0'); } catch (e) {} }
  }
  btn.addEventListener('click', function () { set(!root.classList.contains('how-on'), true); });
  var saved = false;
  try { saved = localStorage.getItem(KEY) === '1'; } catch (e) {}
  set(saved, false);
})();
