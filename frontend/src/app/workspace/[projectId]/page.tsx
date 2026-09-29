"use client";

import { useEffect, useState, use, useCallback, useRef } from "react";
import Link from "next/link";
import { api } from "@/lib/api";

interface FileItem {
  path: string;
  type: "file" | "directory";
  size_bytes?: number;
}

interface OpenTab {
  path: string;
  content: string;
  originalContent: string;
  isDirty: boolean;
}

/**
 * RUNIX Cloud IDE Workspace
 * Implements Stitch Screen: RUNIX Cloud IDE - Browser Workspace (ff9274589d334fffbba97dfdec1f63e2)
 */
export default function WorkspacePage({
  params,
}: {
  params: Promise<{ projectId: string }>;
}) {
  const resolvedParams = use(params);
  const projectId = resolvedParams.projectId;

  const [project, setProject] = useState<any>(null);
  const [files, setFiles] = useState<FileItem[]>([]);
  const [openTabs, setOpenTabs] = useState<OpenTab[]>([]);
  const [activeTabPath, setActiveTabPath] = useState<string | null>(null);
  const [bottomTab, setBottomTab] = useState<"terminal" | "output" | "preview">("terminal");
  const [terminalLogs, setTerminalLogs] = useState<string[]>([
    "⚡ RUNIX Cloud IDE Workspace Terminal v2.4.1",
    "Isolated workspace environment initialized.",
    "Type commands (e.g. ls, cat package.json, npm run dev, help, clear).",
  ]);
  const [commandInput, setCommandInput] = useState("");
  const [commandHistory, setCommandHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState<number>(-1);
  const [isExecuting, setIsExecuting] = useState(false);
  const [wsConnected, setWsConnected] = useState(false);
  const [saving, setSaving] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string>("Ready");
  const [newFileInput, setNewFileInput] = useState("");
  const [showNewFileModal, setShowNewFileModal] = useState(false);

  const wsRef = useRef<WebSocket | null>(null);
  const terminalBottomRef = useRef<HTMLDivElement | null>(null);

  // Load project metadata & file tree
  const loadFiles = useCallback(async () => {
    try {
      const res = await api.listFiles(projectId);
      setFiles(res.items || []);
    } catch (err) {
      console.error("Failed to load files:", err);
    }
  }, [projectId]);

  useEffect(() => {
    async function init() {
      try {
        const [proj] = await Promise.all([
          api.getProject(projectId).catch(() => ({
            name: "Cloud Workspace",
            slug: "cloud-workspace",
            template: "react-vite-ts",
          })),
          loadFiles(),
        ]);
        setProject(proj);
      } catch (err) {
        console.error("Init failed:", err);
      }
    }
    init();
  }, [projectId, loadFiles]);

  // Open file into editor tab
  const handleOpenFile = async (path: string) => {
    // If already open, switch to it
    const existing = openTabs.find((t) => t.path === path);
    if (existing) {
      setActiveTabPath(path);
      return;
    }

    try {
      setStatusMessage(`Reading ${path}...`);
      const fileData = await api.readFile(projectId, path);
      const newTab: OpenTab = {
        path,
        content: fileData.content,
        originalContent: fileData.content,
        isDirty: false,
      };
      setOpenTabs((prev) => [...prev, newTab]);
      setActiveTabPath(path);
      setStatusMessage("Ready");
    } catch (err: any) {
      setStatusMessage(`Error: ${err.message}`);
    }
  };

  // Close tab
  const handleCloseTab = (path: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const updated = openTabs.filter((t) => t.path !== path);
    setOpenTabs(updated);
    if (activeTabPath === path) {
      setActiveTabPath(updated.length > 0 ? updated[updated.length - 1].path : null);
    }
  };

  // Content change
  const handleContentChange = (newContent: string) => {
    if (!activeTabPath) return;
    setOpenTabs((prev) =>
      prev.map((tab) =>
        tab.path === activeTabPath
          ? {
              ...tab,
              content: newContent,
              isDirty: newContent !== tab.originalContent,
            }
          : tab
      )
    );
  };

  // Save current file
  const handleSave = async () => {
    const current = openTabs.find((t) => t.path === activeTabPath);
    if (!current || !current.isDirty) return;

    setSaving(true);
    setStatusMessage(`Saving ${current.path}...`);
    try {
      await api.writeFile(projectId, current.path, current.content);
      setOpenTabs((prev) =>
        prev.map((t) =>
          t.path === current.path
            ? { ...t, originalContent: t.content, isDirty: false }
            : t
        )
      );
      setStatusMessage("Saved successfully");
      setTimeout(() => setStatusMessage("Ready"), 2000);
    } catch (err: any) {
      setStatusMessage(`Save failed: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  // Create new file
  const handleCreateFile = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFileInput.trim()) return;

    try {
      await api.writeFile(projectId, newFileInput.trim(), "// New file created in RUNIX\n");
      setShowNewFileModal(false);
      const createdPath = newFileInput.trim();
      setNewFileInput("");
      await loadFiles();
      await handleOpenFile(createdPath);
    } catch (err: any) {
      alert(`Error creating file: ${err.message}`);
    }
  };

  // Terminal WebSocket lifecycle
  useEffect(() => {
    if (!projectId) return;

    let isSubscribed = true;
    let ws: WebSocket | null = null;
    let reconnectTimer: any = null;

    const connectWs = () => {
      if (!isSubscribed) return;
      try {
        const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
        const host = window.location.hostname || "localhost";
        const wsUrl = `${protocol}//${host}:8000/ws/projects/${projectId}/terminal`;
        ws = new WebSocket(wsUrl);
        wsRef.current = ws;

        ws.onopen = () => {
          if (!isSubscribed) return;
          setWsConnected(true);
        };

        ws.onmessage = (event) => {
          if (!isSubscribed) return;
          try {
            const msg = JSON.parse(event.data);
            if (msg.type === "output" && msg.data) {
              const cleaned = msg.data.replace(/\x1b\[[0-9;]*[a-zA-Z]/g, "").replace(/\r/g, "");
              const lines = cleaned.split("\n").filter((l: string, idx: number, arr: string[]) => idx < arr.length - 1 || l.length > 0);
              setTerminalLogs((prev) => [...prev, ...lines]);
            } else if (msg.type === "clear") {
              setTerminalLogs([]);
            } else if (msg.type === "exit") {
              setIsExecuting(false);
              loadFiles();
            } else if (msg.type === "error" && msg.data) {
              setTerminalLogs((prev) => [...prev, `[error] ${msg.data}`]);
              setIsExecuting(false);
            }
          } catch {
            setTerminalLogs((prev) => [...prev, event.data]);
          }
        };

        ws.onclose = () => {
          if (!isSubscribed) return;
          setWsConnected(false);
          reconnectTimer = setTimeout(connectWs, 3000);
        };

        ws.onerror = (err) => {
          console.warn("Terminal WebSocket error:", err);
          if (ws) ws.close();
        };
      } catch (err) {
        console.warn("Failed to create WS connection:", err);
      }
    };

    connectWs();

    return () => {
      isSubscribed = false;
      if (reconnectTimer) clearTimeout(reconnectTimer);
      if (ws) ws.close();
      wsRef.current = null;
    };
  }, [projectId, loadFiles]);

  // Terminal Auto-Scroll
  useEffect(() => {
    if (bottomTab === "terminal" && terminalBottomRef.current) {
      terminalBottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [terminalLogs, bottomTab]);

  // Execute command via WebSocket or REST fallback
  const handleExecuteCommandString = async (cmd: string) => {
    if (!cmd.trim() || isExecuting) return;
    const trimmed = cmd.trim();

    setCommandHistory((prev) => [...prev, trimmed]);
    setHistoryIndex(-1);
    setTerminalLogs((prev) => [...prev, `runix@sandbox:~$ ${trimmed}`]);

    if (trimmed === "clear" || trimmed === "cls") {
      setTerminalLogs([]);
      return;
    }

    setIsExecuting(true);

    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: "input", data: trimmed }));
    } else {
      try {
        const res = await api.executeCommand(projectId, trimmed);
        if (res.stdout) {
          const lines = res.stdout.replace(/\r/g, "").split("\n").filter((l, idx, arr) => idx < arr.length - 1 || l.length > 0);
          setTerminalLogs((prev) => [...prev, ...lines]);
        }
        if (res.stderr) {
          const lines = res.stderr.replace(/\r/g, "").split("\n").filter((l, idx, arr) => idx < arr.length - 1 || l.length > 0);
          setTerminalLogs((prev) => [...prev, ...lines]);
        }
        if (res.exit_code !== 0 && !res.stderr && !res.stdout) {
          setTerminalLogs((prev) => [...prev, `Process exited with code ${res.exit_code}`]);
        }
      } catch (err: any) {
        setTerminalLogs((prev) => [...prev, `Command failed: ${err.message}`]);
      } finally {
        setIsExecuting(false);
        loadFiles();
      }
    }
  };

  const handleRunCommand = (e: React.FormEvent) => {
    e.preventDefault();
    if (!commandInput.trim()) return;
    const cmd = commandInput;
    setCommandInput("");
    handleExecuteCommandString(cmd);
  };

  const handleTerminalKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "ArrowUp") {
      e.preventDefault();
      if (commandHistory.length === 0) return;
      const nextIndex = historyIndex === -1 ? commandHistory.length - 1 : Math.max(0, historyIndex - 1);
      setHistoryIndex(nextIndex);
      setCommandInput(commandHistory[nextIndex]);
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      if (historyIndex === -1) return;
      const nextIndex = historyIndex + 1;
      if (nextIndex >= commandHistory.length) {
        setHistoryIndex(-1);
        setCommandInput("");
      } else {
        setHistoryIndex(nextIndex);
        setCommandInput(commandHistory[nextIndex]);
      }
    }
  };

  // Keyboard shortcut listener (Cmd+S / Ctrl+S)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "s") {
        e.preventDefault();
        handleSave();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  });

  const activeTab = openTabs.find((t) => t.path === activeTabPath);

  return (
    <div className="bg-[#0f131b] text-[#dfe2ee] h-screen w-screen flex flex-col font-sans select-none overflow-hidden antialiased">
      {/* Top Header / Context Bar */}
      <header className="h-12 bg-[#0a0e16] border-b border-[#31353e]/40 px-3 flex items-center justify-between text-xs shrink-0 z-40">
        <div className="flex items-center gap-3">
          <Link href="/dashboard" className="flex items-center gap-2 group">
            <div className="w-6 h-6 rounded bg-[#4f46e5] flex items-center justify-center text-white font-mono text-xs font-bold">
              &gt;_
            </div>
            <span className="font-mono text-sm tracking-wider font-semibold text-[#dfe2ee] group-hover:text-white transition-colors">
              RUNIX
            </span>
          </Link>

          <span className="text-[#918fa1]">/</span>

          <div className="flex items-center gap-1.5 font-mono">
            <span className="font-semibold text-[#dfe2ee]">
              {project?.name || "Workspace"}
            </span>
            <span className="text-[#918fa1]">({project?.template || "react-vite-ts"})</span>
          </div>

          <div className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#181c24] text-[11px] font-mono text-[#adc6ff] border border-[#31353e]/40">
            <span>🌿</span>
            <span>main</span>
          </div>

          <div className="hidden md:flex items-center gap-1.5 px-2 py-0.5 rounded bg-[#181c24] text-[11px] font-mono border border-[#31353e]/40">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-[#c7c4d8]">Runtime Online (Port 5173)</span>
          </div>
        </div>

        {/* Quick Action Toolbar */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleSave}
            disabled={saving || !activeTab?.isDirty}
            className={`h-7 px-3 rounded font-mono text-xs flex items-center gap-1.5 transition-colors ${
              activeTab?.isDirty
                ? "bg-[#4f46e5] hover:bg-[#4f46e5]/90 text-white font-semibold"
                : "bg-[#1c2028] text-[#918fa1] cursor-default"
            }`}
          >
            <span>💾</span>
            <span>{saving ? "Saving..." : activeTab?.isDirty ? "Save *" : "Saved"}</span>
            <kbd className="text-[10px] opacity-70">⌘S</kbd>
          </button>

          <button
            onClick={() => {
              setBottomTab("terminal");
              handleExecuteCommandString("npm run dev");
            }}
            className="h-7 px-3 rounded bg-[#1c2028] hover:bg-[#262a33] text-emerald-400 font-mono text-xs flex items-center gap-1 transition-colors border border-[#31353e]/40"
          >
            <span>▶</span>
            <span>Run</span>
          </button>

          <button
            onClick={() => setBottomTab("preview")}
            className={`h-7 px-3 rounded font-mono text-xs flex items-center gap-1 transition-colors border border-[#31353e]/40 ${
              bottomTab === "preview"
                ? "bg-[#262a33] text-[#c3c0ff] border-[#c3c0ff]/40"
                : "bg-[#1c2028] hover:bg-[#262a33] text-[#dfe2ee]"
            }`}
          >
            <span>🌐</span>
            <span>Preview</span>
          </button>

          <Link
            href="/dashboard"
            className="h-7 px-2.5 rounded bg-[#1c2028] hover:bg-[#262a33] text-[#c7c4d8] font-mono text-xs flex items-center transition-colors border border-[#31353e]/40"
            title="Exit to Dashboard"
          >
            ✕
          </Link>
        </div>
      </header>

      {/* Main Workspace Body */}
      <div className="flex-1 flex overflow-hidden w-full">
        {/* Left Sidebar Activity Bar */}
        <aside className="w-11 bg-[#0a0e16] border-r border-[#31353e]/40 flex flex-col items-center py-2 justify-between shrink-0">
          <div className="flex flex-col items-center gap-2">
            <button
              className="w-8 h-8 rounded bg-[#262a33] text-[#c3c0ff] flex items-center justify-center text-sm shadow-sm"
              title="Files Explorer"
            >
              📁
            </button>
            <button
              className="w-8 h-8 rounded hover:bg-[#1c2028] text-[#918fa1] hover:text-[#dfe2ee] flex items-center justify-center text-sm transition-colors"
              title="Search Workspace"
            >
              🔍
            </button>
            <button
              className="w-8 h-8 rounded hover:bg-[#1c2028] text-[#918fa1] hover:text-[#dfe2ee] flex items-center justify-center text-sm transition-colors"
              title="Git Source Control"
            >
              🌿
            </button>
          </div>

          <div className="flex flex-col items-center gap-2">
            <button
              onClick={() => setBottomTab(bottomTab === "terminal" ? "preview" : "terminal")}
              className="w-8 h-8 rounded hover:bg-[#1c2028] text-[#918fa1] hover:text-[#dfe2ee] flex items-center justify-center text-sm transition-colors"
              title="Terminal Panel"
            >
              &gt;_
            </button>
          </div>
        </aside>

        {/* Panel 1: File Explorer */}
        <section className="w-60 bg-[#181c24] border-r border-[#31353e]/40 flex flex-col justify-between shrink-0 overflow-hidden">
          <div className="flex flex-col flex-1 overflow-y-auto">
            {/* Header */}
            <div className="h-8 px-3 flex items-center justify-between bg-[#1c2028] text-[#c7c4d8] font-mono text-[11px] uppercase tracking-wider border-b border-[#31353e]/30">
              <span className="font-semibold text-xs">Explorer</span>
              <div className="flex items-center gap-1 text-[#918fa1]">
                <button
                  onClick={() => setShowNewFileModal(true)}
                  className="hover:text-[#dfe2ee] p-1"
                  title="New File"
                >
                  +
                </button>
                <button
                  onClick={loadFiles}
                  className="hover:text-[#dfe2ee] p-1"
                  title="Refresh"
                >
                  ↻
                </button>
              </div>
            </div>

            {/* Tree */}
            <div className="py-2 text-xs font-mono">
              <div className="px-3 py-1 font-semibold text-[#dfe2ee] flex items-center gap-1.5 opacity-80">
                <span>📦</span>
                <span>{project?.name || "root"}</span>
              </div>

              {files.map((file) => {
                const isOpen = activeTabPath === file.path;
                return (
                  <div
                    key={file.path}
                    onClick={() => {
                      if (file.type === "file") {
                        handleOpenFile(file.path);
                      }
                    }}
                    className={`px-6 py-1 cursor-pointer flex items-center justify-between transition-colors ${
                      isOpen
                        ? "bg-[#262a33] text-[#c3c0ff] font-semibold"
                        : "text-[#c7c4d8] hover:bg-[#1c2028] hover:text-[#dfe2ee]"
                    }`}
                  >
                    <div className="flex items-center gap-2 truncate">
                      <span>{file.type === "directory" ? "📁" : "📄"}</span>
                      <span className="truncate">{file.path}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Explorer Bottom Shelf */}
          <div className="p-2 border-t border-[#31353e]/40 bg-[#141820] text-[10px] font-mono text-[#918fa1] flex items-center justify-between">
            <span>{files.length} items</span>
            <span>UTF-8</span>
          </div>
        </section>

        {/* Center Panel: Code Editor + Tabs + Terminal */}
        <div className="flex-1 flex flex-col min-w-0 bg-[#0f131b] overflow-hidden">
          {/* Editor Tab Bar */}
          <div className="h-9 bg-[#141820] border-b border-[#31353e]/40 flex items-center overflow-x-auto text-xs shrink-0">
            {openTabs.map((tab) => {
              const isActive = activeTabPath === tab.path;
              return (
                <div
                  key={tab.path}
                  onClick={() => setActiveTabPath(tab.path)}
                  className={`h-full px-4 flex items-center gap-2 cursor-pointer font-mono border-r border-[#31353e]/30 transition-colors ${
                    isActive
                      ? "bg-[#181c24] text-[#dfe2ee] border-t-2 border-t-[#c3c0ff]"
                      : "text-[#918fa1] hover:text-[#dfe2ee] hover:bg-[#181c24]/50"
                  }`}
                >
                  <span>📄</span>
                  <span>{tab.path}</span>
                  {tab.isDirty && <span className="w-1.5 h-1.5 rounded-full bg-[#c3c0ff]" />}
                  <button
                    onClick={(e) => handleCloseTab(tab.path, e)}
                    className="ml-1 text-[#918fa1] hover:text-white text-xs"
                  >
                    ×
                  </button>
                </div>
              );
            })}
          </div>

          {/* Active File Editor Area */}
          <div className="flex-1 relative flex overflow-hidden bg-[#10141d]">
            {activeTab ? (
              <div className="flex-1 flex overflow-hidden">
                {/* Line Numbers Gutter */}
                <div className="select-none text-right text-[#918fa1]/40 py-4 pl-3 pr-3 font-mono text-sm leading-relaxed border-r border-[#31353e]/30 bg-[#0c1017] min-w-[3.2rem]">
                  {Array.from(
                    { length: Math.max(activeTab.content.split("\n").length, 1) },
                    (_, i) => (
                      <div key={i}>{i + 1}</div>
                    )
                  )}
                </div>
                {/* Editor Textarea */}
                <textarea
                  value={activeTab.content}
                  onChange={(e) => handleContentChange(e.target.value)}
                  spellCheck={false}
                  className="w-full flex-1 p-4 bg-transparent text-[#dfe2ee] font-mono text-sm leading-relaxed outline-none resize-none selection:bg-[#4f46e5]/40 overflow-auto"
                />
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-center p-6">
                <div className="w-12 h-12 rounded-xl bg-[#1c2028] flex items-center justify-center text-2xl text-[#c3c0ff] mb-3">
                  ⚡
                </div>
                <h3 className="text-sm font-semibold text-[#dfe2ee]">
                  No file selected
                </h3>
                <p className="text-xs text-[#918fa1] mt-1 max-w-xs">
                  Select a file from the explorer on the left or create a new file to start coding.
                </p>
              </div>
            )}
          </div>

          {/* Bottom Dock / Drawer (Terminal, Output, Live Preview) */}
          <div className="h-56 bg-[#0a0e16] border-t border-[#31353e]/50 flex flex-col shrink-0">
            {/* Drawer Tabs */}
            <div className="h-8 px-3 bg-[#141820] border-b border-[#31353e]/30 flex items-center gap-4 text-xs font-mono">
              <button
                onClick={() => setBottomTab("terminal")}
                className={`flex items-center gap-1.5 transition-colors ${
                  bottomTab === "terminal" ? "text-[#c3c0ff] font-semibold" : "text-[#918fa1] hover:text-[#dfe2ee]"
                }`}
              >
                <span>&gt;_</span>
                <span>Terminal</span>
              </button>

              <button
                onClick={() => setBottomTab("preview")}
                className={`flex items-center gap-1.5 transition-colors ${
                  bottomTab === "preview" ? "text-[#c3c0ff] font-semibold" : "text-[#918fa1] hover:text-[#dfe2ee]"
                }`}
              >
                <span>🌐</span>
                <span>Live Preview (Port 5173)</span>
              </button>

              <div className="ml-auto text-[11px] text-[#918fa1]">
                Status: <span className="text-[#dfe2ee]">{statusMessage}</span>
              </div>
            </div>

            {/* Drawer Content */}
            <div className="flex-1 overflow-hidden p-3 font-mono text-xs">
              {bottomTab === "terminal" ? (
                <div className="h-full flex flex-col">
                  <div className="flex-1 overflow-y-auto space-y-1 text-[#c7c4d8] font-mono select-text">
                    {terminalLogs.map((log, idx) => (
                      <div key={idx} className="leading-relaxed whitespace-pre-wrap break-all">
                        {log}
                      </div>
                    ))}
                    {isExecuting && (
                      <div className="text-amber-400/80 animate-pulse text-xs flex items-center gap-2">
                        <span>⚙</span>
                        <span>Running command...</span>
                      </div>
                    )}
                    <div ref={terminalBottomRef} />
                  </div>

                  <form onSubmit={handleRunCommand} className="mt-2 flex items-center gap-2 border-t border-[#31353e]/40 pt-2">
                    <span className="text-emerald-400 font-bold shrink-0">runix@sandbox:~$</span>
                    <input
                      type="text"
                      value={commandInput}
                      onChange={(e) => setCommandInput(e.target.value)}
                      onKeyDown={handleTerminalKeyDown}
                      placeholder={isExecuting ? "Executing command..." : "Try: ls, cat package.json, python, npm run dev, clear"}
                      disabled={isExecuting}
                      className="flex-1 bg-transparent text-[#dfe2ee] outline-none placeholder:text-[#464555] font-mono text-xs"
                    />
                    <div className="flex items-center gap-1.5 px-2 py-0.5 rounded bg-[#141820] text-[10px] text-[#918fa1] border border-[#31353e]/30">
                      <span className={`w-1.5 h-1.5 rounded-full ${wsConnected ? "bg-emerald-400 animate-pulse" : "bg-amber-400"}`} />
                      <span>{wsConnected ? "WS Live" : "REST"}</span>
                    </div>
                  </form>
                </div>
              ) : (
                <div className="h-full w-full rounded bg-[#0f131b] border border-[#31353e]/40 flex flex-col items-center justify-center p-6 text-center">
                  <div className="w-10 h-10 rounded bg-[#4f46e5]/20 text-[#c3c0ff] flex items-center justify-center text-xl mb-2">
                    ⚡
                  </div>
                  <h4 className="text-sm font-semibold text-[#dfe2ee]">
                    Live Preview Active on :5173
                  </h4>
                  <p className="text-xs text-[#918fa1] max-w-md mt-1 mb-4">
                    Your application preview is isolated and tunneled securely through the RUNIX preview gateway.
                  </p>
                  <div className="px-4 py-2 rounded bg-[#1c2028] border border-[#31353e] text-xs font-mono text-emerald-400">
                    HTTP 200 OK • Sandbox container running
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* New File Modal */}
      {showNewFileModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="w-full max-w-sm rounded-xl bg-[#181c24] border border-[#464555] p-5 shadow-2xl">
            <h3 className="text-sm font-bold text-[#dfe2ee] mb-2 font-mono">
              Create New File
            </h3>
            <form onSubmit={handleCreateFile}>
              <input
                type="text"
                required
                placeholder="e.g. src/utils.ts or test.js"
                value={newFileInput}
                onChange={(e) => setNewFileInput(e.target.value)}
                className="w-full h-9 px-3 rounded bg-[#1c2028] border border-[#464555] text-xs font-mono text-[#dfe2ee] outline-none focus:border-[#c3c0ff] mb-4"
              />
              <div className="flex justify-end gap-2 text-xs font-mono">
                <button
                  type="button"
                  onClick={() => setShowNewFileModal(false)}
                  className="px-3 py-1.5 rounded bg-[#1c2028] hover:bg-[#262a33] text-[#c7c4d8]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-3 py-1.5 rounded bg-[#4f46e5] hover:bg-[#4f46e5]/90 text-white font-semibold"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
