
import express from 'express';
import Joi from 'joi';
import db from '../db.js';

const router = express.Router();

// List projects with budget vs actuals summary
router.get('/', async (req, res, next) => {
  try {
    const { rows } = await db.query('SELECT * FROM v_project_budget_vs_actual ORDER BY name');
    res.json(rows);
  } catch (err) { next(err); }
});

// Create a project
const projectSchema = Joi.object({
  capex_id: Joi.string().optional(),
  name: Joi.string().min(3).required(),
  description: Joi.string().allow(''),
  department: Joi.string().allow(''),
  cost_center: Joi.string().allow(''),
  approved_budget: Joi.number().min(0).required(),
  contingency_percent: Joi.number().min(0).max(100).default(0),
  start_date: Joi.date().optional(),
  target_completion_date: Joi.date().optional(),
  manager_id: Joi.string().guid({ version: 'uuidv4' }).optional(),
  sponsor_id: Joi.string().guid({ version: 'uuidv4' }).optional()
});

router.post('/', async (req, res, next) => {
  try {
    const body = await projectSchema.validateAsync(req.body, { abortEarly: false });
    const { rows } = await db.query(
      `INSERT INTO projects (capex_id, name, description, department, cost_center, approved_budget, contingency_percent, start_date, target_completion_date)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
       RETURNING *`,
      [
        body.capex_id || null,
        body.name,
        body.description || null,
        body.department || null,
        body.cost_center || null,
        body.approved_budget,
        body.contingency_percent || 0,
        body.start_date || null,
        body.target_completion_date || null
      ]
    );
    res.status(201).json(rows[0]);
  } catch (err) { next(err); }
});

// Get a project by id
router.get('/:id', async (req, res, next) => {
  try {
    const { rows } = await db.query('SELECT * FROM projects WHERE id = $1', [req.params.id]);
    if (!rows[0]) return res.status(404).json({ error: 'Not found' });
    res.json(rows[0]);
  } catch (err) { next(err); }
});

// Project summary (uses the view)
router.get('/:id/summary', async (req, res, next) => {
  try {
    const { rows } = await db.query('SELECT * FROM v_project_budget_vs_actual WHERE id = $1', [req.params.id]);
    if (!rows[0]) return res.status(404).json({ error: 'Not found' });
    res.json(rows[0]);
  } catch (err) { next(err); }
});

// Actuals
const actualSchema = Joi.object({
  txn_date: Joi.date().required(),
  category: Joi.string().valid('construction','equipment','it','soft_costs','contingency','other').required(),
  vendor: Joi.string().allow(''),
  po_number: Joi.string().allow(''),
  invoice_number: Joi.string().allow(''),
  amount: Joi.number().required(),
  description: Joi.string().allow('')
});

router.get('/:id/actuals', async (req, res, next) => {
  try {
    const { rows } = await db.query('SELECT * FROM actuals WHERE project_id = $1 ORDER BY txn_date DESC', [req.params.id]);
    res.json(rows);
  } catch (err) { next(err); }
});

router.post('/:id/actuals', async (req, res, next) => {
  try {
    const body = await actualSchema.validateAsync(req.body, { abortEarly: false });
    const { rows } = await db.query(
      `INSERT INTO actuals (project_id, txn_date, category, vendor, po_number, invoice_number, amount, description)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
       RETURNING *`,
      [
        req.params.id,
        body.txn_date,
        body.category,
        body.vendor || null,
        body.po_number || null,
        body.invoice_number || null,
        body.amount,
        body.description || null
      ]
    );
    res.status(201).json(rows[0]);
  } catch (err) { next(err); }
});

export default router;
