# Landing + Marketing Screens (LockN Score)

Source references: `web/src/pages/Demo.tsx`, `web/src/pages/Home.tsx`, `web/src/components/demo/*`, `web/src/design-system/tokens.ts`

## Global Frame Specs
- Desktop artboard: **1440×1024**
- Tablet artboard: **1024×1366**
- Mobile artboard: **390×844**
- Background: `#05070f`
- Main container max width: `1152px` (`max-w-6xl`), centered
- Horizontal padding: 16 (mobile), 24 (tablet), 40 (desktop)

---

## Screen L1 — Demo Landing (Interactive Marketing)

### Layout (Desktop 1440×1024)
1. **Hero badge** at (x: 620, y: 48), size 200×28
   - Copy: `INTERACTIVE DEMO`
2. **Hero title block** (x: 360, y: 92), size 720×140
   - Title: `Experience LockN Score`
   - Subtitle: `AI-powered real-time scoring for pickleball. Try the live dashboard below — tap buttons to simulate a game.`
3. **Live score demo card** (x: 160, y: 260), size 1120×220
   - Scoreboard module + controls row (+ Home, + Away, Rally Hit, New Game)
4. **Feature card grid** (x: 160, y: 500), size 1120×320
   - 3 columns × 2 rows, each card 360×150, 20px gap
5. **Upgrade banner** (x: 160, y: 840), size 1120×120
6. **Social proof row** (x: 280, y: 980), size 880×120
7. **Final CTA** (x: 470, y: 1120), size 500×100
   - Button: `Join the Beta — Free to Start`

### Component Usage
- Hero chip: rounded pill, neon border (`#4DD0E1` @ 20%)
- Feature cards: dark elevated cards (`#121620` / `#1A1F2E`), optional lock overlay
- Upgrade banner component
- Lead capture modal (`LeadCaptureModal`)

### States
- **Loading**: Skeleton for hero + cards
- **Empty**: If social proof stats unavailable → show placeholders (`--`)
- **Error**: Lead form submit error: `Couldn’t submit. Try again.`
- **Success**: Lead submit success: `You're on the beta list.` + auto-close modal

### Responsive
- Tablet: stack hero + score card full width; feature grid 2 columns
- Mobile: single-column cards; controls wrap 2 per row

### Interactions + Motion
- Hero fade-in (`y: -10 → 0`)
- Locked card click opens lead modal
- Upgrade CTA:
  - If no lead: opens modal
  - If lead captured: redirect checkout

### Copy (exact)
- `Interactive Demo`
- `Experience LockN Score`
- `Join the Beta — Free to Start`
- Locked features:
  - `Advanced Analytics`
  - `Multiplayer Sync`
  - `Game History`

---

## Screen L2 — Product Home (Post-login launcher)

### Layout (Desktop 1440×900)
1. Header shell card (x: 160, y: 32), size 1120×88
2. Hero split panel (x: 160, y: 144), size 1120×360
   - Left CTA card: 650×360
   - Right recent games card: 446×360
3. Quick stats strip (x: 160, y: 528), size 1120×132

### Component Usage
- New Game CTA button (height 56, min width 220)
- Recent game list items (3 rows)
- Stats cards (3-up)

### States
- **Loading**: shimmer list on recent games
- **Empty recent games**: copy `No games yet. Start your first session.`
- **Error**: toast `Could not load game history.`
- **Success**: after creating new game route transition to `/create`

### Responsive
- Desktop: 2-column hero
- Tablet: stacked hero panels
- Mobile: full single-column; quick stats become vertical cards

### Interactions
- Primary CTA `New Game` routes to `/create`
- `View all` opens `/history`

### Copy
- `Ready to run your next session?`
- `Start a new game session for practice, rally challenge, or full match play.`
- `Recent Games`
- `Games Played`, `Win Rate`, `Best Rally`

---

## Screen L3 — Lead Capture Modal

### Modal Frame
- Desktop modal: 520×620 centered
- Backdrop: black @ 60%
- Corner radius: 16

### Fields
- Name input
- Email input
- Optional: Team/Org
- CTA: `Join Waitlist`

### States
- Loading submit
- Validation errors (email format)
- Success confirmation panel

### Motion
- Scale in: 0.96 → 1.0, 220ms
- Backdrop fade: 160ms

---

## Figma Build Notes
- Use auto-layout for all card stacks and grids.
- Define reusable components: `HeroBadge`, `FeatureCard`, `StatsTile`, `LeadModal`.
- Use color tokens from `tokens.ts` directly for swatches.
