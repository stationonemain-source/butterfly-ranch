/* Forms: the three-step volunteer form, and the donate box's "what this pays for" line. Without script the volunteer
   form is one long form that still submits. Preview site: nothing is sent; the thank-you says so. */
(function () {
  document.querySelectorAll('form[data-steps]').forEach(function (f) {
    var steps = [].slice.call(f.querySelectorAll('.sf-step')), bar = f.querySelector('.sf-bar i'), err = f.querySelector('.sf-err'), at = 0;
    f.classList.add('js');
    function go(n) {
      at = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach(function (s, i) { s.classList.toggle('on', i === at); });
      if (bar) bar.style.width = ((at + 1) / steps.length * 100).toFixed(1) + '%';
      var first = steps[at].querySelector('input:not([type=checkbox]),textarea');
      if (first && at === steps.length - 1) setTimeout(function () { first.focus({ preventScroll: true }); }, 60);
    }
    f.querySelectorAll('.sf-next').forEach(function (b) { b.addEventListener('click', function () { go(at + 1); }); });
    f.querySelectorAll('.sf-back').forEach(function (b) { b.addEventListener('click', function () { go(at - 1); }); });
    f.addEventListener('submit', function (ev) {
      ev.preventDefault(); ev.stopImmediatePropagation();
      var name = f.querySelector('[name=name]'), email = f.querySelector('[name=email]'), bad = null;
      [name, email].forEach(function (x) { x.removeAttribute('aria-invalid'); });
      if (!name.value.trim()) bad = [name, 'Add your name so the ranch knows who to look for.'];
      else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) bad = [email, 'That email doesn’t look right.'];
      if (bad) { bad[0].setAttribute('aria-invalid', 'true'); err.textContent = bad[1]; err.hidden = false; bad[0].focus(); return; }
      err.hidden = true;
      steps.forEach(function (s) { s.classList.remove('on'); s.style.display = 'none'; });
      if (bar) bar.style.width = '100%';
      var done = f.querySelector('.sf-done');
      done.querySelector('[data-first]').textContent = name.value.trim().split(/\s+/)[0];
      done.hidden = false; done.focus({ preventScroll: true });
    }, true);
    go(0);
  });

  // donate: say what the chosen amount covers
  var g = document.getElementById('giver');
  if (g) {
    var line = g.querySelector('.impact');
    var tiers = [].slice.call(g.querySelectorAll('.tiles label')).map(function (l) {
      return { amt: +l.querySelector('input').value, what: l.querySelector('.f').textContent.trim().toLowerCase() };
    }).sort(function (a, b) { return a.amt - b.amt; });
    function say() {
      if (!line) return;
      var other = g.querySelector('input[name=other]'), t = [].filter.call(g.querySelectorAll('input[name=amt]'), function (x) { return x.checked; })[0];
      var a = other && other.value ? +other.value : (t ? +t.value : 0);
      var monthly = (g.querySelector('input[name=freq]:checked') || {}).value === 'monthly';
      var fit = tiers.filter(function (x) { return x.amt <= a; }).pop();
      line.textContent = a && fit ? '$' + a + (monthly ? ' a month' : '') + ' covers ' + fit.what + (monthly ? ', every month.' : '.') : '';
    }
    g.addEventListener('change', say); g.addEventListener('input', say); say();
  }
})();
