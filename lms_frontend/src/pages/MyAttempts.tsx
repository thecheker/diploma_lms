import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getMyAttempts, retryQuiz } from "../api";

const statusLabel = (s: string) => ({ AUTO_GRADED: "Пройден", COMPLETED: "Не пройден", IN_PROGRESS: "В процессе" }[s] || s);
const statusClass = (s: string) => ({ AUTO_GRADED: "badge-green", COMPLETED: "badge-red", IN_PROGRESS: "badge-gray" }[s] || "badge-gray");

export default function MyAttempts() {
  const [attempts, setAttempts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const load = () => {
    getMyAttempts()
      .then(res => setAttempts(Array.isArray(res.data) ? res.data : []))
      .catch(() => setAttempts([]))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const handleRetry = async (quizId: string) => {
    try { await retryQuiz(quizId); load(); }
    catch (err: any) { alert(err.response?.data?.detail || err.message); }
  };

  return (
    <div className="page">
      <div className="mb-6">
        <h1 className="page-title">Мои попытки</h1>
        <p className="text-gray-500 text-sm mt-1">История прохождения тестов</p>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3].map(i => <div key={i} className="card h-20 animate-pulse" />)}
        </div>
      ) : attempts.length === 0 ? (
        <div className="card p-16 text-center">
          <p className="text-gray-400 font-medium">Вы ещё не проходили тесты</p>
          <Link to="/courses" className="btn-primary mt-4 inline-flex">Перейти к курсам</Link>
        </div>
      ) : (
        <div className="card divide-y divide-gray-50">
          {attempts.map(a => (
            <div key={a.id} className="flex items-center justify-between gap-4 px-5 py-4 hover:bg-gray-50/50 transition-colors">
              <div className="min-w-0">
                <p className="font-semibold text-sm text-gray-900 truncate">{a.quiz_title || a.quiz_id}</p>
                <p className="text-xs text-gray-400 mt-0.5 truncate">{a.course_title} · {new Date(a.started_at).toLocaleDateString("ru")}</p>
              </div>
              <div className="flex items-center gap-4 shrink-0">
                {a.score !== null && (
                  <span className={`text-sm font-bold ${a.status === "AUTO_GRADED" ? "text-emerald-600" : "text-red-500"}`}>
                    {(a.score * 100).toFixed(0)}%
                  </span>
                )}
                <span className={statusClass(a.status)}>{statusLabel(a.status)}</span>
                <div className="flex gap-2">
                  <button onClick={() => handleRetry(a.quiz_id)} className="btn-outline text-xs py-1.5 px-3">Перепройти</button>
                  <Link to={`/quiz/${a.quiz_id}/start`} state={{ fromAttempts: true }} className="btn-ghost text-xs py-1.5 px-3">Просмотр</Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
