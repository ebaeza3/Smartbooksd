# Smart Book SD – Website

Static website for Smart Book SD (online tax, bookkeeping & payroll). No server or database needed:
it runs on GitHub Pages, Netlify or any static host.

## Editing the site
All pages are generated from **`_build/build.py`**. Open it, change the **SETTINGS** block at the top
(phone, email, booking link, credentials, reviews…) or any page text, then run:

```
python3 _build/build.py      # requires Python 3.12+
```

This rewrites every `.html` page plus `sitemap.xml` and `robots.txt`. Styles live in `assets/styles.css`,
behavior in `assets/main.js`.

## Before launch checklist
1. **Activate the contact form.** Submit the form once on the live site. FormSubmit emails
   Smartbooksd@gmail.com an activation link; click it. After that, every submission arrives by email.
2. **Set `SITE_URL`** in `build.py` if you use a custom domain, then rebuild.
3. **Add credentials** (`CREDENTIALS`), such as your CTEC registration and/or PTIN, EA or CPA license.
4. **Add real reviews only** (`TESTIMONIALS`), with the client's permission.
5. Optional: add a scheduling link (`BOOKING_URL`) and Google Business / Yelp links (`SOCIAL`).
6. Have the Privacy Policy and Terms reviewed by a professional.
7. Each January, update the dates in `DEADLINES` for the new year.

## Pages
Home · Services (+5 service pages) · Resources · Tax Deadlines · Document Checklist · About · FAQ ·
Contact · Privacy · Terms · Accessibility · 404
