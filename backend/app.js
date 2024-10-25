const express = require("express");
const axios = require("axios");
const cors = require("cors"); // to allow CORS for frontend requests
const app = express();
const PORT = 3000;

app.use(cors()); // enable CORS
app.use(express.json()); // parse JSON request body

app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.post("/api/scoreboard", async (req, res) => {
  const { link } = req.body; // get the link from the request body
  const fullUrl = `${link}/api/v1/scoreboard`; // construct the full URL

  try {
    const response = await axios.get(fullUrl); // make the request to the URL
    res.json(response.data); // send back the JSON data to the frontend
  } catch (error) {
    console.error("Error fetching scoreboard data:", error);
    res.status(500).json({ error: "Failed to fetch scoreboard data" });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
