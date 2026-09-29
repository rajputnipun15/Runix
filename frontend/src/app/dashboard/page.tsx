"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api, setStoredToken } from "@/lib/api";

interface ProjectItem {
  id: string;
  name: string;
  slug: string;
  template: string;
  visibility: string;
  status: string;
  updated_at: string;
}

/**
 * RUNIX Developer Dashboard
 * Implements Stitch Screen: RUNIX Developer Dashboard (a42d31e3c79a48a8a72729fc41fe4160)
 */
export default function DashboardPage() {
  const router = useRouter();
  const [projects, setProjects] = useState<ProjectItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<{ display_name: string; email: string } | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [meData, projectsData] = await Promise.all([
          api.getMe().catch(() => null),
          api.listProjects().catch(() => ({ items: [], total: 0 })),
        ]);

        if (meData) {
          setUser(meData);
        } else {
          // Fallback demo user for local exploration
          setUser({ display_name: "Developer", email: "developer@runix.internal" });
        }

        setProjects(projectsData.items || []);
      } catch (err) {
        console.error("Failed to load dashboard data:", err);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  const handleLogout = async () => {
    try {
      await api.logout();
    } catch {
      // ignore
    }
    setStoredToken(null);
    router.push("/login");
  };

  return (
    <div className="bg-[#0f131b] text-[#dfe2ee] min-h-screen font-sans antialiased selection:bg-[#4f46e5] selection:text-[#dad7ff]">
      {/* Top Navbar */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-[#0a0e16]/90 backdrop-blur-md border-b border-[#31353e]/40 shadow-sm">
        <div className="h-14 max-w-7xl mx-auto px-6 flex items-center justify-between gap-4">
          <div className="flex items-center gap-6">
            <Link href="/dashboard" className="flex items-center gap-2 group">
              <div className="w-6 h-6 rounded bg-[#4f46e5] flex items-center justify-center text-white font-mono text-xs font-bold">
                &gt;_
              </div>
              <span className="font-mono text-sm tracking-wider font-semibold text-[#dfe2ee] group-hover:text-white transition-colors">
                RUNIX
              </span>
              <span className="px-1.5 py-0.5 rounded bg-[#262a33] text-[#c7c4d8] font-mono text-[10px] uppercase">
                Cloud
              </span>
            </Link>

            <nav className="flex items-center gap-1 text-xs">
              <Link
                href="/dashboard"
                className="px-2.5 py-1.5 rounded bg-[#262a33] text-[#dfe2ee] font-semibold"
              >
                Projects
              </Link>
              <Link
                href="/projects/new"
                className="px-2.5 py-1.5 rounded text-[#c7c4d8] hover:text-[#dfe2ee] transition-colors"
              >
                Templates
              </Link>
            </nav>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-2 bg-[#181c24] px-3 py-1 rounded w-64 text-[#c7c4d8] border border-[#31353e]/40">
              <span className="text-xs text-[#918fa1]">🔍</span>
              <span className="text-xs flex-1 select-none text-[#918fa1]">
                Search workspaces...
              </span>
              <kbd className="font-mono text-[10px] px-1 py-0.5 rounded bg-[#31353e] text-[#c7c4d8]">
                ⌘K
              </kbd>
            </div>

            <div className="flex items-center gap-1.5 px-2 py-1 rounded bg-[#181c24] border border-[#31353e]/30">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="font-mono text-[11px] text-[#c7c4d8]">
                All systems operational
              </span>
            </div>

            <div className="flex items-center gap-2 pl-2">
              <div className="w-8 h-8 rounded-full bg-[#4f46e5]/30 border border-[#c3c0ff]/40 flex items-center justify-center font-mono text-xs text-[#c3c0ff] font-semibold">
                {user?.display_name ? user.display_name.charAt(0).toUpperCase() : "D"}
              </div>
              <button
                onClick={handleLogout}
                className="text-xs text-[#918fa1] hover:text-[#dfe2ee] transition-colors"
                title="Sign Out"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Page Body */}
      <main className="w-full pt-20 px-6 pb-12 max-w-7xl mx-auto">
        {/* Subtle Ambient Mesh */}
        <div className="relative w-full">
          <div className="absolute -top-16 left-1/4 w-96 h-96 bg-[#4f46e5]/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute -top-12 right-1/4 w-80 h-80 bg-[#0566d9]/10 rounded-full blur-3xl pointer-events-none" />
        </div>

        {/* Greeting & Header Context */}
        <section className="flex flex-col lg:flex-row lg:items-end justify-between gap-4 mb-8">
          <div className="flex flex-col gap-1 max-w-2xl">
            <div className="flex items-center gap-2 mb-1">
              <span className="font-mono text-xs text-[#c7c4d8] uppercase tracking-wider">
                Workspace ID: rnx-usr-{user?.display_name ? user.display_name.toLowerCase().slice(0, 4) : "dev"}
              </span>
              <span className="w-1 h-1 rounded-full bg-[#464555]" />
              <div className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-[#262a33]">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                <span className="font-mono text-xs text-[#adc6ff]">
                  99.99% Uptime
                </span>
              </div>
            </div>
            <h1 className="text-3xl font-bold text-[#dfe2ee] tracking-tight">
              Good day, <span className="text-[#c3c0ff]">{user?.display_name || "Developer"}</span>
            </h1>
            <p className="text-sm text-[#c7c4d8]">
              Continue building where you left off across your isolated cloud environments.
            </p>
          </div>

          {/* Action Cluster */}
          <div className="flex items-center gap-3 flex-wrap">
            <Link
              href="/projects/new"
              className="inline-flex items-center gap-2 px-4 py-2 rounded bg-[#4f46e5] hover:bg-[#4f46e5]/90 text-white font-mono text-xs font-semibold transition-all shadow-md"
            >
              <span>+</span>
              <span>New Project</span>
              <kbd className="px-1.5 py-0.5 rounded bg-black/30 text-white/90 text-[10px]">
                ⌘N
              </kbd>
            </Link>
          </div>
        </section>

        {/* Hardware & Metric Band */}
        <section className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-8">
          <div className="p-4 rounded-lg bg-[#181c24] border border-[#31353e]/40 flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#c7c4d8]">
              <span className="font-mono text-xs uppercase tracking-wider">
                Active Projects
              </span>
              <span className="text-sm text-[#918fa1]">📁</span>
            </div>
            <div className="mt-3 flex items-baseline gap-1.5">
              <span className="text-2xl font-bold text-[#dfe2ee]">{projects.length}</span>
              <span className="font-mono text-xs text-[#c7c4d8]">/ 8 allocated</span>
            </div>
            <div className="w-full bg-[#262a33] h-1.5 rounded mt-3 overflow-hidden">
              <div
                className="bg-[#c3c0ff] h-full rounded transition-all"
                style={{ width: `${Math.min(100, (projects.length / 8) * 100)}%` }}
              />
            </div>
          </div>

          <div className="p-4 rounded-lg bg-[#181c24] border border-[#31353e]/40 flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#c7c4d8]">
              <span className="font-mono text-xs uppercase tracking-wider">
                Container Runtimes
              </span>
              <span className="text-sm text-emerald-400">⚡</span>
            </div>
            <div className="mt-3 flex items-baseline gap-1.5">
              <span className="text-2xl font-bold text-[#dfe2ee]">
                {projects.filter((p) => p.status === "active").length}
              </span>
              <span className="font-mono text-xs text-emerald-400">ready</span>
            </div>
            <div className="w-full bg-[#262a33] h-1.5 rounded mt-3 overflow-hidden">
              <div className="bg-emerald-400 h-full rounded" style={{ width: "100%" }} />
            </div>
          </div>

          <div className="p-4 rounded-lg bg-[#181c24] border border-[#31353e]/40 flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#c7c4d8]">
              <span className="font-mono text-xs uppercase tracking-wider">
                Memory Quota
              </span>
              <span className="text-sm text-[#adc6ff]">🧠</span>
            </div>
            <div className="mt-3 flex items-baseline gap-1.5">
              <span className="text-2xl font-bold text-[#dfe2ee]">1.0</span>
              <span className="font-mono text-xs text-[#c7c4d8]">GB / 8 GB</span>
            </div>
            <div className="w-full bg-[#262a33] h-1.5 rounded mt-3 overflow-hidden">
              <div className="bg-[#0566d9] h-full rounded" style={{ width: "12.5%" }} />
            </div>
          </div>

          <div className="p-4 rounded-lg bg-[#181c24] border border-[#31353e]/40 flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#c7c4d8]">
              <span className="font-mono text-xs uppercase tracking-wider">
                Platform Health
              </span>
              <span className="text-sm text-emerald-400">✓</span>
            </div>
            <div className="mt-3 flex items-baseline gap-1.5">
              <span className="text-2xl font-bold text-[#dfe2ee]">100%</span>
              <span className="font-mono text-xs text-[#c7c4d8]">Healthy</span>
            </div>
            <div className="w-full bg-[#262a33] h-1.5 rounded mt-3 overflow-hidden">
              <div className="bg-emerald-500 h-full rounded" style={{ width: "100%" }} />
            </div>
          </div>
        </section>

        {/* Projects Shelf */}
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#4f46e5] animate-pulse" />
              <h2 className="text-lg font-semibold text-[#dfe2ee]">
                Active Workspaces
              </h2>
              <span className="px-2 py-0.5 rounded bg-[#262a33] font-mono text-xs text-[#c7c4d8]">
                {projects.length} total
              </span>
            </div>
            <span className="font-mono text-xs text-[#918fa1]">
              Isolated sandbox containers • Zero idle spinup
            </span>
          </div>

          {loading ? (
            <div className="p-12 text-center text-sm text-[#918fa1] font-mono">
              Loading workspaces...
            </div>
          ) : projects.length === 0 ? (
            <div className="p-12 rounded-xl bg-[#181c24] border border-[#31353e]/40 text-center flex flex-col items-center justify-center">
              <div className="w-12 h-12 rounded-xl bg-[#262a33] flex items-center justify-center text-2xl text-[#c3c0ff] mb-4">
                ⚡
              </div>
              <h3 className="text-base font-semibold text-[#dfe2ee] mb-1">
                No active workspaces yet
              </h3>
              <p className="text-xs text-[#c7c4d8] max-w-sm mb-6">
                Create a new project from one of our pre-configured templates (React, Node, FastAPI, MERN) to get started immediately.
              </p>
              <Link
                href="/projects/new"
                className="px-4 py-2 rounded bg-[#4f46e5] hover:bg-[#4f46e5]/90 text-white font-mono text-xs font-semibold transition-colors"
              >
                + Create First Project
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {projects.map((project) => (
                <div
                  key={project.id}
                  className="p-5 rounded-lg bg-[#181c24] hover:bg-[#1c2028] border border-[#31353e]/40 hover:border-[#c3c0ff]/30 transition-all flex flex-col justify-between gap-4 shadow-sm group"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-[#dfe2ee] text-base group-hover:text-[#c3c0ff] transition-colors">
                          {project.name}
                        </span>
                        <span className="px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono text-[10px]">
                          {project.status}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 font-mono text-xs text-[#c7c4d8] mt-1">
                        <span>{project.template}</span>
                        <span>•</span>
                        <span className="text-[#918fa1]">{project.visibility}</span>
                      </div>
                    </div>
                    <span className="text-xs text-[#918fa1] font-mono">
                      {new Date(project.updated_at).toLocaleDateString()}
                    </span>
                  </div>

                  <div className="pt-2 border-t border-[#31353e]/40 flex items-center justify-between">
                    <span className="font-mono text-xs text-[#918fa1]">
                      id: {project.id.slice(0, 8)}...
                    </span>
                    <Link
                      href={`/workspace/${project.id}`}
                      className="px-3 py-1 rounded bg-[#262a33] hover:bg-[#4f46e5] text-[#dfe2ee] hover:text-white font-mono text-xs font-semibold transition-colors flex items-center gap-1.5"
                    >
                      <span>Open Workspace</span>
                      <span>→</span>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
