# evenzo-site

Static legal and support pages for the iPhone budget app (Evenzo): home, Privacy Policy, Terms of Use and Support. English only for now; the tooling is ready for 11 languages. No cookies, no analytics, no external resources.

## Files

| Path | Purpose |
| --- | --- |
| `index.html`, `privacy.html`, `terms.html`, `support.html` | Generated English pages at the root (served by GitHub Pages; do not edit by hand) |
| `src/en/index.html` | Home page fragment (`src/en/` is the source language) |
| `src/en/privacy.md`, `terms.md`, `support.md` | Page text in Markdown |
| `src/layout.html` | Shared page template (header, navigation, footer) |
| `config.env` | `APP_NAME`, `SUPPORT_EMAIL`, `DEVELOPER_NAME`, `SITE_URL`, `YEAR`, `ENABLED_LANGS`, `EFFECTIVE_DATE_<KEY>` per language |
| `build.py`, `check.py` | Build and check scripts (Python 3 standard library only) |
| `assets/style.css`, `assets/favicon.svg` | Styles (B3 Sticker palette) and icon |
| `.nojekyll` | Turns off Jekyll processing on GitHub Pages; keep it |

## Rebuild

```sh
python3 build.py     # regenerates every enabled language from src/ and config.env
python3 check.py     # links, anchors, canonical, hreflang, switcher, parity with English, tags, tokens, emoji, external resources
```

Use `python3 check.py --strict` before publishing. It fails while open decisions written in square brackets (for example `[BACKUP_RETENTION_STATEMENT]`, `[2 business days]`, `[APP_STORE_LINK]`) remain in the text.

Where to change things:

- App name (when the store name is chosen), e-mail, effective date, site URL: `config.env`, then rebuild. Texts use the `{{APP_NAME}}` token.
- Wording: the English file in `src/en/` first, then every translation, then rebuild. Keep the app repo (`PrivacyInfo.xcprivacy`) and the App Privacy answers in App Store Connect in sync.
- More languages: add `src/<folder>/` files (tr, de, fr, it, es, pt-br, ru, ja, ko, zh-hant), `EFFECTIVE_DATE_<KEY>` in `config.env`, then add the code to `ENABLED_LANGS`.

## Publish with GitHub Pages

1. Create a public GitHub repository named `evenzo-site` (the free Pages plan needs a public repository) and push `main`.
2. Settings > Pages > Build and deployment > Source: "Deploy from a branch", Branch: `main`, folder `/ (root)`.
3. After a minute or two the site is live at `https://inceilyas.github.io/evenzo-site/`.

URLs for the app and App Store Connect:

- Privacy Policy: `https://inceilyas.github.io/evenzo-site/privacy.html`
- Terms of Use: `https://inceilyas.github.io/evenzo-site/terms.html`
- Support: `https://inceilyas.github.io/evenzo-site/support.html`
- Marketing: `https://inceilyas.github.io/evenzo-site/`

## Before publishing

- `python3 check.py --strict` passes (no open placeholders).
- Texts match the shipped app (retention periods, deletion flow, prices) and the App Privacy answers.
- A lawyer review of the privacy policy and terms is recommended; none has been done.
