#!/usr/bin/env python3
"""
Renders learning-plan.md, resources/README.md, and starter-project/README.md
into a small multi-page site (site/style.css + site/script.js alongside):

  index.html          course overview (hero stats, Context, phase cards, paid summary)
  phase-0.html ... phase-6.html   one page per phase
  resources.html, starter-project.html

Each phase gets its own page (rather than one long scroll) so it's not
possible to accidentally scroll from one phase straight into the next.

The markdown files stay the source of truth. Re-run this after editing them:
    cd site && source .venv/bin/activate && python build.py
"""

import html
import json
import re
from pathlib import Path

import markdown as md

SITE_DIR = Path(__file__).resolve().parent
ROOT_DIR = SITE_DIR.parent

MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists"]

# One accent color per phase (0-6), used for the nav dot, section accent
# bar, and phase-number badge. Keeps each phase visually distinct while
# scrolling/scanning the sidebar.
PHASE_COLORS = [
    "#0d9488",  # 0 teal
    "#2563eb",  # 1 blue
    "#7c3aed",  # 2 violet
    "#c026d3",  # 3 magenta
    "#e11d48",  # 4 rose
    "#ea580c",  # 5 orange
    "#16a34a",  # 6 green
]


def render_md(text: str) -> str:
    return md.markdown(text, extensions=MD_EXTENSIONS)


# ---------------------------------------------------------------------------
# Callout wrapping: turn recognizable **Marker:** paragraphs (and the list
# that immediately follows, for video blocks) into styled <div> callouts.
# Operates on already-rendered HTML, since list rendering must happen first.
# ---------------------------------------------------------------------------

CALLOUT_RULES = [
    # (label pattern matched at start of a <strong>/<em>, css class, icon, consume following <ul>?)
    (r"🎥 Watch first", "callout-video", "🎥", True),
    (r"🧪 Test yourself(?: \(cumulative\))?:", "callout-test", "🧪", True),
    (r"Checkpoint:", "callout-checkpoint", "✅", False),
    (r"Hands-on[^<:]*:", "callout-handson", "🛠️", False),
    (r"Big picture(?: \(optional\))?:", "callout-bigpicture", "🧭", False),
    (r"\[PAID[^\]]*\]", "callout-paid", "💲", False),
]

YOUTUBE_LINK_RE = re.compile(
    r'<a href="https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]{6,})"([^>]*)>(.*?)</a>'
)


def embed_videos(list_html: str) -> str:
    """Turn each <li>...youtube link...</li> into a clickable thumbnail card + caption.

    A true <iframe> embed of youtube.com/youtube-nocookie.com throws "Error 153"
    when the page is opened via file:// (no origin for YouTube to validate against),
    which is exactly how this site is meant to be opened. A thumbnail image linking
    out to the real video sidesteps that restriction entirely while still being far
    more visual than a plain text link.
    """

    def li_repl(m: re.Match) -> str:
        li_inner = m.group(1)
        vm = YOUTUBE_LINK_RE.search(li_inner)
        if not vm:
            return m.group(0)
        video_id, _attrs, _label = vm.groups()
        thumb = (
            f'<a class="video-thumb" href="https://www.youtube.com/watch?v={video_id}" '
            f'target="_blank" rel="noopener">'
            f'<img src="https://img.youtube.com/vi/{video_id}/hqdefault.jpg" '
            f'loading="lazy" alt="Video thumbnail">'
            f'<span class="play-badge">▶</span>'
            f"</a>"
        )
        return f'<li class="video-item">{thumb}<p class="video-caption">{li_inner}</p></li>'

    return re.sub(r"<li>(.*?)</li>", li_repl, list_html, flags=re.DOTALL)


def wrap_callouts(section_html: str) -> str:
    for label_pat, css_class, icon, consume_list in CALLOUT_RULES:
        if consume_list:
            pattern = re.compile(
                r"<p>(?:<strong>|<em>)(" + label_pat + r".*?)(?:</strong>|</em>)</p>\s*(<ul>.*?</ul>)",
                re.DOTALL,
            )

            def repl(m: re.Match) -> str:
                video_list = embed_videos(m.group(2)) if css_class == "callout-video" else m.group(2)
                return (
                    f'<div class="callout {css_class}">'
                    f'<p class="callout-label">{icon} {m.group(1)}</p>'
                    f"{video_list}</div>"
                )

            section_html = pattern.sub(repl, section_html)
        else:
            pattern = re.compile(
                r"<p>(?:<strong>|<em>)(" + label_pat + r")(?:</strong>|</em>)(.*?)</p>",
                re.DOTALL,
            )

            def repl(m: re.Match) -> str:
                return (
                    f'<div class="callout {css_class}">'
                    f'<p><span class="callout-label">{icon} {m.group(1)}</span>{m.group(2)}</p>'
                    f"</div>"
                )

            section_html = pattern.sub(repl, section_html)
    return section_html


# ---------------------------------------------------------------------------
# Lecture splitting: break each phase into Udemy-style checkable "lectures"
# instead of one flat scroll of content. A lecture boundary is any checkable
# callout (video / hands-on / test-yourself / checkpoint); everything before
# the first one is its own "Overview & Resources" lecture. Any <h3> found
# inside a lecture's slice becomes that lecture's title (more descriptive
# than the generic callout label), falling back to the callout's own label
# when there's no <h3> in that slice.
# ---------------------------------------------------------------------------

LECTURE_SPLIT_CLASSES = ("callout-video", "callout-handson", "callout-test", "callout-checkpoint")
LECTURE_ICONS = {
    "callout-video": "🎥",
    "callout-handson": "🛠️",
    "callout-test": "🧪",
    "callout-checkpoint": "✅",
}
LECTURE_FALLBACK_TITLES = {
    "callout-video": "🎥 Watch first",
    "callout-handson": "🛠️ Hands-on",
    "callout-test": "🧪 Test yourself",
    "callout-checkpoint": "✅ Checkpoint",
}

LECTURE_CALLOUT_RE = re.compile(
    r'<div class="callout (' + "|".join(LECTURE_SPLIT_CLASSES) + r')">.*?</div>',
    re.DOTALL,
)
H3_TEXT_RE = re.compile(r"<h3>(.*?)</h3>")


def split_into_lectures(phase_html: str):
    """Returns an ordered list of (title, html_fragment) lecture slices."""
    matches = list(LECTURE_CALLOUT_RE.finditer(phase_html))
    if not matches:
        return [("Overview & Resources", phase_html)]

    lectures = []
    overview_html = phase_html[: matches[0].start()]
    if overview_html.strip():
        lectures.append(("📖 Overview & Resources", overview_html))

    prev_end = matches[0].start()
    for m in matches:
        seg_html = phase_html[prev_end : m.end()]
        css_class = m.group(1)
        h3_texts = H3_TEXT_RE.findall(seg_html)
        if h3_texts:
            title = f"{LECTURE_ICONS[css_class]} {re.sub('<[^>]+>', '', h3_texts[-1])}"
        else:
            title = LECTURE_FALLBACK_TITLES[css_class]
        lectures.append((title, seg_html))
        prev_end = m.end()

    # De-duplicate repeated titles within the same phase ("🛠️ Hands-on" twice, etc.)
    seen = {}
    deduped = []
    for title, seg_html in lectures:
        seen[title] = seen.get(title, 0) + 1
        deduped.append((f"{title} ({seen[title]})" if seen[title] > 1 else title, seg_html))
    return deduped


# ---------------------------------------------------------------------------
# Split learning-plan.md into H1 title + ordered (heading, body) sections
# ---------------------------------------------------------------------------

def split_sections(markdown_text: str):
    lines = markdown_text.splitlines()
    title = ""
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        lines = lines[1:]
    body = "\n".join(lines)

    parts = re.split(r"^## (.+)$", body, flags=re.MULTILINE)
    sections = []
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        content = parts[i + 1] if i + 1 < len(parts) else ""
        content = content.strip("\n")
        content = re.sub(r"\n---\s*$", "", content).strip()
        sections.append((heading, content))
    return title, sections


PHASE_RE = re.compile(r"^Phase (\d+) — (.+)$")


# ---------------------------------------------------------------------------
# Build page
# ---------------------------------------------------------------------------

def rewrite_relative_links(section_html: str, prefix: str) -> str:
    def repl(m: re.Match) -> str:
        target = m.group(1)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        return f'href="{prefix}{target}"'

    return re.sub(r'href="([^"]+)"', repl, section_html)


def open_pdfs_in_new_tab(section_html: str) -> str:
    """PDF links open in a new tab (target="_blank") rather than navigating the
    site away in the current one — the browser's native PDF viewer takes over
    the tab either way, so this keeps the site itself intact behind it."""
    return re.sub(
        r'<a href="([^"]+\.pdf)">',
        r'<a href="\1" target="_blank" rel="noopener" class="pdf-link">',
        section_html,
    )


def parse_learning_plan():
    """Returns (title, context_html, phases, paid_summary_html).

    phases is an ordered list of dicts: id, n, label, short_title, color,
    hours, lectures (list of (lecture_id, lecture_title, lecture_html)).
    """
    text = (ROOT_DIR / "learning-plan.md").read_text()
    title, raw_sections = split_sections(text)

    context_html = ""
    paid_summary_html = ""
    phases = []

    for heading, content in raw_sections:
        m = PHASE_RE.match(heading)
        if m:
            n = int(m.group(1))
            sec_id = f"phase-{n}"
            color = PHASE_COLORS[n % len(PHASE_COLORS)]
            short_title = m.group(2).split("(")[0].strip()
            hrs_match = re.search(r"~(\d+(?:\.\d+)?)\s*hrs", heading)
            hours = float(hrs_match.group(1)) if hrs_match else 0
            rendered = wrap_callouts(render_md(content))
            lecture_slices = split_into_lectures(rendered)
            lectures = []
            for i, (lecture_title, lecture_body) in enumerate(lecture_slices):
                lecture_id = f"{sec_id}-lecture-{i}"
                lectures.append((lecture_id, lecture_title, lecture_body))
            phases.append(
                {
                    "id": sec_id,
                    "n": n,
                    "label": f"Phase {n}: {short_title}",
                    "full_heading": m.group(2),
                    "color": color,
                    "hours": hours,
                    "lectures": lectures,
                }
            )
        elif heading.strip() == "Context":
            context_html = render_md(content)
        elif heading.lower().startswith("summary of paid resources"):
            paid_summary_html = f"<h2>{html.escape(heading)}</h2>{render_md(content)}"

    return title, context_html, phases, paid_summary_html


def render_sidebar(phases, reference_items, n_lectures_total, active_id):
    """active_id is the id of the page currently being rendered — used to
    mark + auto-expand the matching nav entry so you always know where
    you are, without needing scroll-position JS."""
    plan_lis = [
        f'<li><a href="index.html" class="nav-link{" active" if active_id == "index" else ""}" '
        f'data-search="overview">🏠 Course Overview</a></li>'
    ]
    for phase in phases:
        sec_id = phase["id"]
        is_active_phase = sec_id == active_id
        lecture_lis = "\n".join(
            f'<li><a href="{sec_id}.html#{lecture_id}" class="lecture-link" data-lecture="{lecture_id}">'
            f'<span class="lecture-check">○</span> {html.escape(lecture_title)}</a></li>'
            for lecture_id, lecture_title, _ in phase["lectures"]
        )
        n_lectures = len(phase["lectures"])
        plan_lis.append(
            f'<li class="nav-phase-group{" expanded active-page" if is_active_phase else ""}" '
            f'data-phase-group="{sec_id}">'
            f'<div class="nav-phase-header">'
            f'<button type="button" class="nav-chevron-btn" data-toggle="{sec_id}" aria-label="Expand">'
            f'<span class="nav-chevron">▸</span></button>'
            f'<a href="{sec_id}.html" class="nav-phase-link{" active" if is_active_phase else ""}" '
            f'data-search="{html.escape(phase["label"].lower())}">'
            f'<span class="nav-dot" style="background:{phase["color"]}"></span>'
            f'<span class="nav-phase-title">{html.escape(phase["label"])}</span>'
            f"</a>"
            f'<span class="nav-phase-fraction" data-fraction="{sec_id}">0/{n_lectures}</span>'
            f"</div>"
            f'<ul class="lecture-list" data-lectures-for="{sec_id}">{lecture_lis}</ul>'
            f"</li>"
        )

    reference_lis = "\n".join(
        f'<li><a href="{sec_id}.html" class="nav-link{" active" if active_id == sec_id else ""}" '
        f'data-search="{html.escape(label.lower())}">{html.escape(label)}</a></li>'
        for sec_id, label in reference_items
    )

    return f"""
    <div class="nav-group-label">Course Curriculum</div>
    <ul class="nav-list">
      {''.join(plan_lis)}
    </ul>
    <div class="nav-group-label">Reference</div>
    <ul class="nav-list">
      {reference_lis}
    </ul>
    """


def render_shell(title, page_title, sidebar_html, main_html, script_globals):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(page_title)} — {html.escape(title)}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<button id="menu-toggle" class="menu-toggle" aria-label="Toggle navigation">☰</button>
<div class="layout">
  <nav class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <h1>{html.escape(title)}</h1>
      <div class="progress-wrap">
        <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
        <div class="progress-label" id="progress-label">0 lectures complete</div>
      </div>
      <input type="search" id="nav-search" class="nav-search" placeholder="Filter…" autocomplete="off">
    </div>
    {sidebar_html}
  </nav>
  <main class="content">
    {main_html}
  </main>
</div>
<div class="sidebar-scrim" id="sidebar-scrim"></div>
<script>
{script_globals}
</script>
<script src="script.js"></script>
</body>
</html>
"""


def render_phase_page(phase, phases, total_hours):
    idx = phase["n"]
    badge = f'<span class="phase-badge" style="background:{phase["color"]}">{idx}</span>'

    lecture_html_parts = []
    for lecture_id, lecture_title, lecture_body in phase["lectures"]:
        lecture_html_parts.append(
            f'<div class="lecture" id="{lecture_id}">'
            f'<label class="lecture-complete">'
            f'<input type="checkbox" class="lecture-checkbox" data-lecture="{lecture_id}"> '
            f'<span class="lecture-title">{html.escape(lecture_title)}</span>'
            f"</label>"
            f"{lecture_body}"
            f"</div>"
        )

    prev_phase = next((p for p in phases if p["n"] == idx - 1), None)
    next_phase = next((p for p in phases if p["n"] == idx + 1), None)
    prev_link = (
        f'<a class="phase-nav-link phase-nav-prev" href="{prev_phase["id"]}.html">← {prev_phase["label"]}</a>'
        if prev_phase
        else '<a class="phase-nav-link phase-nav-prev" href="index.html">← Course Overview</a>'
    )
    next_link = (
        f'<a class="phase-nav-link phase-nav-next" href="{next_phase["id"]}.html">{next_phase["label"]} →</a>'
        if next_phase
        else ""
    )

    breadcrumb = (
        f'<div class="phase-breadcrumb">'
        f'<a href="index.html">← Course Overview</a>'
        f'<span class="phase-breadcrumb-pos">Phase {idx} of {len(phases) - 1}</span>'
        f"</div>"
    )

    main_html = (
        f"{breadcrumb}"
        f'<section id="{phase["id"]}" class="content-section phase-section" style="--accent:{phase["color"]}">'
        f'<h2>{badge}{html.escape(phase["full_heading"])}</h2>'
        f"{''.join(lecture_html_parts)}"
        f'<div class="phase-nav">{prev_link}{next_link}</div>'
        f"</section>"
    )
    return main_html


def render_simple_doc_page(rel_path: str, page_title: str):
    text = (ROOT_DIR / rel_path).read_text()
    rendered = render_md(text)
    doc_dir_prefix = Path(rel_path).parent.as_posix() + "/"
    rendered = rewrite_relative_links(rendered, f"../{doc_dir_prefix}")
    rendered = open_pdfs_in_new_tab(rendered)
    return (
        f'<div class="phase-breadcrumb"><a href="index.html">← Course Overview</a></div>'
        f'<section class="content-section"><h2>{html.escape(page_title)}</h2>{rendered}</section>'
    )


def build():
    title, context_html, phases, paid_summary_html = parse_learning_plan()

    reference_items = [("resources", "Resources (PDFs & repos)"), ("starter-project", "Starter Project")]

    all_lecture_ids = [lid for phase in phases for lid, _, _ in phase["lectures"]]
    n_lectures_total = len(all_lecture_ids)
    total_hours = sum(p["hours"] for p in phases)
    phase_lectures_json = json.dumps(
        {p["id"]: [lid for lid, _, _ in p["lectures"]] for p in phases}
    )
    script_globals = (
        f"  window.PHASE_LECTURES = {phase_lectures_json};\n"
        f"  window.ALL_LECTURE_IDS = {json.dumps(all_lecture_ids)};\n"
    )

    written_files = []

    def write_page(filename, page_title, active_id, main_html):
        sidebar_html = render_sidebar(phases, reference_items, n_lectures_total, active_id)
        page = render_shell(title, page_title, sidebar_html, main_html, script_globals)
        (SITE_DIR / filename).write_text(page)
        written_files.append(filename)
        print(f"Wrote {filename} ({len(page):,} bytes)")

    # index.html — course overview
    phase_cards = "\n".join(
        f'<a class="phase-card" href="{p["id"]}.html" style="--accent:{p["color"]}">'
        f'<span class="phase-card-badge">{p["n"]}</span>'
        f'<span class="phase-card-title">{html.escape(p["label"].split(": ", 1)[1])}</span>'
        f'<span class="phase-card-meta">{len(p["lectures"])} lectures · ~{int(p["hours"])} hrs</span>'
        f"</a>"
        for p in phases
    )
    index_main = f"""
    <div class="hero">
      <div class="hero-stat"><span class="hero-stat-num">{len(phases)}</span><span class="hero-stat-label">Phases</span></div>
      <div class="hero-stat"><span class="hero-stat-num">{n_lectures_total}</span><span class="hero-stat-label">Lectures</span></div>
      <div class="hero-stat"><span class="hero-stat-num">~{int(total_hours)}</span><span class="hero-stat-label">Core hours</span></div>
      <div class="hero-stat"><span class="hero-stat-num">6</span><span class="hero-stat-label">Hrs/week</span></div>
    </div>
    <section class="content-section"><h2>Context</h2>{context_html}</section>
    <section class="content-section">
      <h2>Course Curriculum</h2>
      <div class="phase-card-grid">{phase_cards}</div>
    </section>
    <section class="content-section">{paid_summary_html}</section>
    """
    write_page("index.html", "Course Overview", "index", index_main)

    # phase-N.html — one per phase
    for phase in phases:
        main_html = render_phase_page(phase, phases, total_hours)
        write_page(f'{phase["id"]}.html', phase["label"], phase["id"], main_html)

    # resources.html / starter-project.html
    write_page(
        "resources.html", "Resources", "resources",
        render_simple_doc_page("resources/README.md", "Resources (PDFs & repos)"),
    )
    write_page(
        "starter-project.html", "Starter Project", "starter-project",
        render_simple_doc_page("starter-project/README.md", "Starter Project"),
    )

    # Verify every relative link across every generated page resolves to a real file.
    broken = []
    for filename in written_files:
        page = (SITE_DIR / filename).read_text()
        for m in re.finditer(r'href="((?!https?://|#)[^"]+)"', page):
            target_path, _, _ = m.group(1).partition("#")
            target = (SITE_DIR / target_path).resolve()
            if not target.exists():
                broken.append(f"{filename} -> {m.group(1)}")
    if broken:
        print("WARNING: broken relative links:")
        for b in broken:
            print(f"  - {b}")
    else:
        print(f"All relative links across {len(written_files)} pages resolve to existing files.")


if __name__ == "__main__":
    build()
