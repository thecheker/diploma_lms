# coding: utf-8
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

W, H = 22, 15
fig, ax = plt.subplots(figsize=(W, H), dpi=150)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
fig.patch.set_facecolor("#F8FAFC")

def rbox(x, y, w, h, fc, ec, lw=2.5, r=0.35, zorder=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=zorder))

def txt(x, y, s, fs=12, bold=False, color="#1E293B",
        ha="center", va="center", zorder=5, ls=1.4):
    ax.text(x, y, s, ha=ha, va=va, fontsize=fs,
            fontweight="bold" if bold else "normal",
            color=color, zorder=zorder, linespacing=ls)

def action(x, y, w, h, fc, ec, text):
    rbox(x, y, w, h, fc, ec, lw=1.6, r=0.2, zorder=4)
    txt(x+w/2, y+h/2, text, fs=10, color="#1E293B", zorder=5)

def arrow_down(x, y1, y2, color="#94A3B8"):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=2.5, mutation_scale=18), zorder=6)

# ── ЗАГОЛОВОК ─────────────────────────────────────────────────────────────────
txt(W/2, H-0.55, "Роли пользователей и их возможности — LMS",
    fs=19, bold=True, color="#0F172A")
txt(W/2, H-1.15, "Три роли · разные права доступа · единая система",
    fs=11, color="#64748B")

# ══════════════════════════════════════════════════════════════════════════════
# КОЛОНКА 1 — STUDENT
# ══════════════════════════════════════════════════════════════════════════════
SX = 0.5
rbox(SX, 0.4, 6.2, 12.8, "#EFF6FF", "#2563EB", lw=3, r=0.5)

# иконка-аватар (круг)
circle = plt.Circle((SX+3.1, 12.45), 0.65, color="#2563EB", zorder=3)
ax.add_patch(circle)
txt(SX+3.1, 12.45, "S", fs=18, bold=True, color="white", zorder=4)

txt(SX+3.1, 11.55, "СТУДЕНТ", fs=16, bold=True, color="#1E3A8A")
txt(SX+3.1, 11.0,  "role = STUDENT", fs=10, color="#3B82F6")

# разделитель
ax.plot([SX+0.3, SX+5.9], [10.65, 10.65], color="#BFDBFE", lw=2)

# действия
actions_student = [
    ("#DBEAFE", "#3B82F6", "Просмотр каталога курсов"),
    ("#DBEAFE", "#3B82F6", "Фильтрация по категории"),
    ("#DBEAFE", "#3B82F6", "Просмотр уроков курса"),
    ("#DBEAFE", "#3B82F6", "Прохождение тестов (Quiz)"),
    ("#DBEAFE", "#3B82F6", "Отправка ответов (submit)"),
    ("#DBEAFE", "#3B82F6", "Просмотр своих попыток"),
    ("#DBEAFE", "#3B82F6", "Просмотр прогресса по курсам"),
    ("#FECACA", "#DC2626", "Создание курсов — ЗАПРЕЩЕНО"),
    ("#FECACA", "#DC2626", "Удаление данных — ЗАПРЕЩЕНО"),
]
ay = 10.3
for fc, ec, text in actions_student:
    action(SX+0.3, ay - 1.0, 5.6, 0.75, fc, ec, text)
    ay -= 0.9

# ══════════════════════════════════════════════════════════════════════════════
# КОЛОНКА 2 — INSTRUCTOR
# ══════════════════════════════════════════════════════════════════════════════
IX = 7.9
rbox(IX, 0.4, 6.2, 12.8, "#F0FDF4", "#16A34A", lw=3, r=0.5)

circle2 = plt.Circle((IX+3.1, 12.45), 0.65, color="#16A34A", zorder=3)
ax.add_patch(circle2)
txt(IX+3.1, 12.45, "I", fs=18, bold=True, color="white", zorder=4)

txt(IX+3.1, 11.55, "ПРЕПОДАВАТЕЛЬ", fs=15, bold=True, color="#14532D")
txt(IX+3.1, 11.0,  "role = INSTRUCTOR", fs=10, color="#16A34A")

ax.plot([IX+0.3, IX+5.9], [10.65, 10.65], color="#BBF7D0", lw=2)

actions_instructor = [
    ("#D1FAE5", "#10B981", "Всё, что может Студент"),
    ("#BBF7D0", "#16A34A", "Создание курсов"),
    ("#BBF7D0", "#16A34A", "Добавление уроков (TEXT/VIDEO)"),
    ("#BBF7D0", "#16A34A", "Создание тестов и вопросов"),
    ("#BBF7D0", "#16A34A", "Редактирование своих курсов"),
    ("#BBF7D0", "#16A34A", "Удаление своих курсов"),
    ("#BBF7D0", "#16A34A", "Редактирование своих тестов"),
    ("#FECACA", "#DC2626", "Чужие курсы — ЗАПРЕЩЕНО"),
    ("#FECACA", "#DC2626", "Управление пользователями — НЕТ"),
]
ay = 10.3
for fc, ec, text in actions_instructor:
    action(IX+0.3, ay - 1.0, 5.6, 0.75, fc, ec, text)
    ay -= 0.9

# ══════════════════════════════════════════════════════════════════════════════
# КОЛОНКА 3 — ADMIN
# ══════════════════════════════════════════════════════════════════════════════
AX = 15.3
rbox(AX, 0.4, 6.2, 12.8, "#FFF7ED", "#EA580C", lw=3, r=0.5)

circle3 = plt.Circle((AX+3.1, 12.45), 0.65, color="#EA580C", zorder=3)
ax.add_patch(circle3)
txt(AX+3.1, 12.45, "A", fs=18, bold=True, color="white", zorder=4)

txt(AX+3.1, 11.55, "АДМИНИСТРАТОР", fs=14, bold=True, color="#7C2D12")
txt(AX+3.1, 11.0,  "role = ADMIN", fs=10, color="#EA580C")

ax.plot([AX+0.3, AX+5.9], [10.65, 10.65], color="#FED7AA", lw=2)

actions_admin = [
    ("#D1FAE5", "#10B981", "Всё, что может Студент"),
    ("#D1FAE5", "#10B981", "Всё, что может Преподаватель"),
    ("#FED7AA", "#EA580C", "Создание ЛЮБЫХ курсов"),
    ("#FED7AA", "#EA580C", "Редактирование ЛЮБЫХ курсов"),
    ("#FED7AA", "#EA580C", "Удаление ЛЮБЫХ курсов"),
    ("#FED7AA", "#EA580C", "Управление ЛЮБЫМИ тестами"),
    ("#FED7AA", "#EA580C", "Просмотр всей статистики"),
    ("#FED7AA", "#EA580C", "Полный доступ к AdminDashboard"),
    ("#FED7AA", "#EA580C", "Полный доступ к AdminQuiz"),
]
ay = 10.3
for fc, ec, text in actions_admin:
    action(AX+0.3, ay - 1.0, 5.6, 0.75, fc, ec, text)
    ay -= 0.9

# ══════════════════════════════════════════════════════════════════════════════
# ОБЩИЕ ЭЛЕМЕНТЫ — авторизация снизу
# ══════════════════════════════════════════════════════════════════════════════
rbox(0.5, 0.42, 21.0, 0.72, "#1E293B", "#0F172A", lw=2, r=0.3, zorder=3)
txt(W/2, 0.78,
    "Авторизация: POST /api/auth/login  →  JWT Bearer Token  →  сохраняется в localStorage  →  отправляется в каждом запросе",
    fs=9.5, color="#F8FAFC", zorder=4)

# ══════════════════════════════════════════════════════════════════════════════
# СТРЕЛКИ-НАСЛЕДОВАНИЕ между ролями
# ══════════════════════════════════════════════════════════════════════════════
# Student → Instructor
ax.annotate("", xy=(IX+0.15, 9.82), xytext=(SX+6.05, 9.82),
            arrowprops=dict(arrowstyle="-|>", color="#16A34A",
                            lw=2.5, mutation_scale=18), zorder=7)
txt((SX+6.05 + IX+0.15)/2, 10.1, "включает", fs=9.5,
    bold=True, color="#16A34A", zorder=8)

# Instructor → Admin
ax.annotate("", xy=(AX+0.15, 9.82), xytext=(IX+6.05, 9.82),
            arrowprops=dict(arrowstyle="-|>", color="#EA580C",
                            lw=2.5, mutation_scale=18), zorder=7)
txt((IX+6.05 + AX+0.15)/2, 10.1, "включает", fs=9.5,
    bold=True, color="#EA580C", zorder=8)

plt.tight_layout(pad=0.2)
fig.savefig(r"C:\Users\thchkr\Desktop\диплом\diploma_lms\roles_diagram.png",
            dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print("Saved roles_diagram.png")
