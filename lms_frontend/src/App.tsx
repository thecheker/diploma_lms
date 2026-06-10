import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Header from "./components/Header";
import Auth from "./pages/Auth";
import Home from "./pages/Home";
import Courses from "./pages/Courses";
import CoursePage from "./pages/CoursePage";
import QuizPage from "./pages/QuizPage";
import AdminCourses from "./pages/AdminCourses";
import QuizEditor from "./pages/QuizEditor";
import MyAttempts from "./pages/MyAttempts";
import MyCourses from "./pages/MyCourses";
const AdminDashboard = () => <Navigate to="/admin/courses" replace />;

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/courses" element={<Courses />} />
            <Route path="/course/:id" element={<CoursePage />} />
            <Route path="/quiz/:quizId" element={<QuizPage />} />
            <Route path="/quiz/:quizId/start" element={<QuizPage startMode />} />
            <Route path="/my-attempts" element={<MyAttempts />} />
            <Route path="/my-courses" element={<MyCourses />} />
            
            {/* 🔥 Админка: /admin → редирект на /admin/courses */}
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/admin/courses" element={<AdminCourses />} />
            <Route path="/admin/quiz/:quizId/edit" element={<QuizEditor />} />
            <Route path="/course/:courseId/quiz/:quizId/edit" element={<QuizEditor />} />
            
            {/* 404 */}
            <Route path="*" element={
              <div className="max-w-2xl mx-auto p-12 text-center">
                <h1 className="text-4xl font-bold mb-4">404</h1>
                <p className="text-slate-600 mb-6">Страница не найдена</p>
                <a href="/" className="btn-primary">На главную</a>
              </div>
            } />
          </Routes>
        </main>
      </div>
    </Router>
  );
}