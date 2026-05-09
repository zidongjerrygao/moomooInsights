"""
Seed the moomoo-site database with:
  1. Admin user: admin@moomoo.com / admin123
  2. SG Market Brief article (from WorkBuddy)
  3. McDonald's Q1 2026 earnings review article
  4. MCD company + earnings data
Run: python backend/seed.py  (from moomoo-site/ root)
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from models import init_db, SessionLocal, User, Article, Company, EarningsRelease
from auth import hash_password
from datetime import datetime

MCD_ARTICLE_HTML = """
<div style="background:linear-gradient(135deg,#1a1f3c 0%,#252b4a 100%);border-radius:12px;padding:32px;margin-bottom:32px;color:white;">
  <div style="font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#ff6900;margin-bottom:12px;">EARNINGS REVIEW · Q1 2026</div>
  <h1 style="font-size:28px;font-weight:800;line-height:1.3;margin-bottom:12px;">McDonald's Q1 2026: EPS Beat Masks Deepening Same-Store Sales Concern</h1>
  <p style="opacity:0.8;font-size:15px;line-height:1.6;">Revenue miss + flat US comp + China softness force a guidance cut. Here's what the golden arches revealed about global consumer health.</p>
</div>

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:32px;">
  <div style="background:white;border:1.5px solid #e5e7eb;border-radius:10px;padding:20px;text-align:center;">
    <div style="font-size:11px;color:#6b7280;text-transform:uppercase;font-weight:700;margin-bottom:6px;">EPS (Reported)</div>
    <div style="font-size:28px;font-weight:800;color:#1a1f3c;">$2.70</div>
    <div style="font-size:13px;color:#16a34a;font-weight:600;">▲ vs $2.65 est. (+1.9%)</div>
  </div>
  <div style="background:white;border:1.5px solid #e5e7eb;border-radius:10px;padding:20px;text-align:center;">
    <div style="font-size:11px;color:#6b7280;text-transform:uppercase;font-weight:700;margin-bottom:6px;">Revenue</div>
    <div style="font-size:28px;font-weight:800;color:#1a1f3c;">$6.12B</div>
    <div style="font-size:13px;color:#dc2626;font-weight:600;">▼ vs $6.18B est. (-1.0%)</div>
  </div>
  <div style="background:white;border:1.5px solid #e5e7eb;border-radius:10px;padding:20px;text-align:center;">
    <div style="font-size:11px;color:#6b7280;text-transform:uppercase;font-weight:700;margin-bottom:6px;">US Same-Store Sales</div>
    <div style="font-size:28px;font-weight:800;color:#1a1f3c;">0.0%</div>
    <div style="font-size:13px;color:#dc2626;font-weight:600;">▼ vs +0.8% est.</div>
  </div>
</div>

<h2 style="font-size:20px;font-weight:800;margin-bottom:12px;">The Headline Result</h2>
<p style="font-size:16px;line-height:1.8;margin-bottom:20px;">
McDonald's delivered a technically positive Q1 2026, reporting adjusted EPS of $2.70 against the Street's $2.65 estimate — a 1.9% beat that marks a fourth consecutive quarter of per-share earnings growth. Revenue of $6.12 billion grew 1.2% year-over-year, driven by systemwide sales expansion across International Operated Markets (IOM) and disciplined cost management. But the beat at the bottom line was hard-fought: the company missed its own implied revenue target by roughly $60 million, and the headline EPS figure owed more to share buybacks and margin discipline than any genuine demand acceleration.
</p>

<h2 style="font-size:20px;font-weight:800;margin-bottom:12px;">What's Driving the Numbers</h2>
<p style="font-size:16px;line-height:1.8;margin-bottom:20px;">
The segment breakdown tells a more complicated story than the EPS line suggests. In the US — McDonald's largest and highest-margin market — comparable sales were exactly flat at 0.0% against a consensus expectation of +0.8%, marking the second consecutive quarter of domestic comp stagnation. The IOM segment (primarily Western Europe) showed resilience with +0.6% comps and revenue of $1.94 billion (+2.8% YoY), benefiting from menu innovation and improving consumer sentiment in the UK and France. The real drag came from the International Developmental Licensed segment (IDL), which covers China and key Asian markets: comps fell 2.3%, reflecting ongoing weakness in Chinese consumer spending that has now persisted for six quarters. Management attributed the softness to "macro uncertainty and value-seeking behavior," code for consumers trading down or eating at home. The stock reacted with a modest -0.8% move the day after earnings — a muted response that suggests the market had already priced in some disappointment.
</p>

<h2 style="font-size:20px;font-weight:800;margin-bottom:12px;">Guidance Cut and the Forward View</h2>
<p style="font-size:16px;line-height:1.8;margin-bottom:20px;">
The most significant development of the quarter was the guidance revision: McDonald's lowered its full-year global same-store sales growth outlook to 1.5%–3.0% from its prior 2.5%–4.0% range. This is a meaningful step-down that signals management's loss of confidence in a near-term demand recovery, particularly in the US and China. The company is leaning heavily on its "Best Value in QSR" positioning — expanding value meals, $5 bundles, and digital loyalty promotions — to stabilize traffic, but margin headwinds from promotional spend will likely offset some of the benefit. For investors, McDonald's remains a cash-generative, dividend-growing franchise with unmatched global scale, but the re-rating story of 2024–2025 has clearly stalled. The next catalyst to watch is Q2 US comps: a return to positive territory would confirm the value strategy is working; a second consecutive flat-or-negative print would raise structural questions about the brand's premium positioning in a value-obsessed environment.
</p>

<div style="background:#fff7f0;border:1px solid #fed7aa;border-radius:10px;padding:20px;margin:24px 0;">
  <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.8px;color:#92400e;margin-bottom:8px;">Moomoo Insights Takeaway</div>
  <p style="font-size:15px;color:#78350f;line-height:1.7;margin:0;">
    <strong>Mixed quarter with a guidance cut.</strong> EPS beat on cost discipline and buybacks, not demand. US same-store sales flat, China deteriorating. Guidance lowered to 1.5%–3.0% SSS growth. Watch Q2 domestic comps as the real test of the value strategy. Hold with a cautious near-term outlook.
  </p>
</div>

<div style="margin-top:32px;">
  <h3 style="font-size:16px;font-weight:700;margin-bottom:16px;">Segment Performance Summary</h3>
  <table style="width:100%;border-collapse:collapse;font-size:14px;">
    <thead>
      <tr style="background:#f9fafb;">
        <th style="text-align:left;padding:10px 14px;border-bottom:2px solid #e5e7eb;font-size:12px;text-transform:uppercase;color:#6b7280;">Segment</th>
        <th style="text-align:right;padding:10px 14px;border-bottom:2px solid #e5e7eb;font-size:12px;text-transform:uppercase;color:#6b7280;">Revenue</th>
        <th style="text-align:right;padding:10px 14px;border-bottom:2px solid #e5e7eb;font-size:12px;text-transform:uppercase;color:#6b7280;">YoY</th>
        <th style="text-align:right;padding:10px 14px;border-bottom:2px solid #e5e7eb;font-size:12px;text-transform:uppercase;color:#6b7280;">Same-Store Sales</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:600;">US</td>
        <td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;text-align:right;">$2.58B</td>
        <td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;text-align:right;color:#16a34a;">+0.7%</td>
        <td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;text-align:right;color:#dc2626;">0.0%</td>
      </tr>
      <tr>
        <td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:600;">International Operated (IOM)</td>
        <td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;text-align:right;">$1.94B</td>
        <td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;text-align:right;color:#16a34a;">+2.8%</td>
        <td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;text-align:right;color:#16a34a;">+0.6%</td>
      </tr>
      <tr>
        <td style="padding:12px 14px;font-weight:600;">International Dev. Licensed (IDL)</td>
        <td style="padding:12px 14px;text-align:right;">$1.60B</td>
        <td style="padding:12px 14px;text-align:right;color:#16a34a;">+1.5%</td>
        <td style="padding:12px 14px;text-align:right;color:#dc2626;">-2.3%</td>
      </tr>
    </tbody>
  </table>
</div>
"""

SG_MARKET_BRIEF_PATH = r"C:\Users\jerrygao\WorkBuddy\20260427094716\SG_Market_Brief_20260427.html"


def read_sg_brief():
    with open(SG_MARKET_BRIEF_PATH, "r", encoding="utf-8") as f:
        raw = f.read()
    # Extract just the body content between <body> tags
    import re
    match = re.search(r"<body[^>]*>(.*)</body>", raw, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else raw


def main():
    init_db()
    db = SessionLocal()

    # ── Admin user ────────────────────────────────────────────────────────────
    existing = db.query(User).filter(User.email == "admin@moomoo.com").first()
    if not existing:
        admin = User(
            email="admin@moomoo.com",
            password_hash=hash_password("admin123"),
            display_name="Moomoo Admin",
            is_admin=True,
        )
        db.add(admin)
        db.commit()
        print("✓ Admin user created: admin@moomoo.com / admin123")
    else:
        print("  Admin user already exists")

    # ── SG Market Brief ───────────────────────────────────────────────────────
    sg_slug = "sg-market-brief-april-2026"
    if not db.query(Article).filter(Article.slug == sg_slug).first():
        try:
            content = read_sg_brief()
            brief = Article(
                title="SG Market Brief — April 2026",
                slug=sg_slug,
                excerpt="Singapore equities navigating a complex macro backdrop: STI momentum, Fed rate path uncertainty, and sector rotation opportunities heading into May.",
                content_html=content,
                tags=["Singapore", "STI", "Market Brief", "April 2026"],
                category="SG Market",
                author="Moomoo Insights",
                published=True,
                featured=False,
            )
            db.add(brief)
            db.commit()
            print("✓ SG Market Brief article seeded")
        except Exception as e:
            print(f"  SG Market Brief skipped: {e}")
    else:
        print("  SG Market Brief already exists")

    # ── MCD Earnings Review ───────────────────────────────────────────────────
    mcd_slug = "mcdonalds-q1-2026-earnings-review"
    if not db.query(Article).filter(Article.slug == mcd_slug).first():
        mcd = Article(
            title="McDonald's Q1 2026: EPS Beat Masks Deepening Same-Store Sales Concern",
            slug=mcd_slug,
            excerpt="Revenue miss, flat US comps, and a China slowdown force a full-year guidance cut. Moomoo Insights breaks down what the golden arches reveal about global consumer health.",
            content_html=MCD_ARTICLE_HTML,
            tags=["Earnings", "MCD", "Q1 2026", "Consumer", "McDonald's"],
            category="Earnings",
            author="Moomoo Insights",
            published=True,
            featured=True,
        )
        db.add(mcd)
        db.commit()
        print("✓ MCD Q1 2026 earnings review article seeded (featured)")
    else:
        print("  MCD article already exists")

    # ── MCD Company + Earnings in this DB ────────────────────────────────────
    mcd_co = db.query(Company).filter(Company.ticker == "MCD").first()
    if not mcd_co:
        mcd_co = Company(ticker="MCD", name="McDonald's", sector="Consumer Disc.", weight_pct=0.62)
        db.add(mcd_co)
        db.commit()

    if not db.query(EarningsRelease).filter(
        EarningsRelease.company_id == mcd_co.id,
        EarningsRelease.fiscal_quarter == "Q1 2026"
    ).first():
        er = EarningsRelease(
            company_id=mcd_co.id,
            report_date="2026-04-28",
            fiscal_quarter="Q1 2026",
            eps_actual=2.70,
            eps_estimate=2.65,
            eps_surprise_pct=1.89,
            revenue_actual=6_120_000_000,
            revenue_estimate=6_180_000_000,
            revenue_surprise_pct=-0.97,
            stock_price_before=296.00,
            stock_price_after=293.50,
            stock_reaction_pct=-0.84,
            guidance="Lowered full-year SSS guidance to 1.5%–3.0% (from 2.5%–4.0%). US consumer under pressure, China IDL segment -2.3% SSS.",
            is_manual_override=True,
        )
        db.add(er)
        db.commit()
        print("✓ MCD Q1 2026 earnings record seeded")
    else:
        print("  MCD earnings already exist")

    db.close()
    print("\nDone. Run: uvicorn backend.main:app --reload --port 8001")


if __name__ == "__main__":
    main()
