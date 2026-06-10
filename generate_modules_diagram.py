"""Module dependency diagram for LMS — high resolution."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

# ── canvas ───────────────────────────────────────────────────────────────────
W, H = 34, 24
fig, ax = plt.subplots(figsize=(W, H), dpi=150)
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")
fig.patch.set_facecolor("#F8FAFC")

# ── palette ───────────────────────────────────────────────────────────────────
C = dict(
    # frontend
    fe_bg="#EFF6FF", fe_hdr="#1D4ED8", fe_entry="#BFDBFE",
    fe_page="#DBEAFE", fe_comp="#A5F3FC", fe_api="#FDE68A",
    # backend
    be_bg="#F0FDF4", be_hdr="#15803D", be_main="#BBF7D0",
    be_router="#A7F3D0", be_core="#6EE7B7",
    be_orm="#D1FAE5",  be_db_layer="#86EFAC",
    # db
    db_bg="#FFF7ED", db_hdr="#C2410C", db_tbl="#FED7AA",
    # arrows
    arr_import="#64748B", arr_http="#1D4ED8", arr_orm="#15803D",
    arr_cfg="#9333EA",
    # section borders
    brd_fe="#3B82F6", brd_be="#16A34A", brd_db="#EA580C",
)

# ── helpers ───────────────────────────────────────────────────────────────────

def rbox(x, y, w, h, fc, ec="#94A3B8", lw=1.4, r=0.25, alpha=1.0, zorder=2):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={r}",
                       facecolor=fc, edgecolor=ec, linewidth=lw,
                       alpha=alpha, zorder=zorder)
    ax.add_patch(p)

def txt(x, y, s, fs=9, bold=False, color="#1E293B", ha="center", va="center",
        zorder=3, wrap=False, ls=1.35):
    kw = dict(fontweight="bold" if bold else "normal", zorder=zorder,
              linespacing=ls, wrap=wrap)
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color, **kw)

def section(x, y, w, h, fc, ec, lw=2.5):
    rbox(x, y, w, h, fc, ec, lw=lw, r=0.5, zorder=1)

def hdr(x, y, w, h, bg, title, fs=11):
    rbox(x, y, w, h, bg, bg, lw=0, r=0.4, zorder=2)
    txt(x+w/2, y+h/2, title, fs=fs, bold=True, color="white", zorder=3)

def mod(x, y, w, h, fc, label, sublabel="", fs=8.8, ec="#94A3B8", lw=1.2):
    rbox(x, y, w, h, fc, ec, lw=lw, r=0.2, zorder=3)
    if sublabel:
        txt(x+w/2, y+h*0.62, label,  fs=fs,   bold=True,  color="#1E293B", zorder=4)
        txt(x+w/2, y+h*0.28, sublabel, fs=fs-1.5, color="#475569", zorder=4)
    else:
        txt(x+w/2, y+h/2, label, fs=fs, bold=True, color="#1E293B", zorder=4)

def arr(x1, y1, x2, y2, color="#64748B", lw=1.8, style="-|>", dash=False):
    ls = (0, (5, 3)) if dash else "solid"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                mutation_scale=14,
                                connectionstyle="arc3,rad=0.0",
                                linestyle=ls),
                zorder=5)

def arr_label(x, y, s, color="#334155", fs=7.5):
    ax.text(x, y, s, ha="center", va="center", fontsize=fs, color=color,
            fontweight="bold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.2", fc="#F8FAFC", ec="none", alpha=0.85))

# ═══════════════════════════════════════════════════════════════════════════
# TITLE
# ═══════════════════════════════════════════════════════════════════════════
txt(W/2, H-0.55, "Диаграмма модулей — LMS (diploma_lms)",
    fs=17, bold=True, color="#0F172A")
txt(W/2, H-1.15,
    "Зависимости между модулями фронтенда (React/TS), бэкенда (FastAPI/Python) и базы данных (SQLite)",
    fs=10, color="#475569")

# ═══════════════════════════════════════════════════════════════════════════
# SECTION A — FRONTEND  x: 0.4 … 11.2
# ═══════════════════════════════════════════════════════════════════════════
FX, FY, FW, FH = 0.4, 1.0, 10.8, 21.5
section(FX, FY, FW, FH, C["fe_bg"], C["brd_fe"])
hdr(FX, FY+FH-1.05, FW, 1.05, C["fe_hdr"],
    "ФРОНТЕНД  ·  lms_frontend/src/", fs=11)
txt(FX+FW/2, FY+FH-1.5,
    "React 18 · TypeScript · Vite · Tailwind CSS · React Router · axios",
    fs=8.5, color="#1E40AF")

# ── A1: Entry point ──────────────────────────────────────────────────────────
rbox(FX+0.3, FY+FH-3.3, FW-0.6, 1.55, "#BFDBFE", C["brd_fe"], lw=1.5, r=0.3, zorder=2)
txt(FX+FW/2, FY+FH-2.45, "Точка входа", fs=8.5, bold=True, color="#1E40AF")

mod(FX+0.55, FY+FH-3.15, 2.0, 0.9, C["fe_entry"],
    "main.tsx", "ReactDOM.createRoot()")
mod(FX+2.75, FY+FH-3.15, 2.5, 0.9, C["fe_entry"],
    "App.tsx", "React Router\n<Routes> / <Route>")
mod(FX+5.45, FY+FH-3.15, 2.3, 0.9, C["fe_entry"],
    "api.ts", "axios instance\nJWT interceptors")
mod(FX+7.95, FY+FH-3.15, 2.5, 0.9, C["fe_entry"],
    "localStorage", "token сессии")

# ── A2: Pages ────────────────────────────────────────────────────────────────
rbox(FX+0.3, FY+FH-13.05, FW-0.6, 9.55, "#DBEAFE", C["brd_fe"], lw=1.5, r=0.3, zorder=2)
txt(FX+FW/2, FY+FH-3.72, "Страницы (Pages)", fs=9, bold=True, color="#1E40AF")

pages = [
    ("Auth.tsx",           "POST /auth/login\nPOST /auth/register"),
    ("Home.tsx",           "Главная, приветствие"),
    ("Courses.tsx",        "GET /courses\nФильтр по категории"),
    ("CoursePage.tsx",     "GET /courses/:id\nСписок уроков"),
    ("QuizPage.tsx",       "POST /quizzes/:id/start\nPOST /attempts/:id/submit"),
    ("MyAttempts.tsx",     "GET /attempts/my\nПопытки студента"),
    ("MyCourses.tsx",      "GET /users/me/courses\nПрогресс по курсам"),
    ("QuizEditor.tsx",     "PUT /quizzes/:id\nРедактор вопросов"),
    ("AdminCourses.tsx",   "POST/PUT/DELETE /courses\nУправление курсами"),
    ("AdminDashboard.tsx", "GET /courses\nСтатистика (Admin)"),
    ("AdminQuiz.tsx",      "GET/DELETE /quizzes\nУправление тестами"),
]
PW, PH = (FW-0.8) / 2 - 0.1, 0.78
PX0, PY0 = FX+0.4, FY+FH-12.9
for i, (name, desc) in enumerate(pages):
    col = i % 2
    row = i // 2
    mod(PX0 + col*(PW+0.1), PY0 + row*(PH+0.1),
        PW, PH, C["fe_page"], name, desc, fs=8)

# ── A3: Component ────────────────────────────────────────────────────────────
rbox(FX+0.3, FY+FH-14.55, FW-0.6, 1.25, "#CFFAFE", C["brd_fe"], lw=1.2, r=0.25, zorder=2)
txt(FX+FW/2, FY+FH-13.23, "Компоненты (Components)", fs=8.5, bold=True, color="#0E7490")
mod(FX+0.5, FY+FH-14.42, FW-1.0, 0.72, C["fe_comp"],
    "Header.tsx",
    "Навигация · роль пользователя (STUDENT/INSTRUCTOR/ADMIN) · logout()")

# ── A4: API-слой ─────────────────────────────────────────────────────────────
rbox(FX+0.3, FY+1.1, FW-0.6, 5.75, "#FEF3C7", "#FCD34D", lw=1.5, r=0.3, zorder=2)
txt(FX+FW/2, FY+6.6, "API-слой  (api.ts)", fs=9, bold=True, color="#92400E")

api_mods = [
    ("login()\nregister()\nlogout()",             "#FDE68A"),
    ("getCourses()\ngetCourse(id)\ncreateCourse()", "#FDE68A"),
    ("updateCourse()\ndeleteCourse()",             "#FDE68A"),
    ("getQuiz()\nstartQuiz()\nupdateQuiz()\ndeleteQuiz()", "#FDE68A"),
    ("submitAttempt()\ngetMyAttempts()\nretryQuiz()", "#FDE68A"),
    ("getMyCourses()",                             "#FDE68A"),
    ("Bearer Token\nAuthorization header",          "#FCA5A5"),
    ("axios.create()\nbaseURL: '/api'\nInterceptors", "#FDBA74"),
]
AW, AH = (FW-0.8)/4 - 0.08, 1.05
AX0, AY0 = FX+0.4, FY+1.25
for i, (label, bg) in enumerate(api_mods):
    col = i % 4; row = i // 4
    mod(AX0+col*(AW+0.1), AY0+row*(AH+0.12), AW, AH, bg, label, fs=7.5)

# ═══════════════════════════════════════════════════════════════════════════
# SECTION B — BACKEND  x: 11.8 … 24.2
# ═══════════════════════════════════════════════════════════════════════════
BX, BY, BW, BH = 11.8, 1.0, 12.4, 21.5
section(BX, BY, BW, BH, C["be_bg"], C["brd_be"])
hdr(BX, BY+BH-1.05, BW, 1.05, C["be_hdr"],
    "БЭКЕНД  ·  backend/app/", fs=11)
txt(BX+BW/2, BY+BH-1.5,
    "Python 3.11 · FastAPI · Uvicorn · SQLAlchemy 2.0 · python-jose · passlib · bcrypt",
    fs=8.5, color="#166534")

# ── B1: main.py ──────────────────────────────────────────────────────────────
rbox(BX+0.3, BY+BH-3.5, BW-0.6, 1.75, C["be_main"], C["brd_be"], lw=1.5, r=0.3, zorder=2)
txt(BX+BW/2, BY+BH-2.0, "Точка входа бэкенда", fs=8.5, bold=True, color="#14532D")
mod(BX+0.5, BY+BH-3.38, BW-1.0, 0.85, C["be_main"],
    "main.py",
    "FastAPI app · CORSMiddleware(allow_origins=['*']) · include_router(×5) · /api/health")

# ── B2: config & database ────────────────────────────────────────────────────
rbox(BX+0.3, BY+BH-5.55, BW-0.6, 1.8, "#E0E7FF", "#6366F1", lw=1.5, r=0.3, zorder=2)
txt(BX+BW/2, BY+BH-3.72, "Конфигурация и слой БД", fs=8.5, bold=True, color="#3730A3")
CW2 = (BW-0.85)/2
mod(BX+0.5,       BY+BH-5.43, CW2, 0.95, "#C7D2FE",
    "config.py",
    "SECRET_KEY · ALGORITHM · TOKEN_EXPIRE\nDATABASE_URL: sqlite:///./lms.db")
mod(BX+0.6+CW2,   BY+BH-5.43, CW2, 0.95, "#C7D2FE",
    "database.py",
    "create_engine() · SessionLocal\nget_db() — dependency injection")

# ── B3: auth & deps ──────────────────────────────────────────────────────────
rbox(BX+0.3, BY+BH-7.65, BW-0.6, 1.85, "#FCE7F3", "#EC4899", lw=1.5, r=0.3, zorder=2)
txt(BX+BW/2, BY+BH-5.73, "Безопасность / Auth", fs=8.5, bold=True, color="#9D174D")
mod(BX+0.5,      BY+BH-7.53, CW2, 1.05, "#FBCFE8",
    "auth.py",
    "hash_password() · verify_password()\ncreate_access_token() — HS256 JWT")
mod(BX+0.6+CW2,  BY+BH-7.53, CW2, 1.05, "#FBCFE8",
    "deps.py",
    "get_current_user()\nJWT decode → User lookup\nHTTPBearer security")

# ── B4: schemas & models ─────────────────────────────────────────────────────
rbox(BX+0.3, BY+BH-9.85, BW-0.6, 1.95, "#F3E8FF", "#9333EA", lw=1.5, r=0.3, zorder=2)
txt(BX+BW/2, BY+BH-7.83, "Модели и схемы данных", fs=8.5, bold=True, color="#6B21A8")
mod(BX+0.5,      BY+BH-9.73, CW2, 1.1, "#E9D5FF",
    "models.py",
    "User · Course · Lesson\nQuiz · Question · Attempt\nSQLAlchemy Base ORM")
mod(BX+0.6+CW2,  BY+BH-9.73, CW2, 1.1, "#E9D5FF",
    "schemas.py",
    "Pydantic v2 schemas:\nUserOut · CourseOut · QuizOut\nAttemptOut · MyCourseOut · Token")

# ── B5: Routers ──────────────────────────────────────────────────────────────
rbox(BX+0.3, BY+1.1, BW-0.6, BY+BH-11.3, C["be_router"], C["brd_be"], lw=1.5, r=0.3, zorder=2)
txt(BX+BW/2, BY+BH-10.04, "Роутеры  (routers/)", fs=9, bold=True, color="#065F46")

routers = [
    ("routers/auth.py",
     "/api/auth/register  [POST] → Создать User, bcrypt пароль\n"
     "/api/auth/login      [POST] → Проверить пароль, вернуть JWT"),
    ("routers/courses.py",
     "/api/courses         [GET]    → Список курсов (фильтр category)\n"
     "/api/courses/:id     [GET]    → Курс + уроки + квизы (joinedload)\n"
     "/api/courses         [POST]   → Создать курс + уроки + Quiz/Questions\n"
     "/api/courses/:id     [PUT]    → Обновить курс (только owner/admin)\n"
     "/api/courses/:id     [DELETE] → Каскадное удаление"),
    ("routers/quizzes.py",
     "/api/quizzes/:id     [GET]    → Тест + вопросы\n"
     "/api/quizzes/:id     [PUT]    → Заменить вопросы (owner/admin)\n"
     "/api/quizzes/:id     [DELETE] → Удалить тест\n"
     "/api/quizzes/:id/start [POST] → Создать Attempt (IN_PROGRESS)"),
    ("routers/attempts.py",
     "/api/attempts/:id/submit [POST] → Подсчёт score, статус AUTO_GRADED/COMPLETED\n"
     "/api/attempts/my         [GET]  → Попытки текущего пользователя\n"
     "/api/attempts/quiz/:id/retry [POST] → Новый Attempt"),
    ("routers/users.py",
     "/api/users/me/courses [GET] → Курсы с прогрессом (completed_lessons/total)"),
]
RH_vals = [1.3, 2.1, 2.1, 2.1, 1.05]
RW = BW - 1.0
ry = BY + 1.25
for (rname, rdesc), rh in zip(routers, RH_vals):
    rbox(BX+0.5, ry, RW, rh, "#ECFDF5", "#6EE7B7", lw=1, r=0.2, zorder=3)
    txt(BX+0.5+RW*0.13, ry+rh/2, rname, fs=8.5, bold=True, color="#065F46",
        ha="center", va="center")
    # vertical separator
    ax.plot([BX+0.5+RW*0.27, BX+0.5+RW*0.27], [ry+0.1, ry+rh-0.1],
            color="#86EFAC", lw=1, zorder=4)
    txt(BX+0.5+RW*0.27+RW*0.37, ry+rh/2, rdesc, fs=7.2, color="#14532D",
        ha="center", va="center", ls=1.55)
    ry += rh + 0.12

# ═══════════════════════════════════════════════════════════════════════════
# SECTION C — DATABASE  x: 24.6 … 33.6
# ═══════════════════════════════════════════════════════════════════════════
DX, DY, DW, DH = 24.6, 1.0, 9.0, 21.5
section(DX, DY, DW, DH, C["db_bg"], C["brd_db"])
hdr(DX, DY+DH-1.05, DW, 1.05, C["db_hdr"],
    "БД  ·  backend/lms.db", fs=11)
txt(DX+DW/2, DY+DH-1.5, "SQLite 3  ·  файл lms.db",
    fs=8.5, color="#9A3412")

tables_info = [
    ("users",
     "PK  id: NVARCHAR(36)\n"
     "    email: NVARCHAR UNIQUE\n"
     "    password_hash: NVARCHAR\n"
     "    role: ENUM(STUDENT|INSTRUCTOR|ADMIN)\n"
     "    created_at: DATETIME",
     "#FED7AA"),
    ("courses",
     "PK  id: NVARCHAR(36)\n"
     "    title: NVARCHAR  [indexed]\n"
     "    description, instructor, image\n"
     "    category: ENUM(PROGRAMMING…OTHER)\n"
     "    created_at, updated_at: DATETIME",
     "#FED7AA"),
    ("lessons",
     "PK  id: NVARCHAR(36)\n"
     "FK  course_id → courses.id  [CASCADE]\n"
     "    title: NVARCHAR\n"
     "    lesson_type: ENUM(TEXT|VIDEO)\n"
     "    content: JSON,  order_index: INT",
     "#FED7AA"),
    ("quizzes",
     "PK  id: NVARCHAR(36)\n"
     "FK  lesson_id → lessons.id  [CASCADE, UNIQUE]\n"
     "FK  creator_id → users.id   [SET NULL]\n"
     "    title, time_limit_sec: INT(600)\n"
     "    passing_score: FLOAT(0.7)",
     "#FED7AA"),
    ("questions",
     "PK  id: NVARCHAR(36)\n"
     "FK  quiz_id → quizzes.id  [CASCADE]\n"
     "    type: ENUM(SINGLE|MULTIPLE|TRUE_FALSE)\n"
     "    text: NVARCHAR\n"
     "    options: JSON [],  correct_answer: JSON {}",
     "#FED7AA"),
    ("attempts",
     "PK  id: NVARCHAR(36)\n"
     "FK  user_id → users.id\n"
     "FK  quiz_id → quizzes.id\n"
     "    status: ENUM(IN_PROGRESS|COMPLETED|AUTO_GRADED)\n"
     "    score: FLOAT,  started_at, finished_at: DATETIME",
     "#FECACA"),
]
TW = DW - 0.6
ty = DY + 0.8
for tname, tcols, tbg in reversed(tables_info):
    TH = 1.8
    rbox(DX+0.3, ty, TW, TH, tbg, "#FB923C", lw=1.1, r=0.2, zorder=3)
    txt(DX+0.3+TW/2, ty+TH-0.28, tname,
        fs=9.5, bold=True, color="#7C2D12", zorder=4)
    ax.plot([DX+0.4, DX+0.3+TW-0.1], [ty+TH-0.45, ty+TH-0.45],
            color="#FB923C", lw=1, zorder=4)
    txt(DX+0.3+TW/2, ty+TH-0.45-0.6, tcols,
        fs=7.0, color="#431407", zorder=4, ls=1.6)
    ty += TH + 0.15

# ═══════════════════════════════════════════════════════════════════════════
# DEPENDENCY ARROWS — Frontend internal
# ═══════════════════════════════════════════════════════════════════════════
# main.tsx → App.tsx
arr(FX+2.55, FY+FH-2.7, FX+2.75, FY+FH-2.7, C["arr_import"])
# App.tsx → Pages (one representative)
arr(FX+3.5,  FY+FH-3.15, FX+3.5,  FY+FH-4.0, C["arr_import"])
# Pages → api.ts
arr(FX+5.45, FY+FH-2.7, FX+5.45, FY+FH-3.15, C["arr_import"], dash=True)
# api.ts → localStorage
arr(FX+7.95, FY+FH-2.7, FX+8.1, FY+FH-2.7, C["arr_import"], dash=True)
# App.tsx → Header
arr(FX+3.5, FY+FH-3.15, FX+3.5, FY+FH-13.35, C["arr_import"], lw=1.4, dash=True)
# api.ts → API layer box (downward)
arr(FX+6.5, FY+FH-3.15, FX+6.5, FY+6.87, C["arr_import"])

arr_label(FX+2.63, FY+FH-2.45, "import", C["arr_import"])
arr_label(FX+3.85, FY+FH-3.58, "renders\npages", C["arr_import"])

# ═══════════════════════════════════════════════════════════════════════════
# DEPENDENCY ARROWS — Backend internal
# ═══════════════════════════════════════════════════════════════════════════
# main.py → each router
arr(BX+BW/2, BY+BH-3.5, BX+BW/2, BY+BH-3.72, C["arr_import"])
# config.py → auth.py
arr(BX+0.5+CW2*0.5, BY+BH-5.55,
    BX+0.5+CW2*0.5, BY+BH-5.73, C["arr_cfg"], lw=1.4, dash=True)
# database.py → routers (get_db)
arr(BX+0.6+CW2+CW2*0.5, BY+BH-5.55,
    BX+0.6+CW2+CW2*0.5, BY+BH-5.73, C["arr_cfg"], lw=1.4, dash=True)
# auth.py → deps.py (uses same config)
arr(BX+0.5+CW2, BY+BH-6.5,
    BX+0.6+CW2,  BY+BH-6.5, "#EC4899", lw=1.3, dash=True)
# deps.py → models.py
arr(BX+0.6+CW2+CW2*0.5, BY+BH-7.65,
    BX+0.6+CW2+CW2*0.5, BY+BH-7.83, "#9333EA", lw=1.4)
# schemas → routers
arr(BX+0.5+CW2, BY+BH-9.85,
    BX+0.5+CW2,  BY+BH-10.04, "#9333EA", lw=1.4)
# models → routers
arr(BX+0.5+CW2*0.5, BY+BH-9.85,
    BX+0.5+CW2*0.5,  BY+BH-10.04, "#9333EA", lw=1.4)

arr_label(BX+BW*0.38, BY+BH-3.62, "include_router()", "#065F46")

# ═══════════════════════════════════════════════════════════════════════════
# MAIN ARROWS — Frontend ↔ Backend
# ═══════════════════════════════════════════════════════════════════════════
# HTTP arrow (bi-directional) at mid height
MID_Y = (FY + FY+FH) / 2
ax.annotate("", xy=(BX, MID_Y), xytext=(FX+FW, MID_Y),
            arrowprops=dict(arrowstyle="<|-|>", color=C["arr_http"],
                            lw=3, mutation_scale=18), zorder=7)
ax.text((FX+FW+BX)/2, MID_Y+0.45,
        "HTTP / REST  ·  JSON  ·  JWT Bearer Token",
        ha="center", va="bottom", fontsize=9.5, fontweight="bold",
        color=C["arr_http"],
        bbox=dict(boxstyle="round,pad=0.3", fc="#EFF6FF", ec=C["arr_http"], lw=1.5),
        zorder=8)

# ═══════════════════════════════════════════════════════════════════════════
# MAIN ARROWS — Backend ↔ Database
# ═══════════════════════════════════════════════════════════════════════════
ax.annotate("", xy=(DX, MID_Y), xytext=(BX+BW, MID_Y),
            arrowprops=dict(arrowstyle="<|-|>", color=C["arr_orm"],
                            lw=3, mutation_scale=18), zorder=7)
ax.text((BX+BW+DX)/2, MID_Y+0.45,
        "SQLAlchemy ORM  ·  SQL queries",
        ha="center", va="bottom", fontsize=9.5, fontweight="bold",
        color=C["arr_orm"],
        bbox=dict(boxstyle="round,pad=0.3", fc="#F0FDF4", ec=C["arr_orm"], lw=1.5),
        zorder=8)

# ═══════════════════════════════════════════════════════════════════════════
# FK relation arrows in DB section
# ═══════════════════════════════════════════════════════════════════════════
# positions of table tops (bottom-to-top order: users, courses, lessons, quizzes, questions, attempts)
table_tops = []
_ty = DY + 0.8
for _ in tables_info:
    table_tops.append(_ty + 1.8)
    _ty += 1.8 + 0.15

# Draw FK lines on the right side of DB section
fk_x = DX + DW - 0.15
# attempts → users  (top table → bottom users)
fk_pairs = [
    (5, 0, "FK: user_id"),   # attempts → users
    (5, 3, "FK: quiz_id"),   # attempts → quizzes
    (4, 3, "FK: quiz_id"),   # questions → quizzes
    (3, 2, "FK: lesson_id"), # quizzes → lessons
    (2, 1, "FK: course_id"), # lessons → courses
]
colors_fk = ["#DC2626","#DC2626","#D97706","#7C3AED","#0891B2"]
for (ti, tj, label), clr in zip(fk_pairs, colors_fk):
    y_from = (table_tops[ti] + (table_tops[ti]-1.8))/2  # center of from-table
    y_to   = (table_tops[tj] + (table_tops[tj]-1.8))/2  # center of to-table
    # draw a small bracket on the right
    xi = DX + DW - 0.05
    ax.plot([xi, xi+0.07, xi+0.07, xi],
            [y_from, y_from, y_to, y_to],
            color=clr, lw=1.2, zorder=5, clip_on=False)
    ax.annotate("", xy=(xi, y_to), xytext=(xi+0.07, y_to),
                arrowprops=dict(arrowstyle="-|>", color=clr, lw=1.2,
                                mutation_scale=9), zorder=5, clip_on=False)

# ═══════════════════════════════════════════════════════════════════════════
# LEGEND
# ═══════════════════════════════════════════════════════════════════════════
legend_handles = [
    mpatches.Patch(fc=C["fe_bg"],     ec=C["brd_fe"], lw=2,  label="Фронтенд (React/TS)"),
    mpatches.Patch(fc=C["be_bg"],     ec=C["brd_be"], lw=2,  label="Бэкенд (FastAPI)"),
    mpatches.Patch(fc=C["db_bg"],     ec=C["brd_db"], lw=2,  label="База данных (SQLite)"),
    mpatches.Patch(fc=C["fe_entry"],  ec="#93C5FD",          label="Точка входа / конфиг"),
    mpatches.Patch(fc=C["fe_page"],   ec="#93C5FD",          label="Страница (Page)"),
    mpatches.Patch(fc=C["fe_comp"],   ec="#67E8F9",          label="Компонент / Header"),
    mpatches.Patch(fc=C["fe_api"],    ec="#FCD34D",          label="API-функция (axios)"),
    mpatches.Patch(fc=C["be_router"], ec="#86EFAC",          label="Router / endpoint"),
    mpatches.Patch(fc=C["db_tbl"],    ec="#FB923C",          label="Таблица БД"),
    mpatches.Patch(fc="#FECACA",      ec="#FB923C",          label="Таблица с FK"),
    mpatches.Patch(fc="none", ec=C["arr_http"], lw=2,        label="HTTP REST (axios ↔ FastAPI)"),
    mpatches.Patch(fc="none", ec=C["arr_orm"],  lw=2,        label="ORM (SQLAlchemy ↔ SQLite)"),
    mpatches.Patch(fc="none", ec=C["arr_import"], lw=1.5,    label="import / зависимость"),
    mpatches.Patch(fc="none", ec="#9333EA", lw=1.5,          label="Pydantic / models import"),
]
ax.legend(handles=legend_handles,
          loc="lower center",
          bbox_to_anchor=(0.5, -0.005),
          ncol=7,
          frameon=True, framealpha=0.97,
          fontsize=8.5, edgecolor="#94A3B8",
          columnspacing=1.0, handlelength=1.5)

# ── save ─────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0.4)
OUT = r"C:\Users\thchkr\Desktop\диплом\diploma_lms\modules_diagram.png"
plt.savefig(OUT, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Saved: {OUT}")
