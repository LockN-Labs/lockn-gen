# Dashboard + Settings Screens

Source references: `web/src/App.tsx`, `web/src/pages/Home.tsx`, `web/src/pages/Setup.tsx`, `web/src/pages/Stats.tsx`, `web/src/pages/History.tsx`, `web/src/pages/SpectatorDashboard.tsx`, component files under `web/src/components/*`.

## Screen D1 — Main App Shell (non-spectator routes)

### Desktop frame (1440×1024)
1. Top suite nav card (x:160, y:24, w:1120, h:72)
   - Left: `LockN Suite`
   - Right links: Launcher / Speak / Score / Gen
2. Header block (x:160, y:116, w:1120, h:92)
   - Title: `Live Dashboard`
   - Subtitle: `Real-time scoring, rally analytics, and voice command monitoring.`
   - Auth button right
3. Main content region (x:160, y:232, w:1120, h:680)
4. Bottom floating nav (centered near bottom), w: min(580, 92vw), h:72
   - Tabs: Game / Setup / History / Stats / Demo / Register

### States
- Active tab highlighted (`bg-neon text-slate-900`)
- Admin mode adds `Admin` shield tab
- Auth loading state in header button

### Responsive
- Tablet: top nav wraps
- Mobile: bottom nav scrollable horizontally if tabs overflow

---

## Screen D2 — Setup / Calibration

### Frame (desktop content area 1120×680)
Sections stacked:
1. Intro text block at y:0 (h:96)
2. Camera section card (h:240)
3. Calibration card (h:220)
4. Verify card (h:180)

### Exact internals
- Camera preview box: full width, height 224
- Primary button: `Enable Camera Preview`
- Error copy on permission deny: `Camera permission denied. Allow camera access and retry.`

### Calibration controls
- Four action buttons grid 2×2:
  - `Mark baseline A`
  - `Mark baseline B`
  - `Mark sideline A`
  - `Mark sideline B`

### Verify actions
- `Start Test Rally`
- `Save Calibration`

### States
- Loading camera
- Camera unavailable API
- Permission denied
- Success preview playing

### Interaction
- `getUserMedia({video:true,audio:false})`

---

## Screen D3 — Spectator Dashboard (Live)

> This complements Journey 3 with implementation-accurate shell details.

### Frame
- Fullscreen 1600×900 target
- Container max width 1600 with 24px padding

### Order (top to bottom)
1. Header card (session ID, `Game X of 3`)
2. ScoreDisplay block (hero)
3. Two-column block:
   - Left: RallyTracker
   - Right: PIPFeeds
4. Game Progress card (3 game chips)
5. Match History chip row (sticky bottom region)

### Key copy
- `LockN Score • Spectator View`
- `Waiting for active session`
- `Game Progress`
- `Best of 3`
- `Waiting for events…`

### Live states
- No session: waiting subtitle
- WS connected + no events
- Event burst: chips prepend, capped at 12
- Game completed: progress tile goes green
- Video frame available: feed card updates

### Error/loading
- Poll fallback every 2200ms
- WS unavailable → continue with polling
- Missing feeds → show placeholders `Camera 1`, `Camera 2`

---

## Screen D4 — Stats Dashboard

### Frame
- Content card 1120×560

### Content
- H1: `Stats`
- Loading: `Loading stats…`
- Empty/error: `No stats available.`
- Populated:
  - `Longest Rally: {value}`
  - `Most Points in a Game: {value}`
  - Leaderboard list

### Leaderboard empty
- `No players yet.`

### Interaction
- GET `/api/stats/overview`

---

## Screen D5 — History Dashboard (spec target)

### Layout
- Header + filter row + list/table
- 3 core filters: date range, mode, player
- Rows include: date, players, mode, final score, duration, actions

### States
- Loading skeleton rows
- Empty: `No games found for this filter.`
- Error: `Couldn’t load history.`
- Success: clickable rows route to detail

### Copy actions
- `View Details`
- `Export`

---

## Settings Panel (global)

### Overlay
- Modal 520×640 centered desktop; full-screen sheet mobile
- Sections:
  1. Account
  2. Camera defaults
  3. Audio defaults
  4. Notifications
  5. Privacy + logout

### Control specs
- Toggle row height: 56
- Select row height: 64
- Save button: full width 56

### States
- Unsaved changes warning on close
- Save loading: `Saving...`
- Save success toast: `Settings saved.`
- Save error: `Failed to save settings.`

---

## Breakpoints
- Mobile <=767: single column, bottom sheet settings
- Tablet 768-1023: reduced margins, cards stack sooner
- Desktop >=1024: split layouts for dashboard-heavy pages

## Figma Build Checklist
- Components:
  - AppShellTopNav
  - BottomTabNav
  - SectionCard
  - StatusChip
  - SettingsModal
- Build variants for states: loading/empty/error/success
- Use token colors from `design-system/tokens.ts`
