"use client";
import { useState } from "react";
import Image from "next/image";
import { ArrowDownToLine, ArrowUpRight, Check, ChevronRight, FlaskConical, Layers, Search, SlidersHorizontal, Waves } from "lucide-react";
type Experiment = {
  id: string; video: string; metadataId: string; synthetic: boolean; resolution: string;
  depth: number; noise: string; clahe: number; eps: number; frames: number;
  meanCount: number; peakClusters: number; images: { raw: string; enhanced: string; annotated: string };
};
type Research = { source: string; sourceSha256: string; status: string; experiments: Experiment[] };
type Stage = "raw" | "enhanced" | "annotated" | "compare";
const labels: Record<Stage, string> = { raw: "Raw frame", enhanced: "Enhanced", annotated: "Detection overlay", compare: "Compare" };
export default function Dashboard({ research }: { research: Research }) {
  const [selectedId, setSelectedId] = useState(research.experiments.find(e => e.id === "video_020")?.id ?? research.experiments[0].id);
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState("all");
  const [sort, setSort] = useState("id");
  const [stage, setStage] = useState<Stage>("annotated");
  const [split, setSplit] = useState(50);
  const selected = research.experiments.find(e => e.id === selectedId)!;
  const experiments = research.experiments.filter(e =>
    `${e.video} ${e.noise} ${e.metadataId}`.toLowerCase().includes(query.toLowerCase()) &&
    (filter === "all" || (filter === "recorded" ? !e.synthetic : e.synthetic))
  ).sort((a, b) => sort === "count" ? b.meanCount - a.meanCount : a.id.localeCompare(b.id));
  const frames = experiments.reduce((sum, e) => sum + e.frames, 0);
  const average = frames ? experiments.reduce((sum, e) => sum + e.meanCount * e.frames, 0) / frames : 0;
  const maxCount = Math.max(1, ...experiments.map(e => e.meanCount));
  return (
    <div className="observatory">
      <a className="skip-link" href="#main">Skip to research</a>
      <header className="topbar">
        <a className="brand" href="#"><span className="brand-mark"><Waves size={23} /></span>AquaEye<span className="brand-sub">RESEARCH</span></a>
        <nav aria-label="Main navigation"><a className="nav-active" href="#experiments">Observatory</a><a href="#methodology">Methodology</a><a href="https://github.com/Ram-madhav05/aquaeye-research" target="_blank" rel="noreferrer">Repository <ArrowUpRight size={13}/></a></nav>
        <span className="status"><span/> Recorded dataset</span>
      </header>
      <main id="main">
        <section className="intro">
          <div><div className="eyebrow"><span className="small-line"/> PRECISION AQUACULTURE / COMPUTER VISION</div><h1>A clearer view.<br/><span>A deeper understanding.</span></h1><p>Explore underwater image enhancement, shrimp candidate detection,<br className="desktop-break"/> and spatial clustering. Every result starts with the evidence.</p></div>
          <a className="primary-button" href="/data/results.csv" download><ArrowDownToLine size={16}/> Download results <span>CSV</span></a>
        </section>
        <div className="research-notice"><FlaskConical size={17}/><p><strong>Research prototype.</strong> These are historical, unvalidated detector outputs. No labeled ground truth or measured accuracy is included. Counts are candidates, not confirmed shrimp populations.</p><a href="#methodology">Read limitations <ChevronRight size={14}/></a></div>
        <section className="metrics" aria-label="Summary of filtered experiments">
          <Metric label="EXPERIMENTS IN VIEW" value={String(experiments.length).padStart(2,"0")} note={`${research.experiments.length} available recordings`}/>
          <Metric label="FRAMES ANALYZED" value={frames.toLocaleString()} note="Limited excerpts of each video"/>
          <Metric label="MEAN CANDIDATES / FRAME" value={frames ? average.toFixed(2) : "—"} note="Weighted by analyzed frame count"/>
          <Metric label="VALIDATION STATUS" value="Exploratory" note="Precision & recall not yet measured" small/>
        </section>
        <section id="experiments" className="workspace">
          <aside className="experiment-panel">
            <div className="panel-heading"><h2>Experiments</h2><span className="counter">{experiments.length}</span></div>
            <label className="search"><Search size={15}/><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search video or noise…" aria-label="Search experiments"/></label>
            <div className="filter-row"><label><span className="sr-only">Data type</span><select value={filter} onChange={e => setFilter(e.target.value)}><option value="all">All data</option><option value="recorded">Recorded footage</option><option value="synthetic">Synthetic sample</option></select></label><label><span className="sr-only">Sort experiments</span><select value={sort} onChange={e => setSort(e.target.value)}><option value="id">Video ID</option><option value="count">Most candidates</option></select></label></div>
            <div className="experiment-list">
              {experiments.length === 0 ? <div className="empty"><Search size={22}/><p>No matching experiments.</p><button onClick={() => {setQuery(""); setFilter("all");}}>Clear filters</button></div> : experiments.map((e, index) => <button key={e.id} className={`experiment ${e.id === selected.id ? "selected" : ""}`} onClick={() => setSelectedId(e.id)} aria-pressed={e.id === selected.id}>
                <span className="experiment-number">{String(index + 1).padStart(2,"0")}</span><span className="experiment-info"><strong>{e.id.replace("_", " ")}</strong><span>{e.synthetic ? "Synthetic sample" : `${e.noise} noise`} · {e.frames} frames</span></span><span className="experiment-count">{e.meanCount.toFixed(2)}<small>mean/frame</small></span>
              </button>)}
            </div>
            <div className="panel-foot"><Check size={13}/> Values imported from batch summary</div>
          </aside>
          <section className="viewer-panel" aria-label="Selected experiment">
            <div className="viewer-heading"><div><div className="eyebrow">EXPERIMENT / {selected.synthetic ? "SYNTHETIC" : "RECORDED"}</div><h2>{selected.video}</h2></div><span className="outline-badge">{selected.resolution.replace("x", " × ")}</span></div>
            {!experiments.some(e => e.id === selected.id) && <p className="selection-note">Selected experiment is outside the current filter.</p>}
            <div className="stage-tabs" aria-label="Frame display mode">{(Object.keys(labels) as Stage[]).map(value => <button key={value} aria-pressed={stage === value} className={stage === value ? "active" : ""} onClick={() => setStage(value)}>{value === "compare" && <SlidersHorizontal size={13}/>} {labels[value]}</button>)}</div>
            <div className="frame-view" key={`${selected.id}-${stage}`}>
              <Image src={stage === "compare" ? selected.images.raw : selected.images[stage]} alt={`${selected.video}: ${stage === "compare" ? "raw frame" : labels[stage]}`} fill sizes="(max-width: 850px) 100vw, 70vw" className="research-frame" priority/>
              {stage === "compare" && <><div className="comparison-overlay" style={{clipPath: `inset(0 ${100-split}% 0 0)`}}><Image src={selected.images.enhanced} alt={`${selected.video}: enhanced frame for visual comparison`} fill sizes="(max-width: 850px) 100vw, 70vw" className="research-frame"/></div><span className="comparison-line" style={{left: `${split}%`}}/><span className="frame-label left">ENHANCED</span><span className="frame-label right">RAW</span></>}
              {stage !== "compare" && <span className="frame-label left"><span className="dot"/> SAVED {stage.toUpperCase()} FRAME</span>}
              <span className="frame-caption">Historical illustration · frame timestamp unavailable</span>
            </div>
            {stage === "compare" && <label className="compare-slider">Enhanced / raw split<input type="range" min="0" max="100" value={split} onChange={e => setSplit(Number(e.target.value))}/><span>{split}%</span></label>}
            <div className="viewer-footer"><span><Layers size={14}/> {selected.frames} frames in source summary</span><a href={stage === "compare" ? selected.images.enhanced : selected.images[stage]} download><ArrowDownToLine size={14}/> Save frame</a></div>
            <div className="parameters"><Parameter label="Mean candidates" value={selected.meanCount.toFixed(2)} unit="/ frame"/><Parameter label="Peak clusters" value={String(selected.peakClusters)} unit="DBSCAN"/><Parameter label="CLAHE clip limit" value={selected.clahe.toFixed(2)} unit="L* channel"/><Parameter label="Cluster radius" value={selected.eps.toFixed(1)} unit="pixels"/></div>
          </section>
        </section>
        <section className="analysis-grid">
          <div className="panel chart-panel"><div className="panel-heading"><div><div className="eyebrow">CROSS-EXPERIMENT VIEW</div><h2>Candidate distribution</h2></div><span className="muted">Mean / frame</span></div><p className="chart-description">Compare recorded detector output across the current selection. Click a bar to inspect its source.</p>
            <div className="bar-chart">{experiments.map(e => <button className={`chart-row ${e.id === selected.id ? "current" : ""}`} key={e.id} onClick={() => setSelectedId(e.id)} aria-label={`Inspect ${e.id}: ${e.meanCount} mean candidates`}><span>{e.id}</span><span className="bar-track"><span style={{width: `${e.meanCount/maxCount*100}%`}}/></span><strong>{e.meanCount.toFixed(2)}</strong></button>)}{!experiments.length && <p className="muted">Adjust your filters to show results.</p>}</div>
          </div>
          <div className="panel provenance"><div className="eyebrow">DATA PROVENANCE</div><h2>Trace the result.</h2><p>The dashboard is generated from the saved batch summary at build time. No simulated detections, live feeds, or invented performance scores.</p><dl><div><dt>Selected metadata key</dt><dd>{selected.metadataId}</dd></div><div><dt>Depth metadata</dt><dd>{selected.depth.toFixed(2)} m <span>(unverified)</span></dd></div><div><dt>Noise label</dt><dd>{selected.noise}</dd></div><div><dt>Run provenance</dt><dd>Legacy / incomplete</dd></div></dl><p className="small-note">Stored overlays may come from a different run than the summary. Use them as illustrations, not frame-level validation.</p><a className="text-link" href="/data/research.json" download>Download data & source hash <ArrowUpRight size={15}/></a></div>
        </section>
        <section id="methodology" className="methodology"><div className="section-heading"><div><div className="eyebrow">METHOD & LIMITATIONS</div><h2>From underwater pixels to testable hypotheses.</h2></div><span className="outline-badge">RESEARCH NOTES / 01</span></div><div className="method-cards"><article><span className="step">01 / ENHANCE</span><h3>Recover visual contrast</h3><p>CIELAB luminance equalization, noise-adaptive filtering, and highlight suppression. Parameters are derived from per-video CSV metadata; they are heuristic, not physically validated calibration.</p></article><article><span className="step">02 / DETECT & GROUP</span><h3>Find candidate patterns</h3><p>Color, motion, and morphology generate candidates. Optional shrimp-class YOLO weights can contribute detections. Temporal association and DBSCAN group candidates in image coordinates.</p></article><article><span className="step">03 / VALIDATE</span><h3>Measure before claiming</h3><p>No usable trained shrimp weights or labeled test set are bundled. Annotate held-out videos, compare raw and enhanced runs, and report precision, recall, F1, count error, and measured throughput.</p></article></div><details><summary>Reproduce and evaluate the research</summary><div className="reproduce"><p>Run from the repository root. Install Python dependencies first. Use separate output directories for enhancement ablations.</p><pre><code>{'python -m src.main --video_dir data/raw_videos --output_dir runs/enhanced --limit 50\npython -m src.main --video_dir data/raw_videos --output_dir runs/raw --limit 50 --no_enhance\npython -m src.evaluate --ground-truth annotations.json --predictions predictions.json --output evaluation.json'}</code></pre><p>Evaluation uses confidence-ranked, one-to-one IoU matching. Include negative frames with empty box lists. Keep pond/video splits separate to avoid adjacent-frame leakage. See the repository research protocol for the full schema and limitations.</p></div></details></section>
        <footer><a className="brand" href="#"><Waves size={19}/> AquaEye</a><span>Evidence first. Precision through validation.</span><a href="/data/research.json" download title={research.sourceSha256}>Source SHA-256: {research.sourceSha256.slice(0,12)}… <ArrowUpRight size={12}/></a></footer>
      </main>
    </div>
  );
}
function Metric({label,value,note,small=false}:{label:string;value:string;note:string;small?:boolean}) {return <div className="metric"><span>{label}</span><strong className={small ? "small-value" : ""}>{value}</strong><p>{note}</p></div>;}
function Parameter({label,value,unit}:{label:string;value:string;unit:string}) {return <div><span>{label}</span><strong>{value}<small>{unit}</small></strong></div>;}
