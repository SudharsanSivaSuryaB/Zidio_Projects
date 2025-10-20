
import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import { initDb } from "./lib/db";
import resumeRoutes from "./routes/resume";
import aiRoutes from "./routes/ai";

const app = express();
app.use(cors());
app.use(bodyParser.json());

const db = initDb(); // opens or creates db/db.sqlite

app.use("/api/resume", resumeRoutes(db));
app.use("/api/ai", aiRoutes(db));

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Backend listening at http://localhost:${PORT}`);
});
