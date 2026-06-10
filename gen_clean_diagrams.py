# coding: utf-8
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ─── primitives ───────────────────────────────────────────────────────────────

def rbox(ax, x, y, w, h, fc, ec, lw=2, r=0.25, zorder=3):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder))

def txt(ax, x, y, s, fs=10, bold=False, color="#1E293B",
        ha="center", va="center", zorder=6, ls=1.3):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs,
            fontweight="bold" if bold else "normal",
            color=color, zorder=zorder, linespacing=ls)

def h_arrow(ax, x1, x2, y, color, lw=2, label="", above=True):
    """Perfectly horizontal arrow. Label always on one side, never touching boxes."""
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=lw, mutation_scale=16), zorder=5)
    if label:
        dy = +0.22 if above else -0.22
        txt(ax, (x1 + x2) / 2, y + dy, label,
            fs=8.8, bold=True, color=color, zorder=7)

def v_arrow(ax, x, y1, y2, color, lw=2, label="", right=True):
    """Perfectly vertical arrow."""
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=lw, mutation_scale=16), zorder=5)
    if label:
        dx = +0.18 if right else -0.18
        txt(ax, x + dx, (y1 + y2) / 2, label,
            fs=8.5, bold=True, color=color,
            ha="left" if right else "right", zorder=7)

def selfbox(ax, cx, cy, w, h, fc, ec, text):
    rbox(ax, cx, cy - h / 2, w, h, fc, ec, lw=1.4, r=0.18, zorder=4)
    txt(ax, cx + w / 2, cy, text, fs=8.8, color=ec, zorder=5)

def phase_hdr(ax, x, y, w, h, fc, ec, label):
    rbox(ax, x, y, w, h, fc, ec, lw=2, r=0.2, zorder=4)
    txt(ax, x + w / 2, y + h / 2, label, fs=9.5, bold=True, color=ec, zorder=5)

def result(ax, x, y, w, h, fc, ec, title, sub):
    rbox(ax, x, y, w, h, fc, ec, lw=2, r=0.22, zorder=4)
    txt(ax, x + w / 2, y + h * 0.67, title, fs=10, bold=True, color=ec, zorder=5)
    txt(ax, x + w / 2, y + h * 0.27, sub, fs=8.5, color="#374151", zorder=5)


# ══════════════════════════════════════════════════════════════════════════════
#  DIAGRAM 1 — SEQUENCE DIAGRAM: АВТОРИЗАЦИЯ
#  Participants evenly spread. One arrow per row. Self-action as a small box.
# ══════════════════════════════════════════════════════════════════════════════
SW, SH = 22, 17
fig, ax = plt.subplots(figsize=(SW, SH), dpi=150)
ax.set_xlim(0, SW); ax.set_ylim(0, SH); ax.axis("off")
fig.patch.set_facecolor("#F8FAFC")

txt(ax, SW/2, SH-0.5,
    "Диаграмма последовательностей — Авторизация (Login)",
    fs=17, bold=True, color="#0F172A")
txt(ax, SW/2, SH-1.1,
    "Пользователь вводит email + пароль  →  JWT токен сохраняется в браузере",
    fs=10, color="#64748B")

# participant definitions
PBW, PBH = 2.5, 0.95
PTOP     = SH - 1.65     # y of top of participant boxes
LBOT     = 1.3           # lifeline bottom

parts = [
    # (cx,   label,          sub,            fc,       ec      )
    ( 2.0,  "Пользователь", "",             "#BFDBFE","#2563EB"),
    ( 5.8,  "Auth.tsx",     "React",        "#A5F3FC","#0891B2"),
    ( 9.8,  "api.ts",       "axios",        "#FDE68A","#D97706"),
    (13.8,  "FastAPI",      "/api/auth",    "#BBF7D0","#16A34A"),
    (17.8,  "База данных",  "SQLite",       "#FED7AA","#EA580C"),
    (21.0,  "localStorage", "браузер",      "#E9D5FF","#9333EA"),
]
xs = {}
for cx, lbl, sub, fc, ec in parts:
    xs[lbl] = cx
    rbox(ax, cx-PBW/2, PTOP-PBH, PBW, PBH, fc, ec, lw=2.5, r=0.28, zorder=4)
    txt(ax, cx, PTOP - PBH*0.50, lbl, fs=10.5, bold=True, zorder=5)
    if sub:
        txt(ax, cx, PTOP - PBH*0.82, sub, fs=8, color="#64748B", zorder=5)
    ax.plot([cx, cx], [PTOP-PBH, LBOT],
            color="#CBD5E1", lw=1.5, linestyle="--", zorder=2)

# row spacing — each step is 1.0 unit
ROW_START = PTOP - PBH - 0.55
RSTEP     = 1.05

def row(i, frm, to, label, color, ret=False):
    y = ROW_START - i * RSTEP
    if ret:
        h_arrow(ax, xs[frm], xs[to], y, color,
                label=label, above=True)
    else:
        h_arrow(ax, xs[frm], xs[to], y, color,
                label=label, above=True)

row(0, "Пользователь", "Auth.tsx",    "1.  Ввод email + пароль",                  "#2563EB")
row(1, "Auth.tsx",     "api.ts",      "2.  login(email, password)",                "#0891B2")
row(2, "api.ts",       "FastAPI",     "3.  POST /api/auth/login  {email, password}","#D97706")
row(3, "FastAPI",      "База данных", "4.  SELECT * FROM users WHERE email = ?",   "#16A34A")
row(4, "База данных",  "FastAPI",     "5.  User {id, email, password_hash, role}", "#EA580C")

# self-action rows (box on FastAPI lifeline)
y6 = ROW_START - 5 * RSTEP
selfbox(ax, xs["FastAPI"]+0.1, y6, 4.2, 0.46,
        "#F0FDF4", "#16A34A", "6.  verify_password()  →  bcrypt")

y7 = ROW_START - 6 * RSTEP
selfbox(ax, xs["FastAPI"]+0.1, y7, 4.2, 0.46,
        "#F0FDF4", "#16A34A", "7.  create_access_token()  →  JWT HS256")

row(7, "FastAPI",      "api.ts",      "8.  {access_token, token_type: bearer}",   "#16A34A")
row(8, "api.ts",       "localStorage","9.  localStorage.setItem('token', jwt)",    "#9333EA")
row(9, "api.ts",       "Auth.tsx",    "10. Ответ получен",                         "#D97706")
row(10,"Auth.tsx",     "Пользователь","11. navigate('/')  →  редирект на главную", "#0891B2")

# result boxes
result(ax, 0.3,  LBOT-0.1, 9.5, 1.2,
       "#F0FDF4","#16A34A","УСПЕХ",
       "Токен сохранён → каждый запрос содержит  Authorization: Bearer <token>")
result(ax, 10.2, LBOT-0.1, 9.5, 1.2,
       "#FEF2F2","#EF4444","ОШИБКА",
       "FastAPI → 401 Unauthorized  «Неверный email или пароль»")

plt.tight_layout(pad=0.3)
fig.savefig(r"C:\Users\thchkr\Desktop\диплом\diploma_lms\seq_auth.png",
            dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved seq_auth.png")
plt.close()


# ══════════════════════════════════════════════════════════════════════════════
#  DIAGRAM 2 — INTERACTION DIAGRAM: ПРОХОЖДЕНИЕ ТЕСТА
#
#  Layout: all objects in ONE row at top.
#  Messages flow top-to-bottom, each on its own y-level.
#  Arrows are ONLY horizontal. FastAPI handles both /quizzes and /attempts.
#  A single vertical line for DB separates concerns.
# ══════════════════════════════════════════════════════════════════════════════
IW, IH = 26, 22
fig2, ax2 = plt.subplots(figsize=(IW, IH), dpi=150)
ax2.set_xlim(0, IW); ax2.set_ylim(0, IH); ax2.axis("off")
fig2.patch.set_facecolor("#F8FAFC")

txt(ax2, IW/2, IH-0.5,
    "Диаграмма взаимодействий — Прохождение теста (Quiz)",
    fs=17, bold=True, color="#0F172A")
txt(ax2, IW/2, IH-1.1,
    "Объекты системы и пронумерованные сообщения между ними  ·  3 фазы",
    fs=10, color="#64748B")

# objects in one row
OBW, OBH = 3.6, 1.05
OTOP = IH - 1.7

objects = [
    # (cx,   label,              sub,                   fc,       ec      )
    ( 2.3,  "Студент",          "",                    "#BFDBFE","#2563EB"),
    ( 6.5,  "QuizPage.tsx",     "React · страница",    "#A5F3FC","#0891B2"),
    (11.0,  "api.ts",           "axios",               "#FDE68A","#D97706"),
    (16.0,  "FastAPI",          "/quizzes · /attempts","#BBF7D0","#16A34A"),
    (21.5,  "База данных",      "SQLite · lms.db",     "#FED7AA","#EA580C"),
]
xs2 = {}
for cx, lbl, sub, fc, ec in objects:
    xs2[lbl] = cx
    rbox(ax2, cx-OBW/2, OTOP-OBH, OBW, OBH, fc, ec, lw=2.5, r=0.28, zorder=4)
    txt(ax2, cx, OTOP - OBH*0.47, lbl, fs=10.5, bold=True, zorder=5)
    if sub:
        txt(ax2, cx, OTOP - OBH*0.80, sub, fs=8, color="#64748B", zorder=5)
    ax2.plot([cx, cx], [OTOP-OBH, 1.2],
             color="#CBD5E1", lw=1.5, linestyle="--", zorder=2)

# ── row helper ────────────────────────────────────────────────────────────────
MSG_START = OTOP - OBH - 0.52
MSTEP     = 0.88   # vertical gap between messages

def msg(i, frm, to, label, color):
    y = MSG_START - i * MSTEP
    h_arrow(ax2, xs2[frm], xs2[to], y, color, lw=2, label=label, above=True)

def sbox(i, cx, label, fc, ec):
    y = MSG_START - i * MSTEP
    selfbox(ax2, cx+0.1, y, 4.5, 0.44, fc, ec, label)

def phase(x, y, w, h, fc, ec, label):
    phase_hdr(ax2, x, y, w, h, fc, ec, label)

# ── phase labels ──────────────────────────────────────────────────────────────
phase(0.3,  IH-2.25, 5.8, 0.62, "#DBEAFE","#2563EB", "ФАЗА 1 — Старт теста")
phase(6.4,  IH-2.25, 6.5, 0.62, "#FEF3C7","#D97706", "ФАЗА 2 — Ответы")
phase(13.2, IH-2.25, 7.5, 0.62, "#D1FAE5","#059669", "ФАЗА 3 — Отправка и результат")

# ── ФАЗА 1: Старт теста (строки 0–9) ─────────────────────────────────────────
msg(0, "Студент",      "QuizPage.tsx", "1.  нажать «Начать тест»",                    "#2563EB")
msg(1, "QuizPage.tsx", "api.ts",       "2.  startQuiz(quizId)",                        "#0891B2")
msg(2, "api.ts",       "FastAPI",      "3.  POST /api/quizzes/:id/start   Bearer <token>","#D97706")
msg(3, "FastAPI",      "База данных",  "4.  SELECT * FROM quizzes + questions WHERE id = ?","#16A34A")
msg(4, "База данных",  "FastAPI",      "5.  Quiz {title, time_limit_sec, questions[]}","#EA580C")
msg(5, "FastAPI",      "База данных",  "6.  INSERT INTO attempts  (status='IN_PROGRESS')","#16A34A")
msg(6, "База данных",  "FastAPI",      "7.  attempt_id",                               "#EA580C")
msg(7, "FastAPI",      "api.ts",       "8.  {attempt_id, title, time_limit_sec, questions[]}","#16A34A")
msg(8, "api.ts",       "QuizPage.tsx", "9.  данные теста получены",                    "#D97706")
msg(9, "QuizPage.tsx", "Студент",      "10. показать вопросы + таймер",                "#0891B2")

# ── ФАЗА 2: Ответы (строки 10–12) ────────────────────────────────────────────
msg(10, "Студент", "QuizPage.tsx", "11. выбор вариантов (radio / checkbox)",           "#2563EB")

# local state note
y_note = MSG_START - 11 * MSTEP
rbox(ax2, xs2["QuizPage.tsx"]-1.6, y_note-0.28, 5.2, 0.70,
     "#F3E8FF","#9333EA", lw=1.4, r=0.18, zorder=4)
txt(ax2, xs2["QuizPage.tsx"]+0.9, y_note+0.07,
    "12. answers{} — локальное состояние React\n      не покидает браузер",
    fs=8.5, color="#6B21A8", zorder=5)

msg(12, "Студент", "QuizPage.tsx", "13. нажать «Завершить тест»",                     "#2563EB")

# ── ФАЗА 3: Submit (строки 13–19) ────────────────────────────────────────────
msg(13, "QuizPage.tsx", "api.ts",      "14. submitAttempt(attempt_id, answers[])",     "#0891B2")
msg(14, "api.ts",       "FastAPI",     "15. POST /api/attempts/:id/submit  {answers[]}","#D97706")

sbox(15, xs2["FastAPI"],
     "16. проверка времени:  elapsed > time_limit_sec → score = 0",
     "#ECFDF5","#059669")
sbox(16, xs2["FastAPI"],
     "17. подсчёт score:  correct_answers / total_questions",
     "#ECFDF5","#059669")

msg(17, "FastAPI",      "База данных", "18. UPDATE attempts SET score, status, finished_at","#16A34A")
msg(18, "База данных",  "FastAPI",     "19. OK",                                       "#EA580C")
msg(19, "FastAPI",      "api.ts",      "20. AttemptOut {score, status: AUTO_GRADED / COMPLETED}","#16A34A")
msg(20, "api.ts",       "QuizPage.tsx","21. результат получен",                        "#D97706")
msg(21, "QuizPage.tsx", "Студент",     "22. показать результат",                       "#0891B2")

# ── result boxes ──────────────────────────────────────────────────────────────
result(ax2, 0.3,  1.25, 12.0, 1.45,
       "#F0FDF4","#16A34A",
       "AUTO_GRADED — Тест пройден!",
       "score >= passing_score (70%)  →  кнопка «Вернуться к курсу»")
result(ax2, 12.8, 1.25, 12.8, 1.45,
       "#FEF2F2","#EF4444",
       "COMPLETED — Попробуйте ещё раз",
       "score < passing_score  →  POST /attempts/quiz/:id/retry")

plt.tight_layout(pad=0.3)
fig2.savefig(r"C:\Users\thchkr\Desktop\диплом\diploma_lms\interaction.png",
             dpi=150, bbox_inches="tight", facecolor=fig2.get_facecolor())
print("Saved interaction.png")
plt.close()
