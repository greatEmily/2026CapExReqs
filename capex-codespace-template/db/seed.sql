
-- Seed users
INSERT INTO users (name, email, role) VALUES
('Emily Duran','emily.duran@example.com','pm') ON CONFLICT DO NOTHING;

-- Seed projects
INSERT INTO projects (capex_id, name, department, approved_budget, stage, status, percent_complete)
VALUES
('CAPEX-2025-001','Warehouse Expansion Bay 3','Facilities',2500000,'approved','on_track',20),
('CAPEX-2025-002','Packaging Line Upgrade','Operations',920000,'execution','at_risk',45)
ON CONFLICT (capex_id) DO NOTHING;

-- Get ids
WITH ids AS (
  SELECT id FROM projects WHERE capex_id='CAPEX-2025-001'
)
INSERT INTO estimates (project_id, category, line_item, quantity, unit_cost)
SELECT (SELECT id FROM projects WHERE capex_id='CAPEX-2025-001'), 'construction','Foundation work',1,150000
UNION ALL
SELECT (SELECT id FROM projects WHERE capex_id='CAPEX-2025-001'), 'soft_costs','Permits',1,12000
ON CONFLICT DO NOTHING;

INSERT INTO actuals (project_id, txn_date, category, vendor, amount, description)
VALUES
((SELECT id FROM projects WHERE capex_id='CAPEX-2025-001'), '2025-07-15','construction','ABC Builders',150000,'Initial site prep'),
((SELECT id FROM projects WHERE capex_id='CAPEX-2025-001'), '2025-08-10','soft_costs','City Permits',12000,'Permit fees'),
((SELECT id FROM projects WHERE capex_id='CAPEX-2025-002'), '2025-08-02','equipment','OEM Parts Co',220000,'Line modules');
