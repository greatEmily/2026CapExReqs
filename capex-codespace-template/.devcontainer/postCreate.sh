
  #!/usr/bin/env bash
  set -euo pipefail

  echo "[postCreate] Installing dependencies..."
  pushd api >/dev/null
  if [ -f package-lock.json ]; then npm ci || npm install; else npm install; fi
  popd >/dev/null

  pushd web >/dev/null
  if [ -f package-lock.json ]; then npm ci || npm install; else npm install; fi
  popd >/dev/null

  echo "[postCreate] Applying database schema & seed..."
  PSQL_URL="postgresql://app:devpass@localhost:5432/capex"
  psql "$PSQL_URL" -v ON_ERROR_STOP=1 -f db/schema.sql
  psql "$PSQL_URL" -v ON_ERROR_STOP=1 -f db/seed.sql

  echo "[postCreate] Creating API .env..."
  cat > api/.env <<'EOF'
  PORT=3000
  CORS_ORIGIN=http://localhost:5173
  DATABASE_URL=postgresql://app:devpass@localhost:5432/capex
  EOF

  echo "[postCreate] Done. Open two terminals and run:
cd api && npm run dev
cd web && npm run dev"
