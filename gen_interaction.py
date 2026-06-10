# coding: utf-8
"""
seq_auth.png      — диаграмма последовательностей (Login)
interaction.png   — диаграмма взаимодействий (Quiz, collaboration style)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ─── helpers ──────────────────────────────────────────────────────────────────

def rbox(ax, x, y, w, h, fc, ec, lw=2.2, r=0.3, zorder=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder))

def txt(ax, x, y, s, fs=10, bold=False, color="#1E293B",
        ha="center", va="center", zorder=6, ls=1.35):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs,
            fontweight="bold" if bold else "normal",
            color=color, zorder=zorder, linespacing=ls)

def obj_box(ax, cx, cy, w, h, fc, ec, title, sub="", zorder=4):
    """Object box centered at (cx,cy)."""
    rbox(ax, cx-w/2, cy-h/2, w, h, fc, ec, lw=2.5, r=0.3, zorder=zorder)
    if sub:
        txt(ax, cx, cy+h*0.17, title, fs=11, bold=True, color="#1E293B", zorder=zorder+1)
        txt(ax, cx, cy-h*0.22, sub,   fs=8.5, color="#475569", zorder=zorder+1)
    else:
        txt(ax, cx, cy, title, fs=11, bold=True, color="#1E293B", zorder=zorder+1)

def link(ax, x1, y1, x2, y2, color="#94A3B8", lw=2):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, zorder=2)

def msg_arrow(ax, x1, y1, x2, y2, msgs, color="#334155",
              lw=2, offset=(0, 0.28), ret=False):
    """Arrow with message label(s). msgs = list of strings."""
    style = "<|-" if ret else "-|>"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color,
                                lw=lw, mutation_scale=16), zorder=5)
    mx = (x1+x2)/2 + offset[0]
    my = (y1+y2)/2 + offset[1]
    label = "\n".join(msgs)
    ax.text(mx, my, label, ha="center", va="center", fontsize=8.5,
            color=color, fontweight="bold", zorder=7, linespacing=1.35,
            bbox=dict(boxstyle="round,pad=0.25", fc="#F8FAFC",
                      ec=color, lw=1.0, alpha=0.92))


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 1 — SEQUENCE (AUTH / LOGIN)  — оставляем чистую версию
# ══════════════════════════════════════════════════════════════════════════════

def make_seq():
    W, H = 22, 17
    fig, ax = plt.subplots(figsize=(W, H), dpi=150)
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    fig.patch.set_facecolor("#F8FAFC")

    txt(ax, W/2, H-0.45, "Диаграмма последовательностей — Авторизация",
        fs=17, bold=True, color="#0F172A")
    txt(ax, W/2, H-1.0,
        "Пользователь вводит email + пароль  →  JWT сохраняется в браузере",
        fs=10, color="#64748B")

    TOP = H - 1.5

    # participants
    parts = [
        (2.2,  "Пользователь", "",               "#BFDBFE","#2563EB"),
        (5.8,  "Auth.tsx",     "React",           "#A5F3FC","#0891B2"),
        (9.5,  "api.ts",       "axios",           "#FDE68A","#D97706"),
        (13.5, "FastAPI",      "/api/auth",       "#BBF7D0","#16A34A"),
        (17.5, "База данных",  "SQLite · users",  "#FED7AA","#EA580C"),
        (21.0, "localStorage", "браузер",         "#E9D5FF","#9333EA"),
    ]

    PW, PH = 2.5, 0.95
    xs = {}
    for cx, label, sub, fc, ec in parts:
        xs[label] = cx
        rbox(ax, cx-PW/2, TOP-PH, PW, PH, fc, ec, lw=2.5, r=0.3, zorder=4)
        txt(ax, cx, TOP-PH*0.52, label, fs=10.5, bold=True, zorder=5)
        if sub:
            txt(ax, cx, TOP-PH*0.82, sub, fs=8, color="#64748B", zorder=5)
        # lifeline
        ax.plot([cx, cx], [TOP-PH, 0.6], color="#CBD5E1", lw=1.5,
                linestyle="--", zorder=2)

    def harrow(x1, x2, y, label, color, ret=False, dy=0.2):
        style = "<|-" if ret else "-|>"
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle=style, color=color,
                                    lw=2, mutation_scale=16), zorder=5)
        ax.text((x1+x2)/2, y+dy, label, ha="center", va="bottom",
                fontsize=8.5, color=color, fontweight="bold", zorder=7,
                bbox=dict(boxstyle="round,pad=0.2", fc="#F8FAFC",
                          ec=color, lw=0.8, alpha=0.9))

    def self_box(cx, y, label, fc="#F0FDF4", ec="#16A34A"):
        rbox(ax, cx+0.1, y-0.22, 4.2, 0.44, fc, ec, lw=1.3, r=0.15, zorder=4)
        txt(ax, cx+2.2, y, label, fs=8.5, color="#14532D", zorder=5)

    # ── шаги ──
    harrow(xs["Пользователь"], xs["Auth.tsx"],    14.8,
           "1.  Ввод email + пароль",              "#2563EB")
    harrow(xs["Auth.tsx"],     xs["api.ts"],       13.7,
           "2.  login(email, password)",            "#0891B2")
    harrow(xs["api.ts"],       xs["FastAPI"],      12.6,
           "3.  POST /api/auth/login  {email, password}", "#D97706")
    harrow(xs["FastAPI"],      xs["База данных"],  11.5,
           "4.  SELECT * FROM users WHERE email = ?", "#16A34A")
    harrow(xs["База данных"],  xs["FastAPI"],      10.5,
           "5.  User {id, email, password_hash, role}", "#EA580C", ret=True)
    self_box(xs["FastAPI"],    9.5,
             "6.  verify_password()  →  bcrypt сравнение хешей")
    self_box(xs["FastAPI"],    8.6,
             "7.  create_access_token()  →  JWT HS256")
    harrow(xs["FastAPI"],      xs["api.ts"],       7.7,
           "8.  {access_token, token_type: bearer}", "#16A34A", ret=True)
    harrow(xs["api.ts"],       xs["localStorage"], 6.7,
           "9.  localStorage.setItem('token', jwt)", "#9333EA")
    harrow(xs["api.ts"],       xs["Auth.tsx"],     5.7,
           "10.  Ответ получен",                   "#D97706", ret=True)
    harrow(xs["Auth.tsx"],     xs["Пользователь"], 4.7,
           "11.  navigate('/')  →  редирект на главную", "#0891B2", ret=True)

    # итог
    rbox(ax, 0.4, 0.65, 9.5, 1.15, "#F0FDF4", "#16A34A", lw=2, r=0.25, zorder=4)
    txt(ax, 5.15, 1.38, "УСПЕХ", fs=9, bold=True, color="#14532D", zorder=5)
    txt(ax, 5.15, 1.0,
        "Токен сохранён в localStorage → каждый следующий запрос\nотправляет:  Authorization: Bearer <token>",
        fs=8.5, color="#064E3B", zorder=5)

    rbox(ax, 10.2, 0.65, 8.5, 1.15, "#FEF2F2", "#EF4444", lw=2, r=0.25, zorder=4)
    txt(ax, 14.45, 1.38, "ОШИБКА", fs=9, bold=True, color="#DC2626", zorder=5)
    txt(ax, 14.45, 1.0,
        "FastAPI → 401 Unauthorized\n«Неверный email или пароль»",
        fs=8.5, color="#7F1D1D", zorder=5)

    plt.tight_layout(pad=0.3)
    fig.savefig(r"C:\Users\thchkr\Desktop\диплом\diploma_lms\seq_auth.png",
                dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print("Saved seq_auth.png")
    plt.close()

make_seq()


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 2 — COLLABORATION / INTERACTION (Quiz flow)
# ══════════════════════════════════════════════════════════════════════════════

W2, H2 = 24, 18
fig2, ax2 = plt.subplots(figsize=(W2, H2), dpi=150)
ax2.set_xlim(0, W2); ax2.set_ylim(0, H2); ax2.axis("off")
fig2.patch.set_facecolor("#F8FAFC")

txt(ax2, W2/2, H2-0.45,
    "Диаграмма взаимодействий — Прохождение теста",
    fs=17, bold=True, color="#0F172A")
txt(ax2, W2/2, H2-1.05,
    "Объекты системы и пронумерованные сообщения между ними",
    fs=10, color="#64748B")

# ── объекты (cx, cy, w, h) ────────────────────────────────────────────────────
OBJ = {
    "student":  ( 3.5, 14.0),
    "quizpage": (11.5, 14.0),
    "api":      (11.5,  9.5),
    "qrouter":  ( 4.5,  5.5),
    "arouter":  (19.0,  9.5),
    "db":       (19.0,  4.5),
    "local":    ( 3.5,  9.5),
}
OW, OH = 3.6, 1.3

boxes = [
    ("student",  "Студент",          "",                      "#BFDBFE","#2563EB"),
    ("quizpage", "QuizPage.tsx",      "React · страница",      "#A5F3FC","#0891B2"),
    ("api",      "api.ts",            "axios · HTTP-клиент",   "#FDE68A","#D97706"),
    ("qrouter",  "FastAPI /quizzes",  "/api/quizzes",          "#BBF7D0","#16A34A"),
    ("arouter",  "FastAPI /attempts", "/api/attempts",         "#D1FAE5","#059669"),
    ("db",       "База данных",       "SQLite · lms.db",       "#FED7AA","#EA580C"),
    ("local",    "localStorage",      "JWT · браузер",         "#E9D5FF","#9333EA"),
]
for key, title, sub, fc, ec in boxes:
    cx, cy = OBJ[key]
    obj_box(ax2, cx, cy, OW, OH, fc, ec, title, sub)

# ── рисуем линии-связи между объектами ───────────────────────────────────────
def edge(k1, k2, color="#CBD5E1", lw=1.8):
    x1, y1 = OBJ[k1]; x2, y2 = OBJ[k2]
    ax2.plot([x1, x2], [y1, y2], color=color, lw=lw, zorder=1, linestyle="-")

edge("student",  "quizpage", "#93C5FD")
edge("quizpage", "api",      "#FCD34D")
edge("api",      "qrouter",  "#6EE7B7")
edge("api",      "arouter",  "#6EE7B7")
edge("qrouter",  "db",       "#FBB6CE")  # diagonal
edge("arouter",  "db",       "#FBB6CE")
edge("quizpage", "local",    "#C4B5FD")

# ── сообщения ────────────────────────────────────────────────────────────────
# helper: arrow + label along a link
def cmsg(ax, k1, k2, msgs, color, ret=False,
         frac=0.5, perp=(0, 0)):
    """
    Place arrow at fraction `frac` along k1→k2 edge.
    perp: manual (dx,dy) nudge for the label box.
    """
    x1, y1 = OBJ[k1]; x2, y2 = OBJ[k2]
    # arrow tip/tail near box edges (approx half-box offset)
    dx, dy = x2-x1, y2-y1
    dist = (dx**2+dy**2)**0.5
    if dist == 0: return
    ux, uy = dx/dist, dy/dist
    # start / end clear of boxes
    sx = x1 + ux*OW*0.52
    sy = y1 + uy*OH*0.52
    ex = x2 - ux*OW*0.52
    ey = y2 - uy*OH*0.52
    # point along the segment
    tx = sx + (ex-sx)*frac
    ty = sy + (ey-sy)*frac
    # tip slightly beyond
    tip_f = min(frac+0.15, 1.0)
    tipx = sx + (ex-sx)*tip_f
    tipy = sy + (ey-sy)*tip_f
    style = "<|-" if ret else "-|>"
    ax.annotate("", xy=(tipx, tipy), xytext=(tx, ty),
                arrowprops=dict(arrowstyle=style, color=color,
                                lw=2, mutation_scale=16), zorder=5)
    label = "\n".join(msgs)
    ax.text(tx + perp[0], ty + perp[1], label,
            ha="center", va="center", fontsize=8.5,
            color=color, fontweight="bold", zorder=7, linespacing=1.3,
            bbox=dict(boxstyle="round,pad=0.28", fc="#F8FAFC",
                      ec=color, lw=1.1, alpha=0.95))

# ── ФАЗА 1: Старт теста ───────────────────────────────────────────────────────
rbox(ax2, 0.25, 15.55, 5.6, 0.65, "#DBEAFE", "#2563EB", lw=2, r=0.2, zorder=4)
txt(ax2, 3.05, 15.875, "ФАЗА 1 — Старт теста", fs=9.5, bold=True, color="#1E3A8A", zorder=5)

cmsg(ax2, "student", "quizpage",
     ["1: нажать «Начать тест»"],
     "#2563EB", frac=0.45, perp=(2.8, 0.3))

cmsg(ax2, "quizpage", "api",
     ["2: startQuiz(quizId)"],
     "#0891B2", frac=0.45, perp=(2.2, 0.0))

cmsg(ax2, "api", "qrouter",
     ["3: POST /api/quizzes/:id/start", "    Bearer <token>"],
     "#D97706", frac=0.42, perp=(-1.5, 1.2))

cmsg(ax2, "qrouter", "db",
     ["4: SELECT * FROM quizzes", "    SELECT * FROM questions"],
     "#16A34A", frac=0.40, perp=(2.2, 0.5))

cmsg(ax2, "db", "qrouter",
     ["5: Quiz + Questions[]"],
     "#EA580C", ret=True, frac=0.62, perp=(-2.8, -0.4))

cmsg(ax2, "qrouter", "db",
     ["6: INSERT INTO attempts", "    status='IN_PROGRESS'"],
     "#16A34A", frac=0.60, perp=(2.0, -0.8))

cmsg(ax2, "db", "qrouter",
     ["7: attempt_id"],
     "#EA580C", ret=True, frac=0.75, perp=(-2.5, -1.6))

cmsg(ax2, "qrouter", "api",
     ["8: {attempt_id, title,", "    time_limit_sec, questions[]}"],
     "#16A34A", ret=True, frac=0.52, perp=(-3.2, 1.8))

cmsg(ax2, "api", "quizpage",
     ["9: данные теста"],
     "#D97706", ret=True, frac=0.55, perp=(-2.2, -0.35))

cmsg(ax2, "quizpage", "student",
     ["10: показать вопросы + таймер"],
     "#0891B2", ret=True, frac=0.55, perp=(-3.3, 0.3))

# ── ФАЗА 2: Ответы ────────────────────────────────────────────────────────────
rbox(ax2, 6.2, 15.55, 5.8, 0.65, "#FEF3C7", "#D97706", lw=2, r=0.2, zorder=4)
txt(ax2, 9.1, 15.875, "ФАЗА 2 — Ответы на вопросы", fs=9.5, bold=True, color="#92400E", zorder=5)

# student → quizpage (немного правее)
ax2.annotate("", xy=(OBJ["quizpage"][0]-OW/2, 12.9),
             xytext=(OBJ["student"][0]+OW/2, 12.9),
             arrowprops=dict(arrowstyle="-|>", color="#2563EB",
                             lw=2, mutation_scale=16), zorder=5)
ax2.text(7.5, 13.15, "11: выбор вариантов\n(radio / checkbox)",
         ha="center", va="center", fontsize=8.5, fontweight="bold",
         color="#2563EB", zorder=7,
         bbox=dict(boxstyle="round,pad=0.25", fc="#F8FAFC", ec="#2563EB", lw=1.0))

# local storage note
rbox(ax2, 0.3, 11.1, 6.2, 1.05, "#F3E8FF", "#9333EA", lw=1.5, r=0.2, zorder=4)
txt(ax2, 3.4, 11.63, "12: answers{} — локальное состояние", fs=8.5, bold=True, color="#6B21A8", zorder=5)
txt(ax2, 3.4, 11.25, "хранится в React useState()\nне покидает браузер", fs=8, color="#581C87", zorder=5)

# student → quizpage submit
ax2.annotate("", xy=(OBJ["quizpage"][0]-OW/2, 10.9),
             xytext=(OBJ["student"][0]+OW/2, 10.9),
             arrowprops=dict(arrowstyle="-|>", color="#2563EB",
                             lw=2, mutation_scale=16), zorder=5)
ax2.text(7.5, 11.13, "13: нажать «Завершить тест»",
         ha="center", va="center", fontsize=8.5, fontweight="bold",
         color="#2563EB", zorder=7,
         bbox=dict(boxstyle="round,pad=0.25", fc="#F8FAFC", ec="#2563EB", lw=1.0))

# ── ФАЗА 3: Submit ────────────────────────────────────────────────────────────
rbox(ax2, 12.5, 15.55, 5.6, 0.65, "#D1FAE5", "#059669", lw=2, r=0.2, zorder=4)
txt(ax2, 15.3, 15.875, "ФАЗА 3 — Отправка и результат", fs=9.5, bold=True, color="#064E3B", zorder=5)

cmsg(ax2, "quizpage", "api",
     ["14: submitAttempt(attempt_id, answers[])"],
     "#0891B2", frac=0.42, perp=(-3.5, -0.4))

cmsg(ax2, "api", "arouter",
     ["15: POST /api/attempts/:id/submit", "    {answers[]}  Bearer <token>"],
     "#D97706", frac=0.45, perp=(0.0, 0.5))

# arouter → db (update)
ax2.annotate("", xy=(OBJ["db"][0], OBJ["db"][1]+OH/2),
             xytext=(OBJ["arouter"][0], OBJ["arouter"][1]-OH/2),
             arrowprops=dict(arrowstyle="-|>", color="#059669",
                             lw=2, mutation_scale=16), zorder=5)
ax2.text(19.7, 7.0, "16: проверить время\n17: подсчёт score\n18: UPDATE attempts",
         ha="center", va="center", fontsize=8.5, fontweight="bold",
         color="#059669", zorder=7,
         bbox=dict(boxstyle="round,pad=0.28", fc="#F8FAFC", ec="#059669", lw=1.1))

cmsg(ax2, "arouter", "api",
     ["19: AttemptOut {score, status}"],
     "#059669", ret=True, frac=0.52, perp=(-1.5, -0.5))

cmsg(ax2, "api", "quizpage",
     ["20: результат получен"],
     "#D97706", ret=True, frac=0.55, perp=(2.5, 0.35))

cmsg(ax2, "quizpage", "student",
     ["21: показать результат"],
     "#0891B2", ret=True, frac=0.52, perp=(-3.5, -0.3))

# ── итоговые блоки ────────────────────────────────────────────────────────────
rbox(ax2, 0.3, 0.4, 10.5, 1.3, "#F0FDF4", "#16A34A", lw=2, r=0.25, zorder=4)
txt(ax2, 5.55, 1.15, "AUTO_GRADED  — Тест пройден!", fs=10, bold=True, color="#14532D", zorder=5)
txt(ax2, 5.55, 0.73, "score >= passing_score (70%)  →  кнопка «Вернуться к курсу»", fs=9, color="#064E3B", zorder=5)

rbox(ax2, 11.2, 0.4, 12.2, 1.3, "#FEF2F2", "#EF4444", lw=2, r=0.25, zorder=4)
txt(ax2, 17.3, 1.15, "COMPLETED  — Попробуйте ещё раз", fs=10, bold=True, color="#991B1B", zorder=5)
txt(ax2, 17.3, 0.73, "score < passing_score  →  кнопка повтора  →  POST /attempts/quiz/:id/retry", fs=9, color="#7F1D1D", zorder=5)

plt.tight_layout(pad=0.3)
fig2.savefig(r"C:\Users\thchkr\Desktop\диплом\diploma_lms\interaction.png",
             dpi=150, bbox_inches="tight", facecolor=fig2.get_facecolor())
print("Saved interaction.png")
plt.close()
