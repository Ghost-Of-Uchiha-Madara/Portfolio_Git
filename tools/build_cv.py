"""Build Sankara Pandi's one-page CV.

Kept to real text in a single column so applicant tracking systems can parse it;
the only colour is the portfolio's amber, used on rules and section headings so
the CV and the site read as one set. Content mirrors the portfolio exactly —
three years shipping, DML's client titles described by role only, and no test
counts anywhere.
"""

import pathlib

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
)

OUT = pathlib.Path(r"D:\GameDev\Version Control\Portfolio_Git\assets\cv\Sankara-Pandi-CV.pdf")
OUT.parent.mkdir(parents=True, exist_ok=True)

INK = colors.HexColor("#1A1A1E")
BODY = colors.HexColor("#33333A")
MUTED = colors.HexColor("#6B6B75")
ACCENT = colors.HexColor("#B77400")   # darkened amber: readable on white
RULE = colors.HexColor("#D8D8DE")

S = {
    "name": ParagraphStyle(
        "name", fontName="Helvetica-Bold", fontSize=21, leading=24,
        textColor=INK, spaceAfter=1,
    ),
    "role": ParagraphStyle(
        "role", fontName="Helvetica", fontSize=10.5, leading=13,
        textColor=ACCENT, spaceAfter=4,
    ),
    "contact": ParagraphStyle(
        "contact", fontName="Helvetica", fontSize=8.3, leading=11.5,
        textColor=MUTED,
    ),
    "h2": ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=9, leading=11,
        textColor=ACCENT, spaceBefore=0, spaceAfter=3,
    ),
    "summary": ParagraphStyle(
        "summary", fontName="Helvetica", fontSize=9.2, leading=13.0,
        textColor=BODY, alignment=TA_JUSTIFY,
    ),
    "jobtitle": ParagraphStyle(
        "jobtitle", fontName="Helvetica-Bold", fontSize=9.7, leading=12,
        textColor=INK,
    ),
    "meta": ParagraphStyle(
        "meta", fontName="Helvetica-Oblique", fontSize=8.3, leading=11,
        textColor=MUTED, spaceAfter=2,
    ),
    "bullet": ParagraphStyle(
        "bullet", fontName="Helvetica", fontSize=9.0, leading=12.4,
        textColor=BODY, leftIndent=9, bulletIndent=0, spaceAfter=1.2,
    ),
    "proj": ParagraphStyle(
        "proj", fontName="Helvetica", fontSize=8.9, leading=12,
        textColor=BODY, spaceAfter=1,
    ),
    "skill": ParagraphStyle(
        "skill", fontName="Helvetica", fontSize=8.7, leading=12,
        textColor=BODY, leftIndent=52, firstLineIndent=-52, spaceAfter=1.5,
    ),
}


def rule(space_before=5, space_after=4.5):
    return HRFlowable(width="100%", thickness=0.7, color=RULE,
                      spaceBefore=space_before, spaceAfter=space_after)


def section(title):
    return [rule(), Paragraph(title.upper(), S["h2"])]


def job(title, org, dates, bullets):
    flow = [
        Paragraph(title, S["jobtitle"]),
        Paragraph(f"{org} &nbsp;&middot;&nbsp; {dates}", S["meta"]),
    ]
    flow += [Paragraph(b, S["bullet"], bulletText="\u2022") for b in bullets]
    flow.append(Spacer(1, 4.5))
    return KeepTogether(flow)


def project(name, stack, text):
    return KeepTogether([
        Paragraph(f'<b>{name}</b> &nbsp;<font color="#6B6B75" size="8">{stack}</font>',
                  S["proj"]),
        Paragraph(text, S["bullet"]),
        Spacer(1, 4),
    ])


story = []

# ---- Header ---------------------------------------------------------------
story.append(Paragraph("Sankara Pandi", S["name"]))
story.append(Paragraph("Unity Developer &mdash; Gameplay &amp; Systems", S["role"]))
story.append(Paragraph(
    "Coimbatore, Tamil Nadu, India &nbsp;&middot;&nbsp; "
    "sankar.gamedev@gmail.com &nbsp;&middot;&nbsp; +91 73394 05631<br/>"
    '<a href="https://www.linkedin.com/in/sankar-gamedev/" color="#B77400">'
    "linkedin.com/in/sankar-gamedev</a> &nbsp;&middot;&nbsp; "
    '<a href="https://github.com/Ghost-Of-Uchiha-Madara" color="#B77400">'
    "github.com/Ghost-Of-Uchiha-Madara</a> &nbsp;&middot;&nbsp; "
    '<a href="https://ghost-of-uchiha-madara.github.io/Portfolio_Git/" color="#B77400">'
    "<b>Portfolio &amp; case studies</b></a>",
    S["contact"]))

story += section("Profile")
story.append(Paragraph(
    "Unity developer with three years shipping iGaming and hyper-casual titles in "
    "production. I build the systems underneath games &mdash; physics, state, "
    "progression &mdash; and the live backends that keep them running. Comfortable "
    "owning a feature from prototype to release, and equally at home in Godot. "
    "Mechatronics background, which is where the rigid-body and integration maths "
    "behind the physics work comes from.",
    S["summary"]))

# ---- Experience -----------------------------------------------------------
story += section("Experience")
story.append(job(
    "Game Developer", "DML, Coimbatore", "Sep 2023 &ndash; Present",
    [
        "Ship iGaming and hyper-casual titles in Unity and Godot, from prototype "
        "through to release.",
        "Build UI-driven game systems &mdash; state machines, reward and progression "
        "logic, and the data layers behind them.",
        "Own gameplay features end to end, working to production deadlines alongside "
        "design and art.",
    ]))
story.append(job(
    "Game Designer", "Arcadix, Remote", "Apr 2023 &ndash; Jul 2023",
    [
        "Designed level layouts and player-progression systems with the design team.",
        "Implemented gameplay mechanics and environmental storytelling beats.",
    ]))
story.append(job(
    "3D Designer", "3dezine, Remote", "Sep 2022 &ndash; Mar 2023",
    [
        "Produced 3D assets for clients across gaming, advertising and architecture.",
        "Ran several projects in parallel against fixed client deadlines.",
    ]))

# ---- Projects -------------------------------------------------------------
story += section("Selected Projects")
story.append(project(
    "Desk Strike", "Unity 6 &middot; URP &middot; C# &middot; Shipped on CrazyGames",
    "Turn-based 3D physics duel for mobile web. A single drag sets aim, power and "
    "contact point at once; the aim line draws the whole predicted path, integrated "
    "against the real physics rather than approximated. Five pens with genuinely "
    "different mass, grip and curve response make pen choice the strategic layer. "
    "Solo developer, ~120 C# scripts."))
story.append(project(
    "Office Trip", "Unity &middot; Multiplayer &middot; PlayFab &middot; Unity Gaming Services",
    "Networked social-deduction game built on a complete live-service backend rather "
    "than a prototype stub: authentication, cloud save, a soft-currency economy, "
    "battle pass, leaderboards, remote config and analytics all sit behind one "
    "service layer the gameplay code calls without knowing who answers. "
    "~665 C# scripts across modular assembly definitions."))

story.append(project(
    "Also built",
    "Godot 4 &middot; Unity AR &middot; Blender",
    "A multiplayer space shooter on Godot's high-level networking API; neAR, an "
    "augmented-reality Unity app using native camera access and on-device tracking; "
    "and character and prop work in Blender, retopologised and textured for real-time "
    "budgets. Case studies for each are on the portfolio."))

# ---- Skills ---------------------------------------------------------------
story += section("Technical Skills")
for label, items in [
    ("Engines", "Unity 6 (URP), Godot 4, Unreal 5"),
    ("Languages", "C#, GDScript, HLSL basics, HTML / CSS / JavaScript"),
    ("Gameplay", "Rigid-body physics, state machines, Input System, Cinemachine, "
                 "opponent AI, progression systems"),
    ("Live services", "PlayFab, Unity Gaming Services, Cloud Save, Economy, "
                      "Leaderboards, Remote Config"),
    ("Practice", "Automated testing, assembly definitions, Git, profiling, "
                 "editor tooling"),
    ("Art", "Blender, Aseprite, Photoshop"),
]:
    story.append(Paragraph(f'<b>{label}</b>&nbsp;&nbsp;&nbsp;{items}', S["skill"]))

# ---- Education ------------------------------------------------------------
story += section("Education")
story.append(Paragraph("B.E. Mechatronics Engineering", S["jobtitle"]))
story.append(Paragraph(
    "Park College of Engineering and Technology, Coimbatore &nbsp;&middot;&nbsp; 2020 &ndash; 2024",
    S["meta"]))
story.append(Spacer(1, 2.5))
story.append(Paragraph("Higher Secondary Certificate", S["jobtitle"]))
story.append(Paragraph("OVC Higher Secondary School &nbsp;&middot;&nbsp; 2018 &ndash; 2020",
                       S["meta"]))

doc = BaseDocTemplate(
    str(OUT), pagesize=A4,
    leftMargin=16 * mm, rightMargin=16 * mm,
    topMargin=14 * mm, bottomMargin=11 * mm,
    title="Sankara Pandi - Unity Developer - CV",
    author="Sankara Pandi",
    subject="Curriculum Vitae",
)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
doc.addPageTemplates([PageTemplate(id="cv", frames=[frame])])
doc.build(story)

print("written:", OUT, f"{OUT.stat().st_size // 1024} KB")
