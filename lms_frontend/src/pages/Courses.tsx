import { useEffect, useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { getCourses } from "../api";

const CATEGORIES = [
  { value: "all",         label: "Все" },
  { value: "programming", label: "Программирование" },
  { value: "design",      label: "Дизайн" },
  { value: "marketing",   label: "Маркетинг" },
  { value: "business",    label: "Бизнес" },
  { value: "languages",   label: "Языки" },
  { value: "other",       label: "Другое" },
];

export default function Courses() {
  const [courses, setCourses] = useState<any[]>([]);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getCourses()
      .then(res => setCourses(res.data || []))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() =>
    selectedCategory === "all" ? courses : courses.filter(c => c.category === selectedCategory),
    [selectedCategory, courses]
  );

  const catLabel = (val: string) => CATEGORIES.find(c => c.value === val)?.label || val;

  return (
    <div className="page">
      {/* Header row */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="page-title">Каталог курсов</h1>
          <p className="text-gray-500 text-sm mt-1">{loading ? "Загрузка..." : `${courses.length} курсов`}</p>
        </div>
        {/* Category pills */}
        <div className="flex flex-wrap gap-2">
          {CATEGORIES.map(cat => (
            <button key={cat.value} onClick={() => setSelectedCategory(cat.value)}
              className={`px-3.5 py-1.5 rounded-full text-sm font-medium transition-all ${
                selectedCategory === cat.value
                  ? "bg-primary-600 text-white shadow-sm"
                  : "bg-white text-gray-600 border border-gray-200 hover:border-primary-300 hover:text-primary-600"
              }`}>
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="card animate-pulse">
              <div className="aspect-video bg-gray-100" />
              <div className="p-5 space-y-3">
                <div className="h-3 bg-gray-100 rounded w-1/4" />
                <div className="h-4 bg-gray-100 rounded w-3/4" />
                <div className="h-3 bg-gray-100 rounded w-full" />
              </div>
            </div>
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <div className="card p-16 text-center">
          <p className="text-gray-400 font-medium">Курсов не найдено</p>
          <p className="text-gray-300 text-sm mt-1">
            {selectedCategory !== "all" && `В категории «${catLabel(selectedCategory)}» пусто`}
          </p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filtered.map(course => (
            <Link key={course.id} to={`/course/${course.id}`} className="card-hover group block">
              <div className="aspect-video overflow-hidden bg-gray-50 rounded-t-2xl">
                <img
                  src={course.image || "https://placehold.co/600x400/7c3aed/white?text=Course"}
                  alt={course.title}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
              </div>
              <div className="p-5">
                <span className="badge-primary mb-3">{catLabel(course.category)}</span>
                <h3 className="font-semibold text-gray-900 mb-1.5 group-hover:text-primary-600 transition-colors line-clamp-2">
                  {course.title}
                </h3>
                <p className="text-gray-400 text-sm mb-4 line-clamp-2">{course.description || "—"}</p>
                <div className="flex items-center justify-between text-xs text-gray-400 pt-3 border-t border-gray-50">
                  <span>{course.instructor}</span>
                  <span>{course.lessons?.length || 0} уроков</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
