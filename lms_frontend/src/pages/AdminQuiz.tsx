// Файл: lms_frontend/src/pages/AdminQuiz.tsx
import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { createCourse } from "../api";

// 🔥 Этот компонент теперь используется ТОЛЬКО для редактирования существующих тестов
// Создание тестов происходит встроенно в AdminCourses.tsx при создании курса

export default function AdminQuiz() {
  const { quizId, courseId } = useParams();
  const navigate = useNavigate();
  
  const [loading, setLoading] = useState(false);
  const [title, setTitle] = useState("Тест к уроку");
  const [timeLimit, setTimeLimit] = useState(600);
  const [passingScore, setPassingScore] = useState(0.7);
  const [questions, setQuestions] = useState<any[]>([
    { id: crypto.randomUUID(), type: "SINGLE_CHOICE", text: "", options: [{ id: crypto.randomUUID(), text: "" }], correct_answer: { ids: [] } }
  ]);

  const addQuestion = () => {
    setQuestions([...questions, {
      id: crypto.randomUUID(),
      type: "SINGLE_CHOICE",
      text: "",
      options: [{ id: crypto.randomUUID(), text: "" }, { id: crypto.randomUUID(), text: "" }],
      correct_answer: { ids: [] }
    }]);
  };

  const updateQuestion = (idx: number, field: string, val: any) => {
    const upd = [...questions];
    upd[idx] = { ...upd[idx], [field]: val };
    if (field === "type" && val === "TRUE_FALSE") {
      upd[idx].options = [
        { id: crypto.randomUUID(), text: "Верно" },
        { id: crypto.randomUUID(), text: "Неверно" }
      ];
    }
    setQuestions(upd);
  };

  const updateOption = (qIdx: number, optIdx: number, text: string) => {
    const upd = [...questions];
    upd[qIdx].options[optIdx].text = text;
    setQuestions(upd);
  };

  const addOption = (qIdx: number) => {
    const upd = [...questions];
    upd[qIdx].options.push({ id: crypto.randomUUID(), text: "" });
    setQuestions(upd);
  };

  const toggleCorrect = (qIdx: number, optIdx: number) => {
    const upd = [...questions];
    const optId = upd[qIdx].options[optIdx].id;
    const ids = upd[qIdx].correct_answer.ids || [];
    
    if (upd[qIdx].type === "SINGLE_CHOICE") {
      upd[qIdx].correct_answer.ids = [optId];
    } else {
      upd[qIdx].correct_answer.ids = ids.includes(optId)
        ? ids.filter((id: string) => id !== optId)
        : [...ids, optId];
    }
    setQuestions(upd);
  };

  const removeQuestion = (idx: number) => {
    setQuestions(questions.filter((_, i) => i !== idx));
  };

  const handleSave = async () => {
    // 🔥 В новой архитектуре тесты редактируются через updateCourse или отдельный эндпоинт
    // Здесь — заглушка для демонстрации
    alert("⚠️ В текущей версии тесты редактируются внутри формы создания курса (AdminCourses).");
    navigate(courseId ? `/course/${courseId}` : "/courses");
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">⚠️ Редактирование тестов</h2>
        <button onClick={() => navigate(courseId ? `/course/${courseId}` : "/courses")} 
                className="px-4 py-2 bg-slate-100 rounded hover:bg-slate-200">
          ← Назад
        </button>
      </div>

      <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg mb-6 text-yellow-800">
        <p className="font-semibold">Примечание:</p>
        <p className="text-sm">В текущей версии тесты создаются и редактируются встроенно в форму создания курса (страница "Создать курс"). Этот экран оставлен для совместимости.</p>
      </div>

      <div className="bg-white p-6 rounded-xl border shadow-sm space-y-6">
        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Название теста</label>
            <input value={title} onChange={e => setTitle(e.target.value)} className="w-full p-2 border rounded" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Время (сек)</label>
            <input type="number" value={timeLimit} onChange={e => setTimeLimit(Number(e.target.value))} className="w-full p-2 border rounded" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Проходной балл (0-1)</label>
            <input type="number" step="0.1" min="0" max="1" value={passingScore} onChange={e => setPassingScore(Number(e.target.value))} className="w-full p-2 border rounded" />
          </div>
        </div>

        <div className="space-y-4">
          <h3 className="font-semibold">Вопросы ({questions.length})</h3>
          {questions.map((q, qIdx) => (
            <div key={q.id || qIdx} className="p-4 bg-slate-50 rounded border">
              <div className="flex justify-between mb-2">
                <select value={q.type} onChange={e => updateQuestion(qIdx, "type", e.target.value)} className="p-1 border rounded text-sm">
                  <option value="SINGLE_CHOICE">Один ответ</option>
                  <option value="MULTIPLE_CHOICE">Несколько ответов</option>
                  <option value="TRUE_FALSE">Верно/Неверно</option>
                </select>
                <button onClick={() => removeQuestion(qIdx)} className="text-red-500 text-sm hover:underline">Удалить</button>
              </div>
              <input value={q.text} onChange={e => updateQuestion(qIdx, "text", e.target.value)} 
                     className="w-full p-2 border rounded mb-2" placeholder="Текст вопроса..." />
              <div className="space-y-2 ml-4">
                {q.options?.map((opt: any, optIdx: number) => (
                  <div key={opt.id || optIdx} className="flex items-center gap-2">
                    <input type={q.type === "MULTIPLE_CHOICE" ? "checkbox" : "radio"}
                           checked={(q.correct_answer.ids || []).includes(opt.id)}
                           onChange={() => toggleCorrect(qIdx, optIdx)} />
                    <input value={opt.text} onChange={e => updateOption(qIdx, optIdx, e.target.value)} 
                           className="flex-1 p-1 border rounded text-sm" placeholder="Вариант ответа" />
                  </div>
                ))}
                {q.type !== "TRUE_FALSE" && (
                  <button onClick={() => addOption(qIdx)} className="text-primary-600 text-xs hover:underline mt-1">
                    + Добавить вариант
                  </button>
                )}
              </div>
            </div>
          ))}
          <button onClick={addQuestion} className="w-full py-2 border-2 border-dashed border-slate-300 rounded text-slate-500 hover:border-primary-500 hover:text-primary-600 transition">
            ➕ Добавить вопрос
          </button>
        </div>

        <button onClick={handleSave} disabled={loading} className="btn-primary w-full py-3 disabled:opacity-50">
          {loading ? "Сохранение..." : "💾 Сохранить изменения"}
        </button>
      </div>
    </div>
  );
}