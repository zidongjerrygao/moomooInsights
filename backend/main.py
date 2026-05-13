import json
import logging
import re
import smtplib
import ssl
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional, List

import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
import stripe
import anthropic as _anthropic

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
_ANTHROPIC_KEY  = os.getenv("ANTHROPIC_API_KEY", "")
_DEEPSEEK_KEY   = os.getenv("DEEPSEEK_API_KEY", "")
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from models import (
    init_db, get_db, SessionLocal, User, Article, CommunityPost, Comment,
    Company, EarningsRelease, EmailSubscriber, EmailSendLog,
)
from auth import (
    hash_password, verify_password, create_token,
    get_current_user, require_user, require_admin,
)
from markets import get_market_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Moomoo Insights", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── helpers ───────────────────────────────────────────────────────────────────

def _slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    return s[:120]


def _article_dict(a: Article) -> dict:
    return {
        "id": a.id,
        "title": a.title,
        "slug": a.slug,
        "excerpt": a.excerpt,
        "content_html": a.content_html,
        "tags": a.tags or [],
        "category": a.category,
        "author": a.author,
        "published": a.published,
        "featured": a.featured,
        "cover_image": a.cover_image,
        "title_zh_cn": a.title_zh_cn,
        "excerpt_zh_cn": a.excerpt_zh_cn,
        "content_html_zh_cn": a.content_html_zh_cn,
        "title_zh_hk": a.title_zh_hk,
        "excerpt_zh_hk": a.excerpt_zh_hk,
        "content_html_zh_hk": a.content_html_zh_hk,
        "created_at": a.created_at.isoformat() if a.created_at else None,
        "updated_at": a.updated_at.isoformat() if a.updated_at else None,
    }


def _post_dict(p: CommunityPost, include_comments=False) -> dict:
    d = {
        "id": p.id,
        "title": p.title,
        "body": p.body,
        "category": p.category,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "author": p.user.display_name or p.user.email.split("@")[0] if p.user else "Unknown",
        "comment_count": len(p.comments),
    }
    if include_comments:
        d["post_user_id"] = p.user_id
        d["comments"] = [
            {
                "id": c.id,
                "body": c.body,
                "user_id": c.user_id,
                "author": c.user.display_name or c.user.email.split("@")[0] if c.user else "Unknown",
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in p.comments
        ]
    return d


def _release_dict(r: EarningsRelease) -> dict:
    return {
        "id": r.id,
        "ticker": r.company.ticker,
        "name": r.company.name,
        "sector": r.company.sector,
        "report_date": r.report_date,
        "fiscal_quarter": r.fiscal_quarter,
        "eps_actual": r.eps_actual,
        "eps_estimate": r.eps_estimate,
        "eps_surprise_pct": r.eps_surprise_pct,
        "revenue_actual": r.revenue_actual,
        "revenue_estimate": r.revenue_estimate,
        "revenue_surprise_pct": r.revenue_surprise_pct,
        "stock_price_before": r.stock_price_before,
        "stock_price_after": r.stock_price_after,
        "stock_reaction_pct": r.stock_reaction_pct,
        "guidance": r.guidance,
        "is_manual_override": r.is_manual_override,
        "updated_at": r.updated_at.isoformat() if r.updated_at else None,
    }


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class RegisterIn(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None


class ArticleIn(BaseModel):
    title: str
    excerpt: Optional[str] = None
    content_html: str
    tags: Optional[List[str]] = []
    category: Optional[str] = "Market Analysis"
    author: Optional[str] = "Moomoo Insights"
    published: Optional[bool] = True
    featured: Optional[bool] = False
    cover_image: Optional[str] = None
    title_zh_cn: Optional[str] = None
    excerpt_zh_cn: Optional[str] = None
    content_html_zh_cn: Optional[str] = None
    title_zh_hk: Optional[str] = None
    excerpt_zh_hk: Optional[str] = None
    content_html_zh_hk: Optional[str] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content_html: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    author: Optional[str] = None
    published: Optional[bool] = None
    featured: Optional[bool] = None
    cover_image: Optional[str] = None
    title_zh_cn: Optional[str] = None
    excerpt_zh_cn: Optional[str] = None
    content_html_zh_cn: Optional[str] = None
    title_zh_hk: Optional[str] = None
    excerpt_zh_hk: Optional[str] = None
    content_html_zh_hk: Optional[str] = None


class PostIn(BaseModel):
    title: str
    body: str
    category: Optional[str] = "General"


class CommentIn(BaseModel):
    body: str


class EarningsCreate(BaseModel):
    ticker: str
    report_date: str
    fiscal_quarter: Optional[str] = None
    eps_actual: Optional[float] = None
    eps_estimate: Optional[float] = None
    eps_surprise_pct: Optional[float] = None
    revenue_actual: Optional[float] = None
    revenue_estimate: Optional[float] = None
    revenue_surprise_pct: Optional[float] = None
    stock_price_before: Optional[float] = None
    stock_price_after: Optional[float] = None
    stock_reaction_pct: Optional[float] = None
    guidance: Optional[str] = None
    is_manual_override: bool = True


class EarningsUpdate(BaseModel):
    report_date: Optional[str] = None
    fiscal_quarter: Optional[str] = None
    eps_actual: Optional[float] = None
    eps_estimate: Optional[float] = None
    eps_surprise_pct: Optional[float] = None
    revenue_actual: Optional[float] = None
    revenue_estimate: Optional[float] = None
    revenue_surprise_pct: Optional[float] = None
    stock_price_before: Optional[float] = None
    stock_price_after: Optional[float] = None
    stock_reaction_pct: Optional[float] = None
    guidance: Optional[str] = None
    is_manual_override: Optional[bool] = None


# ── Auth routes ───────────────────────────────────────────────────────────────

def _user_dict(user: User) -> dict:
    minutes = user.reading_time_minutes or 0.0
    level = min(10, int(minutes // 100) + 1)
    return {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "is_admin": user.is_admin,
        "reading_time_minutes": round(minutes, 1),
        "level": level,
        "is_premium": bool(user.is_premium),
    }


@app.post("/auth/register", status_code=201)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email.lower()).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    is_first = db.query(User).count() == 0
    user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
        display_name=payload.display_name or payload.email.split("@")[0],
        is_admin=is_first,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"token": create_token(user.id), "user": _user_dict(user)}


@app.post("/auth/login")
def login(payload: RegisterIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": create_token(user.id), "user": _user_dict(user)}


@app.get("/auth/me")
def me(user: User = Depends(require_user)):
    return _user_dict(user)


class ReadingTimeIn(BaseModel):
    seconds: float


@app.post("/api/users/reading-time")
def add_reading_time(payload: ReadingTimeIn, user: User = Depends(require_user), db: Session = Depends(get_db)):
    if payload.seconds <= 0:
        return _user_dict(user)
    u = db.query(User).filter(User.id == user.id).first()
    u.reading_time_minutes = (u.reading_time_minutes or 0.0) + payload.seconds / 60.0
    db.commit()
    db.refresh(u)
    return _user_dict(u)


# ── Markets ───────────────────────────────────────────────────────────────────

@app.get("/api/markets")
def markets():
    return get_market_data()


# ── Articles ──────────────────────────────────────────────────────────────────

@app.get("/api/articles")
def list_articles(
    category: Optional[str] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    q = db.query(Article).filter(Article.published == True)
    if category:
        q = q.filter(Article.category == category)
    if featured is not None:
        q = q.filter(Article.featured == featured)
    articles = q.order_by(Article.created_at.desc()).all()
    return [_article_dict(a) for a in articles]


@app.get("/api/articles/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
    a = db.query(Article).filter(Article.id == article_id).first()
    if not a:
        raise HTTPException(404, "Article not found")
    return _article_dict(a)


@app.get("/api/articles/by-slug/{slug}")
def get_article_by_slug(slug: str, db: Session = Depends(get_db)):
    a = db.query(Article).filter(Article.slug == slug).first()
    if not a:
        raise HTTPException(404, "Article not found")
    return _article_dict(a)


@app.post("/api/articles", status_code=201)
def create_article(payload: ArticleIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    base_slug = _slugify(payload.title)
    slug = base_slug
    n = 1
    while db.query(Article).filter(Article.slug == slug).first():
        slug = f"{base_slug}-{n}"
        n += 1
    a = Article(slug=slug, **payload.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return _article_dict(a)


@app.put("/api/articles/{article_id}")
def update_article(article_id: int, payload: ArticleUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    a = db.query(Article).filter(Article.id == article_id).first()
    if not a:
        raise HTTPException(404, "Not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(a, field, value)
    a.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(a)
    return _article_dict(a)


@app.delete("/api/articles/{article_id}", status_code=204)
def delete_article(article_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    a = db.query(Article).filter(Article.id == article_id).first()
    if not a:
        raise HTTPException(404, "Not found")
    db.delete(a)
    db.commit()


# ── Community ─────────────────────────────────────────────────────────────────

@app.get("/api/community")
def list_posts(category: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(CommunityPost)
    if category:
        q = q.filter(CommunityPost.category == category)
    posts = q.order_by(CommunityPost.created_at.desc()).all()
    return [_post_dict(p) for p in posts]


@app.get("/api/community/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    p = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not p:
        raise HTTPException(404, "Post not found")
    return _post_dict(p, include_comments=True)


@app.post("/api/community", status_code=201)
def create_post(payload: PostIn, db: Session = Depends(get_db), user: User = Depends(require_user)):
    p = CommunityPost(user_id=user.id, **payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return _post_dict(p)


@app.delete("/api/community/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    p = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not p:
        raise HTTPException(404, "Post not found")
    if not (user.is_admin or p.user_id == user.id):
        raise HTTPException(403, "Not authorized")
    db.delete(p)
    db.commit()


@app.post("/api/community/{post_id}/comments", status_code=201)
def add_comment(post_id: int, payload: CommentIn, db: Session = Depends(get_db), user: User = Depends(require_user)):
    p = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not p:
        raise HTTPException(404, "Post not found")
    c = Comment(post_id=post_id, user_id=user.id, body=payload.body)
    db.add(c)
    db.commit()
    return {"status": "ok"}


@app.delete("/api/community/{post_id}/comments/{comment_id}", status_code=204)
def delete_comment(post_id: int, comment_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
    c = db.query(Comment).filter(Comment.id == comment_id, Comment.post_id == post_id).first()
    if not c:
        raise HTTPException(404, "Comment not found")
    post = db.query(CommunityPost).filter(CommunityPost.id == post_id).first()
    if not (user.is_admin or c.user_id == user.id or post.user_id == user.id):
        raise HTTPException(403, "Not authorized")
    db.delete(c)
    db.commit()


# ── Earnings ──────────────────────────────────────────────────────────────────

@app.get("/api/earnings")
def list_earnings(
    ticker: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    upcoming: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    q = db.query(EarningsRelease).join(Company)
    if ticker:
        q = q.filter(Company.ticker == ticker.upper())
    if from_date:
        q = q.filter(EarningsRelease.report_date >= from_date)
    if to_date:
        q = q.filter(EarningsRelease.report_date <= to_date)
    if upcoming is True:
        q = q.filter(EarningsRelease.report_date >= today)
    elif upcoming is False:
        q = q.filter(EarningsRelease.report_date < today)
    order = EarningsRelease.report_date.asc() if upcoming is True else EarningsRelease.report_date.desc()
    releases = q.order_by(order).all()
    return [_release_dict(r) for r in releases]


@app.get("/api/earnings/{release_id}")
def get_earning(release_id: int, db: Session = Depends(get_db)):
    r = db.query(EarningsRelease).filter(EarningsRelease.id == release_id).first()
    if not r:
        raise HTTPException(404, "Not found")
    return _release_dict(r)


@app.post("/api/earnings", status_code=201)
def create_earning(payload: EarningsCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    company = db.query(Company).filter(Company.ticker == payload.ticker.upper()).first()
    if not company:
        raise HTTPException(404, f"Ticker {payload.ticker} not in watchlist")
    r = EarningsRelease(company_id=company.id, **{k: v for k, v in payload.model_dump().items() if k != "ticker"})
    db.add(r)
    db.commit()
    db.refresh(r)
    return _release_dict(r)


@app.put("/api/earnings/{release_id}")
def update_earning(release_id: int, payload: EarningsUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    r = db.query(EarningsRelease).filter(EarningsRelease.id == release_id).first()
    if not r:
        raise HTTPException(404, "Not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(r, field, value)
    r.is_manual_override = True
    r.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(r)
    return _release_dict(r)


@app.delete("/api/earnings/{release_id}", status_code=204)
def delete_earning(release_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    r = db.query(EarningsRelease).filter(EarningsRelease.id == release_id).first()
    if not r:
        raise HTTPException(404, "Not found")
    db.delete(r)
    db.commit()


@app.get("/api/companies")
def list_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).order_by(Company.weight_pct.desc()).all()
    return [{"id": c.id, "ticker": c.ticker, "name": c.name, "sector": c.sector, "weight_pct": c.weight_pct} for c in companies]


class CompanyIn(BaseModel):
    ticker: str
    name: str
    sector: Optional[str] = None
    weight_pct: Optional[float] = None


@app.post("/api/companies", status_code=201)
def create_company(payload: CompanyIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    existing = db.query(Company).filter(Company.ticker == payload.ticker.upper()).first()
    if existing:
        for field, value in payload.model_dump(exclude_unset=True).items():
            if field == "ticker":
                continue
            setattr(existing, field, value)
        db.commit()
        db.refresh(existing)
        return {"id": existing.id, "ticker": existing.ticker, "name": existing.name, "sector": existing.sector, "weight_pct": existing.weight_pct}
    c = Company(ticker=payload.ticker.upper(), name=payload.name, sector=payload.sector, weight_pct=payload.weight_pct or 0.0)
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "ticker": c.ticker, "name": c.name, "sector": c.sector, "weight_pct": c.weight_pct}


@app.get("/api/status")
def api_status():
    return {"server_time": datetime.utcnow().isoformat(), "status": "ok"}


# ── Stripe subscription ───────────────────────────────────────────────────────

STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
_FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8001")


@app.post("/api/stripe/create-checkout-session")
def create_checkout_session(user: User = Depends(require_user), db: Session = Depends(get_db)):
    if not stripe.api_key:
        raise HTTPException(500, "Stripe not configured")
    u = db.query(User).filter(User.id == user.id).first()
    customer_id = u.stripe_customer_id
    if not customer_id:
        customer = stripe.Customer.create(email=u.email, metadata={"user_id": u.id})
        u.stripe_customer_id = customer.id
        db.commit()
        customer_id = customer.id
    session = stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        line_items=[{"price": STRIPE_PRICE_ID, "quantity": 1}],
        success_url=f"{_FRONTEND_URL}/payment-success.html?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{_FRONTEND_URL}/payment.html?cancelled=1",
        allow_promotion_codes=True,
    )
    return {"url": session.url}


@app.post("/api/stripe/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
    except Exception:
        raise HTTPException(400, "Invalid signature")

    et = event["type"]
    if et in ("customer.subscription.created", "customer.subscription.updated"):
        sub = event["data"]["object"]
        customer_id = sub["customer"]
        active = sub["status"] in ("active", "trialing")
        u = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        if u:
            u.is_premium = active
            u.stripe_subscription_id = sub["id"]
            db.commit()
    elif et == "customer.subscription.deleted":
        sub = event["data"]["object"]
        u = db.query(User).filter(User.stripe_customer_id == sub["customer"]).first()
        if u:
            u.is_premium = False
            db.commit()
    return {"received": True}


# ── Email distribution ────────────────────────────────────────────────────────

_SMTP_HOST     = os.getenv("SMTP_HOST", "")
_SMTP_PORT     = int(os.getenv("SMTP_PORT", "587"))
_SMTP_USER     = os.getenv("SMTP_USER", "")
_SMTP_PASS     = os.getenv("SMTP_PASS", "")
_EMAIL_FROM    = os.getenv("EMAIL_FROM", _SMTP_USER)
_EMAIL_FROM_NAME = os.getenv("EMAIL_FROM_NAME", "Moomoo Insights")
_SITE_URL      = os.getenv("SITE_URL", os.getenv("FRONTEND_URL", "https://moomooinsights-production.up.railway.app"))

_BUNDLE_CATEGORIES = {
    "daily":    ["Macro", "Equity", "Credit", "Market Brief"],
    "strategy": ["Market Analysis", "Strategy"],
}
_BUNDLE_DAYS = {"daily": 2, "strategy": 7}
_BUNDLE_LABELS = {
    "daily":    "Daily Market Brief",
    "strategy": "Strategy & In-Depth Research",
}

CATEGORY_EMOJI_MAP = {
    "Macro": "🌍", "Equity": "📈", "Credit": "💳",
    "Market Analysis": "🔬", "Strategy": "♟️",
    "Earnings": "📊", "Market Brief": "📰",
}


def _build_email_html(bundle_type: str, articles: list, site_url: str) -> str:
    label = _BUNDLE_LABELS.get(bundle_type, bundle_type)
    today = datetime.utcnow().strftime("%B %-d, %Y") if os.name != "nt" else datetime.utcnow().strftime("%B %d, %Y")

    cards = ""
    for a in articles:
        emoji = CATEGORY_EMOJI_MAP.get(a["category"], "📄")
        excerpt = (a["excerpt"] or "")[:220]
        if len(a["excerpt"] or "") > 220:
            excerpt += "…"
        link = f"{site_url}/article.html?id={a['id']}"
        cards += f"""
        <tr>
          <td style="padding:0 0 20px 0;">
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e5e7eb;">
              <tr>
                <td style="background:linear-gradient(135deg,#1a1f3c 0%,#252b4a 100%);padding:14px 20px;">
                  <table width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td>
                        <span style="display:inline-block;background:#ff6900;color:#ffffff;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;padding:3px 8px;border-radius:4px;">{a['category']}</span>
                      </td>
                      <td align="right" style="font-size:22px;">{emoji}</td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr>
                <td style="padding:20px 20px 8px 20px;">
                  <p style="margin:0 0 10px 0;font-size:18px;font-weight:800;color:#1a1a1a;line-height:1.3;">{a['title']}</p>
                  <p style="margin:0 0 16px 0;font-size:14px;color:#4b5563;line-height:1.6;">{excerpt}</p>
                </td>
              </tr>
              <tr>
                <td style="padding:0 20px 20px 20px;">
                  <a href="{link}" style="display:inline-block;background:#ff6900;color:#ffffff;font-size:13px;font-weight:700;padding:9px 18px;border-radius:6px;text-decoration:none;letter-spacing:0.3px;">Read Full Article →</a>
                  <span style="font-size:11px;color:#9ca3af;margin-left:12px;">{a.get('author','Moomoo Insights')} · {a.get('created_at','')[:10]}</span>
                </td>
              </tr>
            </table>
          </td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{label} — Moomoo Insights</title></head>
<body style="margin:0;padding:0;background:#f1f5f9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f1f5f9;">
  <tr><td align="center" style="padding:32px 16px;">
    <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

      <!-- Header -->
      <tr><td style="background:linear-gradient(135deg,#1a1f3c 0%,#252b4a 100%);border-radius:14px 14px 0 0;padding:28px 32px;">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td>
              <span style="font-size:22px;font-weight:900;color:#ffffff;letter-spacing:-0.5px;">moomoo</span><span style="font-size:22px;font-weight:900;color:#ff6900;">Insights</span>
              <p style="margin:4px 0 0 0;font-size:12px;color:#64748b;letter-spacing:1px;text-transform:uppercase;">{label}</p>
            </td>
            <td align="right" valign="top">
              <p style="margin:0;font-size:12px;color:#64748b;">{today}</p>
            </td>
          </tr>
        </table>
      </td></tr>

      <!-- Intro strip -->
      <tr><td style="background:#ff6900;padding:12px 32px;">
        <p style="margin:0;font-size:13px;font-weight:700;color:#ffffff;">Your curated market intelligence — {len(articles)} article{'s' if len(articles) != 1 else ''} selected for you</p>
      </td></tr>

      <!-- Articles -->
      <tr><td style="padding:24px 24px 8px 24px;">
        <table width="100%" cellpadding="0" cellspacing="0">
          {cards}
        </table>
      </td></tr>

      <!-- CTA -->
      <tr><td style="padding:0 24px 24px 24px;text-align:center;">
        <a href="{site_url}" style="display:inline-block;border:2px solid #1a1f3c;color:#1a1f3c;font-size:13px;font-weight:700;padding:10px 24px;border-radius:8px;text-decoration:none;">View All Articles on Moomoo Insights →</a>
      </td></tr>

      <!-- Footer -->
      <tr><td style="background:#1a1f3c;border-radius:0 0 14px 14px;padding:20px 32px;text-align:center;">
        <p style="margin:0 0 6px 0;font-size:12px;color:#475569;">© 2026 Moomoo Insights · Exclusive Wealth Intelligence</p>
        <p style="margin:0;font-size:11px;color:#334155;line-height:1.5;">This email is for informational purposes only and does not constitute investment advice. Past performance is not indicative of future results.</p>
      </td></tr>

    </table>
  </td></tr>
</table>
</body>
</html>"""


def _send_email(to_addr: str, subject: str, html: str) -> None:
    if not _SMTP_HOST or not _SMTP_USER or not _SMTP_PASS:
        raise RuntimeError("SMTP not configured (set SMTP_HOST, SMTP_USER, SMTP_PASS env vars)")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{_EMAIL_FROM_NAME} <{_EMAIL_FROM}>"
    msg["To"] = to_addr
    msg.attach(MIMEText(html, "html"))
    ctx = ssl.create_default_context()
    port = _SMTP_PORT
    if port == 465:
        with smtplib.SMTP_SSL(_SMTP_HOST, port, context=ctx) as srv:
            srv.login(_SMTP_USER, _SMTP_PASS)
            srv.sendmail(_EMAIL_FROM, to_addr, msg.as_string())
    else:
        with smtplib.SMTP(_SMTP_HOST, port) as srv:
            srv.ehlo()
            srv.starttls(context=ctx)
            srv.login(_SMTP_USER, _SMTP_PASS)
            srv.sendmail(_EMAIL_FROM, to_addr, msg.as_string())


class SubscriberIn(BaseModel):
    email: str
    name: Optional[str] = None
    bundles: Optional[List[str]] = ["daily", "strategy"]


class SendBundleIn(BaseModel):
    bundle_type: str  # "daily" or "strategy"


@app.get("/api/admin/subscribers")
def list_subscribers(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    subs = db.query(EmailSubscriber).order_by(EmailSubscriber.created_at.desc()).all()
    return [{"id": s.id, "email": s.email, "name": s.name, "bundles": s.bundles or [], "active": s.active, "created_at": s.created_at.isoformat()} for s in subs]


@app.post("/api/admin/subscribers", status_code=201)
def add_subscriber(payload: SubscriberIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    existing = db.query(EmailSubscriber).filter(EmailSubscriber.email == payload.email.lower()).first()
    if existing:
        existing.name = payload.name or existing.name
        existing.bundles = payload.bundles
        existing.active = True
        db.commit()
        db.refresh(existing)
        return {"id": existing.id, "email": existing.email, "name": existing.name, "bundles": existing.bundles, "active": existing.active}
    s = EmailSubscriber(email=payload.email.lower(), name=payload.name, bundles=payload.bundles or ["daily", "strategy"])
    db.add(s)
    db.commit()
    db.refresh(s)
    return {"id": s.id, "email": s.email, "name": s.name, "bundles": s.bundles, "active": s.active}


@app.delete("/api/admin/subscribers/{sub_id}", status_code=204)
def remove_subscriber(sub_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    s = db.query(EmailSubscriber).filter(EmailSubscriber.id == sub_id).first()
    if not s:
        raise HTTPException(404, "Subscriber not found")
    db.delete(s)
    db.commit()


@app.post("/api/admin/email/send")
def send_bundle(payload: SendBundleIn, background_tasks: BackgroundTasks, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    bt = payload.bundle_type.lower()
    if bt not in _BUNDLE_CATEGORIES:
        raise HTTPException(400, f"bundle_type must be one of: {list(_BUNDLE_CATEGORIES)}")

    cats = _BUNDLE_CATEGORIES[bt]
    days = _BUNDLE_DAYS[bt]
    cutoff = datetime.utcnow() - timedelta(days=days)
    articles = (
        db.query(Article)
        .filter(Article.published == True, Article.category.in_(cats), Article.created_at >= cutoff)
        .order_by(Article.created_at.desc())
        .limit(8)
        .all()
    )
    if not articles:
        raise HTTPException(404, f"No articles found for bundle '{bt}' in the last {days} days")

    all_active = db.query(EmailSubscriber).filter(EmailSubscriber.active == True).all()
    subscribers = [s for s in all_active if bt in (s.bundles or [])]
    if not subscribers:
        raise HTTPException(404, "No active subscribers for this bundle")

    art_dicts = [_article_dict(a) for a in articles]
    label = _BUNDLE_LABELS[bt]
    subject = f"{label} — {datetime.utcnow().strftime('%b %d, %Y')} | Moomoo Insights"
    html = _build_email_html(bt, art_dicts, _SITE_URL)

    recipient_emails = [sub.email for sub in subscribers]

    log = EmailSendLog(
        bundle_type=bt, subject=subject,
        recipients_count=len(subscribers), articles_count=len(articles),
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    log_id = log.id

    def _dispatch():
        errors = []
        for email in recipient_emails:
            try:
                _send_email(email, subject, html)
            except Exception as exc:
                errors.append(f"{email}: {exc}")
        with SessionLocal() as s2:
            entry = s2.query(EmailSendLog).filter(EmailSendLog.id == log_id).first()
            if entry:
                entry.status = "error" if errors else "ok"
                entry.error = "\n".join(errors) if errors else None
                s2.commit()

    background_tasks.add_task(_dispatch)
    return {"status": "sending", "bundle": bt, "recipients": len(subscribers), "articles": len(articles), "subject": subject}


@app.get("/api/admin/email/logs")
def list_send_logs(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    logs = db.query(EmailSendLog).order_by(EmailSendLog.sent_at.desc()).limit(20).all()
    return [{"id": l.id, "bundle_type": l.bundle_type, "subject": l.subject, "recipients_count": l.recipients_count, "articles_count": l.articles_count, "sent_at": l.sent_at.isoformat(), "status": l.status, "error": l.error} for l in logs]


@app.post("/api/admin/email/test")
def test_email(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """Synchronous email test — returns the actual error immediately (not in background)."""
    cfg = {
        "SMTP_HOST": _SMTP_HOST or "(not set)",
        "SMTP_PORT": _SMTP_PORT,
        "SMTP_USER": _SMTP_USER or "(not set)",
        "SMTP_PASS": "***" if _SMTP_PASS else "(not set)",
        "EMAIL_FROM": _EMAIL_FROM or "(not set)",
    }
    if not _SMTP_HOST or not _SMTP_USER or not _SMTP_PASS:
        return {"ok": False, "config": cfg, "error": "SMTP env vars missing — set SMTP_HOST, SMTP_USER, SMTP_PASS in Railway"}
    try:
        _send_email(_SMTP_USER, "Moomoo Email Test", "<p>Email delivery is working ✓</p>")
        return {"ok": True, "config": cfg, "message": f"Test email sent to {_SMTP_USER}"}
    except Exception as e:
        return {"ok": False, "config": cfg, "error": str(e)}


# ── Talk to Pro — DeepSeek streaming chat with dual persona ───────────────────

_SYSTEM_CEMBALEST = """You are the Moomoo Investment Research Team's resident market strategist, \
responding in the analytical style of the Eye on the Market series.

PERSONA:
- Open with the sharpest observation first — a cultural reference, data paradox, or direct \
  challenge to consensus. Never a bland summary or preamble.
- Data-heavy and precise: cite specific figures inline (percentages, price levels, historical \
  comparisons). Never approximate when a number is available.
- Contrarian where the evidence supports it — never contrarian for its own sake.
- Acknowledge the bull case honestly before challenging it.
- Dry wit is permitted. Historical grounding is mandatory — anchor every forward claim to \
  historical context ("the last time this happened was…").
- One idea per paragraph, 3–5 sentences max. Close with either a specific indicator to watch \
  or an open tension the market will resolve.

TONE RULES:
- No investment-bank clichés: never say "cautiously optimistic", "headwinds persist", \
  "navigating uncertainty", or "compelling risk/reward".
- Precision over hedging: "Fed cuts are unlikely before Q3 2026 given core PCE path" beats \
  "rates may move in either direction".
- When you don't know something, say so directly and flag what data would resolve it.

SCOPE: equities, fixed income, macro, geopolitics, energy transition, AI productivity, \
fiscal sustainability, alternatives vs 60/40, FX, and commodities.
No personalised financial advice or individual security recommendations. \
Direct users to qualified advisors for portfolio decisions.

BRANDING: You represent Moomoo Insights. Never reference J.P. Morgan, JPMorgan, Chase, \
or any specific analyst by name."""

_SYSTEM_DBS = """You are the Moomoo Investment Strategy Team's chief strategist, \
responding in the style of Asia's leading private bank investment office.

PERSONA:
- Asia-first lens: US and Europe are always contextualized through their implications \
  for Asian investors. Address Asia ex-Japan first, then China/HK, then US, then Europe.
- Central framework is the Barbell Strategy: growth assets (AI infrastructure, Asian \
  consumption, selective EM equities) on one side; income/defensive assets (Asian IG bonds \
  2–5Y, dividend equities) on the other. Connect every recommendation to the Barbell.
- Directive language: "We advocate", "We favour", "We maintain our constructive view". \
  Never passive voice or hedged waffling.
- Structural vs. cyclical framing: always distinguish durable trends from temporary noise.
- Bifurcation is key: no broad market calls — always "winners vs. losers within the sector".

GEOGRAPHIC HIERARCHY (address in this order when relevant):
1. Asia ex-Japan — primary conviction region
2. China/Hong Kong — policy clarity and valuation are the two levers
3. Japan — neutral to cautious
4. US — sector bifurcation only, not broad index calls
5. Europe — typically underweight; energy cost drag, fiscal constraints

AI FRAMEWORK — always use this distinction:
- Infrastructure winners: proprietary data, mission-critical infrastructure, hyperscaler \
  networking, semiconductor supply chains
- Adapters at risk: labour-intensive IT services, standalone SaaS, creative software, \
  CRM/marketing automation with AI-native challengers

TONE RULES:
- Measured and intellectually honest — acknowledges complexity without doom-mongering.
- Quantify everything: ranges, spreads, allocation percentages, forecast horizons.
- Risks framed as "fragility" or "uncertainty", always paired with a positioning response.
- Tight paragraphs: 3–5 sentences max; one idea per paragraph.

SCOPE: Asia equities, global macro, fixed income (especially Asian IG credit), \
alternatives, gold, and asset allocation strategy.
No personalised financial advice. Direct users to qualified advisors.

BRANDING: You represent Moomoo Insights. Never reference DBS, DBS Bank, or DBS Private Bank."""

_CHAT_SYSTEMS = {"cembalest": _SYSTEM_CEMBALEST, "dbs": _SYSTEM_DBS}


class ChatRequest(BaseModel):
    messages: List[dict]
    mode: str = "cembalest"


@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    if not _DEEPSEEK_KEY:
        raise HTTPException(status_code=503, detail="DEEPSEEK_API_KEY not configured — set it in Railway environment variables")

    system = _CHAT_SYSTEMS.get(req.mode, _SYSTEM_CEMBALEST)
    safe_messages = [
        {"role": m["role"], "content": str(m["content"])}
        for m in req.messages
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]
    if not safe_messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    async def generate():
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=_DEEPSEEK_KEY, base_url="https://api.deepseek.com")
            stream = await client.chat.completions.create(
                model="deepseek-chat",
                max_tokens=1024,
                messages=[{"role": "system", "content": system}] + safe_messages,
                stream=True,
            )
            async for chunk in stream:
                text = chunk.choices[0].delta.content or ""
                if text:
                    yield f"data: {json.dumps({'text': text})}\n\n"
        except Exception as exc:
            yield f"data: {json.dumps({'error': str(exc)})}\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ── Static files ──────────────────────────────────────────────────────────────

_FRONTEND = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(_FRONTEND), html=True), name="frontend")
