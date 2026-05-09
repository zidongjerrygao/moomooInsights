import sys
sys.path.insert(0, r"C:\Users\jerrygao\moomoo-site\backend")
from models import init_db, get_db, Article
from datetime import datetime

init_db()
db = next(get_db())

content_html = """
<div class="brief-meta">Macro Strategy &middot; May 2026</div>

<div class="brief-lead">
  Charles Dickens gave the world Mr. Micawber's rule in 1850: spend a halfpenny less than you earn and the result is happiness; a halfpenny more, the result is misery. The United States federal government has been choosing misery for 24 consecutive years — and for the first time in modern history, the annual interest bill on that misery has just eclipsed the entire defense budget.
</div>

<div class="brief-h3">The Setup: Bonds Are Forgiving; Math Is Not</div>

<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  The consensus view holds that the US fiscal situation is serious but manageable — that the dollar's reserve currency status provides a buffer, that growth will outpace debt over time, and that politicians will act before a genuine crisis forces their hand. This view has been correct for decades. The problem is that the arithmetic underlying it has quietly and significantly deteriorated.
</p>

<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  In fiscal year 2025, net interest payments on the federal debt reached an estimated $952 billion — surpassing defense spending of $922 billion for the first time since the post-WWII demobilization era. This is not a rounding error or a technical accounting quirk. It reflects 20 months of 4%-plus policy rates colliding with $36 trillion in accumulated borrowing. The interest clock does not stop when the Fed pauses.
</p>

<div class="chart-block">
  <div class="chart-title">Where the Money Goes — Federal Spending FY2025 ($ billions)</div>
  <div class="chart-subtitle">Net interest has overtaken defense for the first time since WWII-era demobilization</div>
  <div class="bar-chart">
    <div class="bar-row">
      <div class="bar-label">Social Security</div>
      <div class="bar-track"><div class="bar-fill" style="width:100%"><span class="bar-val">$1,407B</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">Medicare</div>
      <div class="bar-track"><div class="bar-fill" style="width:62%"><span class="bar-val">$869B</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;color:var(--orange);">Net Interest</div>
      <div class="bar-track"><div class="bar-fill" style="width:68%;background:var(--orange)"><span class="bar-val">$952B</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">Defense</div>
      <div class="bar-track"><div class="bar-fill" style="width:66%"><span class="bar-val">$922B</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">Medicaid</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:44%"><span class="bar-val">$618B</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">Other Discretionary</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:48%"><span class="bar-val">$672B</span></div></div>
    </div>
  </div>
  <div class="chart-note">Sources: Congressional Budget Office, Office of Management and Budget. FY2025 estimates.</div>
</div>

<div class="brief-h3">The Compound Problem</div>

<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  Four data points capture the structural nature of what's happening. First, net interest now consumes approximately 19 cents of every dollar of federal revenue — up from 8 cents a decade ago. At current trajectory, the CBO projects this ratio reaches 24 cents by 2030. Second, the primary deficit (spending minus interest) is roughly $960 billion, meaning the US is not merely paying interest on past borrowing — it is adding to principal at a rate that compounds the interest burden forward. Third, the CBO baseline — which already assumes TCJA provisions expire — shows debt reaching 156% of GDP by 2035. If current tax cut legislation extends in full, add another 15-20 percentage points. Fourth, the Social Security trust fund exhaustion date of 2033 represents an automatic $350 billion annual shortfall that no current legislative framework resolves.
</p>

<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  The bull case on fiscal sustainability rests on nominal GDP growth outpacing the average interest rate on debt — what economists call the "r &lt; g" condition. From 2012 to 2021, near-zero rates held the average cost of outstanding debt well below GDP growth and the condition was satisfied. It is no longer satisfied. The weighted average interest rate on federal debt has risen from 1.6% in 2021 to approximately 3.3% today, and continues rising as cheap pandemic-era debt matures and refinances at current rates. By 2027, the average cost of the entire debt stack will likely exceed 4%.
</p>

<div class="chart-block">
  <div class="chart-title">Federal Debt as % of GDP — A 25-Year Arc</div>
  <div class="chart-subtitle">Debt stabilized briefly after 2020 then resumed climbing; CBO projects a steep new leg higher by 2035</div>
  <div class="bar-chart">
    <div class="bar-row">
      <div class="bar-label">2000</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:35%"><span class="bar-val">55%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">2008</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:44%"><span class="bar-val">68%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">2012</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:64%"><span class="bar-val">100%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">2019</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:69%"><span class="bar-val">107%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">2020</div>
      <div class="bar-track"><div class="bar-fill" style="width:82%"><span class="bar-val">128%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">2025</div>
      <div class="bar-track"><div class="bar-fill" style="width:80%"><span class="bar-val">124%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;color:var(--orange);">2035 (CBO proj.)</div>
      <div class="bar-track"><div class="bar-fill" style="width:100%;background:var(--orange)"><span class="bar-val">156%</span></div></div>
    </div>
  </div>
  <div class="chart-note">Sources: Federal Reserve, Congressional Budget Office May 2025 baseline. 2035 assumes TCJA expiration; TCJA extension adds 15–20 ppts.</div>
</div>

<div class="brief-h3">What the Market Is — and Isn't — Pricing</div>

<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  Ten-year Treasury yields at 4.35% embed a real yield of approximately 2.1% — historically elevated for a reserve currency issuer, but not at levels that signal imminent crisis. The yield curve has steepened roughly 80 basis points since the Fed began cutting, suggesting the market is quietly demanding a term premium for fiscal risk that policymakers have not yet acknowledged publicly. Foreign official holdings of Treasuries have fallen from 33% to 23% of total outstanding over the past decade, as central banks from China to Saudi Arabia have diversified reserves. This is a slowly rising tide, not a wave.
</p>

<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  Equity markets have been largely indifferent, which is understandable — equities are real assets with some inflation protection, and corporate balance sheets carry no direct obligation for sovereign debt. But equities are not immune to a scenario where fiscal crowding-out forces long rates higher regardless of Fed policy, or where a credibility shock triggers the rapid repricing that gradual deterioration tends to precede. The 1994 "bond massacre," triggered not by crisis but by a modest upward surprise in inflation expectations, erased 15% from equity valuations in four months.
</p>

<div class="chart-block">
  <div class="chart-title">Net Interest as % of Federal Revenue</div>
  <div class="chart-subtitle">Every dollar the government raises, 19 cents now services past debt — up from 8 cents a decade ago</div>
  <div class="bar-chart">
    <div class="bar-row">
      <div class="bar-label">2015</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:25%"><span class="bar-val">6.1%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">2017</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:32%"><span class="bar-val">7.7%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">2019</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:36%"><span class="bar-val">8.7%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">2021</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:24%"><span class="bar-val">5.8%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">2023</div>
      <div class="bar-track"><div class="bar-fill" style="width:60%"><span class="bar-val">14.4%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">2024</div>
      <div class="bar-track"><div class="bar-fill" style="width:68%"><span class="bar-val">16.4%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">2025E</div>
      <div class="bar-track"><div class="bar-fill" style="width:81%"><span class="bar-val">19.4%</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;color:var(--orange);">2030P (CBO)</div>
      <div class="bar-track"><div class="bar-fill" style="width:100%;background:var(--orange)"><span class="bar-val">24%</span></div></div>
    </div>
  </div>
  <div class="chart-note">Sources: Congressional Budget Office, Office of Management and Budget. 2025E = estimate; 2030P = CBO projection under current law.</div>
</div>

<div class="brief-h3">What Would Have to Be True for the Bull Case to Hold</div>

<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  The optimists need at least two of the following three things: nominal GDP growth sustained above 5% annually for a decade (possible but historically unusual outside wartime or a genuine AI productivity boom), a return of sub-3% long rates without reigniting inflation (logically difficult given fiscal deficits of this scale), or a credible medium-term fiscal consolidation of 2-3% of GDP (possible but requiring political will that has not materialized in either party's current platform). One of these is plausible. All three simultaneously is the kind of scenario that usually requires a crisis to catalyze. We note that the Peterson Foundation has been publishing these warnings since 2008, and the crisis has not yet arrived — which either means the warnings are wrong, or the timeline is simply longer than anyone expects.
</p>

<div class="brief-h3">Risk Scenarios</div>

<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:16px;font-style:italic;">
  If proposed federal legislation extending and expanding current tax policy passes in full — adding $3–4 trillion to the 10-year debt trajectory — then the 10-year Treasury yield likely tests 5% and equity valuations compress as the risk-free rate re-rates higher. Watch 30-year auction tails for the early warning signal; a tail above 2 basis points across consecutive auctions is the tell.
</p>

<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:16px;font-style:italic;">
  If Social Security reform fails to materialize before the 2033 trust fund exhaustion, then the mandatory spending cliff becomes a hard constraint, forcing either a 23% benefit cut or emergency deficit financing at scale — both of which would be disorderly. Watch annual Social Security Trustees Reports for the exhaustion date; any acceleration beyond 2033 is a warning flag.
</p>

<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:24px;font-style:italic;">
  If foreign central bank demand for Treasuries continues its structural decline — foreign official holdings are down 10 percentage points over the past decade — then domestic dealers absorb a growing share of issuance at wider spreads, making the deficit self-reinforcing through higher financing costs. Watch the foreign central bank participation rate at 10-year auctions; below 10% would be a historically anomalous signal.
</p>

<div class="brief-h3">Macro Moo View</div>

<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  We are cautious on duration and constructive on real assets. Not because a debt crisis is imminent — it is not, and the structural advantages of dollar hegemony are real — but because the asymmetry is unfavorable: the upside to owning 10-year Treasuries from 4.35% is modest, while the tail risk is a disorderly repricing that would be difficult to navigate in real time. We hold modest overweights in TIPS, commodities, and international equities as partial hedges against the scenario where fiscal arithmetic eventually overwhelms fiscal patience. Mr. Micawber's rule was not a prediction about timing; it was a prediction about direction. The direction here is not ambiguous.
</p>

<div class="brief-disclosure">
  This analysis is produced by the Moomoo Investment Research Team for informational purposes only and draws on publicly available data and research, including Congressional Budget Office projections and Federal Reserve data. Past performance is not indicative of future results. This does not constitute investment advice. Investors should consult a qualified financial advisor before making investment decisions.
</div>
"""

excerpt = "For the first time since the post-WWII demobilization era, net interest on federal debt has eclipsed the defense budget. With debt at 124% of GDP and the interest-to-revenue ratio hitting 19 cents on every dollar — and rising — the math behind America's fiscal trajectory deserves more attention than markets are currently giving it."

# Delete existing article id=4 if it exists, then insert new one
existing = db.query(Article).filter(Article.id == 4).first()
if existing:
    db.delete(existing)
    db.commit()
    print("Deleted existing article id=4")

article = Article(
    title="Mr. Micawber's Arithmetic — The Interest Bill That Now Outranks the Pentagon",
    slug="us-fiscal-debt-interest-burden-2026",
    excerpt=excerpt,
    content_html=content_html,
    category="Macro",
    author="Macro Moo",
    featured=False,
    published=True,
    created_at=datetime(2026, 5, 9, 9, 0, 0)
)

db.add(article)
db.flush()
new_id = article.id
db.commit()
print(f"Inserted new macro article with id={new_id}")
print(f"Title: {article.title}")
print(f"Category: {article.category}")
