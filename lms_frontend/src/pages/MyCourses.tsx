import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getMyCourses } from "../api";

export default function MyCourses() {
  const [courses, setCourses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMyCourses()
      .then(res => setCourses(Array.isArray(res.data) ? res.data : []))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="page">
      <div className="mb-6">
        <h1 className="page-title">Мои курсы</h1>
        <p className="text-gray-500 text-sm mt-1">Курсы, в которых вы начали обучение</p>
      </div>

      {loading ? (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {[1, 2, 3].map(i => <div key={i} className="card h-48 animate-pulse" />)}
        </div>
      ) : courses.length === 0 ? (
        <div className="card p-16 text-center">
          <p className="text-gray-400 font-medium">Вы ещё не начали ни один курс</p>
          <Link to="/courses" className="btn-primary mt-4 inline-flex">Перейти к каталогу</Link>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {courses.map(c => (
            <Link key={c.course_id} to={`/course/${c.course_id}`} className="card-hover group block">
              <div className="aspect-video relative overflow-hidden bg-gray-50 rounded-t-2xl">
                <img
                  src={c.course_image || "https://placehold.co/600x400/7c3aed/white?text=Course"}
                  alt={c.course_title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                {c.completed && (
                  <div className="absolute top-3 right-3 badge-green shadow-sm">
                    Завершён
                  </div>
                )}
              </div>
              <div className="p-5">
                <h3 className="font-semibold text-gray-900 mb-3 group-hover:text-primary-600 transition-colors line-clamp-2">
                  {c.course_title}
                </h3>
                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs text-gray-400">
                    <span>Прогресс</span>
                    <span className="font-semibold text-gray-600">{c.progress_percent}%</span>
                  </div>
                  <div className="progress-bar h-1.5">
                    <div className="progress-fill h-1.5" style={{ width: `${c.progress_percent}%` }} />
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
