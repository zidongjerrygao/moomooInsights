const API = "";

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
  }

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
    const items = data.indices || [];
    const html = items.map(i => {
      const cls = i.change_pct >= 0 ? "up" : "dn";
      const sign = i.change_pct >= 0 ? "+" : "";
      return `<span class="ticker-item">
        <span class="label">${i.symbol}</span>
        <span class="price">${formatPrice(i.price, i.symbol)}</span>
        <span class="${cls}">${sign}${i.change_pct.toFixed(2)}%</span>
      </span>`;
    }).join("");
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

// ── Article card ──────────────────────────────────────────────────────────────
function articleCardHTML(a) {
  return `
    <div class="article-card" onclick="location.href='article.html?id=${a.id}'">
      <div class="article-card-img-placeholder">${categoryEmoji(a.category)}</div>
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
    </div>`;
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
