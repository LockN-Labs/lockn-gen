# LockN Score QA Report: Dashboard Modes & Views

**Project:** LockN Score web app  
**Codebase reviewed:** `/home/sean/repos/lockn-score/web/src`  
**Date:** 2026-02-11  
**Prepared for:** UX team (pre-Figma current-state review)

---

## Scope & Method

I reviewed:
- Top-level route definitions (`App.tsx`)
- All page components under `web/src/pages/**`
- Supporting mode/view components used inside pages (session flow + spectator variants)
- Additional mode components present in codebase but not currently wired to routes

This report lists **every distinct screen/mode currently implemented in code** and flags maturity as:
- **Complete** = fully realized UI flow with meaningful logic/data wiring
- **Partial** = usable UI but with mock/static data, missing integrations, or obvious in-progress behavior
- **Placeholder** = mostly scaffold/basic shell, minimal UX depth

---

## Route Map (Current)

## Main app routes
- `/` → Home
- `/setup` → Setup (camera calibration)
- `/create` → SessionCreate (3-step wizard)
- `/history` → History
- `/stats` → Stats
- `/demo` → Demo experience
- `/spectator` → SpectatorDashboard
- `/spectator/:sessionId` → SpectatorDashboard (session-scoped)
- `/register` → PlayerRegistration (protected)
- `/join` → JoinSession
- `/camera-setup` → CameraSetup
- `/pregame` → PreGame (protected)
- `/history/player/:id` → PlayerHistory (protected)
- `/admin/invites` → Admin Invites (protected)

## Special routing behavior
- Any `/spectator*` path bypasses the standard app chrome/nav and renders spectator layout directly.

---

## Detailed Mode/View Inventory

## 1) Launcher / Live Dashboard Home
- **Mode name:** Home / Launcher Dashboard
- **Route:** `/`
- **Key UI components visible:**
  - Header with LockN Score branding + settings/profile icon buttons
  - Primary CTA card (“New Game”) linking to `/create`
  - Recent Games list (static sample cards)
  - Quick stats tiles (static sample values)
- **Layout description:**
  - Two-column hero area on desktop: large CTA panel + right-side recent games panel
  - Stats strip below in 3 tiles
  - Uses rounded card-heavy dashboard style
- **Implementation state:** **Partial**
  - Structurally polished, but recent games/stats are hardcoded sample data (not live-fed).

---

## 2) Camera Calibration & Alignment
- **Mode name:** Setup / Camera Calibration
- **Route:** `/setup`
- **Key UI components visible:**
  - Step 1 Position Camera panel with live preview container + enable/recheck button
  - Step 2 Calibration panel with four marker buttons
  - Step 3 Verify panel with test/save actions
- **Layout description:**
  - Vertical 3-section wizard-like layout within one page
  - Prominent instructional text and action buttons per step
- **Implementation state:** **Partial**
  - Camera preview permission flow is functional.
  - Calibration/verify controls are mostly UI scaffolding (no evident backend/canvas calibration persistence wiring in this page).

---

## 3) Session Creation Wizard (Container Mode)
- **Mode name:** Session Create Wizard
- **Route:** `/create`
- **Key UI components visible:**
  - 3-step progress indicator: Mode → Settings → Lobby
  - Animated step transitions
  - Back/Continue/Start controls
- **Layout description:**
  - Single card container with internal step-based subviews
  - Large central content area for each step
- **Implementation state:** **Partial to near-complete**
  - End-to-end start-session API call exists (`/api/session/{solo|rally|game}`), then navigates to spectator session.
  - Player lobby population is currently static/empty in this page (`lobbyPlayers = []`).

### 3a) Submode: Mode Selection
- **Route context:** `/create` (step 1)
- **Key components:** `ModeCard` options for:
  - Solo Practice
  - Rally Challenge
  - Full Game
- **Layout:** 3-card selection grid
- **State:** **Complete (UI + mode state selection)**

### 3b) Submode: Game Settings
- **Route context:** `/create` (step 2)
- **Key components:** `GameSettings`
  - Full mode: points-to-win, serve interval, best-of sets
  - Solo/rally modes: target rally count
- **Layout:** settings panel with segmented controls / numeric input
- **State:** **Partial**
  - Connected to request payload generation.
  - Options are currently constrained/minimal (e.g., serve interval only “5”, best-of only “1”).

### 3c) Submode: Waiting Lobby
- **Route context:** `/create` (step 3)
- **Key components:** `WaitingLobby`
  - Session code display
  - Player QR code
  - Camera QR code
  - “Players joining” list area
- **Layout:** two-column (code/QR left, player list right)
- **State:** **Partial**
  - QR generation and join URL logic are implemented.
  - Joined players list is currently empty/static from parent page (no live join feed wired here).

---

## 4) Session Join (Role Split Entry)
- **Mode name:** Join Session
- **Route:** `/join`
- **Key UI components visible:**
  - Session code input
  - Role selector (Player vs Camera) when role not pre-provided
  - Join button with role-based label
- **Layout description:**
  - Centered mobile-first cardless layout
  - Optional QR-derived session badge
- **Implementation state:** **Complete**
  - Supports URL params (`session`, `role`), auto-route behavior, and role-based navigation:
    - Player → `/pregame?session=...`
    - Camera → `/camera-setup?session=...`

---

## 5) Camera Device Streaming Mode
- **Mode name:** Camera Setup / Live Stream Uplink
- **Route:** `/camera-setup?session=...`
- **Key UI components visible:**
  - Live device preview video
  - Flip-camera control
  - Start Streaming CTA → live status state
  - Error panel and leave action
- **Layout description:**
  - Mobile-oriented single-column stream control screen
  - Large preview + explicit start button
- **Implementation state:** **Partial to near-complete**
  - Camera + mic acquisition and WebSocket streaming are implemented.
  - Uses lower-level browser/audio processing and session WS path.
  - UX is functional but still utilitarian and likely not polished for production edge cases.

---

## 6) Pre-Game Player Readiness
- **Mode name:** Pre-Game Setup
- **Route:** `/pregame?session=...` (protected)
- **Key UI components visible:**
  - Stream preview (`StreamPreview`)
  - Permission status checklist (camera/mic)
  - Connection state card
  - Error alert state
  - Ready button (`ReadyButton`) and leave action
- **Layout description:**
  - Mobile-first centered stack of status cards
  - Readiness gating before entering spectator/game view
- **Implementation state:** **Partial**
  - Strong UX structure and state handling.
  - Session connection currently simulated with timed transitions (not true server session handshake in this page).
  - Ready navigates to spectator session route.

---

## 7) Spectator Dashboard (Container Mode)
- **Mode name:** Spectator Dashboard
- **Routes:** `/spectator`, `/spectator/:sessionId`
- **Key UI components visible (overall):**
  - Spectator header with mode badge
  - Dynamic branch to rally-focused dashboard OR full-game dashboard
  - WebSocket + polling updates
- **Layout description:**
  - Full-screen dark “broadcast” style view
  - Distinct layout depending on resolved session mode
- **Implementation state:** **Complete (core spectator architecture), with partial data assumptions**
  - Real-time handling appears substantial (WS + poll fallback + event handling + toasts + feed updates).
  - Some mode inference fallback (active player count) suggests resilience but also indicates backend mode certainty is not always guaranteed.

### 7a) Submode: Solo Spectator Hero
- **Route context:** `/spectator*` when mode resolves to `solo`
- **Key components:** `RallyHeroDashboard` (solo variant)
  - Giant current rally number
  - Longest rally, sparkline/history, bar mini-chart
  - Single player identity card
  - Single large camera feed card
  - Session stats (avg rally, total hits, duration)
- **Layout:** split-pane hero analytics layout
- **State:** **Complete**

### 7b) Submode: Rally Spectator Hero (2-player)
- **Route context:** `/spectator*` when mode resolves to `rally`
- **Key components:** `RallyHeroDashboard` (rally variant)
  - Same analytics hero block
  - Two player identity cards
  - Two camera feed cards
  - Co-op rally stats panel
- **Layout:** same shell, multi-player variant content
- **State:** **Complete**

### 7c) Submode: Full Game Spectator Scoreboard
- **Route context:** `/spectator*` when mode resolves to `game`
- **Key components:**
  - `ScoreDisplay` (two players + server + manual score override)
  - Point toast notifications
  - `RallyTracker` + `PIPFeeds`
  - Game progress strip (best-of-3 style)
  - Match event chips/history
- **Layout:** top scoreboard + lower analytics/feed split + progress/history sections
- **State:** **Complete (feature-rich)**
  - Includes manual override action dispatch via WebSocket.

---

## 8) Player Registration / Profile Capture
- **Mode name:** Player Registration
- **Route:** `/register` (protected)
- **Key UI components visible:**
  - Auth gate state (login required)
  - Name input + profile creation
  - Existing profile display
  - Camera capture (`CameraCapture`) for selfie
  - Retake/upload flow
- **Layout description:**
  - Card-based onboarding flow with conditional sections
- **Implementation state:** **Complete**
  - Registration and photo upload API calls are implemented.
  - Good UX branching for first-time vs returning player.

---

## 9) History Overview
- **Mode name:** History Dashboard
- **Route:** `/history`
- **Key UI components visible:**
  - Recent games list
  - Link to full player history route
  - Empty state
- **Layout description:**
  - Single list card under page header
- **Implementation state:** **Partial**
  - Fetches `/api/games`, but currently simplistic and uses default player id fallback in-page.
  - UX scope limited to basic list.

---

## 10) Player Detail History
- **Mode name:** Player History Detail
- **Route:** `/history/player/:id` (protected)
- **Key UI components visible:**
  - Loading/error/no-data states
  - Performance stat tiles
  - Detailed game history cards (win/loss, scores, rally/duration metadata)
- **Layout description:**
  - Header + summary metrics section + detailed chronological game list
- **Implementation state:** **Complete**
  - Pulls player stats and games from APIs and handles full state lifecycle.

---

## 11) Stats Overview
- **Mode name:** Stats
- **Route:** `/stats`
- **Key UI components visible:**
  - Heading
  - Basic overview values (longest rally, most points)
  - Leaderboard ordered list
- **Layout description:**
  - Minimal unthemed/basic page structure compared to rest of app
- **Implementation state:** **Placeholder to Partial**
  - Fetches real endpoint (`/api/stats/overview`) but UI is very basic and visually inconsistent with main dashboard system.

---

## 12) Interactive Demo Experience
- **Mode name:** Demo / Marketing Sandbox
- **Route:** `/demo`
- **Key UI components visible:**
  - Simulated live scoreboard (`ScoreBoard`)
  - Rally counter (`RallyCounter`)
  - Manual simulation buttons
  - Feature cards (`DemoFeatureCard`) with locked feature gating
  - High-score board sample
  - Upgrade banners + CTA funnel
  - Lead capture modal (`LeadCaptureModal`)
- **Layout description:**
  - Multi-section marketing/demo page with strong conversion CTAs
- **Implementation state:** **Complete (for demo intent)**
  - Uses simulated data intentionally; appears purpose-built for product demo/lead-gen.

---

## 13) Admin Invite Management
- **Mode name:** Admin Invites
- **Route:** `/admin/invites` (protected)
- **Key UI components visible:**
  - Header + create invite action
  - Filter bar (search + status)
  - Invites table (desktop) and card list (mobile)
  - Pagination
  - Create Invite modal (form + created state + copy link)
  - Revoke action
- **Layout description:**
  - Full CRUD-style admin management surface
- **Implementation state:** **Complete**
  - Robust list/filter/paginate/create/revoke interactions.
  - “Resend” action is intentionally present as disabled/coming-soon.

---

## Additional Modes Present in Code (Not Currently Routed)

These are implemented components but not directly reachable via current route config:

## A) Legacy/Standalone Mode Selector
- **Component:** `components/ModeSelector.tsx`
- **Mode values:** solo, rally, game
- **State:** **Partial/Unused in current route flow**
- **Notes:** Appears to be an earlier reusable selector; session wizard now uses `ModeCard` instead.

## B) Legacy Solo Mode Panel
- **Component:** `components/SoloMode.tsx`
- **UI:** streak/high-score/status/audio-detection panel
- **State:** **Partial/Unused in current routing**
- **Notes:** No direct page route currently renders it.

## C) Legacy Two-Player Mode Panel
- **Component:** `components/TwoPlayerMode.tsx`
- **Submodes inside component:** rally-mode panel and game-mode panel
- **State:** **Partial/Unused in current routing**
- **Notes:** Superseded by spectator-specific components (`RallyHeroDashboard`, spectator `ScoreDisplay`, etc.).

---

## UX-Relevant Gaps / Current-State Observations

1. **Session Create lobby is visually ready but data-thin**
   - Lobby player list does not currently ingest real joined participants in this page.

2. **Setup/calibration page has strong structure, weak backend linkage**
   - Calibration actions look presentational right now.

3. **Stats page styling maturity lags behind rest of app**
   - Functional endpoint call exists, but page does not match primary dashboard visual language.

4. **PreGame connection is partially simulated**
   - Good UX flow, but connection readiness appears timer-driven in-page.

5. **Spectator mode is the most mature dashboard surface**
   - Multiple view states, robust event handling, and broadcast-oriented layout are in place.

---

## Summary: Distinct Screens/Modes Count

### Route-backed screens/views
1. Home
2. Setup
3. Session Create (container)
4. Session Create – Mode step
5. Session Create – Settings step
6. Session Create – Lobby step
7. Join Session
8. Camera Setup
9. Pre-Game
10. Spectator (container)
11. Spectator Solo variant
12. Spectator Rally variant
13. Spectator Full Game variant
14. Player Registration
15. History overview
16. Player History detail
17. Stats
18. Demo
19. Admin Invites

### Additional non-routed mode components
20. Legacy ModeSelector
21. Legacy SoloMode panel
22. Legacy TwoPlayerMode panel (rally/game internal variants)

**Total distinct mode/view surfaces identified in codebase:** **22**

---

If useful for the Figma phase, I can produce a follow-up matrix with:
- Recommended canonical UX names,
- Priority (P0/P1/P2),
- Candidate consolidation opportunities (e.g., legacy mode panels vs spectator patterns).