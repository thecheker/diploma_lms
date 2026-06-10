import { Link } from "react-router-dom";

const FEATURES = [
  { icon: "✦", title: "Практические курсы", desc: "Реальные проекты и задачи от практикующих специалистов" },
  { icon: "✦", title: "Тесты и проверка", desc: "Автоматическая оценка знаний после каждого урока" },
  { icon: "✦", title: "Прогресс в реальном времени", desc: "Отслеживайте своё обучение и возвращайтесь в любой момент" },
  { icon: "✦", title: "Удобный редактор", desc: "Создавайте курсы и тесты прямо в браузере без лишних инструментов" },
];

const CATEGORIES = [
  { name: "Программирование", slug: "programming", bg: "from-violet-500 to-indigo-600" },
  { name: "Дизайн",           slug: "design",       bg: "from-pink-500 to-rose-600" },
  { name: "Маркетинг",        slug: "marketing",    bg: "from-amber-500 to-orange-600" },
  { name: "Бизнес",           slug: "business",     bg: "from-emerald-500 to-teal-600" },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero */}
      <section className="relative overflow-hidden bg-dark pt-24 pb-32">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(124,58,237,0.3),rgba(255,255,255,0))]" />
        <div className="relative max-w-4xl mx-auto px-6 text-center">
          <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 rounded-full px-4 py-1.5 text-sm text-gray-400 mb-8">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            Дипломный проект · 2026
          </div>
          <h1 className="text-5xl md:text-7xl font-bold text-white leading-[1.05] tracking-tight mb-6">
            Учитесь новому.<br />
            <span className="bg-gradient-to-r from-primary-400 to-violet-300 bg-clip-text text-transparent">
              Растите быстрее.
            </span>
          </h1>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            LowSkill — платформа для практического обучения. Создавайте курсы,
            проходите тесты и отслеживайте прогресс в одном месте.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link to="/courses"
              className="inline-flex items-center justify-center gap-2 bg-primary-600 hover:bg-primary-500 text-white font-semibold px-7 py-3.5 rounded-xl transition-all shadow-lg shadow-primary-900/30">
              Начать обучение
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
            <Link to="/auth?mode=register"
              className="inline-flex items-center justify-center gap-2 bg-white/5 hover:bg-white/10 border border-white/10 text-gray-300 font-semibold px-7 py-3.5 rounded-xl transition-all">
              Создать аккаунт
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-24 bg-surface">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-14">
            <h2 className="section-title mb-4">Всё что нужно для обучения</h2>
            <p className="text-gray-500 max-w-xl mx-auto">Мы собрали всё необходимое в одном месте — от материалов до проверки знаний</p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {FEATURES.map((f, i) => (
              <div key={i} className="card p-6 hover:shadow-card-hover hover:-translate-y-0.5 transition-all duration-200">
                <div className="w-8 h-8 rounded-lg bg-primary-100 flex items-center justify-center text-primary-600 font-bold mb-4 text-sm">
                  {f.icon}
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{f.title}</h3>
                <p className="text-gray-500 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="py-24 bg-white">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-14">
            <h2 className="section-title mb-4">Категории курсов</h2>
            <p className="text-gray-500 max-w-xl mx-auto">Выберите направление и начните учиться прямо сейчас</p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {CATEGORIES.map((cat, i) => (
              <Link key={i} to={`/courses`}
                className="group relative overflow-hidden rounded-2xl h-36 flex flex-col justify-end p-5">
                <div className={`absolute inset-0 bg-gradient-to-br ${cat.bg} opacity-90 group-hover:opacity-100 transition-opacity`} />
                <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity"
                  style={{ background: "radial-gradient(circle at 30% 107%, rgba(255,255,255,0.15) 0%, transparent 50%)" }} />
                <h3 className="relative text-white font-bold text-lg">{cat.name}</h3>
                <span className="relative text-white/60 text-xs mt-0.5 group-hover:text-white/80 transition-colors">
                  Смотреть курсы →
                </span>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 bg-surface">
        <div className="max-w-3xl mx-auto px-6 text-center">
          <div className="card p-12">
            <h2 className="text-3xl font-bold mb-4">Готовы начать?</h2>
            <p className="text-gray-500 mb-8">Присоединяйтесь и начните обучение уже сегодня</p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Link to="/courses" className="btn-primary px-7 py-3 text-base">Смотреть курсы</Link>
              <Link to="/auth" className="btn-outline px-7 py-3 text-base">Войти в аккаунт</Link>
            </div>
          </div>
        </div>
      </section>

      <footer className="bg-dark border-t border-white/5 py-8">
        <div className="max-w-7xl mx-auto px-6 text-center text-gray-600 text-sm">
          © 2026 LowSkill · Дипломный проект
        </div>
      </footer>
    </div>
  );
}
