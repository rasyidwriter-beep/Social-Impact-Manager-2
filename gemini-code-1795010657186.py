import os, zipfile

os.makedirs("social-impact-manager/css", exist_ok=True)
os.makedirs("social-impact-manager/js", exist_ok=True)
os.makedirs("social-impact-manager/assets/characters", exist_ok=True)
os.makedirs("social-impact-manager/assets/environment", exist_ok=True)
os.makedirs("social-impact-manager/assets/buildings", exist_ok=True)
os.makedirs("social-impact-manager/assets/ui", exist_ok=True)

index_html = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Social Impact Manager — Islamic Social Finance RPG</title>
  <link rel="stylesheet" href="css/style.css" />
</head>
<body>
  <div id="app">
    <!-- START / CHARACTER SELECTION OVERLAY -->
    <div id="start-screen" class="overlay active">
      <div class="start-card">
        <div class="badge">ISLAMIC SOCIAL FINANCE SIMULATION RPG</div>
        <h1>SOCIAL IMPACT MANAGER</h1>
        <p class="subtitle">Kelola amanah dana umat, identifikasi masalah desa, dan bangun dampak sosial berkelanjutan.</p>

        <div class="char-select-group">
          <label class="section-label">Pilih Karakter Amil / Manajer Program:</label>
          <div class="char-options">
            <button type="button" class="char-card selected" data-gender="male" id="select-male">
              <canvas id="preview-male" width="72" height="84"></canvas>
              <div class="char-info">
                <strong>Faris Al-Amin</strong>
                <span>Manajer Program Laki-laki</span>
              </div>
            </button>
            <button type="button" class="char-card" data-gender="female" id="select-female">
              <canvas id="preview-female" width="72" height="84"></canvas>
              <div class="char-info">
                <strong>Aisyah Rahma</strong>
                <span>Manajer Program Perempuan</span>
              </div>
            </button>
          </div>
        </div>

        <div class="start-actions">
          <button id="btn-start-new" class="btn-primary">Mulai Amanah Baru</button>
          <button id="btn-continue" class="btn-secondary hidden">Lanjutkan Progres Tersimpan</button>
        </div>
        <div class="controls-hint">
          <span>Desktop: <b>WASD / Panah</b> Gerak &bull; <b>E / Spasi</b> Interaksi</span>
          <span>Mobile: <b>Virtual D-Pad</b> &amp; <b>Tombol Aksi</b></span>
        </div>
      </div>
    </div>

    <!-- TOP HUD -->
    <header id="top-hud">
      <div class="hud-brand">
        <span class="brand-dot"></span>
        <div>
          <div class="brand-title">BSI Maslahat &bull; Desa Sejahtera</div>
          <div class="hud-day" id="hud-day">Periode: Hari 1 / 30</div>
        </div>
      </div>

      <div class="hud-metrics">
        <div class="metric-pill" title="Dana Lembaga (Likuiditas)">
          <span class="metric-label">Dana Amanah</span>
          <span class="metric-value" id="hud-budget">Rp 15.000.000</span>
        </div>
        <div class="metric-pill" title="Reputasi & Kepercayaan Masyarakat">
          <span class="metric-label">Reputasi</span>
          <span class="metric-value" id="hud-reputation">70%</span>
        </div>
        <div class="metric-pill" title="Total Skor Dampak Sosial">
          <span class="metric-label">Dampak Sosial</span>
          <span class="metric-value" id="hud-impact">0</span>
        </div>
        <div class="metric-pill" title="Warga Terbantu">
          <span class="metric-label">Terbantu</span>
          <span class="metric-value" id="hud-beneficiaries">0 Jiwa</span>
        </div>
      </div>

      <div class="hud-actions">
        <button id="btn-open-dashboard" class="btn-hud" title="Buka Dashboard Lembaga">📊 Lembaga</button>
        <button id="btn-next-day" class="btn-hud btn-accent" title="Akhiri Hari & Evaluasi Program">⏭️ Hari Berikutnya</button>
      </div>
    </header>

    <!-- MAIN GAME CANVAS -->
    <main id="game-wrapper">
      <canvas id="game-canvas"></canvas>

      <!-- FLOATING INTERACTION PROMPT -->
      <div id="interact-prompt" class="hidden">
        <span class="key-badge">E</span>
        <span id="interact-label">Bicara</span>
      </div>

      <!-- NOTIFICATION TOAST -->
      <div id="toast-container"></div>

      <!-- MINI MISSION TRACKER -->
      <aside id="mini-tracker">
        <div class="tracker-header">
          <span>📌 Program Aktif (<span id="active-count">0</span>)</span>
          <button id="btn-toggle-tracker" aria-label="Minimize">−</button>
        </div>
        <div id="tracker-body">
          <p class="empty-note">Jelajahi desa &amp; bicara dengan warga untuk mengidentifikasi kebutuhan.</p>
        </div>
      </aside>

      <!-- MOBILE TOUCH CONTROLS -->
      <div id="mobile-controls">
        <div class="dpad">
          <button class="dpad-btn up" data-dir="up" aria-label="Atas">▲</button>
          <button class="dpad-btn left" data-dir="left" aria-label="Kiri">◀</button>
          <button class="dpad-btn right" data-dir="right" aria-label="Kanan">▶</button>
          <button class="dpad-btn down" data-dir="down" aria-label="Bawah">▼</button>
        </div>
        <button id="btn-mobile-interact" class="action-btn">INTERAKSI<br><small>(E)</small></button>
      </div>
    </main>

    <!-- DIALOG MODAL (NPC & BUILDING INTERACTION) -->
    <div id="dialog-modal" class="modal hidden">
      <div class="modal-card dialog-card">
        <div class="dialog-header">
          <div class="npc-avatar" id="dialog-avatar"></div>
          <div>
            <h3 id="dialog-speaker">Nama NPC</h3>
            <span class="npc-role" id="dialog-role">Peran</span>
          </div>
          <button class="btn-close" id="btn-close-dialog">&times;</button>
        </div>
        <div class="dialog-body">
          <p id="dialog-text">Teks dialog...</p>
          <div id="dialog-quest-box" class="quest-offer hidden"></div>
        </div>
        <div class="dialog-footer" id="dialog-choices"></div>
      </div>
    </div>

    <!-- INSTITUTION MANAGEMENT DASHBOARD MODAL -->
    <div id="dashboard-modal" class="modal hidden">
      <div class="modal-card dashboard-card">
        <div class="modal-header">
          <div>
            <h2>Manajemen Lembaga &amp; Tata Kelola Dana</h2>
            <p class="modal-sub">Evaluasi likuiditas, opportunity cost, dan prioritas program sosial</p>
          </div>
          <button class="btn-close" id="btn-close-dashboard">&times;</button>
        </div>

        <div class="dash-stats-grid">
          <div class="stat-box">
            <span>Dana Likuid Tersedia</span>
            <strong id="dash-budget">Rp 15.000.000</strong>
            <small id="dash-liquidity-status">Likuiditas Sehat</small>
          </div>
          <div class="stat-box">
            <span>Reputasi Lembaga</span>
            <strong id="dash-reputation">70%</strong>
            <small id="dash-rep-status">Dipercaya Warga</small>
          </div>
          <div class="stat-box">
            <span>Total Dampak Sosial</span>
            <strong id="dash-impact">0 Poin</strong>
            <small id="dash-sustainability">Keberlanjutan: 0%</small>
          </div>
          <div class="stat-box">
            <span>Program Berjalan / Selesai</span>
            <strong id="dash-programs">0 / 0</strong>
            <small id="dash-beneficiaries">0 Jiwa Terbantu</small>
          </div>
        </div>

        <div class="dash-tabs">
          <button class="tab-btn active" data-tab="tab-quests">Daftar Misi &amp; Alokasi</button>
          <button class="tab-btn" data-tab="tab-finance">Kebijakan Keuangan &amp; Ziswaf</button>
          <button class="tab-btn" data-tab="tab-log">Laporan Evaluasi</button>
        </div>

        <div class="tab-content active" id="tab-quests">
          <div id="dash-quest-list" class="quest-list"></div>
        </div>

        <div class="tab-content" id="tab-finance">
          <div class="finance-grid">
            <div class="finance-card">
              <h4>1. Skema Penyaluran Dana</h4>
              <p>Pilih pendekatan penyaluran untuk menentukan efisiensi biaya vs kecepatan dampak:</p>
              <div class="policy-options">
                <button class="policy-btn" data-policy="efficiency" id="pol-efficiency">
                  <strong>Audit Ketat &amp; Swakelola</strong>
                  <span>Biaya program -15%, tapi pengerjaan +1 hari lebih lama.</span>
                </button>
                <button class="policy-btn active" data-policy="balanced" id="pol-balanced">
                  <strong>Standar Transparan (Seimbang)</strong>
                  <span>Biaya normal, waktu standar, reputasi stabil.</span>
                </button>
                <button class="policy-btn" data-policy="fast" id="pol-fast">
                  <strong>Penyaluran Cepat Tanggap</strong>
                  <span>Selesai 1 hari lebih cepat, namun biaya operasional +20%.</span>
                </button>
              </div>
            </div>
            <div class="finance-card">
              <h4>2. Penghimpunan Dana ZISWAF &amp; Donatur</h4>
              <p>Gunakan reputasi lembaga untuk menggalang dana tambahan atau mencairkan imbal hasil wakaf produktif.</p>
              <div class="fundraise-box">
                <button id="btn-fundraise" class="btn-primary">Galang Dana Donatur (Butuh Reputasi &ge; 60%)</button>
                <small id="fundraise-cooldown">Tersedia setiap 3 hari sekali.</small>
              </div>
              <div class="system-actions">
                <button id="btn-save-manual" class="btn-secondary">💾 Simpan Progres</button>
                <button id="btn-reset-game" class="btn-danger">🔄 Reset Permainan</button>
              </div>
            </div>
          </div>
        </div>

        <div class="tab-content" id="tab-log">
          <div id="evaluation-log" class="log-list"></div>
        </div>
      </div>
    </div>

    <!-- END PERIOD SUMMARY MODAL -->
    <div id="summary-modal" class="modal hidden">
      <div class="modal-card summary-card">
        <div class="badge">LAPORAN AKHIR PERIODE (30 HARI)</div>
        <h2 id="summary-title">Evaluasi Kinerja Lembaga Sosial</h2>
        <p id="summary-desc"></p>
        <div class="dash-stats-grid" id="summary-stats"></div>
        <button id="btn-restart-summary" class="btn-primary">Mulai Periode Baru</button>
      </div>
    </div>
  </div>

  <script src="js/economy.js"></script>
  <script src="js/quest.js"></script>
  <script src="js/world.js"></script>
  <script src="js/player.js"></script>
  <script src="js/npc.js"></script>
  <script src="js/interface.js"></script>
  <script src="js/game.js"></script>
</body>
</html>
"""

style_css = """/* =========================================================
   SOCIAL IMPACT MANAGER — MODERN ISLAMIC SOCIAL FINANCE RPG
   Palette: Deep Emerald (#0f5132), Sage (#e9f5ee), Gold (#d97706),
            Warm Sand (#f8faf8), Slate (#1e293b)
   ========================================================= */

:root {
  --emerald-900: #064e3b;
  --emerald-800: #065f46;
  --emerald-700: #047857;
  --emerald-600: #059669;
  --emerald-100: #d1fae5;
  --emerald-50: #ecfdf5;
  --gold-600: #d97706;
  --gold-500: #f59e0b;
  --gold-100: #fef3c7;
  --bg-surface: #ffffff;
  --bg-muted: #f4f7f5;
  --text-main: #0f172a;
  --text-muted: #475569;
  --border-light: #cbd5e1;
  --danger: #dc2626;
  --shadow-lg: 0 18px 40px rgba(6, 78, 59, 0.18);
  --shadow-sm: 0 4px 12px rgba(15, 23, 42, 0.08);
  --radius-lg: 16px;
  --radius-md: 10px;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  font-family: 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
  background-color: #143627;
  color: var(--text-main);
}

#app {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.hidden {
  display: none !important;
}

/* =========================================================
   TOP HUD
   ========================================================= */
#top-hud {
  height: 62px;
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(8px);
  border-bottom: 2px solid var(--emerald-100);
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  z-index: 20;
  box-shadow: var(--shadow-sm);
}

.hud-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 185px;
}

.brand-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--emerald-600), var(--gold-500));
  box-shadow: 0 0 0 4px var(--emerald-50);
}

.brand-title {
  font-weight: 700;
  font-size: 0.92rem;
  color: var(--emerald-900);
}

.hud-day {
  font-size: 0.78rem;
  color: var(--text-muted);
  font-weight: 600;
}

.hud-metrics {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.metric-pill {
  background: var(--bg-muted);
  border: 1px solid #d8e5de;
  border-radius: 999px;
  padding: 5px 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.metric-label {
  font-size: 0.74rem;
  color: var(--text-muted);
  font-weight: 600;
}

.metric-value {
  font-size: 0.85rem;
  font-weight: 800;
  color: var(--emerald-800);
}

.hud-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-hud {
  border: 1px solid var(--emerald-700);
  background: var(--bg-surface);
  color: var(--emerald-800);
  font-weight: 700;
  font-size: 0.82rem;
  padding: 8px 13px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.18s ease;
}

.btn-hud:hover {
  background: var(--emerald-50);
  transform: translateY(-1px);
}

.btn-hud.btn-accent {
  background: var(--emerald-700);
  color: #ffffff;
}

.btn-hud.btn-accent:hover {
  background: var(--emerald-800);
}

/* =========================================================
   GAME VIEWPORT & OVERLAYS
   ========================================================= */
#game-wrapper {
  position: relative;
  flex: 1;
  width: 100%;
  overflow: hidden;
  background: #2b593f;
}

#game-canvas {
  display: block;
  width: 100%;
  height: 100%;
}

#interact-prompt {
  position: absolute;
  bottom: 26px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(6, 78, 59, 0.94);
  color: #fff;
  padding: 8px 16px;
  border-radius: 999px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.88rem;
  font-weight: 600;
  box-shadow: 0 8px 20px rgba(0,0,0,0.25);
  border: 1px solid rgba(255,255,255,0.2);
  z-index: 15;
  animation: pulseFloat 1.6s infinite ease-in-out;
}

@keyframes pulseFloat {
  0%, 100% { transform: translate(-50%, 0); }
  50% { transform: translate(-50%, -4px); }
}

.key-badge {
  background: var(--gold-500);
  color: #0f172a;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 6px;
  font-size: 0.78rem;
}

/* MINI MISSION TRACKER */
#mini-tracker {
  position: absolute;
  top: 14px;
  right: 14px;
  width: 265px;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(6px);
  border-radius: 12px;
  border: 1px solid #cce3d6;
  box-shadow: var(--shadow-sm);
  z-index: 14;
  overflow: hidden;
}

.tracker-header {
  background: var(--emerald-800);
  color: #fff;
  padding: 8px 12px;
  font-size: 0.8rem;
  font-weight: 700;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tracker-header button {
  background: rgba(255,255,255,0.2);
  border: none;
  color: #fff;
  width: 22px;
  height: 22px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

#tracker-body {
  padding: 10px 12px;
  max-height: 210px;
  overflow-y: auto;
  font-size: 0.78rem;
}

#tracker-body.collapsed {
  display: none;
}

.tracker-item {
  padding: 6px 0;
  border-bottom: 1px dashed #d8e5de;
}

.tracker-item:last-child {
  border-bottom: none;
}

.tracker-item strong {
  display: block;
  color: var(--emerald-900);
}

.tracker-progress {
  height: 6px;
  background: #e2e8f0;
  border-radius: 99px;
  margin-top: 4px;
  overflow: hidden;
}

.tracker-progress-fill {
  height: 100%;
  background: var(--emerald-600);
  transition: width 0.3s ease;
}

.empty-note {
  color: var(--text-muted);
  line-height: 1.4;
}

/* TOAST NOTIFICATIONS */
#toast-container {
  position: absolute;
  top: 14px;
  left: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 30;
  pointer-events: none;
  max-width: 340px;
}

.toast {
  background: rgba(15, 23, 42, 0.92);
  color: #fff;
  padding: 10px 14px;
  border-radius: 10px;
  font-size: 0.82rem;
  border-left: 4px solid var(--emerald-500, #10b981);
  box-shadow: var(--shadow-sm);
  animation: slideIn 0.25s ease;
}

.toast.warn {
  border-left-color: var(--gold-500);
}

.toast.danger {
  border-left-color: var(--danger);
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-16px); }
  to { opacity: 1; transform: translateX(0); }
}

/* =========================================================
   MOBILE CONTROLS
   ========================================================= */
#mobile-controls {
  display: none;
  position: absolute;
  bottom: 18px;
  left: 18px;
  right: 18px;
  justify-content: space-between;
  align-items: flex-end;
  pointer-events: none;
  z-index: 18;
}

.dpad {
  position: relative;
  width: 132px;
  height: 132px;
  pointer-events: auto;
}

.dpad-btn {
  position: absolute;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.45);
  background: rgba(6, 78, 59, 0.78);
  color: #fff;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(4px);
}

.dpad-btn:active {
  background: var(--gold-500);
  color: #0f172a;
}

.dpad-btn.up { top: 0; left: 44px; }
.dpad-btn.down { bottom: 0; left: 44px; }
.dpad-btn.left { top: 44px; left: 0; }
.dpad-btn.right { top: 44px; right: 0; }

.action-btn {
  pointer-events: auto;
  width: 82px;
  height: 82px;
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,0.6);
  background: rgba(217, 119, 6, 0.88);
  color: #fff;
  font-weight: 800;
  font-size: 0.72rem;
  box-shadow: 0 8px 18px rgba(0,0,0,0.3);
}

.action-btn:active {
  transform: scale(0.94);
}

@media (max-width: 860px), (pointer: coarse) {
  #mobile-controls {
    display: flex;
  }
  #mini-tracker {
    width: 200px;
    top: 10px;
    right: 10px;
  }
  .hud-brand {
    display: none;
  }
  .metric-pill {
    padding: 4px 8px;
  }
  .metric-label {
    font-size: 0.68rem;
  }
  .metric-value {
    font-size: 0.78rem;
  }
}

/* =========================================================
   START SCREEN & MODALS
   ========================================================= */
.overlay, .modal {
  position: fixed;
  inset: 0;
  background: rgba(6, 38, 28, 0.78);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  z-index: 50;
}

.start-card, .modal-card {
  background: var(--bg-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  width: 100%;
  max-width: 620px;
  padding: 28px;
  border: 1px solid #d1fae5;
  animation: popIn 0.24s ease;
}

.dashboard-card {
  max-width: 860px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

@keyframes popIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

.badge {
  display: inline-block;
  background: var(--emerald-100);
  color: var(--emerald-900);
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  padding: 5px 10px;
  border-radius: 999px;
  margin-bottom: 10px;
}

.start-card h1 {
  font-size: 1.85rem;
  color: var(--emerald-900);
  margin-bottom: 6px;
}

.subtitle {
  color: var(--text-muted);
  font-size: 0.94rem;
  line-height: 1.5;
  margin-bottom: 20px;
}

.section-label {
  display: block;
  font-weight: 700;
  font-size: 0.86rem;
  color: var(--emerald-900);
  margin-bottom: 10px;
}

.char-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 22px;
}

.char-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 12px;
  border: 2px solid #cbd5e1;
  background: var(--bg-muted);
  cursor: pointer;
  text-align: left;
  transition: all 0.18s ease;
}

.char-card.selected {
  border-color: var(--emerald-600);
  background: var(--emerald-50);
  box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.15);
}

.char-info strong {
  display: block;
  font-size: 0.96rem;
  color: var(--emerald-900);
}

.char-info span {
  font-size: 0.78rem;
  color: var(--text-muted);
}

.start-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn-primary, .btn-secondary, .btn-danger {
  padding: 11px 18px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  border: none;
  transition: all 0.18s ease;
}

.btn-primary {
  background: var(--emerald-700);
  color: #fff;
  flex: 1;
}

.btn-primary:hover {
  background: var(--emerald-800);
}

.btn-primary:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--emerald-100);
  color: var(--emerald-900);
}

.btn-secondary:hover {
  background: #a7f3d0;
}

.btn-danger {
  background: #fee2e2;
  color: var(--danger);
}

.controls-hint {
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 0.78rem;
  color: var(--text-muted);
}

/* DIALOG MODAL */
.dialog-header, .modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-bottom: 14px;
  border-bottom: 1px solid #e2e8f0;
}

.npc-avatar {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  background: var(--emerald-100);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.45rem;
  font-weight: 800;
  color: var(--emerald-900);
}

.npc-role, .modal-sub {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.btn-close {
  background: #f1f5f9;
  border: none;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  font-size: 1.3rem;
  cursor: pointer;
  color: var(--text-muted);
}

.dialog-body {
  padding: 16px 0;
  line-height: 1.6;
  font-size: 0.95rem;
}

.quest-offer {
  margin-top: 14px;
  background: var(--emerald-50);
  border: 1px solid #a7f3d0;
  border-radius: 12px;
  padding: 14px;
}

.quest-offer h4 {
  color: var(--emerald-900);
  margin-bottom: 4px;
}

.quest-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 8px;
  font-size: 0.78rem;
  font-weight: 700;
}

.tag {
  background: #fff;
  border: 1px solid #cbd5e1;
  padding: 3px 8px;
  border-radius: 6px;
}

.dialog-footer {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.choice-btn {
  text-align: left;
  padding: 11px 14px;
  border-radius: 10px;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text-main);
  cursor: pointer;
  transition: all 0.15s ease;
}

.choice-btn:hover {
  border-color: var(--emerald-600);
  background: var(--emerald-50);
}

.choice-btn.primary-choice {
  background: var(--emerald-700);
  color: #fff;
  border-color: var(--emerald-700);
}

.choice-btn.primary-choice:hover {
  background: var(--emerald-800);
}

/* DASHBOARD TABS & LISTS */
.dash-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin: 14px 0;
}

@media (max-width: 680px) {
  .dash-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-box {
  background: var(--bg-muted);
  border: 1px solid #d8e5de;
  border-radius: 12px;
  padding: 12px;
}

.stat-box span {
  display: block;
  font-size: 0.74rem;
  color: var(--text-muted);
  font-weight: 600;
}

.stat-box strong {
  display: block;
  font-size: 1.08rem;
  color: var(--emerald-900);
  margin: 3px 0;
}

.stat-box small {
  font-size: 0.72rem;
  color: var(--emerald-700);
  font-weight: 600;
}

.dash-tabs {
  display: flex;
  gap: 8px;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 10px;
  margin-bottom: 12px;
}

.tab-btn {
  background: #f1f5f9;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.82rem;
  color: var(--text-muted);
  cursor: pointer;
}

.tab-btn.active {
  background: var(--emerald-800);
  color: #fff;
}

.tab-content {
  display: none;
  overflow-y: auto;
  flex: 1;
  padding-right: 4px;
}

.tab-content.active {
  display: block;
}

.quest-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quest-card {
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  padding: 14px;
  background: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.quest-card.urgent {
  border-left: 5px solid var(--danger);
  background: #fffafa;
}

.quest-card.completed {
  background: #f0fdf4;
  border-color: #86efac;
}

.quest-card-info {
  flex: 1;
  min-width: 240px;
}

.quest-card-info h4 {
  color: var(--emerald-900);
  margin-bottom: 4px;
}

.quest-card-info p {
  font-size: 0.83rem;
  color: var(--text-muted);
  margin-bottom: 6px;
}

.finance-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

@media (max-width: 680px) {
  .finance-grid {
    grid-template-columns: 1fr;
  }
}

.finance-card {
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  padding: 16px;
  background: var(--bg-muted);
}

.finance-card h4 {
  color: var(--emerald-900);
  margin-bottom: 6px;
}

.finance-card p {
  font-size: 0.82rem;
  color: var(--text-muted);
  margin-bottom: 12px;
}

.policy-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.policy-btn {
  text-align: left;
  padding: 10px 12px;
  border-radius: 10px;
  border: 2px solid #cbd5e1;
  background: #fff;
  cursor: pointer;
}

.policy-btn.active {
  border-color: var(--emerald-600);
  background: var(--emerald-50);
}

.policy-btn strong {
  display: block;
  font-size: 0.85rem;
  color: var(--emerald-900);
}

.policy-btn span {
  font-size: 0.76rem;
  color: var(--text-muted);
}

.fundraise-box {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 18px;
}

.system-actions {
  display: flex;
  gap: 8px;
  padding-top: 12px;
  border-top: 1px solid #cbd5e1;
}

.log-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.log-entry {
  padding: 10px 12px;
  border-radius: 8px;
  background: var(--bg-muted);
  border-left: 4px solid var(--emerald-600);
  font-size: 0.83rem;
}
"""

economy_js = """// =========================================================
// ECONOMY.JS — Islamic Social Finance & Resource Management
// =========================================================

const EconomySystem = {
  formatRupiah(amount) {
    return 'Rp ' + Math.round(amount).toLocaleString('id-ID');
  },

  getPolicyModifiers(policy) {
    switch (policy) {
      case 'efficiency':
        return { costMult: 0.85, durationDelta: 1, repBonus: 2, label: 'Audit Ketat & Swakelola' };
      case 'fast':
        return { costMult: 1.20, durationDelta: -1, repBonus: 1, label: 'Penyaluran Cepat Tanggap' };
      case 'balanced':
      default:
        return { costMult: 1.00, durationDelta: 0, repBonus: 0, label: 'Standar Transparan' };
    }
  },

  calculateEffectiveCost(baseCost, policy) {
    const mod = this.getPolicyModifiers(policy);
    return Math.round(baseCost * mod.costMult);
  },

  calculateEffectiveDuration(baseDays, policy) {
    const mod = this.getPolicyModifiers(policy);
    return Math.max(1, baseDays + mod.durationDelta);
  },

  evaluateLiquidity(budget) {
    if (budget >= 8000000) return { status: 'Likuiditas Sangat Sehat', risk: 'low' };
    if (budget >= 3500000) return { status: 'Likuiditas Terjaga (Waspada)', risk: 'medium' };
    if (budget > 0) return { status: 'Likuiditas Kritis! Risiko Gagal Bayar', risk: 'high' };
    return { status: 'Kas Kosong (Butuh Penghimpunan)', risk: 'critical' };
  },

  // Daily passive operational & productive waqf returns
  processDailyCycle(state) {
    const logs = [];
    // Operational overhead (small realistic admin cost)
    const adminCost = 150000;
    state.budget = Math.max(0, state.budget - adminCost);
    logs.push(`Hari ${state.day}: Biaya operasional harian lembaga sebesar ${this.formatRupiah(adminCost)}.`);

    // Productive Waqf / Empowerment dividend if sustainability > 0
    if (state.sustainabilityScore > 0) {
      const dividend = state.sustainabilityScore * 25000;
      state.budget += dividend;
      logs.push(`Imbal hasil Wakaf Produktif & Pemberdayaan Ekonomi masuk sebesar +${this.formatRupiah(dividend)}.`);
    }

    // Low liquidity penalty on reputation if budget drops below 1M while urgent quests exist
    const urgentUnfunded = state.quests.filter(q => q.urgent && q.status === 'available');
    if (urgentUnfunded.length > 0) {
      state.reputation = Math.max(0, state.reputation - 3);
      logs.push(`Peringatan: ${urgentUnfunded.length} krisis darurat belum ditangani (−3% Reputasi).`);
    }

    return logs;
  },

  fundraise(state) {
    if (state.reputation < 60) {
      return { ok: false, message: 'Reputasi minimal 60% untuk meyakinkan donatur ZISWAF.' };
    }
    if (state.day - state.lastFundraiseDay < 3 && state.lastFundraiseDay !== 0) {
      const wait = 3 - (state.day - state.lastFundraiseDay);
      return { ok: false, message: `Kampanye donasi baru bisa dilakukan ${wait} hari lagi.` };
    }

    const baseRaise = 3500000;
    const repBonus = Math.round((state.reputation - 50) * 65000);
    const impactBonus = Math.round(state.impact * 12000);
    const total = baseRaise + repBonus + impactBonus;

    state.budget += total;
    state.lastFundraiseDay = state.day;
    return {
      ok: true,
      amount: total,
      message: `Alhamdulillah! Dana ZISWAF & donatur terkumpul sebesar ${this.formatRupiah(total)}.`
    };
  }
};
"""

quest_js = """// =========================================================
// QUEST.JS — Dynamic Social Missions & Crisis Events
// =========================================================

const INITIAL_QUESTS = [
  {
    id: 'q_water',
    npcId: 'bu_sari',
    title: 'Pemulihan Sumur & Pipa Air Bersih',
    category: 'Infrastruktur Dasar',
    description: 'Membangun filtrasi dan pompa air bersih untuk 45 kepala keluarga yang mengalami krisis air.',
    baseCost: 4000000,
    baseDays: 2,
    impactReward: 30,
    reputationReward: 8,
    beneficiaries: 180,
    sustainabilityGain: 5,
    urgent: false,
    status: 'discovered', // hidden | discovered | active | completed
    daysLeft: 2,
    unlockDay: 1
  },
  {
    id: 'q_edu',
    npcId: 'pak_hasan',
    title: 'Renovasi Ruang Belajar & Beasiswa Yatim',
    category: 'Pendidikan',
    description: 'Memperbaiki atap kelas madrasah/sekolah yang bocor dan menyediakan paket alat tulis siswa.',
    baseCost: 3500000,
    baseDays: 2,
    impactReward: 25,
    reputationReward: 7,
    beneficiaries: 95,
    sustainabilityGain: 8,
    urgent: false,
    status: 'discovered',
    daysLeft: 2,
    unlockDay: 1
  },
  {
    id: 'q_health',
    npcId: 'nadia',
    title: 'Posyandu Keliling & Obat Dasar Klinik',
    category: 'Kesehatan',
    description: 'Pengadaan obat esensial, vitamin ibu hamil, dan pemeriksaan kesehatan gratis di klinik desa.',
    baseCost: 2500000,
    baseDays: 1,
    impactReward: 20,
    reputationReward: 6,
    beneficiaries: 140,
    sustainabilityGain: 4,
    urgent: false,
    status: 'discovered',
    daysLeft: 1,
    unlockDay: 1
  },
  {
    id: 'q_umkm',
    npcId: 'pak_rahmat',
    title: 'Modal Bergulir Qardhul Hasan UMKM Desa',
    category: 'Pemberdayaan Ekonomi',
    description: 'Pembiayaan tanpa bunga dan pendampingan usaha olahan hasil tani agar warga mandiri secara ekonomi.',
    baseCost: 4500000,
    baseDays: 3,
    impactReward: 35,
    reputationReward: 10,
    beneficiaries: 60,
    sustainabilityGain: 25,
    urgent: false,
    status: 'hidden',
    daysLeft: 3,
    unlockDay: 2
  },
  {
    id: 'q_flood',
    npcId: 'pak_rahmat',
    title: 'DARURAT: Banjir Bandang & Dapur Umum',
    category: 'Tanggap Bencana',
    description: 'Hujan lebat merendam pemukiman hilir. Warga butuh logistik pangan, selimut, dan evakuasi segera.',
    baseCost: 5000000,
    baseDays: 1,
    impactReward: 40,
    reputationReward: 14,
    beneficiaries: 250,
    sustainabilityGain: 2,
    urgent: true,
    status: 'hidden',
    daysLeft: 1,
    unlockDay: 5
  },
  {
    id: 'q_dropout',
    npcId: 'pak_hasan',
    title: 'Program Cegah Anak Putus Sekolah',
    category: 'Pendidikan & Advokasi',
    description: 'Pendampingan keluarga prasejahtera agar anak-anak yang bekerja di ladang dapat kembali bersekolah.',
    baseCost: 3000000,
    baseDays: 2,
    impactReward: 28,
    reputationReward: 9,
    beneficiaries: 40,
    sustainabilityGain: 15,
    urgent: false,
    status: 'hidden',
    daysLeft: 2,
    unlockDay: 8
  },
  {
    id: 'q_fire',
    npcId: 'bu_sari',
    title: 'DARURAT: Kebakaran Lahan & Masker Respirasi',
    category: 'Bencana Lingkungan',
    description: 'Asap kebakaran hutan mengancam pernapasan warga. Klinik butuh oksigen, masker N95, dan sekat bakar.',
    baseCost: 4200000,
    baseDays: 1,
    impactReward: 38,
    reputationReward: 12,
    beneficiaries: 210,
    sustainabilityGain: 6,
    urgent: true,
    status: 'hidden',
    daysLeft: 1,
    unlockDay: 12
  },
  {
    id: 'q_waqf_farm',
    npcId: 'pak_rahmat',
    title: 'Kebun Wakaf Produktif & Ketahanan Pangan',
    category: 'Wakaf Produktif',
    description: 'Mengelola lahan tidur masjid menjadi kebun hidroponik & pangan produktif berkelanjutan.',
    baseCost: 6000000,
    baseDays: 3,
    impactReward: 50,
    reputationReward: 15,
    beneficiaries: 300,
    sustainabilityGain: 35,
    urgent: false,
    status: 'hidden',
    daysLeft: 3,
    unlockDay: 15
  }
];

const QuestSystem = {
  cloneInitialQuests() {
    return JSON.parse(JSON.stringify(INITIAL_QUESTS));
  },

  checkDynamicEvents(state) {
    const announcements = [];
    state.quests.forEach(q => {
      if (q.status === 'hidden' && state.day >= q.unlockDay) {
        q.status = 'discovered';
        announcements.push(
          q.urgent
            ? `🚨 KRISIS BARU: ${q.title}! Segera alokasikan dana sebelum reputasi turun.`
            : `📢 Kebutuhan Baru Teridentifikasi: ${q.title}.`
        );
      }
    });
    return announcements;
  },

  approveQuest(state, questId) {
    const q = state.quests.find(item => item.id === questId);
    if (!q || (q.status !== 'discovered' && q.status !== 'available')) {
      return { ok: false, message: 'Program tidak tersedia untuk disetujui.' };
    }

    const effectiveCost = EconomySystem.calculateEffectiveCost(q.baseCost, state.policy);
    if (state.budget < effectiveCost) {
      return {
        ok: false,
        message: `Dana tidak mencukupi! Butuh ${EconomySystem.formatRupiah(effectiveCost)}, tersedia ${EconomySystem.formatRupiah(state.budget)}.`
      };
    }

    const effectiveDays = EconomySystem.calculateEffectiveDuration(q.baseDays, state.policy);
    state.budget -= effectiveCost;
    q.status = 'active';
    q.daysLeft = effectiveDays;
    q.totalDays = effectiveDays;
    q.spentCost = effectiveCost;

    // Opportunity cost feedback if liquidity drops low
    let warning = '';
    if (state.budget < 2000000) {
      warning = ' Peringatan: Likuiditas lembaga kini sangat tipis!';
    }

    return {
      ok: true,
      message: `Program "${q.title}" disetujui (${EconomySystem.formatRupiah(effectiveCost)}, estimasi ${effectiveDays} hari).${warning}`
    };
  },

  advanceActiveQuests(state) {
    const results = [];
    const policyMod = EconomySystem.getPolicyModifiers(state.policy);

    state.quests.forEach(q => {
      if (q.status === 'active') {
        q.daysLeft -= 1;
        if (q.daysLeft <= 0) {
          q.status = 'completed';
          state.impact += q.impactReward;
          state.reputation = Math.min(100, state.reputation + q.reputationReward + policyMod.repBonus);
          state.beneficiaries += q.beneficiaries;
          state.sustainabilityScore += q.sustainabilityGain;
          results.push(
            `✅ Program Selesai: "${q.title}" (+${q.impactReward} Dampak, +${q.beneficiaries} jiwa terbantu).`
          );
        }
      }
    });

    return results;
  }
};
"""

world_js = """// =========================================================
// WORLD.JS — 2D Top-Down Village Environment & Buildings
// =========================================================

const WorldMap = {
  width: 1800,
  height: 1300,
  tileSize: 48,

  buildings: [
    {
      id: 'office',
      name: 'Kantor Lembaga BSI Maslahat',
      role: 'Pusat Tata Kelola & Keuangan',
      x: 760,
      y: 440,
      w: 220,
      h: 150,
      roofColor: '#065f46',
      wallColor: '#f8fafc',
      accentColor: '#f59e0b',
      doorX: 870,
      doorY: 590,
      description: 'Pusat perencanaan program sosial, audit dana ZISWAF, dan evaluasi dampak masyarakat.',
      actionType: 'dashboard'
    },
    {
      id: 'mosque',
      name: 'Masjid Al-Maslahah',
      role: 'Pusat Ibadah & Baitul Mal',
      x: 1140,
      y: 380,
      w: 230,
      h: 175,
      roofColor: '#047857',
      wallColor: '#fefce8',
      accentColor: '#d97706',
      doorX: 1255,
      doorY: 555,
      description: 'Pusat penghimpunan zakat, infak, sedekah, wakaf produktif, dan musyawarah umat.',
      actionType: 'fundraise'
    },
    {
      id: 'school',
      name: 'Madrasah & Sekolah Harapan',
      role: 'Fasilitas Pendidikan Desa',
      x: 260,
      y: 260,
      w: 230,
      h: 155,
      roofColor: '#1d4ed8',
      wallColor: '#eff6ff',
      accentColor: '#3b82f6',
      doorX: 375,
      doorY: 415,
      description: 'Tempat belajar anak-anak desa. Beberapa ruang kelas membutuhkan renovasi dan beasiswa.',
      actionType: 'quest_edu'
    },
    {
      id: 'clinic',
      name: 'Klinik Pratama Sehat Umat',
      role: 'Layanan Kesehatan Masyarakat',
      x: 1220,
      y: 780,
      w: 210,
      h: 145,
      roofColor: '#be123c',
      wallColor: '#fff1f2',
      accentColor: '#fb7185',
      doorX: 1325,
      doorY: 925,
      description: 'Klinik layanan ibu dan anak serta pengobatan dasar bagi keluarga prasejahtera.',
      actionType: 'quest_health'
    },
    {
      id: 'hall',
      name: 'Balai Musyawarah Masyarakat',
      role: 'Pusat Koordinasi Warga',
      x: 740,
      y: 820,
      w: 240,
      h: 150,
      roofColor: '#92400e',
      wallColor: '#fffbeb',
      accentColor: '#d97706',
      doorX: 860,
      doorY: 970,
      description: 'Tempat warga berkumpul menyampaikan aspirasi, laporan bencana, dan pelatihan UMKM.',
      actionType: 'hall_info'
    },
    {
      id: 'house_1',
      name: 'Rumah Warga (Kawasan Sumur Tua)',
      role: 'Pemukiman Warga Barat',
      x: 240,
      y: 760,
      w: 170,
      h: 125,
      roofColor: '#7c2d12',
      wallColor: '#fef3c7',
      accentColor: '#b45309',
      doorX: 325,
      doorY: 885,
      description: 'Pemukiman warga yang terdampak kekeringan dan keterbatasan akses air bersih.',
      actionType: 'quest_water'
    },
    {
      id: 'house_2',
      name: 'Rumah Warga & Sentra Tani',
      role: 'Pemukiman Warga Timur',
      x: 460,
      y: 800,
      w: 165,
      h: 120,
      roofColor: '#78350f',
      wallColor: '#fef9c3',
      accentColor: '#ca8a04',
      doorX: 542,
      doorY: 920,
      description: 'Perumahan petani dan pelaku usaha mikro desa yang membutuhkan modal bergulir.',
      actionType: 'house_info'
    }
  ],

  trees: [
    { x: 120, y: 140, r: 28 }, { x: 185, y: 120, r: 24 }, { x: 600, y: 160, r: 30 },
    { x: 670, y: 145, r: 25 }, { x: 1020, y: 170, r: 28 }, { x: 1520, y: 200, r: 32 },
    { x: 1600, y: 270, r: 26 }, { x: 1580, y: 620, r: 30 }, { x: 1640, y: 1040, r: 32 },
    { x: 150, y: 540, r: 28 }, { x: 130, y: 1040, r: 32 }, { x: 420, y: 1120, r: 27 },
    { x: 1050, y: 1100, r: 30 }, { x: 1130, y: 1130, r: 25 }, { x: 640, y: 520, r: 22 }
  ],

  well: { x: 195, y: 925, r: 22 },

  colliders: [],

  init() {
    this.colliders = [];
    // Building solid bounding boxes
    this.buildings.forEach(b => {
      this.colliders.push({ x: b.x + 6, y: b.y + 18, w: b.w - 12, h: b.h - 22 });
    });
    // Tree trunks
    this.trees.forEach(t => {
      this.colliders.push({ x: t.x - 10, y: t.y - 6, w: 20, h: 18 });
    });
    // Village well
    this.colliders.push({ x: this.well.x - 18, y: this.well.y - 18, w: 36, h: 36 });
  },

  checkCollision(rect) {
    if (rect.x < 24 || rect.y < 24 || rect.x + rect.w > this.width - 24 || rect.y + rect.h > this.height - 24) {
      return true;
    }
    for (const c of this.colliders) {
      if (
        rect.x < c.x + c.w &&
        rect.x + rect.w > c.x &&
        rect.y < c.y + c.h &&
        rect.y + rect.h > c.y
      ) {
        return true;
      }
    }
    return false;
  },

  draw(ctx, camera) {
    ctx.save();
    ctx.translate(-camera.x, -camera.y);

    // Base lush meadow grass
    ctx.fillStyle = '#4d8b55';
    ctx.fillRect(0, 0, this.width, this.height);

    // Subtle grass texture tiles
    ctx.fillStyle = '#46824e';
    for (let gx = 0; gx < this.width; gx += 96) {
      for (let gy = 0; gy < this.height; gy += 96) {
        if ((gx + gy) % 192 === 0) {
          ctx.fillRect(gx, gy, 48, 48);
        }
      }
    }

    // Perimeter hedge / border
    ctx.strokeStyle = '#1e4620';
    ctx.lineWidth = 24;
    ctx.strokeRect(12, 12, this.width - 24, this.height - 24);

    // Village Roads (Paved Stone/Sand Pathways)
    ctx.fillStyle = '#e5dec9';
    // Horizontal main avenue
    ctx.fillRect(280, 645, 1120, 68);
    // Vertical central avenue
    ctx.fillRect(835, 340, 68, 690);
    // Branch to School
    ctx.fillRect(340, 415, 58, 250);
    // Branch to Mosque
    ctx.fillRect(1225, 555, 58, 110);
    // Branch to Clinic
    ctx.fillRect(1295, 695, 58, 240);
    // Branch to West Houses
    ctx.fillRect(300, 695, 54, 210);

    // Road borders
    ctx.strokeStyle = '#cbbba0';
    ctx.lineWidth = 3;
    ctx.strokeRect(280, 645, 1120, 68);
    ctx.strokeRect(835, 340, 68, 690);

    // Public Town Plaza (Alun-alun / Taman Sosial)
    ctx.fillStyle = '#d6e6d5';
    ctx.beginPath();
    ctx.roundRect(960, 600, 190, 165, 18);
    ctx.fill();
    ctx.strokeStyle = '#86efac';
    ctx.lineWidth = 3;
    ctx.stroke();

    // Plaza Fountain
    ctx.fillStyle = '#38bdf8';
    ctx.beginPath();
    ctx.arc(1055, 682, 26, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#0284c7';
    ctx.lineWidth = 4;
    ctx.stroke();

    // Village Well near Bu Sari
    ctx.fillStyle = '#64748b';
    ctx.beginPath();
    ctx.arc(this.well.x, this.well.y, this.well.r, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#0ea5e9';
    ctx.beginPath();
    ctx.arc(this.well.x, this.well.y, 14, 0, Math.PI * 2);
    ctx.fill();

    // Draw Buildings
    this.buildings.forEach(b => this.drawBuilding(ctx, b));

    // Draw Trees
    this.trees.forEach(t => this.drawTree(ctx, t));

    ctx.restore();
  },

  drawBuilding(ctx, b) {
    // Shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.18)';
    ctx.beginPath();
    ctx.roundRect(b.x + 8, b.y + 12, b.w, b.h, 12);
    ctx.fill();

    // Wall body
    ctx.fillStyle = b.wallColor;
    ctx.beginPath();
    ctx.roundRect(b.x, b.y + 28, b.w, b.h - 28, 8);
    ctx.fill();
    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Roof
    ctx.fillStyle = b.roofColor;
    ctx.beginPath();
    ctx.roundRect(b.x - 6, b.y, b.w + 12, 54, 10);
    ctx.fill();

    // Roof trim
    ctx.fillStyle = b.accentColor;
    ctx.fillRect(b.x + 8, b.y + 44, b.w - 16, 6);

    // Mosque Dome ornament
    if (b.id === 'mosque') {
      ctx.fillStyle = '#f59e0b';
      ctx.beginPath();
      ctx.arc(b.x + b.w / 2, b.y + 22, 24, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    // Windows
    ctx.fillStyle = '#bae6fd';
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 1.5;
    const winY = b.y + 70;
    ctx.fillRect(b.x + 24, winY, 34, 28);
    ctx.strokeRect(b.x + 24, winY, 34, 28);
    ctx.fillRect(b.x + b.w - 58, winY, 34, 28);
    ctx.strokeRect(b.x + b.w - 58, winY, 34, 28);

    // Door
    ctx.fillStyle = '#78350f';
    ctx.fillRect(b.doorX - 16, b.y + b.h - 42, 32, 42);

    // Door interaction mat
    ctx.fillStyle = 'rgba(245, 158, 11, 0.35)';
    ctx.beginPath();
    ctx.arc(b.doorX, b.doorY + 14, 16, 0, Math.PI * 2);
    ctx.fill();

    // Building Signboard
    ctx.font = 'bold 12px Segoe UI, sans-serif';
    const textWidth = ctx.measureText(b.name).width;
    ctx.fillStyle = 'rgba(15, 23, 42, 0.84)';
    ctx.beginPath();
    ctx.roundRect(b.x + b.w / 2 - textWidth / 2 - 8, b.y - 24, textWidth + 16, 20, 6);
    ctx.fill();
    ctx.fillStyle = '#ffffff';
    ctx.textAlign = 'center';
    ctx.fillText(b.name, b.x + b.w / 2, b.y - 10);
  },

  drawTree(ctx, t) {
    // Ground shadow
    ctx.fillStyle = 'rgba(0,0,0,0.16)';
    ctx.beginPath();
    ctx.ellipse(t.x + 6, t.y + 14, t.r * 0.9, t.r * 0.5, 0, 0, Math.PI * 2);
    ctx.fill();

    // Trunk
    ctx.fillStyle = '#5c4033';
    ctx.fillRect(t.x - 5, t.y - 4, 10, 18);

    // Foliage layers
    ctx.fillStyle = '#1b5e20';
    ctx.beginPath();
    ctx.arc(t.x, t.y - 12, t.r, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = '#2e7d32';
    ctx.beginPath();
    ctx.arc(t.x - 5, t.y - 16, t.r * 0.72, 0, Math.PI * 2);
    ctx.fill();
  }
};
"""

player_js = """// =========================================================
// PLAYER.JS — Articulated 2D Top-Down Human Character
// =========================================================

const Player = {
  x: 870,
  y: 650,
  w: 28,
  h: 24,
  speed: 225,
  gender: 'male', // 'male' | 'female'
  direction: 'down', // 'down' | 'up' | 'left' | 'right'
  walkTimer: 0,
  isMoving: false,

  reset(gender = 'male') {
    this.x = 870;
    this.y = 650;
    this.gender = gender;
    this.direction = 'down';
    this.walkTimer = 0;
    this.isMoving = false;
  },

  update(dt, input) {
    let vx = 0;
    let vy = 0;

    if (input.up) vy -= 1;
    if (input.down) vy += 1;
    if (input.left) vx -= 1;
    if (input.right) vx += 1;

    if (vx !== 0 && vy !== 0) {
      const inv = 1 / Math.SQRT2;
      vx *= inv;
      vy *= inv;
    }

    this.isMoving = vx !== 0 || vy !== 0;

    if (this.isMoving) {
      if (Math.abs(vx) > Math.abs(vy)) {
        this.direction = vx < 0 ? 'left' : 'right';
      } else {
        this.direction = vy < 0 ? 'up' : 'down';
      }
      this.walkTimer += dt * 10;

      // Axis-separated smooth collision
      const nextX = this.x + vx * this.speed * dt;
      if (!WorldMap.checkCollision({ x: nextX - this.w / 2, y: this.y - this.h / 2, w: this.w, h: this.h })) {
        this.x = nextX;
      }

      const nextY = this.y + vy * this.speed * dt;
      if (!WorldMap.checkCollision({ x: this.x - this.w / 2, y: nextY - this.h / 2, w: this.w, h: this.h })) {
        this.y = nextY;
      }
    } else {
      this.walkTimer = 0;
    }
  },

  draw(ctx, camera) {
    ctx.save();
    ctx.translate(this.x - camera.x, this.y - camera.y);
    drawHumanCharacter(ctx, {
      gender: this.gender,
      direction: this.direction,
      walkPhase: this.walkTimer,
      isMoving: this.isMoving,
      outfitPrimary: '#047857',
      outfitSecondary: '#f8fafc',
      accent: '#f59e0b',
      scale: 1
    });
    ctx.restore();
  }
};

// Reusable realistic human proportion renderer (for Player & NPCs)
function drawHumanCharacter(ctx, opts) {
  const {
    gender = 'male',
    direction = 'down',
    walkPhase = 0,
    isMoving = false,
    outfitPrimary = '#047857',
    outfitSecondary = '#f8fafc',
    accent = '#f59e0b',
    scale = 1
  } = opts;

  ctx.save();
  ctx.scale(scale, scale);

  const swing = isMoving ? Math.sin(walkPhase) * 4.5 : 0;
  const bob = isMoving ? Math.abs(Math.cos(walkPhase)) * 1.8 : 0;

  // Ground shadow
  ctx.fillStyle = 'rgba(0, 0, 0, 0.24)';
  ctx.beginPath();
  ctx.ellipse(0, 12, 13, 6, 0, 0, Math.PI * 2);
  ctx.fill();

  // Legs / Trousers (Proportional human lower body)
  ctx.fillStyle = '#1e293b';
  if (direction === 'left' || direction === 'right') {
    ctx.beginPath();
    ctx.roundRect(-4 + swing, 1, 7, 11, 3);
    ctx.roundRect(-4 - swing, 1, 7, 11, 3);
    ctx.fill();
  } else {
    ctx.beginPath();
    ctx.roundRect(-7, 1 + swing * 0.5, 6, 11, 3);
    ctx.roundRect(1, 1 - swing * 0.5, 6, 11, 3);
    ctx.fill();
  }

  // Torso (Realistic shoulder-to-head ratio, ~20px wide, ~18px tall)
  const torsoY = -16 - bob;
  ctx.fillStyle = outfitPrimary;
  if (direction === 'left' || direction === 'right') {
    ctx.beginPath();
    ctx.roundRect(-7, torsoY, 14, 19, 5);
    ctx.fill();
  } else {
    // Shoulders & Vest/Tunic
    ctx.beginPath();
    ctx.roundRect(-10, torsoY, 20, 19, 6);
    ctx.fill();

    // Inner shirt / lanyard detail
    if (direction === 'down') {
      ctx.fillStyle = outfitSecondary;
      ctx.beginPath();
      ctx.moveTo(-4, torsoY);
      ctx.lineTo(4, torsoY);
      ctx.lineTo(0, torsoY + 9);
      ctx.closePath();
      ctx.fill();

      // ID Badge / Lanyard
      ctx.fillStyle = accent;
      ctx.fillRect(2, torsoY + 6, 4, 5);
    }
  }

  // Arms
  ctx.fillStyle = outfitPrimary;
  if (direction === 'down' || direction === 'up') {
    ctx.beginPath();
    ctx.roundRect(-14, torsoY + 2 - swing * 0.4, 4.5, 13, 2.5);
    ctx.roundRect(9.5, torsoY + 2 + swing * 0.4, 4.5, 13, 2.5);
    ctx.fill();
    // Hands
    ctx.fillStyle = '#f1c27d';
    ctx.beginPath();
    ctx.arc(-11.8, torsoY + 15 - swing * 0.4, 2.3, 0, Math.PI * 2);
    ctx.arc(11.8, torsoY + 15 + swing * 0.4, 2.3, 0, Math.PI * 2);
    ctx.fill();
  } else {
    // Side arm swinging
    ctx.beginPath();
    ctx.roundRect(-2.5 - swing * 0.6, torsoY + 2, 5, 13, 2.5);
    ctx.fill();
    ctx.fillStyle = '#f1c27d';
    ctx.beginPath();
    ctx.arc(-swing * 0.6, torsoY + 15, 2.3, 0, Math.PI * 2);
    ctx.fill();
  }

  // Head (Proportional human head: radius ~7.5px, NOT oversized chibi)
  const headY = torsoY - 7;
  ctx.fillStyle = '#f1c27d';
  ctx.beginPath();
  ctx.arc(0, headY, 7.5, 0, Math.PI * 2);
  ctx.fill();

  // Hair / Hijab / Peci styling
  if (gender === 'female') {
    // Neat modern Hijab draping naturally over shoulders
    ctx.fillStyle = outfitSecondary;
    ctx.beginPath();
    ctx.arc(0, headY - 0.5, 8.8, Math.PI * 0.85, Math.PI * 2.15);
    ctx.lineTo(8.5, torsoY + 4);
    ctx.lineTo(-8.5, torsoY + 4);
    ctx.closePath();
    ctx.fill();

    if (direction !== 'up') {
      // Face opening
      ctx.fillStyle = '#f1c27d';
      const faceOffsetX = direction === 'left' ? -2.5 : direction === 'right' ? 2.5 : 0;
      ctx.beginPath();
      ctx.arc(faceOffsetX, headY + 0.5, 5.8, 0, Math.PI * 2);
      ctx.fill();
    }
  } else {
    // Male hair & neat cap/peci
    ctx.fillStyle = '#1e293b';
    ctx.beginPath();
    ctx.arc(0, headY - 1.5, 7.8, Math.PI, Math.PI * 2);
    ctx.fill();
    if (direction === 'up') {
      ctx.beginPath();
      ctx.arc(0, headY, 7.8, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  // Eyes (Directional)
  if (direction !== 'up') {
    ctx.fillStyle = '#0f172a';
    if (direction === 'down') {
      ctx.fillRect(-3.2, headY - 0.5, 1.8, 2.2);
      ctx.fillRect(1.5, headY - 0.5, 1.8, 2.2);
    } else if (direction === 'left') {
      ctx.fillRect(-5.2, headY - 0.5, 1.8, 2.2);
    } else if (direction === 'right') {
      ctx.fillRect(3.4, headY - 0.5, 1.8, 2.2);
    }
  }

  ctx.restore();
}
"""

npc_js = """// =========================================================
// NPC.JS — Interactive Villagers & Dynamic Dialogue
// =========================================================

const NPCSystem = {
  list: [
    {
      id: 'bu_sari',
      name: 'Bu Sari',
      role: 'Perwakilan Warga & Kader PKK',
      x: 245,
      y: 930,
      gender: 'female',
      direction: 'right',
      outfitPrimary: '#b45309',
      outfitSecondary: '#fef3c7',
      accent: '#10b981',
      questIds: ['q_water', 'q_fire']
    },
    {
      id: 'pak_hasan',
      name: 'Pak Hasan',
      role: 'Kepala Madrasah & Guru Desa',
      x: 425,
      y: 445,
      gender: 'male',
      direction: 'down',
      outfitPrimary: '#1e40af',
      outfitSecondary: '#dbeafe',
      accent: '#f59e0b',
      questIds: ['q_edu', 'q_dropout']
    },
    {
      id: 'nadia',
      name: 'Nadia',
      role: 'Relawan Kesehatan Klinik',
      x: 1275,
      y: 950,
      gender: 'female',
      direction: 'left',
      outfitPrimary: '#be123c',
      outfitSecondary: '#ffffff',
      accent: '#059669',
      questIds: ['q_health']
    },
    {
      id: 'pak_rahmat',
      name: 'Pak Rahmat',
      role: 'Koordinator Masyarakat Desa',
      x: 915,
      y: 990,
      gender: 'male',
      direction: 'up',
      outfitPrimary: '#3f6212',
      outfitSecondary: '#ecfccb',
      accent: '#d97706',
      questIds: ['q_umkm', 'q_flood', 'q_waqf_farm']
    }
  ],

  draw(ctx, camera, state) {
    this.list.forEach(npc => {
      // Face toward player if nearby
      const dx = Player.x - npc.x;
      const dy = Player.y - npc.y;
      const dist = Math.hypot(dx, dy);
      if (dist < 90) {
        if (Math.abs(dx) > Math.abs(dy)) {
          npc.direction = dx < 0 ? 'left' : 'right';
        } else {
          npc.direction = dy < 0 ? 'up' : 'down';
        }
      }

      ctx.save();
      ctx.translate(npc.x - camera.x, npc.y - camera.y);
      drawHumanCharacter(ctx, {
        gender: npc.gender,
        direction: npc.direction,
        isMoving: false,
        outfitPrimary: npc.outfitPrimary,
        outfitSecondary: npc.outfitSecondary,
        accent: npc.accent
      });

      // Nameplate
      ctx.font = 'bold 11px Segoe UI, sans-serif';
      const label = npc.name;
      const w = ctx.measureText(label).width + 12;
      ctx.fillStyle = 'rgba(15, 23, 42, 0.78)';
      ctx.beginPath();
      ctx.roundRect(-w / 2, -42, w, 17, 5);
      ctx.fill();
      ctx.fillStyle = '#fff';
      ctx.textAlign = 'center';
      ctx.fillText(label, 0, -30);

      // Quest indicator marker (! or ?)
      const npcQuests = state.quests.filter(q => npc.questIds.includes(q.id));
      const hasUrgent = npcQuests.some(q => q.urgent && q.status === 'discovered');
      const hasNew = npcQuests.some(q => q.status === 'discovered');
      const hasActive = npcQuests.some(q => q.status === 'active');

      if (hasUrgent || hasNew || hasActive) {
        ctx.fillStyle = hasUrgent ? '#dc2626' : hasNew ? '#f59e0b' : '#10b981';
        ctx.beginPath();
        ctx.arc(0, -54, 9, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 12px Segoe UI, sans-serif';
        ctx.fillText(hasUrgent ? '!!' : hasNew ? '!' : '⏳', 0, -50);
      }

      ctx.restore();
    });
  },

  getDialogueData(npc, state) {
    const relatedQuests = state.quests.filter(q => npc.questIds.includes(q.id) && q.status !== 'hidden');
    const availableQuest = relatedQuests.find(q => q.status === 'discovered');
    const activeQuest = relatedQuests.find(q => q.status === 'active');
    const completedCount = relatedQuests.filter(q => q.status === 'completed').length;

    let text = '';
    if (availableQuest) {
      if (npc.id === 'bu_sari') {
        text = availableQuest.id === 'q_water'
          ? 'Assalamualaikum! Sumur warga di sisi barat mengering dan airnya keruh. Warga sangat membutuhkan bantuan instalasi filter & pompa air bersih.'
          : 'Asap kebakaran lahan mulai masuk ke pemukiman! Anak-anak dan lansia sesak napas, kami butuh masker dan bantuan darurat segera.';
      } else if (npc.id === 'pak_hasan') {
        text = availableQuest.id === 'q_edu'
          ? 'Selamat datang di Madrasah Harapan. Atap dua ruang kelas kami bocor saat hujan dan banyak siswa yatim kekurangan perlengkapan belajar.'
          : 'Beberapa siswa terpaksa ikut orang tuanya ke ladang karena kesulitan biaya. Kami butuh program pendampingan agar mereka tidak putus sekolah.';
      } else if (npc.id === 'nadia') {
        text = 'Stok obat dasar dan vitamin untuk ibu hamil serta balita di Klinik Pratama menipis. Dukungan lembaga akan menyelamatkan layanan kesehatan warga.';
      } else if (npc.id === 'pak_rahmat') {
        if (availableQuest.id === 'q_umkm') {
          text = 'Banyak ibu rumah tangga dan petani punya keterampilan olahan pangan, tapi terjerat rentenir. Skema Qardhul Hasan tanpa bunga akan sangat membantu kemandirian mereka.';
        } else if (availableQuest.id === 'q_flood') {
          text = 'Banjir bandang merendam dusun hilir! Warga mengungsi di balai dan membutuhkan dapur umum serta logistik darurat hari ini juga.';
        } else {
          text = 'Reputasi lembaga Anda sangat baik! Warga siap bergotong-royong mengelola lahan tidur masjid menjadi Kebun Wakaf Produktif.';
        }
      }
    } else if (activeQuest) {
      text = `Terima kasih! Tim lapangan sedang menjalankan "${activeQuest.title}". Perkiraan selesai dalam ${activeQuest.daysLeft} hari lagi.`;
    } else if (completedCount > 0) {
      text = `Alhamdulillah, warga sangat bersyukur atas realisasi program dari lembaga Anda. Kepercayaan masyarakat terhadap amanah ZISWAF semakin kuat!`;
    } else {
      text = `Assalamualaikum! Kondisi lingkungan sekitar saat ini terpantau kondusif. Silakan pantau terus kebutuhan warga di balai maupun kantor lembaga.`;
    }

    return {
      speaker: npc.name,
      role: npc.role,
      avatarText: npc.name.charAt(0),
      text,
      quest: availableQuest || activeQuest || null
    };
  }
};
"""

interface_js = """// =========================================================
// INTERFACE.JS — HUD, Dialogues, Dashboard & Notifications
// =========================================================

const UI = {
  init(callbacks) {
    this.callbacks = callbacks;

    // Dashboard open/close
    document.getElementById('btn-open-dashboard').addEventListener('click', () => {
      this.openDashboard();
    });
    document.getElementById('btn-close-dashboard').addEventListener('click', () => {
      document.getElementById('dashboard-modal').classList.add('hidden');
    });

    // Next day
    document.getElementById('btn-next-day').addEventListener('click', () => {
      callbacks.onNextDay();
    });

    // Dialog close
    document.getElementById('btn-close-dialog').addEventListener('click', () => {
      this.closeDialog();
    });

    // Tracker collapse toggle
    document.getElementById('btn-toggle-tracker').addEventListener('click', (e) => {
      const body = document.getElementById('tracker-body');
      body.classList.toggle('collapsed');
      e.target.textContent = body.classList.contains('collapsed') ? '+' : '−';
    });

    // Dashboard Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.add('active');
      });
    });

    // Financial Policy buttons
    document.querySelectorAll('.policy-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        callbacks.onChangePolicy(btn.dataset.policy);
      });
    });

    // Fundraise button
    document.getElementById('btn-fundraise').addEventListener('click', () => {
      callbacks.onFundraise();
    });

    // Save & Reset
    document.getElementById('btn-save-manual').addEventListener('click', () => {
      callbacks.onSave();
    });
    document.getElementById('btn-reset-game').addEventListener('click', () => {
      callbacks.onReset();
    });

    // Summary restart
    document.getElementById('btn-restart-summary').addEventListener('click', () => {
      callbacks.onReset();
    });
  },

  toast(message, type = 'normal') {
    const container = document.getElementById('toast-container');
    const el = document.createElement('div');
    el.className = `toast ${type}`;
    el.textContent = message;
    container.appendChild(el);
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transform = 'translateX(-12px)';
      el.style.transition = 'all 0.25s ease';
      setTimeout(() => el.remove(), 260);
    }, 3600);
  },

  updateHUD(state) {
    document.getElementById('hud-day').textContent = `Periode: Hari ${state.day} / ${state.maxDays}`;
    document.getElementById('hud-budget').textContent = EconomySystem.formatRupiah(state.budget);
    document.getElementById('hud-reputation').textContent = `${state.reputation}%`;
    document.getElementById('hud-impact').textContent = state.impact;
    document.getElementById('hud-beneficiaries').textContent = `${state.beneficiaries} Jiwa`;

    // Mini tracker update
    const activeQuests = state.quests.filter(q => q.status === 'active');
    document.getElementById('active-count').textContent = activeQuests.length;
    const trackerBody = document.getElementById('tracker-body');

    if (activeQuests.length === 0) {
      trackerBody.innerHTML = '<p class="empty-note">Belum ada program berjalan. Temui warga atau buka menu Lembaga.</p>';
    } else {
      trackerBody.innerHTML = activeQuests.map(q => {
        const total = q.totalDays || q.baseDays;
        const done = Math.max(0, total - q.daysLeft);
        const pct = Math.min(100, Math.round((done / total) * 100));
        return `
          <div class="tracker-item">
            <strong>${q.title}</strong>
            <span>Sisa waktu: ${q.daysLeft} hari</span>
            <div class="tracker-progress">
              <div class="tracker-progress-fill" style="width:${pct}%"></div>
            </div>
          </div>
        `;
      }).join('');
    }
  },

  setInteractPrompt(visible, label = '') {
    const prompt = document.getElementById('interact-prompt');
    if (visible) {
      document.getElementById('interact-label').textContent = label;
      prompt.classList.remove('hidden');
    } else {
      prompt.classList.add('hidden');
    }
  },

  openDialog(data, state) {
    document.getElementById('dialog-speaker').textContent = data.speaker;
    document.getElementById('dialog-role').textContent = data.role;
    document.getElementById('dialog-avatar').textContent = data.avatarText;
    document.getElementById('dialog-text').textContent = data.text;

    const questBox = document.getElementById('dialog-quest-box');
    const choicesBox = document.getElementById('dialog-choices');
    choicesBox.innerHTML = '';

    if (data.quest) {
      const q = data.quest;
      const effCost = EconomySystem.calculateEffectiveCost(q.baseCost, state.policy);
      const effDays = EconomySystem.calculateEffectiveDuration(q.baseDays, state.policy);
      questBox.classList.remove('hidden');
      questBox.innerHTML = `
        <h4>${q.urgent ? '🚨 ' : '📋 '}${q.title}</h4>
        <p style="font-size:0.84rem;color:#334155;margin-top:4px;">${q.description}</p>
        <div class="quest-meta">
          <span class="tag">Anggaran: ${EconomySystem.formatRupiah(effCost)}</span>
          <span class="tag">Durasi: ${effDays} Hari</span>
          <span class="tag">Dampak: +${q.impactReward}</span>
          <span class="tag">Penerima: ${q.beneficiaries} Jiwa</span>
        </div>
      `;

      if (q.status === 'discovered') {
        const approveBtn = document.createElement('button');
        approveBtn.className = 'choice-btn primary-choice';
        approveBtn.textContent = `Setujui & Salurkan Dana (${EconomySystem.formatRupiah(effCost)})`;
        approveBtn.onclick = () => {
          this.callbacks.onApproveQuest(q.id);
          this.closeDialog();
        };
        choicesBox.appendChild(approveBtn);
      }
    } else {
      questBox.classList.add('hidden');
    }

    if (data.extraAction) {
      const extraBtn = document.createElement('button');
      extraBtn.className = 'choice-btn primary-choice';
      extraBtn.textContent = data.extraAction.label;
      extraBtn.onclick = () => {
        this.closeDialog();
        data.extraAction.handler();
      };
      choicesBox.appendChild(extraBtn);
    }

    const closeChoice = document.createElement('button');
    closeChoice.className = 'choice-btn';
    closeChoice.textContent = 'Tutup Percakapan';
    closeChoice.onclick = () => this.closeDialog();
    choicesBox.appendChild(closeChoice);

    document.getElementById('dialog-modal').classList.remove('hidden');
  },

  closeDialog() {
    document.getElementById('dialog-modal').classList.add('hidden');
  },

  openDashboard(state = Game.state) {
    this.renderDashboard(state);
    document.getElementById('dashboard-modal').classList.remove('hidden');
  },

  renderDashboard(state) {
    const liq = EconomySystem.evaluateLiquidity(state.budget);
    const activeCount = state.quests.filter(q => q.status === 'active').length;
    const completedCount = state.quests.filter(q => q.status === 'completed').length;

    document.getElementById('dash-budget').textContent = EconomySystem.formatRupiah(state.budget);
    document.getElementById('dash-liquidity-status').textContent = liq.status;
    document.getElementById('dash-reputation').textContent = `${state.reputation}%`;
    document.getElementById('dash-rep-status').textContent = state.reputation >= 75 ? 'Sangat Dipercaya' : state.reputation >= 50 ? 'Cukup Baik' : 'Perlu Pemulihan';
    document.getElementById('dash-impact').textContent = `${state.impact} Poin`;
    document.getElementById('dash-sustainability').textContent = `Indeks Kemandirian: ${state.sustainabilityScore}%`;
    document.getElementById('dash-programs').textContent = `${activeCount} Berjalan / ${completedCount} Selesai`;
    document.getElementById('dash-beneficiaries').textContent = `${state.beneficiaries} Jiwa Terbantu`;

    // Policy buttons state
    document.querySelectorAll('.policy-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.policy === state.policy);
    });

    // Quest list
    const listEl = document.getElementById('dash-quest-list');
    const visibleQuests = state.quests.filter(q => q.status !== 'hidden');

    listEl.innerHTML = visibleQuests.map(q => {
      const effCost = EconomySystem.calculateEffectiveCost(q.baseCost, state.policy);
      const effDays = EconomySystem.calculateEffectiveDuration(q.baseDays, state.policy);
      let actionHtml = '';

      if (q.status === 'discovered') {
        const canAfford = state.budget >= effCost;
        actionHtml = `<button class="btn-primary" data-approve="${q.id}" ${canAfford ? '' : 'disabled'}>
          ${canAfford ? 'Alokasikan Dana' : 'Dana Kurang'}
        </button>`;
      } else if (q.status === 'active') {
        actionHtml = `<span class="tag" style="background:#fef3c7;color:#92400e;">⏳ Berjalan (${q.daysLeft} hari)</span>`;
      } else if (q.status === 'completed') {
        actionHtml = `<span class="tag" style="background:#dcfce7;color:#166534;">✅ Selesai</span>`;
      }

      return `
        <div class="quest-card ${q.urgent && q.status === 'discovered' ? 'urgent' : ''} ${q.status === 'completed' ? 'completed' : ''}">
          <div class="quest-card-info">
            <h4>${q.urgent ? '🚨 [DARURAT] ' : ''}${q.title}</h4>
            <p>${q.description}</p>
            <div class="quest-meta">
              <span class="tag">${q.category}</span>
              <span class="tag">Biaya: ${EconomySystem.formatRupiah(effCost)}</span>
              <span class="tag">Waktu: ${effDays} Hari</span>
              <span class="tag">Dampak: +${q.impactReward}</span>
              <span class="tag">Kemandirian: +${q.sustainabilityGain}%</span>
            </div>
          </div>
          <div>${actionHtml}</div>
        </div>
      `;
    }).join('');

    listEl.querySelectorAll('[data-approve]').forEach(btn => {
      btn.addEventListener('click', () => {
        this.callbacks.onApproveQuest(btn.dataset.approve);
        this.renderDashboard(state);
      });
    });

    // Evaluation log
    const logEl = document.getElementById('evaluation-log');
    logEl.innerHTML = state.logs.slice().reverse().map(entry => `<div class="log-entry">${entry}</div>`).join('');
  },

  showSummary(state) {
    const completed = state.quests.filter(q => q.status === 'completed').length;
    const grade = state.impact >= 160 && state.reputation >= 75
      ? 'SANGAT AMANAH & BERDAMPAK TINGGI'
      : state.impact >= 90
      ? 'BAIK & BERKELANJUTAN'
      : 'CUKUP (PERLU OPTIMALISASI ANGGARAN)';

    document.getElementById('summary-title').textContent = `Predikat: ${grade}`;
    document.getElementById('summary-desc').textContent =
      `Selama 30 hari periode pengelolaan, lembaga Anda menyalurkan amanah sosial kepada ${state.beneficiaries} jiwa dengan total skor dampak ${state.impact} poin.`;

    document.getElementById('summary-stats').innerHTML = `
      <div class="stat-box"><span>Sisa Kas Lembaga</span><strong>${EconomySystem.formatRupiah(state.budget)}</strong></div>
      <div class="stat-box"><span>Reputasi Akhir</span><strong>${state.reputation}%</strong></div>
      <div class="stat-box"><span>Program Selesai</span><strong>${completed} Program</strong></div>
      <div class="stat-box"><span>Indeks Kemandirian</span><strong>${state.sustainabilityScore}%</strong></div>
    `;
    document.getElementById('summary-modal').classList.remove('hidden');
  }
};
"""

game_js = """// =========================================================
// GAME.JS — Core Engine, Game Loop, Controls & Persistence
// =========================================================

const STORAGE_KEY = 'social_impact_manager_save_v1';

const Game = {
  canvas: null,
  ctx: null,
  lastTime: 0,
  running: false,
  selectedGender: 'male',

  input: {
    up: false,
    down: false,
    left: false,
    right: false
  },

  camera: {
    x: 0,
    y: 0
  },

  state: null,
  nearbyTarget: null,

  createFreshState(gender = 'male') {
    return {
      day: 1,
      maxDays: 30,
      budget: 15000000,
      reputation: 70,
      impact: 0,
      beneficiaries: 0,
      sustainabilityScore: 0,
      policy: 'balanced',
      lastFundraiseDay: 0,
      gender,
      quests: QuestSystem.cloneInitialQuests(),
      logs: [
        'Hari 1: Amanah dimulai dengan dana awal Rp 15.000.000. Temui warga untuk mengidentifikasi prioritas kebutuhan.'
      ]
    };
  },

  init() {
    this.canvas = document.getElementById('game-canvas');
    this.ctx = this.canvas.getContext('2d');

    WorldMap.init();
    this.renderCharacterPreviews();
    this.bindStartScreen();
    this.bindControls();

    UI.init({
      onApproveQuest: (questId) => this.handleApproveQuest(questId),
      onNextDay: () => this.handleNextDay(),
      onChangePolicy: (pol) => this.handleChangePolicy(pol),
      onFundraise: () => this.handleFundraise(),
      onSave: () => this.saveProgress(true),
      onReset: () => this.resetGame()
    });

    window.addEventListener('resize', () => this.resizeCanvas());
    this.resizeCanvas();
  },

  renderCharacterPreviews() {
    const drawPrev = (canvasId, gender) => {
      const c = document.getElementById(canvasId);
      const cx = c.getContext('2d');
      cx.clearRect(0, 0, c.width, c.height);
      cx.save();
      cx.translate(c.width / 2, c.height / 2 + 12);
      drawHumanCharacter(cx, {
        gender,
        direction: 'down',
        isMoving: false,
        outfitPrimary: '#047857',
        outfitSecondary: '#f8fafc',
        accent: '#f59e0b',
        scale: 1.75
      });
      cx.restore();
    };
    drawPrev('preview-male', 'male');
    drawPrev('preview-female', 'female');
  },

  bindStartScreen() {
    const cards = document.querySelectorAll('.char-card');
    cards.forEach(card => {
      card.addEventListener('click', () => {
        cards.forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        this.selectedGender = card.dataset.gender;
      });
    });

    // Check saved progress
    const saved = localStorage.getItem(STORAGE_KEY);
    const btnContinue = document.getElementById('btn-continue');
    if (saved) {
      btnContinue.classList.remove('hidden');
    }

    document.getElementById('btn-start-new').addEventListener('click', () => {
      this.state = this.createFreshState(this.selectedGender);
      Player.reset(this.selectedGender);
      this.startGame();
      this.saveProgress(false);
    });

    btnContinue.addEventListener('click', () => {
      try {
        const parsed = JSON.parse(saved);
        this.state = parsed;
        Player.reset(parsed.gender || 'male');
        if (parsed.playerPos) {
          Player.x = parsed.playerPos.x;
          Player.y = parsed.playerPos.y;
        }
        this.startGame();
        UI.toast('Progres tersimpan berhasil dimuat.');
      } catch (e) {
        UI.toast('Gagal memuat progres, memulai sesi baru.', 'warn');
        this.state = this.createFreshState(this.selectedGender);
        Player.reset(this.selectedGender);
        this.startGame();
      }
    });
  },

  startGame() {
    document.getElementById('start-screen').classList.add('hidden');
    document.getElementById('summary-modal').classList.add('hidden');
    UI.updateHUD(this.state);
    this.running = true;
    this.lastTime = performance.now();
    requestAnimationFrame((t) => this.loop(t));
  },

  resizeCanvas() {
    const wrapper = document.getElementById('game-wrapper');
    this.canvas.width = wrapper.clientWidth;
    this.canvas.height = wrapper.clientHeight;
  },

  bindControls() {
    window.addEventListener('keydown', (e) => {
      if (!this.running) return;
      const key = e.key.toLowerCase();
      if (key === 'w' || e.key === 'ArrowUp') this.input.up = true;
      if (key === 's' || e.key === 'ArrowDown') this.input.down = true;
      if (key === 'a' || e.key === 'ArrowLeft') this.input.left = true;
      if (key === 'd' || e.key === 'ArrowRight') this.input.right = true;
      if (key === 'e' || e.key === ' ') {
        if (document.querySelector('.modal:not(.hidden)')) return;
        this.triggerInteract();
      }
    });

    window.addEventListener('keyup', (e) => {
      const key = e.key.toLowerCase();
      if (key === 'w' || e.key === 'ArrowUp') this.input.up = false;
      if (key === 's' || e.key === 'ArrowDown') this.input.down = false;
      if (key === 'a' || e.key === 'ArrowLeft') this.input.left = false;
      if (key === 'd' || e.key === 'ArrowRight') this.input.right = false;
    });

    // Touch D-Pad
    document.querySelectorAll('.dpad-btn').forEach(btn => {
      const dir = btn.dataset.dir;
      const setDir = (val) => { this.input[dir] = val; };
      btn.addEventListener('touchstart', (e) => { e.preventDefault(); setDir(true); });
      btn.addEventListener('touchend', (e) => { e.preventDefault(); setDir(false); });
      btn.addEventListener('mousedown', () => setDir(true));
      btn.addEventListener('mouseup', () => setDir(false));
      btn.addEventListener('mouseleave', () => setDir(false));
    });

    document.getElementById('btn-mobile-interact').addEventListener('click', () => {
      this.triggerInteract();
    });
  },

  findNearbyInteractable() {
    // 1. Check NPCs first
    for (const npc of NPCSystem.list) {
      const dist = Math.hypot(Player.x - npc.x, Player.y - npc.y);
      if (dist < 62) {
        return { type: 'npc', target: npc, label: `Bicara dengan ${npc.name}` };
      }
    }
    // 2. Check Building doors
    for (const b of WorldMap.buildings) {
      const dist = Math.hypot(Player.x - b.doorX, Player.y - (b.doorY + 12));
      if (dist < 56) {
        return { type: 'building', target: b, label: `Masuk / Cek ${b.name}` };
      }
    }
    return null;
  },

  triggerInteract() {
    if (!this.nearbyTarget) return;
    if (this.nearbyTarget.type === 'npc') {
      const data = NPCSystem.getDialogueData(this.nearbyTarget.target, this.state);
      UI.openDialog(data, this.state);
    } else if (this.nearbyTarget.type === 'building') {
      const b = this.nearbyTarget.target;
      if (b.actionType === 'dashboard') {
        UI.openDashboard(this.state);
        return;
      }
      const extraAction = b.actionType === 'fundraise'
        ? { label: 'Galang Dana ZISWAF di Baitul Mal', handler: () => this.handleFundraise() }
        : { label: 'Buka Dashboard Alokasi Program', handler: () => UI.openDashboard(this.state) };

      UI.openDialog({
        speaker: b.name,
        role: b.role,
        avatarText: '🏛️',
        text: b.description,
        extraAction
      }, this.state);
    }
  },

  handleApproveQuest(questId) {
    const res = QuestSystem.approveQuest(this.state, questId);
    UI.toast(res.message, res.ok ? 'normal' : 'danger');
    if (res.ok) {
      this.state.logs.push(`Hari ${this.state.day}: ${res.message}`);
      UI.updateHUD(this.state);
      this.saveProgress(false);
    }
  },

  handleNextDay() {
    if (this.state.day >= this.state.maxDays) {
      UI.showSummary(this.state);
      return;
    }

    this.state.day += 1;

    // 1. Advance active programs
    const questUpdates = QuestSystem.advanceActiveQuests(this.state);
    questUpdates.forEach(msg => {
      UI.toast(msg);
      this.state.logs.push(`Hari ${this.state.day}: ${msg}`);
    });

    // 2. Daily financial cycle
    const econLogs = EconomySystem.processDailyCycle(this.state);
    econLogs.forEach(l => this.state.logs.push(l));

    // 3. Check dynamic events / crisis unlocks
    const eventMsgs = QuestSystem.checkDynamicEvents(this.state);
    eventMsgs.forEach(msg => {
      UI.toast(msg, 'warn');
      this.state.logs.push(`Hari ${this.state.day}: ${msg}`);
    });

    UI.updateHUD(this.state);
    this.saveProgress(false);

    if (this.state.day >= this.state.maxDays) {
      UI.showSummary(this.state);
    } else if (questUpdates.length === 0 && eventMsgs.length === 0) {
      UI.toast(`Memasuki Hari ke-${this.state.day}.`);
    }
  },

  handleChangePolicy(policy) {
    this.state.policy = policy;
    const label = EconomySystem.getPolicyModifiers(policy).label;
    UI.toast(`Kebijakan penyaluran diubah ke: ${label}`);
    UI.renderDashboard(this.state);
    this.saveProgress(false);
  },

  handleFundraise() {
    const res = EconomySystem.fundraise(this.state);
    UI.toast(res.message, res.ok ? 'normal' : 'warn');
    if (res.ok) {
      this.state.logs.push(`Hari ${this.state.day}: ${res.message}`);
      UI.updateHUD(this.state);
      if (!document.getElementById('dashboard-modal').classList.contains('hidden')) {
        UI.renderDashboard(this.state);
      }
      this.saveProgress(false);
    }
  },

  saveProgress(notify = true) {
    const payload = {
      ...this.state,
      playerPos: { x: Player.x, y: Player.y }
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    if (notify) UI.toast('Progres berhasil disimpan ke LocalStorage.');
  },

  resetGame() {
    localStorage.removeItem(STORAGE_KEY);
    location.reload();
  },

  update(dt) {
    const modalOpen = document.querySelector('.modal:not(.hidden)') !== null;
    if (!modalOpen) {
      Player.update(dt, this.input);
    }

    // Smooth camera follow clamped to world bounds
    const targetCamX = Math.max(0, Math.min(WorldMap.width - this.canvas.width, Player.x - this.canvas.width / 2));
    const targetCamY = Math.max(0, Math.min(WorldMap.height - this.canvas.height, Player.y - this.canvas.height / 2));
    this.camera.x += (targetCamX - this.camera.x) * Math.min(1, dt * 10);
    this.camera.y += (targetCamY - this.camera.y) * Math.min(1, dt * 10);

    this.nearbyTarget = this.findNearbyInteractable();
    UI.setInteractPrompt(Boolean(this.nearbyTarget), this.nearbyTarget ? this.nearbyTarget.label : '');
  },

  render() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    WorldMap.draw(this.ctx, this.camera);
    NPCSystem.draw(this.ctx, this.camera, this.state);
    Player.draw(this.ctx, this.camera);
  },

  loop(now) {
    if (!this.running) return;
    const dt = Math.min(0.05, (now - this.lastTime) / 1000);
    this.lastTime = now;

    this.update(dt);
    this.render();
    requestAnimationFrame((t) => this.loop(t));
  }
};

window.addEventListener('DOMContentLoaded', () => {
  Game.init();
});
"""

readme_md = """# Social Impact Manager — Islamic Social Finance RPG

Game simulasi RPG 2D Top-Down berbasis web yang terinspirasi dari ekosistem **Islamic Social Finance** (ZISWAF & lembaga pengelola dana umat seperti BSI Maslahat). Pemain berperan sebagai Manajer Program Sosial yang menjelajahi desa, berdialog dengan warga, menganalisis krisis, mengelola likuiditas dana terbatas, dan mengevaluasi dampak program secara berkelanjutan.

## Fitur Utama
1. **Eksplorasi Dunia 2D Top-Down**: Lingkungan desa interaktif berisi Kantor Lembaga, Masjid Al-Maslahah, Madrasah/Sekolah, Klinik Pratama, Balai Masyarakat, Pemukiman Warga, Sumur Desa, dan Taman Publik.
2. **Pemilihan Karakter & Animasi Berjalan**: Tersedia pilihan karakter laki-laki (*Faris Al-Amin*) dan perempuan (*Aisyah Rahma*) dengan proporsi anatomi manusia realistis serta animasi arah atas, bawah, kiri, dan kanan.
3. **Kontrol Desktop & Mobile**: Mendukung `WASD` / `Arrow Keys` + `E` untuk desktop serta *Virtual D-Pad* + tombol aksi sentuh untuk smartphone.
4. **NPC & Misi Dinamis**: Berinteraksi dengan Bu Sari, Pak Hasan, Nadia, dan Pak Rahmat. Tantangan berkembang dinamis mulai dari krisis air bersih, renovasi sekolah, layanan klinik, modal bergulir *Qardhul Hasan*, hingga krisis darurat banjir bandang, kebakaran lahan, dan kebun wakaf produktif.
5. **Sistem Keuangan & Opportunity Cost**: Pengelolaan anggaran terbatas, pilihan kebijakan penyaluran (*Audit Ketat*, *Standar Transparan*, *Cepat Tanggap*), imbal hasil wakaf produktif harian, dan penghimpunan dana donatur berbasis reputasi.
6. **Penyimpanan Progres Otomatis**: Tersimpan secara lokal melalui `LocalStorage`.

## Struktur Proyek
```text
social-impact-manager/
├── index.html
├── README.md
├── assets/
│   ├── characters/
│   ├── environment/
│   ├── buildings/
│   └── ui/
├── css/
│   └── style.css
└── js/
    ├── economy.js
    ├── quest.js
    ├── world.js
    ├── player.js
    ├── npc.js
    ├── interface.js
    └── game.js