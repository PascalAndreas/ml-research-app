# ML Research Paper Manager — Design Specification (v0.1)

## 1 Overview

A cross‑platform **desktop application** for machine‑learning researchers to **organise, tag and browse PDF papers** stored in a single user‑chosen folder.
Built with **Python + FastAPI (backend)**, **Tauri + React (desktop UI)** and **SQLite** for persistence.

---

## 2 Requirements

| Category            | Must‑Have                                                                       | Nice‑to‑Have (future)             |
| ------------------- | ------------------------------------------------------------------------------- | --------------------------------- |
| **File Ingestion**  | • Scan folder on first launch• Watch for additions/renames/deletes at runtime   | • Drag‑drop import                |
| **Metadata**        | • Extract title, authors, abstract, year• Date‐added & last‑accessed timestamps | • BibTeX export                   |
| **Tagging**         | • Unlimited user tags• Coloured labels (one colour per tag)                     | • Tag hierarchy / aliases         |
| **Search & Filter** | • Title / author / tag filter                                                   | • Full‑text search via embeddings |
| **Viewer**          | • In‑app PDF viewer• Open externally                                            | • Split‑screen notes              |
| **Cross‑Platform**  | Windows, macOS, Linux                                                           | —                                 |

---

## 3 Key Design Decisions

### 3.1 PDF Parsing Library

**Chosen:** **PyMuPDF (********`fitz`****\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*)**

* **Pros**: Fast C++ core, easy text & metadata extraction, supports outlining, small API.
* **Cons**: Binary wheels ≈ 15 MB each (acceptable).
* **Why not ********************************`pdfminer.six`********************************?** Pure‑Python but \~5× slower and poorer layout retention.

### 3.2 Single‑Folder Philosophy

All PDFs live in one folder.

* Keeps sync simple
* Hash fingerprint (SHA‑1 of bytes) used as immutable primary key in DB even if filename changes.

### 3.3 Watchdog Strategy

* `watchdog.Observer` + `PollingObserver` fallback.
* Events funneled into async queue; debounce bursts (e.g. git clone) with 300 ms window.

### 3.4 Coloured Tags

* `tags` table stores `hue` (0‑359).
* Default palette generated via golden‑angle sequence; user can override in UI.

---

## 4 System Architecture

```
┌─────────────┐      HTTP (localhost)       ┌─────────────┐
│ React UI    │  ◄══════════════════════►  │  FastAPI    │
│ (Tauri Web) │                           │  Backend    │
└─────────────┘                           └─────────────┘
        ▲                                        ▲
        │ filesystem API (Rust)                  │ ORM
        ▼                                        ▼
┌─────────────┐                           ┌────────────────┐
│   Tauri     │—invoke/emit→ IPC →———→│  SQLite DB   │
└─────────────┘                           └────────────────┘
```

* **Tauri rust side** exposes a single command `select_folder()` and persists the path.
* React communicates with FastAPI over `http://localhost:14285` (port configurable).

---

## 5 Data Model (SQLite)

```sql
-- papers table
CREATE TABLE papers (
  id            TEXT PRIMARY KEY, -- SHA1 hash
  filename      TEXT NOT NULL,
  title         TEXT,
  authors       TEXT,
  abstract      TEXT,
  year          INTEGER,
  date_added    DATETIME,
  last_accessed DATETIME
);

-- tags table
CREATE TABLE tags (
  id     INTEGER PRIMARY KEY AUTOINCREMENT,
  name   TEXT UNIQUE NOT NULL,
  hue    INTEGER NOT NULL CHECK (hue BETWEEN 0 AND 359)
);

-- many‑to‑many
CREATE TABLE paper_tags (
  paper_id TEXT    REFERENCES papers(id) ON DELETE CASCADE,
  tag_id   INTEGER REFERENCES tags(id)   ON DELETE CASCADE,
  PRIMARY KEY (paper_id, tag_id)
);
```

ORM suggestion: **SQLModel** (SQLAlchemy 2.x under the hood, pydantic models baked in).

---

## 6 REST API (FastAPI)

```http
GET    /papers           # list w/ query params: ?tag=, ?q=, ?sort=
POST   /papers/rescan    # trigger folder rescan
GET    /papers/{id}      # metadata + first 1000 chars abstract
GET    /papers/{id}/pdf  # stream bytes to viewer
PATCH  /papers/{id}      # update metadata (e.g. title fix)

GET    /tags             # list tags
POST   /tags             # { name, hue }
DELETE /tags/{tag_id}
POST   /papers/{id}/tags # { tag_ids: [] }
DELETE /papers/{id}/tags/{tag_id}
```

All endpoints async; streaming responses use `FileResponse`.

---

## 7 Scaffold / Repo Layout

```
ml-paper-manager/
├─ backend/
│  ├─ app/
│  │  ├─ main.py           # FastAPI entry
│  │  ├─ models.py         # SQLModel tables
│  │  ├─ crud.py           # DB helpers
│  │  ├─ file_watcher.py   # watchdog consumer
│  │  └─ pdf_utils.py      # PyMuPDF helpers
│  └─ requirements.txt
├─ src-tauri/
│  ├─ src/
│  │  └─ main.rs           # Tauri commands
│  └─ tauri.conf.json
├─ frontend/
│  ├─ package.json
│  ├─ vite.config.ts
│  ├─ src/
│  │  ├─ App.tsx
│  │  ├─ components/
│  │  │  ├─ PaperList.tsx
│  │  │  ├─ TagChip.tsx
│  │  │  ├─ PdfViewer.tsx (pdf.js)
│  │  │  └─ TagDialog.tsx
│  │  └─ hooks/
│  │     └─ useApi.ts
│  └─ tailwind.config.js
└─ README.md
```

### 7.1 Backend `main.py` (excerpt)

```python
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine

from .file_watcher import start_watcher
from .routes import paper_router, tag_router

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['tauri://localhost'],
                   allow_methods=['*'], allow_headers=['*'])

engine = create_engine('sqlite:///papers.db', echo=False)
SQLModel.metadata.create_all(engine)

start_watcher(engine)  # background task
app.include_router(paper_router)
app.include_router(tag_router)
```

### 7.2 Tauri Rust Command

```rust
#[tauri::command]
async fn select_folder() -> Result<String, String> {
    let path = tauri::api::dialog::blocking::FileDialogBuilder::default()
        .pick_folder()
        .ok_or("Folder not chosen")?;
    Ok(path.to_string_lossy().into())
}
```

---

## 8 Development Workflow

1. `python -m venv .venv && pip install -r backend/requirements.txt`
2. `cd frontend && pnpm install && pnpm dev` (Vite hot‑reload)
3. `cargo tauri dev` (spawns backend & UI)

Back‑end port injection handled via `TAURI_CONFIG__BUILD__DEV_PATH`.

---

## 9 Future Extensions

* **Embeddings search** (Chroma + `all‑MiniLM‑L6-v2`)
* **Citation import** (BibTeX drag‑drop)
* **Obsidian note sync** via Markdown front‑matter.
* **Cloud sync** (Litestream or SQLite DB sync).

---

## 10 Open Questions for Architect

1. Use **RPC over IPC** instead of HTTP to bypass loopback?

   We will use HTTP.
2. PDF viewer: bundle wasm‑pdfjs vs native OS preview?

   Use wasm-pdfjs to integrate pdf view within the app 
3. Packaging: provide arm64 + x64 separate bundles or fat binaries?

   separate bundles
