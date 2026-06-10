"""Generate client-server architecture diagram for LMS."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(20, 13))
ax.set_xlim(0, 20)
ax.set_ylim(0, 13)
ax.axis("off")
fig.patch.set_facecolor("#F0F4F8")

# ── helpers ──────────────────────────────────────────────────────────────────

def box(x, y, w, h, color, radius=0.3, lw=1.5, edge="#334155"):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={radius}",
                       facecolor=color, edgecolor=edge, linewidth=lw, zorder=2)
    ax.add_patch(p)

def header_box(x, y, w, h, bg, title, fontsize=10):
    box(x, y, w, h, bg, lw=2, edge="#1E3A5F")
    ax.text(x + w/2, y + h - 0.35, title,
            ha="center", va="top", fontsize=fontsize, fontweight="bold",
            color="white", zorder=3)

def item_box(x, y, w, h, bg, text, fontsize=8.5, color="#1E293B"):
    box(x, y, w, h, bg, radius=0.2, lw=1, edge="#94A3B8")
    ax.text(x + w/2, y + h/2, text,
            ha="center", va="center", fontsize=fontsize,
            color=color, zorder=3, wrap=True,
            multialignment="center")

def arrow(x1, y1, x2, y2, label="", color="#334155"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=2, mutation_scale=18), zorder=4)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.18, label, ha="center", va="bottom",
                fontsize=7.5, color=color, fontweight="bold", zorder=5)

def double_arrow(x1, y1, x2, y2, label="", color="#334155"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="<|-|>", color=color,
                                lw=2.2, mutation_scale=18), zorder=4)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        offset = 0.22 if x1 == x2 else 0
        ax.text(mx + offset, my + 0.2, label, ha="center", va="bottom",
                fontsize=7.5, color=color, fontweight="bold", zorder=5,
                bbox=dict(boxstyle="round,pad=0.15", fc="#F0F4F8", ec="none"))

# ── TITLE ────────────────────────────────────────────────────────────────────
ax.text(10, 12.55, "Клиент-серверная архитектура LMS",
        ha="center", va="top", fontsize=16, fontweight="bold", color="#1E3A5F")

# ═══════════════════════════════════════════════════════════════════════════
# BLOCK 1 — CLIENT  (x 0.4 … 6.6)
# ═══════════════════════════════════════════════════════════════════════════
CL = 0.4; CW = 6.2; CY = 1.0; CH = 11.0
box(CL, CY, CW, CH, "#EFF6FF", lw=2.5, edge="#3B82F6")
header_box(CL, CY+CH-0.9, CW, 0.9, "#2563EB",
           "КЛИЕНТ  (Браузер)", fontsize=11)

# -- React / Vite label
ax.text(CL+CW/2, CY+CH-1.3, "React 18 + TypeScript  ·  Vite  ·  Tailwind CSS",
        ha="center", va="top", fontsize=8.5, color="#1E40AF", style="italic")

# Pages group
box(CL+0.25, CY+4.3, CW-0.5, 5.1, "#DBEAFE", lw=1.2, edge="#93C5FD")
ax.text(CL+CW/2, CY+9.1, "Страницы (Pages)",
        ha="center", va="top", fontsize=9, color="#1D4ED8", fontweight="bold")

pages = [
    ("Home", "Главная страница"),
    ("Auth", "Авторизация / регистрация"),
    ("Courses", "Список курсов"),
    ("CoursePage", "Страница курса + уроки"),
    ("QuizPage", "Прохождение теста"),
    ("MyAttempts", "Мои попытки"),
    ("MyCourses", "Мои курсы"),
    ("QuizEditor", "Редактор теста"),
    ("AdminCourses", "Управление курсами"),
    ("AdminDashboard", "Панель администратора"),
    ("AdminQuiz", "Управление тестами"),
]
cols = 2
pw, ph, px0, py0 = 2.65, 0.52, CL+0.35, CY+4.55
for i, (name, desc) in enumerate(pages):
    c = i % cols
    r = i // cols
    item_box(px0 + c*(pw+0.1), py0 + r*(ph+0.08),
             pw, ph, "#BFDBFE",
             f"{name}\n{desc}", fontsize=7.2)

# Header component
item_box(CL+0.25, CY+3.55, CW-0.5, 0.62, "#A5F3FC",
         "Header  —  навигация, роль пользователя, кнопка выхода", fontsize=8)

# API layer
box(CL+0.25, CY+0.3, CW-0.5, 2.95, "#FEF3C7", lw=1.2, edge="#FCD34D")
ax.text(CL+CW/2, CY+2.95, "API-слой  (axios)",
        ha="center", va="top", fontsize=9, color="#92400E", fontweight="bold")

api_items = [
    ("POST /auth/login\nPOST /auth/register", "#FDE68A"),
    ("GET/POST/PUT/DELETE\n/courses, /lessons", "#FDE68A"),
    ("GET/POST/PUT/DELETE\n/quizzes", "#FDE68A"),
    ("POST /attempts/submit\nGET /attempts/my", "#FDE68A"),
    ("GET /users/me/courses", "#FDE68A"),
    ("JWT Bearer Token\n(localStorage)", "#FCA5A5"),
]
aw, ah = 2.6, 0.62
for i, (txt, bg) in enumerate(api_items):
    c = i % 2; r = i // 2
    item_box(CL+0.35 + c*(aw+0.1), CY+0.35 + r*(ah+0.08),
             aw, ah, bg, txt, fontsize=7)

# ═══════════════════════════════════════════════════════════════════════════
# BLOCK 2 — SERVER  (x 7.3 … 13.5)
# ═══════════════════════════════════════════════════════════════════════════
SL = 7.3; SW = 6.2; SY = 1.0; SH = 11.0
box(SL, SY, SW, SH, "#F0FDF4", lw=2.5, edge="#16A34A")
header_box(SL, SY+SH-0.9, SW, 0.9, "#15803D",
           "СЕРВЕР  (FastAPI / Python)", fontsize=11)

ax.text(SL+SW/2, SY+SH-1.3, "Python 3.11  ·  FastAPI  ·  Uvicorn  ·  SQLAlchemy 2.0",
        ha="center", va="top", fontsize=8.5, color="#166534", style="italic")

# Middleware
item_box(SL+0.25, SY+9.0, SW-0.5, 0.65, "#BBF7D0",
         "CORS Middleware  (allow_origins=[\"*\"])", fontsize=8.5)

# Routers group
box(SL+0.25, SY+4.3, SW-0.5, 4.45, "#DCFCE7", lw=1.2, edge="#86EFAC")
ax.text(SL+SW/2, SY+8.55, "Routers  (/api/...)",
        ha="center", va="top", fontsize=9, color="#15803D", fontweight="bold")

routers = [
    ("/auth", "login, register"),
    ("/courses", "CRUD курсов и уроков"),
    ("/quizzes", "CRUD тестов и вопросов"),
    ("/attempts", "submit, my, retry"),
    ("/users", "me/courses"),
]
rw, rh = SW-0.6, 0.62
for i, (path, desc) in enumerate(routers):
    item_box(SL+0.3, SY+4.45 + i*(rh+0.1),
             rw, rh, "#A7F3D0",
             f"{path}  —  {desc}", fontsize=8.2)

# Auth / JWT module
box(SL+0.25, SY+2.5, SW-0.5, 1.65, "#ECFDF5", lw=1.2, edge="#6EE7B7")
ax.text(SL+SW/2, SY+3.93, "Auth & Security",
        ha="center", va="top", fontsize=9, color="#065F46", fontweight="bold")
auth_items = [
    ("JWT (HS256)\naccess_token", "#6EE7B7"),
    ("Bcrypt\npassword hash", "#6EE7B7"),
    ("Depends()\nget_current_user", "#6EE7B7"),
]
aaw = (SW-0.7) / 3
for i, (txt, bg) in enumerate(auth_items):
    item_box(SL+0.35 + i*(aaw+0.05), SY+2.6, aaw, 0.68, bg, txt, fontsize=7.5)

# ORM layer
item_box(SL+0.25, SY+0.85, SW-0.5, 1.42, "#D1FAE5",
         "SQLAlchemy ORM\nModels: User · Course · Lesson\nQuiz · Question · Attempt",
         fontsize=8.5)

# Session / Engine
item_box(SL+0.25, SY+0.25, SW-0.5, 0.55, "#A7F3D0",
         "SessionLocal  ·  engine  (sqlite:///./lms.db)", fontsize=8)

# ═══════════════════════════════════════════════════════════════════════════
# BLOCK 3 — DATABASE  (x 14.1 … 19.6)
# ═══════════════════════════════════════════════════════════════════════════
DL = 14.1; DW = 5.5; DY = 1.0; DH = 11.0
box(DL, DY, DW, DH, "#FFF7ED", lw=2.5, edge="#EA580C")
header_box(DL, DY+DH-0.9, DW, 0.9, "#C2410C",
           "БАЗА ДАННЫХ  (SQLite)", fontsize=11)

ax.text(DL+DW/2, DY+DH-1.3, "lms.db  —  SQLite 3",
        ha="center", va="top", fontsize=8.5, color="#9A3412", style="italic")

tables = [
    ("users",     "id · email · password_hash\nrole · created_at",                  "#FED7AA"),
    ("courses",   "id · title · description · instructor\ncategory · image · created_at / updated_at", "#FED7AA"),
    ("lessons",   "id · course_id (FK) · title\nlesson_type · content · order_index","#FED7AA"),
    ("quizzes",   "id · lesson_id (FK) · title\ntime_limit_sec · passing_score · creator_id (FK)", "#FED7AA"),
    ("questions", "id · quiz_id (FK) · type · text\noptions (JSON) · correct_answer (JSON)", "#FED7AA"),
    ("attempts",  "id · user_id (FK) · quiz_id (FK)\nstatus · score · started_at · finished_at", "#FECACA"),
]
tw = DW - 0.5; th = 1.42
ty0 = DY + 0.35
for i, (name, cols_txt, bg) in enumerate(tables):
    ty = ty0 + i * (th + 0.08)
    box(DL+0.25, ty, tw, th, bg, radius=0.2, lw=1, edge="#FB923C")
    ax.text(DL+0.25+tw/2, ty+th-0.22, name,
            ha="center", va="top", fontsize=9, fontweight="bold", color="#7C2D12")
    ax.text(DL+0.25+tw/2, ty+th-0.55, cols_txt,
            ha="center", va="top", fontsize=7, color="#431407", linespacing=1.5)

# ═══════════════════════════════════════════════════════════════════════════
# ARROWS
# ═══════════════════════════════════════════════════════════════════════════

# Client <-> Server
double_arrow(CL+CW, 6.5, SL, 6.5,
             "HTTP/REST  JSON\nJWT Bearer Token", "#1D4ED8")

# Server <-> DB
double_arrow(SL+SW, 6.5, DL, 6.5,
             "SQLAlchemy ORM\nSQL queries", "#15803D")

# ═══════════════════════════════════════════════════════════════════════════
# LEGEND
# ═══════════════════════════════════════════════════════════════════════════
legend_items = [
    (mpatches.Patch(facecolor="#EFF6FF", edgecolor="#3B82F6", lw=2), "Клиент (React SPA)"),
    (mpatches.Patch(facecolor="#F0FDF4", edgecolor="#16A34A", lw=2), "Сервер (FastAPI)"),
    (mpatches.Patch(facecolor="#FFF7ED", edgecolor="#EA580C", lw=2), "База данных (SQLite)"),
    (mpatches.Patch(facecolor="#FED7AA", edgecolor="#FB923C"),        "Таблица БД"),
    (mpatches.Patch(facecolor="#FECACA", edgecolor="#FB923C"),        "Таблица с FK-связями"),
]
handles, labels = zip(*legend_items)
ax.legend(handles, labels, loc="lower center",
          bbox_to_anchor=(0.5, -0.01), ncol=5,
          frameon=True, framealpha=0.95,
          fontsize=8.5, edgecolor="#94A3B8")

plt.tight_layout(pad=0.3)
out = r"C:\Users\thchkr\Desktop\диплом\diploma_lms\architecture_diagram.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved: {out}")
