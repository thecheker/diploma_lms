import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getQuiz, updateQuiz } from "../api";

export default function QuizEditor() {
  const { quizId, courseId } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [title, setTitle] = useState("Новый тест");
  const [timeLimit, setTimeLimit] = useState(600);
  const [passingScore, setPassingScore] = useState(0.7);
  const [questions, setQuestions] = useState<any[]>([]);

  useEffect(() => {
    if (!quizId) { setLoading(false); return; }
    getQuiz(quizId)
      .then(res => {
        const d = res.data;
        setTitle(d.title);
        setTimeLimit(d.time_limit_sec);
        setPassingScore(d.passing_score);
        setQuestions((d.questions || []).map((q: any) => ({ ...q, correct_answer: q.correct_answer || { ids: [] } })));
      })
      .catch(() => alert("Не удалось загрузить тест"))
      .finally(() => setLoading(false));
  }, [quizId]);

  const addQuestion = () => setQuestions(qs => [...qs, {
    id: crypto.randomUUID(), type: "SINGLE_CHOICE", text: "",
    options: [{ id: crypto.randomUUID(), text: "" }, { id: crypto.randomUUID(), text: "" }],
    correct_answer: { ids: [] },
  }]);

  const updQ = (idx: number, field: string, val: any) =>
    setQuestions(qs => qs.map((q, i) => {
      if (i !== idx) return q;
      const u = { ...q, [field]: val };
      if (field === "type" && val === "TRUE_FALSE")
        u.options = [{ id: crypto.randomUUID(), text: "Верно" }, { id: crypto.randomUUID(), text: "Неверно" }];
      return u;
    }));

  const updOption = (qi: number, oi: number, text: string) =>
    setQuestions(qs => qs.map((q, i) => i !== qi ? q : { ...q, options: q.options.map((o: any, j: number) => j === oi ? { ...o, text } : o) }));

  const addOption = (qi: number) =>
    setQuestions(qs => qs.map((q, i) => i !== qi ? q : { ...q, options: [...q.options, { id: crypto.randomUUID(), text: "" }] }));

  const toggleCorrect = (qi: number, oi: number) =>
    setQuestions(qs => qs.map((q, i) => {
      if (i !== qi) return q;
      const optId = q.options[oi].id;
      const ids: string[] = q.correct_answer?.ids || [];
      const newIds = q.type === "SINGLE_CHOICE" ? [optId] : ids.includes(optId) ? ids.filter((id: string) => id !== optId) : [...ids, optId];
      return { ...q, correct_answer: { ids: newIds } };
    }));

  const back = () => navigate(courseId ? `/course/${courseId}` : "/courses");

  const handleSave = async () => {
    setSaving(true);
    try {
      await updateQuiz(quizId!, {
        title, time_limit_sec: timeLimit, passing_score: passingScore,
        questions: questions.map(q => ({ ...q, correct_answer: { ids: q.correct_answer?.ids || [] } })),
      });
      back();
    } catch (err: any) {
      alert(err.response?.data?.detail || err.message);
    } finally { setSaving(false); }
  };

  if (loading) return <div className="page text-center text-gray-400">Загрузка...</div>;

  return (
    <div className="page max-w-3xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="page-title">Редактор теста</h1>
          <p className="text-gray-400 text-sm mt-0.5">Изменения применяются после сохранения</p>
        </div>
        <button onClick={back} className="btn-ghost">← Отмена</button>
      </div>

      {/* Settings */}
      <div className="card p-5 mb-5">
        <h2 className="font-semibold text-sm text-gray-900 mb-4">Настройки теста</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <label className="label">Название</label>
            <input value={title} onChange={e => setTitle(e.target.value)} className="input" />
          </div>
          <div>
            <label className="label">Время (сек)</label>
            <input type="number" value={timeLimit} onChange={e => setTimeLimit(Number(e.target.value))} className="input" />
          </div>
          <div>
            <label className="label">Проходной балл (0–1)</label>
            <input type="number" step="0.1" min="0" max="1" value={passingScore} onChange={e => setPassingScore(Number(e.target.value))} className="input" />
          </div>
        </div>
      </div>

      {/* Questions */}
      <div className="space-y-3 mb-5">
        {questions.map((q, qi) => (
          <div key={q.id || qi} className="card p-5">
            <div className="flex items-center gap-3 mb-3">
              <span className="w-6 h-6 rounded-lg bg-primary-100 text-primary-600 text-xs font-bold flex items-center justify-center shrink-0">{qi + 1}</span>
              <select value={q.type} onChange={e => updQ(qi, "type", e.target.value)} className="select text-xs py-1.5 flex-1 max-w-[180px]">
                <option value="SINGLE_CHOICE">Один ответ</option>
                <option value="MULTIPLE_CHOICE">Несколько ответов</option>
                <option value="TRUE_FALSE">Верно / Неверно</option>
              </select>
              <button onClick={() => setQuestions(qs => qs.filter((_, i) => i !== qi))} className="btn-ghost text-red-400 hover:text-red-600 ml-auto text-xs">Удалить</button>
            </div>
            <input value={q.text} onChange={e => updQ(qi, "text", e.target.value)} className="input mb-3" placeholder="Текст вопроса..." />
            <div className="space-y-2 pl-2">
              {q.options?.map((opt: any, oi: number) => (
                <div key={opt.id || oi} className="flex items-center gap-2.5">
                  <input
                    type={q.type === "MULTIPLE_CHOICE" ? "checkbox" : "radio"}
                    checked={(q.correct_answer?.ids || []).includes(opt.id)}
                    onChange={() => toggleCorrect(qi, oi)}
                    className="w-4 h-4 accent-primary-600 shrink-0"
                  />
                  <input value={opt.text} onChange={e => updOption(qi, oi, e.target.value)}
                    className="input text-sm py-2" placeholder="Вариант ответа" />
                </div>
              ))}
              {q.type !== "TRUE_FALSE" && (
                <button onClick={() => addOption(qi)} className="text-xs text-primary-600 hover:text-primary-700 font-medium pl-6">+ Добавить вариант</button>
              )}
            </div>
          </div>
        ))}

        <button onClick={addQuestion}
          className="w-full py-3 border-2 border-dashed border-gray-200 rounded-xl text-sm text-gray-400 hover:border-primary-300 hover:text-primary-600 transition-colors font-medium">
          + Добавить вопрос
        </button>
      </div>

      <button onClick={handleSave} disabled={saving} className="btn-primary w-full py-3 text-base disabled:opacity-50">
        {saving ? "Сохранение..." : "Сохранить тест"}
      </button>
    </div>
  );
}
