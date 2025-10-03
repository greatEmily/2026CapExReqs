import express from 'express';

const app = express();
const PORT = 3000;

app.get('/api/projects', (req, res) => {
  res.json([
    { id: 1, name: 'Project A' },
    { id: 2, name: 'Project B' }
  ]);
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});