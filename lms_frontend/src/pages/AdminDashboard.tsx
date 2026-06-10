// Файл: lms_frontend/src/pages/AdminDashboard.tsx
import { Routes, Route, Link, useLocation, Navigate } from "react-router-dom";
import AdminCourses from "./AdminCourses";
import AdminQuiz from "./AdminQuiz";

export default function AdminDashboard() {
  const loc = useLocation();
  const token = localStorage.getItem("token");
  
  // Защита роутов: если нет токена — редирект на вход
  if (!token) return <Navigate to="/auth" replace />;
  
  const isCourses = loc.pathname.includes("/courses");
  
  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex gap-4 mb-6 border-b pb-4">
        <Link to="/admin/courses" className={`px-4 py-2 rounded-lg font-medium transition ${
          isCourses ? 'bg-primary-600 text-white' : 'text-slate-600 hover:bg-slate-100'
        }`}>
          📚 Курсы и уроки
        </Link>
        <Link to="/admin/quizzes" className={`px-4 py-2 rounded-lg font-medium transition ${
          !isCourses ? 'bg-primary-600 text-white' : 'text-slate-600 hover:bg-slate-100'
        }`}>
          🧠 Редактор тестов
        </Link>
      </div>
      
      <Routes>
        <Route path="courses" element={<AdminCourses />} />
        <Route path="quizzes" element={<AdminQuiz />} />
        <Route index element={<AdminCourses />} />
      </Routes>
    </div>
  );
}