// ── Moomoo Insights i18n ──────────────────────────────────────────────────────
const TRANSLATIONS = {
  en: {
    // Nav
    nav_news:          "News",
    nav_markets:       "Markets",
    nav_strategy:      "Strategy",
    nav_trade:         "Trade",
    nav_community:     "Community",
    nav_talk_to_pro:   "Talk to Pro",
    nav_admin:         "Admin",
    nav_login:         "Log in",
    nav_signup:        "Sign up",

    // Portal / user dropdown
    portal_sign_out:        "Sign out",
    portal_total_time:      "Total reading time",
    portal_rank:            "Rank",
    portal_role:            "Role",
    portal_admin_role:      "Admin",
    portal_max_level:       "Max level!",
    portal_min_to_lv:       "min to Lv.",
    portal_legend_tier:     "Legend tier",
    portal_upgrade:         "Upgrade to Premium",
    portal_premium_member:  "⭐ Premium Member",
    portal_hrs:             "hrs",
    portal_min:             "min",

    // Footer
    footer_privacy:  "Privacy",
    footer_terms:    "Terms",
    footer_copy:     "© 2026 Moomoo Insights",

    // Index page
    idx_daily_brief:  "Daily Market Brief",
    idx_earnings:     "Earnings",
    idx_no_articles:  "No articles yet. Check back soon.",
    idx_new_brief:    "New brief published each trading day.",
    idx_earnings_sub: "Earnings reviews published when S&P 500 top companies report.",

    // Markets page
    mkt_overview:          "Market Overview",
    mkt_us_movers:         "US Top Movers",
    mkt_refresh:           "↻ Refresh",
    mkt_auto_refresh:      "auto-refreshes every 60s",
    mkt_upcoming_earnings: "Upcoming Earnings",
    mkt_ticker:            "Ticker",
    mkt_name:              "Name",
    mkt_price:             "Price (USD)",
    mkt_change_pct:        "Change %",
    mkt_volume:            "Volume",
    mkt_date:              "Date",
    mkt_company:           "Company",
    mkt_quarter:           "Quarter",
    mkt_eps_beat:          "EPS Beat",
    mkt_rev_beat:          "Rev Beat",
    mkt_sector:            "Sector",
    mkt_next7:             "Next 7d",
    mkt_next14:            "Next 14d",
    mkt_next30:            "Next 30d",
    mkt_all_upcoming:      "All upcoming",
    mkt_loading:           "Loading…",
    mkt_no_movers:         "No movers data available",
    mkt_no_earnings:       "No upcoming earnings in this range",
    mkt_openD_note:        "",
    mkt_view_markets:      "View full markets →",

    // Strategy page
    strat_heading: "Strategy",
    strat_macro:   "Macro",
    strat_equity:  "Equity",
    strat_credit:  "Credit",
    strat_more:    "More",

    // Trade page
    trade_heading: "Trade",
    trade_tsla_meta: "Intraday & swing setups for $TSLA",
    trade_nvda_meta: "Intraday & swing setups for $NVDA",
    trade_spx_meta:  "Intraday & swing setups for $SPX",

    // Community page
    comm_heading:       "Community",
    comm_new_post:      "New Post",
    comm_search_ph:     "Search discussions…",
    comm_all:           "All",
    comm_analysis:      "Analysis",
    comm_question:      "Question",
    comm_discussion:    "Discussion",
    comm_idea:          "Idea",
    comm_no_posts:      "No posts yet. Be the first!",
    comm_post_title_ph: "Post title",
    comm_post_body_ph:  "Share your analysis, question or idea…",
    comm_post_cat:      "Category",
    comm_submit:        "Post",
    comm_cancel:        "Cancel",
    comm_likes:         "likes",
    comm_replies:       "replies",
    comm_reply_ph:      "Write a reply…",
    comm_reply_btn:     "Reply",
    comm_delete:        "Delete",
    comm_login_to_post:      "Log in to join the discussion.",
    comm_earnings:           "Earnings",
    comm_comments_heading:   "Comments",
    comm_post_title:         "Title",

    // Talk to Pro page
    ttp_heading:     "Talk to Pro",
    ttp_subtitle:    "Your AI investment research assistant",
    ttp_disclaimer:  "AI-generated insights for educational purposes only. Not financial advice.",
    ttp_input_ph:    "Ask about any stock, market trend, or investment strategy…",
    ttp_send:        "Send",
    ttp_welcome:     "Hello! I'm your Moomoo AI research assistant. Ask me about markets, stocks, earnings, or investment strategy.",
    ttp_chip_tsla:   "Analyse TSLA",
    ttp_chip_macro:  "Weekly macro outlook",
    ttp_chip_nvda:   "NVDA earnings",
    ttp_chip_options:"Explain options flow",

    // Login page
    login_tab_login:    "Log in",
    login_tab_register: "Register",
    login_tab_signup:   "Sign Up",
    login_email:        "Email",
    login_email_lbl:    "Email",
    login_password:     "Password",
    login_password_lbl: "Password",
    login_display_name: "Display name (optional)",
    login_name_lbl:     "Display Name",
    login_btn_login:    "Log in",
    login_btn_register: "Create account",
    login_btn_signup:   "Create Account",
    login_back:         "← Back to Moomoo Insights",
    login_email_ph:     "you@example.com",
    login_password_ph:  "Password",
    login_name_ph:      "How should we call you?",
    login_first_admin:  "The first account created becomes admin.",

    // Payment page
    pay_tagline:      "Institutional-grade research for retail investors",
    pay_premium:      "⭐ PREMIUM",
    pay_per_month:    "/month",
    pay_cancel_any:   "Cancel anytime · Billed monthly",
    pay_everything:   "Everything in Premium",
    pay_perk1_title:  "Full Research Access",
    pay_perk1_desc:   "Cembalest-style macro deep-dives, earnings analysis, and strategy reports",
    pay_perk2_title:  "Unlimited AI Chat",
    pay_perk2_desc:   "Talk to Pro with no daily message limits",
    pay_perk3_title:  "Daily Trade Briefs",
    pay_perk3_desc:   "TSLA, NVDA, and SPX setups with Smart Money levels and options flow",
    pay_perk4_title:  "Earnings Alerts",
    pay_perk4_desc:   "Pre-market earnings digests with beat/miss analysis before the open",
    pay_perk5_title:  "Premium Badge",
    pay_perk5_desc:   "Gold Premium badge on your community profile",
    pay_subscribe:    "Subscribe Now — $9/month",
    pay_secure:       "🔒 Secure payment via Stripe · SSL encrypted",
    pay_back:         "← Back to Moomoo Insights",
    pay_create_acct:  "Create an account",
    pay_or_login:     "or",
    pay_to_subscribe: "to subscribe.",
    pay_already:      "✓ You're already Premium!",
    pay_cancelled:    "Payment cancelled — no charge was made.",
    pay_redirecting:  "Redirecting to Stripe…",
    pay_login_to_sub: "log in",

    // Payment success page
    pay_success_title: "Welcome to Premium!",
    pay_success_sub:   "Your subscription is active. You now have full access to all Moomoo Insights Premium features.",
    pay_success_badge: "⭐ PREMIUM MEMBER",
    pay_success_btn:   "Start Reading →",

    // Article page
    art_edit:          "Edit Article",
    art_delete:        "Delete",
    art_save:          "Save Changes",
    art_cancel:        "Cancel",
    art_title_lbl:     "Title",
    art_excerpt_lbl:   "Excerpt",
    art_category_lbl:  "Category",
    art_tags_lbl:      "Tags (comma-separated)",
    art_content_lbl:   "Content HTML",
    art_published_yes: "Yes",
    art_published_no:  "No",
    art_admin_badge:   "🛠 Admin",
    art_markets:       "Markets",
    art_related:       "Related",
    login_subtitle:          "Market intelligence for everyone",
    login_password_reg_ph:   "At least 6 characters",
    comm_modal_title:        "New Community Post",
    comm_cat_lbl:            "Category",
    comm_body_lbl:           "Content",
    comm_close:              "Close",
    comm_comments:           "comments",
    comm_no_comments:        "No comments yet.",
    comm_post_comment:       "Post Comment",
    comm_market_news:        "Market News",
    comm_education:          "Education",
    comm_general:            "General",
    trade_latest:            "Latest Analysis",
    trade_price_unavailable: "Price unavailable",
    ttp_subtitle_detail:     "Moomoo Investment Research · Eye on the Market style",
    ttp_chip1:               "Fed policy outlook",
    ttp_chip2:               "AI capex — bubble or foundation?",
    ttp_chip3:               "Energy transition realism",
    ttp_chip4:               "US fiscal sustainability",
    ttp_chip5:               "60/40 vs alternatives",
    ttp_chip6:               "China — investable again?",
    ttp_welcome1:            "Markets are rarely wrong about direction — only timing. Ask me about macro themes, asset allocation, sector dynamics, or anything you'd expect from a data-driven investment strategist.",
    ttp_welcome2:            "I'll give you precise, historically grounded analysis. No platitudes, no hedged non-answers.",
    art_edit_tab_en:         "English",
    art_edit_tab_cn:         "简体中文",
    art_edit_tab_hk:         "繁體中文",
  },

  "zh-cn": {
    // Nav
    nav_news:          "新闻",
    nav_markets:       "市场",
    nav_strategy:      "策略",
    nav_trade:         "交易",
    nav_community:     "社区",
    nav_talk_to_pro:   "专业咨询",
    nav_admin:         "管理",
    nav_login:         "登录",
    nav_signup:        "注册",

    // Portal
    portal_sign_out:        "退出登录",
    portal_total_time:      "总阅读时长",
    portal_rank:            "称号",
    portal_role:            "身份",
    portal_admin_role:      "管理员",
    portal_max_level:       "最高等级！",
    portal_min_to_lv:       "分钟升至等级",
    portal_legend_tier:     "传奇段位",
    portal_upgrade:         "升级到高级版",
    portal_premium_member:  "⭐ 高级会员",
    portal_hrs:             "小时",
    portal_min:             "分钟",

    // Footer
    footer_privacy:  "隐私政策",
    footer_terms:    "服务条款",
    footer_copy:     "© 2026 Moomoo Insights",

    // Index
    idx_daily_brief:  "每日市场简报",
    idx_earnings:     "财报",
    idx_no_articles:  "暂无文章，请稍后查看。",
    idx_new_brief:    "每个交易日发布新简报。",
    idx_earnings_sub: "标普500重要公司财报发布时同步更新。",

    // Markets
    mkt_overview:          "市场概览",
    mkt_us_movers:         "美股涨跌幅榜",
    mkt_refresh:           "↻ 刷新",
    mkt_auto_refresh:      "每60秒自动刷新",
    mkt_upcoming_earnings: "即将发布的财报",
    mkt_ticker:            "代码",
    mkt_name:              "名称",
    mkt_price:             "价格（美元）",
    mkt_change_pct:        "涨跌幅",
    mkt_volume:            "成交量",
    mkt_date:              "日期",
    mkt_company:           "公司",
    mkt_quarter:           "季度",
    mkt_eps_beat:          "EPS超预期",
    mkt_rev_beat:          "营收超预期",
    mkt_sector:            "板块",
    mkt_next7:             "未来7天",
    mkt_next14:            "未来14天",
    mkt_next30:            "未来30天",
    mkt_all_upcoming:      "全部即将发布",
    mkt_loading:           "加载中…",
    mkt_no_movers:         "暂无涨跌幅数据",
    mkt_no_earnings:       "此范围内暂无即将发布的财报",
    mkt_openD_note:        "",
    mkt_view_markets:      "查看完整市场 →",

    // Strategy
    strat_heading: "策略",
    strat_macro:   "宏观",
    strat_equity:  "股票",
    strat_credit:  "信用",
    strat_more:    "更多",

    // Trade
    trade_heading:   "交易",
    trade_tsla_meta: "$TSLA日内及波段交易设置",
    trade_nvda_meta: "$NVDA日内及波段交易设置",
    trade_spx_meta:  "$SPX日内及波段交易设置",

    // Community
    comm_heading:       "社区",
    comm_new_post:      "发帖",
    comm_search_ph:     "搜索讨论…",
    comm_all:           "全部",
    comm_analysis:      "分析",
    comm_question:      "提问",
    comm_discussion:    "讨论",
    comm_idea:          "想法",
    comm_no_posts:      "暂无帖子，来发第一篇吧！",
    comm_post_title_ph: "帖子标题",
    comm_post_body_ph:  "分享你的分析、问题或想法…",
    comm_post_cat:      "分类",
    comm_submit:        "发布",
    comm_cancel:        "取消",
    comm_likes:         "点赞",
    comm_replies:       "回复",
    comm_reply_ph:      "写回复…",
    comm_reply_btn:     "回复",
    comm_delete:        "删除",
    comm_login_to_post:      "登录后参与讨论。",
    comm_earnings:           "财报",
    comm_comments_heading:   "评论",
    comm_post_title:         "标题",

    // Talk to Pro
    ttp_heading:     "专业咨询",
    ttp_subtitle:    "您的AI投资研究助手",
    ttp_disclaimer:  "AI生成内容仅供教育参考，不构成投资建议。",
    ttp_input_ph:    "询问任何股票、市场趋势或投资策略…",
    ttp_send:        "发送",
    ttp_welcome:     "您好！我是您的Moomoo AI研究助手。您可以问我有关市场、股票、财报或投资策略的问题。",
    ttp_chip_tsla:   "分析TSLA",
    ttp_chip_macro:  "每周宏观展望",
    ttp_chip_nvda:   "NVDA财报",
    ttp_chip_options:"解释期权流",

    // Login
    login_tab_login:    "登录",
    login_tab_register: "注册",
    login_tab_signup:   "注册",
    login_email:        "邮箱",
    login_email_lbl:    "邮箱",
    login_password:     "密码",
    login_password_lbl: "密码",
    login_display_name: "显示名称（可选）",
    login_name_lbl:     "显示名称",
    login_btn_login:    "登录",
    login_btn_register: "创建账号",
    login_btn_signup:   "创建账号",
    login_back:         "← 返回Moomoo Insights",
    login_email_ph:     "you@example.com",
    login_password_ph:  "密码",
    login_name_ph:      "您希望我们如何称呼您？",
    login_first_admin:  "第一个创建的账号将成为管理员。",

    // Payment
    pay_tagline:      "面向散户的机构级研究",
    pay_premium:      "⭐ 高级版",
    pay_per_month:    "/月",
    pay_cancel_any:   "随时取消 · 按月计费",
    pay_everything:   "高级版全部权益",
    pay_perk1_title:  "完整研究权限",
    pay_perk1_desc:   "Cembalest风格宏观深度研究、财报分析及策略报告",
    pay_perk2_title:  "无限AI对话",
    pay_perk2_desc:   "专业咨询无每日消息限制",
    pay_perk3_title:  "每日交易简报",
    pay_perk3_desc:   "含智能资金水平和期权流的TSLA、NVDA和SPX交易设置",
    pay_perk4_title:  "财报预警",
    pay_perk4_desc:   "开市前财报摘要，含超预期/低于预期分析",
    pay_perk5_title:  "高级徽章",
    pay_perk5_desc:   "社区主页金色高级徽章",
    pay_subscribe:    "立即订阅 — $9/月",
    pay_secure:       "🔒 通过Stripe安全支付 · SSL加密",
    pay_back:         "← 返回Moomoo Insights",
    pay_create_acct:  "创建账号",
    pay_or_login:     "或",
    pay_to_subscribe: "以订阅。",
    pay_already:      "✓ 您已是高级会员！",
    pay_cancelled:    "支付已取消 — 未收取任何费用。",
    pay_redirecting:  "正在跳转至Stripe…",
    pay_login_to_sub: "登录",

    // Payment success
    pay_success_title: "欢迎加入高级版！",
    pay_success_sub:   "您的订阅已激活。您现在可以访问Moomoo Insights高级版的所有功能。",
    pay_success_badge: "⭐ 高级会员",
    pay_success_btn:   "开始阅读 →",

    // Article
    art_edit:          "编辑文章",
    art_delete:        "删除",
    art_save:          "保存更改",
    art_cancel:        "取消",
    art_title_lbl:     "标题",
    art_excerpt_lbl:   "摘要",
    art_category_lbl:  "分类",
    art_tags_lbl:      "标签（逗号分隔）",
    art_content_lbl:   "内容HTML",
    art_published_yes: "是",
    art_published_no:  "否",
    art_admin_badge:   "🛠 管理",
    art_markets:       "市场",
    art_related:       "相关文章",
    login_subtitle:          "人人皆可享有的市场智慧",
    login_password_reg_ph:   "至少6个字符",
    comm_modal_title:        "发布社区帖子",
    comm_cat_lbl:            "分类",
    comm_body_lbl:           "内容",
    comm_close:              "关闭",
    comm_comments:           "条评论",
    comm_no_comments:        "暂无评论。",
    comm_post_comment:       "发布评论",
    comm_market_news:        "市场新闻",
    comm_education:          "教育",
    comm_general:            "综合",
    trade_latest:            "最新分析",
    trade_price_unavailable: "价格暂不可用",
    ttp_subtitle_detail:     "Moomoo投资研究 · 市场洞见风格",
    ttp_chip1:               "美联储政策展望",
    ttp_chip2:               "AI资本支出 — 泡沫还是基础？",
    ttp_chip3:               "能源转型的现实",
    ttp_chip4:               "美国财政可持续性",
    ttp_chip5:               "60/40 vs 另类资产",
    ttp_chip6:               "中国 — 值得投资了吗？",
    ttp_welcome1:            "市场对方向的判断鲜有错误，只是时机不同。请问我有关宏观主题、资产配置、行业动态或任何数据驱动型投资策略师所关注的话题。",
    ttp_welcome2:            "我将提供精准且有历史依据的分析。没有陈词滥调，没有模棱两可的回答。",
    art_edit_tab_en:         "英文",
    art_edit_tab_cn:         "简体中文",
    art_edit_tab_hk:         "繁體中文",
  },

  "zh-hk": {
    // Nav
    nav_news:          "新聞",
    nav_markets:       "市場",
    nav_strategy:      "策略",
    nav_trade:         "交易",
    nav_community:     "社群",
    nav_talk_to_pro:   "專業諮詢",
    nav_admin:         "管理",
    nav_login:         "登入",
    nav_signup:        "立即註冊",

    // Portal
    portal_sign_out:        "登出",
    portal_total_time:      "總閱讀時間",
    portal_rank:            "稱謂",
    portal_role:            "身份",
    portal_admin_role:      "管理員",
    portal_max_level:       "最高等級！",
    portal_min_to_lv:       "分鐘升至等級",
    portal_legend_tier:     "傳奇段位",
    portal_upgrade:         "升級至高級版",
    portal_premium_member:  "⭐ 高級會員",
    portal_hrs:             "小時",
    portal_min:             "分鐘",

    // Footer
    footer_privacy:  "私隱政策",
    footer_terms:    "服務條款",
    footer_copy:     "© 2026 Moomoo Insights",

    // Index
    idx_daily_brief:  "每日市場簡報",
    idx_earnings:     "業績",
    idx_no_articles:  "暫無文章，請稍後查看。",
    idx_new_brief:    "每個交易日發布新簡報。",
    idx_earnings_sub: "標普500重要公司業績公佈時同步更新。",

    // Markets
    mkt_overview:          "市場概覽",
    mkt_us_movers:         "美股升跌榜",
    mkt_refresh:           "↻ 重新整理",
    mkt_auto_refresh:      "每60秒自動重新整理",
    mkt_upcoming_earnings: "即將公佈的業績",
    mkt_ticker:            "代號",
    mkt_name:              "名稱",
    mkt_price:             "價格（美元）",
    mkt_change_pct:        "升跌幅",
    mkt_volume:            "成交量",
    mkt_date:              "日期",
    mkt_company:           "公司",
    mkt_quarter:           "季度",
    mkt_eps_beat:          "EPS超預期",
    mkt_rev_beat:          "收入超預期",
    mkt_sector:            "板塊",
    mkt_next7:             "未來7日",
    mkt_next14:            "未來14日",
    mkt_next30:            "未來30日",
    mkt_all_upcoming:      "全部即將公佈",
    mkt_loading:           "載入中…",
    mkt_no_movers:         "暫無升跌幅數據",
    mkt_no_earnings:       "此範圍內暫無即將公佈的業績",
    mkt_openD_note:        "",
    mkt_view_markets:      "查看完整市場 →",

    // Strategy
    strat_heading: "策略",
    strat_macro:   "宏觀",
    strat_equity:  "股票",
    strat_credit:  "信用",
    strat_more:    "更多",

    // Trade
    trade_heading:   "交易",
    trade_tsla_meta: "$TSLA即日及波段交易設置",
    trade_nvda_meta: "$NVDA即日及波段交易設置",
    trade_spx_meta:  "$SPX即日及波段交易設置",

    // Community
    comm_heading:       "社群",
    comm_new_post:      "發帖",
    comm_search_ph:     "搜尋討論…",
    comm_all:           "全部",
    comm_analysis:      "分析",
    comm_question:      "提問",
    comm_discussion:    "討論",
    comm_idea:          "想法",
    comm_no_posts:      "暫無帖子，來發第一篇吧！",
    comm_post_title_ph: "帖子標題",
    comm_post_body_ph:  "分享你的分析、問題或想法…",
    comm_post_cat:      "分類",
    comm_submit:        "發佈",
    comm_cancel:        "取消",
    comm_likes:         "讚好",
    comm_replies:       "回覆",
    comm_reply_ph:      "撰寫回覆…",
    comm_reply_btn:     "回覆",
    comm_delete:        "刪除",
    comm_login_to_post:      "登入後參與討論。",
    comm_earnings:           "業績",
    comm_comments_heading:   "評論",
    comm_post_title:         "標題",

    // Talk to Pro
    ttp_heading:     "專業諮詢",
    ttp_subtitle:    "您的AI投資研究助手",
    ttp_disclaimer:  "AI生成內容僅供教育參考，不構成投資建議。",
    ttp_input_ph:    "詢問任何股票、市場趨勢或投資策略…",
    ttp_send:        "發送",
    ttp_welcome:     "您好！我是您的Moomoo AI研究助手。您可以問我有關市場、股票、業績或投資策略的問題。",
    ttp_chip_tsla:   "分析TSLA",
    ttp_chip_macro:  "每週宏觀展望",
    ttp_chip_nvda:   "NVDA業績",
    ttp_chip_options:"解釋期權流",

    // Login
    login_tab_login:    "登入",
    login_tab_register: "註冊",
    login_tab_signup:   "立即註冊",
    login_email:        "電郵",
    login_email_lbl:    "電郵",
    login_password:     "密碼",
    login_password_lbl: "密碼",
    login_display_name: "顯示名稱（選填）",
    login_name_lbl:     "顯示名稱",
    login_btn_login:    "登入",
    login_btn_register: "建立帳號",
    login_btn_signup:   "建立帳號",
    login_back:         "← 返回Moomoo Insights",
    login_email_ph:     "you@example.com",
    login_password_ph:  "密碼",
    login_name_ph:      "請問我們應如何稱呼您？",
    login_first_admin:  "第一個建立的帳號將成為管理員。",

    // Payment
    pay_tagline:      "面向散戶的機構級研究",
    pay_premium:      "⭐ 高級版",
    pay_per_month:    "/月",
    pay_cancel_any:   "隨時取消 · 按月計費",
    pay_everything:   "高級版全部權益",
    pay_perk1_title:  "完整研究權限",
    pay_perk1_desc:   "Cembalest風格宏觀深度研究、業績分析及策略報告",
    pay_perk2_title:  "無限AI對話",
    pay_perk2_desc:   "專業諮詢無每日訊息限制",
    pay_perk3_title:  "每日交易簡報",
    pay_perk3_desc:   "含智能資金水平和期權流的TSLA、NVDA和SPX交易設置",
    pay_perk4_title:  "業績預警",
    pay_perk4_desc:   "開市前業績摘要，含超預期/低於預期分析",
    pay_perk5_title:  "高級徽章",
    pay_perk5_desc:   "社群主頁金色高級徽章",
    pay_subscribe:    "立即訂閱 — $9/月",
    pay_secure:       "🔒 通過Stripe安全付款 · SSL加密",
    pay_back:         "← 返回Moomoo Insights",
    pay_create_acct:  "建立帳號",
    pay_or_login:     "或",
    pay_to_subscribe: "以訂閱。",
    pay_already:      "✓ 您已是高級會員！",
    pay_cancelled:    "付款已取消 — 未收取任何費用。",
    pay_redirecting:  "正在跳轉至Stripe…",
    pay_login_to_sub: "登入",

    // Payment success
    pay_success_title: "歡迎加入高級版！",
    pay_success_sub:   "您的訂閱已啟用。您現在可以存取Moomoo Insights高級版的所有功能。",
    pay_success_badge: "⭐ 高級會員",
    pay_success_btn:   "開始閱讀 →",

    // Article
    art_edit:          "編輯文章",
    art_delete:        "刪除",
    art_save:          "儲存更改",
    art_cancel:        "取消",
    art_title_lbl:     "標題",
    art_excerpt_lbl:   "摘要",
    art_category_lbl:  "分類",
    art_tags_lbl:      "標籤（逗號分隔）",
    art_content_lbl:   "內容HTML",
    art_published_yes: "是",
    art_published_no:  "否",
    art_admin_badge:   "🛠 管理",
    art_markets:       "市場",
    art_related:       "相關文章",
    login_subtitle:          "人人皆可享有的市場智慧",
    login_password_reg_ph:   "至少6個字元",
    comm_modal_title:        "發布社群帖子",
    comm_cat_lbl:            "分類",
    comm_body_lbl:           "內容",
    comm_close:              "關閉",
    comm_comments:           "則評論",
    comm_no_comments:        "暫無評論。",
    comm_post_comment:       "發布評論",
    comm_market_news:        "市場新聞",
    comm_education:          "教育",
    comm_general:            "綜合",
    trade_latest:            "最新分析",
    trade_price_unavailable: "價格暫不可用",
    ttp_subtitle_detail:     "Moomoo投資研究 · 市場洞見風格",
    ttp_chip1:               "美聯儲政策展望",
    ttp_chip2:               "AI資本支出 — 泡沫還是基礎？",
    ttp_chip3:               "能源轉型的現實",
    ttp_chip4:               "美國財政可持續性",
    ttp_chip5:               "60/40 vs 另類資產",
    ttp_chip6:               "中國 — 值得投資了嗎？",
    ttp_welcome1:            "市場對方向的判斷鮮有錯誤，只是時機不同。請問我有關宏觀主題、資產配置、行業動態或任何數據驅動型投資策略師所關注的話題。",
    ttp_welcome2:            "我將提供精準且有歷史依據的分析。沒有陳詞濫調，沒有模稜兩可的回答。",
    art_edit_tab_en:         "英文",
    art_edit_tab_cn:         "简体中文",
    art_edit_tab_hk:         "繁體中文",
  },
};

// ── Core API ──────────────────────────────────────────────────────────────────
function getLang() {
  return localStorage.getItem("moomoo_lang") || "en";
}

function setLang(lang) {
  localStorage.setItem("moomoo_lang", lang);
  document.documentElement.lang = lang === "en" ? "en" : lang === "zh-cn" ? "zh-CN" : "zh-HK";
  applyI18n();
  // Re-render nav so lang button label updates
  if (typeof renderNav === "function") renderNav();
}

function t(key) {
  const lang = getLang();
  const dict = TRANSLATIONS[lang] || TRANSLATIONS["en"];
  return dict[key] || TRANSLATIONS["en"][key] || key;
}

function applyI18n() {
  // Text content
  document.querySelectorAll("[data-i18n]").forEach(el => {
    el.textContent = t(el.dataset.i18n);
  });
  // Placeholders
  document.querySelectorAll("[data-i18n-ph]").forEach(el => {
    el.placeholder = t(el.dataset.i18nPh);
  });
  // HTML content (for rich text)
  document.querySelectorAll("[data-i18n-html]").forEach(el => {
    el.innerHTML = t(el.dataset.i18nHtml);
  });
  // Title attributes
  document.querySelectorAll("[data-i18n-title]").forEach(el => {
    el.title = t(el.dataset.i18nTitle);
  });
}

// Language switcher UI helpers
function getLangLabel(lang) {
  return { en: "EN", "zh-cn": "简中", "zh-hk": "繁中" }[lang] || "EN";
}

function toggleLangMenu(e) {
  e.stopPropagation();
  document.getElementById("lang-menu")?.classList.toggle("open");
}

function switchLang(lang) {
  document.getElementById("lang-menu")?.classList.remove("open");
  setLang(lang);
}

// Close lang menu on outside click
document.addEventListener("click", e => {
  if (!e.target.closest(".lang-switcher")) {
    document.getElementById("lang-menu")?.classList.remove("open");
  }
});

// Apply on initial load
document.addEventListener("DOMContentLoaded", () => {
  document.documentElement.lang = getLang() === "en" ? "en" : getLang() === "zh-cn" ? "zh-CN" : "zh-HK";
  applyI18n();
});
