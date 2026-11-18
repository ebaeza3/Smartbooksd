# Smart Book SD – Website

Static website for Smart Book SD (online tax, bookkeeping & payroll).
Plain HTML/CSS/JS with no build step. Open `index.html` in a browser, or host on GitHub Pages, Netlify, etc.

- `index.html` – Home
- `services.html` – Services
- `about.html` – About
- `contact.html` – Book a free consultation (form opens the visitor's email app addressed to Smartbooksd@gmail.com)
- `assets/` – styles, script, favicon

To receive form submissions without email apps, sign up for a form service (e.g. Formspree), set the
form's `action`/`method` in `contact.html`, and remove the `data-mailto` attribute.
