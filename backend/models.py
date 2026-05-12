import os
from datetime import datetime
from pathlib import Path
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Boolean,
    DateTime, Text, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

_DB_PATH = Path(__file__).parent / "moomoo.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{_DB_PATH}")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    display_name = Column(String)
    is_admin = Column(Boolean, default=False)
    reading_time_minutes = Column(Float, default=0.0)
    is_premium = Column(Boolean, default=False)
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    comments = relationship("Comment", back_populates="user")
    community_posts = relationship("CommunityPost", back_populates="user")


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    excerpt = Column(Text)
    content_html = Column(Text, nullable=False)
    tags = Column(JSON, default=list)
    category = Column(String, default="Market Analysis")
    author = Column(String, default="Moomoo Insights")
    published = Column(Boolean, default=True)
    featured = Column(Boolean, default=False)
    cover_image = Column(String)
    title_zh_cn = Column(Text)
    excerpt_zh_cn = Column(Text)
    content_html_zh_cn = Column(Text)
    title_zh_hk = Column(Text)
    excerpt_zh_hk = Column(Text)
    content_html_zh_hk = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CommunityPost(Base):
    __tablename__ = "community_posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    category = Column(String, default="General")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="community_posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("community_posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="comments")
    post = relationship("CommunityPost", back_populates="comments")


# ── SPX Earnings (mirrored from spx-earnings project) ────────────────────────

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    ticker = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    sector = Column(String)
    weight_pct = Column(Float)
    releases = relationship("EarningsRelease", back_populates="company")


class EarningsRelease(Base):
    __tablename__ = "earnings_releases"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    report_date = Column(String)
    fiscal_quarter = Column(String)
    eps_actual = Column(Float)
    eps_estimate = Column(Float)
    eps_surprise_pct = Column(Float)
    revenue_actual = Column(Float)
    revenue_estimate = Column(Float)
    revenue_surprise_pct = Column(Float)
    stock_price_before = Column(Float)
    stock_price_after = Column(Float)
    stock_reaction_pct = Column(Float)
    guidance = Column(Text)
    is_manual_override = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    company = relationship("Company", back_populates="releases")


class EmailSubscriber(Base):
    __tablename__ = "email_subscribers"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
    bundles = Column(JSON, default=list)  # ["daily", "strategy"]
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class EmailSendLog(Base):
    __tablename__ = "email_send_logs"
    id = Column(Integer, primary_key=True)
    bundle_type = Column(String, nullable=False)
    subject = Column(String)
    recipients_count = Column(Integer, default=0)
    articles_count = Column(Integer, default=0)
    sent_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="ok")
    error = Column(Text)


def init_db():
    Base.metadata.create_all(bind=engine)
    # Safe migration: add reading_time_minutes if missing
    with engine.connect() as conn:
        try:
            conn.execute(__import__("sqlalchemy").text(
                "ALTER TABLE users ADD COLUMN reading_time_minutes REAL DEFAULT 0.0"
            ))
            conn.commit()
        except Exception:
            pass  # Column already exists
    for col_sql in [
        "ALTER TABLE users ADD COLUMN is_premium INTEGER DEFAULT 0",
        "ALTER TABLE users ADD COLUMN stripe_customer_id TEXT",
        "ALTER TABLE users ADD COLUMN stripe_subscription_id TEXT",
    ]:
        with engine.connect() as conn:
            try:
                conn.execute(__import__("sqlalchemy").text(col_sql))
                conn.commit()
            except Exception:
                pass
    for col_sql in [
        "ALTER TABLE articles ADD COLUMN title_zh_cn TEXT",
        "ALTER TABLE articles ADD COLUMN excerpt_zh_cn TEXT",
        "ALTER TABLE articles ADD COLUMN content_html_zh_cn TEXT",
        "ALTER TABLE articles ADD COLUMN title_zh_hk TEXT",
        "ALTER TABLE articles ADD COLUMN excerpt_zh_hk TEXT",
        "ALTER TABLE articles ADD COLUMN content_html_zh_hk TEXT",
    ]:
        with engine.connect() as conn:
            try:
                conn.execute(__import__("sqlalchemy").text(col_sql))
                conn.commit()
            except Exception:
                pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
