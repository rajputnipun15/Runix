"""RUNIX Workspace Filesystem Service.

Per docs/09-WORKSPACE-FILESYSTEM.md and Rule 5 (security non-negotiable):
- Never allow path traversal
- Atomic writes
- Storage separation from PostgreSQL
"""

import os
import tempfile
from pathlib import Path

from app.core.config import get_settings
from app.core.exceptions import (
    FileNotFoundError as RunixFileNotFoundError,
)
from app.core.exceptions import (
    FileTooLargeError,
    PathTraversalError,
)
from app.schemas.file import FileContentResponse, FileTreeItem, FileWriteResponse

settings = get_settings()

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB limit
IGNORED_NAMES = {
    ".git",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".next",
    ".venv",
    ".DS_Store",
}


class WorkspaceService:
    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = Path(base_dir or settings.workspace_base_dir).resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_workspace_dir(self, project_id: str) -> Path:
        """Resolve workspace root directory for a project and ensure it exists."""
        workspace_dir = (self.base_dir / str(project_id)).resolve()
        # Security: verify it stays under base_dir
        if not str(workspace_dir).startswith(str(self.base_dir)):
            raise PathTraversalError()
        workspace_dir.mkdir(parents=True, exist_ok=True)
        return workspace_dir

    def resolve_safe_path(self, project_id: str, relative_path: str) -> Path:
        """Resolve a relative path inside the project's workspace safely."""
        clean_path = relative_path.strip().lstrip("/\\")
        workspace_dir = self.get_workspace_dir(project_id)
        target = (workspace_dir / clean_path).resolve()

        # Security check: must start with workspace_dir
        if not str(target).startswith(str(workspace_dir)):
            raise PathTraversalError()

        return target

    def list_files(self, project_id: str) -> list[FileTreeItem]:
        """List all files and directories in the workspace recursively."""
        workspace_dir = self.get_workspace_dir(project_id)
        items: list[FileTreeItem] = []

        for root, dirs, files in os.walk(workspace_dir):
            # Prune ignored directories in-place
            dirs[:] = [d for d in dirs if d not in IGNORED_NAMES]

            rel_root = Path(root).relative_to(workspace_dir)

            for d in dirs:
                rel_path = (rel_root / d).as_posix()
                items.append(FileTreeItem(path=rel_path, type="directory"))

            for f in files:
                if f in IGNORED_NAMES:
                    continue
                file_path = Path(root) / f
                rel_path = (rel_root / f).as_posix()
                try:
                    size = file_path.stat().st_size
                except OSError:
                    size = 0
                items.append(FileTreeItem(path=rel_path, type="file", size_bytes=size))

        items.sort(key=lambda x: (x.type != "directory", x.path))
        return items

    def read_file(self, project_id: str, relative_path: str) -> FileContentResponse:
        """Read content of a file inside the workspace."""
        file_path = self.resolve_safe_path(project_id, relative_path)

        if not file_path.is_file():
            raise RunixFileNotFoundError(path=relative_path)

        stat = file_path.stat()
        if stat.st_size > MAX_FILE_SIZE_BYTES:
            raise FileTooLargeError()

        raw = file_path.read_bytes()
        if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
            try:
                content = raw.decode("utf-16")
            except Exception:
                content = raw.decode("latin-1", errors="replace")
        elif raw.startswith(b"\xef\xbb\xbf"):
            content = raw.decode("utf-8-sig")
        else:
            try:
                content = raw.decode("utf-8")
            except UnicodeDecodeError:
                content = raw.decode("latin-1", errors="replace")

        rel_path = file_path.relative_to(self.get_workspace_dir(project_id)).as_posix()
        return FileContentResponse(
            path=rel_path,
            content=content,
            encoding="utf-8",
            size_bytes=stat.st_size,
        )

    def write_file(self, project_id: str, relative_path: str, content: str) -> FileWriteResponse:
        """Write content atomically to a file inside the workspace."""
        file_path = self.resolve_safe_path(project_id, relative_path)

        # Enforce size limit
        encoded = content.encode("utf-8")
        if len(encoded) > MAX_FILE_SIZE_BYTES:
            raise FileTooLargeError()

        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Atomic write via temporary file
        temp_dir = file_path.parent
        with tempfile.NamedTemporaryFile("wb", dir=temp_dir, delete=False) as tf:
            tf.write(encoded)
            temp_name = tf.name

        os.replace(temp_name, file_path)

        rel_path = file_path.relative_to(self.get_workspace_dir(project_id)).as_posix()
        return FileWriteResponse(path=rel_path, saved=True, size_bytes=len(encoded))

    def create_directory(self, project_id: str, relative_path: str) -> str:
        """Create a directory inside the workspace."""
        dir_path = self.resolve_safe_path(project_id, relative_path)
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path.relative_to(self.get_workspace_dir(project_id)).as_posix()

    def delete_item(self, project_id: str, relative_path: str) -> None:
        """Delete a file or directory inside the workspace."""
        target = self.resolve_safe_path(project_id, relative_path)
        workspace_dir = self.get_workspace_dir(project_id)

        # Cannot delete the workspace root itself
        if target == workspace_dir:
            raise PathTraversalError()

        if not target.exists():
            raise RunixFileNotFoundError(path=relative_path)

        if target.is_dir():
            import shutil

            shutil.rmtree(target)
        else:
            target.unlink()

    def delete_workspace(self, project_id: str) -> None:
        """Delete entire workspace folder upon project deletion."""
        workspace_dir = self.get_workspace_dir(project_id)
        if workspace_dir.exists():
            import shutil

            shutil.rmtree(workspace_dir, ignore_errors=True)
