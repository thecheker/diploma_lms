import { useEffect, useState, useRef } from "react";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { startQuiz, submitAttempt } from "../api";

export default function QuizPage({ startMode = false }: { startMode?: boolean }) {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const courseId = location.state?.courseId;
  const fromAttempts = location.state?.fromAttempts;

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [quiz, setQuiz] = useState<any>(null);
  const [attemptId, setAttemptId] = useState("");
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [timeLeft, setTimeLeft] = useState<number | null>(null);
  const [result, setResult] = useState<any>(null);

  const submittingRef = useRef(false);
  const attemptIdRef = useRef("");
  const answersRef = useRef<Record<string, any>>({});

  useEffect(() => { submittingRef.current = submitting; }, [submitting]);
  useEffect(() => { attemptIdRef.current = attemptId; }, [attemptId]);
  useEffect(() => { answersRef.current = answers; }, [answers]);

  useEffect(() => {
    if (startMode && quizId) startQuizAttempt();
  }, [quizId, startMode]);

  useEffect(() => {
    if (timeLeft === null || timeLeft <= 0) return;
    const t = setInterval(() => {
      setTimeLeft(prev => {
        if (prev === null || prev <= 1) {
          clearInterval(t);
          if (attemptIdRef.current && !submittingRef.current) handleSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(t);
  }, [timeLeft]);

  const startQuizAttempt = async () => {
    try {
      const res = await startQuiz(quizId!);
      setQuiz(res.data);
      setAttemptId(res.data.attempt_id);
      setTimeLeft(res.data.time_limit_sec);
      const init: Record<string, any> = {};
      res.data.questions.forEach((q: any) => { init[q.id] = { selected_ids: [] }; });
      setAnswers(init);
    } catch (err: any) {
      alert(err.response?.data?.detail || "Не удалось начать тест");
      navigate(-1);
    } finally { setLoading(false); }
  };

  const handleSelect = (qId: string, optId: string, type: string) => {
    setAnswers(prev => {
      const current = prev[qId]?.selected_ids || [];
      const newSelected = (type === "SINGLE_CHOICE" || type === "TRUE_FALSE")
        ? [optId]
        : current.includes(optId) ? current.filter((id: string) => id !== optId) : [...current, optId];
      return { ...prev, [qId]: { selected_ids: newSelected } };
    });
  };

  const handleSubmit = async () => {
    if (!attemptIdRef.current || submittingRef.current) return;
    setSubmitting(true);
    try {
      const formatted = Object.entries(answersRef.current).map(([qId, ans]: [string, any]) => ({
        question_id: qId,
        user_answer: ans || { selected_ids: [] },
      }));
      const res = await submitAttempt(attemptIdRef.current, formatted);
      setResult(res.data);
    } catch (err: any) {
      alert(err.response?.data?.detail || "Ошибка отправки");
    } finally { setSubmitting(false); }
  };

  const fmt = (s: number) => `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, "0")}`;

  if (result) {
    const passed = result.status === "AUTO_GRADED";
    return (
      <div className="page flex items-start justify-center pt-8">
        <div className={`card p-12 text-center w-full max-w-md border ${passed ? "border-emerald-100" : "border-red-100"}`}>
          <div className={`w-16 h-16 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-6 font-bold ${passed ? "bg-emerald-100 text-emerald-600" : "bg-red-50 text-red-500"}`}>
            {passed ? "✓" : "✗"}
          </div>
          <h2 className="text-2xl font-bold mb-2">{passed ? "Тест пройден!" : "Попробуйте ещё раз"}</h2>
          <p className="text-gray-500 mb-1">
            Результат: <span className="font-bold text-gray-900">{(result.score * 100).toFixed(0)}%</span>
          </p>
          <p className="text-gray-400 text-sm mb-8">Проходной: {(quiz?.passing_score * 100).toFixed(0)}%</p>
          <button onClick={() => {
            if (fromAttempts) navigate("/my-attempts");
            else if (courseId) navigate(`/course/${courseId}`, { state: { quizResult: result, quizId } });
            else navigate("/courses");
          }} className="btn-primary px-8 py-3 w-full">
            {fromAttempts ? "← К попыткам" : "← Вернуться к курсу"}
          </button>
        </div>
      </div>
    );
  }

  if (loading) return (
    <div className="page">
      <div className="animate-pulse space-y-4 max-w-2xl mx-auto">
        <div className="h-10 bg-gray-100 rounded-xl" />
        {[1, 2, 3].map(i => <div key={i} className="h-32 bg-gray-100 rounded-2xl" />)}
      </div>
    </div>
  );
  if (!quiz) return <div className="page text-center text-gray-400">Тест не найден</div>;

  const answeredCount = Object.values(answers).filter((a: any) => a.selected_ids?.length > 0).length;
  const total = quiz.questions?.length || 0;

  return (
    <div className="page max-w-2xl">
      {/* Sticky header */}
      <div className="sticky top-14 z-10 -mx-4 px-4 pb-4">
        <div className="card px-5 py-3.5 flex items-center justify-between">
          <div>
            <p className="font-semibold text-sm text-gray-900">{quiz.title}</p>
            <p className="text-xs text-gray-400 mt-0.5">
              Отвечено {answeredCount} из {total}
              {answeredCount > 0 && (
                <span className="ml-2 inline-flex">
                  <span className="w-24 h-1 bg-gray-100 rounded-full overflow-hidden inline-block align-middle">
                    <span className="h-full bg-primary-500 rounded-full block transition-all" style={{ width: `${(answeredCount / total) * 100}%` }} />
                  </span>
                </span>
              )}
            </p>
          </div>
          {timeLeft !== null && (
            <div className={`font-mono font-bold text-sm px-3 py-1.5 rounded-lg ${timeLeft < 60 ? "bg-red-50 text-red-600" : "bg-gray-50 text-gray-700"}`}>
              {fmt(timeLeft)}
            </div>
          )}
        </div>
      </div>

      {/* Questions */}
      <div className="space-y-4 mb-5">
        {quiz.questions?.map((q: any, idx: number) => (
          <div key={q.id} className="card p-5">
            <p className="font-semibold text-gray-900 mb-4 text-sm leading-relaxed">
              <span className="text-primary-600 mr-2">{idx + 1}.</span>{q.text}
            </p>
            <div className="space-y-2">
              {q.options?.map((opt: any) => {
                const sel = answers[q.id]?.selected_ids?.includes(opt.id);
                return (
                  <label key={opt.id}
                    className={`flex items-center gap-3 px-4 py-3 rounded-xl border cursor-pointer transition-all text-sm ${
                      sel ? "bg-primary-50 border-primary-300 text-primary-900" : "border-gray-100 hover:border-gray-200 hover:bg-gray-50 text-gray-700"
                    }`}>
                    <input
                      type={q.type === "MULTIPLE_CHOICE" ? "checkbox" : "radio"}
                      name={`q-${q.id}`}
                      checked={!!sel}
                      onChange={() => handleSelect(q.id, opt.id, q.type)}
                      className="w-4 h-4 accent-primary-600"
                    />
                    <span>{opt.text}</span>
                  </label>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <button onClick={handleSubmit} disabled={submitting || !attemptId}
        className="btn-primary w-full py-3.5 text-base disabled:opacity-50">
        {submitting ? "Отправка..." : "Завершить тест"}
      </button>
    </div>
  );
}
