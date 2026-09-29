"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api, setStoredToken } from "@/lib/api";

/**
 * RUNIX Developer Sign In Page
 * Implements Stitch Screen: RUNIX — Developer Sign In (e5837e279f004f5fa918ab1812f5f056)
 */
export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const data = await api.login({ email, password });
      setStoredToken(data.access_token);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Failed to sign in. Please verify your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-[#0f131b] text-[#dfe2ee] min-h-screen flex items-center justify-center p-3 font-sans selection:bg-[#4f46e5] selection:text-[#dad7ff]">
      <main className="w-full max-w-md mx-auto">
        <div className="relative w-full rounded-xl bg-[#181c24] border border-[#464555]/40 shadow-2xl p-6 overflow-hidden">
          {/* Subtle top ambient light glow */}
          <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-72 h-32 bg-[#4f46e5]/15 blur-3xl pointer-events-none rounded-full" />

          {/* Header Section */}
          <div className="relative flex flex-col mb-6">
            <div className="flex items-center justify-between">
              <Link href="/" className="flex items-center space-x-2 group">
                <div className="w-7 h-7 rounded bg-[#4f46e5] flex items-center justify-center text-white font-mono font-bold shadow-sm">
                  <span className="text-sm font-mono">&gt;_</span>
                </div>
                <span className="font-mono text-lg font-bold tracking-tight text-[#dfe2ee] group-hover:text-white transition-colors">
                  RUNIX
                </span>
              </Link>
              <div className="flex items-center space-x-1.5 px-2 py-0.5 rounded bg-[#31353e]/60 text-[#c7c4d8] font-mono text-xs">
                <span className="w-1.5 h-1.5 rounded-full bg-[#adc6ff]" />
                <span>v2.4.1-prod</span>
              </div>
            </div>

            <div className="pt-4">
              <h1 className="text-2xl font-bold text-[#dfe2ee] tracking-tight">
                Welcome back.
              </h1>
              <p className="text-xs text-[#c7c4d8] mt-1">
                Enter your developer credentials or sign in with your Git provider.
              </p>
            </div>
          </div>

          {/* Error Banner */}
          {error && (
            <div className="mb-4 p-2.5 rounded bg-[#93000a]/20 border border-[#ffb4ab]/30 text-[#ffb4ab] text-xs flex items-center gap-2">
              <span className="font-bold">Error:</span>
              <span>{error}</span>
            </div>
          )}

          {/* Primary Form */}
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="space-y-1">
              <div className="flex items-center justify-between">
                <label className="font-mono text-xs text-[#dfe2ee]" htmlFor="email">
                  Email Address
                </label>
                <span className="font-mono text-[11px] text-[#c7c4d8]/70">
                  user@domain.com
                </span>
              </div>
              <div className="relative flex items-center">
                <span className="absolute left-2.5 text-xs text-[#918fa1] pointer-events-none">
                  @
                </span>
                <input
                  id="email"
                  type="email"
                  required
                  placeholder="developer@runix.internal"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full h-9 pl-7 pr-3 rounded bg-[#1c2028] border border-[#464555]/60 text-[#dfe2ee] placeholder:text-[#918fa1] font-mono text-xs focus:outline-none focus:border-[#c3c0ff] focus:bg-[#262a33] transition-colors"
                />
              </div>
            </div>

            <div className="space-y-1">
              <div className="flex items-center justify-between">
                <label className="font-mono text-xs text-[#dfe2ee]" htmlFor="password">
                  Password
                </label>
                <a
                  href="#"
                  className="font-mono text-[11px] text-[#c3c0ff] hover:text-[#e2dfff] transition-colors"
                >
                  Forgot password?
                </a>
              </div>
              <div className="relative flex items-center">
                <span className="absolute left-2.5 text-xs text-[#918fa1] pointer-events-none">
                  🔒
                </span>
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  required
                  placeholder="••••••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full h-9 pl-7 pr-9 rounded bg-[#1c2028] border border-[#464555]/60 text-[#dfe2ee] placeholder:text-[#918fa1] font-mono text-xs focus:outline-none focus:border-[#c3c0ff] focus:bg-[#262a33] transition-colors"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-2 text-[#918fa1] hover:text-[#dfe2ee] text-xs p-1"
                >
                  {showPassword ? "hide" : "show"}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full h-9 mt-2 rounded bg-[#4f46e5] hover:bg-[#4f46e5]/90 active:bg-[#4f46e5]/80 text-[#dad7ff] font-mono text-xs font-semibold flex items-center justify-between px-3 transition-colors shadow-sm disabled:opacity-50"
            >
              <span>{loading ? "Authenticating..." : "Sign In"}</span>
              <span className="flex items-center space-x-1 px-1.5 py-0.5 rounded bg-black/30 text-[#dad7ff]/90 text-[10px]">
                <span>↵</span>
                <span>Enter</span>
              </span>
            </button>
          </form>

          {/* Visual Separator */}
          <div className="relative my-5 flex items-center justify-center">
            <div className="w-full h-[1px] bg-[#31353e]" />
            <span className="absolute bg-[#181c24] px-2 font-mono text-[10px] text-[#918fa1] uppercase tracking-wider">
              or verify via
            </span>
          </div>

          {/* Alternative Integrations */}
          <div className="space-y-2">
            <button
              type="button"
              onClick={() => {
                setEmail("demo@runix.internal");
                setPassword("Demopassword123!");
              }}
              className="w-full rounded bg-[#1c2028] hover:bg-[#262a33] border border-[#464555]/40 text-[#dfe2ee] p-2.5 transition-colors text-left flex items-start space-x-3 group"
            >
              <div className="w-7 h-7 rounded bg-[#31353e] flex items-center justify-center shrink-0 mt-0.5 group-hover:text-[#c3c0ff] transition-colors">
                <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
                  <path
                    fillRule="evenodd"
                    clipRule="evenodd"
                    d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                  />
                </svg>
              </div>
              <div className="flex flex-col min-w-0 flex-1">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-medium text-[#dfe2ee]">
                    Fill Demo Credentials
                  </span>
                  <span className="font-mono text-[10px] text-[#adc6ff]">
                    QUICK TEST
                  </span>
                </div>
                <span className="text-xs text-[#c7c4d8] truncate mt-0.5">
                  Load developer test account credentials
                </span>
              </div>
            </button>
          </div>

          {/* Security Micro-VM Banner */}
          <div className="mt-4 rounded bg-[#1c2028]/80 border border-[#464555]/30 p-2 flex items-center space-x-2.5">
            <div className="w-5 h-5 rounded-full bg-[#31353e] flex items-center justify-center shrink-0 text-[#a4c9ff] text-xs">
              🛡️
            </div>
            <p className="text-xs text-[#c7c4d8] leading-tight">
              Protected by end-to-end encrypted micro-VM sessions
            </p>
          </div>

          {/* Footer Register Prompt */}
          <div className="mt-4 pt-3 flex items-center justify-center text-xs text-[#c7c4d8]">
            <span>Don&apos;t have an account?</span>
            <Link
              href="/register"
              className="ml-1 text-[#c3c0ff] hover:text-[#e2dfff] transition-colors font-semibold"
            >
              Create one.
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
