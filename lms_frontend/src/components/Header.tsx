import { Link, useLocation, useNavigate } from "react-router-dom";

const getUser = () => {
  const token = localStorage.getItem("token");
  if (!token) return null;
  try {
    const p = JSON.parse(atob(token.split(".")[1]));
    return { role: (p.role || "STUDENT").toUpperCase() };
  } catch { return null; }
};

export default function Header() {
  const navigate = useNavigate();
  const location = useLocation();
  const user = getUser();
  const isAdmin = user?.role === "ADMIN" || user?.role === "INSTRUCTOR";

  const isActive = (path: string) =>
    location.pathname === path || location.pathname.startsWith(path + "/");

  const navLink = (to: string, label: string) => (
    <Link
      to={to}
      className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
        isActive(to)
          ? "bg-white/10 text-white"
          : "text-gray-400 hover:text-white hover:bg-white/5"
      }`}
    >
      {label}
    </Link>
  );

  return (
    <header className="bg-dark border-b border-white/5 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center gap-6">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 shrink-0">
          <div className="w-7 h-7 bg-primary-600 rounded-lg flex items-center justify-center">
            <svg className="w-4 h-4 text-white" viewBox="0 0 16 16" fill="currentColor">
              <path d="M2 3a1 1 0 011-1h10a1 1 0 011 1v2H2V3zm0 4h12v6a1 1 0 01-1 1H3a1 1 0 01-1-1V7zm4 2a.5.5 0 000 1h4a.5.5 0 000-1H6z"/>
            </svg>
          </div>
          <span className="text-white font-bold text-sm tracking-tight">LowSkill</span>
        </Link>

        {/* Nav */}
        <nav className="flex items-center gap-1 flex-1">
          {navLink("/", "Главная")}
          {navLink("/courses", "Каталог")}
          {user && navLink("/my-courses", "Мои курсы")}
          {user && navLink("/my-attempts", "Попытки")}
        </nav>

        {/* Right */}
        <div className="flex items-center gap-2 shrink-0">
          {isAdmin && (
            <Link to="/admin" className="btn-primary py-1.5 px-3 text-xs rounded-lg shadow-none">
              Управление
            </Link>
          )}
          {user ? (
            <button
              onClick={() => { localStorage.removeItem("token"); navigate("/"); window.location.reload(); }}
              className="text-gray-400 hover:text-white text-sm font-medium transition-colors px-3 py-1.5"
            >
              Выйти
            </button>
          ) : (
            <Link to="/auth" className="btn-primary py-1.5 px-4 text-xs rounded-lg">
              Войти
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
