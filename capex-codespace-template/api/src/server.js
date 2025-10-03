
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import projectsRouter from './routes/projects.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(cors({ origin: (process.env.CORS_ORIGIN || '*').split(','), credentials: false }));

app.get('/api/health', (req, res) => res.json({ status: 'ok' }));
app.use('/api/projects', projectsRouter);

app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: 'Internal Server Error', details: err.message });
});

app.listen(PORT, () => console.log(`API listening on http://localhost:${PORT}`));
