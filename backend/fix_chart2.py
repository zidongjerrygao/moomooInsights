import sys
sys.path.insert(0, r"C:\Users\jerrygao\moomoo-site\backend")
from models import init_db, get_db, Article
init_db()
db = next(get_db())

a = db.query(Article).filter(Article.id == 1).first()

# Find and replace just the beat-chart div
import re
new_beat = '''<div class="beat-chart">
    <div class="beat-metric-block">
      <div class="beat-metric-label">EPS Beat Rate</div>
      <div class="beat-bar-row">
        <span class="beat-bar-tag">Q1 2026</span>
        <div class="beat-bar-track"><div class="beat-bar-cur" style="width:83%"></div></div>
        <span class="beat-bar-pct cur">83%</span>
      </div>
      <div class="beat-bar-row">
        <span class="beat-bar-tag">5-yr avg</span>
        <div class="beat-bar-track"><div class="beat-bar-avg" style="width:78%"></div></div>
        <span class="beat-bar-pct avg">78%</span>
      </div>
    </div>
    <div class="beat-metric-block">
      <div class="beat-metric-label">Revenue Beat Rate</div>
      <div class="beat-bar-row">
        <span class="beat-bar-tag">Q1 2026</span>
        <div class="beat-bar-track"><div class="beat-bar-cur" style="width:77%"></div></div>
        <span class="beat-bar-pct cur">77%</span>
      </div>
      <div class="beat-bar-row">
        <span class="beat-bar-tag">5-yr avg</span>
        <div class="beat-bar-track"><div class="beat-bar-avg" style="width:70%"></div></div>
        <span class="beat-bar-pct avg">70%</span>
      </div>
    </div>
  </div>'''

# Replace from <div class="beat-chart"> to </div> (the closing of beat-chart)
html = a.content_html
new_html = re.sub(
    r'<div class="beat-chart">.*?</div>\s*\n\s*<div class="chart-note">',
    new_beat + '\n  <div class="chart-note">',
    html,
    flags=re.DOTALL
)

if new_html != html:
    a.content_html = new_html
    db.commit()
    print("Chart 2 updated successfully")
else:
    print("Regex did not match — check pattern")
    idx = html.find('beat-chart')
    print(repr(html[idx:idx+100]))
