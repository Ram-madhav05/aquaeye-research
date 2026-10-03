import { readFile, writeFile, mkdir, access } from "node:fs/promises";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import path from "node:path";
const web = fileURLToPath(new URL("../", import.meta.url));
const root = path.resolve(web, "..");
export function parseCsv(text) {
  const rows = []; let row = [], field = "", quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '"') {
      if (quoted && text[i + 1] === '"') { field += '"'; i++; }
      else quoted = !quoted;
    } else if (c === "," && !quoted) { row.push(field); field = ""; }
    else if ((c === "\n" || c === "\r") && !quoted) {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); if (row.some(Boolean)) rows.push(row); row = []; field = "";
    } else field += c;
  }
  if (quoted) throw new Error("Unterminated CSV quote");
  row.push(field); if (row.some(Boolean)) rows.push(row);
  const [headers, ...values] = rows;
  if (!headers) throw new Error("Empty summary CSV");
  return values.map(values => {
    if (values.length !== headers.length) throw new Error("CSV column count mismatch");
    return Object.fromEntries(headers.map((key, i) => [key, values[i]]));
  });
}
const source = "data/processed_videos/batch_processing_summary.csv";
const csv = await readFile(path.join(root, source), "utf8");
const rows = parseCsv(csv.replace(/^\uFEFF/, ""));
const number = (row, key) => {
  if (!row[key]?.trim()) throw new Error(`Missing ${key} for ${row.video_name}`);
  const value = Number(row[key]);
  if (!Number.isFinite(value) || value < 0) throw new Error(`Invalid ${key} for ${row.video_name}`);
  return value;
};
const seen = new Set();
const experiments = await Promise.all(rows.map(async row => {
  const id = row.video_name.replace(/\.[^.]+$/, "");
  if (!/^[a-zA-Z0-9_-]+$/.test(id) || seen.has(id)) throw new Error(`Invalid or duplicate experiment: ${id}`);
  seen.add(id);
  const images = {};
  for (const stage of ["raw", "enhanced", "annotated"]) {
    const relative = `/assets/${id}_${stage}.jpg`;
    await access(path.join(web, "public", relative));
    images[stage] = relative;
  }
  return { id, video: row.video_name, metadataId: row.video_id,
    synthetic: id.startsWith("sample_"), resolution: row.resolution,
    depth: number(row, "depth_m"), noise: row.noise_type,
    clahe: number(row, "clahe_clip"), eps: number(row, "dbscan_eps"),
    frames: number(row, "total_frames"), meanCount: number(row, "average_shrimp_count"),
    peakClusters: number(row, "max_clusters_detected"), images };
}));
if (!experiments.length) throw new Error("No experiments in summary");
const research = { schemaVersion: 1, source,
  sourceSha256: createHash("sha256").update(csv).digest("hex"),
  status: "Historical export; detector version and timing not recorded", experiments };
await mkdir(path.join(web, "src/data"), { recursive: true });
await mkdir(path.join(web, "public/data"), { recursive: true });
const output = JSON.stringify(research, null, 2) + "\n";
await writeFile(path.join(web, "src/data/research.json"), output);
await writeFile(path.join(web, "public/data/research.json"), output);
const columns = ["video_name", "video_id", "resolution", "depth_m", "noise_type", "clahe_clip", "dbscan_eps", "total_frames", "average_shrimp_count", "max_clusters_detected"];
const quote = value => '"' + String(value).replaceAll('"', '""') + '"';
await writeFile(path.join(web, "public/data/results.csv"), [columns.join(","), ...rows.map(row => columns.map(key => quote(row[key])).join(","))].join("\n") + "\n");
console.log(`Exported ${experiments.length} experiments from ${source}`);
