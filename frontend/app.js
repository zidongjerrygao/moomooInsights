const API = (typeof Capacitor !== "undefined" && Capacitor.isNativePlatform())
  ? "https://moomooinsights-production.up.railway.app"
  : "";

// ── Auth helpers ──────────────────────────────────────────────────────────────
function getToken() { return localStorage.getItem("moomoo_token"); }
function getUser()  { try { return JSON.parse(localStorage.getItem("moomoo_user") || "null"); } catch { return null; } }
function isAdmin()  { const u = getUser(); return u && u.is_admin; }
function logout()   { localStorage.removeItem("moomoo_token"); localStorage.removeItem("moomoo_user"); location.href = "/index.html"; }

// ── Level system ──────────────────────────────────────────────────────────────
const LEVEL_NAMES = ["","Reader","Analyst","Researcher","Strategist","Investor","Trader","Pro","Expert","Master","Legend"];
function getLevel(minutes) { return Math.min(10, Math.floor((minutes || 0) / 100) + 1); }
function getLevelName(level) { return LEVEL_NAMES[level] || "Legend"; }
function getLevelProgress(minutes) {
  const m = minutes || 0;
  if (m >= 1000) return 100;
  return (m % 100);
}
function getMinutesToNext(minutes) {
  const m = minutes || 0;
  if (m >= 1000) return 0;
  const level = getLevel(m);
  return Math.ceil(level * 100 - m);
}

// ── Reading time tracker ──────────────────────────────────────────────────────
(function() {
  if (!getToken()) return;
  let sessionStart = null;
  let accumulated = 0;

  function startTimer() { if (!sessionStart) sessionStart = Date.now(); }
  function pauseTimer() {
    if (sessionStart) {
      accumulated += (Date.now() - sessionStart) / 1000;
      sessionStart = null;
    }
  }
  function flush(sync) {
    pauseTimer();
    const secs = accumulated;
    accumulated = 0;
    if (secs < 1 || !getToken()) return;
    const body = JSON.stringify({ seconds: secs });
    if (sync && navigator.sendBeacon) {
      const blob = new Blob([body], { type: "application/json" });
      navigator.sendBeacon(`${API}/api/users/reading-time`, blob);
    } else {
      apiFetch("/api/users/reading-time", { method: "POST", body }).then(updated => {
        if (updated) {
          const u = getUser();
          if (u) {
            u.reading_time_minutes = updated.reading_time_minutes;
            u.level = updated.level;
            localStorage.setItem("moomoo_user", JSON.stringify(u));
            renderPortal();
          }
        }
      }).catch(() => {});
    }
    startTimer();
  }

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) flush(true); else startTimer();
  });
  window.addEventListener("beforeunload", () => flush(true));
  setInterval(() => flush(false), 60000);
  if (!document.hidden) startTimer();
})();

async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options.headers };
  const res = await fetch(`${API}${path}`, { ...options, headers });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => null);
  if (!res.ok) throw new Error(data?.detail || `HTTP ${res.status}`);
  return data;
}

const apiGet    = (path)         => apiFetch(path);
const apiPost   = (path, body)   => apiFetch(path, { method: "POST",   body: JSON.stringify(body) });
const apiPut    = (path, body)   => apiFetch(path, { method: "PUT",    body: JSON.stringify(body) });
const apiDelete = (path)         => apiFetch(path, { method: "DELETE" });

// ── Nav ───────────────────────────────────────────────────────────────────────
function renderNav() {
  const user = getUser();
  const page = location.pathname.split("/").pop() || "index.html";
  const tFn = typeof t === "function" ? t : k => k;

  const links = [
    { href: "index.html",        key: "nav_news"        },
    { href: "markets.html",      key: "nav_markets"     },
    { href: "strategy.html",     key: "nav_strategy"    },
    { href: "trade.html",        key: "nav_trade"       },
    { href: "community.html",    key: "nav_community"   },
    { href: "talk-to-pro.html",  key: "nav_talk_to_pro" },
  ];

  const navLinks = document.getElementById("nav-links");
  const navActions = document.getElementById("nav-actions");
  const navUserInfo = document.getElementById("nav-user-info");
  const tickerBar = document.getElementById("ticker-bar");

  if (navLinks) {
    navLinks.innerHTML = links.map(l =>
      `<a href="${l.href}" class="${page === l.href ? "active" : ""}">${tFn(l.key)}</a>`
    ).join("");
    if (user?.is_admin) navLinks.innerHTML += `<a href="admin.html" class="${page === "admin.html" ? "active" : ""}">${tFn("nav_admin")}</a>`;

    // Close mobile nav when a link is clicked
    navLinks.querySelectorAll("a").forEach(a => a.addEventListener("click", () => navLinks.classList.remove("open")));
  }

  // Hamburger button for mobile
  if (!document.getElementById("nav-hamburger")) {
    const hamburger = document.createElement("button");
    hamburger.id = "nav-hamburger";
    hamburger.className = "nav-hamburger";
    hamburger.innerHTML = "&#9776;";
    hamburger.setAttribute("aria-label", "Menu");
    hamburger.addEventListener("click", e => {
      e.stopPropagation();
      document.getElementById("nav-links")?.classList.toggle("open");
    });
    document.querySelector(".nav-inner")?.appendChild(hamburger);
  }

  document.addEventListener("click", () => document.getElementById("nav-links")?.classList.remove("open"), { once: false });

  const langLabel = typeof getLangLabel === "function" ? getLangLabel(typeof getLang === "function" ? getLang() : "en") : "EN";
  const langSwitcher = `
    <div class="lang-switcher">
      <button class="lang-btn" onclick="toggleLangMenu(event)">${langLabel} ▾</button>
      <div class="lang-menu" id="lang-menu">
        <div class="lang-option${(typeof getLang === "function" ? getLang() : "en") === "en" ? " active" : ""}" onclick="switchLang('en')">English</div>
        <div class="lang-option${(typeof getLang === "function" ? getLang() : "") === "zh-cn" ? " active" : ""}" onclick="switchLang('zh-cn')">简体中文</div>
        <div class="lang-option${(typeof getLang === "function" ? getLang() : "") === "zh-hk" ? " active" : ""}" onclick="switchLang('zh-hk')">繁體中文</div>
      </div>
    </div>`;

  if (navUserInfo && navActions) {
    if (user) {
      navUserInfo.innerHTML = "";
      navActions.innerHTML = `${langSwitcher}<div id="portal-wrapper"></div>`;
      renderPortal();
    } else {
      navUserInfo.innerHTML = "";
      navActions.innerHTML = `
        ${langSwitcher}
        <a href="login.html" class="btn btn-outline btn-sm">${tFn("nav_login")}</a>
        <a href="login.html?tab=register" class="btn btn-primary btn-sm">${tFn("nav_signup")}</a>
      `;
    }
  }

  if (tickerBar) loadTickerBar(tickerBar);
}

// ── Portal ────────────────────────────────────────────────────────────────────
function renderPortal() {
  const wrapper = document.getElementById("portal-wrapper");
  if (!wrapper) return;
  const user = getUser();
  if (!user) return;

  const tFn = typeof t === "function" ? t : k => k;
  const minutes = user.reading_time_minutes || 0;
  const level = user.level || getLevel(minutes);
  const levelName = getLevelName(level);
  const progress = getLevelProgress(minutes);
  const toNext = getMinutesToNext(minutes);
  const initials = (user.display_name || user.email || "?").charAt(0).toUpperCase();
  const timeLabel = minutes >= 60 ? (minutes / 60).toFixed(1) + " " + tFn("portal_hrs") : Math.round(minutes) + " " + tFn("portal_min");

  wrapper.innerHTML = `
    <div style="position:relative;">
      <button class="portal-btn" id="portal-toggle" onclick="togglePortal(event)">
        <div class="portal-avatar">${initials}</div>
        <span>Lv.${level}</span>
        <span class="portal-level-badge">${levelName}</span>
      </button>
      <div class="portal-dropdown" id="portal-dropdown">
        <div class="portal-user-header">
          <div class="portal-avatar-lg">${initials}</div>
          <div>
            <div class="portal-user-name">${user.display_name || user.email.split("@")[0]}</div>
            <div class="portal-user-email">${user.email}</div>
          </div>
        </div>
        <div class="portal-level-section">
          <div class="portal-level-row">
            <div>
              <span class="portal-level-num">Level ${level}</span>
              <span class="portal-level-name" style="margin-left:8px;">${levelName}</span>
            </div>
            ${level < 10 ? `<span class="portal-level-next">${toNext} ${tFn("portal_min_to_lv")}${level + 1}</span>` : `<span class="portal-level-next" style="color:var(--orange);">${tFn("portal_max_level")}</span>`}
          </div>
          <div class="portal-progress-track">
            <div class="portal-progress-fill" style="width:${progress}%"></div>
          </div>
          <div class="portal-progress-label">
            <span>${level < 10 ? Math.floor(minutes % 100) : 100} / 100 ${tFn("portal_min")}</span>
            <span>${level < 10 ? "Lv." + (level + 1) + " — " + getLevelName(level + 1) : tFn("portal_legend_tier")}</span>
          </div>
        </div>
        <hr class="portal-divider">
        <div class="portal-stat-row">
          <span class="portal-stat-label">${tFn("portal_total_time")}</span>
          <span class="portal-stat-val">${timeLabel}</span>
        </div>
        <div class="portal-stat-row">
          <span class="portal-stat-label">${tFn("portal_rank")}</span>
          <span class="portal-stat-val">${levelName}</span>
        </div>
        ${user.is_admin ? `<div class="portal-stat-row"><span class="portal-stat-label">${tFn("portal_role")}</span><span class="portal-stat-val" style="color:var(--orange);">${tFn("portal_admin_role")}</span></div>` : ""}
        ${!user.is_premium ? `
        <a href="payment.html" class="portal-premium-btn">
          <span>⭐ ${tFn("portal_upgrade")}</span>
          <span class="portal-premium-badge">PRO</span>
        </a>` : `
        <div class="portal-premium-active">${tFn("portal_premium_member")}</div>`}
        <button class="portal-logout-btn" onclick="logout()">${tFn("portal_sign_out")}</button>
      </div>
    </div>
  `;
}

function togglePortal(e) {
  e.stopPropagation();
  document.getElementById("portal-dropdown")?.classList.toggle("open");
}

document.addEventListener("click", e => {
  if (!e.target.closest("#portal-wrapper")) {
    document.getElementById("portal-dropdown")?.classList.remove("open");
  }
});

// ── Ticker bar ────────────────────────────────────────────────────────────────
async function loadTickerBar(container) {
  try {
    const data = await apiGet("/api/markets");
    const indices = (data.indices || []).map(i => {
      const cls  = i.change_pct >= 0 ? "up" : "dn";
      const sign = i.change_pct >= 0 ? "+" : "";
      return `<span class="ticker-item">
        <span class="label">${i.symbol}</span>
        <span class="price">${formatPrice(i.price, i.symbol)}</span>
        <span class="${cls}">${sign}${i.change_pct.toFixed(2)}%</span>
      </span>`;
    });
    const yields = (data.treasuries || []).map(y => {
      const cls  = y.change >= 0 ? "up" : "dn";
      const sign = y.change >= 0 ? "+" : "";
      return `<span class="ticker-item">
        <span class="label">${y.label}</span>
        <span class="price">${y.rate.toFixed(2)}%</span>
        <span class="${cls}">${sign}${y.change.toFixed(3)}</span>
      </span>`;
    });
    const html = [...indices, ...yields].join("");
    // duplicate for seamless loop
    container.innerHTML = `<div class="ticker-scroll">${html}${html}</div>`;
  } catch {
    container.innerHTML = `<div class="ticker-scroll"><span class="ticker-item"><span class="label">Markets data loading...</span></span></div>`;
  }
}

function formatPrice(price, symbol) {
  if (!price) return "-";
  if (symbol === "USDSGD") return price.toFixed(4);
  if (price > 10000) return price.toLocaleString("en-US", { maximumFractionDigits: 0 });
  return price.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// ── Toast ─────────────────────────────────────────────────────────────────────
function toast(msg, type = "default") {
  let container = document.querySelector(".toast-container");
  if (!container) {
    container = document.createElement("div");
    container.className = "toast-container";
    document.body.appendChild(container);
  }
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = msg;
  container.appendChild(el);
  setTimeout(() => el.remove(), 3500);
}

// ── Format helpers ────────────────────────────────────────────────────────────
function formatDate(d) {
  if (!d) return "";
  return new Date(d).toLocaleDateString("en-SG", { year: "numeric", month: "short", day: "numeric" });
}

function formatRev(v) {
  if (!v) return "-";
  if (v >= 1e12) return `$${(v / 1e12).toFixed(2)}T`;
  if (v >= 1e9)  return `$${(v / 1e9).toFixed(2)}B`;
  if (v >= 1e6)  return `$${(v / 1e6).toFixed(0)}M`;
  return `$${v.toFixed(0)}`;
}

function surpriseColor(pct) {
  if (pct == null) return "";
  return pct > 0 ? "td-up" : "td-dn";
}

// ── Modal helpers ─────────────────────────────────────────────────────────────
function openModal(id)  { document.getElementById(id)?.classList.add("open"); }
function closeModal(id) { document.getElementById(id)?.classList.remove("open"); }

// Close modal on overlay click
document.addEventListener("click", e => {
  if (e.target.classList.contains("modal-overlay")) {
    e.target.classList.remove("open");
  }
});

// ── Dynamic thumbnail SVG ─────────────────────────────────────────────────────
const THUMB_TICKER = {
  AAPL:{g1:'#1d1d1f',g2:'#2d2d2f',ac:'#f5f5f7'},
  MSFT:{g1:'#0058a0',g2:'#003f74',ac:'#50e6ff'},
  NVDA:{g1:'#1a3a00',g2:'#2d5c00',ac:'#76b900'},
  AMZN:{g1:'#b36900',g2:'#7a4800',ac:'#ff9900'},
  META:{g1:'#1877f2',g2:'#0a4fa0',ac:'#a8c8ff'},
  GOOGL:{g1:'#1a73e8',g2:'#0d47a1',ac:'#f9ab00'},
  TSLA:{g1:'#b30000',g2:'#7a0000',ac:'#ff6666'},
  JPM:{g1:'#003087',g2:'#001a4d',ac:'#4a90d9'},
  MCD:{g1:'#da291c',g2:'#9a1a10',ac:'#ffbc0d'},
  CSCO:{g1:'#049fd9',g2:'#0270a0',ac:'#a0e4f8'},
  AMD:{g1:'#ed1c24',g2:'#a01018',ac:'#fff'},
  NFLX:{g1:'#e50914',g2:'#8c0610',ac:'#fff'},
  AVGO:{g1:'#cc2200',g2:'#801400',ac:'#ff9966'},
  ORCL:{g1:'#c74634',g2:'#8a2818',ac:'#f8c85c'},
  QCOM:{g1:'#3253dc',g2:'#1a37aa',ac:'#a0b4ff'},
  CRM:{g1:'#009edb',g2:'#006c99',ac:'#fff'},
  WMT:{g1:'#0071ce',g2:'#004c8c',ac:'#ffc220'},
  UNH:{g1:'#002677',g2:'#001040',ac:'#00bcd4'},
  HD:{g1:'#f96302',g2:'#c04800',ac:'#fff'},
  GS:{g1:'#1a2b5e',g2:'#0d1b3e',ac:'#7eb6ff'},
  MS:{g1:'#003087',g2:'#001550',ac:'#6ea8ff'},
  BAC:{g1:'#c42126',g2:'#8a1218',ac:'#fff'},
  LLY:{g1:'#c02832',g2:'#8a1a20',ac:'#f9a825'},
  INTU:{g1:'#365ebf',g2:'#1e3e8c',ac:'#00b0f5'},
  NOW:{g1:'#2e9b3f',g2:'#1a6828',ac:'#fff'},
  ISRG:{g1:'#005b99',g2:'#003d66',ac:'#7ecfff'},
  GE:{g1:'#005f87',g2:'#003d5c',ac:'#4db8ff'},
  CAT:{g1:'#ffb200',g2:'#cc8e00',ac:'#fff'},
  RTX:{g1:'#003087',g2:'#001550',ac:'#a0c4ff'},
  SPGI:{g1:'#0057a8',g2:'#003d7a',ac:'#7ec8ff'},
  AXP:{g1:'#006fcf',g2:'#004c9b',ac:'#fff'},
  ACN:{g1:'#a100ff',g2:'#7000b3',ac:'#e0b3ff'},
  TXN:{g1:'#c1121f',g2:'#8a0d16',ac:'#ffb3b8'},
  LIN:{g1:'#009de0',g2:'#006ea8',ac:'#fff'},
  ABT:{g1:'#0070c9',g2:'#004d8c',ac:'#7ec8ff'},
  TMO:{g1:'#0e4da4',g2:'#093580',ac:'#7eb6ff'},
  WFC:{g1:'#d71921',g2:'#9e1219',ac:'#fff'},
  XOM:{g1:'#c02424',g2:'#8a1a1a',ac:'#ffb3b3'},
  CVX:{g1:'#1c4c9c',g2:'#102e6a',ac:'#7eb6ff'},
  KO:{g1:'#f40009',g2:'#b00007',ac:'#fff'},
  PEP:{g1:'#004b87',g2:'#003060',ac:'#7eb6ff'},
  ABBV:{g1:'#071d49',g2:'#040f2a',ac:'#7eb6ff'},
  MRK:{g1:'#00857c',g2:'#005c55',ac:'#7efff9'},
  PG:{g1:'#003590',g2:'#002060',ac:'#7eaaff'},
  JNJ:{g1:'#c8102e',g2:'#8c0b20',ac:'#fff'},
  V:{g1:'#1a1f71',g2:'#0e1250',ac:'#f7b600'},
  MA:{g1:'#eb001b',g2:'#a00013',ac:'#f79e1b'},
  COST:{g1:'#005daa',g2:'#003d77',ac:'#fff'},
  BRK:{g1:'#1a2b5e',g2:'#0d1b3e',ac:'#c4a747'},
};
const THUMB_CAT = {
  'Daily Brief':    {g1:'#1a2035',g2:'#0f1628',ac:'#ff6b00',lb:'Daily Brief'},
  'Earnings':       {g1:'#1e3a5f',g2:'#0f2744',ac:'#fbbf24',lb:'Earnings'},
  'Macro':          {g1:'#0f2744',g2:'#0a1a30',ac:'#60a5fa',lb:'Macro'},
  'Equity':         {g1:'#064e3b',g2:'#043a2b',ac:'#34d399',lb:'Equity'},
  'Credit':         {g1:'#1e1b4b',g2:'#14123a',ac:'#a78bfa',lb:'Credit'},
  'Market Analysis':{g1:'#0c4a6e',g2:'#073549',ac:'#38bdf8',lb:'Market Analysis'},
  'TSLA':           {g1:'#b30000',g2:'#7a0000',ac:'#ff6666',lb:'TSLA'},
  'NVDA':           {g1:'#1a3a00',g2:'#2d5c00',ac:'#76b900',lb:'NVDA'},
  'Strategy':       {g1:'#2d1b4e',g2:'#1a0f30',ac:'#c084fc',lb:'Strategy'},
  'Sector':         {g1:'#1e3a2f',g2:'#0f2420',ac:'#4ade80',lb:'Sector'},
  'Trade Plan':     {g1:'#1a1f3c',g2:'#10142a',ac:'#f97316',lb:'Trade Plan'},
};

function articleThumbnailSVG(article) {
  const title = article.title || '';
  const excerpt = article.excerpt || '';
  const cat = article.category || '';
  const id = article.id || 0;

  // Resolve theme: try to extract ticker from title first
  let theme = THUMB_CAT[cat] || THUMB_CAT['Daily Brief'];
  let mainText = theme.lb;
  let subText = '';
  let iconPath = '';

  // Extract ticker from earnings/trade titles (e.g. "NVDA Earnings Review...")
  const tickerM = title.match(/^([A-Z]{2,5})[\s:]/);
  if (tickerM && THUMB_TICKER[tickerM[1]]) {
    const t = THUMB_TICKER[tickerM[1]];
    theme = {g1:t.g1, g2:t.g2, ac:t.ac, lb:tickerM[1]};
    mainText = tickerM[1];
  } else if (['TSLA','NVDA'].includes(cat) && THUMB_TICKER[cat]) {
    const t = THUMB_TICKER[cat];
    theme = {g1:t.g1, g2:t.g2, ac:t.ac, lb:cat};
    mainText = cat;
  }

  // For Daily Brief: extract date from title for subText
  if (cat === 'Daily Brief') {
    const dm = title.match(/[—–-]\s*(.{4,20}?)(?:\s*$)/);
    if (dm) subText = dm[1].trim();
  }

  // For Earnings: try to pull EPS/revenue number from excerpt
  if (cat === 'Earnings') {
    const epsM = (excerpt + ' ' + title).match(/\$?([\d.]+[BM]?\s*(?:EPS|Revenue|Rev|billion|million)?)/i);
    if (epsM) subText = epsM[0].trim().slice(0, 18);
    else subText = title.match(/Preview|Review/i) ? (title.includes('Preview') ? 'EARNINGS PREVIEW' : 'EARNINGS REVIEW') : '';
  }

  // Seeded decorative bars
  const bars = Array.from({length:12}, (_, i) => 15 + ((id*7+i*17+i*i*3)%100+100)%100*0.6);
  const bw=11, bgap=4, bx0=200-bars.length*(bw+bgap)/2, baseY=168;
  const uid = `m${id}`;

  const mainFs = mainText.length > 9 ? 26 : mainText.length > 6 ? 34 : mainText.length > 4 ? 40 : 50;
  const mainY = subText ? 83 : 90;
  const catLb = (THUMB_CAT[cat]||THUMB_CAT['Daily Brief']).lb;
  const pillW = catLb.length * 7.5 + 20;

  // Up/down arrow for Daily Brief
  const arrow = cat === 'Daily Brief'
    ? `<polygon points="200,52 215,70 205,70 205,82 195,82 195,70 185,70" fill="${theme.ac}" opacity="0.3"/>`
    : '';

  return `<svg viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" style="display:block;pointer-events:none;" preserveAspectRatio="none">
<defs>
  <linearGradient id="bg${uid}" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="${theme.g1}"/><stop offset="100%" stop-color="${theme.g2}"/></linearGradient>
  <linearGradient id="fd${uid}" x1="0%" y1="30%" x2="0%" y2="100%"><stop offset="0%" stop-color="${theme.g2}" stop-opacity="0"/><stop offset="100%" stop-color="${theme.g1}" stop-opacity="0.9"/></linearGradient>
</defs>
<rect width="400" height="180" fill="url(#bg${uid})"/>
<circle cx="370" cy="-5" r="60" fill="${theme.ac}" opacity="0.10"/>
<circle cx="15" cy="185" r="50" fill="${theme.ac}" opacity="0.07"/>
${Array.from({length:4},(_,r)=>Array.from({length:9},(_,c)=>`<circle cx="${c*50+25}" cy="${r*60+30}" r="1" fill="${theme.ac}" opacity="0.08"/>`).join('')).join('')}
${bars.map((h,i)=>{const bh=h*0.62,x=bx0+i*(bw+bgap);return `<rect x="${x.toFixed(1)}" y="${(baseY-bh).toFixed(1)}" width="${bw}" height="${bh.toFixed(1)}" fill="${i%4===1?theme.ac:'#fff'}" opacity="${(0.15+i/bars.length*0.40).toFixed(2)}" rx="2"/>`;}).join('')}
<rect width="400" height="180" fill="url(#fd${uid})"/>
<rect x="10" y="10" width="${pillW.toFixed(1)}" height="22" rx="4" fill="${theme.ac}" opacity="0.25"/>
<text x="${(10 + pillW / 2).toFixed(1)}" y="25" font-family="system-ui,sans-serif" font-size="11" font-weight="700" fill="${theme.ac}" text-anchor="middle" letter-spacing="0.5">${catLb}</text>
${arrow}
<text x="200" y="${mainY}" font-family="system-ui,sans-serif" font-size="${mainFs}" font-weight="900" fill="white" text-anchor="middle" dominant-baseline="middle" letter-spacing="2" opacity="0.95">${mainText}</text>
${subText ? `<text x="200" y="${mainY + mainFs*0.68}" font-family="system-ui,sans-serif" font-size="11" fill="white" text-anchor="middle" dominant-baseline="middle" opacity="0.65" letter-spacing="0.5">${subText}</text>` : ''}
<text x="392" y="172" font-family="system-ui,sans-serif" font-size="10" font-weight="600" fill="white" text-anchor="end" opacity="0.3">Moomoo Insights</text>
</svg>`;
}

// ── Article card ──────────────────────────────────────────────────────────────
function articleCardHTML(a) {
  return `
    <a href="article.html?id=${a.id}" class="article-card" style="text-decoration:none;color:inherit;display:flex;flex-direction:column;">
      <div class="article-card-img-placeholder" style="padding:0;overflow:hidden;">${articleThumbnailSVG(a)}</div>
      <div class="article-card-body">
        <div class="article-card-category">${a.category || "Market Analysis"}</div>
        <div class="article-card-title">${a.title}</div>
        <div class="article-card-excerpt">${a.excerpt || ""}</div>
        <div class="article-card-meta">
          <span>${a.author || "Moomoo Insights"}</span>
          <span class="dot">·</span>
          <span>${formatDate(a.created_at)}</span>
        </div>
      </div>
    </a>`;
}

function categoryEmoji(cat) {
  const map = {
    "Market Analysis": "📊", "Earnings": "💰", "Economy": "🌐",
    "Tech": "💻", "Energy": "⚡", "Healthcare": "🏥",
    "Finance": "🏦", "SG Market": "🇸🇬", "US Market": "🇺🇸",
    "Macro": "🌐", "Equity": "📈", "Credit": "💳",
    "TSLA": "🚗", "NVDA": "🟢",
  };
  return map[cat] || "📰";
}

// ── Init ──────────────────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", renderNav);
