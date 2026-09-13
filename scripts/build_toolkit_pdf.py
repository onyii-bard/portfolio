"""
Build 'The 6-Skill Marketer's Toolkit' v2, an editorial-styled PDF sourced
from the marketing-skills SKILL.md pack. Avenir Next + Bodoni 72, not
default Helvetica, no card-template look.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, NextPageTemplate, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas as pdfcanvas

# ---------------------------------------------------------------- fonts ----
pdfmetrics.registerFont(TTFont("AvenirNext", "/System/Library/Fonts/Avenir Next.ttc", subfontIndex=7))
pdfmetrics.registerFont(TTFont("AvenirNext-Italic", "/System/Library/Fonts/Avenir Next.ttc", subfontIndex=4))
pdfmetrics.registerFont(TTFont("AvenirNext-Medium", "/System/Library/Fonts/Avenir Next.ttc", subfontIndex=5))
pdfmetrics.registerFont(TTFont("AvenirNext-Demi", "/System/Library/Fonts/Avenir Next.ttc", subfontIndex=2))
pdfmetrics.registerFont(TTFont("AvenirNext-Bold", "/System/Library/Fonts/Avenir Next.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("AvenirNext-Heavy", "/System/Library/Fonts/Avenir Next.ttc", subfontIndex=8))
pdfmetrics.registerFont(TTFont("Bodoni", "/System/Library/Fonts/Supplemental/Bodoni 72.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("Bodoni-Italic", "/System/Library/Fonts/Supplemental/Bodoni 72.ttc", subfontIndex=1))
pdfmetrics.registerFont(TTFont("Bodoni-Bold", "/System/Library/Fonts/Supplemental/Bodoni 72.ttc", subfontIndex=2))

# ---- Brand palette ----
PRIMARY   = colors.HexColor("#F4A261")
SECONDARY = colors.HexColor("#E76F51")
DARK      = colors.HexColor("#264653")
NEUTRAL   = colors.HexColor("#FAF9F6")
TEXT      = colors.HexColor("#1A1A1A")
MUTED     = colors.HexColor("#6E6E6E")
LINE      = colors.HexColor("#E4E1DA")
WHITE     = colors.white

# Per-skill accent, cycling through the palette
ACCENTS = [SECONDARY, DARK, PRIMARY, SECONDARY, DARK, PRIMARY]

PAGE_W, PAGE_H = letter
MARGIN = 0.78 * inch

OUT_PATH = "/Users/onyinyeojukwu/Hivemind Brain/portfolio/assets/The-6-Skill-Marketers-Toolkit.pdf"

# ---------------------------------------------------------------- styles ----
def style(name, **kw):
    base = dict(fontName="AvenirNext", fontSize=10.4, leading=15.8, textColor=TEXT)
    base.update(kw)
    return ParagraphStyle(name, **base)

S = {
    "kicker_cover": style("kicker_cover", fontName="AvenirNext-Demi", fontSize=10.5,
                           textColor=SECONDARY, leading=13),
    "cover_title": style("cover_title", fontName="AvenirNext-Heavy", fontSize=54,
                          leading=56, textColor=DARK),
    "cover_sub": style("cover_sub", fontName="Bodoni-Italic", fontSize=15.5,
                        leading=22, textColor=colors.HexColor("#3F3F3F")),
    "cover_byline": style("cover_byline", fontName="AvenirNext-Demi", fontSize=11,
                           leading=15, textColor=DARK),
    "cover_byline_sub": style("cover_byline_sub", fontName="AvenirNext", fontSize=10,
                               leading=14, textColor=MUTED),

    "toc_kicker": style("toc_kicker", fontName="AvenirNext-Demi", fontSize=10,
                         textColor=SECONDARY, leading=13),
    "toc_h": style("toc_h", fontName="AvenirNext-Heavy", fontSize=30, leading=33,
                    textColor=DARK),
    "toc_num": style("toc_num", fontName="Bodoni-Bold", fontSize=19, leading=19,
                      textColor=WHITE, alignment=TA_CENTER),
    "toc_title": style("toc_title", fontName="AvenirNext-Bold", fontSize=13.5,
                        leading=17, textColor=DARK),
    "toc_teaser": style("toc_teaser", fontName="AvenirNext", fontSize=9.6,
                         leading=13.5, textColor=MUTED),

    "skill_kicker": style("skill_kicker", fontName="AvenirNext-Demi", fontSize=9,
                           textColor=colors.HexColor("#9A9A9A"), leading=11),
    "skill_title": style("skill_title", fontName="AvenirNext-Heavy", fontSize=32,
                          leading=34, textColor=DARK),
    "skill_sub": style("skill_sub", fontName="Bodoni-Italic", fontSize=13.5,
                        leading=18, textColor=colors.HexColor("#3F3F3F")),

    "subhead": style("subhead", fontName="AvenirNext-Bold", fontSize=12.5,
                      leading=16, textColor=DARK, spaceBefore=14, spaceAfter=7),
    "body": style("body", spaceAfter=8),
    "body_tight": style("body_tight", spaceAfter=4),
    "label_lead": style("label_lead", fontName="AvenirNext-Demi", fontSize=10.4,
                         leading=15.8, textColor=DARK, spaceAfter=6),
    "example_quote": style("example_quote", fontName="AvenirNext-Medium", fontSize=10.6,
                            leading=15.5, textColor=TEXT, spaceAfter=3, leftIndent=2),

    "pq": style("pq", fontName="Bodoni-Italic", fontSize=13.5, leading=19,
                textColor=DARK, spaceBefore=4, spaceAfter=4),

    "checklist_item": style("checklist_item", fontSize=10.2, leading=14.5,
                             textColor=TEXT),

    "closing_kicker": style("closing_kicker", fontName="AvenirNext-Demi", fontSize=10,
                             textColor=PRIMARY, alignment=TA_CENTER, leading=13),
    "closing_h": style("closing_h", fontName="Bodoni-Italic", fontSize=32, leading=40,
                        textColor=WHITE, alignment=TA_CENTER, spaceAfter=16),
    "closing_body": style("closing_body", fontName="AvenirNext", fontSize=11,
                           leading=17, textColor=colors.HexColor("#CBD8DC"),
                           alignment=TA_CENTER, spaceAfter=4),
    "closing_contact": style("closing_contact", fontName="AvenirNext-Bold", fontSize=12,
                              leading=18, textColor=PRIMARY, alignment=TA_CENTER),
}


# ------------------------------------------------------------- backgrounds --
def draw_cover_bg(c: pdfcanvas.Canvas, doc):
    c.saveState()
    c.setFillColor(NEUTRAL)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(PRIMARY)
    c.setFillAlpha(0.14)
    c.circle(PAGE_W - 0.5 * inch, PAGE_H - 0.9 * inch, 2.5 * inch, fill=1, stroke=0)
    c.setFillAlpha(1)
    # Big outline "6" as an editorial anchor, bottom-left, bleeding off the page
    c.setFont("Bodoni-Bold", 620)
    c.setFillColor(DARK)
    c.setFillAlpha(0.045)
    c.drawString(-1.55 * inch, -1.7 * inch, "6")
    c.setFillAlpha(1)
    seg_w = PAGE_W / 3.0
    bar_h = 0.16 * inch
    for i, col in enumerate([DARK, SECONDARY, PRIMARY]):
        c.setFillColor(col)
        c.rect(seg_w * i, 0, seg_w, bar_h, fill=1, stroke=0)
    c.restoreState()


def draw_toc_bg(c: pdfcanvas.Canvas, doc):
    c.saveState()
    c.setFillColor(WHITE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(PRIMARY)
    c.rect(0, PAGE_H - 0.07 * inch, PAGE_W, 0.07 * inch, fill=1, stroke=0)
    c.restoreState()


def make_skill_bg(number, accent):
    def _draw(c: pdfcanvas.Canvas, doc):
        c.saveState()
        c.setFillColor(WHITE)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        # thin top accent rule
        c.setFillColor(accent)
        c.rect(0, PAGE_H - 0.065 * inch, PAGE_W, 0.065 * inch, fill=1, stroke=0)
        # giant faint outline numeral, top-right, editorial watermark
        c.setFont("Bodoni-Bold", 260)
        c.setFillColor(DARK)
        c.setFillAlpha(0.035)
        c.drawRightString(PAGE_W - 0.15 * inch, PAGE_H - 2.55 * inch, str(number))
        c.setFillAlpha(1)
        # running header
        c.setFont("AvenirNext-Demi", 8)
        c.setFillColor(colors.HexColor("#B9B9B9"))
        c.drawString(MARGIN, PAGE_H - 0.46 * inch, "MARKETING SKILLS")
        c.setFillColor(accent)
        c.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.46 * inch, f"0{number} / 06")
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(MARGIN, PAGE_H - 0.56 * inch, PAGE_W - MARGIN, PAGE_H - 0.56 * inch)
        # footer
        c.setFont("AvenirNext", 8)
        c.setFillColor(MUTED)
        c.drawString(MARGIN, 0.5 * inch, "onlyonyi.com")
        c.drawRightString(PAGE_W - MARGIN, 0.5 * inch, f"Page {doc.page - 1}")
        c.restoreState()
    return _draw


def draw_closing_bg(c: pdfcanvas.Canvas, doc):
    c.saveState()
    c.setFillColor(DARK)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    cx, cy = PAGE_W / 2, PAGE_H / 2 + 1.3 * inch
    c.setFillColor(SECONDARY)
    for radius, alpha in [(2.9 * inch, 0.10), (2.2 * inch, 0.16), (1.5 * inch, 0.22)]:
        c.setFillAlpha(alpha)
        c.circle(cx, cy, radius, fill=1, stroke=0)
    c.setFillAlpha(1)
    seg_w = PAGE_W / 3.0
    bar_h = 0.14 * inch
    for i, col in enumerate([PRIMARY, SECONDARY, colors.HexColor("#3A5A68")]):
        c.setFillColor(col)
        c.rect(seg_w * i, PAGE_H - bar_h, seg_w, bar_h, fill=1, stroke=0)
    c.restoreState()


# --------------------------------------------------------------- helpers ----
def P(text, key="body"):
    return Paragraph(text, S[key])


def skill_header(number, title, sub):
    return [
        P("MARKETING SKILL", "skill_kicker"),
        Spacer(1, 4),
        P(title, "skill_title"),
        Spacer(1, 3),
        P(sub, "skill_sub"),
        Spacer(1, 14),
    ]


def pull_quote(text, accent):
    inner = Table([[P(text, "pq")]], colWidths=[PAGE_W - 2 * MARGIN - 0.28 * inch])
    inner.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBEFORE", (0, 0), (0, 0), 2.4, accent),
    ]))
    return inner


def checklist(items):
    rows = []
    for it in items:
        box = Table([[""]], colWidths=[0.16 * inch], rowHeights=[0.16 * inch])
        box.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1.1, DARK),
        ]))
        rows.append([box, P(it, "checklist_item")])
    t = Table(rows, colWidths=[0.3 * inch, PAGE_W - 2 * MARGIN - 0.3 * inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (1, 0), (1, -1), 0),
        ("LEFTPADDING", (1, 0), (1, -1), 10),
    ]))
    return t


def numbered(items):
    rows = []
    for i, it in enumerate(items, 1):
        rows.append([P(str(i), "label_lead"), P(it, "checklist_item")])
    t = Table(rows, colWidths=[0.28 * inch, PAGE_W - 2 * MARGIN - 0.28 * inch])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def sidebar(title, examples, why, accent, tint):
    flow = [P(f"<font color='{accent.hexval()}'><b>{title}</b></font>", "subhead")]
    for ex in examples:
        flow.append(P(f"&ldquo;{ex}&rdquo;", "example_quote"))
    flow.append(Spacer(1, 3))
    flow.append(P(f"<i>{why}</i>", "body_tight"))
    t = Table([[flow]], colWidths=[PAGE_W - 2 * MARGIN - 0.3 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), tint),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LINEBEFORE", (0, 0), (0, 0), 2.6, accent),
    ]))
    return t


# ------------------------------------------------------------------ build ---
doc = BaseDocTemplate(
    OUT_PATH, pagesize=letter,
    leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=MARGIN,
    title="The 6-Skill Marketer's Toolkit", author="Onyinye Ojukwu",
)

cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover",
                     leftPadding=1.05 * inch, rightPadding=1.0 * inch,
                     topPadding=1.5 * inch, bottomPadding=1.0 * inch)
toc_frame = Frame(0, 0, PAGE_W, PAGE_H, id="toc",
                   leftPadding=1.0 * inch, rightPadding=1.0 * inch,
                   topPadding=1.3 * inch, bottomPadding=1.0 * inch)
closing_frame = Frame(0, 0, PAGE_W, PAGE_H, id="closing",
                       leftPadding=1.0 * inch, rightPadding=1.0 * inch,
                       topPadding=3.3 * inch, bottomPadding=1.0 * inch)

templates = [
    PageTemplate(id="Cover", frames=[cover_frame], onPage=draw_cover_bg),
    PageTemplate(id="TOC", frames=[toc_frame], onPage=draw_toc_bg),
    PageTemplate(id="Closing", frames=[closing_frame], onPage=draw_closing_bg),
]
for i in range(1, 7):
    f = Frame(MARGIN, MARGIN, PAGE_W - 2 * MARGIN, PAGE_H - 1.65 * inch,
              id=f"skill{i}", topPadding=0.55 * inch)
    templates.append(PageTemplate(id=f"Skill{i}", frames=[f],
                                   onPage=make_skill_bg(i, ACCENTS[i - 1])))
doc.addPageTemplates(templates)

story = []

# ============================================================== COVER ======
story.append(P("A FREE RESOURCE FOR BUSINESS OWNERS", "kicker_cover"))
story.append(Spacer(1, 10))
story.append(P("The 6-Skill<br/>Marketer's<br/>Toolkit", "cover_title"))
story.append(Spacer(1, 14))
story.append(P(
    "Six practical frameworks for SEO, outreach, content, email, "
    "analytics, and CRM, pulled from real campaigns and real research, "
    "not recycled listicle advice.",
    "cover_sub"
))
story.append(Spacer(1, 30))
story.append(P("By Onyinye Ojukwu", "cover_byline"))
story.append(P("Digital Marketer &amp; Content Strategist", "cover_byline_sub"))

story.append(NextPageTemplate("TOC"))
story.append(PageBreak())

# ============================================================ CONTENTS =====
toc_data = [
    ("01", "SEO", "The 3-Layer Content Audit", DARK),
    ("02", "Outreach", "The Give-Before-You-Ask Sequence", SECONDARY),
    ("03", "Content Marketing", "One Idea, Five Formats", PRIMARY),
    ("04", "Email Marketing", "Subject Lines by Lifecycle Stage", DARK),
    ("05", "Analytics", "The 3-Number Weekly Check", SECONDARY),
    ("06", "CRM", "How to Truly See Your CRM", PRIMARY),
]
story.append(P("CONTENTS", "toc_kicker"))
story.append(Spacer(1, 6))
story.append(P("6 skills every business needs.", "toc_h"))
story.append(Spacer(1, 26))

for num, title, teaser, accent in toc_data:
    num_box = Table([[P(num, "toc_num")]], colWidths=[0.56 * inch], rowHeights=[0.5 * inch])
    num_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    text_block = [P(title, "toc_title"), P(teaser, "toc_teaser")]
    row = Table([[num_box, text_block]], colWidths=[0.7 * inch, None])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LINEBELOW", (0, 0), (-1, -1), 0.6, LINE),
    ]))
    story.append(row)
    story.append(Spacer(1, 16))

# ============================================================ SKILL 1 SEO ==
story.append(NextPageTemplate("Skill1"))
story.append(PageBreak())
story.extend(skill_header(1, "SEO", "The 3-Layer Content Audit"))

story.append(P(
    "Before writing anything new, audit what you already have. Most sites "
    "are sitting on pages that could rank with small fixes, not full "
    "rewrites.",
    "body"
))
story.append(P("<b>Layer 1, Technical:</b> Is it indexed? Check Google Search "
               "Console's Coverage report. Pages stuck in &ldquo;Discovered, not "
               "indexed&rdquo; usually have thin content or weak internal linking, "
               "not a Google penalty.", "body"))
story.append(P("<b>Layer 2, Relevance:</b> Does your title/H1 match what people "
               "actually search? Pull the exact &ldquo;People Also Ask&rdquo; questions "
               "and the &ldquo;Related searches&rdquo; at the bottom of the results "
               "page, and use those as your section headers, not your own "
               "guess at structure.", "body"))
story.append(P("<b>Layer 3, Authority:</b> Does the page link to 2-3 other "
               "relevant pages on your site, and get linked <i>to</i> by at "
               "least one other page? Orphan pages (zero internal links "
               "pointing in) almost never rank, regardless of content "
               "quality.", "body"))
story.append(Spacer(1, 6))
story.append(pull_quote(
    "Most SEO fails at Layer 2: you write what you want to say, not what "
    "people are searching for.", ACCENTS[0]))
story.append(Spacer(1, 4))

story.append(P("Keyword Research Without the Paid Tools", "subhead"))
story.append(P("You don't need Ahrefs or SEMrush to start:", "body_tight"))
story.append(numbered([
    "Type your topic into Google, don't hit enter yet, screenshot the "
    "autocomplete suggestions.",
    "Search it for real, scroll to &ldquo;People Also Ask&rdquo; and expand every "
    "question, they reveal sub-topics Google already knows people want.",
    "Scroll to the bottom, &ldquo;Related searches&rdquo; shows you the exact "
    "phrasing to use in your subheadings.",
    "Search &ldquo;[topic] reddit&rdquo;, the actual language real people use in "
    "threads is almost always more specific and more useful than what a "
    "keyword tool gives you.",
]))

story.append(P("On-Page Checklist", "subhead"))
story.append(P("Run this on every published page:", "body_tight"))
story.append(checklist([
    "Target keyword appears in the title, the H1, and the first 100 words",
    "URL is short and matches the topic (no dates, no stop words)",
    "At least one internal link in, one internal link out",
    "Image alt text describes the image, not stuffed with keywords",
    "Meta description is written to earn the click, not just describe the "
    "page (treat it like ad copy)",
]))

story.append(P("The Mistake That Wastes the Most Time", "subhead"))
story.append(P(
    "Chasing high-volume keywords with zero realistic shot at ranking. A "
    "site with no backlink history competing for a term that Forbes and "
    "NerdWallet rank for is a guaranteed loss. Instead, target the "
    "specific, lower-volume, &ldquo;long-tail&rdquo; version of the question: the "
    "exact phrase someone would type when they're closer to taking "
    "action, not just browsing.", "body"))

story.append(P("Weekly Rhythm", "subhead"))
story.append(P(
    "10 minutes, not a rabbit hole. Check GSC's Performance report, sort "
    "by impressions. Any page with high impressions but low clicks has a "
    "title/meta-description problem, not a content problem, that's your "
    "quickest win of the week.", "body"))

# ====================================================== SKILL 2 OUTREACH ===
story.append(NextPageTemplate("Skill2"))
story.append(PageBreak())
story.extend(skill_header(2, "Outreach", "The Give-Before-You-Ask Sequence"))

story.append(P(
    "A 3-touch framework that doesn't feel like spam, because it isn't "
    "structured like spam:", "body"))
story.append(P("<b>Touch 1:</b> Share something genuinely useful to them, a "
               "resource, a specific mention of their work, a real comment "
               "on something they posted. No ask attached.", "body"))
story.append(P("<b>Touch 2 (3-5 days later):</b> Reference touch 1 by name, "
               "then make one small, specific ask. Not &ldquo;let's hop on a "
               "call,&rdquo; but the smallest version of the ask that still moves "
               "things forward.", "body"))
story.append(P("<b>Touch 3 (if no reply, 5-7 days after touch 2):</b> A "
               "short, no-pressure close. &ldquo;No worries if now's not the "
               "time, just say the word and I'll leave it there.&rdquo;", "body"))
story.append(Spacer(1, 6))
story.append(pull_quote(
    "The mistake most people make: asking in touch 1. If your first "
    "message to a stranger contains a request, you've told them exactly "
    "why you're in their inbox, and it isn't for them.", ACCENTS[1]))
story.append(Spacer(1, 4))

story.append(P("Research Checklist", "subhead"))
story.append(P("5 minutes, before you write a single word:", "body_tight"))
story.append(checklist([
    "What did they post/publish/launch in the last 2 weeks? Reference "
    "something recent, not their bio.",
    "Do you have any real connection point (mutual contact, shared "
    "community, a specific piece of their work you actually used)? Lead "
    "with that, not with your company name.",
    "What do they actually want more of? (Visibility, revenue, "
    "credibility, time back?) Your ask should map to that, not to what's "
    "convenient for you.",
    "Have they said no to something similar publicly? Don't repeat a "
    "pitch they've already rejected in public.",
]))

story.append(P("Channel-Specific Openers", "subhead"))
story.append(P("<b>Cold email:</b> Subject line should read like it's from "
               "a person, not a campaign. &ldquo;Quick question about [specific "
               "thing]&rdquo; beats &ldquo;Partnership opportunity with [Your "
               "Company]&rdquo; every time, because the second one announces "
               "itself as outreach before it's even opened.", "body"))
story.append(P("<b>LinkedIn:</b> Comment on their post first, genuinely, "
               "before ever sending a connection request or DM. Cold "
               "LinkedIn requests with no prior interaction convert far "
               "worse than a warm one where you showed up in their "
               "comments first.", "body"))
story.append(P("<b>Cold DM:</b> Keep touch 1 under 3 sentences. DMs get "
               "skimmed on a phone, a long opener reads as a copy-paste "
               "template even when it isn't.", "body"))

story.append(P("Exact Follow-Up Timing", "subhead"))
story.append(checklist([
    "Touch 1 to Touch 2: 3-5 business days (not sooner, gives the value "
    "time to land, not so long they've forgotten who you are)",
    "Touch 2 to Touch 3: 5-7 business days",
    "After Touch 3 with no reply: stop. A 4th unsolicited message reads "
    "as pressure, not persistence.",
]))

story.append(P("Tracking Without Overbuilding", "subhead"))
story.append(P(
    "You don't need a CRM to run this well at small volume. A simple "
    "sheet with 4 columns is enough: Name, Touch 1 date, Touch 2 date, "
    "Status. The moment you're managing more than roughly 30 active "
    "threads at once is the moment to move this into an actual CRM.",
    "body"))

# =================================================== SKILL 3 CONTENT =======
story.append(NextPageTemplate("Skill3"))
story.append(PageBreak())
story.extend(skill_header(3, "Content Marketing", "One Idea, Five Formats"))

story.append(P(
    "Stop starting from a blank page for every platform. Take <b>one "
    "core idea</b> (a lesson, a stat, an opinion) and turn it into five "
    "things: a LinkedIn post, a tweet thread, an email, a short-form "
    "video script, and a carousel. You're not creating 5 ideas a week, "
    "you're reshaping 1.", "body"))

story.append(P("Worked Example", "subhead"))
story.append(P(
    "<b>The core idea:</b> &ldquo;Every welcome email I've ever seen with a "
    "50%+ open rate skipped the word 'welcome' in the subject line.&rdquo;",
    "body"))
story.append(checklist([
    "<b>LinkedIn post:</b> Open with the counterintuitive claim, walk "
    "through 2-3 real examples, close with a question to drive comments.",
    "<b>Tweet thread:</b> Tweet 1 is the claim alone, no context, built "
    "to make people stop scrolling. Tweets 2-5 unpack it.",
    "<b>Email:</b> Use the actual insight as your own subject line, "
    "prove the concept in the send itself.",
    "<b>Short-form video:</b> Hook in the first 2 seconds has to BE the "
    "claim, not a lead-up to it.",
    "<b>Carousel:</b> Slide 1 is the claim as a headline. Slides 2-4 are "
    "one example each. Final slide restates the takeaway as an action.",
]))
story.append(P(
    "Same idea, five formats, five different reasons someone would stop "
    "and engage with each one.", "body"))

story.append(P("Format-Specific Rules", "subhead"))
story.append(P("<b>LinkedIn:</b> The first line is the whole game, it's "
               "what shows before &ldquo;see more.&rdquo; If it doesn't work "
               "standalone, rewrite it before touching anything else.", "body"))
story.append(P("<b>Twitter/X threads:</b> Tweet 1 must work with zero "
               "context. Most threads fail because tweet 1 assumes the "
               "reader already cares.", "body"))
story.append(P("<b>Email:</b> Say the interesting thing early. There's no "
               "algorithm gatekeeping reach here, so the cost of burying "
               "the point is a reader who stops halfway.", "body"))
story.append(P("<b>Short-form video:</b> If you can't state the hook in "
               "under 3 seconds, the idea isn't sharp enough yet.", "body"))
story.append(P("<b>Carousels:</b> One idea per slide, not one idea per "
               "sentence. If a slide needs two sentences, it's actually "
               "two slides.", "body"))

story.append(P("Weekly Rhythm", "subhead"))
story.append(P(
    "Pick one idea a week, and build the full week's content from it. "
    "Batch by format, not by day, write all 5 LinkedIn posts in one "
    "sitting instead of one cold post a day.", "body"))

story.append(P("The Mistake That Makes Most People Quit Posting", "subhead"))
story.append(P(
    "Treating each platform as a separate content strategy that needs "
    "its own fresh ideas. That's 5x the creative load for the same "
    "output, and it's the single biggest reason people post consistently "
    "for 3 weeks and then stop.", "body"))

# ===================================================== SKILL 4 EMAIL =======
story.append(NextPageTemplate("Skill4"))
story.append(PageBreak())
story.extend(skill_header(4, "Email Marketing", "Subject Lines by Lifecycle Stage"))

story.append(P(
    "Generic subject line advice isn't wrong, but it's incomplete, "
    "because the right approach depends entirely on where the reader is "
    "in their relationship with you. Here's what's working, by stage:",
    "body"))
story.append(Spacer(1, 4))

story.append(sidebar(
    "Welcome Emails",
    ["You're in, [Name]. Here's what's next.",
     "Welcome. Let's start with something useful.",
     "Your account is ready. One thing to do first."],
    "Highest open rates of any email type (commonly 40-65%+ for "
    "high-intent triggers, against 15-25% for standard sends). People "
    "just took an action, they're primed to open.",
    ACCENTS[3], colors.HexColor("#FEF0E8")
))
story.append(Spacer(1, 10))
story.append(sidebar(
    "Cart Abandonment (&ldquo;Open Cart&rdquo;)",
    ["Where did you go?!",
     "Hey, you forgot something.",
     "The price dropped on something in your cart."],
    "Already opens at roughly 45% on average. First-name personalization "
    "lifts that further by around 22%, and including the word &ldquo;cart&rdquo; "
    "adds another ~10%.",
    ACCENTS[3], colors.HexColor("#E8F0F2")
))
story.append(Spacer(1, 10))
story.append(sidebar(
    "Win-Back (&ldquo;Closed Cart&rdquo; / Lapsed Customers)",
    ["Have you been seeing someone else?",
     "It's been a while, [Name]. Let's catch up on [new feature].",
     "Your opinion matters, help us improve."],
    "Curiosity beats a straight discount here. The gap needs to be "
    "specific enough to intrigue, vague enough that only opening "
    "resolves it.",
    ACCENTS[3], colors.HexColor("#FEF0E8")
))
story.append(Spacer(1, 10))
story.append(sidebar(
    "Regular Newsletters",
    ["We found something surprising in your data.",
     "Do we have this in common?",
     "3 things that changed our open rate this month."],
    "6-10 words, under 50 characters, wins consistently: roughly 12% "
    "higher opens, 75% higher clicks than longer subject lines.",
    ACCENTS[3], colors.HexColor("#E8F0F2")
))

story.append(P("Pre-Send Checklist", "subhead"))
story.append(checklist([
    "Would this make sense to someone with zero context, or does it "
    "only work if they remember your last email?",
    "Does the subject line's promise get paid off in the first two "
    "lines of the body?",
    "Is there a specific noun in it (a product, a number, a name), not "
    "just a vague benefit?",
    "Read it out loud. If it sounds like ad copy, soften it.",
]))

story.append(P("The Mistake That Costs You Long-Term", "subhead"))
story.append(P(
    "Curiosity only works once per broken promise. Clickbait that "
    "disappoints in the body doesn't just cost that reader's trust, it "
    "measurably hurts deliverability and spam complaints on the sends "
    "that follow. Every curiosity-gap subject line is a debt the email "
    "body has to repay immediately, not eventually.", "body"))

# =================================================== SKILL 5 ANALYTICS =====
story.append(NextPageTemplate("Skill5"))
story.append(PageBreak())
story.extend(skill_header(5, "Analytics", "The 3-Number Weekly Check"))

story.append(P(
    "Most people either ignore analytics entirely or fall into it for "
    "hours without a plan. Three numbers, checked weekly, catch problems "
    "early without turning into a rabbit hole:", "body"))
story.append(numbered([
    "<b>Google Search Console:</b> Average position for your top 5 "
    "pages, climbing or dropping?",
    "<b>Google Analytics:</b> Where your traffic is actually coming "
    "from, don't guess.",
    "<b>Google Analytics:</b> Your top exit page, that's your fix-it "
    "list for the week.",
]))

story.append(P("Why &ldquo;Average Position&rdquo; Is Easy to Misread", "subhead"))
story.append(P(
    "A page can rank #2 for one query and #47 for another, and Search "
    "Console will report an &ldquo;average position&rdquo; of 24.5 as if that "
    "means anything real. It gets worse as a page ranks for more "
    "queries: new, lower-ranking keywords can drag the average down even "
    "while your best keywords are climbing.", "body"))
story.append(pull_quote(
    "Never read average position at the page level alone. Filter by "
    "individual query first, then check that query's position over "
    "time.", ACCENTS[4]))
story.append(Spacer(1, 8))

story.append(P("The GA4 Engagement Rate Trap", "subhead"))
story.append(P(
    "If you learned analytics on Universal Analytics, unlearn &ldquo;bounce "
    "rate&rdquo; as your main quality signal. GA4 replaced it with engagement "
    "rate, and it isn't the same metric renamed.", "body"))
story.append(checklist([
    "A session counts as <b>engaged</b> if it fires a conversion event, "
    "lasts longer than 10 seconds, or generates a second pageview.",
    "Bounce rate in GA4 is simply 100% minus engagement rate, a "
    "byproduct, not its own measurement.",
    "This makes GA4 more forgiving: someone who reads for 12 seconds "
    "and leaves now counts as &ldquo;engaged.&rdquo;",
]))

story.append(P("The Direct Traffic Trap", "subhead"))
story.append(P(
    "If &ldquo;Direct&rdquo; suddenly becomes your top channel, don't conclude "
    "people are typing your URL from memory. GA4 dumps any session it "
    "can't confidently attribute into Direct:", "body"))
story.append(checklist([
    "Untagged email campaigns (no UTM parameters) can inject thousands "
    "of sessions into Direct overnight.",
    "Links shared through WhatsApp, Slack, or iMessage typically strip "
    "referrer data before the click registers.",
    "Misconfigured redirects can strip the parameters that would show "
    "the real source.",
    "Bots deliberately obscure their origin, some of the inflation may "
    "not be human traffic at all.",
]))

story.append(P("The Mistake That Wastes the Most Analysis Time", "subhead"))
story.append(P(
    "Treating every number as equally trustworthy. Average position, "
    "Direct traffic, and engagement rate all have known blind spots "
    "baked into how they're calculated. The skill is knowing which ones "
    "lie by default, and checking the query or campaign level before "
    "making a decision off the summary number.", "body"))

# ========================================================= SKILL 6 CRM =====
story.append(NextPageTemplate("Skill6"))
story.append(PageBreak())
story.extend(skill_header(6, "CRM", "How to Truly See Your CRM"))

story.append(P(
    "The surface-level take is &ldquo;tag your contacts by temperature.&rdquo; "
    "The real insight is deeper: <b>most CRMs fail not because the tool "
    "is bad, but because of who the data entry actually benefits.</b>",
    "body"))
story.append(P(
    "60-70% of CRM failures are adoption failures, not platform failures "
    "(Forrester puts it at 70%). When a rep logs a call that mainly "
    "feeds someone else's dashboard and gives them nothing back, "
    "skipping it isn't laziness, it's a rational read of a bad trade.",
    "body"))

story.append(P("Platform by Platform", "subhead"))
story.append(P("<b>Salesforce</b> is genuinely powerful, but every custom "
               "field and approval you bolt on adds friction that "
               "compounds, teams often need paid consultants for basic "
               "changes. Adoption often lands around 40-50% at 90 days "
               "without real change management.", "body"))
story.append(P("<b>HubSpot</b> wins on adoption (often 80%+ in month one) "
               "because the interface leads with activities, not forms. "
               "The tradeoff: advanced features and modules get expensive "
               "fast as you scale.", "body"))
story.append(P("<b>Lark</b> folds contact/deal tracking into the same "
               "workspace as chat, docs, and calendar. For small or "
               "remote-first teams, data entry often happens as a "
               "byproduct of work already being done.", "body"))

story.append(P("Building a Temperature System That Sticks", "subhead"))
story.append(checklist([
    "<b>Avoid overcomplication.</b> Scoring systems with a dozen "
    "weighted variables get abandoned within a month. Start with 2-3 "
    "signals that actually predict a close.",
    "<b>Watch for stale signals.</b> A contact tagged &ldquo;warm&rdquo; off a "
    "6-month-old newsletter open isn't warm, it's cold with extra "
    "steps, and reaching out that way reads as a tone mismatch.",
]))

story.append(pull_quote(
    "Before you pick a temperature system, ask what the CRM gives back "
    "to the person entering the data: a clear next action, or a "
    "reminder that saves them an awkward follow-up moment. Tag on top "
    "of that, and it sticks. Tag without it, and it's dead within a "
    "month.", ACCENTS[5]))
story.append(Spacer(1, 10))

story.append(P("A Hygiene Cadence That Survives Real Work", "subhead"))
story.append(checklist([
    "<b>Daily:</b> Log the call/email while it's still in short-term "
    "memory.",
    "<b>Weekly:</b> Scan for deals with no activity in 7+ days.",
    "<b>Monthly:</b> Audit for duplicate contacts and dead stages.",
    "<b>Quarterly:</b> A full field audit, is every custom field still "
    "earning its place on the form?",
]))

story.append(P("The Mistake That Undoes Everything Else", "subhead"))
story.append(P(
    "Treating hygiene as a punishment instead of ownership. Teams that "
    "frame CRM discipline as a personal advantage for the rep, not a "
    "compliance requirement for management, are the ones where it "
    "actually sticks.", "body"))

# ============================================================ CLOSING ======
story.append(NextPageTemplate("Closing"))
story.append(PageBreak())
story.append(P("A NOTE FROM ME", "closing_kicker"))
story.append(Spacer(1, 14))
story.append(P("&ldquo;That's the toolkit.&rdquo;", "closing_h"))
story.append(P(
    "Six frameworks, pulled from real campaigns and real research, not "
    "recycled listicle advice.", "closing_body"))
story.append(P(
    "If you want help putting any of these to work for your team, "
    "let's talk.", "closing_body"))
story.append(Spacer(1, 20))
story.append(P("onlyonyi.com &nbsp;&middot;&nbsp; onyinyeojukwu11@gmail.com", "closing_contact"))

doc.build(story)
print("done:", OUT_PATH)
