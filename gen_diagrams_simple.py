# coding: utf-8
"""Simple block diagrams — no internal arrows, only clean inter-block arrows."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ─── helpers ──────────────────────────────────────────────────────────────────

def rbox(ax, x, y, w, h, fc, ec, lw=2.5, r=0.35, zorder=2):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder))

def txt(ax, x, y, s, fs=12, bold=False, color="#1E293B",
        ha="center", va="center", zorder=5, ls=1.35):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs,
            fontweight="bold" if bold else "normal",
            color=color, zorder=zorder, linespacing=ls)

def h_arrow(ax, x1, x2, y, color, lw=4):
    """Perfectly horizontal double-headed arrow between two x positions at height y."""
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<|-|>", color=color,
                                lw=lw, mutation_scale=26), zorder=8)

def arrow_label(ax, x, y, text, color, bg):
    ax.text(x, y, text, ha="center", va="center", fontsize=11,
            fontweight="bold", color=color, zorder=9,
            bbox=dict(boxstyle="round,pad=0.4", fc=bg, ec=color, lw=2.0))

def mod(ax, x, y, w, h, fc, ec, title, sub="", tfs=11, sfs=9):
    rbox(ax, x, y, w, h, fc, ec, lw=1.8, r=0.22, zorder=3)
    ty = y + h * (0.65 if sub else 0.5)
    txt(ax, x+w/2, ty, title, fs=tfs, bold=True, color="#1E293B", zorder=4)
    if sub:
        txt(ax, x+w/2, y + h*0.25, sub, fs=sfs, color="#374151", zorder=4)


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 1 — CLIENT-SERVER ARCHITECTURE  (no internal arrows)
# ══════════════════════════════════════════════════════════════════════════════
W, H = 26, 15
fig, ax = plt.subplots(figsize=(W, H), dpi=150)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
fig.patch.set_facecolor("#F1F5F9")

txt(ax, W/2, H-0.55, "Клиент-серверная архитектура LMS",
    fs=20, bold=True, color="#0F172A")

# ── КЛИЕНТ ───────────────────────────────────────────────────────────────────
CX, CY, CW, CH = 0.4, 0.5, 7.2, 13.5
rbox(ax, CX, CY, CW, CH, "#EFF6FF", "#2563EB", lw=3, r=0.5)
txt(ax, CX+CW/2, CY+CH-0.6, "КЛИЕНТ", fs=18, bold=True, color="#1E3A8A")
txt(ax, CX+CW/2, CY+CH-1.15, "Браузер · React + TypeScript", fs=11, color="#1D4ED8")

client_blocks = [
    (0.75, 11.15, 6.5, 1.3,  "#BFDBFE","#3B82F6", "main.tsx  /  App.tsx",
     "Точка входа · React Router · маршруты"),
    (0.75,  9.55, 6.5, 1.3,  "#BAE6FD","#0284C7", "Страницы (Pages)",
     "Auth · Courses · CoursePage · QuizPage\nMyAttempts · MyCourses · QuizEditor · Admin*"),
    (0.75,  8.05, 6.5, 1.2,  "#A5F3FC","#0891B2", "Header.tsx",
     "Навигация · роль пользователя · logout"),
    (0.75,  6.45, 6.5, 1.3,  "#FDE68A","#D97706", "api.ts  (axios)",
     "GET / POST / PUT / DELETE\nJWT Bearer interceptor · baseURL='/api'"),
    (0.75,  4.85, 6.5, 1.3,  "#FCA5A5","#DC2626", "localStorage",
     "Хранение access_token (JWT)"),
    (0.75,  3.25, 6.5, 1.3,  "#C4B5FD","#7C3AED", "Tailwind CSS  ·  Vite",
     "Стили · сборка проекта"),
    (0.75,  1.65, 6.5, 1.3,  "#D1FAE5","#059669", "React Router v6",
     "Клиентская маршрутизация · защита роутов"),
    (0.75,  0.65, 6.5, 0.8,  "#E0E7FF","#6366F1", "React 18  ·  TypeScript  ·  Vite  ·  axios", ""),
]
for x, y, w, h, fc, ec, t1, t2 in client_blocks:
    mod(ax, x, y, w, h, fc, ec, t1, t2)

# ── СЕРВЕР ────────────────────────────────────────────────────────────────────
SX, SY, SW, SH = 9.4, 0.5, 7.2, 13.5
rbox(ax, SX, SY, SW, SH, "#F0FDF4", "#16A34A", lw=3, r=0.5)
txt(ax, SX+SW/2, SY+SH-0.6, "СЕРВЕР", fs=18, bold=True, color="#14532D")
txt(ax, SX+SW/2, SY+SH-1.15, "Python · FastAPI · Uvicorn", fs=11, color="#15803D")

server_blocks = [
    (9.75, 11.15, 6.5, 1.3,  "#BBF7D0","#22C55E", "main.py",
     "FastAPI() · CORSMiddleware · /api/health"),
    (9.75,  9.55, 6.5, 1.3,  "#A7F3D0","#10B981", "Роутеры  (/api/...)",
     "/auth · /courses · /quizzes · /attempts · /users"),
    (9.75,  8.05, 6.5, 1.2,  "#6EE7B7","#059669", "auth.py  +  deps.py",
     "JWT HS256 · bcrypt · get_current_user"),
    (9.75,  6.45, 6.5, 1.3,  "#D1FAE5","#34D399", "models.py",
     "SQLAlchemy ORM\nUser · Course · Lesson · Quiz · Question · Attempt"),
    (9.75,  4.85, 6.5, 1.3,  "#ECFDF5","#6EE7B7", "schemas.py",
     "Pydantic v2 · валидация запросов и ответов"),
    (9.75,  3.25, 6.5, 1.3,  "#C7D2FE","#6366F1", "config.py  +  database.py",
     "SECRET_KEY · DATABASE_URL · engine · SessionLocal"),
    (9.75,  1.65, 6.5, 1.3,  "#FEF3C7","#F59E0B", "python-jose  ·  passlib  ·  bcrypt",
     "Библиотеки безопасности"),
    (9.75,  0.65, 6.5, 0.8,  "#E0E7FF","#6366F1", "SQLAlchemy 2.0  ·  FastAPI  ·  Uvicorn", ""),
]
for x, y, w, h, fc, ec, t1, t2 in server_blocks:
    mod(ax, x, y, w, h, fc, ec, t1, t2)

# ── БАЗА ДАННЫХ ───────────────────────────────────────────────────────────────
DX, DY, DW, DH = 18.4, 0.5, 7.2, 13.5
rbox(ax, DX, DY, DW, DH, "#FFF7ED", "#EA580C", lw=3, r=0.5)
txt(ax, DX+DW/2, DY+DH-0.6, "БАЗА ДАННЫХ", fs=18, bold=True, color="#7C2D12")
txt(ax, DX+DW/2, DY+DH-1.15, "SQLite · lms.db", fs=11, color="#C2410C")

db_blocks = [
    (18.75, 11.15, 6.5, 1.2,  "#FED7AA","#FB923C", "users",
     "id · email · password_hash · role"),
    (18.75,  9.65, 6.5, 1.2,  "#FED7AA","#FB923C", "courses",
     "id · title · category · instructor · image"),
    (18.75,  8.15, 6.5, 1.2,  "#FED7AA","#FB923C", "lessons",
     "id · course_id (FK) · title · type · content"),
    (18.75,  6.65, 6.5, 1.2,  "#FED7AA","#FB923C", "quizzes",
     "id · lesson_id (FK) · title · passing_score"),
    (18.75,  5.15, 6.5, 1.2,  "#FED7AA","#FB923C", "questions",
     "id · quiz_id (FK) · type · options (JSON)"),
    (18.75,  3.65, 6.5, 1.2,  "#FECACA","#EF4444", "attempts",
     "id · user_id (FK) · quiz_id (FK) · score"),
    (18.75,  1.85, 6.5, 1.5,  "#E0E7FF","#6366F1", "FK  (CASCADE DELETE)",
     "courses -> lessons -> quizzes -> questions"),
    (18.75,  0.65, 6.5, 0.9,  "#FEF3C7","#F59E0B", "SQLite 3  ·  файл lms.db", ""),
]
for x, y, w, h, fc, ec, t1, t2 in db_blocks:
    mod(ax, x, y, w, h, fc, ec, t1, t2)

# ── СТРЕЛКИ МЕЖДУ БЛОКАМИ (только горизонтальные) ────────────────────────────
ARR_Y = 7.25   # одна общая высота для обеих стрелок

h_arrow(ax, CX+CW, SX, ARR_Y, "#1D4ED8", lw=4)
arrow_label(ax, (CX+CW + SX)/2, ARR_Y + 0.75,
            "HTTP / REST · JSON · JWT",  "#1D4ED8", "#EFF6FF")

h_arrow(ax, SX+SW, DX, ARR_Y, "#15803D", lw=4)
arrow_label(ax, (SX+SW + DX)/2, ARR_Y + 0.75,
            "SQLAlchemy ORM · SQL", "#15803D", "#F0FDF4")

plt.tight_layout(pad=0.3)
fig.savefig(r"C:\Users\thchkr\Desktop\диплом\diploma_lms\architecture_simple.png",
            dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved architecture_simple.png")
plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# DIAGRAM 2 — MODULE DIAGRAM  (no internal arrows)
# ══════════════════════════════════════════════════════════════════════════════
W2, H2 = 30, 19
fig2, ax2 = plt.subplots(figsize=(W2, H2), dpi=150)
ax2.set_xlim(0, W2); ax2.set_ylim(0, H2); ax2.axis("off")
fig2.patch.set_facecolor("#F1F5F9")

txt(ax2, W2/2, H2-0.55, "Диаграмма модулей — LMS",
    fs=22, bold=True, color="#0F172A")

# ── ФРОНТЕНД ──────────────────────────────────────────────────────────────────
FX, FY, FW, FH = 0.4, 0.4, 8.8, 17.6
rbox(ax2, FX, FY, FW, FH, "#EFF6FF", "#2563EB", lw=3, r=0.6, zorder=1)
txt(ax2, FX+FW/2, FY+FH-0.65, "ФРОНТЕНД", fs=18, bold=True, color="#1E3A8A")
txt(ax2, FX+FW/2, FY+FH-1.25, "lms_frontend/src/", fs=11, color="#1D4ED8")

fe = [
    (0.75, 15.4,  8.1, 1.3,  "#BFDBFE","#3B82F6",
     "main.tsx", "ReactDOM.createRoot()  ·  точка входа"),
    (0.75, 13.8,  8.1, 1.3,  "#BFDBFE","#3B82F6",
     "App.tsx",  "React Router · <Routes> · защита маршрутов"),
    (0.75, 12.2,  8.1, 1.3,  "#A5F3FC","#0891B2",
     "Header.tsx", "Навигация · роль (STUDENT/INSTRUCTOR/ADMIN) · logout"),
    (0.75, 10.6,  8.1, 1.3,  "#FDE68A","#D97706",
     "api.ts", "axios · baseURL '/api' · JWT Bearer interceptor"),

    # pages header
    (0.75,  9.85, 8.1, 0.55, "#DBEAFE","#93C5FD", "── Страницы (Pages) ──", ""),

    # pages grid 2 cols
    (0.75,  8.7,  3.9, 0.9,  "#DBEAFE","#60A5FA",
     "Auth.tsx", "login / register"),
    (4.85,  8.7,  4.0, 0.9,  "#DBEAFE","#60A5FA",
     "Home.tsx", "главная"),
    (0.75,  7.6,  3.9, 0.9,  "#DBEAFE","#60A5FA",
     "Courses.tsx", "GET /courses"),
    (4.85,  7.6,  4.0, 0.9,  "#DBEAFE","#60A5FA",
     "CoursePage.tsx", "GET /courses/:id"),
    (0.75,  6.5,  3.9, 0.9,  "#DBEAFE","#60A5FA",
     "QuizPage.tsx", "start / submit"),
    (4.85,  6.5,  4.0, 0.9,  "#DBEAFE","#60A5FA",
     "MyAttempts.tsx", "GET /attempts/my"),
    (0.75,  5.4,  3.9, 0.9,  "#DBEAFE","#60A5FA",
     "MyCourses.tsx", "GET /users/me/courses"),
    (4.85,  5.4,  4.0, 0.9,  "#DBEAFE","#60A5FA",
     "QuizEditor.tsx", "PUT /quizzes/:id"),
    (0.75,  4.3,  3.9, 0.9,  "#DBEAFE","#60A5FA",
     "AdminCourses.tsx", "CRUD /courses"),
    (4.85,  4.3,  4.0, 0.9,  "#DBEAFE","#60A5FA",
     "AdminDashboard.tsx", "статистика"),
    (0.75,  3.2,  8.1, 0.9,  "#DBEAFE","#60A5FA",
     "AdminQuiz.tsx", "GET · DELETE /quizzes"),

    (0.75,  1.65, 8.1, 1.25, "#E0E7FF","#6366F1",
     "React 18  ·  TypeScript  ·  Vite  ·  Tailwind CSS  ·  React Router  ·  axios", ""),
    (0.75,  0.65, 8.1, 0.75, "#FDE68A","#D97706",
     "localStorage  —  хранение JWT токена", ""),
]
for x, y, w, h, fc, ec, t1, t2 in fe:
    mod(ax2, x, y, w, h, fc, ec, t1, t2, tfs=10.5, sfs=8.5)

# ── БЭКЕНД ────────────────────────────────────────────────────────────────────
BX, BY, BW, BH = 10.4, 0.4, 9.2, 17.6
rbox(ax2, BX, BY, BW, BH, "#F0FDF4", "#16A34A", lw=3, r=0.6, zorder=1)
txt(ax2, BX+BW/2, BY+BH-0.65, "БЭКЕНД", fs=18, bold=True, color="#14532D")
txt(ax2, BX+BW/2, BY+BH-1.25, "backend/app/", fs=11, color="#15803D")

be = [
    (10.75, 15.4,  8.5, 1.3,  "#BBF7D0","#22C55E",
     "main.py", "FastAPI()  ·  CORSMiddleware  ·  include_router(×5)"),
    # config + database side by side
    (10.75, 13.8,  4.1, 1.3,  "#C7D2FE","#6366F1",
     "config.py", "SECRET_KEY · DB_URL · EXPIRE"),
    (15.05, 13.8,  4.1, 1.3,  "#C7D2FE","#6366F1",
     "database.py", "engine · SessionLocal · get_db()"),
    # auth + deps side by side
    (10.75, 12.2,  4.1, 1.3,  "#FBCFE8","#EC4899",
     "auth.py", "hash_password · verify_password\ncreate_access_token (HS256)"),
    (15.05, 12.2,  4.1, 1.3,  "#FBCFE8","#EC4899",
     "deps.py", "get_current_user()\nJWT decode · HTTPBearer"),

    (10.75, 10.6,  8.5, 1.3,  "#E9D5FF","#9333EA",
     "models.py",
     "User · Course · Lesson · Quiz · Question · Attempt  (SQLAlchemy ORM)"),
    (10.75,  9.05, 8.5, 1.3,  "#E9D5FF","#9333EA",
     "schemas.py",
     "Pydantic: UserOut · CourseOut · QuizOut · AttemptOut · Token · MyCourseOut"),

    # routers header
    (10.75,  8.3,  8.5, 0.55, "#A7F3D0","#10B981", "── Роутеры  /api/ ──", ""),

    (10.75,  7.15, 8.5, 0.95, "#A7F3D0","#10B981",
     "routers/auth.py", "POST /auth/register  ·  POST /auth/login"),
    (10.75,  6.0,  8.5, 0.95, "#A7F3D0","#10B981",
     "routers/courses.py", "GET · POST · PUT · DELETE  /courses"),
    (10.75,  4.85, 8.5, 0.95, "#A7F3D0","#10B981",
     "routers/quizzes.py", "GET · PUT · DELETE /quizzes  ·  POST /quizzes/:id/start"),
    (10.75,  3.7,  8.5, 0.95, "#A7F3D0","#10B981",
     "routers/attempts.py", "POST /submit  ·  GET /my  ·  POST /retry"),
    (10.75,  2.55, 8.5, 0.95, "#A7F3D0","#10B981",
     "routers/users.py", "GET /users/me/courses  →  прогресс по курсам"),

    (10.75,  1.65, 8.5, 0.65, "#FEF3C7","#F59E0B",
     "python-jose  ·  passlib  ·  bcrypt  ·  SQLAlchemy 2.0  ·  FastAPI  ·  Uvicorn", ""),
    (10.75,  0.65, 8.5, 0.75, "#BBF7D0","#22C55E",
     "Uvicorn ASGI-сервер  ·  порт 8000", ""),
]
for x, y, w, h, fc, ec, t1, t2 in be:
    mod(ax2, x, y, w, h, fc, ec, t1, t2, tfs=10.5, sfs=8.5)

# ── БАЗА ДАННЫХ ───────────────────────────────────────────────────────────────
DX2, DY2, DW2, DH2 = 20.8, 0.4, 8.8, 17.6
rbox(ax2, DX2, DY2, DW2, DH2, "#FFF7ED", "#EA580C", lw=3, r=0.6, zorder=1)
txt(ax2, DX2+DW2/2, DY2+DH2-0.65, "БАЗА ДАННЫХ", fs=18, bold=True, color="#7C2D12")
txt(ax2, DX2+DW2/2, DY2+DH2-1.25, "SQLite · lms.db", fs=11, color="#C2410C")

db = [
    (21.15, 15.1,  8.1, 2.0,  "#FED7AA","#FB923C", "users",
     "id (PK)  ·  email (UNIQUE)\npassword_hash  ·  role  ·  created_at"),
    (21.15, 12.8,  8.1, 2.0,  "#FED7AA","#FB923C", "courses",
     "id (PK)  ·  title  ·  description\ninstructor  ·  category  ·  image  ·  updated_at"),
    (21.15, 10.5,  8.1, 2.0,  "#FED7AA","#FB923C", "lessons",
     "id (PK)  ·  course_id (FK)\ntitle  ·  lesson_type  ·  content  ·  order_index"),
    (21.15,  8.2,  8.1, 2.0,  "#FED7AA","#FB923C", "quizzes",
     "id (PK)  ·  lesson_id (FK, UNIQUE)\ncreator_id (FK)  ·  time_limit_sec  ·  passing_score"),
    (21.15,  5.9,  8.1, 2.0,  "#FED7AA","#FB923C", "questions",
     "id (PK)  ·  quiz_id (FK)\ntype  ·  text  ·  options (JSON)  ·  correct_answer (JSON)"),
    (21.15,  3.6,  8.1, 2.0,  "#FECACA","#EF4444", "attempts",
     "id (PK)  ·  user_id (FK)  ·  quiz_id (FK)\nstatus  ·  score  ·  started_at  ·  finished_at"),
    (21.15,  1.65, 8.1, 1.65, "#E0E7FF","#6366F1",
     "Связи (CASCADE DELETE)",
     "courses → lessons → quizzes → questions\nattempts.user_id → users  ·  attempts.quiz_id → quizzes"),
    (21.15,  0.65, 8.1, 0.75, "#FEF3C7","#F59E0B",
     "SQLite 3  ·  файл lms.db", ""),
]
for x, y, w, h, fc, ec, t1, t2 in db:
    mod(ax2, x, y, w, h, fc, ec, t1, t2, tfs=11, sfs=8.8)

# ── СТРЕЛКИ МЕЖДУ БЛОКАМИ ─────────────────────────────────────────────────────
ARR_Y2 = 9.2   # середина по высоте

h_arrow(ax2, FX+FW, BX, ARR_Y2, "#1D4ED8", lw=5)
arrow_label(ax2, (FX+FW + BX)/2, ARR_Y2 + 0.85,
            "HTTP / REST · JSON · JWT", "#1D4ED8", "#EFF6FF")

h_arrow(ax2, BX+BW, DX2, ARR_Y2, "#15803D", lw=5)
arrow_label(ax2, (BX+BW + DX2)/2, ARR_Y2 + 0.85,
            "SQLAlchemy ORM · SQL", "#15803D", "#F0FDF4")

plt.tight_layout(pad=0.3)
fig2.savefig(r"C:\Users\thchkr\Desktop\диплом\diploma_lms\modules_simple.png",
             dpi=150, bbox_inches="tight", facecolor=fig2.get_facecolor())
print("Saved modules_simple.png")
plt.close()
