
-- CapEx Tracker schema
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- users
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  role TEXT CHECK (role IN ('requester','pm','finance','approver','admin')) NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

-- projects
CREATE TABLE IF NOT EXISTS projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  capex_id TEXT UNIQUE,
  name TEXT NOT NULL,
  description TEXT,
  department TEXT,
  cost_center TEXT,
  sponsor_id UUID REFERENCES users(id),
  manager_id UUID REFERENCES users(id),
  stage TEXT CHECK (stage IN (
    'intake','feasibility','business_case','approved','procurement','execution','closeout'
  )) DEFAULT 'intake',
  status TEXT CHECK (status IN ('on_track','at_risk','blocked','on_hold')) DEFAULT 'on_track',
  approved_budget NUMERIC(14,2) DEFAULT 0,
  contingency_percent NUMERIC(5,2) DEFAULT 0,
  start_date DATE,
  target_completion_date DATE,
  percent_complete NUMERIC(5,2) DEFAULT 0,
  risk_rating TEXT CHECK (risk_rating IN ('low','medium','high')) DEFAULT 'low',
  created_by UUID, updated_by UUID,
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);

-- estimates
CREATE TABLE IF NOT EXISTS estimates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  version INT NOT NULL DEFAULT 1,
  is_current BOOLEAN DEFAULT TRUE,
  category TEXT CHECK (category IN (
    'construction','equipment','it','soft_costs','contingency','other'
  )) NOT NULL,
  line_item TEXT NOT NULL,
  quantity NUMERIC(12,2) DEFAULT 1,
  unit_cost NUMERIC(14,2) DEFAULT 0,
  amount NUMERIC(14,2) GENERATED ALWAYS AS (quantity * unit_cost) STORED,
  notes TEXT,
  created_at TIMESTAMP DEFAULT now()
);

-- actuals
CREATE TABLE IF NOT EXISTS actuals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  txn_date DATE NOT NULL,
  category TEXT CHECK (category IN (
    'construction','equipment','it','soft_costs','contingency','other'
  )) NOT NULL,
  vendor TEXT, po_number TEXT, invoice_number TEXT,
  amount NUMERIC(14,2) NOT NULL,
  description TEXT,
  created_by UUID,
  created_at TIMESTAMP DEFAULT now()
);

-- stage gates
CREATE TABLE IF NOT EXISTS stage_gates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  gate TEXT CHECK (gate IN ('intake','business_case','approval','procurement','execution','closeout')) NOT NULL,
  status TEXT CHECK (status IN ('pending','approved','rejected')) DEFAULT 'pending',
  owner_id UUID, approved_at TIMESTAMP, notes TEXT,
  created_at TIMESTAMP DEFAULT now()
);

-- helpful views
CREATE OR REPLACE VIEW v_project_budget_vs_actual AS
SELECT p.id,
       p.capex_id,
       p.name,
       p.stage,
       p.status,
       p.approved_budget,
       COALESCE(SUM(a.amount), 0) AS actuals_to_date,
       (p.approved_budget - COALESCE(SUM(a.amount),0)) AS variance
FROM projects p
LEFT JOIN actuals a ON a.project_id = p.id
GROUP BY p.id;

CREATE OR REPLACE VIEW v_category_variance AS
SELECT e.project_id,
       e.category,
       SUM(e.amount) AS estimate_total,
       COALESCE(SUM(a.amount),0) AS actual_total,
       (SUM(e.amount) - COALESCE(SUM(a.amount),0)) AS category_variance
FROM estimates e
LEFT JOIN actuals a ON a.project_id = e.project_id AND a.category = e.category
GROUP BY e.project_id, e.category;
