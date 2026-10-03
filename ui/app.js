// AquaEye Vision & Spatial Swarm Tracking - Dashboard Engine v2.4

const VIDEO_DATA = [
  {
    name: "video_016.mp4",
    id: "video_016",
    title: "Sector 16 - Whiteleg Schooling Swarm",
    category: "swarm",
    resolution: "1568x886",
    depth_m: 16.77,
    noise_type: "SaltPepper",
    clahe_clip: 2.80,
    dbscan_eps: 85.5,
    avg_shrimp: 13.8,
    peak_clusters: 6,
    density_category: "High Density Swarm",
    feeder_target: [780, 440],
    video_src: "videos/video_016_processed.mp4",
    snapshot: "assets/video_016_processed_frame.jpg",
    raw: "assets/video_016_raw.jpg",
    enhanced: "assets/video_016_enhanced.jpg",
    annotated: "assets/video_016_annotated.jpg",
    transmission_err: 1,
    disparity_mean: 2.22,
    reflection_sum: 1653,
    complexity_score: 0.663
  },
  {
    name: "video_013.mp4",
    id: "video_013",
    title: "Sector 13 - Turbid Low-Density Channel",
    category: "macro",
    resolution: "886x496",
    depth_m: 2.99,
    noise_type: "Impulse",
    clahe_clip: 2.44,
    dbscan_eps: 160.0,
    avg_shrimp: 2.0,
    peak_clusters: 0,
    density_category: "Feeding Pair (Macro)",
    feeder_target: [328, 293],
    video_src: "videos/video_013_processed.mp4",
    snapshot: "assets/video_013_processed_frame.jpg",
    raw: "assets/video_013_raw.jpg",
    enhanced: "assets/video_013_enhanced.jpg",
    annotated: "assets/video_013_annotated.jpg",
    transmission_err: 1,
    disparity_mean: 1.28,
    reflection_sum: 4112,
    complexity_score: 0.351
  },
  {
    name: "video_018.mp4",
    id: "video_018",
    title: "Sector 18 - Substrate Feeding Group",
    category: "turbid",
    resolution: "1568x886",
    depth_m: 15.64,
    noise_type: "Speckle",
    clahe_clip: 2.71,
    dbscan_eps: 91.6,
    avg_shrimp: 1.6,
    peak_clusters: 0,
    density_category: "Low Density",
    feeder_target: [920, 510],
    video_src: "videos/video_018_processed.mp4",
    snapshot: "assets/video_018_processed_frame.jpg",
    raw: "assets/video_018_raw.jpg",
    enhanced: "assets/video_018_enhanced.jpg",
    annotated: "assets/video_018_annotated.jpg",
    transmission_err: 4,
    disparity_mean: 2.55,
    reflection_sum: 3871,
    complexity_score: 0.864
  },
  {
    name: "video_019.mp4",
    id: "video_019",
    title: "Sector 19 - Deep Pelagic Swarm Column",
    category: "turbid",
    resolution: "1568x886",
    depth_m: 29.91,
    noise_type: "SaltPepper",
    clahe_clip: 1.69,
    dbscan_eps: 47.9,
    avg_shrimp: 9.1,
    peak_clusters: 0,
    density_category: "Pelagic Swarm",
    feeder_target: [640, 380],
    video_src: "videos/video_019_processed.mp4",
    snapshot: "assets/video_019_processed_frame.jpg",
    raw: "assets/video_019_raw.jpg",
    enhanced: "assets/video_019_enhanced.jpg",
    annotated: "assets/video_019_annotated.jpg",
    transmission_err: 6,
    disparity_mean: 8.43,
    reflection_sum: 4181,
    complexity_score: 0.849
  },
  {
    name: "video_020.mp4",
    id: "video_020",
    title: "Sector 20 - Nursery Schooling Channel",
    category: "swarm",
    resolution: "1920x886",
    depth_m: 3.97,
    noise_type: "SaltPepper",
    clahe_clip: 3.21,
    dbscan_eps: 160.0,
    avg_shrimp: 59.6,
    peak_clusters: 6,
    density_category: "High Density Swarm",
    feeder_target: [1050, 490],
    video_src: "videos/video_020_processed.mp4",
    snapshot: "assets/video_020_processed_frame.jpg",
    raw: "assets/video_016_raw.jpg",
    enhanced: "assets/video_016_enhanced.jpg",
    annotated: "assets/video_020_processed_frame.jpg",
    transmission_err: 3,
    disparity_mean: 1.11,
    reflection_sum: 1541,
    complexity_score: 0.830
  },
  {
    name: "video_023.mp4",
    id: "video_023",
    title: "Sector 23 - Substrate Radial Swarm",
    category: "macro",
    resolution: "1024x768",
    depth_m: 22.33,
    noise_type: "Impulse",
    clahe_clip: 2.98,
    dbscan_eps: 157.2,
    avg_shrimp: 12.0,
    peak_clusters: 2,
    density_category: "Moderate Swarm",
    feeder_target: [512, 384],
    video_src: "videos/video_023_processed.mp4",
    snapshot: "assets/video_023_processed_frame.jpg",
    raw: "assets/video_019_raw.jpg",
    enhanced: "assets/video_019_enhanced.jpg",
    annotated: "assets/video_023_processed_frame.jpg",
    transmission_err: 5,
    disparity_mean: 2.06,
    reflection_sum: 2612,
    complexity_score: 0.827
  },
  {
    name: "video_024.mov",
    id: "video_024",
    title: "Sector 24 - Effluent Drain Schooling",
    category: "swarm",
    resolution: "800x600",
    depth_m: 24.68,
    noise_type: "Gaussian",
    clahe_clip: 2.44,
    dbscan_eps: 142.2,
    avg_shrimp: 34.8,
    peak_clusters: 3,
    density_category: "Medium-High",
    feeder_target: [420, 310],
    video_src: "videos/video_024_processed.mp4",
    snapshot: "assets/video_024_processed_frame.jpg",
    raw: "assets/video_016_raw.jpg",
    enhanced: "assets/video_016_enhanced.jpg",
    annotated: "assets/video_024_processed_frame.jpg",
    transmission_err: 5,
    disparity_mean: 8.76,
    reflection_sum: 4784,
    complexity_score: 0.581
  },
  {
    name: "video_032.mp4",
    id: "video_032",
    title: "Sector 32 - Feed Tray Active Clusters",
    category: "macro",
    resolution: "1920x1080",
    depth_m: 1.90,
    noise_type: "Poisson",
    clahe_clip: 2.37,
    dbscan_eps: 160.0,
    avg_shrimp: 11.3,
    peak_clusters: 3,
    density_category: "Active Feeding",
    feeder_target: [980, 540],
    video_src: "videos/video_032_processed.mp4",
    snapshot: "assets/video_032_processed_frame.jpg",
    raw: "assets/video_019_raw.jpg",
    enhanced: "assets/video_019_enhanced.jpg",
    annotated: "assets/video_032_processed_frame.jpg",
    transmission_err: 4,
    disparity_mean: 5.90,
    reflection_sum: 4050,
    complexity_score: 0.351
  },
  {
    name: "video_008.mp4",
    id: "video_008",
    title: "Sector 08 - Surface Aerator Station",
    category: "turbid",
    resolution: "1568x886",
    depth_m: 1.36,
    noise_type: "Impulse",
    clahe_clip: 2.55,
    dbscan_eps: 160.0,
    avg_shrimp: 1.3,
    peak_clusters: 1,
    density_category: "Aerator Margin",
    feeder_target: [784, 443],
    video_src: "videos/video_008_processed.mp4",
    snapshot: "assets/video_008_processed_frame.jpg",
    raw: "assets/video_016_raw.jpg",
    enhanced: "assets/video_016_enhanced.jpg",
    annotated: "assets/video_008_processed_frame.jpg",
    transmission_err: 3,
    disparity_mean: 7.20,
    reflection_sum: 3634,
    complexity_score: 0.524
  },
  {
    name: "sample_01.mp4",
    id: "sample_01",
    title: "Sample 01 - Reference Tank Stream",
    category: "macro",
    resolution: "640x480",
    depth_m: 17.19,
    noise_type: "Poisson",
    clahe_clip: 1.40,
    dbscan_eps: 35.0,
    avg_shrimp: 10.4,
    peak_clusters: 1,
    density_category: "Baseline",
    feeder_target: [320, 240],
    video_src: "videos/sample_01_processed.mp4",
    snapshot: "assets/sample_01_processed_frame.jpg",
    raw: "assets/sample_01_processed_frame.jpg",
    enhanced: "assets/sample_01_processed_frame.jpg",
    annotated: "assets/sample_01_processed_frame.jpg",
    transmission_err: 1,
    disparity_mean: 6.09,
    reflection_sum: 4534,
    complexity_score: 0.694
  }
];

let currentVideo = VIDEO_DATA[0];
let activeView = "video";
let activeFilter = "all";
let searchTerm = "";
let radarAnimationId = null;
let feedDropAnimationId = null;
let isDispensing = false;

// Audio Context for Feeder Chime (Web Audio API)
let audioCtx = null;
function playFeederChime() {
  try {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); // D5
    osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.15); // A5
    gain.gain.setValueAtTime(0.18, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.35);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.36);
  } catch (e) {
    // Audio optional
  }
}

// Initialization
document.addEventListener("DOMContentLoaded", () => {
  renderSidebarList();
  renderSummaryTable();
  selectVideo(VIDEO_DATA[0].id);
  setupViewControls();
  setupVideoPlaybackControls();
  setupFilterControls();
  setupFeederControls();
  setupBenchmarkModal();
  setupExportAudit();
});

// Render Sidebar List with Category and Search Filter
function renderSidebarList() {
  const container = document.getElementById("videoListContainer");
  container.innerHTML = "";

  const filtered = VIDEO_DATA.filter(v => {
    const matchesFilter = activeFilter === "all" || v.category === activeFilter;
    const matchesSearch = searchTerm === "" || 
      v.id.toLowerCase().includes(searchTerm) || 
      v.title.toLowerCase().includes(searchTerm) ||
      v.noise_type.toLowerCase().includes(searchTerm);
    return matchesFilter && matchesSearch;
  });

  document.getElementById("streamCountBadge").innerText = `${filtered.length} Active`;

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="padding: 1.5rem; text-align: center; color: var(--text-muted); font-size: 0.8rem;">
        No video streams matching current filter.
      </div>
    `;
    return;
  }

  filtered.forEach(v => {
    const item = document.createElement("div");
    item.className = `video-item ${v.id === currentVideo.id ? "selected" : ""}`;
    item.id = `item-${v.id}`;
    item.onclick = () => selectVideo(v.id);

    item.innerHTML = `
      <div class="video-item-info">
        <h4>${v.id.toUpperCase()}</h4>
        <span>${v.title}</span>
      </div>
      <div class="video-metrics-chips">
        <span class="chip cyan">${Math.round(v.avg_shrimp)} shrimp</span>
        <span class="chip green">${v.peak_clusters} clusters</span>
      </div>
    `;
    container.appendChild(item);
  });
}

// Select Active Sector Video
function selectVideo(videoId) {
  const found = VIDEO_DATA.find(v => v.id === videoId);
  if (!found) return;

  currentVideo = found;

  document.querySelectorAll(".video-item").forEach(el => el.classList.remove("selected"));
  const activeEl = document.getElementById(`item-${videoId}`);
  if (activeEl) activeEl.classList.add("selected");

  // Highlight row in summary table
  document.querySelectorAll("#summaryTableBody tr").forEach(tr => {
    tr.classList.toggle("active-row", tr.dataset.videoId === videoId);
  });

  // Calculate biomass feed dosage: ~3.8g pellets per verified shrimp per feeding session
  const shrimpPop = Math.max(1, Math.round(currentVideo.avg_shrimp));
  const doseGrams = (shrimpPop * 3.8).toFixed(1);

  // Update Header & KPIs
  document.getElementById("activeVideoTitle").innerText = `${currentVideo.id.toUpperCase()}: ${currentVideo.title}`;
  document.getElementById("kpiTotalShrimp").innerText = shrimpPop.toLocaleString();
  document.getElementById("kpiActiveSchools").innerText = currentVideo.peak_clusters;
  document.getElementById("kpiSchoolType").innerText = currentVideo.peak_clusters > 0 ? "DBSCAN Hulls" : "Solitary/Pair";
  document.getElementById("kpiDepth").innerText = `${currentVideo.depth_m.toFixed(1)} m`;
  document.getElementById("kpiEpsScale").innerText = `ε: ${currentVideo.dbscan_eps.toFixed(1)}px`;
  document.getElementById("kpiFeederTarget").innerText = `(${currentVideo.feeder_target[0]}, ${currentVideo.feeder_target[1]})`;
  document.getElementById("kpiFeederDose").innerText = `${doseGrams}g`;

  // Update Telemetry Cards
  document.getElementById("telemetryDepth").innerText = `${currentVideo.depth_m.toFixed(2)} m`;
  document.getElementById("telemetryDisparity").innerText = `${currentVideo.disparity_mean.toFixed(2)} px`;
  document.getElementById("telemetryNoise").innerText = currentVideo.noise_type;
  document.getElementById("telemetryKernel").innerText = getKernelName(currentVideo.noise_type);
  document.getElementById("telemetryErrors").innerText = `${currentVideo.transmission_err} pkts`;
  document.getElementById("telemetryClip").innerText = currentVideo.clahe_clip.toFixed(2);
  document.getElementById("telemetryReflection").innerText = currentVideo.reflection_sum.toLocaleString();
  document.getElementById("telemetryEps").innerText = `${currentVideo.dbscan_eps.toFixed(1)} px`;
  document.getElementById("telemetryComplexity").innerText = currentVideo.complexity_score.toFixed(3);

  // Update Feeder Recommendation Banner
  document.getElementById("feederRecText").innerText = 
    `Targeting biomass concentration in ${currentVideo.id.toUpperCase()} at coordinates (${currentVideo.feeder_target[0]}, ${currentVideo.feeder_target[1]}). Verified school population: ${shrimpPop} shrimp.`;
  document.getElementById("feederDoseAmount").innerText = `${doseGrams} g`;

  // Update Active Media View
  updateMediaView();
}

function getKernelName(noiseType) {
  const n = String(noiseType).toLowerCase();
  if (n.includes("salt") || n.includes("impulse")) return "Median Blur (5x5)";
  if (n.includes("poisson")) return "Gaussian Blur (5x5)";
  return "Bilateral Edge Filter (d=7)";
}

// Media Viewport Switcher
function updateMediaView() {
  const videoPane = document.getElementById("videoView");
  const trackingPane = document.getElementById("trackingView");
  const comparePane = document.getElementById("compareView");
  const radarPane = document.getElementById("radarView");
  const playbackToolbar = document.getElementById("playbackToolbar");

  // Hide all panes
  [videoPane, trackingPane, comparePane, radarPane].forEach(p => p.classList.remove("active"));
  stopRadar();

  const video = document.getElementById("streamVideo");

  if (activeView === "video") {
    videoPane.classList.add("active");
    playbackToolbar.style.display = "flex";

    if (video.getAttribute("data-loaded-id") !== currentVideo.id) {
      video.src = currentVideo.video_src;
      video.setAttribute("data-loaded-id", currentVideo.id);
      video.load();
      video.play().catch(() => {});
    }
  } else if (activeView === "tracking") {
    trackingPane.classList.add("active");
    playbackToolbar.style.display = "none";
    document.getElementById("annotatedImage").src = currentVideo.snapshot;
  } else if (activeView === "compare") {
    comparePane.classList.add("active");
    playbackToolbar.style.display = "none";
    document.getElementById("rawImg").src = currentVideo.raw;
    document.getElementById("enhancedImg").src = currentVideo.enhanced;
    document.getElementById("annotatedImg").src = currentVideo.annotated;
  } else if (activeView === "radar") {
    radarPane.classList.add("active");
    playbackToolbar.style.display = "none";
    startRadar();
  }
}

function setupViewControls() {
  const buttons = document.querySelectorAll(".view-btn");
  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeView = btn.dataset.view;
      updateMediaView();
    });
  });
}

// Video Playback Controls Bar
function setupVideoPlaybackControls() {
  const video = document.getElementById("streamVideo");
  const btnPlayPause = document.getElementById("btnPlayPause");
  const playIcon = document.getElementById("playIcon");
  const btnRestart = document.getElementById("btnRestart");
  const scrubber = document.getElementById("timelineScrubber");
  const timeReadout = document.getElementById("timeReadout");
  const btnFullscreen = document.getElementById("btnFullscreen");
  const speedButtons = document.querySelectorAll(".speed-btn");

  btnPlayPause.addEventListener("click", () => {
    if (video.paused) {
      video.play();
      playIcon.innerText = "⏸";
    } else {
      video.pause();
      playIcon.innerText = "▶";
    }
  });

  video.addEventListener("play", () => { playIcon.innerText = "⏸"; });
  video.addEventListener("pause", () => { playIcon.innerText = "▶"; });

  btnRestart.addEventListener("click", () => {
    video.currentTime = 0;
    video.play();
  });

  video.addEventListener("timeupdate", () => {
    if (!isNaN(video.duration) && video.duration > 0) {
      const progress = (video.currentTime / video.duration) * 100;
      scrubber.value = progress;
      timeReadout.innerText = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
    }
  });

  scrubber.addEventListener("input", () => {
    if (!isNaN(video.duration) && video.duration > 0) {
      video.currentTime = (scrubber.value / 100) * video.duration;
    }
  });

  speedButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      speedButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      video.playbackRate = parseFloat(btn.dataset.speed);
    });
  });

  btnFullscreen.addEventListener("click", () => {
    const viewport = document.getElementById("mediaViewport");
    if (!document.fullscreenElement) {
      viewport.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  });
}

function formatTime(secs) {
  const m = Math.floor(secs / 60);
  const s = Math.floor(secs % 60);
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

// Quick Filter Chips & Search Bar
function setupFilterControls() {
  const chips = document.querySelectorAll(".filter-chip");
  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      chips.forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      activeFilter = chip.dataset.filter;
      renderSidebarList();
    });
  });

  const searchInput = document.getElementById("sectorSearchInput");
  searchInput.addEventListener("input", (e) => {
    searchTerm = e.target.value.toLowerCase().trim();
    renderSidebarList();
  });
}

// 2D Swarm Radar Map with Concentric Range Rings & Sweep Line
let radarParticles = [];
let radarAngle = 0;

function initRadarParticles() {
  radarParticles = [];
  const count = Math.max(Math.min(Math.round(currentVideo.avg_shrimp), 60), 4);
  const targetX = currentVideo.feeder_target[0];
  const targetY = currentVideo.feeder_target[1];

  for (let i = 0; i < count; i++) {
    const angle = Math.random() * Math.PI * 2;
    const dist = Math.random() * currentVideo.dbscan_eps * 1.1;
    radarParticles.push({
      x: targetX + Math.cos(angle) * dist,
      y: targetY + Math.sin(angle) * dist,
      vx: (Math.random() - 0.5) * 0.9,
      vy: (Math.random() - 0.5) * 0.9,
      isClustered: i < (currentVideo.peak_clusters * 6),
      size: 3 + Math.random() * 2
    });
  }
}

function startRadar() {
  const canvas = document.getElementById("radarCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;

  initRadarParticles();

  function drawRadar() {
    ctx.fillStyle = "rgba(4, 8, 16, 0.18)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const cx = canvas.width / 2;
    const cy = canvas.height / 2;
    const maxRadius = Math.min(cx, cy) * 0.88;

    // 1. Draw Concentric Sonar Rings
    ctx.strokeStyle = "rgba(0, 242, 254, 0.15)";
    ctx.lineWidth = 1;
    for (let r = 1; r <= 4; r++) {
      ctx.beginPath();
      ctx.arc(cx, cy, (maxRadius / 4) * r, 0, Math.PI * 2);
      ctx.stroke();

      // Distance labels
      ctx.fillStyle = "rgba(0, 242, 254, 0.4)";
      ctx.font = "9px 'JetBrains Mono'";
      ctx.fillText(`${(r * 5)}m`, cx + (maxRadius / 4) * r - 20, cy - 6);
    }

    // Crosshairs
    ctx.strokeStyle = "rgba(0, 242, 254, 0.1)";
    ctx.beginPath();
    ctx.moveTo(cx, cy - maxRadius);
    ctx.lineTo(cx, cy + maxRadius);
    ctx.moveTo(cx - maxRadius, cy);
    ctx.lineTo(cx + maxRadius, cy);
    ctx.stroke();

    // 2. Rotating Radar Sweep Beam
    radarAngle += 0.025;
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(radarAngle);

    const grad = ctx.createRadialGradient(0, 0, 0, 0, 0, maxRadius);
    grad.addColorStop(0, "rgba(0, 242, 254, 0.35)");
    grad.addColorStop(1, "rgba(0, 242, 254, 0.0)");

    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.arc(0, 0, maxRadius, -0.25, 0);
    ctx.closePath();
    ctx.fill();

    ctx.strokeStyle = "rgba(0, 242, 254, 0.8)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(maxRadius, 0);
    ctx.stroke();
    ctx.restore();

    // 3. Feeder Target Reticle (scaled to canvas)
    const normX = (currentVideo.feeder_target[0] / 1500) * canvas.width;
    const normY = (currentVideo.feeder_target[1] / 900) * canvas.height;

    ctx.strokeStyle = "rgba(245, 158, 11, 0.8)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(normX, normY, 14 + Math.sin(Date.now() / 200) * 3, 0, Math.PI * 2);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(normX - 8, normY);
    ctx.lineTo(normX + 8, normY);
    ctx.moveTo(normX, normY - 8);
    ctx.lineTo(normX, normY + 8);
    ctx.stroke();

    // 4. Shrimp Swarm Blips
    radarParticles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;

      if (Math.abs(p.x - currentVideo.feeder_target[0]) > currentVideo.dbscan_eps * 1.5) p.vx *= -1;
      if (Math.abs(p.y - currentVideo.feeder_target[1]) > currentVideo.dbscan_eps * 1.5) p.vy *= -1;

      const px = (p.x / 1500) * canvas.width;
      const py = (p.y / 900) * canvas.height;

      ctx.fillStyle = p.isClustered ? "rgba(16, 185, 129, 0.9)" : "rgba(0, 242, 254, 0.9)";
      ctx.shadowColor = p.isClustered ? "#10b981" : "#00f2fe";
      ctx.shadowBlur = 8;
      ctx.beginPath();
      ctx.arc(px, py, p.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;
    });

    radarAnimationId = requestAnimationFrame(drawRadar);
  }

  drawRadar();
}

function stopRadar() {
  if (radarAnimationId) {
    cancelAnimationFrame(radarAnimationId);
    radarAnimationId = null;
  }
}

// Precision Feeder Simulation & Particle Drop Animation
function setupFeederControls() {
  const triggerBtn = document.getElementById("triggerFeederBtn");
  const statusTag = document.getElementById("feederStatusTag");

  triggerBtn.addEventListener("click", () => {
    if (isDispensing) return;
    isDispensing = true;

    playFeederChime();

    statusTag.innerText = "DISPENSING BATCH...";
    statusTag.className = "feeder-status-tag dispensing";
    triggerBtn.disabled = true;

    // Trigger visual pellet drop on canvas
    startFeedDropAnimation(() => {
      statusTag.innerText = "FEEDING COMPLETE ✓";
      statusTag.className = "feeder-status-tag";
      
      setTimeout(() => {
        statusTag.innerText = "READY FOR DEPLOYMENT";
        triggerBtn.disabled = false;
        isDispensing = false;
      }, 2500);
    });
  });
}

function startFeedDropAnimation(onComplete) {
  const canvas = document.getElementById("feedDropCanvas");
  if (!canvas) { onComplete(); return; }
  const ctx = canvas.getContext("2d");

  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;

  const targetX = (currentVideo.feeder_target[0] / 1500) * canvas.width;
  const targetY = (currentVideo.feeder_target[1] / 900) * canvas.height;

  const pellets = [];
  for (let i = 0; i < 45; i++) {
    pellets.push({
      x: targetX + (Math.random() - 0.5) * 50,
      y: -20 - Math.random() * 120,
      targetY: targetY + (Math.random() - 0.5) * 60,
      vy: 4 + Math.random() * 4,
      size: 2.5 + Math.random() * 2,
      opacity: 1
    });
  }

  const ripples = [];

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    let activeCount = 0;

    // Pellets falling
    pellets.forEach(p => {
      if (p.y < p.targetY) {
        p.y += p.vy;
        activeCount++;
        ctx.fillStyle = "#fbbf24";
        ctx.shadowColor = "#f59e0b";
        ctx.shadowBlur = 6;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;

        if (p.y >= p.targetY) {
          ripples.push({ x: p.x, y: p.targetY, r: 2, maxR: 20 + Math.random() * 15, alpha: 0.8 });
        }
      }
    });

    // Ripples expanding on substrate
    for (let i = ripples.length - 1; i >= 0; i--) {
      const rip = ripples[i];
      rip.r += 0.8;
      rip.alpha -= 0.025;

      if (rip.alpha > 0) {
        activeCount++;
        ctx.strokeStyle = `rgba(0, 242, 254, ${rip.alpha})`;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.ellipse(rip.x, rip.y, rip.r * 1.5, rip.r * 0.7, 0, 0, Math.PI * 2);
        ctx.stroke();
      } else {
        ripples.splice(i, 1);
      }
    }

    if (activeCount > 0) {
      feedDropAnimationId = requestAnimationFrame(animate);
    } else {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      onComplete();
    }
  }

  animate();
}

// Render Summary Table & Sorting
function renderSummaryTable() {
  const tbody = document.getElementById("summaryTableBody");
  tbody.innerHTML = "";

  VIDEO_DATA.forEach(v => {
    const tr = document.createElement("tr");
    tr.dataset.videoId = v.id;
    if (v.id === currentVideo.id) tr.classList.add("active-row");

    tr.onclick = () => selectVideo(v.id);

    tr.innerHTML = `
      <td><strong>${v.name}</strong></td>
      <td><span class="chip cyan">${v.id.toUpperCase()}</span></td>
      <td>${v.resolution}</td>
      <td>${v.depth_m.toFixed(2)}m</td>
      <td>${v.noise_type}</td>
      <td>${v.clahe_clip.toFixed(2)}</td>
      <td>${v.dbscan_eps.toFixed(1)}px</td>
      <td><strong>${v.avg_shrimp.toFixed(1)}</strong></td>
      <td>${v.peak_clusters}</td>
      <td><span class="chip green">${v.density_category}</span></td>
      <td>(${v.feeder_target[0]}, ${v.feeder_target[1]})</td>
    `;
    tbody.appendChild(tr);
  });

  // Table Sorting Handlers
  document.getElementById("btnSortCount").addEventListener("click", () => {
    VIDEO_DATA.sort((a, b) => b.avg_shrimp - a.avg_shrimp);
    renderSummaryTable();
    renderSidebarList();
  });

  document.getElementById("btnSortClusters").addEventListener("click", () => {
    VIDEO_DATA.sort((a, b) => b.peak_clusters - a.peak_clusters);
    renderSummaryTable();
    renderSidebarList();
  });
}

// Benchmark Performance Diagnostic Modal
function setupBenchmarkModal() {
  const modal = document.getElementById("benchmarkModal");
  const openBtn = document.getElementById("btnBenchmark");
  const closeBtn = document.getElementById("btnCloseBenchmark");
  const dismissBtn = document.getElementById("btnDismissBenchmark");

  openBtn.addEventListener("click", () => modal.classList.add("active"));
  closeBtn.addEventListener("click", () => modal.classList.remove("active"));
  dismissBtn.addEventListener("click", () => modal.classList.remove("active"));

  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.classList.remove("active");
  });
}

// Export Inspection Audit
function setupExportAudit() {
  const btn = document.getElementById("btnExportAudit");
  btn.addEventListener("click", () => {
    const headers = [
      "video_id", "video_name", "title", "resolution", "depth_m",
      "noise_type", "clahe_clip", "dbscan_eps", "avg_shrimp",
      "peak_clusters", "density_category", "feeder_x", "feeder_y"
    ];

    const rows = VIDEO_DATA.map(v => [
      v.id, v.name, `"${v.title}"`, v.resolution, v.depth_m,
      v.noise_type, v.clahe_clip, v.dbscan_eps, v.avg_shrimp,
      v.peak_clusters, `"${v.density_category}"`, v.feeder_target[0], v.feeder_target[1]
    ]);

    const csvContent = "data:text/csv;charset=utf-8," + 
      [headers.join(","), ...rows.map(r => r.join(","))].join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `aquaeye_audit_ledger_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });
}
