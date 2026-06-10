import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createCourse } from "../api";

const CATEGORIES = [
  { value: "programming", label: "Программирование" },
  { value: "design",      label: "Дизайн" },
  { value: "marketing",   label: "Маркетинг" },
  { value: "business",    label: "Бизнес" },
  { value: "languages",   label: "Языки" },
  { value: "other",       label: "Другое" },
];

const newLesson = () => ({
  title: "", lesson_type: "TEXT", content: { body: "" }, has_quiz: false,
  quiz: { title: "Тест к уроку", time_limit_sec: 600, passing_score: 0.7, questions: [] },
});

const newQuestion = () => ({
  type: "SINGLE_CHOICE", text: "",
  options: [{ id: crypto.randomUUID(), text: "" }, { id: crypto.randomUUID(), text: "" }],
  correct_answer: { ids: [] },
});

export default function AdminCourses() {
  const navigate = useNavigate();
  const [title, setTitle]           = useState("");
  const [description, setDesc]      = useState("");
  const [instructor, setInstructor] = useState("");
  const [image, setImage]           = useState("");
  const [category, setCategory]     = useState("programming");
  const [lessons, setLessons]       = useState<any[]>([newLesson()]);
  const [msg, setMsg]               = useState("");
  const [loading, setLoading]       = useState(false);

  /* ── lesson helpers ── */
  const updLesson = (i: number, field: string, val: any) =>
    setLessons(ls => ls.map((l, idx) => idx !== i ? l : { ...l, [field]: val }));

  const updQuiz = (i: number, field: string, val: any) =>
    setLessons(ls => ls.map((l, idx) => idx !== i ? l : { ...l, quiz: { ...l.quiz, [field]: val } }));

  const addQuestion = (i: number) =>
    setLessons(ls => ls.map((l, idx) => idx !== i ? l : {
      ...l, quiz: { ...l.quiz, questions: [...l.quiz.questions, newQuestion()] },
    }));

  const updQuestion = (li: number, qi: number, field: string, val: any) =>
    setLessons(ls => ls.map((l, idx) => {
      if (idx !== li) return l;
      const questions = l.quiz.questions.map((q: any, j: number) => {
        if (j !== qi) return q;
        const u = { ...q, [field]: val };
        if (field === "type" && val === "TRUE_FALSE")
          u.options = [{ id: crypto.randomUUID(), text: "Верно" }, { id: crypto.randomUUID(), text: "Неверно" }];
        return u;
      });
      return { ...l, quiz: { ...l.quiz, questions } };
    }));

  const updOption = (li: number, qi: number, oi: number, text: string) =>
    setLessons(ls => ls.map((l, idx) => {
      if (idx !== li) return l;
      const questions = l.quiz.questions.map((q: any, j: number) =>
        j !== qi ? q : { ...q, options: q.options.map((o: any, k: number) => k === oi ? { ...o, text } : o) }
      );
      return { ...l, quiz: { ...l.quiz, questions } };
    }));

  const toggleCorrect = (li: number, qi: number, oi: number) =>
    setLessons(ls => ls.map((l, idx) => {
      if (idx !== li) return l;
      const questions = l.quiz.questions.map((q: any, j: number) => {
        if (j !== qi) return q;
        const optId = q.options[oi].id;
        const ids: string[] = q.correct_answer.ids || [];
        const newIds = q.type === "SINGLE_CHOICE" ? [optId] : ids.includes(optId) ? ids.filter((id: string) => id !== optId) : [...ids, optId];
        return { ...q, correct_answer: { ids: newIds } };
      });
      return { ...l, quiz: { ...l.quiz, questions } };
    }));

  /* ── submit ── */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMsg("");
    try {
      const res = await createCourse({
        title, description, instructor, image, category,
        lessons: lessons.map((l, i) => ({
          title: l.title || `Урок ${i + 1}`,
          lesson_type: l.lesson_type,
          content: l.lesson_type === "VIDEO" ? { url: l.content?.url || "" } : { body: l.content?.body || "" },
          order_index: i,
          quiz: l.has_quiz ? l.quiz : undefined,
        })),
      });
      setMsg("success");
      setTimeout(() => navigate(`/course/${res.data.id}`), 1200);
    } catch (err: any) {
      setMsg(err.response?.data?.detail || "Ошибка создания курса");
    } finally { setLoading(false); }
  };

  return (
    <div className="page max-w-3xl">
      <div className="mb-6">
        <h1 className="page-title">Создать курс</h1>
        <p className="text-gray-400 text-sm mt-0.5">Заполните информацию и добавьте уроки</p>
      </div>

      {msg === "success" && <div className="alert-success mb-5">Курс создан! Переходим...</div>}
      {msg && msg !== "success" && <div className="alert-error mb-5">{msg}</div>}

      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Course info */}
        <div className="card p-5 space-y-4">
          <h2 className="font-semibold text-sm text-gray-900">Информация о курсе</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="label">Название *</label>
              <input value={title} onChange={e => setTitle(e.target.value)} className="input" placeholder="Введите название курса" required />
            </div>
            <div>
              <label className="label">Категория</label>
              <select value={category} onChange={e => setCategory(e.target.value)} className="select">
                {CATEGORIES.map(c => <option key={c.value} value={c.value}>{c.label}</option>)}
              </select>
            </div>
          </div>
          <div>
            <label className="label">Описание</label>
            <textarea value={description} onChange={e => setDesc(e.target.value)} className="textarea h-20" placeholder="Краткое описание курса" />
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="label">Преподаватель</label>
              <input value={instructor} onChange={e => setInstructor(e.target.value)} className="input" placeholder="Имя преподавателя" />
            </div>
            <div>
              <label className="label">URL обложки</label>
              <input value={image} onChange={e => setImage(e.target.value)} className="input" placeholder="https://..." />
            </div>
          </div>
        </div>

        {/* Lessons */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="font-semibold text-sm text-gray-900">Уроки</h2>
            <button type="button" onClick={() => setLessons(ls => [...ls, newLesson()])} className="btn-outline text-xs py-1.5 px-3">+ Добавить урок</button>
          </div>

          {lessons.map((l, i) => (
            <div key={i} className="card p-5">
              <div className="flex items-center gap-3 mb-4">
                <span className="w-6 h-6 bg-primary-100 text-primary-600 rounded-lg text-xs font-bold flex items-center justify-center shrink-0">{i + 1}</span>
                <span className="font-semibold text-sm text-gray-700 flex-1">Урок {i + 1}</span>
                {lessons.length > 1 && (
                  <button type="button" onClick={() => setLessons(ls => ls.filter((_, idx) => idx !== i))} className="text-xs text-red-400 hover:text-red-600 font-medium">Удалить</button>
                )}
              </div>

              <div className="space-y-3">
                <div>
                  <label className="label">Название урока *</label>
                  <input value={l.title} onChange={e => updLesson(i, "title", e.target.value)} className="input" placeholder="Название урока" required />
                </div>

                <div className="flex gap-3 items-center">
                  <div className="flex-1">
                    <label className="label">Тип</label>
                    <select value={l.lesson_type} onChange={e => updLesson(i, "lesson_type", e.target.value)} className="select">
                      <option value="TEXT">Текст</option>
                      <option value="VIDEO">Видео</option>
                    </select>
                  </div>
                  <div className="pt-6">
                    <label className="flex items-center gap-2 cursor-pointer select-none">
                      <input type="checkbox" checked={l.has_quiz} onChange={e => updLesson(i, "has_quiz", e.target.checked)} className="w-4 h-4 accent-primary-600" />
                      <span className="text-sm text-gray-700 font-medium">Добавить тест</span>
                    </label>
                  </div>
                </div>

                {l.lesson_type === "VIDEO" ? (
                  <div>
                    <label className="label">URL видео</label>
                    <input value={l.content.url || ""} onChange={e => updLesson(i, "content", { ...l.content, url: e.target.value })} className="input" placeholder="https://..." />
                  </div>
                ) : (
                  <div>
                    <label className="label">Содержимое урока</label>
                    <textarea value={l.content.body || ""} onChange={e => updLesson(i, "content", { ...l.content, body: e.target.value })} className="textarea h-24" placeholder="Текст урока..." />
                  </div>
                )}

                {/* Quiz editor */}
                {l.has_quiz && (
                  <div className="mt-2 p-4 bg-primary-50 border border-primary-100 rounded-xl space-y-3">
                    <h4 className="font-semibold text-sm text-primary-800">Тест к уроку</h4>
                    <div className="grid grid-cols-3 gap-3">
                      <div>
                        <label className="label text-xs">Название</label>
                        <input value={l.quiz.title} onChange={e => updQuiz(i, "title", e.target.value)} className="input text-sm py-2" />
                      </div>
                      <div>
                        <label className="label text-xs">Время (сек)</label>
                        <input type="number" value={l.quiz.time_limit_sec} onChange={e => updQuiz(i, "time_limit_sec", Number(e.target.value))} className="input text-sm py-2" />
                      </div>
                      <div>
                        <label className="label text-xs">Проходной (0–1)</label>
                        <input type="number" step="0.1" value={l.quiz.passing_score} onChange={e => updQuiz(i, "passing_score", Number(e.target.value))} className="input text-sm py-2" />
                      </div>
                    </div>

                    {/* Questions */}
                    <div className="space-y-2">
                      {l.quiz.questions.map((q: any, qi: number) => (
                        <div key={qi} className="bg-white rounded-xl border border-primary-100 p-3">
                          <div className="flex items-center gap-2 mb-2">
                            <select value={q.type} onChange={e => updQuestion(i, qi, "type", e.target.value)} className="select text-xs py-1.5 flex-1 max-w-[160px]">
                              <option value="SINGLE_CHOICE">Один ответ</option>
                              <option value="MULTIPLE_CHOICE">Несколько</option>
                              <option value="TRUE_FALSE">Верно/Неверно</option>
                            </select>
                            <button type="button" onClick={() => setLessons(ls => ls.map((l2, li) => li !== i ? l2 : {
                              ...l2, quiz: { ...l2.quiz, questions: l2.quiz.questions.filter((_: any, qi2: number) => qi2 !== qi) }
                            }))} className="text-red-400 hover:text-red-600 text-xs ml-auto">✕</button>
                          </div>
                          <input value={q.text} onChange={e => updQuestion(i, qi, "text", e.target.value)} className="input text-sm py-1.5 mb-2" placeholder="Текст вопроса" />
                          {q.options.map((opt: any, oi: number) => (
                            <div key={oi} className="flex items-center gap-2 mb-1.5">
                              <input type={q.type === "MULTIPLE_CHOICE" ? "checkbox" : "radio"} checked={(q.correct_answer.ids || []).includes(opt.id)} onChange={() => toggleCorrect(i, qi, oi)} className="w-3.5 h-3.5 accent-primary-600 shrink-0" />
                              <input value={opt.text} onChange={e => updOption(i, qi, oi, e.target.value)} className="input text-xs py-1" placeholder="Вариант" />
                            </div>
                          ))}
                        </div>
                      ))}
                      <button type="button" onClick={() => addQuestion(i)} className="text-xs text-primary-600 hover:text-primary-700 font-medium">+ Добавить вопрос</button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        <button type="submit" disabled={loading} className="btn-primary w-full py-3.5 text-base">
          {loading ? "Создание..." : "Создать курс"}
        </button>
      </form>
    </div>
  );
}
