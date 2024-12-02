const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Hello, Node.js!");
});

const port = 8080;
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
