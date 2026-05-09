"""Update article id=3 with light-themed EOTM-style content matching site design."""
import sqlite3, pathlib

DB = pathlib.Path(__file__).parent / "moomoo.db"

EXCERPT = (
    "$370 billion will flow into AI infrastructure in 2026 alone. "
    "We've seen this movie before — and the third act is always the same: the builders get rich first, "
    "the users take decades to catch up. Here's what the history of transformative technologies tells us "
    "about the AI ROI question no one wants to answer honestly."
)

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
.ea-section{margin:36px 0}
.ea-section h2{font-size:18px;font-weight:800;color:#1a1a2e;margin-bottom:14px;padding-bottom:10px;border-bottom:1px solid #f3f4f6;display:flex;align-items:center;gap:8px}
.ea-section h2::before{content:"";display:inline-block;width:3px;height:18px;background:#ff6900;border-radius:2px;flex-shrink:0}
.ea-section p{font-size:15px;color:#374151;margin-bottom:14px;line-height:1.75}
.ea-section p strong{color:#1a1a2e}
.ea-chart-wrap{background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:18px;margin:20px 0}
.ea-chart-title{font-size:12px;font-weight:700;color:#9ca3af;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:2px}
.ea-chart-sub{font-size:12px;color:#d1d5db;margin-bottom:14px}
.ea-chart-wrap canvas{max-height:240px}
.ea-phase-strip{display:flex;gap:4px;margin-bottom:10px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.4px}
.ea-phase{padding:3px 10px;border-radius:4px;color:#fff}
.ea-phase.p1{background:#d1d5db;color:#6b7280;flex:2}
.ea-phase.p2{background:#93c5fd;color:#1e40af;flex:3}
.ea-phase.p3{background:#ff6900;flex:4}
.ea-risk-grid{display:grid;gap:12px;margin:20px 0}
.ea-risk-card{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:18px 20px;border-left:3px solid #ff6900}
.ea-risk-card strong{color:#ff6900;display:block;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px}
.ea-risk-card p{font-size:14px;color:#6b7280;margin:0;line-height:1.6}
.ea-risk-card .ea-watch{font-size:12px;color:#9ca3af;margin-top:6px;font-style:italic}
.ea-moomoo-view{background:#fff7f0;border:1px solid #fed7aa;border-radius:12px;padding:24px;margin:36px 0;border-top:3px solid #ff6900}
.ea-moomoo-view-head{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.ea-moomoo-view-logo{font-size:15px;font-weight:800;color:#1a1a2e}
.ea-moomoo-view-logo span{color:#ff6900}
.ea-stance{background:#ff6900;color:#fff;font-size:11px;font-weight:700;padding:3px 10px;border-radius:10px;text-transform:uppercase;letter-spacing:0.5px}
.ea-moomoo-view p{font-size:14px;color:#6b7280;line-height:1.75;margin-bottom:10px}
.ea-moomoo-view p:last-child{margin-bottom:0}
.ea-disclosure{font-size:11px;color:#d1d5db;line-height:1.6;margin-top:36px;padding-top:16px;border-top:1px solid #f3f4f6}
</style>

<div class="ea">

<div class="ea-eyebrow">Eye on the Market &nbsp;|&nbsp; Moomoo Investment Strategy &nbsp;|&nbsp; May 2026</div>
<div class="ea-deck">$370 billion will flow into AI infrastructure in 2026 alone. We've seen this movie before — and the third act is always the same: the builders get rich first, the users take decades to catch up. Here's what the history of transformative technologies tells us about the AI ROI question no one wants to answer honestly.</div>

<div class="ea-byline">
  <div class="ea-avatar">MI</div>
  <div class="ea-byline-text">
    <strong>Moomoo Investment Research Team</strong>
    May 9, 2026 &nbsp;·&nbsp; Eye on the Market
  </div>
</div>

<div class="ea-stat-row">
  <div class="ea-stat ora">
    <div class="ea-stat-val">$370B</div>
    <div class="ea-stat-lbl">2026E AI Capex</div>
    <div class="ea-stat-sub">Big 4 hyperscalers</div>
  </div>
  <div class="ea-stat grn">
    <div class="ea-stat-val">+2.3%</div>
    <div class="ea-stat-lbl">US Productivity</div>
    <div class="ea-stat-sub">2025 BLS</div>
  </div>
  <div class="ea-stat blu">
    <div class="ea-stat-val">+142%</div>
    <div class="ea-stat-lbl">NVDA Revenue</div>
    <div class="ea-stat-sub">FY2025 YoY</div>
  </div>
  <div class="ea-stat red">
    <div class="ea-stat-val">78%</div>
    <div class="ea-stat-lbl">AI Projects</div>
    <div class="ea-stat-sub">Never reach prod</div>
  </div>
</div>

<div class="ea-section">
  <h2>The Trillion-Dollar Setup</h2>
  <p>The consensus narrative in 2026 goes like this: AI is the most important technology since the internet, the hyperscalers understand this, and the ones who don't spend enough now will lose the platform war permanently. <strong>Amazon, Microsoft, Google, and Meta have committed a combined $370 billion in infrastructure capex for 2026 alone</strong> — a figure that would have been unthinkable four years ago, when the same four companies spent roughly $87 billion combined.</p>
  <p>The bull case is straightforward and not wrong: general-purpose AI at scale requires physical infrastructure first. You can't run GPT-5 on a server room from 2018. The platform logic is real — whoever builds the best model plus the best inference network wins a winner-take-most distribution. And NVIDIA's gross margins, currently north of 70%, suggest that <strong>at least one company in this chain has already solved its ROI problem</strong>.</p>

  <div class="ea-chart-wrap">
    <div class="ea-chart-title">Hyperscaler AI Capex Explosion</div>
    <div class="ea-chart-sub">Annual capex ($bn) — Amazon, Microsoft, Google, Meta · 2020–2026E</div>
    <div class="ea-phase-strip">
      <div class="ea-phase p1">Pre-ChatGPT</div>
      <div class="ea-phase p2">AI Awakening</div>
      <div class="ea-phase p3">AI Arms Race</div>
    </div>
    <canvas id="eotm-c1"></canvas>
  </div>
</div>

<div class="ea-section">
  <h2>The History Lesson No One Is Pricing In</h2>
  <p>The uncomfortable question is not whether AI will be transformative — it almost certainly will be. The question is <em>when</em> that transformation shows up in productivity statistics, earnings per share, and GDP growth. History's answer is: later than you think, and not where you expect it.</p>
  <p>Consider electrification. The dynamo was commercially deployed in the 1880s. <strong>Measurable productivity gains from factory electrification didn't arrive until the 1920s</strong> — a 30-year lag during which enormous capital was spent and fortunes were made by utilities and equipment manufacturers. The users — manufacturers — captured the gains only after they redesigned their entire production processes around the new technology, not just plugged motors into existing workflows.</p>
  <p>The internet is the optimistic case. Broadband was widely available by the late 1990s, yet the productivity paradox persisted well into the 2000s. <strong>The lag from internet deployment to measurable economy-wide productivity acceleration was roughly 10 years.</strong> Mobile and social media were faster — 8 years from iPhone to meaningful productivity capture — but that was an unusually fast adoption curve built on existing infrastructure.</p>

  <div class="ea-chart-wrap">
    <div class="ea-chart-title">AI Capex vs. US Productivity Growth</div>
    <div class="ea-chart-sub">Annual AI-related capex ($bn, left axis) vs. US nonfarm productivity growth % (right axis) · 2018–2026E</div>
    <canvas id="eotm-c2"></canvas>
  </div>

  <div class="ea-chart-wrap">
    <div class="ea-chart-title">Technology ROI Lag — Historical Comparison</div>
    <div class="ea-chart-sub">Years from infrastructure deployment to measurable economy-wide productivity gain</div>
    <canvas id="eotm-c3"></canvas>
  </div>
</div>

<div class="ea-section">
  <h2>The Complication: Concentration and the NVDA Ceiling</h2>
  <p>The current AI capex cycle has a structural feature prior technology waves did not: <strong>an unusually high degree of spend concentration</strong>. Four companies account for roughly 85% of disclosed AI infrastructure investment. This isn't the distributed buildout of the 1990s internet, where thousands of ISPs and telcos were laying fiber simultaneously. It's four engineering-driven monopolies in a race they define themselves.</p>
  <p>That concentration has two implications. First, the ROI calculus for the hyperscalers is different from the economy-wide productivity story — <strong>they are simultaneously the infrastructure builders and the primary application layer</strong>, which shortens their internal payback period even as external spillovers lag. Second, NVIDIA's current pricing power — roughly $30,000–$40,000 per H100 equivalent with gross margins above 70% — is a tax on that buildout that will compress as AMD, Google's TPUs, Amazon's Trainium, and Meta's MTIA mature.</p>

  <div class="ea-chart-wrap">
    <div class="ea-chart-title">2026E AI Capex by Company</div>
    <div class="ea-chart-sub">Estimated infrastructure spend ($bn) — top disclosed spenders</div>
    <canvas id="eotm-c4"></canvas>
  </div>
</div>

<div class="ea-section">
  <h2>Where This Could Go Wrong — and Right</h2>
  <p>The scenario most investors are not pricing is a <strong>capex overshoot followed by a utilization gap</strong>. Between 2000 and 2002, US telecom companies laid enough fiber to carry 100x the internet traffic that existed at the time — and then went bankrupt. The fiber was real and useful; it just didn't generate the cash flows needed to service the debt used to build it.</p>
  <p>The scenario most bears are underweighting is <strong>rapid application-layer value creation within the hyperscalers' own ecosystems</strong>. Microsoft's Copilot seat count, Google's AI Overviews monetization, and Meta's AI-driven ad targeting improvements are early but real signals that at least some of the capex is generating near-term returns. The question is whether those returns justify the entire $370 billion commitment — or whether they justify $100 billion of it and the rest is competitive defense spending with uncertain payback.</p>

  <div class="ea-risk-grid">
    <div class="ea-risk-card">
      <strong>Risk 1 — Demand Miss</strong>
      <p>If enterprise AI adoption slows materially — due to budget constraints, implementation complexity, or continued underwhelming productivity evidence — hyperscaler capex will outrun monetization. <span class="ea-watch">Watch: Azure AI revenue growth vs. capex growth ratio; if capex grows faster than revenue for 3+ consecutive quarters, the math becomes difficult to defend.</span></p>
    </div>
    <div class="ea-risk-card">
      <strong>Risk 2 — NVDA Margin Compression</strong>
      <p>If AMD's MI300X series reaches 80%+ of H100 performance at 60% of the price — or if hyperscaler custom silicon reaches cost-competitive throughput — NVIDIA's 70%+ gross margins are not sustainable. <span class="ea-watch">Watch: AMD datacenter revenue growth rate; any quarter above 40% YoY signals meaningful share capture.</span></p>
    </div>
    <div class="ea-risk-card">
      <strong>Risk 3 — Regulatory Intervention</strong>
      <p>The EU AI Act, US executive orders on compute export controls, and antitrust scrutiny of hyperscaler model monopolies all represent non-zero probability disruptions to the buildout trajectory. <span class="ea-watch">Watch: OFAC export control updates on H100 successors; any expansion to Tier 2 country restrictions would materially reduce addressable market.</span></p>
    </div>
  </div>
</div>

<div class="ea-moomoo-view">
  <div class="ea-moomoo-view-head">
    <div class="ea-moomoo-view-logo">moomoo<span>Insights</span></div>
    <div class="ea-stance">Selectively Constructive</div>
  </div>
  <p>The infrastructure buildout is real, the capital commitment is irreversible, and the near-term beneficiaries — semiconductor equipment, power infrastructure, cooling systems, and NVIDIA itself — have already been identified and priced. The more interesting question for 2026–2028 is where the application layer value accretes: which enterprises will show up in earnings calls with AI-driven margin improvement, not just AI-driven cost centers.</p>
  <p>Our positioning reflects selective constructiveness on AI infrastructure plays with defensible moats while maintaining skepticism on the broader "AI will fix everything" narrative embedded in S&P 500 forward multiples. <strong>The history of transformative technology says the ROI lag is long, the distribution is uneven, and the first wave of infrastructure investors rarely captures the full value they create.</strong> The winding road to ROI runs through a lot of data centers before it gets to GDP.</p>
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

    // Chart 1 — Stacked bar: Hyperscaler capex 2020-2026E
    var c1=document.getElementById('eotm-c1');
    if(c1){new Chart(c1,{
      type:'bar',
      data:{
        labels:['2020','2021','2022','2023','2024','2025','2026E'],
        datasets:[
          {label:'Amazon',data:[35,52,61,56,75,91,105],backgroundColor:'rgba(255,105,0,0.75)',borderRadius:3,stack:'s'},
          {label:'Microsoft',data:[15,20,23,28,55,75,80],backgroundColor:'rgba(37,99,235,0.7)',borderRadius:3,stack:'s'},
          {label:'Google',data:[22,24,31,32,52,58,75],backgroundColor:'rgba(22,163,74,0.65)',borderRadius:3,stack:'s'},
          {label:'Meta',data:[15,19,32,28,38,65,65],backgroundColor:'rgba(168,85,247,0.65)',borderRadius:3,stack:'s'}
        ]
      },
      options:{
        responsive:true,maintainAspectRatio:true,
        scales:{
          x:{grid:{color:G},ticks:{color:'#9ca3af'}},
          y:{grid:{color:G},ticks:{color:'#9ca3af',callback:function(v){return'$'+v+'B'}},title:{display:true,text:'Capex ($bn)',color:'#9ca3af'}}
        },
        plugins:{legend:{labels:{color:'#6b7280',boxWidth:10}},tooltip:{...TT,callbacks:{label:function(c){return c.dataset.label+': $'+c.parsed.y+'B'}}}}
      }
    });}

    // Chart 2 — Dual axis: capex vs productivity
    var c2=document.getElementById('eotm-c2');
    if(c2){new Chart(c2,{
      type:'bar',
      data:{
        labels:['2018','2019','2020','2021','2022','2023','2024','2025','2026E'],
        datasets:[
          {label:'AI Capex ($B)',data:[50,60,87,115,147,144,220,289,370],backgroundColor:'rgba(255,105,0,0.6)',borderRadius:3,yAxisID:'y'},
          {label:'US Productivity %',data:[1.3,1.7,3.8,2.3,-1.8,3.5,2.4,2.3,null],type:'line',borderColor:'#16a34a',backgroundColor:'rgba(22,163,74,0.08)',pointRadius:4,pointBackgroundColor:'#16a34a',fill:true,tension:0.35,yAxisID:'y1',borderWidth:2}
        ]
      },
      options:{
        responsive:true,maintainAspectRatio:true,
        scales:{
          x:{grid:{color:G},ticks:{color:'#9ca3af'}},
          y:{grid:{color:G},ticks:{color:'#ff6900',callback:function(v){return'$'+v+'B'}},position:'left'},
          y1:{grid:{drawOnChartArea:false},ticks:{color:'#16a34a',callback:function(v){return v+'%'}},position:'right'}
        },
        plugins:{legend:{labels:{color:'#6b7280',boxWidth:10}},tooltip:TT}
      }
    });}

    // Chart 3 — Horizontal bar: ROI lag by technology
    var c3=document.getElementById('eotm-c3');
    if(c3){
      var techs=['AI (Bull Case)','AI (Base Case)','Mobile/Social','Internet','PC Era','Mainframe','Mass Production','Electrification'];
      var lags=[5,8,8,10,15,18,20,30];
      var colors=lags.map(function(v,i){return i<=1?'rgba(255,105,0,0.75)':'rgba(37,99,235,0.45)';});
      new Chart(c3,{
        type:'bar',
        data:{labels:techs,datasets:[{label:'Years to Economy-Wide Productivity Gain',data:lags,backgroundColor:colors,borderRadius:3}]},
        options:{
          indexAxis:'y',responsive:true,maintainAspectRatio:true,
          scales:{
            x:{grid:{color:G},ticks:{color:'#9ca3af',callback:function(v){return v+'yr'}},max:35},
            y:{grid:{color:G},ticks:{color:'#6b7280'}}
          },
          plugins:{legend:{display:false},tooltip:{...TT,callbacks:{label:function(c){return c.parsed.x+' years'}}}}
        }
      });
    }

    // Chart 4 — Horizontal bar: 2026E capex by company
    var c4=document.getElementById('eotm-c4');
    if(c4){
      var cos=['Amazon','Microsoft','Google','Meta','Oracle','Tesla','Apple','Others'];
      var vals=[105,80,75,65,25,12,8,45];
      var cc=['rgba(255,105,0,0.75)','rgba(37,99,235,0.7)','rgba(22,163,74,0.65)','rgba(168,85,247,0.65)','rgba(245,158,11,0.65)','rgba(239,68,68,0.6)','rgba(107,114,128,0.5)','rgba(156,163,175,0.4)'];
      new Chart(c4,{
        type:'bar',
        data:{labels:cos,datasets:[{label:'2026E Capex ($bn)',data:vals,backgroundColor:cc,borderRadius:3}]},
        options:{
          indexAxis:'y',responsive:true,maintainAspectRatio:true,
          scales:{
            x:{grid:{color:G},ticks:{color:'#9ca3af',callback:function(v){return'$'+v+'B'}}},
            y:{grid:{color:G},ticks:{color:'#6b7280'}}
          },
          plugins:{legend:{display:false},tooltip:{...TT,callbacks:{label:function(c){return'$'+c.parsed.x+'B'}}}}
        }
      });
    }
  }
  initCharts();
})();
</script>"""

conn = sqlite3.connect(str(DB))
cur = conn.cursor()
cur.execute("UPDATE articles SET content_html=?, excerpt=? WHERE id=3", (CONTENT, EXCERPT))
conn.commit()
rows = cur.rowcount
conn.close()
print(f"Updated {rows} row(s).")
