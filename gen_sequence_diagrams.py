# coding: utf-8
"""Sequence diagrams: 1) Auth/Login  2) Quiz flow"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ─── primitives ───────────────────────────────────────────────────────────────

def rbox(ax, x, y, w, h, fc, ec, lw=2, r=0.25, zorder=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder))

def txt(ax, x, y, s, fs=10, bold=False, color="#1E293B",
        ha="center", va="center", zorder=6, ls=1.3):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs,
            fontweight="bold" if bold else "normal",
            color=color, zorder=zorder, linespacing=ls)

def participant(ax, cx, top, label, sub, fc, ec, W=2.3, H=0.9):
    """Draw participant box centered at cx."""
    rbox(ax, cx - W/2, top - H, W, H, fc, ec, lw=2.5, r=0.3, zorder=4)
    txt(ax, cx, top - H*0.55, label, fs=11, bold=True, color="#1E293B", zorder=5)
    if sub:
        txt(ax, cx, top - H*0.78, sub, fs=7.5, color="#64748B", zorder=5)

def lifeline(ax, cx, y_top, y_bot, color="#CBD5E1"):
    ax.plot([cx, cx], [y_top, y_bot], color=color,
            lw=1.5, linestyle="--", zorder=2)

def h_arrow(ax, x1, x2, y, label, color="#334155",
            lw=2, fs=9, above=True, ret=False):
    """Horizontal arrow from x1 to x2 at height y with label."""
    style = "<|-" if ret else "-|>"
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle=style, color=color,
                                lw=lw, mutation_scale=16), zorder=5)
    mx = (x1 + x2) / 2
    dy = 0.18 if above else -0.22
    txt(ax, mx, y + dy, label, fs=fs, color=color, zorder=6)

def step_box(ax, x, y, w, h, num, text, fc="#F1F5F9", ec="#94A3B8"):
    """Numbered action box on a lifeline."""
    rbox(ax, x - w/2, y - h/2, w, h, fc, ec, lw=1.5, r=0.2, zorder=4)
    txt(ax, x - w/2 + 0.25, y, str(num), fs=9, bold=True, color=ec, zorder=5)
    txt(ax, x, y, f"  {text}", fs=8.8, color="#1E293B", zorder=5)

def divider(ax, y, W, color="#E2E8F0"):
    ax.plot([0.3, W-0.3], [y, y], color=color, lw=1, zorder=1)


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 1 — АВТОРИЗАЦИЯ (LOGIN)
# ══════════════════════════════════════════════════════════════════════════════
DW, DH = 22, 17
fig, ax = plt.subplots(figsize=(DW, DH), dpi=150)
ax.set_xlim(0, DW); ax.set_ylim(0, DH); ax.axis("off")
fig.patch.set_facecolor("#F8FAFC")

# title
txt(ax, DW/2, DH-0.45, "Диаграмма последовательностей — Авторизация (Login)",
    fs=17, bold=True, color="#0F172A")
txt(ax, DW/2, DH-1.0, "Поток: Пользователь вводит email + пароль  →  JWT токен сохраняется в браузере",
    fs=10, color="#64748B")

TOP = DH - 1.4   # participant boxes top edge
BOT = 0.5        # lifeline bottom

# participants: cx positions
P = {
    "user":    2.2,
    "auth":    5.8,
    "api":     9.4,
    "fastapi": 13.2,
    "db":      17.4,
    "local":   21.0,
}
pdata = [
    ("user",    "Пользователь",   "",              "#BFDBFE","#2563EB"),
    ("auth",    "Auth.tsx",       "React страница","#A5F3FC","#0891B2"),
    ("api",     "api.ts",         "axios",         "#FDE68A","#D97706"),
    ("fastapi", "FastAPI",        "/api/auth/login","#BBF7D0","#16A34A"),
    ("db",      "База данных",    "SQLite · users", "#FED7AA","#EA580C"),
    ("local",   "localStorage",  "Браузер",        "#E9D5FF","#9333EA"),
]
for key, label, sub, fc, ec in pdata:
    participant(ax, P[key], TOP, label, sub, fc, ec, W=2.5, H=1.0)
    lifeline(ax, P[key], TOP-1.0, BOT)

# ── шаги ──────────────────────────────────────────────────────────────────────
steps = [
    # y,    x1_key,   x2_key,   label,                              color,   ret
    (14.8, "user",   "auth",   "1. Ввод email + пароль",           "#2563EB", False),
    (13.8, "auth",   "api",    "2. login(email, password)",         "#0891B2", False),
    (12.8, "api",    "fastapi","3. POST /api/auth/login\n{email, password}","#D97706", False),
    (11.7, "fastapi","db",     "4. SELECT * FROM users\nWHERE email = ?",   "#16A34A", False),
    (10.8, "db",     "fastapi","5. User (id, email, password_hash, role)",  "#EA580C", True),
    ( 9.8, "fastapi","fastapi","6. verify_password() → bcrypt проверка",    "#16A34A", False),
    ( 8.8, "fastapi","fastapi","7. create_access_token() → JWT HS256",      "#16A34A", False),
    ( 7.8, "fastapi","api",    "8. {access_token, token_type: bearer}",     "#16A34A", True),
    ( 6.8, "api",    "local",  "9. localStorage.setItem('token', jwt)",     "#9333EA", False),
    ( 5.8, "api",    "auth",   "10. Успешный ответ",                        "#0891B2", True),
    ( 4.8, "auth",   "user",   "11. navigate('/') — редирект на главную",   "#2563EB", True),
]

for (y, k1, k2, label, color, ret) in steps:
    if k1 == k2:
        # self-loop: draw a small box on the lifeline
        cx = P[k1]
        rbox(ax, cx-0.05, y-0.28, 4.0, 0.56, "#F0FDF4", "#16A34A", lw=1.2, r=0.15, zorder=4)
        txt(ax, cx+2.0, y, label, fs=8.5, color="#14532D", zorder=5)
    else:
        h_arrow(ax, P[k1], P[k2], y, label, color, lw=2, ret=ret)

# error branch box
rbox(ax, 0.4, 3.3, 7.5, 1.2, "#FEF2F2", "#EF4444", lw=1.5, r=0.25, zorder=4)
txt(ax, 4.15, 4.1, "Ошибка — неверный пароль / email не найден", fs=9, bold=True, color="#DC2626", zorder=5)
txt(ax, 4.15, 3.65, "FastAPI → 401 Unauthorized\n«Неверный email или пароль»", fs=8.5, color="#7F1D1D", zorder=5)

rbox(ax, 0.4, 1.8, 7.5, 1.2, "#F0FDF4", "#16A34A", lw=1.5, r=0.25, zorder=4)
txt(ax, 4.15, 2.6, "Успех — токен получен", fs=9, bold=True, color="#14532D", zorder=5)
txt(ax, 4.15, 2.15, "access_token сохранён → добавляется в каждый запрос\nAuthorization: Bearer <token>", fs=8.5, color="#064E3B", zorder=5)

plt.tight_layout(pad=0.3)
fig.savefig(r"C:\Users\thchkr\Desktop\диплом\diploma_lms\seq_auth.png",
            dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved seq_auth.png")
plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 2 — ПРОХОЖДЕНИЕ ТЕСТА (QUIZ FLOW)
# ══════════════════════════════════════════════════════════════════════════════
DW2, DH2 = 24, 20
fig2, ax2 = plt.subplots(figsize=(DW2, DH2), dpi=150)
ax2.set_xlim(0, DW2); ax2.set_ylim(0, DH2); ax2.axis("off")
fig2.patch.set_facecolor("#F8FAFC")

txt(ax2, DW2/2, DH2-0.45,
    "Диаграмма последовательностей — Прохождение теста (Quiz)",
    fs=17, bold=True, color="#0F172A")
txt(ax2, DW2/2, DH2-1.0,
    "Поток: Студент начинает тест  →  отвечает на вопросы  →  получает результат",
    fs=10, color="#64748B")

TOP2 = DH2 - 1.4
BOT2 = 0.5

P2 = {
    "student":  2.0,
    "quiz":     5.8,
    "api":      9.6,
    "quizzes":  13.5,
    "attempts": 17.8,
    "db":       22.0,
}
pdata2 = [
    ("student",  "Студент",       "",                    "#BFDBFE","#2563EB"),
    ("quiz",     "QuizPage.tsx",  "React страница",      "#A5F3FC","#0891B2"),
    ("api",      "api.ts",        "axios",               "#FDE68A","#D97706"),
    ("quizzes",  "FastAPI",       "/api/quizzes",        "#BBF7D0","#16A34A"),
    ("attempts", "FastAPI",       "/api/attempts",       "#D1FAE5","#059669"),
    ("db",       "База данных",   "SQLite",              "#FED7AA","#EA580C"),
]
for key, label, sub, fc, ec in pdata2:
    participant(ax2, P2[key], TOP2, label, sub, fc, ec, W=2.6, H=1.0)
    lifeline(ax2, P2[key], TOP2-1.0, BOT2)

# фаза 1 — START
rbox(ax2, 0.3, 15.4, 4.0, 0.5, "#DBEAFE", "#2563EB", lw=2, r=0.2, zorder=4)
txt(ax2, 2.3, 15.65, "ФАЗА 1 — Начало теста", fs=9, bold=True, color="#1E3A8A", zorder=5)

steps2_start = [
    (15.1, "student","quiz",     "1. Нажать «Начать тест»",             "#2563EB", False),
    (14.2, "quiz",   "api",      "2. startQuiz(quizId)",                 "#0891B2", False),
    (13.3, "api",    "quizzes",  "3. POST /api/quizzes/:id/start\nBearer <token>","#D97706", False),
    (12.2, "quizzes","db",       "4. SELECT * FROM quizzes\nWHERE id = ?",       "#16A34A", False),
    (11.3, "db",     "quizzes",  "5. Quiz (title, time_limit_sec,\npassing_score, questions)",  "#EA580C", True),
    (10.2, "quizzes","db",       "6. INSERT INTO attempts\n(user_id, quiz_id, status='IN_PROGRESS')", "#16A34A", False),
    ( 9.3, "db",     "quizzes",  "7. attempt_id",                        "#EA580C", True),
    ( 8.3, "quizzes","api",      "8. {attempt_id, title,\ntime_limit_sec, questions[]}","#16A34A", True),
    ( 7.3, "api",    "quiz",     "9. Данные теста получены",             "#D97706", True),
    ( 6.4, "quiz",   "student",  "10. Показать вопросы + таймер",        "#0891B2", True),
]
for (y, k1, k2, label, color, ret) in steps2_start:
    h_arrow(ax2, P2[k1], P2[k2], y, label, color, lw=2, ret=ret)

# фаза 2 — ОТВЕТЫ
rbox(ax2, 0.3, 6.0, 4.5, 0.5, "#FEF3C7", "#D97706", lw=2, r=0.2, zorder=4)
txt(ax2, 2.55, 6.25, "ФАЗА 2 — Студент отвечает на вопросы", fs=9, bold=True, color="#92400E", zorder=5)

h_arrow(ax2, P2["student"], P2["quiz"],
        5.6, "11. Выбор вариантов ответов\n(radio / checkbox)", "#2563EB", lw=2)
# self note on quiz
rbox(ax2, P2["quiz"]-0.1, 4.8, 4.8, 0.55, "#FEF9C3", "#D97706", lw=1.2, r=0.15, zorder=4)
txt(ax2, P2["quiz"]+2.4, 5.07, "12. Состояние answers{} обновляется локально", fs=8.5, color="#78350F", zorder=5)

h_arrow(ax2, P2["student"], P2["quiz"],
        4.3, "13. Нажать «Завершить тест»", "#2563EB", lw=2)

# фаза 3 — SUBMIT
rbox(ax2, 0.3, 3.85, 4.0, 0.5, "#D1FAE5", "#059669", lw=2, r=0.2, zorder=4)
txt(ax2, 2.3, 4.1, "ФАЗА 3 — Отправка и результат", fs=9, bold=True, color="#064E3B", zorder=5)

steps2_submit = [
    (3.5, "quiz",    "api",     "14. submitAttempt(attempt_id, answers[])",    "#0891B2", False),
    (2.7, "api",     "attempts","15. POST /api/attempts/:id/submit\n{answers[]}", "#D97706", False),
]
for (y, k1, k2, label, color, ret) in steps2_submit:
    h_arrow(ax2, P2[k1], P2[k2], y, label, color, lw=2, ret=ret)

# submit logic box
rbox(ax2, P2["attempts"]-0.15, 1.55, 6.5, 1.6, "#ECFDF5", "#059669", lw=1.5, r=0.2, zorder=4)
txt(ax2, P2["attempts"]+3.1, 2.65, "16. Проверка времени:", fs=8.5, bold=True, color="#065F46", zorder=5)
txt(ax2, P2["attempts"]+3.1, 2.3,  "elapsed > time_limit_sec → score = 0", fs=8, color="#065F46", zorder=5)
txt(ax2, P2["attempts"]+3.1, 1.97, "17. Подсчёт score:", fs=8.5, bold=True, color="#065F46", zorder=5)
txt(ax2, P2["attempts"]+3.1, 1.65, "correct_answers / total_questions", fs=8, color="#065F46", zorder=5)

# db update
ax2.annotate("", xy=(P2["db"], 1.45), xytext=(P2["attempts"], 1.45),
             arrowprops=dict(arrowstyle="-|>", color="#059669", lw=2,
                             mutation_scale=16), zorder=5)
txt(ax2, (P2["attempts"]+P2["db"])/2, 1.65,
    "18. UPDATE attempts SET score, status, finished_at", fs=8, color="#059669", zorder=6)

# return result
ax2.annotate("", xy=(P2["quiz"], 0.85), xytext=(P2["attempts"], 0.85),
             arrowprops=dict(arrowstyle="<|-", color="#059669", lw=2,
                             mutation_scale=16), zorder=5)
txt(ax2, (P2["quiz"]+P2["attempts"])/2, 1.05,
    "19. AttemptOut {score, status: AUTO_GRADED / COMPLETED}", fs=8.5, color="#059669", zorder=6)

# result box
rbox(ax2, 0.3, 0.4, 8.5, 0.7, "#F0FDF4", "#16A34A", lw=2, r=0.2, zorder=4)
txt(ax2, 4.55, 0.75, "20. Показать результат:  score >= passing_score → «Тест пройден!» (AUTO_GRADED)", fs=9, bold=True, color="#14532D", zorder=5)
rbox(ax2, 9.1, 0.4, 7.0, 0.7, "#FEF2F2", "#EF4444", lw=2, r=0.2, zorder=4)
txt(ax2, 12.6, 0.75, "score < passing_score → «Попробуйте ещё раз» (COMPLETED)", fs=9, bold=True, color="#991B1B", zorder=5)

plt.tight_layout(pad=0.3)
fig2.savefig(r"C:\Users\thchkr\Desktop\диплом\diploma_lms\seq_quiz.png",
             dpi=150, bbox_inches="tight", facecolor=fig2.get_facecolor())
print("Saved seq_quiz.png")
plt.close()
