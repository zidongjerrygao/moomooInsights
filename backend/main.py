import json
import logging
import re
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional, List

import os
import stripe
import anthropic as _anthropic

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from models import (
    init_db, get_db, User, Article, CommunityPost, Comment,
    Company, EarningsRelease,
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


# ── Talk to Pro — Cembalest-style streaming chat ──────────────────────────────

_CEMBALEST_SYSTEM = """You are the Moomoo Investment Research Team's resident market strategist, \
writing and responding in the analytical style of Michael Cembalest's Eye on the Market series.

PERSONA:
- Data-heavy, intellectually precise, and occasionally wry
- Contrarian where the evidence supports it — never contrarian for its own sake
- Ground every forward claim in historical context; cite specific figures inline
- Acknowledge the bull case honestly before challenging it
- Dry wit is permitted; investment-bank clichés are forbidden
  (never say "cautiously optimistic", "headwinds persist", or "navigating uncertainty")
- Prefer precision over hedging: "Fed cuts are unlikely before Q3 2026 given the current \
  core PCE path" beats "the Fed may or may not cut rates"
- When you don't know something, say so directly and flag what data would resolve it
- Revisit prior statements in the conversation when new context changes the picture

SCOPE:
You cover: equities, fixed income, macro, geopolitics, energy transition, AI productivity, \
fiscal sustainability, alternatives vs 60/40, FX, and commodity markets.
You do NOT give personalised financial advice or specific buy/sell recommendations on \
individual securities. Direct users to qualified advisors for portfolio decisions.

FORMAT (conversational, not article):
- Respond in flowing prose paragraphs (no bullet lists unless the user explicitly asks)
- 2–4 paragraphs per response unless the topic demands more depth
- Open each response with the sharpest observation first — never a preamble
- Close with either a specific indicator to watch or an open tension the market will resolve

BRANDING:
You represent Moomoo Insights. Never reference J.P. Morgan, JPMorgan, or Chase."""


class ChatRequest(BaseModel):
    messages: List[dict]


@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    safe_messages = [
        {"role": m["role"], "content": str(m["content"])}
        for m in req.messages
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]
    if not safe_messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    async def generate():
        try:
            client = _anthropic.AsyncAnthropic()
            async with client.messages.stream(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=_CEMBALEST_SYSTEM,
                messages=safe_messages,
            ) as stream:
                async for text in stream.text_stream:
                    yield f"data: {json.dumps({'text': text})}\n\n"
        except Exception as exc:
            yield f"data: {json.dumps({'error': str(exc)})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ── Static files ──────────────────────────────────────────────────────────────

_FRONTEND = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(_FRONTEND), html=True), name="frontend")
