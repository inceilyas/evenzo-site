#!/usr/bin/env python3
"""Consistency check for the built site (run after build.py): python3 check.py [--strict]

For every language and page: file exists, html lang, canonical URL, hreflang set (11 languages + x-default, reciprocal),
language switcher present, "English version prevails" note on non-English legal pages, internal links and #anchors,
single h1, heading order, balanced tags, leftover {{tokens}}, emoji, external resources (none allowed), non-ASCII
characters inside link targets, and structural parity with the English page (same h2/h3/table/list counts and the same
internal link targets). Open [PLACEHOLDER] decisions are warnings, errors with --strict.

Only languages listed in ENABLED_LANGS (config.env) are published and must pass. Languages that are not enabled yet
but already have built pages are checked as a preview: their problems are printed as "PENDING ERROR" lines and do not
change the exit code.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402

ROOT = build.ROOT
EMOJI = re.compile("[" + chr(0x1F000) + "-" + chr(0x1FAFF) + chr(0x2600) + "-" + chr(0x27BF) + chr(0x2B00) + "-" + chr(0x2BFF) + chr(0xFE0F) + chr(0x200D) + "]")
VOID = {"meta", "link", "br", "img", "hr", "input"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids, self.h, self.alts = [], set(), [], {}
        self.canonical = self.lang = self.title = None
        self.stack, self.problems, self.external = [], [], []
        self.counts = {"table": 0, "ul": 0, "ol": 0, "li": 0, "details": 0, "note": 0, "tr": 0}
        self._in_title = False
        self.in_main = False
        self.in_note = False
        self.main_counts = dict.fromkeys(("table", "ul", "ol", "li", "tr"), 0)
        self.main_links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        elif re.fullmatch(r"h[1-6]", tag):
            self.h.append(int(tag[1]))
        elif tag == "title":
            self._in_title, self.title = True, ""
        if tag == "main":
            self.in_main = True
        if tag in self.counts:
            self.counts[tag] += 1
        if self.in_main and tag in self.main_counts:
            self.main_counts[tag] += 1
        if self.in_main and not self.in_note and tag == "a" and a.get("href"):
            self.main_links.append(a["href"])
        if "legal-note" in (a.get("class") or ""):
            self.counts["note"] += 1
            self.in_note = True
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "link" and a.get("rel") == "alternate":
            self.alts[a.get("hreflang")] = a.get("href")
        elif tag == "link" and a.get("href"):
            self.links.append(a["href"])
            if a["href"].startswith(("http:", "https:", "//")):
                self.external.append(a["href"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("script", "img", "iframe", "source", "video", "audio"):
            self.external.append(f"<{tag}> {a.get('src', '')}")
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
        if tag == "div":
            self.in_note = False
        if tag == "title":
            self._in_title = False
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.problems.append(f"unbalanced </{tag}> (open: {self.stack[-3:]})")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def internal_targets(links):
    """Internal link targets as language-neutral names (file + fragment), for parity checks."""
    out = []
    for href in links:
        if href.startswith(("mailto:", "http:", "https:")):
            continue
        u = urlparse(href)
        name = Path(unquote(u.path)).name if u.path else ""
        out.append(f"{name}#{u.fragment}" if u.fragment else name)
    return sorted(out)


def main():
    strict = "--strict" in sys.argv
    cfg = build.read_config()
    base = cfg["SITE_URL"]
    errors, warnings, pages, pending = [], [], {}, []
    enabled = build.enabled_langs(cfg)
    previews = [l for l in build.LANGS if l not in enabled and build.out_path(l, "index").exists()]
    for lang in enabled + previews:
        for page in build.PAGES:
            f = build.out_path(lang, page)
            if not f.exists():
                (pending if lang in previews else errors).append(f"missing {f.relative_to(ROOT)}")
                continue
            text = f.read_text(encoding="utf-8")
            p = Page()
            p.feed(text)
            pages[f.resolve()] = (lang, page, p, text)
    english = {}
    for f, (lang, page, p, text) in pages.items():
        if lang["code"] == "en":
            english[page] = p
    all_errors = errors
    for f, (lang, page, p, text) in pages.items():
        where = str(f.relative_to(ROOT))
        errors = pending if lang in previews else all_errors
        active = build.active_langs(cfg, lang)
        if p.stack:
            errors.append(f"{where}: unclosed tags {p.stack}")
        errors += [f"{where}: {x}" for x in p.problems]
        if p.lang != lang["code"]:
            errors.append(f"{where}: html lang {p.lang!r}, expected {lang['code']!r}")
        if not p.title or not p.title.strip().replace("|", "").strip():
            errors.append(f"{where}: empty title")
        if p.canonical != build.page_url(cfg, lang, page):
            errors.append(f"{where}: canonical {p.canonical!r}")
        expected = {l["code"]: build.page_url(cfg, l, page) for l in active}
        expected["x-default"] = build.page_url(cfg, build.BY_CODE[build.X_DEFAULT_LANG], page)
        if p.alts != expected:
            errors.append(f"{where}: hreflang differs: {set(p.alts.items()) ^ set(expected.items())}")
        if p.h.count(1) != 1:
            errors.append(f"{where}: {p.h.count(1)} h1 elements")
        for prev, cur in zip(p.h, p.h[1:]):
            if cur > prev + 1:
                errors.append(f"{where}: heading jumps from h{prev} to h{cur}")
        if "{{" in text or "}}" in text:
            errors.append(f"{where}: leftover token")
        if EMOJI.search(text):
            errors.append(f"{where}: emoji found")
        if p.external:
            errors.append(f"{where}: external resources {p.external}")
        if p.counts["details"] != 1:
            errors.append(f"{where}: expected one language <details>, found {p.counts['details']}")
        want_note = 1 if (page in build.LEGAL_PAGES and lang["code"] != "en") else 0
        if p.counts["note"] != want_note:
            errors.append(f"{where}: conflict note count {p.counts['note']}, expected {want_note}")
        for m in build.OPEN_PLACEHOLDER.finditer(re.sub(r"<[^>]+>", "", text)):
            warnings.append(f"{where}: open placeholder {m.group(0)}")
        for href in p.links:
            if re.search(r"[^\x00-\x7f]", href):
                errors.append(f"{where}: non-ASCII character in link {href!r} (put a space after URLs in the source)")
            u = urlparse(href)
            if u.scheme in ("http", "https", "mailto"):
                continue
            target = f if not u.path else (f.parent / unquote(u.path)).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{where}: broken link {href}")
            elif u.fragment and target.suffix == ".html":
                tp = pages.get(target)
                if u.fragment not in (tp[2].ids if tp else set()):
                    errors.append(f"{where}: missing anchor {href}")
        # structural parity with English (translations must not drop or add blocks)
        if lang["code"] != "en" and page in english:
            en = english[page]
            if p.h != en.h:
                errors.append(f"{where}: heading structure differs from English ({len(p.h)} vs {len(en.h)} headings)")
            for k in ("table", "ul", "ol", "li", "tr"):
                if p.main_counts[k] != en.main_counts[k]:
                    errors.append(f"{where}: {k} count {p.main_counts[k]} differs from English {en.main_counts[k]}")
            if internal_targets(p.main_links) != internal_targets(en.main_links):
                errors.append(f"{where}: internal link targets differ from English")
            ext_p = sorted(h for h in p.main_links if h.startswith(("http:", "https:")))
            ext_e = sorted(h for h in en.main_links if h.startswith(("http:", "https:")))
            if ext_p != ext_e:
                errors.append(f"{where}: external links differ from English")
    errors = all_errors
    css = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
    if re.search(r"@import|url\(\s*['\"]?(https?:|//)", css):
        errors.append("style.css loads an external resource")
    for url in re.findall(r"url\(\s*['\"]?([^'\")]+)", css):
        if not (ROOT / "assets" / url).exists():
            errors.append(f"style.css: missing file {url}")
    if not (ROOT / "assets" / "favicon.svg").exists():
        errors.append("missing assets/favicon.svg")
    if not (ROOT / ".nojekyll").exists():
        errors.append("missing .nojekyll")
    for w in warnings:
        print("WARNING", w)
    for e in errors:
        print("ERROR", e)
    for e in pending:
        print("PENDING ERROR", e)
    if previews:
        print("preview (not enabled):", ", ".join(l["code"] for l in previews))
    if errors or (strict and warnings):
        return 1
    n_links = sum(len(v[2].links) for v in pages.values())
    print(f"OK: {len(pages)} pages in {len(enabled)} enabled language(s), {n_links} links checked, {len(warnings)} open placeholder warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
