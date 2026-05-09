"""Insert Hormuz EOTM-style article — short form, 2 charts, author: Macro moo."""
import sqlite3, pathlib, json
from datetime import datetime

DB = pathlib.Path(__file__).parent / "moomoo.db"

TITLE    = 'The Hormuz Trap: Why "Energy Independence" Is the Wrong Mental Model for 2026'
SLUG     = "the-hormuz-trap-energy-independence-2026"
EXCERPT  = (
    "Global oil inventories are drawing down at 8 million barrels per day. "
    "The US is a net fossil fuel exporter. Both facts are real. "
    "Neither one tells you what's actually at risk in your equity portfolio."
)
CATEGORY = "Macro"
AUTHOR   = "Macro moo"
TAGS     = json.dumps(["energy", "macro", "geopolitics", "oil"])

CONTENT = r"""<style>
.ea{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.ea *{box-sizing:border-box}
.ea-eyebrow{font-size:11px;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;color:#ff6900;margin-bottom:12px}
.ea-deck{font-size:16px;color:#6b7280;line-height:1.65;margin-bottom:28px;padding-left:14px;border-left:3px solid #ff6900}
.ea-byline{display:flex;align-items:center;gap:10px;margin-bottom:32px;padding-bottom:20px;border-bottom:1px solid #e5e7eb}
.ea-avatar{width:36px;height:36px;border-radius:50%;background:#ff6900;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;font-size:14px;flex-shrink:0}
.ea-byline-text{font-size:13px;color:#9ca3af}
.ea-byline-text strong{color:#374151;display:block;font-size:14px;font-weight:600}
.ea-stat-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:28px 0}
@media(max-width:640px){.ea-stat-row{grid-template-columns:repeat(2,1fr)}}
.ea-stat{background:#f9fafb;border-radius:10px;padding:16px;border-top:3px solid #e5e7eb;text-align:center}
.ea-stat.ora{border-top-color:#ff6900}
.ea-stat.grn{border-top-color:#16a34a}
.ea-stat.blu{border-top-color:#2563eb}
.ea-stat.red{border-top-color:#dc2626}
.ea-stat-val{font-size:26px;font-weight:800;color:#1a1a2e;letter-spacing:-0.5px}
.ea-stat-lbl{font-size:11px;color:#9ca3af;margin-top:3px;text-transform:uppercase;letter-spacing:0.4px}
.ea-stat-sub{font-size:12px;font-weight:600;margin-top:2px}
.ea-stat.ora .ea-stat-sub{color:#ff6900}
.ea-stat.grn .ea-stat-sub{color:#16a34a}
.ea-stat.blu .ea-stat-sub{color:#2563eb}
.ea-stat.red .ea-stat-sub{color:#dc2626}
.ea-section{margin:32px 0}
.ea-section h2{font-size:18px;font-weight:800;color:#1a1a2e;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #f3f4f6;display:flex;align-items:center;gap:8px}
.ea-section h2::before{content:"";display:inline-block;width:3px;height:18px;background:#ff6900;border-radius:2px;flex-shrink:0}
.ea-section p{font-size:15px;color:#374151;margin-bottom:14px;line-height:1.75}
.ea-section p strong{color:#1a1a2e}
.ea-chart-wrap{background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:18px;margin:20px 0}
.ea-chart-title{font-size:12px;font-weight:700;color:#9ca3af;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:2px}
.ea-chart-sub{font-size:12px;color:#d1d5db;margin-bottom:14px}
.ea-chart-wrap canvas{max-height:240px}
.ea-risk-grid{display:grid;gap:12px;margin:20px 0}
.ea-risk-card{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:18px 20px;border-left:3px solid #ff6900}
.ea-risk-card strong{color:#ff6900;display:block;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px}
.ea-risk-card p{font-size:14px;color:#6b7280;margin:0;line-height:1.6}
.ea-risk-card .ea-watch{font-size:12px;color:#9ca3af;margin-top:6px;font-style:italic}
.ea-moomoo-view{background:#fff7f0;border:1px solid #fed7aa;border-radius:12px;padding:24px;margin:32px 0;border-top:3px solid #ff6900}
.ea-moomoo-view-head{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.ea-moomoo-view-logo{font-size:15px;font-weight:800;color:#1a1a2e}
.ea-moomoo-view-logo span{color:#ff6900}
.ea-stance{background:#ff6900;color:#fff;font-size:11px;font-weight:700;padding:3px 10px;border-radius:10px;text-transform:uppercase;letter-spacing:0.5px}
.ea-moomoo-view p{font-size:14px;color:#6b7280;line-height:1.75;margin-bottom:10px}
.ea-moomoo-view p:last-child{margin-bottom:0}
.ea-disclosure{font-size:11px;color:#d1d5db;line-height:1.6;margin-top:32px;padding-top:16px;border-top:1px solid #f3f4f6}
</style>

<div class="ea">

<div class="ea-eyebrow">Eye on the Market &nbsp;|&nbsp; Moomoo Strategy &nbsp;|&nbsp; May 2026</div>
<div class="ea-deck">Global oil inventories are drawing down at 8 million barrels per day. The US is a net fossil fuel exporter. Both facts are true. Neither one tells you what's actually at risk in your equity portfolio.</div>

<div class="ea-byline">
  <div class="ea-avatar">MM</div>
  <div class="ea-byline-text">
    <strong>Macro moo</strong>
    May 9, 2026 &nbsp;·&nbsp; Eye on the Market
  </div>
</div>

<div class="ea-stat-row">
  <div class="ea-stat red">
    <div class="ea-stat-val">−8M</div>
    <div class="ea-stat-lbl">Inventory Draw</div>
    <div class="ea-stat-sub">Barrels/day</div>
  </div>
  <div class="ea-stat grn">
    <div class="ea-stat-val">−78%</div>
    <div class="ea-stat-lbl">S&amp;P Oil Intensity</div>
    <div class="ea-stat-sub">Since 1990</div>
  </div>
  <div class="ea-stat ora">
    <div class="ea-stat-val">+112%</div>
    <div class="ea-stat-lbl">Crude Pass-Through</div>
    <div class="ea-stat-sub">To wholesale gasoline</div>
  </div>
  <div class="ea-stat blu">
    <div class="ea-stat-val">4</div>
    <div class="ea-stat-lbl">US Mine-Hunters</div>
    <div class="ea-stat-sub">Down from 21 in 1980s</div>
  </div>
</div>

<div class="ea-section">
  <h2>The Myth of Pricing Independence</h2>
  <p>"Energy independent" has become one of the most reassuring and analytically misleading phrases in American macro discourse. The US produced more oil and gas in 2025 than any country in history. It is a net fossil fuel exporter. These facts matter for the trade balance. What they do <em>not</em> do is insulate American equity markets from a global oil price shock.</p>
  <p>Oil is priced globally. When attacks on Gulf infrastructure remove supply from the market, West Texas Intermediate moves alongside Brent. A manufacturer in Ohio buying domestic fuel oil does not receive a discount because the US drills its own crude. The global clearing price adjusts — and the pass-through is essentially the same as in every prior shock: <strong>crude price changes flow to wholesale gasoline at roughly 112% and to marine shipping fuel at 123%</strong>. Production independence is not pricing independence. It never was.</p>
  <p>The real question for 2026 is not whether the US is exposed to a price shock. It obviously is. The question is which parts of the equity market bear the risk — and the answer has changed materially since 1973.</p>

  <div class="ea-chart-wrap">
    <div class="ea-chart-title">S&amp;P 500 Oil Earnings Sensitivity — A Structural Decline</div>
    <div class="ea-chart-sub">Estimated share of S&P 500 earnings directly sensitive to oil prices · 1980–2026E</div>
    <canvas id="hm-c1"></canvas>
  </div>
</div>

<div class="ea-section">
  <h2>Where the 2026 Exposure Actually Lives</h2>
  <p>The S&amp;P 500's direct oil intensity has fallen 75–80% since 1990. Energy's share of the index dropped from 28% in 1980 to under 4% by 2024. The 2022 spike above $120/barrel did not produce anything close to the carnage of 1973 or 1979. That structural shift is real and should not be dismissed.</p>
  <p>But the exposure in 2026 is not to oil company earnings — it is to second-order effects hitting the companies that now dominate the index. The four largest hyperscalers have committed roughly $370 billion in infrastructure capex for 2026 alone. Data centers run on power — much of it generated from natural gas. Construction materials ship on vessels running marine fuel. <strong>If Hormuz remains disrupted into Q3, the cost escalation on in-progress AI infrastructure buildout — which accounts for approximately 75–85% of S&amp;P 500 forward earnings and capex growth — is not trivial.</strong></p>
  <p>The 1973 shock hit oil-intensive industrials that were already a shrinking share of the market. A 2026 escalation threatens the cost structure of the most capital-intensive technology cycle in US corporate history. The exposure is different. It is not smaller.</p>
  <p>Geographically, the asymmetry is stark. Japan imports over 80% of its oil through the Gulf; Europe relies on fossil fuels for roughly 75% of its energy mix. The US is the least exposed major economy — but US multinationals' revenues run through the most exposed economies in the world.</p>

  <div class="ea-chart-wrap">
    <div class="ea-chart-title">Oil Import Dependence — US vs. the World</div>
    <div class="ea-chart-sub">Share of oil consumption met by imports (%) · 2025</div>
    <canvas id="hm-c2"></canvas>
  </div>
</div>

<div class="ea-section">
  <h2>The June-July Test</h2>
  <p>At the current 8 million barrel/day drawdown pace, commercial inventory buffers reach operational stress thresholds for Asian and European refiners in June-July. A coordinated IEA strategic reserve release of 60 million barrels covers roughly 7 days at this rate. It is a gesture, not a solution.</p>
  <p>The physical constraint almost no equity analyst is modeling: June Gulf temperatures reach 130°F, at which point military and maritime equipment operates at the edge of its reliability envelope. The US Navy maintains 4 mine-hunting vessels — down from 21 in the 1980s. Clearing a mined strait does not scale with budget allocations. It scales with capacity that was quietly allowed to atrophy.</p>

  <div class="ea-risk-grid">
    <div class="ea-risk-card">
      <strong>Risk — Escalation Past Summer</strong>
      <p>If Hormuz remains disrupted through July, Asian and European refinery throughput cuts will reach US multinational revenue lines by Q3. <span class="ea-watch">Watch: Microsoft and Amazon Q2 capex guidance — any downward revision to 2026 infrastructure plans is a more important signal than the oil price itself.</span></p>
    </div>
    <div class="ea-risk-card">
      <strong>Upside — Diplomatic Resolution</strong>
      <p>Back-channel Gulf resolutions have historically arrived faster than military timelines would predict. If a transit agreement materializes before June temperatures bind, the inventory math reverses quickly. <span class="ea-watch">Watch: UAE and Qatar tanker transit volumes — any return toward 2025 baseline signals a deal regardless of public statements.</span></p>
    </div>
  </div>
</div>

<div class="ea-moomoo-view">
  <div class="ea-moomoo-view-head">
    <div class="ea-moomoo-view-logo">moomoo<span>Insights</span></div>
    <div class="ea-stance">Cautiously Positioned</div>
  </div>
  <p>The US equity market's structural de-oiling over 35 years is real — this is not 1973. The more precise concern for 2026 is whether a sustained disruption compounds the valuation argument for the AI infrastructure complex, which has become the load-bearing pillar of S&amp;P 500 forward earnings in a way that has no historical precedent.</p>
  <p>We are overweight domestic US services and healthcare — sectors with minimal direct commodity exposure — and underweight Asian manufacturing supply chains most exposed to a Hormuz closure. The June-July window is the critical test. <strong>If the Strait reopens before temperature constraints bind, the shock is manageable. If it doesn't, "energy independence" will need to be retired from investor vocabulary until someone explains why globally integrated commodity markets stopped clearing globally.</strong></p>
</div>

<div class="ea-disclosure">
  This analysis is produced by the Moomoo Investment Research Team for informational purposes only and draws on publicly available data and research. Past performance is not indicative of future results. This does not constitute investment advice. Investors should consult a qualified financial advisor before making investment decisions.
</div>

</div>

<script>
(function(){
  var _inited=false;
  function initCharts(){
    if(typeof Chart==='undefined'){setTimeout(initCharts,100);return;}
    if(_inited)return;_inited=true;
    Chart.defaults.color='#9ca3af';
    Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif";
    Chart.defaults.font.size=11;
    var G='rgba(229,231,235,0.8)';
    var TT={backgroundColor:'#1f2937',borderColor:'#374151',borderWidth:1,titleColor:'#f9fafb',bodyColor:'#d1d5db',padding:10,boxPadding:4};

    // Chart 1 — S&P 500 oil earnings sensitivity (line)
    var c1=document.getElementById('hm-c1');
    if(c1){new Chart(c1,{
      type:'line',
      data:{
        labels:['1980','1985','1990','1995','2000','2005','2010','2015','2020','2025','2026E'],
        datasets:[{
          label:'Oil-sensitive share of S&P 500 earnings (%)',
          data:[28,29,28,22,18,20,16,12,9,6,5],
          borderColor:'#ff6900',backgroundColor:'rgba(255,105,0,0.08)',
          fill:true,tension:0.4,pointRadius:3,pointBackgroundColor:'#ff6900',borderWidth:2
        }]
      },
      options:{
        responsive:true,maintainAspectRatio:true,
        scales:{
          x:{grid:{color:G},ticks:{color:'#9ca3af'}},
          y:{grid:{color:G},ticks:{color:'#ff6900',callback:function(v){return v+'%'}},
             title:{display:true,text:'% of S&P 500 Earnings',color:'#9ca3af'},max:35,min:0}
        },
        plugins:{legend:{labels:{color:'#6b7280',boxWidth:10}},
          tooltip:{...TT,callbacks:{label:function(c){return c.parsed.y+'% oil-sensitive'}}}}
      }
    });}

    // Chart 2 — Oil import dependence by region (horizontal bar)
    var c2=document.getElementById('hm-c2');
    if(c2){
      new Chart(c2,{
        type:'bar',
        data:{
          labels:['United States','China','India','Europe','Japan','South Korea'],
          datasets:[{
            label:'Oil import dependence (%)',
            data:[12,73,82,75,83,89],
            backgroundColor:[
              'rgba(22,163,74,0.75)','rgba(255,105,0,0.7)','rgba(245,158,11,0.7)',
              'rgba(37,99,235,0.7)','rgba(220,38,38,0.75)','rgba(168,85,247,0.65)'
            ],
            borderRadius:4
          }]
        },
        options:{
          indexAxis:'y',responsive:true,maintainAspectRatio:true,
          scales:{
            x:{grid:{color:G},ticks:{color:'#9ca3af',callback:function(v){return v+'%'}},max:100,min:0},
            y:{grid:{color:G},ticks:{color:'#6b7280'}}
          },
          plugins:{legend:{display:false},
            tooltip:{...TT,callbacks:{label:function(c){return c.parsed.x+'% import dependent'}}}}
        }
      });
    }
  }
  initCharts();
})();
</script>"""

conn = sqlite3.connect(str(DB))
cur  = conn.cursor()

cur.execute("SELECT id FROM articles WHERE slug=?", (SLUG,))
row = cur.fetchone()
if row:
    print(f"Slug already exists (id={row[0]}). Updating content and author...")
    now = datetime.utcnow().isoformat()
    cur.execute(
        "UPDATE articles SET title=?,excerpt=?,content_html=?,author=?,category=?,updated_at=? WHERE id=?",
        (TITLE, EXCERPT, CONTENT, AUTHOR, CATEGORY, now, row[0])
    )
    conn.commit()
    print(f"Updated article id={row[0]}")
else:
    now = datetime.utcnow().isoformat()
    cur.execute(
        """INSERT INTO articles
           (title, slug, excerpt, content_html, tags, category, author,
            published, featured, cover_image, created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (TITLE, SLUG, EXCERPT, CONTENT, TAGS, CATEGORY, AUTHOR,
         1, 0, None, now, now)
    )
    conn.commit()
    print(f"Inserted article id={cur.lastrowid}  '{TITLE}'")

conn.close()
