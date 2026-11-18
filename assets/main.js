// Mobile nav toggle
const toggle = document.querySelector('.nav-toggle');
const links = document.querySelector('.nav-links');
if (toggle && links) {
  toggle.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
  });
}

// Footer year
document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());

// Preselect service from ?service= on contact page
const params = new URLSearchParams(location.search);
const svc = params.get('service');
const select = document.getElementById('service');
if (svc && select) {
  [...select.options].forEach(o => { if (o.value === svc) o.selected = true; });
}

// Contact form: compose an email to the firm (no backend required).
// To use a form service instead (e.g. Formspree), set the form's action
// attribute and remove data-mailto.
const form = document.getElementById('contact-form');
if (form && form.hasAttribute('data-mailto')) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const d = new FormData(form);
    const subject = `Free consultation request – ${d.get('service') || 'General'}`;
    const body = [
      `Name: ${d.get('name')}`,
      `Email: ${d.get('email')}`,
      `Phone: ${d.get('phone') || '-'}`,
      `Service: ${d.get('service')}`,
      `Preferred contact: ${d.get('contact_pref')}`,
      '',
      d.get('message') || ''
    ].join('\n');
    location.href = `mailto:Smartbooksd@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    const status = document.getElementById('form-status');
    if (status) status.textContent = 'Opening your email app… If nothing happens, email us at Smartbooksd@gmail.com.';
  });
}
