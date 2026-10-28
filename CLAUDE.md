# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A multi-page static HTML portfolio site for artist 박현지 (Park Hyun Ji, artist name "켡"/HYUNZ, brand "예술보부상"/Art Bobusang). No build system, no package manager, no JS framework — every page is a hand-editable `.html` file with its CSS inlined in a `<style>` block and a little vanilla JS where needed. There is no dev server or bundler.

The site is pushed to GitHub at `zzzprk/artbobu` (see `git remote -v`) and served as a static site from there — **pushing to `main` is effectively deploying.** Only push when the user explicitly asks to deploy; "commit only" means commit without pushing.

## Pages

Top navigation (same on every page): `about · text · exhibition · works · contact`, logo links to `index.html`.

| File | Content |
| --- | --- |
| [index.html](index.html) | Landing page: artist name, hero image (`image_001.jpg`), five-category menu |
| [about.html](about.html) | Short intro + the **full CV** (Solo / Group exhibitions, Art Fair, Video & Performance, Illustration & Drawing, Residencies, Awards, Publications, Art Bobusang brand history) |
| [text.html](text.html) | Bilingual Artist Note (KR + EN) |
| [exhibition.html](exhibition.html) | Exhibition portfolio. One collapsible row per exhibition (`<details class="exh" id="exh-N">`); opening a row shows its video and/or exhibited works. No work/video counts are shown on the rows. |
| [works.html](works.html) | Works, split into tabs (see below) |
| [contact.html](contact.html) | Email and Instagram |

**CSS is duplicated in every page's `<style>` block** (there is no shared stylesheet). When changing shared styles (nav, figure/caption, footer, tokens in `:root`), apply the same change to every page.

## Exhibition page

- Each exhibition = `<details class="exh" id="exh-N"><summary>…year / t-kr / t-en / venue…</summary><div class="exh-body">…figures…</div></details>`, newest first. `exhibition.html#exh-N` opens that row.
- Works shown inside an exhibition use the normal `figure.work` structure with the **work's original caption** (title, English title, medium/size/year). Do **not** write generic captions such as "전시 전경" / "전시 작품" / the exhibition name. If a photo has no known caption, leave it without a caption.
- The 2026 "여기는 카페 켡입니다" row contains a YouTube embed plus a photo gallery (`.exh-gallery`, photos have no captions). The iframe uses `data-src`; a small script sets `src` when the row opens and removes it when it closes (stops playback). Embedding **does not work when the page is opened as a `file://`** (YouTube shows a player configuration error) — preview through a local server (`python -m http.server 8000`) or the deployed site. A "Watch on YouTube" link is kept under the video as a fallback.
- Exhibition rows only exist for exhibitions that have works/video to show; the complete exhibition list lives in `about.html`.

## Works page

Tabs (buttons `.wtab[data-cat]` switching `div.wcat#<id>`; selected tab is kept in the URL hash, e.g. `works.html#media-art`):

1. `painting` — 그림 / Painting (currently empty, shows "작품을 준비 중입니다 · Coming soon")
2. `analog-motion` — 아날로그 모션 / Analog Motion
3. `media-art` — 미디어 아트 / Media Art
4. `installation-art` — 설치 미술 / Installation Art
5. `art-kit` — 예술 키트 / Art Kit

An empty category carries `data-empty="1"`; on load the first non-empty tab is opened by default.

**Dedup rule (user's preference):** a work lives either in `exhibition.html` or in `works.html`, not both, and the same work title should not appear twice on one page. When moving a work into an exhibition, remove it from `works.html`.

## Repository layout

- `image/` — `image_001.jpg` … `image_062.jpg`, sequentially named and referenced by path (`src="image/image_0NN.jpg"`).
- `image/cafe_kyun/cafe_kyun_01.jpg … 13.jpg` — web-optimized (≤1800px) photos of the "여기는 카페 켡입니다" exhibition. Full-size originals sit in `image/cafe_kyun/original/` and are **not** deployed.
- `image/added/` — web-optimized images extracted from `pdf/넣을것.pdf` / `pdf/넣을것2.pdf` (descriptive names, e.g. `daejeon2018_poster.jpg`); used by new exhibition rows (2018 대전, 2019 장, 2020 담양·조치원) and the 그림 / 설치 미술 tabs.
- `works/fleeting_gaze/` — 〈찰나의 시선〉 flipbook: `moment_1_web.jpg`, `moment_2_web.mp4` (+ `moment_2_poster.jpg`) are used by the page; `moment_1.jpg` / `moment_2.mp4` are unused originals (not deployed).
- `mov/` — local video files (not used by the site; not deployed).
- `pdf/` — source portfolio PDF (`포트폴리오 정리중.pdf`) the early images were extracted from.
- `extract_images.py` — one-off PyMuPDF script for that extraction; a template, not something to re-run as-is.

## Working with content

- **Images `image_001`–`image_062` are numbered sequentially and gapless.** If you add, remove, or reorder one of these, keep the sequence contiguous and update every `<img src>` that points to a renumbered file. New photo sets go in their own subfolder (like `image/cafe_kyun/`) with names like `cafe_kyun_NN.jpg` instead of extending the numbered series.
- Every work entry is a `<figure class="work">` with an `<img>` and a `<figcaption>` containing `.t-kr` (Korean title), `.t-en` (English title), `<br/>`, then a line of medium/dimensions/year (bilingual, `·`-separated), and an optional `.desc` span. Follow this structure exactly.
- Always keep `width`/`height` on `<img>` equal to the real file's aspect ratio (prevents layout shift) and write a real descriptive Korean `alt`. (`image_043.jpg` is deliberately displayed at 470px wide.)
- CV entries use `.cv-item` (`.yr` | content) with paired `.lang-ko` / `.lang-en` spans, both shown together. Only the first row of a year carries the year in `.yr`. Keep the KR/EN pairing when adding rows.
- Gallery images use `loading="lazy"`; the scroll-reveal effect (`.work`/`.hero-fig` fade-in via `IntersectionObserver`) applies on pages that include that script.
- **Videos must be H.264 + AAC with `-movflags +faststart`.** Phone videos are often HEVC and will not play in most browsers — transcode (`ffmpeg -c:v libx264 -pix_fmt yuv420p -crf 26 -c:a aac -movflags +faststart`) before using. Photos from phones should be resized (≈1800px long side, quality ≈85) before they are added.
- Do not deploy unused or original-size media (see layout above). If a new media folder holds originals, keep them out of the commit.

## Verifying changes

There is no test suite, linter, or build step. Preview through a static server (`python -m http.server 8000`, then `http://localhost:8000/`) rather than double-clicking, so YouTube embeds work. Check the affected page visually — image aspect ratios, caption alignment, tab switching on `works.html`, accordion open/close on `exhibition.html`, and mobile width.

Before deploying, confirm every local `src`/`poster`/`href` in the pages points to a file that exists in the repo.
