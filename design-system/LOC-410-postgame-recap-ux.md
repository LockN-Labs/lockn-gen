# LOC-410: Post-Game Recap UX — Highlights + Stats Overlay

## Research Summary

### Competitive Analysis

**NBA App** — Uses AI-driven narrative highlights, vertical-scroll video feed, multiple recap lengths ("All Possessions," "10-Minute Condensed," "Key Highlights"). Post-game box score is stat-dense but clean. Key insight: *layered depth* — casual fans see headlines, stat nerds can drill down.

**FIFA+ / FIFA World Cup App** — AR-enhanced real-time stats, heatmaps, possession breakdowns. Post-match reports include scoreline progression timeline, per-player performance data with linked video clips. Key insight: *video-linked stats* — every stat can be traced back to a moment.

**Strava** — Post-activity summary shows 3 "most notable" stats auto-selected, map, splits, and shareable activity cards. Social feed integration drives engagement. Key insight: *shareability as first-class feature* — the shareable card IS the summary.

**Apple Fitness+** — Workout summary: total time, active calories, avg heart rate, total calories. Clean single-screen summary with rings/progress visualization. Key insight: *instant gratification* — summary appears immediately, feels like a reward.

### What Makes Post-Game Feel Rewarding

1. **Immediate dopamine** — Celebration animation within 500ms of game end
2. **Personal records / milestones** — "Your longest rally ever!" badges
3. **Narrative framing** — Not just numbers, but story ("You came back from 8-10 to win 11-8")
4. **Social proof** — Easy sharing that looks good on Instagram/iMessage
5. **Progression** — Stats in context of history (win streak, improvement trends)

### Stats That Matter

| Audience | Primary Stats | Secondary Stats |
|----------|--------------|-----------------|
| **Casual** | Final score, winner, game duration, "best moment" highlight | Total rallies, who served more |
| **Competitive** | Serve %, points won on serve vs return, scoring runs, momentum shifts | Rally length distribution, clutch point conversion, deuce stats |

---

## Screen Architecture

The post-game experience is a **single scrollable screen** with distinct sections, not separate pages. This follows Strava's model — everything on one canvas, scroll to explore.

### Layout (Top → Bottom)

```
┌─────────────────────────────────────┐
│         WINNER CELEBRATION          │  Section 0 — Auto-plays, then collapses
│      (full-screen overlay, 2.5s)    │
├─────────────────────────────────────┤
│           SCORE CARD                │  Section 1 — Hero area
│     Player A  11 — 8  Player B     │
│      Duration • Rallies • Date     │
├─────────────────────────────────────┤
│         MATCH NARRATIVE             │  Section 2 — One-liner story
│  "Comeback win — rallied from 4-9" │
├─────────────────────────────────────┤
│         PLAYER STATS                │  Section 3 — Side-by-side comparison
│    [Player A]    vs    [Player B]   │
│   Serve % · Longest Rally · etc    │
├─────────────────────────────────────┤
│       MOMENTUM TIMELINE             │  Section 4 — Visual chart
│    ───────/\──────\/────/\───►      │
├─────────────────────────────────────┤
│        HIGHLIGHTS REEL              │  Section 5 — Horizontal scroll cards
│   [Clip 1] [Clip 2] [Clip 3]       │
├─────────────────────────────────────┤
│          ACTIONS                    │  Section 6 — Sticky bottom or inline
│  [Share] [Rematch] [New Game] [End] │
└─────────────────────────────────────┘
```

---

## Section Specs

### Section 0: Winner Celebration Overlay

**Trigger:** Fires immediately when match point is confirmed (within 1 frame of the final score update).

**Animation sequence (2.5s total):**
1. **0–400ms:** Live dashboard fades to 40% opacity. Dark scrim slides up.
2. **400–1000ms:** Winner's avatar scales up from center (spring animation, `dampingRatio: 0.7`, `stiffness: 300`). Confetti particle emitter fires from top corners — gold + team color particles, 60–80 particles, gravity-affected, 1.5s lifespan.
3. **1000–1800ms:** Winner name fades in below avatar (`Typography: Display Medium, 36pt`). Score fades in below name (`Headline Large, 28pt`). Subtle haptic: `UIImpactFeedbackGenerator(.heavy)` at 400ms, then `.medium` at 1000ms.
4. **1800–2500ms:** Hold. User can tap anywhere to dismiss early.
5. **2500ms+:** Overlay crossfades to recap screen (300ms ease-out).

**Design:**
- Background: Radial gradient from `surface` (#1C1B1F) center to `scrim` (#000000) edges
- Avatar: 120pt circle, 3pt `primary` (#D0BCFF) border, subtle drop shadow
- Confetti colors: `primary`, `tertiary` (#EFB8C8), `primaryContainer` (#4F378B)
- If no avatar set: Large trophy icon (SF Symbol `trophy.fill`) with same animation

**iPad adaptation:** Avatar scales to 160pt, name to Display Large 45pt. Confetti particle count doubles.

### Section 1: Score Card (Hero)

**Layout:** Centered, padded 24pt horizontal, 32pt top (after celebration dismisses).

```
┌──────────────────────────────────────┐
│                                      │
│   [Avatar]          [Avatar]         │
│   Player A          Player B         │
│                                      │
│        11    —    8                   │
│                                      │
│   12:34  •  47 rallies  •  Feb 10    │
│                                      │
└──────────────────────────────────────┘
```

**Typography:**
- Player names: `Title Large` (22pt), `onSurface` color, winner name gets `primary` color
- Score: `Display Large` (57pt), winner's score in `primary`, loser's in `onSurfaceVariant`
- Metadata row: `Body Medium` (14pt), `onSurfaceVariant`, separated by `·` with 8pt spacing
- The `—` between scores: `Display Large`, `outline` color

**Component:** MD3 `Card` variant `filled`, `surfaceContainerLow` background, corner radius 28pt.

**Avatars:** 56pt circles, side by side with 80pt gap (score numbers between them). Winner has a subtle gold ring (2pt, `tertiary`).

**iPad:** Score bumps to 72pt. Card gets max-width 600pt, centered.

### Section 2: Match Narrative

**Auto-generated one-liner** based on game data. Examples:
- "Dominant win — led from start to finish"
- "Comeback! Rallied from 4–9 to take it 11–9"
- "Nail-biter — 5 deuces before the finish"
- "Shutout — flawless 11–0 performance"

**Typography:** `Title Medium` (16pt), `onSurfaceVariant`, centered, italic. Padded 16pt vertical.

**Logic for narrative selection (priority order):**
1. Shutout (11-0) → "Flawless"
2. Comeback (trailed by 5+ and won) → "Comeback"
3. Extended deuce (3+ deuces) → "Nail-biter"
4. Dominant (never trailed) → "Dominant"
5. Default → "Great match" + final score context

### Section 3: Player Stats Comparison

**Layout:** Side-by-side stat bars, player columns flanking a center axis.

```
         Player A          Player B
Serve %    72% ████████░░ ░░░░████ 40%
Longest     8  ██████░░░░ ░░░████░  6
Rally
Pts on      7  ███████░░░ ░░░░░███  5
Serve
Pts on      4  ████░░░░░░ ░░░░████  3  (only show if data available - added as optional)
Return
```

**Visual treatment:**
- Horizontal bar chart, mirrored from center
- Player A bars extend left, Player B bars extend right
- Winner's bars: `primary` (#D0BCFF)
- Loser's bars: `surfaceContainerHighest` (#E6E0E9) at 60% opacity
- Stat labels: `Label Large` (14pt), centered between bars
- Stat values: `Title Medium` (16pt), at the outer edges of bars
- Bar height: 24pt, corner radius 12pt, 8pt vertical gap between bars

**Stats shown (in order):**
1. **Points Scored** — total points each player won
2. **Serve %** — percentage of service games/points won
3. **Longest Rally** — longest rally in hits for each player
4. **Scoring Run** — longest consecutive points streak

**Container:** MD3 `Card` variant `outlined`, 16pt internal padding, 28pt corner radius.

### Section 4: Momentum Timeline

**Visualization:** Line chart showing score differential over time (by point number).

```
  +5 ┤         ╱╲
     │        ╱  ╲
   0 ┤───╱╲──╱────╲──╱──
     │  ╱  ╲╱      ╲╱
  -5 ┤╱
     └────────────────────►
     1    5    10   15   20  (point #)
```

**Design:**
- X-axis: Point number (1 to total points played)
- Y-axis: Score differential (positive = Player A leading, negative = Player B leading)
- Line: 2pt stroke, gradient from Player A's color to Player B's color based on who's leading
- Fill: Subtle gradient fill below/above zero line, 10% opacity
- Zero line: 1pt dashed, `outline` color
- Key moments (longest rally, match point) marked with dots (8pt circles, `tertiary`)
- Tappable dots → tooltip showing "Point 15: Longest rally (12 hits)"

**Typography:**
- Section header: `Title Medium` (16pt), "Momentum", `onSurface`
- Axis labels: `Label Small` (11pt), `onSurfaceVariant`
- Tooltip: `Body Small` (12pt) in an MD3 `PlainTooltip`

**Container:** Full-width, 200pt height (280pt on iPad), 16pt horizontal padding.

**Chart library recommendation:** Swift Charts (iOS 16+). Fallback: custom `Path` drawing in SwiftUI Canvas.

### Section 5: Highlights Reel

**Layout:** Horizontal scroll (`LazyHStack`), snap-to-item behavior.

Each highlight card:
```
┌──────────────────────┐
│  ┌──────────────────┐│
│  │                  ││
│  │   Video thumb    ││
│  │     ▶ 0:12      ││
│  │                  ││
│  └──────────────────┘│
│  🔥 Longest Rally    │
│  12 hits at 8-7      │
│  Point 15 • 0:34     │
└──────────────────────┘
```

**Card specs:**
- Width: 240pt (iPhone), 300pt (iPad)
- Thumbnail: 16:9 aspect ratio, corner radius 16pt (top corners)
- Play button: Centered, 48pt circle, `surfaceContainerHighest` at 80% opacity, SF Symbol `play.fill` 20pt
- Duration badge: Bottom-right of thumbnail, `Body Small` (12pt), `inverseSurface` pill with 6pt horizontal padding
- Title: `Title Small` (14pt), with emoji prefix for type (🔥 longest rally, 🎯 clutch point, 🏆 match point, ⚡ scoring run)
- Description: `Body Small` (12pt), `onSurfaceVariant`
- Timestamp: `Label Small` (11pt), `onSurfaceVariant`
- Card: MD3 `ElevatedCard`, `surfaceContainerLow`, corner radius 16pt

**Auto-detected highlight types (priority order):**
1. 🏆 **Match point** — always included
2. 🔥 **Longest rally** — if ≥ 6 hits
3. 🎯 **Clutch points** — points scored when trailing by 1 in deuce or at 9-10/10-9
4. ⚡ **Scoring runs** — 3+ consecutive points
5. 💪 **Comeback moments** — point where trailing player ties the score after being down 3+

**Playback:** Tapping a card opens a sheet (`.sheet` modifier) with video player. Simple controls: play/pause, scrub, close. No full-screen needed for these short clips (typically 5–15 seconds).

**Empty state:** If no highlights detected (rare), show a single card: "No standout moments this game — every point was solid! 💪"

### Section 6: Actions

**Layout:** Two rows of buttons at bottom of scroll, plus a persistent bottom bar for primary action.

**Persistent bottom bar** (fixed, not scrolling):
```
┌─────────────────────────────────────┐
│  [Rematch]          [Share ↗]       │
└─────────────────────────────────────┘
```

- Height: 72pt + safe area inset
- Background: `surfaceContainer` with top border 0.5pt `outlineVariant`
- "Share": MD3 `FilledButton`, `primary` container, `onPrimary` text
- "Rematch": MD3 `OutlinedButton`, `primary` border + text

**Inline actions** (above bottom bar, end of scroll content):
```
  [New Game]     [End Session]     [Game History]
```

- MD3 `TextButton` style, `primary` color, `Title Small` (14pt)
- Horizontal row, evenly spaced, 48pt touch target height
- 32pt bottom padding to clear persistent bar

**Share action** triggers the **Shareable Card** generation (see below).

**"Rematch"** → Navigates directly to game setup with same players pre-filled.
**"New Game"** → Fresh game setup screen.
**"End Session"** → Confirmation dialog, then returns to home.
**"Game History"** → Navigates to match history list.

---

## Shareable Card

Generated as a 1080×1920 image (Instagram Story ratio) or 1080×1080 (square, for feed posts).

### Story Format (1080×1920):

```
┌──────────────────────────┐
│                          │
│      🏓 LockN Score      │  Top — branding
│                          │
│   ┌──────────────────┐   │
│   │  Winner Avatar   │   │
│   │     "WINNER"     │   │
│   │   Player Name    │   │
│   └──────────────────┘   │
│                          │
│      11  —  8            │  Score, large
│                          │
│   Player A vs Player B   │
│   Feb 10, 2026           │
│                          │
│   ┌──────────────────┐   │
│   │ 47 rallies       │   │
│   │ 12:34 duration   │   │
│   │ 12-hit longest   │   │
│   │ rally             │   │
│   └──────────────────┘   │
│                          │
│   ┌──────────────────┐   │
│   │ Mini momentum    │   │
│   │ chart            │   │
│   └──────────────────┘   │
│                          │
│   locknscore.app         │  Bottom — CTA
│                          │
└──────────────────────────┘
```

**Design:**
- Background: Dark gradient, `surface` → `surfaceContainerLowest`
- Branding: App icon (24pt) + "LockN Score" wordmark, `onSurfaceVariant`, top center
- Score: Same treatment as in-app but scaled for image
- Stats block: 3–4 key stats in a rounded rect, `surfaceContainer` background
- Momentum chart: Simplified (no labels/tooltips), just the line + gradient fill
- CTA: App URL or QR code, bottom center, `onSurfaceVariant`
- Overall feel: Premium, dark, minimal — looks good when screenshotted or shared

**Generation:** Use `UIGraphicsImageRenderer` to render a SwiftUI view to image. Share via `UIActivityViewController` / `ShareLink`.

---

## Transitions & Animations

### Live Dashboard → Recap

1. **Game end detected** → Score display pulses once (scale 1.0 → 1.05 → 1.0, 200ms)
2. **500ms delay** → Celebration overlay begins (Section 0)
3. **After celebration** → Dashboard content crossfades to recap content:
   - Existing score card morphs (shared element transition / `matchedGeometryEffect` on score numbers and player names)
   - New sections fade in sequentially, 100ms stagger between each
   - Scroll position resets to top

### Section Entry Animations (on first scroll into view)

- **Score Card:** Already visible from transition. Score numbers count up from 0 to final (500ms, ease-out).
- **Narrative:** Fade in + slide up 16pt (300ms, ease-out)
- **Player Stats:** Bars animate from 0 width to final width (400ms per bar, 50ms stagger, ease-out-cubic)
- **Momentum Timeline:** Line draws from left to right (800ms, ease-in-out), fill fades in after (200ms)
- **Highlights:** Cards slide in from right (300ms, spring)
- **Actions:** Fade in (200ms)

All animations use `withAnimation(.spring(response: 0.5, dampingFraction: 0.8))` unless specified.

### Haptics

| Event | Haptic |
|-------|--------|
| Game end confirmed | `.notification(.success)` |
| Celebration confetti | `.impact(.heavy)` then `.impact(.medium)` |
| Celebration dismiss | `.impact(.light)` |
| Share card generated | `.notification(.success)` |
| Rematch tapped | `.impact(.medium)` |

---

## Responsive Layout

### iPhone (compact width)

- Single column, full-width cards
- Score: 57pt Display Large
- Stats bars: full width minus 32pt padding
- Highlight cards: 240pt width, horizontal scroll
- Bottom bar: standard 72pt + safe area

### iPad (regular width)

- Max content width: 680pt, centered
- Score: 72pt
- Stats bars: within 680pt container
- Highlight cards: 300pt width, can show 2+ at once
- Momentum chart: 280pt height (vs 200pt on iPhone)
- Bottom bar: buttons centered, max 400pt width

### Orientation

- **Portrait:** Default layout as described
- **Landscape (iPad only):** Two-column layout possible — score card + stats on left, highlights + chart on right. For v1, single column with scroll is acceptable.

---

## Dark Mode Color Tokens (MD3)

All colors reference Material Design 3 dark theme tokens:

| Token | Hex | Usage |
|-------|-----|-------|
| `primary` | #D0BCFF | Winner accents, primary buttons, winning score |
| `onPrimary` | #381E72 | Text on primary buttons |
| `primaryContainer` | #4F378B | Confetti, chart fills |
| `secondary` | #CCC2DC | Secondary text accents |
| `tertiary` | #EFB8C8 | Highlight badges, special moments |
| `surface` | #1C1B1F | Main background |
| `surfaceContainer` | #211F26 | Card backgrounds, bottom bar |
| `surfaceContainerLow` | #1D1B20 | Elevated card backgrounds |
| `surfaceContainerHighest` | #E6E0E9 | Loser stat bars (at 60% opacity) |
| `onSurface` | #E6E1E5 | Primary text |
| `onSurfaceVariant` | #CAC4D0 | Secondary text, labels |
| `outline` | #938F99 | Borders, zero line |
| `outlineVariant` | #49454F | Subtle borders |

---

## Data Model

```swift
struct GameRecap {
    let id: UUID
    let date: Date
    let duration: TimeInterval
    let playerA: PlayerRecap
    let playerB: PlayerRecap
    let winner: PlayerSide // .a or .b
    let totalRallies: Int
    let averageRallyLength: Double // in hits
    let scoreProgression: [ScoreState] // for momentum chart
    let highlights: [Highlight]
    let narrative: RecapNarrative
}

struct PlayerRecap {
    let player: Player
    let finalScore: Int
    let servePercentage: Double
    let longestRally: Int // in hits
    let longestScoringRun: Int
    let pointsWonOnServe: Int
    let pointsWonOnReturn: Int
}

struct ScoreState {
    let pointNumber: Int
    let scoreA: Int
    let scoreB: Int
    let server: PlayerSide
    let rallyLength: Int
}

struct Highlight {
    let type: HighlightType // .matchPoint, .longestRally, .clutchPoint, .scoringRun, .comeback
    let pointNumber: Int
    let timestamp: TimeInterval // video timestamp
    let duration: TimeInterval
    let description: String
    let thumbnailURL: URL?
    let videoClipURL: URL?
}

enum RecapNarrative {
    case shutout
    case comeback(deficit: Int)
    case nailbiter(deuceCount: Int)
    case dominant
    case standard
    
    var displayText: String { /* ... */ }
}
```

---

## Implementation Notes

1. **Swift Charts** for momentum timeline — native, performant, accessible
2. **matchedGeometryEffect** for score transition from live → recap
3. **UIGraphicsImageRenderer** for shareable card generation
4. **ShareLink** (iOS 16+) for share sheet integration
5. Video clips stored locally during game, trimmed post-game based on highlight timestamps
6. Accessibility: All charts have `accessibilityLabel` descriptions, VoiceOver reads stats linearly
7. Reduce Motion: Skip confetti, replace slide animations with fades, skip score count-up
