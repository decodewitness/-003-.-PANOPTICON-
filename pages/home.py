HTML_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>UROPS PANOPT | Home</title>
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

    /* FEED 1 */
    .feed1-frame {
      width: 800px;
      height: 650px;
      background: #0b0d12;
      border: 2px solid var(--border);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
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
    }

    .feed1-frame .placeholder {
      color: var(--muted);
      font-size: 14px;
      text-align: center;
      padding: 0 14px;
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
    }

    .feed-desc {
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 8px;
      color: var(--muted);
      font-size: 12px;
    }
  </style>
</head>
<script>
  async function loadFeed(n) {
    const panel = document.querySelector(`.feed-panel[data-feed="${n}"]`);
    if (!panel) return;

    const contentEl = panel.querySelector(".feed-content");
    const descEl = panel.querySelector(".feed-desc");

    try {
      contentEl.textContent = "Loading…";
      const res = await fetch(`/api/feed/${n}`, { cache: "no-store" });
      const data = await res.json();

      if (!res.ok) {
        contentEl.textContent = JSON.stringify(data, null, 2);
        descEl.textContent = `Error loading FEED ${n}.`;
        return;
      }

      // Expecting your placeholder payload to be JSON-friendly.
      // Common patterns: {items:[...], description:"..."} or similar.
      contentEl.textContent = JSON.stringify(data, null, 2);

      if (data && typeof data.description === "string") {
        descEl.textContent = data.description;
      } else {
        descEl.textContent = `Description for FEED ${n}.`;
      }
    } catch (err) {
      contentEl.textContent = String(err);
      descEl.textContent = `Error loading FEED ${n}.`;
    }
  }

  function wirePanels() {
    document.querySelectorAll(".feed-panel").forEach(panel => {
      const n = Number(panel.getAttribute("data-feed"));
      const btn = panel.querySelector(".add-feed");
      if (btn) btn.addEventListener("click", () => loadFeed(n));
    });
  }

  // Initial load feeds 2–6
  window.addEventListener("DOMContentLoaded", () => {
    wirePanels();
    wireGridButtons();
    [2,3,4,5,6].forEach(loadFeed);
  });
</script>
<body>
  <div class="wrap">
    <div class="header">
      <h1>UROPS PANOPT | Home</h1>
      <div class="sub">Prototype UI scaffold (FEED 1 placeholder + FEED 2–6 panels)</div>
    </div>

    <div class="feed1-frame">
      <div class="label">FEED 1</div>
      <div class="placeholder">
        Fixed 800×650 window. Later: replace this area with an image/screencap stream.
      </div>
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
        <input type="text" size="34" placeholder="   - Your Input Here -" />
        <button class="enter-btn">Enter</button>
      </div>
    </div>

    <div class="feeds">
      <div class="feed-panel" data-feed="2">
        <div class="row">
          <div class="title">FEED 2</div>
          <button class="add-feed">Refresh</button>
        </div>
        <div class="feed-content">Loading…</div>
        <div class="feed-desc">Description for FEED 2.</div>
      </div>

      <div class="feed-panel" data-feed="2">
        <div class="row">
          <div class="title">FEED 2</div>
          <button class="add-feed">Refresh</button>
        </div>
        <div class="feed-content">Loading…</div>
        <div class="feed-desc">Description for FEED 2.</div>
      </div>

      <div class="feed-panel" data-feed="2">
        <div class="row">
          <div class="title">FEED 2</div>
          <button class="add-feed">Refresh</button>
        </div>
        <div class="feed-content">Loading…</div>
        <div class="feed-desc">Description for FEED 2.</div>
      </div>

      <div class="feed-panel" data-feed="2">
        <div class="row">
          <div class="title">FEED 2</div>
          <button class="add-feed">Refresh</button>
        </div>
        <div class="feed-content">Loading…</div>
        <div class="feed-desc">Description for FEED 2.</div>
      </div>

      <div class="feed-panel" data-feed="2">
        <div class="row">
          <div class="title">FEED 2</div>
          <button class="add-feed">Refresh</button>
        </div>
        <div class="feed-content">Loading…</div>
        <div class="feed-desc">Description for FEED 2.</div>
      </div>
    </div>
  </div>
  async function sendAction(action, payload) {
    // This will 404 until you implement it server-side; that’s fine for now.
    const res = await fetch("/api/action", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ action, payload })
    });
    return res.json().catch(() => ({}));
  }

  function wireGridButtons() {
    document.querySelectorAll(".btn[data-action]").forEach(btn => {
      btn.addEventListener("click", async () => {
        const action = btn.getAttribute("data-action");
        btn.disabled = true;
        try {
          await sendAction(action, null);
        } finally {
          btn.disabled = false;
        }
      });
    });
  }
</body>
</html>
"""
