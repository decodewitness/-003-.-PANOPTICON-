# pages/home.py

HTML_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>UROPS PANOPT | Home</title>

  <!-- CesiumJS (renderer for Google Photorealistic 3D Tiles) -->
  <script src="https://ajax.googleapis.com/ajax/libs/cesiumjs/1.105/Build/Cesium/Cesium.js"></script>
  <link href="https://ajax.googleapis.com/ajax/libs/cesiumjs/1.105/Build/Cesium/Widgets/widgets.css" rel="stylesheet">

  <style>
    :root {
      --bg: #0f1115;
      --panel: #151924;
      --border: #2a3142;
      --text: #e8ecf5;
      --muted: #aeb6c7;
      --btn: #1d2434;
      --btnHover: #26304a;
      --accent: #3b82f6;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .wrap {
      width: 100%;
      max-width: 1000px;
      padding: 20px 16px 30px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .header {
      width: 100%;
      text-align: center;
      border-bottom: 1px solid var(--border);
      padding-bottom: 10px;
      margin-bottom: 20px;
    }

    .header h1 {
      margin: 0;
      font-size: 18px;
      font-weight: 650;
    }

    .header .sub {
      color: var(--muted);
      font-size: 12px;
      margin-top: 4px;
    }

    /* FEED 1 (Cesium container) */
    .feed1-frame {
      width: 800px;
      height: 650px;
      background: #0b0d12;
      border: 2px solid var(--border);
      border-radius: 10px;
      position: relative;
      overflow: hidden;
      margin-bottom: 16px;
    }

    .feed1-frame .label {
      position: absolute;
      top: 10px;
      left: 12px;
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: rgba(21,25,36,0.7);
      font-size: 12px;
      color: var(--muted);
      z-index: 5;
      pointer-events: none;
    }

    #cesiumContainer {
      width: 100%;
      height: 100%;
    }

    /* Controls */
    .controls {
      width: 800px;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 16px;
      margin-bottom: 30px;
      flex-wrap: wrap;
    }

    .grid-buttons {
      display: grid;
      grid-template-columns: repeat(12, 60px);
      gap: 8px;
      justify-content: center;
    }

    .btn {
      height: 42px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--btn);
      color: var(--text);
      cursor: pointer;
      font-weight: 600;
    }

    .btn:hover { background: var(--btnHover); }

    .enter-area {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .enter-btn {
      height: 42px;
      padding: 0 14px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--accent);
      color: white;
      cursor: pointer;
      font-weight: 700;
    }

    input[type="text"] {
      height: 42px;
      width: 21ch;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #0b0d12;
      color: var(--text);
      padding: 0 10px;
    }

    /* Lower feeds */
    .feeds {
      width: 800px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;
    }

    .feed-panel {
      width: 100%;
      border: 2px solid var(--border);
      background: var(--panel);
      border-radius: 10px;
      padding: 12px;
      text-align: center;
    }

    .feed-panel .row {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 12px;
      margin-bottom: 10px;
    }

    .feed-panel .title {
      font-weight: 700;
    }

    .add-feed {
      height: 32px;
      padding: 0 12px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #0b0d12;
      color: var(--text);
      cursor: pointer;
    }

    .feed-content {
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #0b0d12;
      padding: 10px;
      min-height: 70px;
      font-family: monospace;
      font-size: 12px;
      margin-bottom: 10px;
      white-space: pre-wrap;
      text-align: left;
    }

    .feed-desc {
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 8px;
      color: var(--muted);
      font-size: 12px;
      text-align: left;
    }
  </style>

  <script>
    // Injected server-side from panopt.py
    const GMP_MAP_TILES_API_KEY = "__GMP_MAP_TILES_API_KEY__";

    async function sendAction(action, payload) {
      const res = await fetch("/api/action", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ action, payload })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error((data && data.error) ? data.error : ("HTTP " + res.status));
      return data;
    }

    async function loadFeed(n) {
      const panel = document.querySelector('.feed-panel[data-feed="' + n + '"]');
      if (!panel) return;

      const contentEl = panel.querySelector(".feed-content");
      const descEl = panel.querySelector(".feed-desc");

      try {
        contentEl.textContent = "Loading…";
        const res = await fetch("/api/feed/" + n, { cache: "no-store" });
        const data = await res.json().catch(() => ({}));

        if (!res.ok) {
          contentEl.textContent = JSON.stringify(data, null, 2);
          descEl.textContent = "Error loading FEED " + n + ".";
          return;
        }

        contentEl.textContent = JSON.stringify(data, null, 2);
        descEl.textContent = (data && typeof data.description === "string")
          ? data.description
          : ("Description for FEED " + n + ".");
      } catch (err) {
        contentEl.textContent = String(err);
        descEl.textContent = "Error loading FEED " + n + ".";
      }
    }

    function wirePanels() {
      document.querySelectorAll(".feed-panel").forEach(panel => {
        const n = Number(panel.getAttribute("data-feed"));
        const btn = panel.querySelector(".add-feed");
        if (btn) btn.addEventListener("click", () => loadFeed(n));
      });
    }

    function wireGridButtons() {
      document.querySelectorAll(".btn[data-action]").forEach(btn => {
        btn.addEventListener("click", async () => {
          const action = btn.getAttribute("data-action");
          btn.disabled = true;
          try {
            await sendAction(action, null);
          } catch (e) {
            console.error(e);
          } finally {
            btn.disabled = false;
          }
        });
      });
    }

    function wireEnter() {
      const input = document.getElementById("enter-input");
      const enterBtn = document.getElementById("enter-btn");

      async function submit() {
        const text = (input.value || "").trim();
        if (!text) return;
        enterBtn.disabled = true;
        try {
          await sendAction("ENTER", { text });
          input.value = "";
        } catch (e) {
          console.error(e);
        } finally {
          enterBtn.disabled = false;
        }
      }

      enterBtn.addEventListener("click", submit);
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") submit(); });
    }

    async function initFeed1Cesium() {
      const label = document.querySelector(".feed1-frame .label");
      const setStatus = (s) => { if (label) label.textContent = s; };

      try {
        if (!GMP_MAP_TILES_API_KEY || GMP_MAP_TILES_API_KEY.includes("REPLACE_ME")) {
          setStatus("FEED 1 (missing API key)");
          return;
        }

        // IMPORTANT: stop Cesium from attempting Ion defaults
        Cesium.Ion.defaultAccessToken = undefined;

        const container = document.getElementById("cesiumContainer");
        if (!container) {
          setStatus("FEED 1 (missing #cesiumContainer)");
          return;
        }

        setStatus("FEED 1 (initializing…)");

        // Google Photorealistic 3D Tiles root tileset
        const rootUrl =
          "https://tile.googleapis.com/v1/3dtiles/root.json?key=" +
          encodeURIComponent(GMP_MAP_TILES_API_KEY);

        // Probe root.json so we get the real HTTP error in-console
        const probeRes = await fetch(rootUrl, { cache: "no-store" });
        if (!probeRes.ok) {
          const txt = await probeRes.text().catch(() => "");
          setStatus(`FEED 1 (root.json HTTP ${probeRes.status})`);
          console.error("root.json error:", probeRes.status, txt);
          return;
        }

        // Create a Viewer with NO base layers / NO terrain (prevents Ion calls)
        const viewer = new Cesium.Viewer(container, {
          baseLayer: false,                 // Cesium >=1.104 way to disable base layer
          baseLayerPicker: false,
          terrain: new Cesium.EllipsoidTerrainProvider(), // no Ion terrain
          geocoder: false,
          homeButton: false,
          sceneModePicker: false,
          navigationHelpButton: false,
          fullscreenButton: false,
          animation: false,
          timeline: false,
          infoBox: false,
          selectionIndicator: false,
          requestRenderMode: false
        });

        // Clean background (no “space” UI)
        viewer.scene.globe.show = false;
        viewer.scene.skyBox.show = false;
        viewer.scene.sun.show = false;
        viewer.scene.moon.show = false;
        viewer.scene.backgroundColor = Cesium.Color.fromCssColorString("#0b0d12");

        // Statue of Liberty
        const lat = 40.6892494;
        const lon = -74.0445004;

        viewer.camera.setView({
          destination: Cesium.Cartesian3.fromDegrees(lon, lat, 2500.0),
          orientation: {
            heading: Cesium.Math.toRadians(20.0),
            pitch: Cesium.Math.toRadians(-35.0),
            roll: 0.0
          }
        });

        setStatus("FEED 1 (loading tiles…)");

        // Modern Cesium API (fixes deprecations)
        const tileset = await Cesium.Cesium3DTileset.fromUrl(rootUrl, {
          showCreditsOnScreen: true
        });

        // Add tileset after it resolves
        viewer.scene.primitives.add(tileset);

        setStatus("FEED 1 (tiles loaded)");

        viewer.camera.flyTo({
          destination: Cesium.Cartesian3.fromDegrees(lon, lat, 900.0),
          orientation: {
            heading: Cesium.Math.toRadians(20.0),
            pitch: Cesium.Math.toRadians(-40.0),
            roll: 0.0
          },
          duration: 1.5
        });

        window.__viewer = viewer;
        window.__tileset = tileset;
      } catch (e) {
        setStatus("FEED 1 (init error)");
        console.error("FEED 1 init error:", e);
      }
    }

    window.addEventListener("DOMContentLoaded", () => {
      wirePanels();
      wireGridButtons();
      wireEnter();

      initFeed1Cesium();

      [2,3,4,5,6].forEach(loadFeed);
      setInterval(() => [2,3,4,5,6].forEach(loadFeed), 5000);
    });
  </script>
</head>

<body>
  <div class="wrap">
    <div class="header">
      <h1>UROPS PANOPT | Home</h1>
      <div class="sub">Prototype UI scaffold (FEED 1: Google Photorealistic 3D Tiles via Cesium + FEED 2–6 panels)</div>
    </div>

    <div class="feed1-frame">
      <div class="label">FEED 1</div>
      <div id="cesiumContainer"></div>
    </div>

    <div class="controls">
      <div class="grid-buttons">
        <button class="btn" data-action="A1">A1</button>
        <button class="btn" data-action="A2">A2</button>
        <button class="btn" data-action="A3">A3</button>
        <button class="btn" data-action="B1">B1</button>
        <button class="btn" data-action="B2">B2</button>
        <button class="btn" data-action="B3">B3</button>
        <button class="btn" data-action="C1">C1</button>
        <button class="btn" data-action="C2">C2</button>
        <button class="btn" data-action="C3">C3</button>
        <button class="btn" data-action="D1">D1</button>
        <button class="btn" data-action="D2">D2</button>
        <button class="btn" data-action="D3">D3</button>
      </div>

      <div class="enter-area">
        <input id="enter-input" type="text" size="34" placeholder="   - Your Input Here -" />
        <button id="enter-btn" class="enter-btn">Enter</button>
      </div>
    </div>

    <div class="feeds">
      <div class="feed-panel" data-feed="2">
        <div class="row"><div class="title">FEED 2</div><button class="add-feed">Refresh</button></div>
        <div class="feed-content">Loading…</div>
        <div class="feed-desc">Description for FEED 2.</div>
      </div>

      <div class="feed-panel" data-feed="3">
        <div class="row"><div class="title">FEED 3</div><button class="add-feed">Refresh</button></div>
        <div class="feed-content">Loading…</div>
        <div class="feed-desc">Description for FEED 3.</div>
      </div>

      <div class="feed-panel" data-feed="4">
        <div class="row"><div class="title">FEED 4</div><button class="add-feed">Refresh</button></div>
        <div class="feed-content">Loading…</div>
        <div class="feed-desc">Description for FEED 4.</div>
      </div>

      <div class="feed-panel" data-feed="5">
        <div class="row"><div class="title">FEED 5</div><button class="add-feed">Refresh</button></div>
        <div class="feed-content">Loading…</div>
        <div class="feed-desc">Description for FEED 5.</div>
      </div>

      <div class="feed-panel" data-feed="6">
        <div class="row"><div class="title">FEED 6</div><button class="add-feed">Refresh</button></div>
        <div class="feed-content">Loading…</div>
        <div class="feed-desc">Description for FEED 6.</div>
      </div>
    </div>
  </div>
</body>
</html>
"""