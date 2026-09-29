"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

interface TemplateItem {
  id: string;
  name: string;
  description: string;
  language: string;
  framework: string;
  runtime: string;
  version: string;
  default_port: number | null;
  tags: string[];
}

/**
 * RUNIX New Workspace Creation Page
 * Implements Stitch Screen: RUNIX New Workspace Creation (984a073b74c94908b31407a4d4a88df7)
 */
export default function CreateProjectPage() {
  const router = useRouter();
  const [templates, setTemplates] = useState<TemplateItem[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string>("react-vite-ts");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [visibility, setVisibility] = useState<"private" | "public">("private");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadTemplates() {
      try {
        const data = await api.listTemplates();
        if (data.items && data.items.length > 0) {
          setTemplates(data.items);
          setSelectedTemplate(data.items[0].id);
        }
      } catch (err) {
        console.error("Failed to load templates from API:", err);
      }
    }
    loadTemplates();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;

    setError(null);
    setLoading(true);

    try {
      await api.createProject({
        name: name.trim(),
        description: description.trim() || undefined,
        template: selectedTemplate,
        visibility,
      });

      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Failed to create project.");
    } finally {
      setLoading(false);
    }
  };

  const currentTemplate = templates.find((t) => t.id === selectedTemplate);

  return (
    <div className="bg-[#0f131b] text-[#dfe2ee] min-h-screen font-sans antialiased selection:bg-[#4f46e5] selection:text-[#dad7ff]">
      {/* Top Navbar */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-[#0a0e16]/90 backdrop-blur-md border-b border-[#31353e]/40 shadow-sm">
        <div className="h-14 max-w-4xl mx-auto px-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className="flex items-center gap-2 group">
              <div className="w-6 h-6 rounded bg-[#4f46e5] flex items-center justify-center text-white font-mono text-xs font-bold">
                &gt;_
              </div>
              <span className="font-mono text-sm tracking-wider font-semibold text-[#dfe2ee] group-hover:text-white transition-colors">
                RUNIX
              </span>
            </Link>
            <span className="text-xs text-[#918fa1]">/</span>
            <span className="text-xs font-semibold text-[#dfe2ee]">
              Create Workspace
            </span>
          </div>

          <Link
            href="/dashboard"
            className="text-xs text-[#c7c4d8] hover:text-[#dfe2ee] transition-colors"
          >
            Cancel
          </Link>
        </div>
      </header>

      {/* Main Container */}
      <main className="w-full pt-20 px-6 pb-16 max-w-4xl mx-auto">
        <div className="mb-8">
          <div className="flex items-center gap-2 font-mono text-xs text-[#adc6ff] uppercase tracking-wider mb-1">
            <span>✨ Instant Provisioning</span>
            <span>•</span>
            <span>Micro-VM Isolation</span>
          </div>
          <h1 className="text-3xl font-bold text-[#dfe2ee] tracking-tight">
            Create a new workspace
          </h1>
          <p className="text-sm text-[#c7c4d8] mt-1">
            Choose a development template and configure your cloud container sandbox.
          </p>
        </div>

        {error && (
          <div className="mb-6 p-3 rounded-lg bg-[#93000a]/20 border border-[#ffb4ab]/30 text-[#ffb4ab] text-xs">
            <span className="font-bold">Error:</span> {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Step 1: Select Template */}
          <section className="space-y-3">
            <div className="flex items-center justify-between">
              <label className="font-mono text-xs uppercase tracking-wider text-[#dfe2ee] font-semibold">
                1. Select Starter Template
              </label>
              <span className="font-mono text-xs text-[#918fa1]">
                {templates.length} templates available
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {templates.map((tpl) => {
                const isSelected = tpl.id === selectedTemplate;
                return (
                  <div
                    key={tpl.id}
                    onClick={() => setSelectedTemplate(tpl.id)}
                    className={`p-4 rounded-xl border cursor-pointer transition-all flex flex-col justify-between gap-3 ${
                      isSelected
                        ? "bg-[#262a33] border-[#c3c0ff] shadow-md shadow-[#4f46e5]/10"
                        : "bg-[#181c24] border-[#31353e]/60 hover:border-[#464555] hover:bg-[#1c2028]"
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between mb-1.5">
                        <span className="font-bold text-sm text-[#dfe2ee]">
                          {tpl.name}
                        </span>
                        {isSelected && (
                          <span className="w-2 h-2 rounded-full bg-[#c3c0ff]" />
                        )}
                      </div>
                      <p className="text-xs text-[#c7c4d8] leading-relaxed">
                        {tpl.description}
                      </p>
                    </div>

                    <div className="flex items-center gap-2 font-mono text-[11px] text-[#918fa1] pt-2 border-t border-[#31353e]/40">
                      <span className="text-[#adc6ff]">{tpl.runtime}</span>
                      {tpl.default_port && (
                        <>
                          <span>•</span>
                          <span>Port :{tpl.default_port}</span>
                        </>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </section>

          {/* Step 2: Project Details */}
          <section className="space-y-4">
            <label className="block font-mono text-xs uppercase tracking-wider text-[#dfe2ee] font-semibold">
              2. Workspace Details
            </label>

            <div className="p-6 rounded-xl bg-[#181c24] border border-[#31353e]/60 space-y-4">
              <div className="space-y-1">
                <label className="font-mono text-xs text-[#dfe2ee]" htmlFor="projectName">
                  Project Name
                </label>
                <input
                  id="projectName"
                  type="text"
                  required
                  placeholder="e.g. portfolio-api or payment-service"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full h-10 px-3 rounded bg-[#1c2028] border border-[#464555]/60 text-[#dfe2ee] placeholder:text-[#918fa1] font-mono text-xs focus:outline-none focus:border-[#c3c0ff] focus:bg-[#262a33] transition-colors"
                />
              </div>

              <div className="space-y-1">
                <label className="font-mono text-xs text-[#dfe2ee]" htmlFor="projectDesc">
                  Description (optional)
                </label>
                <textarea
                  id="projectDesc"
                  rows={2}
                  placeholder="Short summary of what this project does..."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full p-3 rounded bg-[#1c2028] border border-[#464555]/60 text-[#dfe2ee] placeholder:text-[#918fa1] text-xs focus:outline-none focus:border-[#c3c0ff] focus:bg-[#262a33] transition-colors resize-none"
                />
              </div>

              <div className="space-y-2 pt-2">
                <label className="font-mono text-xs text-[#dfe2ee] block">
                  Visibility
                </label>
                <div className="flex gap-4">
                  <label className="flex items-center gap-2 cursor-pointer text-xs">
                    <input
                      type="radio"
                      name="visibility"
                      checked={visibility === "private"}
                      onChange={() => setVisibility("private")}
                      className="accent-[#4f46e5]"
                    />
                    <span>Private (only accessible by you)</span>
                  </label>
                  <label className="flex items-center gap-2 cursor-pointer text-xs">
                    <input
                      type="radio"
                      name="visibility"
                      checked={visibility === "public"}
                      onChange={() => setVisibility("public")}
                      className="accent-[#4f46e5]"
                    />
                    <span>Public (viewable by other developers)</span>
                  </label>
                </div>
              </div>
            </div>
          </section>

          {/* Submit Action */}
          <div className="flex items-center justify-between pt-4 border-t border-[#31353e]/40">
            <div className="flex items-center gap-2 text-xs text-[#918fa1] font-mono">
              <span>Target Runtime:</span>
              <span className="text-[#dfe2ee] font-semibold">
                {currentTemplate?.runtime || "RUNIX Sandboxed Engine"}
              </span>
            </div>

            <button
              type="submit"
              disabled={loading || !name.trim()}
              className="px-6 py-2.5 rounded bg-[#4f46e5] hover:bg-[#4f46e5]/90 active:bg-[#4f46e5]/80 text-white font-mono text-xs font-semibold transition-all shadow-md disabled:opacity-50 flex items-center gap-2"
            >
              <span>{loading ? "Provisioning Sandbox..." : "Create Workspace"}</span>
              <span>→</span>
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}
