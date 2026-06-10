import { useState } from "react";
import { useSearchParams, useNavigate, Link } from "react-router-dom";
import { login, register } from "../api";

export default function Auth() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const isRegister = params.get("mode") === "register";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      if (isRegister) {
        await register(email, password);
        alert("Регистрация успешна! Теперь войдите.");
        navigate("/auth");
      } else {
        await login(email, password);
        navigate("/");
        setTimeout(() => window.location.reload(), 100);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Ошибка авторизации");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-3.5rem)] flex">
      {/* Left panel */}
      <div className="hidden lg:flex flex-col justify-between w-[420px] bg-dark p-10 shrink-0">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 bg-primary-600 rounded-lg flex items-center justify-center">
            <svg className="w-4 h-4 text-white" viewBox="0 0 16 16" fill="currentColor">
              <path d="M2 3a1 1 0 011-1h10a1 1 0 011 1v2H2V3zm0 4h12v6a1 1 0 01-1 1H3a1 1 0 01-1-1V7zm4 2a.5.5 0 000 1h4a.5.5 0 000-1H6z"/>
            </svg>
          </div>
          <span className="text-white font-bold text-sm">LowSkill</span>
        </div>
        <div>
          <blockquote className="text-gray-300 text-lg font-medium leading-relaxed mb-4">
            "Лучшее вложение — это вложение в знания. Оно приносит наилучшие проценты."
          </blockquote>
          <p className="text-gray-500 text-sm">Платформа для практического обучения</p>
        </div>
      </div>

      {/* Right panel */}
      <div className="flex-1 flex items-center justify-center p-6 bg-surface">
        <div className="w-full max-w-sm">
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-1">
              {isRegister ? "Создать аккаунт" : "Добро пожаловать"}
            </h1>
            <p className="text-gray-500 text-sm">
              {isRegister ? "Заполните данные для регистрации" : "Войдите в свой аккаунт"}
            </p>
          </div>

          {error && <div className="alert-error mb-5">{error}</div>}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Email</label>
              <input type="email" value={email} onChange={e => setEmail(e.target.value)}
                className="input" placeholder="name@example.com" required />
            </div>
            <div>
              <label className="label">Пароль</label>
              <input type="password" value={password} onChange={e => setPassword(e.target.value)}
                className="input" placeholder="••••••••" required />
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full py-3 mt-2">
              {loading ? "Загрузка..." : (isRegister ? "Зарегистрироваться" : "Войти")}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-500">
            {isRegister ? "Уже есть аккаунт? " : "Нет аккаунта? "}
            <Link to={isRegister ? "/auth" : "/auth?mode=register"}
              className="text-primary-600 font-semibold hover:text-primary-700">
              {isRegister ? "Войти" : "Создать"}
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
