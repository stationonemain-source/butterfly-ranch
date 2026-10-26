/* Donations through Station Give (our own system; Stripe moves the money, into the ranch's own account).
   Donate page: amount + once/monthly -> Stripe's secure form opens right here in the page.
   Sponsor page: [data-sponsor] buttons start a monthly sponsorship for one horse.
   Thanks page: confirms the gift from the Checkout Session.
   Until checkout is switched on, the service answers 503 {preview:true} and the page says so honestly. */
(function () {
  var API = (document.querySelector('meta[name=give-api]') || {}).content;
  if (!API) return;
  var stripeP = null, checkout = null;

  function loadStripe(pk, account) {
    if (stripeP) return stripeP;
    stripeP = new Promise(function (ok, no) {
      var s = document.createElement('script');
      s.src = 'https://js.stripe.com/v3/'; s.onload = function () { ok(Stripe(pk, account ? { stripeAccount: account } : undefined)); };
      s.onerror = function () { stripeP = null; no(new Error('Stripe did not load')); };
      document.head.appendChild(s);
    });
    return stripeP;
  }

  function post(path, body) {
    return fetch(API + path, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (j) { j._status = r.status; return j; }); });
  }

  // one sheet for the payment form: inline on wide screens, full-height on phones
  function sheet() {
    var d = document.getElementById('give-sheet');
    if (d) return d;
    d = document.createElement('div');
    d.id = 'give-sheet'; d.className = 'give-sheet'; d.hidden = true;
    d.setAttribute('role', 'dialog'); d.setAttribute('aria-modal', 'true'); d.setAttribute('aria-label', 'Secure checkout');
    d.innerHTML = '<div class="gs-card"><div class="gs-top"><b>Secure checkout</b><span class="gs-test" hidden>Test mode: use card 4242 4242 4242 4242, any future date, any CVC. No money moves.</span>' +
      '<button type="button" class="gs-x" aria-label="Close checkout">×</button></div><div id="give-mount"></div></div>';
    document.body.appendChild(d);
    d.querySelector('.gs-x').addEventListener('click', close);
    d.addEventListener('click', function (e) { if (e.target === d) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !d.hidden) close(); });
    return d;
  }
  var opener = null;
  function close() {
    var d = document.getElementById('give-sheet');
    if (checkout) { try { checkout.destroy(); } catch (e) {} checkout = null; }
    if (d) d.hidden = true;
    document.documentElement.classList.remove('gs-open');
    if (opener) opener.focus();
  }

  function start(body, say, btn) {
    opener = btn;
    var was = btn.textContent; btn.disabled = true; btn.textContent = 'Opening secure checkout…';
    post('/checkout', body).then(function (j) {
      if (j._status === 503 && j.preview) {
        say('Preview: checkout switches on when the ranch connects its own Stripe account. Nothing was charged.');
        return;
      }
      if (!j.client_secret) { say(j.error || 'Checkout could not start. Please try again.'); return; }
      return loadStripe(j.publishable_key, j.stripe_account).then(function (stripe) {
        var d = sheet();
        d.querySelector('.gs-test').hidden = !j.test;
        d.hidden = false; document.documentElement.classList.add('gs-open');
        var make = stripe.createEmbeddedCheckoutPage || stripe.initEmbeddedCheckout;
        return make.call(stripe, { fetchClientSecret: function () { return Promise.resolve(j.client_secret); } }).then(function (c) {
          checkout = c; c.mount('#give-mount'); d.querySelector('.gs-x').focus();
        });
      });
    }).catch(function () { say('Checkout could not start. Please try again in a minute, or call the ranch.'); })
      .then(function () { btn.disabled = false; btn.textContent = was; });
  }

  // donate page
  var g = document.getElementById('giver');
  if (g) {
    g.addEventListener('submit', function (ev) {
      ev.preventDefault(); ev.stopImmediatePropagation();
      var other = g.querySelector('input[name=other]'), t = [].filter.call(g.querySelectorAll('input[name=amt]'), function (x) { return x.checked; })[0];
      var a = other.value ? Number(other.value) : (t ? Number(t.value) : 0), out = g.querySelector('.sent');
      if (!a) { other.focus(); return; }
      var monthly = g.querySelector('input[name=freq]:checked').value === 'monthly';
      out.classList.remove('on');
      start({ amount: a, freq: monthly ? 'monthly' : 'once', horse: g.dataset.horse || '' },
        function (m) { out.textContent = m; out.classList.add('on'); }, g.querySelector('button[type=submit]'));
    }, true);
  }

  var want = new URLSearchParams(location.search).get('horse') || '';

  // a gift for one horse (?horse=<slug> from a horse page)
  if (g && want) {
    var names = JSON.parse(g.dataset.horses || '{}'), fh = g.querySelector('.for-horse');
    if (names[want]) { g.dataset.horse = want; fh.textContent = 'Your gift goes to the care of ' + names[want] + '.'; fh.hidden = false; }
  }

  // sponsor form: one horse, a monthly amount, name on the page if they like
  var sf = document.querySelector('form[data-sponsor-form]');
  if (sf) {
    var sel = sf.querySelector('select[name=horse]');
    if (want && sel.querySelector('option[value="' + want.replace(/[^a-z0-9-]/g, '') + '"]')) sel.value = want;
    sf.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var amt = sf.querySelector('input[name=amount]'), out = sf.querySelector('.sent'), a = Number(amt.value);
      out.classList.remove('on');
      if (!a || a < 5) { amt.setAttribute('aria-invalid', 'true'); out.textContent = 'Choose a monthly amount of $5 or more.'; out.classList.add('on'); amt.focus(); return; }
      amt.removeAttribute('aria-invalid');
      start({ amount: a, sponsor: true, horse: sel.value, name_on_page: sf.querySelector('[name=name_on_page]').checked },
        function (m) { out.textContent = m; out.classList.add('on'); }, sf.querySelector('button[type=submit]'));
    });
  }

  // the torn-poster footer's sign-up
  var tn = document.querySelector('.tpf-news');
  if (tn) tn.addEventListener('submit', function (ev) {
    var input = tn.querySelector('input'), v = (input.value || '').trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return;           // tear.js shows "check that email"
    var sent = tn.querySelector('.tpf-sent');
    post('/subscribe', { email: v }).then(function (j) {
      if (sent) sent.lastChild.textContent = j.result ? " you're on the list" : ' please try again';
    }).catch(function () { if (sent) sent.lastChild.textContent = ' please try again'; });
  });

  // monthly-update sign-up forms: data-signup
  document.querySelectorAll('form[data-signup]').forEach(function (f) {
    f.addEventListener('submit', function (ev) {
      ev.preventDefault(); ev.stopImmediatePropagation();
      var email = f.querySelector('[type=email]'), out = f.querySelector('.sent,[role=status]');
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test((email.value || '').trim())) { email.setAttribute('aria-invalid', 'true'); email.focus(); return; }
      email.removeAttribute('aria-invalid');
      post('/subscribe', { email: email.value.trim(), name: ((f.querySelector('[name=name]') || {}).value || '') }).then(function (j) {
        if (out) { out.textContent = j.result ? "You're on the list." : (j.error || 'Please try again.'); out.classList.add('on'); }
        if (j.result) f.reset();
      }).catch(function () { if (out) { out.textContent = 'Please try again in a minute.'; out.classList.add('on'); } });
    }, true);
  });

  // thanks page
  var th = document.getElementById('give-thanks');
  if (th) {
    var sid = new URLSearchParams(location.search).get('session_id');
    if (!sid) { th.querySelector('.gt-msg').textContent = 'No gift to show here. If you just gave, your receipt will arrive by email.'; }
    else fetch(API + '/session/' + encodeURIComponent(sid)).then(function (r) { return r.json(); }).then(function (j) {
      var m = th.querySelector('.gt-msg');
      if (j.error) { m.textContent = 'We couldn’t find that checkout. If you just gave, your receipt will arrive by email.'; return; }
      if (j.status === 'complete') {
        th.querySelector('.gt-ok').hidden = false;
        m.textContent = (j.payment_status === 'unpaid' ? 'Your bank payment of ' + j.amount + ' is on its way. ' : 'Your gift of ' + j.amount +
          (j.kind === 'monthly' ? ' a month' : '') + ' came through. ') + 'Your receipt is going to ' + (j.email || 'your email') + '.' +
          (j.test ? ' (Test gift: no money moved.)' : '');
      } else m.textContent = 'This checkout was not finished, so nothing was charged.';
    }).catch(function () { th.querySelector('.gt-msg').textContent = 'We couldn’t check your gift just now. If it went through, your receipt will arrive by email.'; });
  }

  // this month's progress, only when the ranch has published its costs (goal) and there is something to show
  document.querySelectorAll('[data-give-progress]').forEach(function (el) {
    fetch(API + '/progress').then(function (r) { return r.json(); }).then(function (p) {
      if (!p.goal_cents) return;
      el.querySelector('i').style.width = p.percent + '%';
      el.querySelector('span').textContent = p.month + ': ' + p.percent + '% of the horses’ costs covered' + (p.test ? ' (test gifts)' : '');
      el.hidden = false;
    }).catch(function () {});
  });
})();
