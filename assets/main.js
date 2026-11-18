/* Smart Book SD — site script (no tracking, no cookies) */
(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var CFG = window.SBSD || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  /* ---- Header / nav ---- */
  var header = $('.site-header');
  var toggle = $('.nav-toggle');
  var menu = $('.nav-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) { toggle.click(); toggle.focus(); }
    });
  }
  var mobileCta = $('.mobile-cta');
  var toTop = $('.to-top');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 8);
    if (mobileCta) mobileCta.classList.toggle('show', y > 420);
    if (toTop) toTop.classList.toggle('show', y > 900);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener('click', function () { window.scrollTo({ top: 0 }); $('#main').focus({ preventScroll: true }); });

  /* ---- Year ---- */
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---- Reveal on scroll ---- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    $$('.reveal').forEach(function (el) { io.observe(el); });
  } else { $$('.reveal').forEach(function (el) { el.classList.add('in'); }); }

  /* ---- Service finder (home) ---- */
  var finder = $('#finder');
  if (finder) {
    var out = $('#finder-out');
    var services = CFG.services || {};
    var render = function () {
      var picks = {};
      $$('input:checked', finder).forEach(function (i) {
        (i.getAttribute('data-svc') || '').split(' ').forEach(function (s) { if (s) picks[s] = true; });
      });
      var keys = Object.keys(picks);
      var list = $('ul', out), btn = $('.btn', out), empty = $('.finder-empty', out);
      list.innerHTML = '';
      if (!keys.length) { empty.hidden = false; list.hidden = true; btn.setAttribute('href', 'contact.html'); return; }
      empty.hidden = true; list.hidden = false;
      keys.forEach(function (k) {
        var s = services[k]; if (!s) return;
        var li = document.createElement('li');
        li.innerHTML = '<span class="ico">' + s.icon + '</span><div><strong><a href="' + s.url + '"></a></strong><small></small></div>';
        $('a', li).textContent = s.name; $('small', li).textContent = s.short;
        list.appendChild(li);
      });
      btn.setAttribute('href', 'contact.html?service=' + encodeURIComponent(keys.join(',')));
    };
    finder.addEventListener('change', render);
    render();
  }

  /* ---- Contact form ---- */
  var form = $('#contact-form');
  if (form) {
    var params = new URLSearchParams(location.search);
    var pre = (params.get('service') || '').split(',');
    $$('input[name="services"]', form).forEach(function (cb) { if (pre.indexOf(cb.value) > -1) cb.checked = true; });

    var status = $('#form-status');
    var showStatus = function (ok, msg) { status.className = 'form-status ' + (ok ? 'ok' : 'bad'); status.textContent = msg; status.focus(); };
    var validate = function () {
      var firstBad = null;
      $$('.field', form).forEach(function (f) {
        var input = $('input,select,textarea', f); if (!input || input.type === 'checkbox') return;
        var bad = !input.checkValidity();
        f.classList.toggle('invalid', bad); input.setAttribute('aria-invalid', String(bad));
        if (bad && !firstBad) firstBad = input;
      });
      var svcBox = $('#svc-field');
      var anySvc = $$('input[name="services"]:checked', form).length > 0;
      if (svcBox) { svcBox.classList.toggle('invalid', !anySvc); if (!anySvc && !firstBad) firstBad = $('input', svcBox); }
      var consent = $('#consent');
      if (consent && !consent.checked && !firstBad) { firstBad = consent; consent.closest('.consent').classList.add('invalid'); }
      if (firstBad) firstBad.focus();
      return !firstBad;
    };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate()) { showStatus(false, 'Please complete the highlighted fields.'); return; }
      if ($('[name="_honey"]', form).value) return; // bot
      var data = {};
      new FormData(form).forEach(function (v, k) {
        if (k === 'services') data[k] = (data[k] ? data[k] + ', ' : '') + v; else data[k] = v;
      });
      var btn = $('button[type="submit"]', form), label = btn.textContent;
      btn.disabled = true; btn.textContent = 'Sending…';
      var mailtoFallback = function () {
        var body = Object.keys(data).filter(function (k) { return k.charAt(0) !== '_'; })
          .map(function (k) { return k + ': ' + data[k]; }).join('\n');
        location.href = 'mailto:' + CFG.email + '?subject=' + encodeURIComponent(data._subject || 'Consultation request') + '&body=' + encodeURIComponent(body);
      };
      if (!CFG.formEndpoint) { mailtoFallback(); btn.disabled = false; btn.textContent = label; showStatus(true, 'Opening your email app to send your request…'); return; }
      fetch(CFG.formEndpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(data)
      }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (!res.ok || String(res.j.success) === 'false') throw new Error('fail');
          form.reset();
          showStatus(true, 'Thank you! Your request was sent. We’ll be in touch' + (CFG.responseTime ? ' within ' + CFG.responseTime : ' soon') + ' to schedule your free consultation.');
        })
        .catch(function () {
          showStatus(false, 'Sorry, something went wrong sending the form. Please call or text ' + CFG.phone + ' or email ' + CFG.email + '.');
        })
        .then(function () { btn.disabled = false; btn.textContent = label; });
    });
    form.addEventListener('input', function (e) {
      var f = e.target.closest('.field, .consent'); if (f && f.classList.contains('invalid')) { f.classList.remove('invalid'); e.target.setAttribute('aria-invalid', 'false'); }
    });
  }

  /* ---- Document checklist ---- */
  var cl = $('#checklist');
  if (cl) {
    var KEY = 'sbsd-checklist-v1';
    var saved = {}; try { saved = JSON.parse(store.get(KEY) || '{}'); } catch (e) {}
    var boxes = $$('input[type="checkbox"]', cl);
    var update = function () {
      var done = boxes.filter(function (b) { return b.checked; }).length;
      $('#cl-count').textContent = done + ' of ' + boxes.length + ' gathered';
      $('#cl-bar').style.width = (boxes.length ? done / boxes.length * 100 : 0) + '%';
    };
    boxes.forEach(function (b) {
      if (saved[b.id]) b.checked = true;
      b.addEventListener('change', function () { saved[b.id] = b.checked; store.set(KEY, JSON.stringify(saved)); update(); });
    });
    $('#cl-print').addEventListener('click', function () { window.print(); });
    $('#cl-reset').addEventListener('click', function () { boxes.forEach(function (b) { b.checked = false; }); saved = {}; store.set(KEY, '{}'); update(); });
    update();
  }

  /* ---- Deadline filter + past marking ---- */
  var dl = $('#deadlines');
  if (dl) {
    var today = new Date(); today.setHours(0, 0, 0, 0);
    $$('.deadline', dl).forEach(function (d) {
      var dt = new Date(d.getAttribute('data-date') + 'T23:59:59');
      if (dt < today) { d.classList.add('past'); d.setAttribute('aria-label', 'Past deadline'); }
    });
    var fb = $('#deadline-filter');
    if (fb) fb.addEventListener('change', function () {
      var v = $('input:checked', fb).value;
      $$('.deadline', dl).forEach(function (d) { d.hidden = v !== 'all' && (d.getAttribute('data-who') || '').indexOf(v) === -1; });
    });
  }
})();
