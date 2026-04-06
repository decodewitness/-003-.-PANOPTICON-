# pages/home.py

HTML_PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>UROPS PANOPT | Home</title>
  <link rel="icon" href="/favicon.ico" type="image/x-icon">
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
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    }

    .wrap {
      width: 100%;
      max-width: 1800px;
      margin: 0 auto;
      padding: 20px 16px 30px;
    }

    .header {
      text-align: center;
      border-bottom: 1px solid var(--border);
      padding-bottom: 12px;
      margin-bottom: 18px;
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

    .topbar {
      border: 2px solid var(--border);
      background: var(--panel);
      border-radius: 12px;
      padding: 12px;
      margin-bottom: 16px;
    }

    .topbar-row {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
      justify-content: space-between;
    }

    .topbar-left, .topbar-right {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }

    .label-inline {
      font-size: 12px;
      color: var(--muted);
    }

    .count-box {
      display: flex;
      align-items: center;
      gap: 8px;
      border: 1px solid var(--border);
      background: #0b0d12;
      border-radius: 10px;
      padding: 8px 10px;
    }

    .count-box input {
      width: 70px;
      height: 34px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #0b0d12;
      color: var(--text);
      padding: 0 8px;
      text-align: center;
    }

    .view-mode-group {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .btn, .small-btn, .search-btn {
      border: 1px solid var(--border);
      background: var(--btn);
      color: var(--text);
      cursor: pointer;
      font-weight: 600;
      border-radius: 8px;
    }

    .btn:hover, .small-btn:hover, .search-btn:hover {
      background: var(--btnHover);
    }

    .btn.active {
      background: var(--accent);
      color: white;
    }

    .small-btn {
      height: 34px;
      min-width: 34px;
      padding: 0 10px;
    }

    .btn {
      height: 38px;
      padding: 0 12px;
    }

    .feeds-grid {
      display: grid;
      gap: 14px;
    }

    .feeds-grid.cols-1 { grid-template-columns: 1fr; }
    .feeds-grid.cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .feeds-grid.cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }

    .feed-card {
      border: 2px solid var(--border);
      background: var(--panel);
      border-radius: 12px;
      padding: 10px;
      min-width: 0;
    }

    .feed-card.hidden {
      display: none;
    }

    .feed-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      margin-bottom: 8px;
      flex-wrap: wrap;
    }

    .feed-title {
      font-weight: 700;
      font-size: 14px;
    }

    .feed-actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .viewer-frame {
      width: 100%;
      height: 380px;
      background: #0b0d12;
      border: 2px solid var(--border);
      border-radius: 10px;
      position: relative;
      overflow: hidden;
      margin-bottom: 10px;
    }

    .viewer-label {
      position: absolute;
      top: 10px;
      left: 12px;
      padding: 6px 10px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: rgba(21, 25, 36, 0.72);
      font-size: 12px;
      color: var(--muted);
      z-index: 5;
      pointer-events: none;
    }

    .viewer-container {
      width: 100%;
      height: 100%;
    }

    .feed-search-wrap {
      position: relative;
      margin-bottom: 8px;
    }

    .feed-search-row {
      display: flex;
      gap: 8px;
    }

    .feed-search-input {
      flex: 1;
      height: 38px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #0b0d12;
      color: var(--text);
      padding: 0 10px;
    }

    .search-btn {
      height: 38px;
      padding: 0 12px;
      background: var(--accent);
      color: white;
      font-weight: 700;
    }

    .autocomplete-list {
      position: absolute;
      top: calc(100% + 6px);
      left: 0;
      right: 0;
      z-index: 20;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: #0b0d12;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
      overflow: hidden;
      max-height: 280px;
      overflow-y: auto;
      display: none;
    }

    .autocomplete-list.open {
      display: block;
    }

    .autocomplete-item {
      width: 100%;
      border: 0;
      border-bottom: 1px solid rgba(42, 49, 66, 0.75);
      background: transparent;
      color: var(--text);
      padding: 10px 12px;
      text-align: left;
      cursor: pointer;
      display: block;
    }

    .autocomplete-item:last-child {
      border-bottom: 0;
    }

    .autocomplete-item:hover,
    .autocomplete-item.active {
      background: var(--btnHover);
    }

    .autocomplete-item .name {
      display: block;
      font-size: 13px;
      font-weight: 700;
      margin-bottom: 2px;
    }

    .autocomplete-item .meta {
      display: block;
      font-size: 11px;
      color: var(--muted);
    }

    .feed-help {
      font-size: 11px;
      color: var(--muted);
      margin-bottom: 8px;
    }

    .location-list {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
      max-height: 220px;
      overflow-y: auto;
      padding-right: 2px;
    }

    .location-item {
      border: 1px solid var(--border);
      border-radius: 8px;
      background: #0b0d12;
      color: var(--text);
      padding: 9px 10px;
      text-align: left;
      cursor: pointer;
      font-size: 12px;
      line-height: 1.3;
    }

    .location-item:hover {
      background: var(--btnHover);
    }

    .location-item .loc-name {
      font-weight: 700;
      display: block;
      margin-bottom: 2px;
    }

    .location-item .loc-meta {
      color: var(--muted);
      font-size: 11px;
    }

    .location-empty {
      border: 1px dashed var(--border);
      border-radius: 8px;
      padding: 12px;
      color: var(--muted);
      font-size: 12px;
      text-align: center;
      grid-column: 1 / -1;
    }

    .controls {
      border: 2px solid var(--border);
      background: var(--panel);
      border-radius: 12px;
      padding: 12px;
      margin-top: 18px;
      margin-bottom: 18px;
    }

    .controls-row {
      display: flex;
      gap: 16px;
      flex-wrap: wrap;
      justify-content: center;
      align-items: center;
    }

    .grid-buttons {
      display: grid;
      grid-template-columns: repeat(12, 60px);
      gap: 8px;
      justify-content: center;
    }

    .enter-area {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    .enter-area input {
      height: 42px;
      width: 28ch;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #0b0d12;
      color: var(--text);
      padding: 0 10px;
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

    .json-feeds {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 14px;
    }

    .json-feed-card {
      border: 2px solid var(--border);
      background: var(--panel);
      border-radius: 12px;
      padding: 12px;
    }

    .json-feed-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      margin-bottom: 10px;
    }

    .json-feed-title {
      font-weight: 700;
      font-size: 14px;
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

    @media (max-width: 1300px) {
      .feeds-grid.cols-3 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }

    @media (max-width: 900px) {
      .feeds-grid.cols-2,
      .feeds-grid.cols-3 { grid-template-columns: 1fr; }

      .location-list {
        grid-template-columns: 1fr;
      }

      .grid-buttons {
        grid-template-columns: repeat(6, 60px);
      }
    }
  </style>

  <script>
    const GMP_MAP_TILES_API_KEY = "__GMP_MAP_TILES_API_KEY__";
    const MAX_FEEDS = 33;

    const COUNTRY_SHOW_HEIGHT = 14000000.0;
    const CITY_SHOW_HEIGHT = 1600000.0;
    const SELECTED_SHOW_HEIGHT = 1600000.0;

    const WORLD_CITIES = [
      { name: "Amsterdam", country: "Netherlands", lat: 52.3676, lon: 4.9041 },
      { name: "Rotterdam", country: "Netherlands", lat: 51.9244, lon: 4.4777 },
      { name: "The Hague", country: "Netherlands", lat: 52.0705, lon: 4.3007 },
      { name: "Brussels", country: "Belgium", lat: 50.8503, lon: 4.3517 },
      { name: "Paris", country: "France", lat: 48.8566, lon: 2.3522 },
      { name: "London", country: "United Kingdom", lat: 51.5072, lon: -0.1276 },
      { name: "Berlin", country: "Germany", lat: 52.5200, lon: 13.4050 },
      { name: "Madrid", country: "Spain", lat: 40.4168, lon: -3.7038 },
      { name: "Rome", country: "Italy", lat: 41.9028, lon: 12.4964 },
      { name: "Vienna", country: "Austria", lat: 48.2082, lon: 16.3738 },
      { name: "Prague", country: "Czechia", lat: 50.0755, lon: 14.4378 },
      { name: "Warsaw", country: "Poland", lat: 52.2297, lon: 21.0122 },
      { name: "Athens", country: "Greece", lat: 37.9838, lon: 23.7275 },
      { name: "Istanbul", country: "Turkey", lat: 41.0082, lon: 28.9784 },
      { name: "Cairo", country: "Egypt", lat: 30.0444, lon: 31.2357 },
      { name: "Nairobi", country: "Kenya", lat: -1.2921, lon: 36.8219 },
      { name: "Lagos", country: "Nigeria", lat: 6.5244, lon: 3.3792 },
      { name: "Johannesburg", country: "South Africa", lat: -26.2041, lon: 28.0473 },
      { name: "Dubai", country: "UAE", lat: 25.2048, lon: 55.2708 },
      { name: "Mumbai", country: "India", lat: 19.0760, lon: 72.8777 },
      { name: "Delhi", country: "India", lat: 28.6139, lon: 77.2090 },
      { name: "Bangkok", country: "Thailand", lat: 13.7563, lon: 100.5018 },
      { name: "Singapore", country: "Singapore", lat: 1.3521, lon: 103.8198 },
      { name: "Jakarta", country: "Indonesia", lat: -6.2088, lon: 106.8456 },
      { name: "Beijing", country: "China", lat: 39.9042, lon: 116.4074 },
      { name: "Shanghai", country: "China", lat: 31.2304, lon: 121.4737 },
      { name: "Seoul", country: "South Korea", lat: 37.5665, lon: 126.9780 },
      { name: "Tokyo", country: "Japan", lat: 35.6762, lon: 139.6503 },
      { name: "Sydney", country: "Australia", lat: -33.8688, lon: 151.2093 },
      { name: "Melbourne", country: "Australia", lat: -37.8136, lon: 144.9631 },
      { name: "Auckland", country: "New Zealand", lat: -36.8509, lon: 174.7645 },
      { name: "Moscow", country: "Russia", lat: 55.7558, lon: 37.6173 },
      { name: "Kyiv", country: "Ukraine", lat: 50.4501, lon: 30.5234 },
      { name: "New York", country: "USA", lat: 40.7128, lon: -74.0060 },
      { name: "Washington", country: "USA", lat: 38.9072, lon: -77.0369 },
      { name: "Chicago", country: "USA", lat: 41.8781, lon: -87.6298 },
      { name: "Los Angeles", country: "USA", lat: 34.0522, lon: -118.2437 },
      { name: "San Francisco", country: "USA", lat: 37.7749, lon: -122.4194 },
      { name: "Toronto", country: "Canada", lat: 43.6532, lon: -79.3832 },
      { name: "Vancouver", country: "Canada", lat: 49.2827, lon: -123.1207 },
      { name: "Mexico City", country: "Mexico", lat: 19.4326, lon: -99.1332 },
      { name: "Bogota", country: "Colombia", lat: 4.7110, lon: -74.0721 },
      { name: "Lima", country: "Peru", lat: -12.0464, lon: -77.0428 },
      { name: "Santiago", country: "Chile", lat: -33.4489, lon: -70.6693 },
      { name: "Buenos Aires", country: "Argentina", lat: -34.6037, lon: -58.3816 },
      { name: "Sao Paulo", country: "Brazil", lat: -23.5505, lon: -46.6333 },
      { name: "Rio de Janeiro", country: "Brazil", lat: -22.9068, lon: -43.1729 }
    ];

    const COUNTRY_LABELS = [
      { name: "Netherlands", lat: 52.1326, lon: 5.2913 },
      { name: "Belgium", lat: 50.5039, lon: 4.4699 },
      { name: "France", lat: 46.2276, lon: 2.2137 },
      { name: "United Kingdom", lat: 55.3781, lon: -3.4360 },
      { name: "Germany", lat: 51.1657, lon: 10.4515 },
      { name: "Spain", lat: 40.4637, lon: -3.7492 },
      { name: "Italy", lat: 41.8719, lon: 12.5674 },
      { name: "Poland", lat: 51.9194, lon: 19.1451 },
      { name: "Greece", lat: 39.0742, lon: 21.8243 },
      { name: "Turkey", lat: 38.9637, lon: 35.2433 },
      { name: "Egypt", lat: 26.8206, lon: 30.8025 },
      { name: "Nigeria", lat: 9.0820, lon: 8.6753 },
      { name: "Kenya", lat: -0.0236, lon: 37.9062 },
      { name: "South Africa", lat: -30.5595, lon: 22.9375 },
      { name: "UAE", lat: 23.4241, lon: 53.8478 },
      { name: "India", lat: 20.5937, lon: 78.9629 },
      { name: "China", lat: 35.8617, lon: 104.1954 },
      { name: "Japan", lat: 36.2048, lon: 138.2529 },
      { name: "Australia", lat: -25.2744, lon: 133.7751 },
      { name: "New Zealand", lat: -40.9006, lon: 174.8860 },
      { name: "Russia", lat: 61.5240, lon: 105.3188 },
      { name: "Ukraine", lat: 48.3794, lon: 31.1656 },
      { name: "Canada", lat: 56.1304, lon: -106.3468 },
      { name: "USA", lat: 39.8283, lon: -98.5795 },
      { name: "Mexico", lat: 23.6345, lon: -102.5528 },
      { name: "Brazil", lat: -14.2350, lon: -51.9253 },
      { name: "Argentina", lat: -38.4161, lon: -63.6167 },
      { name: "Chile", lat: -35.6751, lon: -71.5430 },
      { name: "Peru", lat: -9.1900, lon: -75.0152 },
      { name: "Colombia", lat: 4.5709, lon: -74.2973 }
    ];

    const IMPORTANT_LOCATIONS = [
      { name: "Statue of Liberty", country: "USA", lat: 40.6892494, lon: -74.0445004, height: 900, heading: 20, pitch: -40 },
      { name: "Times Square", country: "USA", lat: 40.7580, lon: -73.9855, height: 1400, heading: 15, pitch: -45 },
      { name: "Central Park", country: "USA", lat: 40.7829, lon: -73.9654, height: 2200, heading: 0, pitch: -55 },
      { name: "Empire State Building", country: "USA", lat: 40.7484, lon: -73.9857, height: 1200, heading: 25, pitch: -45 },
      { name: "Brooklyn Bridge", country: "USA", lat: 40.7061, lon: -73.9969, height: 1200, heading: 35, pitch: -40 },
      { name: "Golden Gate Bridge", country: "USA", lat: 37.8199, lon: -122.4783, height: 1800, heading: 40, pitch: -45 },
      { name: "Alcatraz Island", country: "USA", lat: 37.8267, lon: -122.4230, height: 1400, heading: 20, pitch: -45 },
      { name: "Space Needle", country: "USA", lat: 47.6205, lon: -122.3493, height: 1100, heading: 25, pitch: -40 },
      { name: "Hollywood Sign", country: "USA", lat: 34.1341, lon: -118.3215, height: 1500, heading: 70, pitch: -35 },
      { name: "Las Vegas Strip", country: "USA", lat: 36.1147, lon: -115.1728, height: 1800, heading: 15, pitch: -50 },
      { name: "Eiffel Tower", country: "France", lat: 48.8584, lon: 2.2945, height: 1100, heading: 35, pitch: -40 },
      { name: "Louvre Museum", country: "France", lat: 48.8606, lon: 2.3376, height: 1300, heading: 20, pitch: -45 },
      { name: "Arc de Triomphe", country: "France", lat: 48.8738, lon: 2.2950, height: 1100, heading: 20, pitch: -40 },
      { name: "Notre-Dame Cathedral", country: "France", lat: 48.8530, lon: 2.3499, height: 1100, heading: 30, pitch: -40 },
      { name: "Mont Saint-Michel", country: "France", lat: 48.6361, lon: -1.5115, height: 1800, heading: 45, pitch: -45 },
      { name: "Big Ben", country: "United Kingdom", lat: 51.5007, lon: -0.1246, height: 1100, heading: 20, pitch: -40 },
      { name: "Tower Bridge", country: "United Kingdom", lat: 51.5055, lon: -0.0754, height: 1200, heading: 35, pitch: -45 },
      { name: "Buckingham Palace", country: "United Kingdom", lat: 51.5014, lon: -0.1419, height: 1300, heading: 15, pitch: -50 },
      { name: "Stonehenge", country: "United Kingdom", lat: 51.1789, lon: -1.8262, height: 1600, heading: 0, pitch: -60 },
      { name: "Edinburgh Castle", country: "United Kingdom", lat: 55.9486, lon: -3.1999, height: 1300, heading: 35, pitch: -45 },
      { name: "Colosseum", country: "Italy", lat: 41.8902, lon: 12.4922, height: 1100, heading: 40, pitch: -40 },
      { name: "Leaning Tower of Pisa", country: "Italy", lat: 43.7229, lon: 10.3966, height: 1000, heading: 25, pitch: -35 },
      { name: "St. Peter's Basilica", country: "Vatican City", lat: 41.9022, lon: 12.4539, height: 1200, heading: 30, pitch: -45 },
      { name: "Trevi Fountain", country: "Italy", lat: 41.9009, lon: 12.4833, height: 900, heading: 20, pitch: -35 },
      { name: "Venice Grand Canal", country: "Italy", lat: 45.4408, lon: 12.3155, height: 1500, heading: 25, pitch: -50 },
      { name: "Sagrada Familia", country: "Spain", lat: 41.4036, lon: 2.1744, height: 1200, heading: 20, pitch: -40 },
      { name: "Park Guell", country: "Spain", lat: 41.4145, lon: 2.1527, height: 1400, heading: 40, pitch: -45 },
      { name: "Plaza Mayor Madrid", country: "Spain", lat: 40.4155, lon: -3.7074, height: 1200, heading: 10, pitch: -50 },
      { name: "Alhambra", country: "Spain", lat: 37.1761, lon: -3.5881, height: 1700, heading: 35, pitch: -45 },
      { name: "Seville Cathedral", country: "Spain", lat: 37.3861, lon: -5.9926, height: 1200, heading: 25, pitch: -40 },
      { name: "Brandenburg Gate", country: "Germany", lat: 52.5163, lon: 13.3777, height: 1100, heading: 25, pitch: -40 },
      { name: "Neuschwanstein Castle", country: "Germany", lat: 47.5576, lon: 10.7498, height: 1800, heading: 40, pitch: -45 },
      { name: "Cologne Cathedral", country: "Germany", lat: 50.9413, lon: 6.9583, height: 1200, heading: 20, pitch: -40 },
      { name: "Berlin Cathedral", country: "Germany", lat: 52.5192, lon: 13.4010, height: 1100, heading: 20, pitch: -40 },
      { name: "Marienplatz Munich", country: "Germany", lat: 48.1374, lon: 11.5755, height: 1200, heading: 20, pitch: -45 },
      { name: "Acropolis of Athens", country: "Greece", lat: 37.9715, lon: 23.7257, height: 1400, heading: 35, pitch: -45 },
      { name: "Santorini Oia", country: "Greece", lat: 36.4618, lon: 25.3753, height: 1500, heading: 60, pitch: -40 },
      { name: "Blue Mosque", country: "Turkey", lat: 41.0054, lon: 28.9768, height: 1200, heading: 20, pitch: -40 },
      { name: "Hagia Sophia", country: "Turkey", lat: 41.0086, lon: 28.9802, height: 1200, heading: 25, pitch: -40 },
      { name: "Burj Khalifa", country: "UAE", lat: 25.1972, lon: 55.2744, height: 1800, heading: 35, pitch: -45 },
      { name: "Pyramids of Giza", country: "Egypt", lat: 29.9792, lon: 31.1342, height: 1900, heading: 40, pitch: -45 },
      { name: "Petra Treasury", country: "Jordan", lat: 30.3285, lon: 35.4444, height: 1500, heading: 20, pitch: -35 },
      { name: "Taj Mahal", country: "India", lat: 27.1751, lon: 78.0421, height: 1300, heading: 25, pitch: -40 },
      { name: "Gateway of India", country: "India", lat: 18.9220, lon: 72.8347, height: 1200, heading: 30, pitch: -40 },
      { name: "Marina Bay Sands", country: "Singapore", lat: 1.2834, lon: 103.8607, height: 1600, heading: 35, pitch: -45 },
      { name: "Tokyo Tower", country: "Japan", lat: 35.6586, lon: 139.7454, height: 1400, heading: 20, pitch: -45 },
      { name: "Shibuya Crossing", country: "Japan", lat: 35.6595, lon: 139.7005, height: 1300, heading: 15, pitch: -45 },
      { name: "Mount Fuji", country: "Japan", lat: 35.3606, lon: 138.7274, height: 4500, heading: 35, pitch: -35 },
      { name: "Forbidden City", country: "China", lat: 39.9163, lon: 116.3972, height: 1800, heading: 0, pitch: -60 },
      { name: "Sydney Opera House", country: "Australia", lat: -33.8568, lon: 151.2153, height: 1400, heading: 30, pitch: -40 },
      { name: "Christ the Redeemer", country: "Brazil", lat: -22.9519, lon: -43.2105, height: 1700, heading: 35, pitch: -40 },
      { name: "Machu Picchu", country: "Peru", lat: -13.1631, lon: -72.5450, height: 2500, heading: 40, pitch: -45 },
      { name: "Chichen Itza", country: "Mexico", lat: 20.6843, lon: -88.5678, height: 1600, heading: 30, pitch: -40 },
      { name: "CN Tower", country: "Canada", lat: 43.6426, lon: -79.3871, height: 1300, heading: 20, pitch: -45 },
      { name: "Niagara Falls", country: "Canada/USA", lat: 43.0799, lon: -79.0747, height: 2200, heading: 35, pitch: -45 }
    ];

    const FEED_STATE = Array.from({ length: MAX_FEEDS }, (_, i) => ({
      id: i + 1,
      viewer: null,
      tileset: null,
      isInitializing: false,
      isInitialized: false,
      cityLabelEntity: null,
      countryLabelEntity: null,
      worldCityEntities: [],
      worldCountryEntities: [],
      currentLocation: IMPORTANT_LOCATIONS[i % IMPORTANT_LOCATIONS.length],
      searchSeq: 0,
      dropdownItems: [],
      dropdownIndex: -1,
      popoutWindow: null
    }));

    function normalizeText(s) {
      return String(s || "").toLowerCase().trim();
    }

    function escapeHtml(s) {
      return String(s || "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
    }

    function isCartesianInCanvas(viewer, CesiumLib, cartesian) {
      if (!viewer || !cartesian) return false;

      const scene = viewer.scene;
      const camera = viewer.camera;
      const ellipsoid = scene.globe && scene.globe.ellipsoid
        ? scene.globe.ellipsoid
        : CesiumLib.Ellipsoid.WGS84;

      const toPoint = CesiumLib.Cartesian3.subtract(
        cartesian,
        camera.positionWC,
        new CesiumLib.Cartesian3()
      );
      const normalized = CesiumLib.Cartesian3.normalize(toPoint, new CesiumLib.Cartesian3());
      const dot = CesiumLib.Cartesian3.dot(camera.directionWC, normalized);
      if (!(dot > 0.0)) return false;

      const occluder = new CesiumLib.EllipsoidalOccluder(ellipsoid, camera.positionWC);
      if (!occluder.isPointVisible(cartesian)) return false;

      const win = CesiumLib.SceneTransforms.wgs84ToWindowCoordinates(scene, cartesian);
      if (!win) return false;
      if (!Number.isFinite(win.x) || !Number.isFinite(win.y)) return false;

      const w = scene.canvas.clientWidth;
      const h = scene.canvas.clientHeight;
      return win.x >= 0 && win.x <= w && win.y >= 0 && win.y <= h;
    }

    function updateEntitiesVisibilityForViewer(viewer, CesiumLib, countryEntities, cityEntities, selectedCityEntity, selectedCountryEntity) {
      if (!viewer) return;

      const h = viewer.camera.positionCartographic
        ? viewer.camera.positionCartographic.height
        : Number.POSITIVE_INFINITY;

      const showCountriesByZoom = h <= COUNTRY_SHOW_HEIGHT;
      const showCitiesByZoom = h <= CITY_SHOW_HEIGHT;
      const showSelectedByZoom = h <= SELECTED_SHOW_HEIGHT;
      const now = CesiumLib.JulianDate.now();

      for (const entity of countryEntities) {
        const pos = entity.position && entity.position.getValue ? entity.position.getValue(now) : null;
        entity.show = showCountriesByZoom && isCartesianInCanvas(viewer, CesiumLib, pos);
      }

      for (const entity of cityEntities) {
        const pos = entity.position && entity.position.getValue ? entity.position.getValue(now) : null;
        entity.show = showCitiesByZoom && isCartesianInCanvas(viewer, CesiumLib, pos);
      }

      if (selectedCityEntity) {
        const pos = selectedCityEntity.position && selectedCityEntity.position.getValue ? selectedCityEntity.position.getValue(now) : null;
        selectedCityEntity.show = showSelectedByZoom && isCartesianInCanvas(viewer, CesiumLib, pos);
      }

      if (selectedCountryEntity) {
        const pos = selectedCountryEntity.position && selectedCountryEntity.position.getValue ? selectedCountryEntity.position.getValue(now) : null;
        selectedCountryEntity.show = showSelectedByZoom && isCartesianInCanvas(viewer, CesiumLib, pos);
      }
    }

    async function sendAction(action, payload) {
      const res = await fetch("/api/action", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ action, payload })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error((data && data.error) ? data.error : ("HTTP " + res.status));
      return data;
    }

    async function loadJsonFeed(n) {
      const panel = document.querySelector('.json-feed-card[data-feed="' + n + '"]');
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

    function wireJsonFeedButtons() {
      document.querySelectorAll(".json-feed-card").forEach(panel => {
        const n = Number(panel.getAttribute("data-feed"));
        const btn = panel.querySelector(".add-feed");
        if (btn) btn.addEventListener("click", () => loadJsonFeed(n));
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
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") submit();
      });
    }

    function scoreLocationMatch(location, query) {
      const q = normalizeText(query);
      if (!q) return 1;

      const name = normalizeText(location.name);
      const country = normalizeText(location.country);
      const combined = name + " " + country;

      if (name === q) return 1000;
      if (combined === q) return 950;
      if (name.startsWith(q)) return 800;
      if (combined.startsWith(q)) return 700;
      if (name.includes(q)) return 600;
      if (country.startsWith(q)) return 500;
      if (country.includes(q)) return 400;

      const parts = q.split(/\\s+/).filter(Boolean);
      let score = 0;
      for (const part of parts) {
        if (name.includes(part)) score += 120;
        if (country.includes(part)) score += 80;
      }
      return score;
    }

    function getCuratedMatches(query) {
      return IMPORTANT_LOCATIONS
        .map(loc => ({ ...loc, _score: scoreLocationMatch(loc, query), sourceType: "curated" }))
        .filter(loc => loc._score > 0)
        .sort((a, b) => b._score - a._score || a.name.localeCompare(b.name));
    }

    function bestAddressName(address, fallbackName) {
      if (!address) return fallbackName || "Unknown location";
      return (
        address.city ||
        address.town ||
        address.village ||
        address.hamlet ||
        address.municipality ||
        address.county ||
        address.state_district ||
        address.state ||
        address.region ||
        fallbackName ||
        "Unknown location"
      );
    }

    function simplifyDisplayName(displayName) {
      return String(displayName || "")
        .split(",")
        .slice(0, 3)
        .join(", ")
        .trim();
    }

    async function geocodeWorldwide(query) {
      const q = String(query || "").trim();
      if (!q) return [];

      const url = "https://nominatim.openstreetmap.org/search?" + new URLSearchParams({
        q,
        format: "jsonv2",
        addressdetails: "1",
        limit: "8"
      }).toString();

      const res = await fetch(url, {
        headers: { "Accept": "application/json" }
      });

      if (!res.ok) {
        throw new Error("Geocoder HTTP " + res.status);
      }

      const data = await res.json();
      if (!Array.isArray(data)) return [];

      return data.map((item) => {
        const address = item.address || {};
        const cityName = bestAddressName(address, item.name || item.display_name);
        const countryName = address.country || "";
        return {
          sourceType: "geocoder",
          name: cityName,
          country: countryName,
          subtitle: simplifyDisplayName(item.display_name),
          lat: Number(item.lat),
          lon: Number(item.lon),
          height: 2200,
          heading: 20,
          pitch: -45,
          raw: item
        };
      });
    }

    function dedupeLocations(items) {
      const out = [];
      const seen = new Set();

      for (const item of items) {
        const key = [
          normalizeText(item.name),
          normalizeText(item.country),
          Number(item.lat).toFixed(5),
          Number(item.lon).toFixed(5)
        ].join("|");

        if (!seen.has(key)) {
          seen.add(key);
          out.push(item);
        }
      }
      return out;
    }

    async function buildSearchResults(query) {
      const q = String(query || "").trim();
      const curated = getCuratedMatches(q);

      if (!q) {
        return {
          dropdown: IMPORTANT_LOCATIONS.slice(0, 8),
          grid: IMPORTANT_LOCATIONS.slice(0, 50)
        };
      }

      try {
        const geocoded = await geocodeWorldwide(q);
        const combined = dedupeLocations([...geocoded, ...curated]);
        return {
          dropdown: combined.slice(0, 8),
          grid: combined.slice(0, 20)
        };
      } catch (err) {
        console.error("Search suggestion error:", err);
        return {
          dropdown: curated.slice(0, 8),
          grid: curated.slice(0, 20)
        };
      }
    }

    function getFeedState(feedId) {
      return FEED_STATE[feedId - 1];
    }

    function getFeedRoot(feedId) {
      return document.querySelector('.feed-card[data-feed="' + feedId + '"]');
    }

    function getFeedInput(feedId) {
      return document.getElementById("feed-search-input-" + feedId);
    }

    function getFeedDropdown(feedId) {
      return document.getElementById("autocomplete-list-" + feedId);
    }

    function getFeedGrid(feedId) {
      return document.getElementById("location-list-" + feedId);
    }

    function getFeedLabel(feedId) {
      return document.getElementById("viewer-label-" + feedId);
    }

    function getFeedContainer(feedId) {
      return document.getElementById("viewer-container-" + feedId);
    }

    function hideDropdown(feedId) {
      const state = getFeedState(feedId);
      const listEl = getFeedDropdown(feedId);
      if (!listEl) return;
      listEl.classList.remove("open");
      listEl.innerHTML = "";
      state.dropdownItems = [];
      state.dropdownIndex = -1;
    }

    function renderDropdown(feedId, items) {
      const state = getFeedState(feedId);
      const listEl = getFeedDropdown(feedId);
      if (!listEl) return;

      listEl.innerHTML = "";
      state.dropdownItems = items.slice(0, 8);
      state.dropdownIndex = state.dropdownItems.length ? 0 : -1;

      if (!state.dropdownItems.length) {
        hideDropdown(feedId);
        return;
      }

      state.dropdownItems.forEach((loc, idx) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "autocomplete-item" + (idx === state.dropdownIndex ? " active" : "");

        const meta = loc.subtitle ? loc.subtitle : (loc.country || "Unknown region");

        btn.innerHTML = `
          <span class="name">${escapeHtml(loc.name)}</span>
          <span class="meta">${escapeHtml(meta)}</span>
        `;

        btn.addEventListener("mousedown", (e) => {
          e.preventDefault();
          selectSuggestion(feedId, idx);
        });

        listEl.appendChild(btn);
      });

      listEl.classList.add("open");
    }

    function refreshDropdownActiveState(feedId) {
      const listEl = getFeedDropdown(feedId);
      const state = getFeedState(feedId);
      if (!listEl) return;

      [...listEl.querySelectorAll(".autocomplete-item")].forEach((el, idx) => {
        el.classList.toggle("active", idx === state.dropdownIndex);
      });
    }

    function renderLocationGrid(feedId, items) {
      const listEl = getFeedGrid(feedId);
      if (!listEl) return;

      listEl.innerHTML = "";

      if (!items.length) {
        const empty = document.createElement("div");
        empty.className = "location-empty";
        empty.textContent = "No matching locations.";
        listEl.appendChild(empty);
        return;
      }

      for (const loc of items) {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "location-item";

        const meta = loc.subtitle ? loc.subtitle : (loc.country || "Unknown region");

        btn.innerHTML = `
          <span class="loc-name">${escapeHtml(loc.name)}</span>
          <span class="loc-meta">${escapeHtml(meta)}</span>
        `;

        btn.addEventListener("click", () => {
          hideDropdown(feedId);
          flyToLocation(feedId, loc);
        });

        listEl.appendChild(btn);
      }
    }

    function clearActiveLocationLabels(feedId) {
      const state = getFeedState(feedId);
      const viewer = state.viewer;
      if (!viewer) return;

      if (state.cityLabelEntity) {
        viewer.entities.remove(state.cityLabelEntity);
        state.cityLabelEntity = null;
      }
      if (state.countryLabelEntity) {
        viewer.entities.remove(state.countryLabelEntity);
        state.countryLabelEntity = null;
      }
    }

    function updateWorldReferenceLabelVisibility(feedId) {
      const state = getFeedState(feedId);
      updateEntitiesVisibilityForViewer(
        state.viewer,
        Cesium,
        state.worldCountryEntities,
        state.worldCityEntities,
        state.cityLabelEntity,
        state.countryLabelEntity
      );
    }

    function addLocationLabels(feedId, location) {
      const state = getFeedState(feedId);
      const viewer = state.viewer;
      if (!viewer || !location) return;

      clearActiveLocationLabels(feedId);

      const position = Cesium.Cartesian3.fromDegrees(location.lon, location.lat, 0);

      state.cityLabelEntity = viewer.entities.add({
        position,
        label: {
          text: String(location.name || "Unknown place"),
          font: "bold 24px sans-serif",
          fillColor: Cesium.Color.WHITE,
          outlineColor: Cesium.Color.BLACK,
          outlineWidth: 3,
          style: Cesium.LabelStyle.FILL,
          pixelOffset: new Cesium.Cartesian2(0, -26),
          verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
          horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
          disableDepthTestDistance: Number.POSITIVE_INFINITY,
          showBackground: false
        }
      });

      state.countryLabelEntity = viewer.entities.add({
        position,
        label: {
          text: String(location.country || ""),
          font: "bold 18px sans-serif",
          fillColor: Cesium.Color.fromCssColorString("#f59e0b"),
          outlineColor: Cesium.Color.BLACK,
          outlineWidth: 3,
          style: Cesium.LabelStyle.FILL,
          pixelOffset: new Cesium.Cartesian2(0, -4),
          verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
          horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
          disableDepthTestDistance: Number.POSITIVE_INFINITY,
          showBackground: false
        }
      });

      updateWorldReferenceLabelVisibility(feedId);
    }

    function addWorldReferenceLabels(feedId) {
      const state = getFeedState(feedId);
      const viewer = state.viewer;
      if (!viewer) return;

      state.worldCountryEntities = COUNTRY_LABELS.map((country) => {
        return viewer.entities.add({
          position: Cesium.Cartesian3.fromDegrees(country.lon, country.lat, 0),
          label: {
            text: country.name,
            font: "bold 18px sans-serif",
            fillColor: Cesium.Color.fromCssColorString("#f59e0b"),
            outlineColor: Cesium.Color.BLACK,
            outlineWidth: 3,
            style: Cesium.LabelStyle.FILL,
            horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
            verticalOrigin: Cesium.VerticalOrigin.CENTER,
            disableDepthTestDistance: Number.POSITIVE_INFINITY,
            showBackground: false
          }
        });
      });

      state.worldCityEntities = WORLD_CITIES.map((city) => {
        return viewer.entities.add({
          position: Cesium.Cartesian3.fromDegrees(city.lon, city.lat, 0),
          label: {
            text: city.name,
            font: "bold 14px sans-serif",
            fillColor: Cesium.Color.WHITE,
            outlineColor: Cesium.Color.BLACK,
            outlineWidth: 3,
            style: Cesium.LabelStyle.FILL,
            pixelOffset: new Cesium.Cartesian2(0, -6),
            horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
            verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
            disableDepthTestDistance: Number.POSITIVE_INFINITY,
            showBackground: false
          }
        });
      });

      updateWorldReferenceLabelVisibility(feedId);
    }

    function lockCameraToLocation(feedId) {
    const state = getFeedState(feedId);
    const viewer = state.viewer;
    const loc = state.currentLocation;

    if (!viewer || !loc) return;

    const target = Cesium.Cartesian3.fromDegrees(loc.lon, loc.lat, 0);

    viewer.scene.postRender.addEventListener(() => {
      const camera = viewer.camera;

      const range = camera.positionCartographic.height;

      camera.lookAt(
        target,
        new Cesium.HeadingPitchRange(
          camera.heading,
          camera.pitch,
          range
        )
      );
    });
  }

    function wireViewerLabelVisibility(feedId) {
      const state = getFeedState(feedId);
      const viewer = state.viewer;
      if (!viewer) return;

      viewer.camera.percentageChanged = 0.01;
      viewer.camera.changed.addEventListener(() => {
        updateWorldReferenceLabelVisibility(feedId);
      });

      viewer.scene.postRender.addEventListener(() => {
        updateWorldReferenceLabelVisibility(feedId);
      });
    }

    function flyToLocation(feedId, location) {
      const state = getFeedState(feedId);
      const viewer = state.viewer;
      const label = getFeedLabel(feedId);

      if (!viewer || !location) return;

      state.currentLocation = location;

      const city = String(location.name || "Unknown place");
      const country = String(location.country || "");

      if (label) {
        label.textContent = country ? `FEED ${feedId} (${city}, ${country})` : `FEED ${feedId} (${city})`;
      }

      addLocationLabels(feedId, location);

      viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(
          Number(location.lon),
          Number(location.lat),
          Number(location.height || 2200)
        ),
        orientation: {
          heading: Cesium.Math.toRadians(Number(location.heading || 20)),
          pitch: Cesium.Math.toRadians(Number(location.pitch || -45)),
          roll: 0.0
        },
        duration: 2.0,
        complete: () => updateWorldReferenceLabelVisibility(feedId)
      });
    }

    async function updateSearchUI(feedId, query) {
      const state = getFeedState(feedId);
      const mySeq = ++state.searchSeq;
      const results = await buildSearchResults(query);
      if (mySeq !== state.searchSeq) return;

      renderDropdown(feedId, results.dropdown);
      renderLocationGrid(feedId, results.grid);
    }

    async function searchAndFlyToBestMatch(feedId) {
      const input = getFeedInput(feedId);
      if (!input) return;

      const q = String(input.value || "").trim();
      if (!q) return;

      const results = await buildSearchResults(q);
      renderDropdown(feedId, results.dropdown);
      renderLocationGrid(feedId, results.grid);

      const best = results.dropdown[0] || results.grid[0];
      if (best) {
        hideDropdown(feedId);
        ensureFeedViewer(feedId).then(() => flyToLocation(feedId, best)).catch(console.error);
      }
    }

    function selectSuggestion(feedId, idx) {
      const state = getFeedState(feedId);
      if (idx < 0 || idx >= state.dropdownItems.length) return;

      const selected = state.dropdownItems[idx];
      const input = getFeedInput(feedId);
      if (input) {
        input.value = selected.country ? `${selected.name}, ${selected.country}` : selected.name;
      }

      hideDropdown(feedId);
      ensureFeedViewer(feedId).then(() => flyToLocation(feedId, selected)).catch(console.error);
    }

    function destroyFeedViewer(feedId) {
      const state = getFeedState(feedId);
      if (!state.viewer) {
        state.isInitialized = false;
        state.isInitializing = false;
        return;
      }

      try {
        state.viewer.destroy();
      } catch (e) {
        console.error("Destroy feed viewer error:", feedId, e);
      }

      state.viewer = null;
      state.tileset = null;
      state.isInitialized = false;
      state.isInitializing = false;
      state.cityLabelEntity = null;
      state.countryLabelEntity = null;
      state.worldCityEntities = [];
      state.worldCountryEntities = [];

      const label = getFeedLabel(feedId);
      if (label) {
        label.textContent = `FEED ${feedId}`;
      }

      const container = getFeedContainer(feedId);
      if (container) {
        container.innerHTML = "";
      }
    }

    async function initFeedViewer(feedId) {
      const state = getFeedState(feedId);
      const container = getFeedContainer(feedId);
      const label = getFeedLabel(feedId);
      const defaultLocation = state.currentLocation;

      if (!container || !label) return;
      if (state.isInitializing || state.isInitialized) return;

      state.isInitializing = true;

      const setStatus = (s) => { label.textContent = s; };

      try {
        if (!GMP_MAP_TILES_API_KEY || GMP_MAP_TILES_API_KEY.includes("REPLACE_ME")) {
          setStatus(`FEED ${feedId} (missing API key)`);
          state.isInitializing = false;
          return;
        }

        Cesium.Ion.defaultAccessToken = undefined;

        const rootUrl = "https://tile.googleapis.com/v1/3dtiles/root.json?key=" +
          encodeURIComponent(GMP_MAP_TILES_API_KEY);

        const probeRes = await fetch(rootUrl, { cache: "no-store" });
        if (!probeRes.ok) {
          const txt = await probeRes.text().catch(() => "");
          setStatus(`FEED ${feedId} (root.json HTTP ${probeRes.status})`);
          console.error("root.json error:", probeRes.status, txt);
          state.isInitializing = false;
          return;
        }

        setStatus(`FEED ${feedId} (initializing…)`);

        const viewer = new Cesium.Viewer(container, {
          baseLayer: false,
          baseLayerPicker: false,
          terrain: new Cesium.EllipsoidTerrainProvider(),
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

        viewer.scene.globe.show = false;
        viewer.scene.skyBox.show = false;
        viewer.scene.sun.show = false;
        viewer.scene.moon.show = false;
        viewer.scene.backgroundColor = Cesium.Color.fromCssColorString("#0b0d12");

        viewer.camera.setView({
          destination: Cesium.Cartesian3.fromDegrees(defaultLocation.lon, defaultLocation.lat, 2500.0),
          orientation: {
            heading: Cesium.Math.toRadians(defaultLocation.heading || 20.0),
            pitch: Cesium.Math.toRadians(-35.0),
            roll: 0.0
          }
        });

        setStatus(`FEED ${feedId} (loading tiles…)`);

        const tileset = await Cesium.Cesium3DTileset.fromUrl(rootUrl, {
          showCreditsOnScreen: true
        });

        viewer.scene.primitives.add(tileset);

        state.viewer = viewer;
        state.tileset = tileset;
        state.isInitialized = true;
        state.isInitializing = false;

        addWorldReferenceLabels(feedId);
        wireViewerLabelVisibility(feedId);
        addLocationLabels(feedId, defaultLocation);

        setStatus(`FEED ${feedId} (${defaultLocation.name}, ${defaultLocation.country})`);

        viewer.camera.flyTo({
          destination: Cesium.Cartesian3.fromDegrees(defaultLocation.lon, defaultLocation.lat, defaultLocation.height || 900.0),
          orientation: {
            heading: Cesium.Math.toRadians(defaultLocation.heading || 20.0),
            pitch: Cesium.Math.toRadians(defaultLocation.pitch || -40.0),
            roll: 0.0
          },
          duration: 1.2,
          complete: () => updateWorldReferenceLabelVisibility(feedId)
        });
      } catch (e) {
        state.isInitializing = false;
        state.isInitialized = false;
        setStatus(`FEED ${feedId} (init error)`);
        console.error("FEED init error:", feedId, e);
      }
    }

    async function ensureFeedViewer(feedId) {
      const state = getFeedState(feedId);
      if (state.isInitialized && state.viewer) return;
      if (state.isInitializing) {
        let tries = 0;
        while (state.isInitializing && tries < 200) {
          await new Promise(r => setTimeout(r, 50));
          tries += 1;
        }
        return;
      }
      await initFeedViewer(feedId);
    }

    function syncVisibleFeedViewers(activeCount) {
      for (let i = 1; i <= MAX_FEEDS; i++) {
        if (i <= activeCount) {
          ensureFeedViewer(i).catch(err => console.error("ensureFeedViewer error:", i, err));
        } else {
          destroyFeedViewer(i);
        }
      }
    }

    function setGridColumns(activeCount) {
      const grid = document.getElementById("feeds-grid");
      if (!grid) return;

      grid.classList.remove("cols-1", "cols-2", "cols-3");

      if (activeCount <= 1) grid.classList.add("cols-1");
      else if (activeCount <= 4) grid.classList.add("cols-2");
      else grid.classList.add("cols-3");
    }

    function setActiveFeedCount(count) {
      const n = Math.max(1, Math.min(MAX_FEEDS, Number(count) || 1));
      const input = document.getElementById("feed-count-input");
      if (input) input.value = String(n);

      document.querySelectorAll(".feed-card").forEach(card => {
        const feedId = Number(card.getAttribute("data-feed"));
        card.classList.toggle("hidden", feedId > n);
      });

      setGridColumns(n);
      syncVisibleFeedViewers(n);
    }

    function wireFeedCountControls() {
      const input = document.getElementById("feed-count-input");
      const plus = document.getElementById("feed-count-plus");
      const minus = document.getElementById("feed-count-minus");
      const tilesBtn = document.getElementById("view-mode-tiles");
      const popBtn = document.getElementById("view-mode-popouts");

      function applyInput() {
        setActiveFeedCount(input.value);
      }

      input.addEventListener("change", applyInput);
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") applyInput();
      });

      plus.addEventListener("click", () => {
        setActiveFeedCount((Number(input.value) || 1) + 1);
      });

      minus.addEventListener("click", () => {
        setActiveFeedCount((Number(input.value) || 1) - 1);
      });

      tilesBtn.addEventListener("click", () => {
        tilesBtn.classList.add("active");
        popBtn.classList.remove("active");
      });

      popBtn.addEventListener("click", () => {
        popBtn.classList.add("active");
        tilesBtn.classList.remove("active");
        openActiveFeedsAsPopouts();
      });

      setActiveFeedCount(1);
    }

    function buildPopoutHtml(feedId) {
      return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>UROPS PANOPT | FEED ${feedId}</title>
  <script src="https://ajax.googleapis.com/ajax/libs/cesiumjs/1.105/Build/Cesium/Cesium.js"><\\/script>
  <link href="https://ajax.googleapis.com/ajax/libs/cesiumjs/1.105/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
  <style>
    html, body { margin: 0; width: 100%; height: 100%; background: #0b0d12; color: #e8ecf5; font-family: Arial, sans-serif; }
    #app { width: 100%; height: 100%; position: relative; }
    #viewer { width: 100%; height: 100%; }
    .label {
      position: absolute;
      top: 12px;
      left: 12px;
      z-index: 10;
      padding: 6px 10px;
      border: 1px solid #2a3142;
      border-radius: 8px;
      background: rgba(21,25,36,0.72);
      color: #aeb6c7;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <div id="app">
    <div id="label" class="label">FEED ${feedId}</div>
    <div id="viewer"></div>
  </div>
</body>
</html>`;
    }

    function addWorldReferenceLabelsToViewer(viewer, CesiumLib) {
      const cityEntities = WORLD_CITIES.map((city) => {
        return viewer.entities.add({
          position: CesiumLib.Cartesian3.fromDegrees(city.lon, city.lat, 0),
          label: {
            text: city.name,
            font: "bold 14px sans-serif",
            fillColor: CesiumLib.Color.WHITE,
            outlineColor: CesiumLib.Color.BLACK,
            outlineWidth: 3,
            style: Cesium.LabelStyle.FILL,
            pixelOffset: new CesiumLib.Cartesian2(0, -6),
            horizontalOrigin: CesiumLib.HorizontalOrigin.CENTER,
            verticalOrigin: CesiumLib.VerticalOrigin.BOTTOM,
            disableDepthTestDistance: Number.POSITIVE_INFINITY,
            showBackground: false
          }
        });
      });

      const countryEntities = COUNTRY_LABELS.map((country) => {
        return viewer.entities.add({
          position: CesiumLib.Cartesian3.fromDegrees(country.lon, country.lat, 0),
          label: {
            text: country.name,
            font: "bold 18px sans-serif",
            fillColor: CesiumLib.Color.fromCssColorString("#f59e0b"),
            outlineColor: CesiumLib.Color.BLACK,
            outlineWidth: 3,
            style: Cesium.LabelStyle.FILL,
            horizontalOrigin: CesiumLib.HorizontalOrigin.CENTER,
            verticalOrigin: CesiumLib.VerticalOrigin.CENTER,
            disableDepthTestDistance: Number.POSITIVE_INFINITY,
            showBackground: false
          }
        });
      });

      viewer.camera.percentageChanged = 0.01;

      const update = () => {
        updateEntitiesVisibilityForViewer(viewer, CesiumLib, countryEntities, cityEntities, null, null);
      };

      viewer.camera.changed.addEventListener(update);
      viewer.scene.postRender.addEventListener(update);
      update();

      return { cityEntities, countryEntities, update };
    }

    async function openFeedInPopout(feedId) {
      const state = getFeedState(feedId);
      const location = state.currentLocation || IMPORTANT_LOCATIONS[feedId - 1] || IMPORTANT_LOCATIONS[0];
      const w = window.open("", "panopt-feed-" + feedId, "width=1200,height=800");
      if (!w) return;

      state.popoutWindow = w;
      w.document.open();
      w.document.write(buildPopoutHtml(feedId));
      w.document.close();

      const init = () => {
        const cw = w.Cesium;
        if (!cw || !w.document.getElementById("viewer")) {
          setTimeout(init, 100);
          return;
        }

        const labelEl = w.document.getElementById("label");
        if (labelEl) {
          labelEl.textContent = location.country
            ? `FEED ${feedId} (${location.name}, ${location.country})`
            : `FEED ${feedId} (${location.name})`;
        }

        cw.Ion.defaultAccessToken = undefined;

        const rootUrl = "https://tile.googleapis.com/v1/3dtiles/root.json?key=" +
          encodeURIComponent(GMP_MAP_TILES_API_KEY);

        const viewer = new cw.Viewer(w.document.getElementById("viewer"), {
          baseLayer: false,
          baseLayerPicker: false,
          terrain: new cw.EllipsoidTerrainProvider(),
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

        viewer.scene.globe.show = false;
        viewer.scene.skyBox.show = false;
        viewer.scene.sun.show = false;
        viewer.scene.moon.show = false;
        viewer.scene.backgroundColor = cw.Color.fromCssColorString("#0b0d12");

        cw.Cesium3DTileset.fromUrl(rootUrl, { showCreditsOnScreen: true })
          .then((tileset) => {
            viewer.scene.primitives.add(tileset);

            const refs = addWorldReferenceLabelsToViewer(viewer, cw);
            const position = cw.Cartesian3.fromDegrees(location.lon, location.lat, 0);

            const cityLabel = viewer.entities.add({
              position,
              label: {
                text: String(location.name || "Unknown place"),
                font: "bold 24px sans-serif",
                fillColor: cw.Color.WHITE,
                outlineColor: cw.Color.BLACK,
                outlineWidth: 3,
                style: Cesium.LabelStyle.FILL,
                pixelOffset: new cw.Cartesian2(0, -26),
                verticalOrigin: cw.VerticalOrigin.BOTTOM,
                horizontalOrigin: cw.HorizontalOrigin.CENTER,
                disableDepthTestDistance: Number.POSITIVE_INFINITY,
                showBackground: false
              }
            });

            const countryLabel = viewer.entities.add({
              position,
              label: {
                text: String(location.country || ""),
                font: "bold 18px sans-serif",
                fillColor: cw.Color.fromCssColorString("#f59e0b"),
                outlineColor: cw.Color.BLACK,
                outlineWidth: 3,
                style: Cesium.LabelStyle.FILL,
                pixelOffset: new cw.Cartesian2(0, -4),
                verticalOrigin: cw.VerticalOrigin.BOTTOM,
                horizontalOrigin: cw.HorizontalOrigin.CENTER,
                disableDepthTestDistance: Number.POSITIVE_INFINITY,
                showBackground: false
              }
            });

            const updateSelected = () => {
              updateEntitiesVisibilityForViewer(viewer, cw, refs.countryEntities, refs.cityEntities, cityLabel, countryLabel);
            };

            viewer.camera.changed.addEventListener(updateSelected);
            viewer.scene.postRender.addEventListener(updateSelected);

            viewer.camera.flyTo({
              destination: cw.Cartesian3.fromDegrees(location.lon, location.lat, location.height || 2200),
              orientation: {
                heading: cw.Math.toRadians(location.heading || 20),
                pitch: cw.Math.toRadians(location.pitch || -45),
                roll: 0.0
              },
              duration: 1.2,
              complete: updateSelected
            });
          })
          .catch((err) => {
            console.error("Popout feed init error:", err);
            if (labelEl) labelEl.textContent = `FEED ${feedId} (init error)`;
          });
      };

      init();
    }

    function openActiveFeedsAsPopouts() {
      document.querySelectorAll(".feed-card:not(.hidden)").forEach(card => {
        const feedId = Number(card.getAttribute("data-feed"));
        openFeedInPopout(feedId);
      });
    }

    function wireFeedSearch(feedId) {
      const state = getFeedState(feedId);
      const root = getFeedRoot(feedId);
      const input = getFeedInput(feedId);
      const btn = document.getElementById("feed-search-btn-" + feedId);
      const popBtn = document.getElementById("feed-popout-btn-" + feedId);
      const resetBtn = document.getElementById("feed-reset-btn-" + feedId);

      if (!root || !input || !btn || !popBtn || !resetBtn) return;

      input.addEventListener("input", () => {
        updateSearchUI(feedId, input.value);
      });

      input.addEventListener("focus", () => {
        updateSearchUI(feedId, input.value);
      });

      input.addEventListener("keydown", async (e) => {
        if (e.key === "ArrowDown") {
          if (!state.dropdownItems.length) return;
          e.preventDefault();
          state.dropdownIndex = Math.min(state.dropdownIndex + 1, state.dropdownItems.length - 1);
          refreshDropdownActiveState(feedId);
          return;
        }

        if (e.key === "ArrowUp") {
          if (!state.dropdownItems.length) return;
          e.preventDefault();
          state.dropdownIndex = Math.max(state.dropdownIndex - 1, 0);
          refreshDropdownActiveState(feedId);
          return;
        }

        if (e.key === "Escape") {
          hideDropdown(feedId);
          return;
        }

        if (e.key === "Enter") {
          e.preventDefault();
          if (state.dropdownItems.length && state.dropdownIndex >= 0) {
            selectSuggestion(feedId, state.dropdownIndex);
          } else {
            await searchAndFlyToBestMatch(feedId);
          }
        }
      });

      btn.addEventListener("click", () => {
        searchAndFlyToBestMatch(feedId);
      });

      popBtn.addEventListener("click", () => {
        openFeedInPopout(feedId);
      });

      resetBtn.addEventListener("click", () => {
        input.value = "";
        hideDropdown(feedId);
        renderLocationGrid(feedId, IMPORTANT_LOCATIONS);
        ensureFeedViewer(feedId).then(() => {
          flyToLocation(feedId, IMPORTANT_LOCATIONS[(feedId - 1) % IMPORTANT_LOCATIONS.length]);
        }).catch(console.error);
      });

      document.addEventListener("click", (e) => {
        if (!root.contains(e.target)) {
          hideDropdown(feedId);
        }
      });

      renderLocationGrid(feedId, IMPORTANT_LOCATIONS);
    }

    function buildFeedCards() {
      const grid = document.getElementById("feeds-grid");
      if (!grid) return;

      grid.innerHTML = "";

      for (let i = 1; i <= MAX_FEEDS; i++) {
        const card = document.createElement("section");
        card.className = "feed-card";
        card.setAttribute("data-feed", String(i));

        card.innerHTML = `
          <div class="feed-top">
            <div class="feed-title">FEED ${i}</div>
            <div class="feed-actions">
              <button id="feed-reset-btn-${i}" class="small-btn" type="button">Reset</button>
              <button id="feed-popout-btn-${i}" class="small-btn" type="button">Pop out</button>
            </div>
          </div>

          <div class="viewer-frame">
            <div id="viewer-label-${i}" class="viewer-label">FEED ${i}</div>
            <div id="viewer-container-${i}" class="viewer-container"></div>
          </div>

          <div class="feed-search-wrap">
            <div class="feed-search-row">
              <input id="feed-search-input-${i}" class="feed-search-input" type="text" placeholder="Search any location for FEED ${i}..." autocomplete="off" />
              <button id="feed-search-btn-${i}" class="search-btn" type="button">Search</button>
            </div>
            <div id="autocomplete-list-${i}" class="autocomplete-list"></div>
          </div>

          <div class="feed-help">
            Only visible feeds are initialized. This avoids GPU/WebGL crashes at high feed counts.
          </div>

          <div id="location-list-${i}" class="location-list"></div>
        `;

        grid.appendChild(card);
      }
    }

    function setGridColumns(activeCount) {
      const grid = document.getElementById("feeds-grid");
      if (!grid) return;

      grid.classList.remove("cols-1", "cols-2", "cols-3");

      if (activeCount <= 1) grid.classList.add("cols-1");
      else if (activeCount <= 4) grid.classList.add("cols-2");
      else grid.classList.add("cols-3");
    }

    function setActiveFeedCount(count) {
      const n = Math.max(1, Math.min(MAX_FEEDS, Number(count) || 1));
      const input = document.getElementById("feed-count-input");
      if (input) input.value = String(n);

      document.querySelectorAll(".feed-card").forEach(card => {
        const feedId = Number(card.getAttribute("data-feed"));
        card.classList.toggle("hidden", feedId > n);
      });

      setGridColumns(n);
      syncVisibleFeedViewers(n);
    }

    window.addEventListener("DOMContentLoaded", async () => {
      buildFeedCards();
      wireFeedCountControls();

      for (let i = 1; i <= MAX_FEEDS; i++) {
        wireFeedSearch(i);
      }

      wireGridButtons();
      wireEnter();
      wireJsonFeedButtons();

      for (let i = 2; i <= MAX_FEEDS; i++) {
        loadJsonFeed(i);
      }

      setInterval(() => {
        for (let i = 2; i <= MAX_FEEDS; i++) {
          loadJsonFeed(i);
        }
      }, 5000);
    });
  </script>
</head>

<body>
  <div class="wrap">
    <div class="header">
      <h1>UROPS PANOPT | Home</h1>
      <div class="sub">Up to 33 feeds, lazy-initialized to avoid WebGL shader/runtime failures.</div>
    </div>

    <div class="topbar">
      <div class="topbar-row">
        <div class="topbar-left">
          <div class="count-box">
            <span class="label-inline">Visible feeds</span>
            <button id="feed-count-minus" class="small-btn" type="button">-</button>
            <input id="feed-count-input" type="number" min="1" max="33" value="1" />
            <button id="feed-count-plus" class="small-btn" type="button">+</button>
          </div>
        </div>

        <div class="topbar-right">
          <span class="label-inline">Display mode</span>
          <div class="view-mode-group">
            <button id="view-mode-tiles" class="btn active" type="button">Tiles</button>
            <button id="view-mode-popouts" class="btn" type="button">Pop out active feeds</button>
          </div>
        </div>
      </div>
    </div>

    <div id="feeds-grid-section">
      <div id="feeds-grid" class="feeds-grid cols-1"></div>
    </div>

    <div class="controls">
      <div class="controls-row">
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
    </div>

    <div class="json-feeds">
      ${''.join([
        f'''
      <div class="json-feed-card" data-feed="{i}">
        <div class="json-feed-top">
          <div class="json-feed-title">DATA FEED {i}</div>
          <button class="small-btn add-feed" type="button">Refresh</button>
        </div>
        <div class="feed-content">Loading…</div>
        <div class="feed-desc">Description for FEED {i}.</div>
      </div>''' for i in range(2, 34)
      ])}
    </div>
  </div>
</body>
</html>
"""