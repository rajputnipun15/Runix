import Link from "next/link";

/**
 * RUNIX Landing Page
 *
 * Implements: Stitch screen "RUNIX — Cloud Platform Landing (Animated)"
 * Screen ID: 9df9ed75441941a79f618295d6ca10c0
 *
 * Design language from Stitch:
 * - Deep dark background (#0f131b)
 * - Indigo primary (#4f46e5 container, #c3c0ff text)
 * - Geist font for body, JetBrains Mono for labels
 * - Terminal icon badge for RUNIX wordmark
 * - Perfectly aligned 3-column navbar and content grid
 */
export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* ──── Navigation ──── */}
      <header className="sticky top-0 z-50 border-b border-outline-variant/30 bg-surface-container-lowest/90 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 h-14 grid grid-cols-3 items-center">
          {/* Brand (Left Column) */}
          <div className="flex items-center gap-2.5 justify-start">
            <div className="w-7 h-7 rounded bg-primary-container flex items-center justify-center shadow-sm">
              <svg
                className="w-4 h-4 text-on-primary-container"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
            </div>
            <span className="text-on-surface font-semibold text-lg tracking-tight font-mono">
              RUNIX
            </span>
          </div>

          {/* Nav links (Center Column - Mathematically Centered) */}
          <nav className="hidden md:flex items-center justify-center gap-8 text-sm text-on-surface-variant font-medium">
            <a href="#features" className="hover:text-on-surface transition-colors">
              Features
            </a>
            <a href="#templates" className="hover:text-on-surface transition-colors">
              Templates
            </a>
            <a href="#architecture" className="hover:text-on-surface transition-colors">
              Architecture
            </a>
          </nav>

          {/* Auth actions (Right Column) */}
          <div className="flex items-center justify-end gap-3">
            <Link
              href="/login"
              className="text-sm text-on-surface-variant hover:text-on-surface transition-colors px-3 py-1.5"
            >
              Sign In
            </Link>
            <Link
              href="/register"
              className="text-sm bg-primary-container text-on-primary-container hover:bg-primary-container/90 px-4 py-1.5 rounded transition-colors shadow-sm font-semibold"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* ──── Hero Section ──── */}
      <main className="flex-1">
        <section className="relative overflow-hidden">
          {/* Ambient glow */}
          <div className="absolute -top-40 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-primary-container/15 blur-[120px] rounded-full pointer-events-none" />

          <div className="max-w-7xl mx-auto px-6 pt-20 pb-16 text-center relative">
            {/* Version badge */}
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container text-on-surface-variant text-xs font-mono mb-8 border border-outline-variant/30">
              <span className="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse" />
              <span>v0.1.0-dev</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-semibold text-on-surface tracking-tight leading-tight max-w-4xl mx-auto">
              Build. Run. Ship.{" "}
              <span className="text-primary">Anywhere.</span>
            </h1>

            <p className="mt-6 text-lg text-on-surface-variant max-w-2xl mx-auto leading-relaxed">
              A complete cloud development environment in your browser.
              Create projects, write code, execute commands, preview apps,
              and deploy — without configuring a local environment.
            </p>

            <div className="mt-10 flex items-center justify-center gap-4">
              <Link
                href="/register"
                className="bg-primary-container text-on-primary-container hover:bg-primary-container/90 px-6 py-2.5 rounded text-sm font-medium transition-colors shadow-md flex items-center gap-2"
              >
                Start Building
                <svg
                  className="w-4 h-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
              <a
                href="#features"
                className="border border-outline-variant/50 text-on-surface-variant hover:text-on-surface hover:border-outline px-6 py-2.5 rounded text-sm transition-colors"
              >
                Learn More
              </a>
            </div>
          </div>
        </section>

        {/* ──── IDE Preview ──── */}
        <section className="max-w-7xl mx-auto px-6 pb-24">
          <div className="rounded-xl border border-outline-variant/30 bg-surface-container-low overflow-hidden shadow-2xl shadow-primary-container/5">
            {/* Window chrome - 3-column symmetric grid */}
            <div className="h-9 bg-surface-container-lowest grid grid-cols-3 items-center px-4 border-b border-outline-variant/20">
              <div className="flex items-center gap-1.5 justify-start">
                <div className="w-3 h-3 rounded-full bg-error/60" />
                <div className="w-3 h-3 rounded-full bg-[#f5a623]/60" />
                <div className="w-3 h-3 rounded-full bg-[#4cd964]/60" />
              </div>
              <div className="flex items-center justify-center">
                <div className="px-4 py-0.5 rounded bg-surface-container text-xs text-on-surface-variant font-mono">
                  RUNIX Cloud IDE — my-portfolio
                </div>
              </div>
              <div className="flex items-center justify-end text-[11px] font-mono text-outline">
                <span>🌿 main</span>
              </div>
            </div>

            {/* IDE body mockup */}
            <div className="flex h-[420px]">
              {/* Sidebar */}
              <div className="w-56 border-r border-outline-variant/20 bg-surface-container-lowest p-3 space-y-1.5 hidden md:block">
                <div className="text-xs text-on-surface-variant font-mono uppercase tracking-wider mb-3 px-1">
                  Explorer
                </div>
                {[
                  { name: "src/", indent: 0, isDir: true },
                  { name: "App.tsx", indent: 1, active: true },
                  { name: "main.tsx", indent: 1 },
                  { name: "index.css", indent: 1 },
                  { name: "components/", indent: 1, isDir: true },
                  { name: "public/", indent: 0, isDir: true },
                  { name: "package.json", indent: 0 },
                  { name: "tsconfig.json", indent: 0 },
                  { name: "vite.config.ts", indent: 0 },
                ].map((item, i) => (
                  <div
                    key={i}
                    className={`flex items-center gap-2 px-2 py-1 rounded text-xs font-mono transition-colors ${
                      item.active
                        ? "bg-primary-container/20 text-primary font-medium"
                        : "text-on-surface-variant hover:text-on-surface hover:bg-surface-container"
                    }`}
                    style={{ paddingLeft: `${item.indent * 12 + 8}px` }}
                  >
                    <span className="text-outline text-[11px]">
                      {item.isDir ? "📁" : "📄"}
                    </span>
                    <span>{item.name}</span>
                  </div>
                ))}
              </div>

              {/* Editor */}
              <div className="flex-1 bg-surface-container-low flex flex-col overflow-hidden">
                {/* Tabs */}
                <div className="flex border-b border-outline-variant/20 bg-surface-container-lowest text-xs font-mono">
                  <div className="px-4 py-2 bg-surface-container-low text-primary border-t-2 border-primary flex items-center gap-2">
                    <span>App.tsx</span>
                  </div>
                  <div className="px-4 py-2 text-on-surface-variant hover:text-on-surface flex items-center gap-2 cursor-pointer">
                    <span>main.tsx</span>
                  </div>
                </div>

                {/* Code with Line Numbers Gutter */}
                <div className="flex-1 p-4 font-mono text-xs overflow-auto flex gap-4">
                  {/* Line numbers gutter */}
                  <div className="select-none text-right text-outline/60 pr-3 border-r border-outline-variant/20 flex flex-col font-mono text-xs">
                    {Array.from({ length: 15 }, (_, i) => (
                      <div key={i} className="h-5 leading-5">{i + 1}</div>
                    ))}
                  </div>

                  {/* Code tokens */}
                  <div className="text-on-surface flex-1 flex flex-col font-mono text-xs">
                    <div className="h-5 leading-5"><span className="text-[#c792ea]">import</span> React <span className="text-[#c792ea]">from</span> <span className="text-[#c3e88d]">&apos;react&apos;</span>;</div>
                    <div className="h-5 leading-5"><span className="text-[#c792ea]">import</span> {"{ useState }"} <span className="text-[#c792ea]">from</span> <span className="text-[#c3e88d]">&apos;react&apos;</span>;</div>
                    <div className="h-5 leading-5">&nbsp;</div>
                    <div className="h-5 leading-5"><span className="text-[#c792ea]">export default function</span> <span className="text-[#82aaff]">App</span>() {"{"}</div>
                    <div className="h-5 leading-5">  <span className="text-[#c792ea]">const</span> [count, setCount] = <span className="text-[#82aaff]">useState</span>(<span className="text-[#f78c6c]">0</span>);</div>
                    <div className="h-5 leading-5">&nbsp;</div>
                    <div className="h-5 leading-5">  <span className="text-[#c792ea]">return</span> (</div>
                    <div className="h-5 leading-5">    &lt;<span className="text-[#f07178]">div</span> className=&quot;app&quot;&gt;</div>
                    <div className="h-5 leading-5">      &lt;<span className="text-[#f07178]">h1</span>&gt;<span className="text-[#c3e88d]">RUNIX Cloud IDE</span>&lt;/<span className="text-[#f07178]">h1</span>&gt;</div>
                    <div className="h-5 leading-5">      &lt;<span className="text-[#f07178]">button</span> <span className="text-[#c792ea]">onClick</span>={"{"}() =&gt; setCount(c =&gt; c + 1){"}"}&gt;</div>
                    <div className="h-5 leading-5">        Count is: {"{"}count{"}"}</div>
                    <div className="h-5 leading-5">      &lt;/<span className="text-[#f07178]">button</span>&gt;</div>
                    <div className="h-5 leading-5">    &lt;/<span className="text-[#f07178]">div</span>&gt;</div>
                    <div className="h-5 leading-5">  );</div>
                    <div className="h-5 leading-5">{"}"}</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Terminal bar */}
            <div className="h-28 border-t border-outline-variant/20 bg-surface-container-lowest p-3 font-mono text-xs">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-on-surface-variant">TERMINAL</span>
                <span className="text-outline">|</span>
                <span className="text-secondary text-[10px]">bash</span>
              </div>
              <div className="text-[#4cd964]">✓ Ready in 245ms</div>
              <div className="text-on-surface-variant">
                <span className="text-secondary">→</span> Local: http://localhost:5173
              </div>
              <div className="flex items-center mt-1">
                <span className="text-primary">$</span>
                <span className="ml-1.5 w-1.5 h-3.5 bg-primary animate-pulse" />
              </div>
            </div>
          </div>
        </section>

        {/* ──── Features Section ──── */}
        <section id="features" className="max-w-7xl mx-auto px-6 py-20">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-semibold text-on-surface tracking-tight">
              Everything You Need to Develop
            </h2>
            <p className="mt-3 text-on-surface-variant max-w-xl mx-auto">
              A complete cloud development environment with real runtime
              isolation, integrated terminal, and live preview.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {[
              {
                icon: "M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z",
                title: "Cloud IDE",
                desc: "Monaco editor with full syntax highlighting, IntelliSense, and multi-tab support.",
              },
              {
                icon: "M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4",
                title: "Isolated Runtimes",
                desc: "Each project runs in its own Docker container with CPU, memory, and storage limits.",
              },
              {
                icon: "M13 10V3L4 14h7v7l9-11h-7z",
                title: "Live Preview",
                desc: "See your application running in real-time through the integrated preview panel.",
              },
              {
                icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4",
                title: "Test Execution",
                desc: "Run tests inside your runtime and view results with structured output.",
              },
              {
                icon: "M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253",
                title: "Git & GitHub",
                desc: "Full Git integration with status, commit, push, pull, and GitHub repository import.",
              },
              {
                icon: "M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z",
                title: "Project Templates",
                desc: "React, Node.js, Python, MERN, and blank Docker — start coding in seconds.",
              },
            ].map((feature, i) => (
              <div
                key={i}
                className="p-5 rounded-xl bg-surface-container-low border border-outline-variant/20 hover:border-outline-variant/40 transition-colors flex flex-col justify-start group"
              >
                <div className="w-10 h-10 rounded-lg bg-surface-container-highest/60 flex items-center justify-center mb-4 group-hover:bg-primary-container/20 transition-colors">
                  <svg
                    className="w-5 h-5 text-on-surface-variant group-hover:text-primary transition-colors"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1.5}
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d={feature.icon} />
                  </svg>
                </div>
                <h3 className="font-semibold text-on-surface text-base mb-1.5">
                  {feature.title}
                </h3>
                <p className="text-xs text-on-surface-variant leading-relaxed">
                  {feature.desc}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* ──── CTA Section ──── */}
        <section className="max-w-7xl mx-auto px-6 pb-24">
          <div className="rounded-2xl bg-surface-container-low border border-outline-variant/20 p-12 text-center relative overflow-hidden">
            <div className="absolute -top-20 left-1/2 -translate-x-1/2 w-96 h-48 bg-primary-container/10 blur-[100px] rounded-full pointer-events-none" />
            <h2 className="text-2xl sm:text-3xl font-semibold text-on-surface tracking-tight relative">
              Ready to start building?
            </h2>
            <p className="mt-3 text-on-surface-variant max-w-md mx-auto text-sm relative">
              Create your free account and launch your first cloud workspace
              in under a minute.
            </p>
            <div className="mt-8 relative">
              <Link
                href="/register"
                className="inline-flex items-center gap-2 bg-primary-container text-on-primary-container hover:bg-primary-container/90 px-8 py-3 rounded text-sm font-semibold transition-colors shadow-lg shadow-primary-container/20"
              >
                Create Account
                <svg
                  className="w-4 h-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </Link>
            </div>
          </div>
        </section>
      </main>

      {/* ──── Footer ──── */}
      <footer className="border-t border-outline-variant/20 bg-surface-container-lowest">
        <div className="max-w-7xl mx-auto px-6 py-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-on-surface-variant">
          <div className="flex items-center gap-2.5">
            <div className="w-5 h-5 rounded bg-primary-container/30 flex items-center justify-center">
              <svg className="w-3 h-3 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <span className="font-semibold text-on-surface font-mono">RUNIX</span>
            <span className="text-outline">·</span>
            <span>Build. Run. Ship. Anywhere.</span>
          </div>

          <div className="flex items-center gap-6">
            <a href="#features" className="hover:text-on-surface transition-colors">
              Features
            </a>
            <Link href="/login" className="hover:text-on-surface transition-colors">
              Sign In
            </Link>
            <Link href="/register" className="hover:text-on-surface transition-colors">
              Register
            </Link>
            <span className="font-mono text-[10px] text-outline">v0.1.0</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
