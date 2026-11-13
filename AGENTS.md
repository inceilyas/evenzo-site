# evenzo-site

Single source of instructions; `CLAUDE.md` only contains `@AGENTS.md`. Make changes here.

## Purpose
Static legal and support site for the iPhone budget app (repo `budgetplanning`; store name "Evenzo"): home, Privacy Policy, Terms of Use, Support. Published with GitHub Pages from the root of `main`. The app and App Store Connect link to the English pages, so those URLs must not change once published (`/`, `/privacy.html`, `/terms.html`, `/support.html`). Other languages will live under `/<lang>/` with the same four pages.

## Rules
- Never use emoji, in any output (pages, comments, commit messages, docs).
- Languages: English (source, served from the root) is the only published language for now (`ENABLED_LANGS=en`). The tooling supports 11: en, tr, de, fr, it, es, pt-br, ru, ja, ko, zh-hant (folders `/tr/`, `/de/`, ...). English is the legal source: every non-English privacy and terms page carries a note that the English version prevails. Change the English text first, then update every translation (a structural parity check in `check.py` catches dropped or added blocks). To add a language: add its sources under `src/<folder>/`, its `EFFECTIVE_DATE_<KEY>` to `config.env`, then add the code to `ENABLED_LANGS`.
- The language switcher (`<details>` menu plus footer list, no JavaScript) is hidden by CSS while only one language is published; every page has `hreflang` links and `x-default` (English).
- No tracking: no cookies, no analytics, no external resources (no CDNs, no web fonts from a server). System fonts only; if a font is added later it must be self-hosted under `assets/fonts` with its OFL license, headings only.
- The text must describe only what the app really does. Sources of truth in the app repo (`/Users/ilyasince/Projects/budgetplanning`): `docs/kapsam.md`, `docs/teknik-tasarim.md`, `docs/faz3.md`, `firestore.rules`, `functions/src/` (retention.ts, account.ts, devices.ts, push.ts, groups.ts, funding.ts, fundingStore.ts, apple.ts, notifications.ts, model.ts), `ios/BudgetApp/PrivacyInfo.xcprivacy`, `ios/BudgetApp/Services/FXService.swift`, `ios/BudgetApp/Screens/Group/AppleContinueButton.swift`. When code and docs disagree, the code wins. Do not write about analytics or tools the app does not have. A change in the app (a new data type, a new SDK, a changed retention period, a new analytics tool) means a change here, in `PrivacyInfo.xcprivacy` and in the App Privacy answers in App Store Connect.
- Sales regions: the EU/EEA is a sales region from 2026-11-13 (owner decision), so the privacy policy carries the sections the GDPR requires (purposes and legal bases, international transfers, rights, retention, whether providing data is required, controller contact; no EU representative is appointed, which the policy states as fact). Keep them true to the code: do not claim consent where the app collects none, and mention a provider's EU-US Data Privacy Framework certification only if it is verified. The UK, China and Thailand remain closed for now; do not write that the app is offered there (the policy's rights wording is worded so it also reads correctly for the UK). Other region-specific legal sections are not added unless the owner opens that region.
- Names, contact data and the effective date live only in `config.env`. Use the `{{APP_NAME}}` token in all texts: the app name will change. Page text lives in `src/<lang>/privacy.md`, `terms.md`, `support.md` and `index.html` (`src/en/` is the source). Never edit the generated `*.html` files by hand.
- Open decisions are written in square brackets (for example `[BACKUP_RETENTION_STATEMENT]`, `[2 business days]`, `[APP_STORE_LINK]`). `check.py --strict` fails while any remain.
- Do not commit or push without the owner's approval.

## Workflow
1. Edit `config.env` or a file in `src/<lang>/`.
2. `python3 build.py` regenerates all enabled pages (`python3 build.py de` builds one language as a preview).
3. `python3 check.py` verifies links, anchors, canonical URLs, hreflang, language switcher, the conflict note, structural parity with English, tags, tokens, emoji and external resources. Use `python3 check.py --strict` before publishing.
4. Commit the sources and the generated pages together.

## Design
"B3 Sticker" palette from the app (`design/b3-sistem.md` in the app repo): cream ground `#FFF3DD` with a dot grid, ink `#241713` text and outlines, tomato `#FF5B3A` accent, sun `#FFC933`, teal `#17B196`, cards with a 2.5px ink outline and a hard offset shadow. Tomato fails 4.5:1 on cream, so links are ink with an underline and tomato is used for fills only. System fonts. Visible keyboard focus, skip link, mobile first.
