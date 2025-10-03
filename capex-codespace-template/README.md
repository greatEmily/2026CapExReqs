
# CapEx Tracker — GitHub Codespaces Template

A full‑stack starter (Node.js + Express + PostgreSQL + React) designed to run **100% in GitHub Codespaces** — no local admin rights or Docker required.

## What's inside
- **.devcontainer/**: Codespaces config with Node 20 + PostgreSQL 16
- **api/**: Express API with `pg` client and example endpoints
- **web/**: React (Vite) front‑end
- **db/**: SQL schema + seed data

## Quick start (in GitHub)
1. Create a **new repository** and upload these files (or click **Use this template** if available).
2. Click **Code ▸ Create codespace on main**.
3. Wait for container to build (Node + Postgres). The **postCreate** script will:
   - install dependencies for `api` and `web`
   - create the `capex` database schema and seed sample data
   - create `api/.env` pointing to the local Postgres
4. In the Codespace, open two terminals:
   - **API**
     ```bash
     cd api
     npm run dev
     # API: http://localhost:3000/api/health
     ```
   - **Web**
     ```bash
     cd web
     npm run dev
     # App: http://localhost:5173
     ```

### Default config
- Database: `postgresql://app:devpass@localhost:5432/capex`
- CORS allowed origin: `http://localhost:5173`

## Next steps
- Add Stage‑Gate endpoints and UI tabs
- Hook up authentication (MSAL / Entra ID) when you deploy
- Swap seed data with real data or an import job

---
### Project structure
```text
.
├─ .devcontainer/
│  ├─ devcontainer.json
│  └─ postCreate.sh
├─ api/
│  ├─ package.json
│  └─ src/
│     ├─ server.js
│     ├─ db.js
│     └─ routes/
│        └─ projects.js
├─ web/
│  ├─ package.json
│  ├─ index.html
│  └─ src/
│     ├─ main.jsx
│     ├─ App.jsx
│     └─ api.js
└─ db/
   ├─ schema.sql
    └─ seed.sql
```
