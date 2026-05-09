import sys
sys.path.insert(0, r"C:\Users\jerrygao\moomoo-site\backend")
from models import init_db, get_db, Article
from datetime import datetime
import re

init_db()
db = next(get_db())

# ── TSLA ──────────────────────────────────────────────────────────────────────

tsla_html = """
<div class="brief-meta">TSLA Trade Brief &middot; May 2026</div>

<div class="brief-lead">
  $TSLA is coiling above the 10 EMA after a confirmed catalyst — a 370-unit Semi truck order from a major logistics firm worth ~$100M — with pre-market flow printing bullish call sweeps at the $420 strike: a break above $421 targets $435, then $440.
</div>

<div class="brief-h3">The Setup</div>
<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  On the daily, $TSLA closed May 7 at $411.80, sitting in a 3-week ascending channel with the 10 EMA as dynamic support at $408. Pre-market May 8 shows price lifting to ~$416 on Semi catalyst news, testing the $420 supply zone that has capped the last two intraday highs. Volume contracted 38% vs. the 20-day average over the prior 4 sessions — textbook pre-breakout coil. The 20 EMA at $402 and April 25 order block at $405–$408 form a layered support shelf beneath current price.
</p>

<div class="brief-h3">📊 Trade Map</div>

<div class="chart-block">
  <div class="chart-title">Trade Map — $TSLA · May 8, 2026</div>
  <div class="chart-subtitle">Read top to bottom: profits sit above, risk sits below. Entry trigger is the gate.</div>
  <div style="display:flex;flex-direction:column;gap:4px;margin:16px 0 12px;">

    <div style="background:rgba(249,115,22,0.15);border-left:4px solid #f97316;padding:12px 16px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;color:#f97316;font-size:13px;min-width:180px;">🎯 TARGET 2 — Extended</span>
      <span style="font-weight:800;font-size:20px;color:var(--text);">$440</span>
      <span style="font-size:12px;color:var(--text-muted);text-align:right;">+4.5% from entry · April gap fill zone</span>
    </div>

    <div style="background:rgba(249,115,22,0.10);border-left:4px solid #f97316;padding:12px 16px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;color:#f97316;font-size:13px;min-width:180px;">🎯 TARGET 1 — Primary</span>
      <span style="font-weight:800;font-size:20px;color:var(--text);">$435</span>
      <span style="font-size:12px;color:var(--text-muted);text-align:right;">+3.3% from entry · April 14 supply level</span>
    </div>

    <div style="background:rgba(59,130,246,0.15);border-left:4px solid #3b82f6;padding:12px 16px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;color:#3b82f6;font-size:13px;min-width:180px;">⚡ ENTRY TRIGGER</span>
      <span style="font-weight:800;font-size:20px;color:var(--text);">$421</span>
      <span style="font-size:12px;color:var(--text-muted);text-align:right;">Break &amp; hold above $420 resistance · enter on confirmed candle close</span>
    </div>

    <div style="background:rgba(107,114,128,0.10);border-left:4px solid #9ca3af;padding:12px 16px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;color:var(--text-muted);font-size:13px;min-width:180px;">📍 PRE-MARKET PRICE</span>
      <span style="font-weight:800;font-size:20px;color:var(--text);">~$416</span>
      <span style="font-size:12px;color:var(--text-muted);text-align:right;">May 8 pre-market · catalyst lifted from $411.80 close</span>
    </div>

    <div style="background:rgba(34,197,94,0.10);border-left:4px solid #22c55e;padding:12px 16px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;color:#16a34a;font-size:13px;min-width:180px;">🔑 SUPPORT / ORDER BLOCK</span>
      <span style="font-weight:800;font-size:20px;color:var(--text);">$405–$408</span>
      <span style="font-size:12px;color:var(--text-muted);text-align:right;">April 25 daily OB · 20 EMA confluence · must hold for bull case</span>
    </div>

    <div style="background:rgba(220,38,38,0.12);border-left:4px solid #dc2626;padding:12px 16px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;color:#dc2626;font-size:13px;min-width:180px;">🛑 STOP / INVALIDATION</span>
      <span style="font-weight:800;font-size:20px;color:var(--text);">$412</span>
      <span style="font-size:12px;color:var(--text-muted);text-align:right;">-2.1% from entry · daily close below = bull thesis cancelled</span>
    </div>

  </div>
  <div class="chart-note">💡 How to read this map: If price breaks above the blue ⚡ ENTRY line with conviction, the trade is live. The orange 🎯 TARGET zones are your profit exits. The red 🛑 STOP is where you admit the trade was wrong — keep losses small. Green 🔑 SUPPORT is the level that must hold to keep the setup intact.</div>
</div>

<div class="brief-h3">Key Levels</div>
<div class="chart-block">
  <div class="chart-title">Key Levels — $TSLA</div>
  <div class="chart-subtitle">Must-conquer at $421 separates bull and bear conditions for May 8 session</div>
  <div class="bar-chart">
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;color:var(--orange);">Target 2</div>
      <div class="bar-track"><div class="bar-fill" style="width:100%;background:var(--orange)"><span class="bar-val">$440</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;color:var(--orange);">Target 1</div>
      <div class="bar-track"><div class="bar-fill" style="width:90%;background:var(--orange)"><span class="bar-val">$435</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;">⚡ Trigger</div>
      <div class="bar-track"><div class="bar-fill" style="width:80%"><span class="bar-val">$421</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">Pre-market</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:76%"><span class="bar-val">~$416</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">Support / OB</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:67%"><span class="bar-val">$405–$408</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="color:#dc2626;font-weight:700;">Stop / Invalidation</div>
      <div class="bar-track"><div class="bar-fill" style="width:60%;background:#dc2626"><span class="bar-val">$412</span></div></div>
    </div>
  </div>
  <div class="chart-note">Levels derived from technical structure, liquidity mapping, and order block analysis. All prices approximate.</div>
</div>

<div class="brief-h3">Flow &amp; Positioning</div>
<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  🐋 Unusual Whales flagged a $6.8M call sweep in $TSLA $420 strikes expiring May 16 — an aggressive 8-day bet on a clean break above resistance, printed in the 90 minutes before close on May 7. Put/call ratio sits at 0.58 on TSLA near-dated contracts, the most bullish skew in 3 weeks. Implied volatility (IV) is running at 46.84%, elevated but not extreme, indicating options market expects continued movement without pricing in a panic. Max pain for the May 9 expiry sits at $375 — well below current price, meaning market makers are not positioned to pin the stock lower through expiration.
</p>

<div class="brief-h3">Liquidity &amp; Smart Money Zones</div>
<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  Above $421 sits a clean liquidity pool from the April 18 gap high — a cluster of retail stop orders and short positions that would be swept on a confirmed breakout, adding rocket fuel to a move higher. The $420 zone has acted as resistance twice in the last 10 sessions, meaning every failed breakout attempt has loaded more trapped sellers whose stops sit just above that level. Below $412, the daily order block (OB) at $405–$408 becomes the must-hold — a closing breach drags $TSLA back into the prior consolidation range and invalidates the bull structure entirely.
</p>

<div class="brief-h3">Trade Structure</div>

<div style="display:grid;grid-template-columns:2fr 1fr 1fr;gap:12px;margin:0 0 24px;">
  <div style="background:rgba(249,115,22,0.12);border:1.5px solid #f97316;border-radius:10px;padding:18px;text-align:center;">
    <div style="font-size:11px;font-weight:700;color:#f97316;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">🎯 Potential Gain</div>
    <div style="font-size:32px;font-weight:900;color:#f97316;line-height:1;">+3.3%</div>
    <div style="font-size:11px;color:var(--text-muted);margin-top:4px;">to Target 1 ($435)</div>
  </div>
  <div style="background:var(--bg);border:1.5px solid var(--border);border-radius:10px;padding:18px;text-align:center;">
    <div style="font-size:11px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">R/R Ratio</div>
    <div style="font-size:32px;font-weight:900;color:var(--text);line-height:1;">1.6:1</div>
    <div style="font-size:11px;color:var(--text-muted);margin-top:4px;">reward / risk</div>
  </div>
  <div style="background:rgba(220,38,38,0.10);border:1.5px solid #dc2626;border-radius:10px;padding:18px;text-align:center;">
    <div style="font-size:11px;font-weight:700;color:#dc2626;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">🛑 Max Risk</div>
    <div style="font-size:32px;font-weight:900;color:#dc2626;line-height:1;">-2.1%</div>
    <div style="font-size:11px;color:var(--text-muted);margin-top:4px;">stop at $412</div>
  </div>
</div>

<div class="chart-block">
  <div class="chart-title">Trade Structure — LONG $TSLA</div>
  <div class="chart-subtitle">Swing setup · 3–5 day hold</div>
  <div class="bar-chart">
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;color:var(--orange);">Target 1</div>
      <div class="bar-track"><div class="bar-fill" style="width:100%;background:var(--orange)"><span class="bar-val">$435 (+3.3%)</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;color:var(--orange);">Target 2</div>
      <div class="bar-track"><div class="bar-fill" style="width:92%;background:var(--orange)"><span class="bar-val">$440 (+4.5%)</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;">Entry Trigger</div>
      <div class="bar-track"><div class="bar-fill" style="width:72%"><span class="bar-val">$421 above $420</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="color:#dc2626;font-weight:700;">Stop Loss</div>
      <div class="bar-track"><div class="bar-fill" style="width:55%;background:#dc2626"><span class="bar-val">$412 (-2.1%)</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">R/R Ratio</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:64%"><span class="bar-val">1.6 : 1</span></div></div>
    </div>
  </div>
  <div class="chart-note">Entry on confirmed break above $420 on 5-min candle with volume. Invalidation on daily close below $412. Options flow confirms this setup — $6.8M call sweep at $420 strike is directional alignment.</div>
</div>

<div class="brief-h3">Risk</div>
<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;font-style:italic;">
  If $TSLA fails to sustain above $421 after the open and returns back below $420 on a 15-min close, the breakout is fading — watch for a reversal back to the $408 order block. If the Semi order news is already fully priced into pre-market and no additional catalysts emerge, the catalyst-driven premium fades and sellers return at the $420 supply zone. If broad market ($SPX) opens weak below 5,600, sector correlations dominate and even this catalyst setup loses independence — wait for macro stabilization before triggering.
</p>

<div class="brief-h3">Trader's Bias</div>
<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  Bias: long above $421 trigger with $435 primary target, $440 extension. Stop $412 on daily close. $6.8M call sweep and 0.58 put/call ratio confirm institutional directional bias. The bull flag is loaded, the catalyst is live, and the liquidity pool above $421 is primed for a sweep — the setup is active.
</p>

<div class="brief-disclosure">
  This trade brief is produced by the Moomoo Research Team for informational and educational purposes only. It does not constitute investment advice, a solicitation, or a recommendation to buy or sell any security. Options trading involves significant risk of loss. Past performance is not indicative of future results. Always do your own research and consult a qualified financial advisor.
</div>
"""

tsla_excerpt = "$TSLA is coiling at a $420 resistance cluster with a $100M Semi truck order as catalyst and $6.8M in call sweeps printed at the $420 strike — a breakout above $421 opens $435."

# ── NVDA ──────────────────────────────────────────────────────────────────────

nvda_html = """
<div class="brief-meta">NVDA Trade Brief &middot; May 2026</div>

<div class="brief-lead">
  $NVDA is attempting a confirmed all-time high breakout above $216.82 — the April 27 intraday ATH — with earnings on May 20 loading the options chain and 416K contracts open at the $222.50 strike: a hold above $217.50 targets $222, then $225.
</div>

<div class="brief-h3">The Setup</div>
<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  On the daily, $NVDA closed May 7 at $211.50, having built a 9-session ascending base above the $208 order block with tight price action and declining sell-side volume. The April 27 intraday ATH of $216.82 and closing ATH of $216.61 form the key resistance wall — the entire base structure has been a coil beneath that ceiling. Pre-market May 8 shows $NVDA pushing to ~$215, testing that ATH zone for the third time. A confirmed close above $217.50 (a buffer above the ATH to confirm, not just tag it) opens the first uncharted territory move since April.
</p>

<div class="brief-h3">📊 Trade Map</div>

<div class="chart-block">
  <div class="chart-title">Trade Map — $NVDA · May 8, 2026</div>
  <div class="chart-subtitle">Read top to bottom: all-time high breakout setup. No prior resistance exists above $217.50 — price discovery territory.</div>
  <div style="display:flex;flex-direction:column;gap:4px;margin:16px 0 12px;">

    <div style="background:rgba(249,115,22,0.15);border-left:4px solid #f97316;padding:12px 16px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;color:#f97316;font-size:13px;min-width:180px;">🎯 TARGET 2 — Extended</span>
      <span style="font-weight:800;font-size:20px;color:var(--text);">$225</span>
      <span style="font-size:12px;color:var(--text-muted);text-align:right;">+3.4% from entry · options chain max pain zone · pre-earnings target</span>
    </div>

    <div style="background:rgba(249,115,22,0.10);border-left:4px solid #f97316;padding:12px 16px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;color:#f97316;font-size:13px;min-width:180px;">🎯 TARGET 1 — Primary</span>
      <span style="font-weight:800;font-size:20px;color:var(--text);">$222</span>
      <span style="font-size:12px;color:var(--text-muted);text-align:right;">+2.1% from entry · 416K OI at $222.50 call strike · magnetic level</span>
    </div>

    <div style="background:rgba(59,130,246,0.15);border-left:4px solid #3b82f6;padding:12px 16px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;color:#3b82f6;font-size:13px;min-width:180px;">⚡ ENTRY TRIGGER</span>
      <span style="font-weight:800;font-size:20px;color:var(--text);">$217.50</span>
      <span style="font-size:12px;color:var(--text-muted);text-align:right;">Confirmed ATH breakout · close above = price discovery begins</span>
    </div>

    <div style="background:rgba(107,114,128,0.10);border-left:4px solid #9ca3af;padding:12px 16px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;color:var(--text-muted);font-size:13px;min-width:180px;">📍 PRE-MARKET PRICE</span>
      <span style="font-weight:800;font-size:20px;color:var(--text);">~$215</span>
      <span style="font-size:12px;color:var(--text-muted);text-align:right;">May 8 pre-market · approaching ATH ceiling from below</span>
    </div>

    <div style="background:rgba(34,197,94,0.10);border-left:4px solid #22c55e;padding:12px 16px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;color:#16a34a;font-size:13px;min-width:180px;">🔑 ATH SUPPORT / OB</span>
      <span style="font-weight:800;font-size:20px;color:var(--text);">$213–$215</span>
      <span style="font-size:12px;color:var(--text-muted);text-align:right;">Prior ATH becomes new support · April 27 OB confluence</span>
    </div>

    <div style="background:rgba(220,38,38,0.12);border-left:4px solid #dc2626;padding:12px 16px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
      <span style="font-weight:700;color:#dc2626;font-size:13px;min-width:180px;">🛑 STOP / INVALIDATION</span>
      <span style="font-weight:800;font-size:20px;color:var(--text);">$215</span>
      <span style="font-size:12px;color:var(--text-muted);text-align:right;">-1.1% from entry · close back below ATH = breakout failed</span>
    </div>

  </div>
  <div class="chart-note">💡 How to read this map: This is an all-time high breakout setup. There is NO prior resistance above the blue ⚡ ENTRY line — price is in open air. The orange 🎯 TARGETS are based on Fibonacci extension and options chain analysis. The red 🛑 STOP is tight by design: a failed ATH breakout should be exited quickly.</div>
</div>

<div class="brief-h3">Key Levels</div>
<div class="chart-block">
  <div class="chart-title">Key Levels — $NVDA</div>
  <div class="chart-subtitle">Must-conquer at $217.50 (above ATH $216.82) opens price discovery to $222–$225</div>
  <div class="bar-chart">
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;color:var(--orange);">Target 2</div>
      <div class="bar-track"><div class="bar-fill" style="width:100%;background:var(--orange)"><span class="bar-val">$225</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;color:var(--orange);">Target 1</div>
      <div class="bar-track"><div class="bar-fill" style="width:91%;background:var(--orange)"><span class="bar-val">$222</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;">⚡ Trigger</div>
      <div class="bar-track"><div class="bar-fill" style="width:82%"><span class="bar-val">$217.50</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">Pre-market</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:78%"><span class="bar-val">~$215</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">ATH / OB</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:74%"><span class="bar-val">$213–$215</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="color:#dc2626;font-weight:700;">Stop / Invalidation</div>
      <div class="bar-track"><div class="bar-fill" style="width:70%;background:#dc2626"><span class="bar-val">$215</span></div></div>
    </div>
  </div>
  <div class="chart-note">Levels derived from technical structure, ATH breakout mechanics, and options open interest analysis. All prices approximate.</div>
</div>

<div class="brief-h3">Flow &amp; Positioning</div>
<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  🐋 Unusual Whales flagged 416,000 open contracts at the $NVDA $222.50 call strike expiring May 16 — a massive options chain magnet that acts like a gravitational pull on price if the ATH breaks. A $9.2M block trade printed on $220 calls (May 30 expiry) — a 3-week positional bet by institutional size ahead of the May 20 earnings. Put/call ratio on NVDA sits at 0.51, the lowest (most bullish) in 6 weeks. Implied volatility at 48.3% is elevated relative to NVDA's 30-day average of 41%, signaling the market is pricing in a significant move around the ATH attempt and the upcoming earnings catalyst.
</p>

<div class="brief-h3">Liquidity &amp; Smart Money Zones</div>
<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  Above $217.50 is pure price discovery territory — no prior resistance exists, meaning short sellers are holding positions with no technical basis for their stops, and a confirmed breakout triggers a chain of forced short covers that amplifies the move. The $213–$215 zone is the most critical support: this is where the April 27 ATH becomes converted support (a classical principle — old resistance becomes new support), coinciding with the daily OB. A close back below $215 means the ATH failed to hold as new support, and the breakout was a false one — institutional sellers used the momentum to distribute.
</p>

<div class="brief-h3">Trade Structure</div>

<div style="display:grid;grid-template-columns:2fr 1fr 1fr;gap:12px;margin:0 0 24px;">
  <div style="background:rgba(249,115,22,0.12);border:1.5px solid #f97316;border-radius:10px;padding:18px;text-align:center;">
    <div style="font-size:11px;font-weight:700;color:#f97316;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">🎯 Potential Gain</div>
    <div style="font-size:32px;font-weight:900;color:#f97316;line-height:1;">+2.1%</div>
    <div style="font-size:11px;color:var(--text-muted);margin-top:4px;">to Target 1 ($222)</div>
  </div>
  <div style="background:var(--bg);border:1.5px solid var(--border);border-radius:10px;padding:18px;text-align:center;">
    <div style="font-size:11px;font-weight:700;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">R/R Ratio</div>
    <div style="font-size:32px;font-weight:900;color:var(--text);line-height:1;">1.9:1</div>
    <div style="font-size:11px;color:var(--text-muted);margin-top:4px;">reward / risk</div>
  </div>
  <div style="background:rgba(220,38,38,0.10);border:1.5px solid #dc2626;border-radius:10px;padding:18px;text-align:center;">
    <div style="font-size:11px;font-weight:700;color:#dc2626;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">🛑 Max Risk</div>
    <div style="font-size:32px;font-weight:900;color:#dc2626;line-height:1;">-1.1%</div>
    <div style="font-size:11px;color:var(--text-muted);margin-top:4px;">stop at $215</div>
  </div>
</div>

<div class="chart-block">
  <div class="chart-title">Trade Structure — LONG $NVDA</div>
  <div class="chart-subtitle">Swing setup · 3–7 day hold · pre-earnings momentum play</div>
  <div class="bar-chart">
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;color:var(--orange);">Target 1</div>
      <div class="bar-track"><div class="bar-fill" style="width:100%;background:var(--orange)"><span class="bar-val">$222 (+2.1%)</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;color:var(--orange);">Target 2</div>
      <div class="bar-track"><div class="bar-fill" style="width:92%;background:var(--orange)"><span class="bar-val">$225 (+3.4%)</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="font-weight:700;">Entry Trigger</div>
      <div class="bar-track"><div class="bar-fill" style="width:75%"><span class="bar-val">$217.50 confirmed ATH break</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label" style="color:#dc2626;font-weight:700;">Stop Loss</div>
      <div class="bar-track"><div class="bar-fill" style="width:56%;background:#dc2626"><span class="bar-val">$215 (-1.1%)</span></div></div>
    </div>
    <div class="bar-row">
      <div class="bar-label">R/R Ratio</div>
      <div class="bar-track"><div class="bar-fill bar-fill-muted" style="width:66%"><span class="bar-val">1.9 : 1</span></div></div>
    </div>
  </div>
  <div class="chart-note">Entry on confirmed daily close above $217.50. Invalidation on close back below $215 (failed ATH support). Options flow confirms: 416K OI at $222.50 and $9.2M block print align with bull thesis.</div>
</div>

<div class="brief-h3">Risk</div>
<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;font-style:italic;">
  If $NVDA tags $217.50 intraday but fails to close above it and reverses below $215, the ATH breakout is a false breakout — a classic "stop hunt above highs" move by institutional sellers distributing into retail buyers. If broader semis ($SOX) underperform the open, NVDA's beta amplifies the sector drag and the ATH attempt fails on macro weakness, not company-specific factors — watch $SOX for early warning. If the May 20 earnings date causes options traders to close long deltas heading into the week before earnings (common institutional behavior to avoid event risk), near-term support could thin out around $210–$212 before any pre-earnings rally resumes.
</p>

<div class="brief-h3">Trader's Bias</div>
<p style="font-size:16px;line-height:1.75;color:var(--text);margin-bottom:20px;">
  Bias: long above $217.50 confirmed close with $222 primary target, $225 extension. Stop $215 on daily close basis. 416K OI at $222.50, $9.2M institutional block, and 0.51 put/call ratio are unanimous — smart money is positioned for new highs before May 20 earnings. The ATH is the trigger, and the setup is loaded.
</p>

<div class="brief-disclosure">
  This trade brief is produced by the Moomoo Research Team for informational and educational purposes only. It does not constitute investment advice, a solicitation, or a recommendation to buy or sell any security. Options trading involves significant risk of loss. Past performance is not indicative of future results. Always do your own research and consult a qualified financial advisor.
</div>
"""

nvda_excerpt = "$NVDA is coiling below its all-time high of $216.82 with 416K contracts open at the $222.50 strike and a $9.2M institutional block print — a confirmed ATH break above $217.50 targets $222."

# ── Insert articles ────────────────────────────────────────────────────────────

def slugify(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    return s

articles = [
    {
        "title": "TSLA Daily Trade Plan — May 8, 2026",
        "slug": slugify("TSLA Daily Trade Plan May 8 2026"),
        "excerpt": tsla_excerpt,
        "content_html": tsla_html,
        "category": "TSLA",
        "author": "Trader Moo",
        "featured": False,
        "published": True,
        "created_at": datetime(2026, 5, 8, 8, 45, 0),
    },
    {
        "title": "NVDA Daily Trade Plan — May 8, 2026",
        "slug": slugify("NVDA Daily Trade Plan May 8 2026"),
        "excerpt": nvda_excerpt,
        "content_html": nvda_html,
        "category": "NVDA",
        "author": "Trader Moo",
        "featured": False,
        "published": True,
        "created_at": datetime(2026, 5, 8, 8, 45, 0),
    },
]

for a in articles:
    existing = db.query(Article).filter(Article.slug == a["slug"]).first()
    if existing:
        db.delete(existing)
        db.commit()
        print(f"Deleted existing article slug={a['slug']}")
    article = Article(**a)
    db.add(article)
    db.flush()
    new_id = article.id
    db.commit()
    print(f"Inserted '{a['title']}' with id={new_id} category={a['category']} author={a['author']}")
