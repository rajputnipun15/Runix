"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api, setStoredToken } from "@/lib/api";

/**
 * RUNIX Developer Registration Page
 */
export default function RegisterPage() {
  const router = useRouter();
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await api.register({
        email,
        password,
        display_name: displayName,
      });

      // Automatically login after successful registration
      const loginData = await api.login({ email, password });
      setStoredToken(loginData.access_token);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Failed to create account. Please try again.");
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
                Create account.
              </h1>
              <p className="text-xs text-[#c7c4d8] mt-1">
                Spin up instant cloud developer environments in seconds.
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
              <label className="font-mono text-xs text-[#dfe2ee]" htmlFor="displayName">
                Display Name
              </label>
              <input
                id="displayName"
                type="text"
                required
                placeholder="Ada Lovelace"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                className="w-full h-9 px-3 rounded bg-[#1c2028] border border-[#464555]/60 text-[#dfe2ee] placeholder:text-[#918fa1] font-mono text-xs focus:outline-none focus:border-[#c3c0ff] focus:bg-[#262a33] transition-colors"
              />
            </div>

            <div className="space-y-1">
              <label className="font-mono text-xs text-[#dfe2ee]" htmlFor="email">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                required
                placeholder="developer@runix.internal"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full h-9 px-3 rounded bg-[#1c2028] border border-[#464555]/60 text-[#dfe2ee] placeholder:text-[#918fa1] font-mono text-xs focus:outline-none focus:border-[#c3c0ff] focus:bg-[#262a33] transition-colors"
              />
            </div>

            <div className="space-y-1">
              <label className="font-mono text-xs text-[#dfe2ee]" htmlFor="password">
                Password (min 8 chars)
              </label>
              <input
                id="password"
                type="password"
                required
                minLength={8}
                placeholder="••••••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full h-9 px-3 rounded bg-[#1c2028] border border-[#464555]/60 text-[#dfe2ee] placeholder:text-[#918fa1] font-mono text-xs focus:outline-none focus:border-[#c3c0ff] focus:bg-[#262a33] transition-colors"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full h-9 mt-2 rounded bg-[#4f46e5] hover:bg-[#4f46e5]/90 active:bg-[#4f46e5]/80 text-[#dad7ff] font-mono text-xs font-semibold flex items-center justify-between px-3 transition-colors shadow-sm disabled:opacity-50"
            >
              <span>{loading ? "Creating Account..." : "Create Account"}</span>
              <span className="flex items-center space-x-1 px-1.5 py-0.5 rounded bg-black/30 text-[#dad7ff]/90 text-[10px]">
                <span>↵</span>
                <span>Enter</span>
              </span>
            </button>
          </form>

          {/* Footer Sign In Prompt */}
          <div className="mt-5 pt-3 flex items-center justify-center text-xs text-[#c7c4d8] border-t border-[#31353e]">
            <span>Already have an account?</span>
            <Link
              href="/login"
              className="ml-1 text-[#c3c0ff] hover:text-[#e2dfff] transition-colors font-semibold"
            >
              Sign In.
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
