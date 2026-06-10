import { useEffect, useState } from "react";
import { useParams, Link, useNavigate, useLocation } from "react-router-dom";
import { getCourse, deleteCourse } from "../api";

const getUser = () => {
  const token = localStorage.getItem("token");
  if (!token) return null;
  try {
    const p = JSON.parse(atob(token.split(".")[1]));
    return { role: (p.role || "STUDENT").toUpperCase(), email: p.sub || "" };
  } catch { return null; }
};

export default function CoursePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();

  const [course, setCourse] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [currentStep, setCurrentStep] = useState(0);
  const [completedLessons, setCompletedLessons] = useState<Set<number>>(new Set());
  const [quizResult, setQuizResult] = useState<any>(null);
  const [courseCompleted, setCourseCompleted] = useState(false);

  const user = getUser();
  const canEdit = user?.role === "ADMIN" || (user?.role === "INSTRUCTOR" && course?.instructor === user?.email);

  useEffect(() => {
    if (!id) { setError("Нет ID курса"); setLoading(false); return; }
    let cancelled = false;
    getCourse(id)
      .then(res => {
        if (cancelled) return;
        setCourse(res.data);
        const saved = localStorage.getItem(`course_progress_${id}`);
        if (saved) {
          const p = JSON.parse(saved);
          setCurrentStep(p.currentStep || 0);
          setCompletedLessons(new Set(p.completed || []));
        }
        if (location.state?.quizResult) {
          setQuizResult(location.state.quizResult);
          window.history.replaceState({}, document.title);
        }
      })
      .catch(err => { if (!cancelled) setError(err.response?.data?.detail || "Не удалось загрузить курс"); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [id, location.state]);

  const saveProgress = (step: number, completed: Set<number>) =>
    localStorage.setItem(`course_progress_${id}`, JSON.stringify({ currentStep: step, completed: Array.from(completed) }));

  const handleNext = () => {
    const newCompleted = new Set(completedLessons);
    newCompleted.add(currentStep);
    setCompletedLessons(newCompleted);
    const next = currentStep + 1;
    if (next < (course?.lessons?.length || 0)) {
      setCurrentStep(next);
      saveProgress(next, newCompleted);
      setQuizResult(null);
    } else {
      setCourseCompleted(true);
      saveProgress(next, newCompleted);
    }
  };

  const handleDelete = async () => {
    if (!confirm("Удалить курс?")) return;
    try { await deleteCourse(id!); navigate("/courses"); }
    catch (err: any) { alert(err.response?.data?.detail || err.message); }
  };

  if (loading) return (
    <div className="page">
      <div className="animate-pulse space-y-4">
        <div className="h-8 bg-gray-100 rounded w-1/2" />
        <div className="h-4 bg-gray-100 rounded w-full" />
        <div className="h-64 bg-gray-100 rounded-2xl" />
      </div>
    </div>
  );

  if (error) return (
    <div className="page text-center">
      <div className="card p-12">
        <p className="text-red-500 mb-4">{error}</p>
        <Link to="/courses" className="btn-outline">← К каталогу</Link>
      </div>
    </div>
  );

  if (courseCompleted) return (
    <div className="page">
      <div className="card p-16 text-center max-w-lg mx-auto">
        <div className="w-16 h-16 bg-emerald-100 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-6">🎉</div>
        <h1 className="text-2xl font-bold mb-2">Курс завершён!</h1>
        <p className="text-gray-500 mb-2">Вы успешно прошли</p>
        <p className="text-primary-600 font-bold text-lg mb-8">{course?.title}</p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Link to="/courses" className="btn-primary">К каталогу</Link>
          <button onClick={() => { setCourseCompleted(false); setCurrentStep(0); setCompletedLessons(new Set()); localStorage.removeItem(`course_progress_${id}`); }} className="btn-outline">Пройти ещё раз</button>
        </div>
      </div>
    </div>
  );

  if (quizResult) {
    const passed = quizResult.status === "AUTO_GRADED";
    return (
      <div className="page">
        <div className={`card p-12 text-center max-w-lg mx-auto border ${passed ? "border-emerald-100" : "border-red-100"}`}>
          <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-2xl mx-auto mb-5 ${passed ? "bg-emerald-100" : "bg-red-50"}`}>
            {passed ? "✓" : "✗"}
          </div>
          <h2 className="text-xl font-bold mb-1">{passed ? "Тест пройден!" : "Попробуйте ещё раз"}</h2>
          <p className="text-gray-500 mb-6">
            Результат: <span className="font-bold text-gray-900">{(quizResult.score * 100).toFixed(0)}%</span>
            {" · "}Проходной: {(course?.lessons?.[currentStep]?.quiz?.passing_score * 100).toFixed(0)}%
          </p>
          <button onClick={() => { setQuizResult(null); handleNext(); }} className="btn-primary px-8">
            {currentStep === (course?.lessons?.length || 0) - 1 ? "Завершить курс" : "Следующий урок →"}
          </button>
        </div>
      </div>
    );
  }

  const lessons = course?.lessons || [];
  if (lessons.length === 0) return <div className="page text-center text-gray-400">В этом курсе пока нет уроков</div>;
  if (currentStep >= lessons.length) { setCurrentStep(0); return null; }

  const lesson = lessons[currentStep];
  const isLast = currentStep === lessons.length - 1;
  const progress = Math.round(((completedLessons.size) / lessons.length) * 100);

  return (
    <div className="page">
      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar — lesson list */}
        <aside className="lg:w-72 shrink-0">
          <div className="card p-4 sticky top-20">
            <h2 className="font-bold text-gray-900 mb-1 text-sm">{course.title}</h2>
            <p className="text-xs text-gray-400 mb-3">{course.instructor}</p>
            {/* Progress */}
            <div className="mb-4">
              <div className="flex justify-between text-xs text-gray-400 mb-1.5">
                <span>Прогресс</span><span>{progress}%</span>
              </div>
              <div className="progress-bar h-1.5">
                <div className="progress-fill h-1.5" style={{ width: `${progress}%` }} />
              </div>
            </div>
            {/* Lessons */}
            <ul className="space-y-1">
              {lessons.map((l: any, i: number) => (
                <li key={l.id}>
                  <button
                    onClick={() => { setCurrentStep(i); setQuizResult(null); }}
                    className={`w-full text-left px-3 py-2.5 rounded-xl text-sm flex items-center gap-3 transition-all ${
                      i === currentStep
                        ? "bg-primary-50 text-primary-700 font-semibold"
                        : "text-gray-600 hover:bg-gray-50"
                    }`}
                  >
                    <span className={`w-5 h-5 rounded-full flex items-center justify-center text-xs shrink-0 ${
                      completedLessons.has(i) ? "bg-emerald-500 text-white" : i === currentStep ? "bg-primary-600 text-white" : "bg-gray-100 text-gray-400"
                    }`}>
                      {completedLessons.has(i) ? "✓" : i + 1}
                    </span>
                    <span className="line-clamp-2 leading-tight">{l.title}</span>
                  </button>
                </li>
              ))}
            </ul>
            {canEdit && (
              <div className="mt-4 pt-4 border-t border-gray-100 space-y-2">
                <button onClick={handleDelete} className="btn-danger w-full text-xs py-2">Удалить курс</button>
              </div>
            )}
          </div>
        </aside>

        {/* Main content */}
        <main className="flex-1 min-w-0">
          <div className="card p-6 mb-4">
            <div className="flex items-start justify-between gap-4 mb-5">
              <div>
                <div className="flex items-center gap-2 text-xs text-gray-400 mb-1">
                  <span>Урок {currentStep + 1} из {lessons.length}</span>
                  {lesson.lesson_type === "VIDEO" && <span className="badge-gray">Видео</span>}
                </div>
                <h1 className="text-xl font-bold text-gray-900">{lesson.title}</h1>
              </div>
            </div>

            {lesson.lesson_type === "VIDEO" ? (
              <div className="bg-gray-50 rounded-xl p-6 flex items-center gap-4">
                <div className="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center text-primary-600">▶</div>
                {lesson.content?.url
                  ? <a href={lesson.content.url} target="_blank" className="text-primary-600 font-medium hover:underline">Открыть видео</a>
                  : <span className="text-gray-400">Видео не добавлено</span>}
              </div>
            ) : (
              <div className="text-gray-700 leading-relaxed whitespace-pre-wrap text-sm">
                {lesson.content?.body || <span className="text-gray-300 italic">Содержимое урока пока не добавлено</span>}
                {lesson.content?.image && <img src={lesson.content.image} alt="" className="mt-4 rounded-xl max-h-80 w-full object-cover" />}
              </div>
            )}
          </div>

          {/* Quiz / Next */}
          <div className="card p-5">
            {lesson.quiz ? (
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center text-primary-600 text-sm font-bold">Q</div>
                  <div>
                    <p className="font-semibold text-sm text-gray-900">{lesson.quiz.title}</p>
                    <p className="text-xs text-gray-400">Тест к уроку · {lesson.quiz.time_limit_sec / 60} мин.</p>
                  </div>
                  {canEdit && (
                    <div className="ml-auto flex gap-3">
                      <Link to={`/admin/quiz/${lesson.quiz.id}/edit`} className="text-xs text-primary-600 hover:underline font-medium">Редактировать</Link>
                      <button onClick={async () => {
                        if (!confirm("Удалить тест?")) return;
                        await fetch(`/api/quizzes/${lesson.quiz.id}`, { method: "DELETE", headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } });
                        window.location.reload();
                      }} className="text-xs text-red-500 hover:underline font-medium">Удалить</button>
                    </div>
                  )}
                </div>
                <div className="flex gap-3">
                  <Link to={`/quiz/${lesson.quiz.id}/start`} state={{ courseId: id }} className="btn-primary flex-1 justify-center py-2.5">
                    Пройти тест
                  </Link>
                  {completedLessons.has(currentStep) && (
                    <button onClick={handleNext} className="btn-outline flex-1 justify-center py-2.5">
                      {isLast ? "Завершить курс" : "Далее →"}
                    </button>
                  )}
                </div>
              </div>
            ) : (
              <button onClick={handleNext} className="btn-primary w-full py-3">
                {isLast ? "Завершить курс" : "Следующий урок →"}
              </button>
            )}
          </div>

          {/* Bottom nav */}
          <div className="flex items-center justify-between mt-4 text-sm">
            {currentStep > 0
              ? <button onClick={() => { setCurrentStep(currentStep - 1); saveProgress(currentStep - 1, completedLessons); setQuizResult(null); }} className="btn-ghost">← Назад</button>
              : <span />}
            <Link to="/courses" className="text-gray-400 hover:text-gray-600 text-xs">← К каталогу</Link>
          </div>
        </main>
      </div>
    </div>
  );
}
