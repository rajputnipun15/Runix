"""RUNIX Template Registry and Initializer Service.

Per docs/15-PROJECT-TEMPLATES.md:
Templates are deterministic, versioned, and provide starter files for user runtimes.
"""

from app.core.exceptions import InvalidTemplateError
from app.schemas.template import TemplateItem
from app.services.workspace_service import WorkspaceService

TEMPLATES: dict[str, TemplateItem] = {
    "react-vite-ts": TemplateItem(
        id="react-vite-ts",
        name="React + Vite + TypeScript",
        description="Fast frontend development with modern React 19, Vite, and TypeScript.",
        language="TypeScript",
        framework="React/Vite",
        runtime="Node.js 22",
        version="1.0.0",
        default_port=5173,
        tags=["frontend", "react", "vite", "typescript"],
    ),
    "node-typescript": TemplateItem(
        id="node-typescript",
        name="Node.js + TypeScript",
        description="Backend API and microservice environment with Node.js and TypeScript.",
        language="TypeScript",
        framework="Node.js",
        runtime="Node.js 22",
        version="1.0.0",
        default_port=3000,
        tags=["backend", "node", "typescript"],
    ),
    "python-fastapi": TemplateItem(
        id="python-fastapi",
        name="Python + FastAPI",
        description="High-performance async Python backend with FastAPI and Uvicorn.",
        language="Python",
        framework="FastAPI",
        runtime="Python 3.12",
        version="1.0.0",
        default_port=8000,
        tags=["backend", "python", "fastapi"],
    ),
    "mern": TemplateItem(
        id="mern",
        name="MERN Stack",
        description="Fullstack JavaScript application with MongoDB, Express, React, and Node.",
        language="TypeScript/JavaScript",
        framework="MongoDB/Express/React/Node",
        runtime="Node.js 22",
        version="1.0.0",
        default_port=5173,
        tags=["fullstack", "mern", "react", "node"],
    ),
    "blank-docker": TemplateItem(
        id="blank-docker",
        name="Blank Development Environment",
        description="A clean, minimal container sandbox with bash and core build tools.",
        language="Shell",
        framework="None",
        runtime="RUNIX Blank",
        version="1.0.0",
        default_port=None,
        tags=["blank", "custom"],
    ),
}

TEMPLATE_STARTER_FILES: dict[str, dict[str, str]] = {
    "react-vite-ts": {
        "package.json": """{
  "name": "runix-react-app",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.3.4",
    "typescript": "^5.7.0",
    "vite": "^6.0.0"
  }
}
""",
        "vite.config.ts": """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
});
""",
        "index.html": """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>RUNIX App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
""",
        "src/main.tsx": """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
""",
        "src/App.tsx": """import React, { useState } from 'react';

export default function App() {
  const [count, setCount] = useState(0);

    <div style={{
      fontFamily: 'Inter, sans-serif',
      padding: '40px',
      textAlign: 'center',
      background: '#0f131b',
      color: '#dfe2ee',
      minHeight: '100vh',
    }}>
      <h1 style={{ fontSize: '2.5rem', marginBottom: '16px' }}>⚡ RUNIX Cloud IDE</h1>
      <p style={{ color: '#c7c4d8', marginBottom: '24px' }}>Build. Run. Ship. Anywhere.</p>
      <button
        onClick={() => setCount((c) => c + 1)}
        style={{
          background: '#4f46e5',
          color: '#ffffff',
          padding: '12px 24px',
          border: 'none',
          borderRadius: '8px',
          fontSize: '1rem',
          cursor: 'pointer',
          fontWeight: 600,
        }}
      >
        Count is: {count}
      </button>
    </div>
  );
}
""",
        "src/index.css": """* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
body {
  background-color: #0f131b;
  color: #dfe2ee;
}
""",
        "README.md": """# RUNIX React + Vite + TypeScript Template

This project was generated in RUNIX Cloud Platform.

## Quickstart

Run development server:
```bash
npm install
npm run dev
```
""",
    },
    "node-typescript": {
        "package.json": """{
  "name": "runix-node-app",
  "version": "1.0.0",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "tsx": "^4.19.0",
    "typescript": "^5.7.0"
  }
}
""",
        "tsconfig.json": """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
""",
        "src/index.ts": """import http from 'http';

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(
    JSON.stringify({
      message: 'Hello from RUNIX Node.js runtime!',
      timestamp: new Date().toISOString(),
    })
  );
});

const PORT = 3000;
server.listen(PORT, '0.0.0.0', () => {
  console.log(`⚡ RUNIX Node.js server running on port ${PORT}`);
});
""",
        "README.md": """# RUNIX Node.js + TypeScript Template

## Quickstart

```bash
npm install
npm run dev
```
""",
    },
    "python-fastapi": {
        "main.py": """from fastapi import FastAPI

app = FastAPI(title="RUNIX User App")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "⚡ Running inside RUNIX Python runtime",
        "platform": "RUNIX Cloud IDE"
    }
""",
        "requirements.txt": """fastapi>=0.115.0
uvicorn[standard]>=0.30.0
""",
        "README.md": """# RUNIX Python FastAPI Template

## Quickstart

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
""",
    },
    "mern": {
        "package.json": """{
  "name": "runix-mern-app",
  "version": "1.0.0",
  "scripts": {
    "dev": "node server.js"
  },
  "dependencies": {
    "express": "^4.21.0",
    "cors": "^2.8.5"
  }
}
""",
        "server.js": """const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', stack: 'MERN', platform: 'RUNIX' });
});

const PORT = 5000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`⚡ MERN API listening on port ${PORT}`);
});
""",
        "README.md": """# RUNIX MERN Template

## Quickstart

```bash
npm install
npm run dev
```
""",
    },
    "blank-docker": {
        "README.md": """# RUNIX Blank Environment

Welcome to your isolated RUNIX Cloud Sandbox!
Use the built-in terminal to create files, install dependencies, and run services.
""",
    },
}


class TemplateService:
    def list_templates(self) -> list[TemplateItem]:
        """Return the list of all supported project templates."""
        return list(TEMPLATES.values())

    def get_template(self, template_id: str) -> TemplateItem:
        """Lookup a specific template by ID."""
        if template_id not in TEMPLATES:
            raise InvalidTemplateError(template_id)
        return TEMPLATES[template_id]

    def seed_template_files(
        self, project_id: str, template_id: str, workspace_service: WorkspaceService
    ) -> None:
        """Populate initial workspace files for a newly created project."""
        files = TEMPLATE_STARTER_FILES.get(template_id, TEMPLATE_STARTER_FILES["blank-docker"])
        for file_path, content in files.items():
            workspace_service.write_file(project_id, file_path, content)
