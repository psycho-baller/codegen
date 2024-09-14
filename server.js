const express = require('express');
const { exec } = require('child_process');
const app = express();
const port = 3000;

app.use(express.static('public'));

app.get('/graph-data', (req, res) => {
  exec('python3 generate_graph.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return res.status(500).send('Error generating graph data');
    }
    res.send(stdout);
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});