#!/usr/bin/env python3
"""Builds the multilingual site: src/<lang>/<page> + src/layout.html + config.env -> HTML pages.

English is served from the site root (index.html, privacy.html, terms.html, support.html), because the app and
App Store Connect link to those URLs. Every other language lives in its own folder (tr/, de/, fr/, it/, es/,
pt-br/, ru/, ja/, ko/, zh-hant/) with the same four pages. The language table is LANGS below.

Sources per language (src/<folder>/): index.html is an HTML fragment; privacy.md, terms.md and support.md are small
Markdown files (headings, paragraphs, lists, tables, **bold**, `code`, [links](url), bare URLs and e-mail addresses;
a paragraph that starts with "> " is the effective-date line). Each source starts with `title:` and `description:`
lines followed by a blank line. {{TOKENS}} are filled from config.env. Python 3 standard library only.
Usage: python3 build.py [lang-code ...]   (no arguments builds every language)
"""
import html
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = ["index", "privacy", "terms", "support"]
LEGAL_PAGES = ("privacy", "terms")

# Language table: code (html lang and hreflang), path (folder; English at the root), key (config.env suffix), name (own language).
LANGS = [
    {"code": "en", "path": "", "key": "EN", "name": "English"},
    {"code": "tr", "path": "tr", "key": "TR", "name": "Türkçe"},
    {"code": "de", "path": "de", "key": "DE", "name": "Deutsch"},
    {"code": "fr", "path": "fr", "key": "FR", "name": "Français"},
    {"code": "it", "path": "it", "key": "IT", "name": "Italiano"},
    {"code": "es", "path": "es", "key": "ES", "name": "Español"},
    {"code": "pt-BR", "path": "pt-br", "key": "PT_BR", "name": "Português (Brasil)"},
    {"code": "ru", "path": "ru", "key": "RU", "name": "Русский"},
    {"code": "ja", "path": "ja", "key": "JA", "name": "日本語"},
    {"code": "ko", "path": "ko", "key": "KO", "name": "한국어"},
    {"code": "zh-Hant", "path": "zh-hant", "key": "ZH_HANT", "name": "繁體中文"},
]
BY_CODE = {l["code"]: l for l in LANGS}
DEFAULT_LANG = "en"      # served from the root
X_DEFAULT_LANG = "en"    # hreflang x-default

# nav: Home / Privacy / Terms / Support. table: accessible label of scrollable tables. conflict and conflict_link:
# the "English version prevails" note shown under the title of the legal pages (every language except English).
UI = {
    "en": {
        "nav": {"index": "Home", "privacy": "Privacy", "terms": "Terms", "support": "Support"},
        "skip": "Skip to content", "menu": "Main menu", "languages": "Language", "table": "Table",
        "footer_rights": "All rights reserved.",
    },
    "tr": {
        "nav": {"index": "Ana sayfa", "privacy": "Gizlilik", "terms": "Şartlar", "support": "Destek"},
        "skip": "İçeriğe geç", "menu": "Ana menü", "languages": "Dil", "table": "Tablo",
        "footer_rights": "Tüm hakları saklıdır.",
        "conflict": "Çeviriler kolaylık içindir. Sürümler arasında çelişki olursa İngilizce sürüm geçerlidir.", "conflict_link": "İngilizce sürüm",
    },
    "de": {
        "nav": {"index": "Start", "privacy": "Datenschutz", "terms": "Bedingungen", "support": "Support"},
        "skip": "Zum Inhalt springen", "menu": "Hauptmenü", "languages": "Sprache", "table": "Tabelle",
        "footer_rights": "Alle Rechte vorbehalten.",
        "conflict": "Die Übersetzung dient der Information. Bei Abweichungen gilt die englische Fassung.", "conflict_link": "Englische Fassung",
    },
    "fr": {
        "nav": {"index": "Accueil", "privacy": "Confidentialité", "terms": "Conditions", "support": "Assistance"},
        "skip": "Aller au contenu", "menu": "Menu principal", "languages": "Langue", "table": "Tableau",
        "footer_rights": "Tous droits réservés.",
        "conflict": "La traduction est fournie à titre indicatif. En cas de divergence, la version anglaise prévaut.", "conflict_link": "Version anglaise",
    },
    "it": {
        "nav": {"index": "Home", "privacy": "Privacy", "terms": "Termini", "support": "Assistenza"},
        "skip": "Vai al contenuto", "menu": "Menu principale", "languages": "Lingua", "table": "Tabella",
        "footer_rights": "Tutti i diritti riservati.",
        "conflict": "La traduzione ha valore informativo. In caso di discrepanza prevale la versione inglese.", "conflict_link": "Versione inglese",
    },
    "es": {
        "nav": {"index": "Inicio", "privacy": "Privacidad", "terms": "Términos", "support": "Ayuda"},
        "skip": "Saltar al contenido", "menu": "Menú principal", "languages": "Idioma", "table": "Tabla",
        "footer_rights": "Todos los derechos reservados.",
        "conflict": "La traducción se ofrece a título informativo. En caso de conflicto, prevalece la versión en inglés.", "conflict_link": "Versión en inglés",
    },
    "pt-BR": {
        "nav": {"index": "Início", "privacy": "Privacidade", "terms": "Termos", "support": "Suporte"},
        "skip": "Ir para o conteúdo", "menu": "Menu principal", "languages": "Idioma", "table": "Tabela",
        "footer_rights": "Todos os direitos reservados.",
        "conflict": "A tradução é fornecida para sua conveniência. Em caso de divergência, prevalece a versão em inglês.", "conflict_link": "Versão em inglês",
    },
    "ru": {
        "nav": {"index": "Главная", "privacy": "Конфиденциальность", "terms": "Условия", "support": "Поддержка"},
        "skip": "Перейти к содержимому", "menu": "Главное меню", "languages": "Язык", "table": "Таблица",
        "footer_rights": "Все права защищены.",
        "conflict": "Перевод предоставлен для удобства. В случае расхождений приоритет имеет английская версия.", "conflict_link": "Английская версия",
    },
    "ja": {
        "nav": {"index": "ホーム", "privacy": "プライバシー", "terms": "利用規約", "support": "サポート"},
        "skip": "本文へスキップ", "menu": "メインメニュー", "languages": "言語", "table": "表",
        "footer_rights": "すべての権利を保有します。",
        "conflict": "この翻訳は参考用です。内容に相違がある場合は、英語版が優先されます。", "conflict_link": "英語版",
    },
    "ko": {
        "nav": {"index": "홈", "privacy": "개인정보", "terms": "약관", "support": "지원"},
        "skip": "본문으로 건너뛰기", "menu": "주 메뉴", "languages": "언어", "table": "표",
        "footer_rights": "모든 권리 보유.",
        "conflict": "번역본은 편의를 위해 제공됩니다. 내용이 서로 다른 경우 영어판이 우선합니다.", "conflict_link": "영어판",
    },
    "zh-Hant": {
        "nav": {"index": "首頁", "privacy": "隱私權", "terms": "條款", "support": "支援"},
        "skip": "跳到主要內容", "menu": "主選單", "languages": "語言", "table": "表格",
        "footer_rights": "保留所有權利。",
        "conflict": "翻譯僅供參考。如各版本內容不一致，以英文版為準。", "conflict_link": "英文版",
    },
}
# Open decisions still written in square brackets inside the sources, e.g. [UPGRADE_RULE] or [2 business days].
OPEN_PLACEHOLDER = re.compile(r"\[(?:[A-Z][A-Z_0-9]{2,}|\d[^\]]*)\](?!\()")


def read_config():
    cfg = {}
    for line in (ROOT / "config.env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        cfg[key.strip()] = value.strip()
    cfg.setdefault("YEAR", str(date.today().year))
    return cfg


def fill(text, values):
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: values.get(m.group(1), m.group(0)), text)


def inline(text):
    stash = []

    def keep(markup):
        stash.append(markup)
        return f"\x00{len(stash) - 1}\x00"

    t = html.escape(text, quote=False)

    def md_link(m):
        label, url = m.group(1), m.group(2)
        ext = url.startswith("http")
        rel = ' rel="noopener"' if ext else ""
        return keep(f'<a href="{html.escape(url)}"{rel}>{label}</a>')

    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", md_link, t)

    def bare_url(m):
        url = m.group(0)
        tail = ""
        while url and url[-1] in ".,;:":
            tail = url[-1] + tail
            url = url[:-1]
        return keep(f'<a href="{url}" rel="noopener">{url}</a>') + tail

    t = re.sub(r"https?://[^\s<>)\x00\u0080-\U0010ffff]+", bare_url, t)
    t = re.sub(r"[A-Za-z0-9.+_-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]*[A-Za-z0-9]", lambda m: keep(f'<a href="mailto:{m.group(0)}">{m.group(0)}</a>'), t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], t)


def render_table(rows, label):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], [r for r in cells[2:]]
    out = [f'<div class="table-wrap" tabindex="0" role="region" aria-label="{html.escape(label)}">', "<table>", "  <thead><tr>"]
    out.append("".join(f'<th scope="col">{inline(c)}</th>' for c in head) + "</tr></thead>")
    out.append("  <tbody>")
    for r in body:
        out.append("    <tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    out += ["  </tbody>", "</table>", "</div>"]
    return "\n".join(out)


def heading_id(text, level, counters):
    """Language-neutral ids: section-N for numbered h2, N-M for numbered h3, else h2-K / q-K counters."""
    m = re.match(r"(\d+)(?:\.(\d+))?\.?\s", text)
    if m and level == 2:
        return f"section-{m.group(1)}"
    if m and level == 3 and m.group(2):
        return f"section-{m.group(1)}-{m.group(2)}"
    counters[level] = counters.get(level, 0) + 1
    return ("h2-" if level == 2 else "q-") + str(counters[level])


def render_markdown(md, table_label="Table"):
    lines = md.splitlines()
    out, toc, i = [], [], 0
    toc_at = None
    counters = {}
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"(#{1,3}) (.+)", line)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 2:
                sid = heading_id(text, 2, counters)
                toc.append((sid, text))
                out.append(f'<h2 id="{sid}">{inline(text)}</h2>')
            elif level == 3:
                out.append(f'<h3 id="{heading_id(text, 3, counters)}">{inline(text)}</h3>')
            else:
                out.append(f"<h1>{inline(text)}</h1>")
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(render_table(rows, table_label))
            continue
        if re.match(r"- ", line):
            items = []
            while i < len(lines) and re.match(r"- ", lines[i]):
                items.append(lines[i][2:].strip())
                i += 1
            out.append("<ul>\n" + "\n".join(f"  <li>{inline(x)}</li>" for x in items) + "\n</ul>")
            continue
        if re.match(r"\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i]).strip())
                i += 1
            out.append("<ol>\n" + "\n".join(f"  <li>{inline(x)}</li>" for x in items) + "\n</ol>")
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"(#{1,3} |\||- |\d+\. )", lines[i]):
            para.append(lines[i].strip())
            i += 1
        cls = ""
        if para[0].startswith("> "):
            para[0] = para[0][2:]
            cls = ' class="meta"'
        text = "<br>\n".join(inline(p) for p in para)
        out.append(f"<p{cls}>{text}</p>")
        if cls and toc_at is None:
            toc_at = len(out)
    if toc_at is not None and len(toc) > 4:
        items = "\n".join(f'    <li><a href="#{sid}">{inline(re.sub(r"^\d+\.\s*", "", t))}</a></li>' for sid, t in toc)
        out.insert(toc_at, f'<nav class="toc" aria-label="Contents">\n  <ol>\n{items}\n  </ol>\n</nav>')
    return "\n\n".join(out)


def parse_source(path):
    raw = path.read_text(encoding="utf-8")
    head, _, body = raw.partition("\n\n")
    meta = {}
    for line in head.splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta, body.strip()


def src_dir(lang):
    return ROOT / "src" / (lang["path"] or "en")


def out_path(lang, page):
    folder = ROOT / lang["path"] if lang["path"] else ROOT
    return folder / f"{page}.html"


def page_url(cfg, lang, page):
    prefix = f"{lang['path']}/" if lang["path"] else ""
    return f"{cfg['SITE_URL']}/{prefix}" + ("" if page == "index" else f"{page}.html")


def rel_link(lang, page, target):
    """Relative link from `page` in `lang` to the same page in `target`."""
    name = f"{page}.html"
    if lang["code"] == target["code"]:
        return name
    up = "../" if lang["path"] else ""
    down = f"{target['path']}/" if target["path"] else ""
    return f"{up}{down}{name}"


def source_file(lang, page):
    return src_dir(lang) / (f"{page}.html" if page == "index" else f"{page}.md")


def effective_date(cfg, lang):
    return cfg.get(f"EFFECTIVE_DATE_{lang['key']}") or cfg["EFFECTIVE_DATE_EN"]


def esc(text):
    return text.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def enabled_langs(cfg):
    """Languages published on the site (config.env ENABLED_LANGS, comma separated, in LANGS order). English is required."""
    codes = [c.strip() for c in cfg.get("ENABLED_LANGS", "en").split(",") if c.strip()]
    unknown = [c for c in codes if c not in BY_CODE]
    if unknown or "en" not in codes:
        raise SystemExit(f"ENABLED_LANGS must contain 'en' and only known codes (got {codes})")
    return [l for l in LANGS if l["code"] in codes]


def active_langs(cfg, extra=None):
    """Enabled languages plus one language being previewed (built explicitly but not published yet)."""
    en = enabled_langs(cfg)
    if extra and extra not in en:
        en = [l for l in LANGS if l in en or l is extra]
    return en


def hreflang_links(cfg, page, langs):
    lines = [f'<link rel="alternate" hreflang="{l["code"]}" href="{page_url(cfg, l, page)}">' for l in langs]
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{page_url(cfg, BY_CODE[X_DEFAULT_LANG], page)}">')
    return "\n  ".join(lines)


def language_list(lang, page, cls, langs):
    """All languages as links; no JavaScript needed. The current language is marked with aria-current."""
    items = []
    for t in langs:
        current = ' aria-current="true"' if t["code"] == lang["code"] else ""
        items.append(
            f'<li><a href="{rel_link(lang, page, t)}" hreflang="{t["code"]}" lang="{t["code"]}"{current}>{t["name"]}</a></li>'
        )
    return f'<ul class="{cls}">\n          ' + "\n          ".join(items) + "\n        </ul>"


def legal_note(lang, page, ui):
    if page not in LEGAL_PAGES or "conflict" not in ui:
        return ""
    href = rel_link(lang, page, BY_CODE[X_DEFAULT_LANG])
    return (
        '<div class="note legal-note" role="note">'
        f'<p>{ui["conflict"]} <a href="{href}" hreflang="en" lang="en">{ui["conflict_link"]}</a></p></div>'
    )


def insert_legal_note(body, note):
    """Insert the note right after the effective-date paragraph."""
    if not note:
        return body
    m = re.search(r'<p class="meta">.*?</p>', body, re.S)
    if not m:
        raise SystemExit('legal note needs a <p class="meta"> effective-date paragraph')
    return body[: m.end()] + "\n\n" + note + body[m.end():]


def write_gitignore(cfg):
    """Keep unpublished languages out of git: their output folders and sources are ignored until enabled."""
    path = ROOT / ".gitignore"
    keep = [l for l in path.read_text(encoding="utf-8").splitlines()] if path.exists() else []
    begin, end = "# BEGIN unpublished languages (managed by build.py)", "# END unpublished languages"
    if begin in keep:
        i, j = keep.index(begin), keep.index(end)
        keep = keep[:i] + keep[j + 1:]
    enabled = {l["code"] for l in enabled_langs(cfg)}
    block = [begin]
    for l in LANGS:
        if l["code"] not in enabled:
            block += [f"/{l['path']}/", f"/src/{l['path']}/"]
    block.append(end)
    if len(block) > 2:
        keep += block
    path.write_text("\n".join(x for x in keep if x is not None).rstrip("\n") + "\n", encoding="utf-8")


def main():
    cfg = read_config()
    layout = (ROOT / "src" / "layout.html").read_text(encoding="utf-8")
    open_found = []
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    enabled = enabled_langs(cfg)
    for code in only:
        if code not in BY_CODE:
            raise SystemExit(f"unknown language code {code!r}")
    to_build = [l for l in LANGS if l["code"] in only] if only else enabled
    for lang in to_build:
        langs = active_langs(cfg, lang)
        ui = UI[lang["code"]]
        prefix = "../" if lang["path"] else ""
        for page in PAGES:
            meta, body = parse_source(source_file(lang, page))
            values = dict(cfg)
            values.update({
                "LANG": lang["code"],
                "ROOT": prefix,
                "APP_NAME": cfg["APP_NAME"],
                "EFFECTIVE_DATE": effective_date(cfg, lang),
            })
            if page != "index":
                body = fill(body, values)
                for m in OPEN_PLACEHOLDER.finditer(body):
                    open_found.append((f"{lang['code']}/{page}", m.group(0)))
                body = render_markdown(body, ui["table"])
            body = insert_legal_note(body, legal_note(lang, page, ui))
            nav = "\n        ".join(
                f'<a href="{p}.html"' + (' aria-current="page"' if p == page else "") + f">{ui['nav'][p]}</a>"
                for p in PAGES
            )
            footer = " ".join(f'<a href="{p}.html">{ui["nav"][p]}</a>' for p in PAGES[1:])
            title = fill(meta["title"], values)
            if page != "index":
                title = f"{title} | {cfg['APP_NAME']}"
            values.update({
                "PAGE_TITLE": html.escape(title, quote=False),
                "DESCRIPTION": esc(fill(meta["description"], values)),
                "CANONICAL": page_url(cfg, lang, page),
                "HREFLANGS": hreflang_links(cfg, page, langs),
                "NAV": nav,
                "FOOTER_LINKS": footer,
                "CONTENT": fill(body, values),
                "LANG_NAME": lang["name"],
                "LANG_LABEL": ui["languages"],
                "LANG_LIST_MENU": language_list(lang, page, "lang-list", langs),
                "LANG_LIST_FOOTER": language_list(lang, page, "lang-list footer-langs", langs),
                "SKIP": ui["skip"],
                "MENU": ui["menu"],
                "FOOTER_RIGHTS": ui["footer_rights"],
                "HOME": "index.html",
                "PAGE": page,
            })
            target = out_path(lang, page)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(fill(layout, values), encoding="utf-8")
            print("written:", target.relative_to(ROOT))
    write_gitignore(cfg)
    for page, token in open_found:
        print(f"WARNING open placeholder in {page}: {token}", file=sys.stderr)
    if open_found:
        print(f"{len(open_found)} open placeholder(s): do not publish before they are resolved.", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
