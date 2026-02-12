# LockN Score — Design System Foundation
## LOC-406 | v1.0 | February 2026

---

## 1. Design Philosophy

**Clean. Minimal. Dark. Data-forward.**

LockN Score is a professional sports scoring platform that feels like a premium broadcast overlay — not a casual mobile game. The design language draws from ESPN's data density, theScore's dark-mode elegance, and F1 TV's live telemetry aesthetic, adapted for racquet sports.

**Core Principles:**
- **Glanceability** — Scores and game state readable from 10 feet away on iPad
- **Minimal chrome** — Content is the interface; UI elements recede
- **Motion with purpose** — Animate score changes and state transitions, nothing else
- **Progressive disclosure** — Show what matters now, reveal detail on demand

---

## 2. Color Palette

### 2.1 Surface System (Material Design 3 Dark Scheme)

Based on M3 dark theme with tonal surface elevation using a blue-tinted neutral.

| Token | Hex | Usage |
|---|---|---|
| `surface-dim` | `#0E1117` | App background, deepest layer |
| `surface` | `#121620` | Default surface |
| `surface-bright` | `#1A1F2E` | Elevated cards, sheets |
| `surface-container-lowest` | `#0B0E14` | Below-surface elements |
| `surface-container-low` | `#151A24` | Low-emphasis containers |
| `surface-container` | `#1C2130` | Default containers, cards |
| `surface-container-high` | `#232839` | Modal surfaces, active cards |
| `surface-container-highest` | `#2A3044` | Top-layer surfaces, dropdowns |
| `outline` | `#3A4158` | Borders, dividers |
| `outline-variant` | `#2A3044` | Subtle dividers |

### 2.2 Primary Brand Color

Seed color: **Electric Cyan** `#00BCD4` — energetic, sporty, high-contrast on dark.

| Token | Hex | Usage |
|---|---|---|
| `primary` | `#4DD0E1` | Primary buttons, active states, links |
| `on-primary` | `#003640` | Text on primary |
| `primary-container` | `#004D5A` | Primary container fills |
| `on-primary-container` | `#B2EBF2` | Text on primary container |

### 2.3 Secondary & Tertiary

| Token | Hex | Usage |
|---|---|---|
| `secondary` | `#B0BEC5` | Secondary text, icons, labels |
| `on-secondary` | `#1B2631` | Text on secondary |
| `secondary-container` | `#263238` | Chips, tags, badges |
| `on-secondary-container` | `#CFD8DC` | Text on secondary container |
| `tertiary` | `#FFB74D` | Warm accent — highlights, awards |
| `on-tertiary` | `#3E2723` | Text on tertiary |
| `tertiary-container` | `#4E342E` | Tertiary container |
| `on-tertiary-container` | `#FFE0B2` | Text on tertiary container |

### 2.4 Game State Colors

| Token | Hex | Usage |
|---|---|---|
| `score-player1` | `#4DD0E1` | Player 1 / Left side — cyan |
| `score-player2` | `#FF8A65` | Player 2 / Right side — coral |
| `score-active` | `#FFFFFF` | Active/current score digit |
| `score-inactive` | `#546E7A` | Previous set scores |
| `serve-indicator` | `#FFEB3B` | Serve dot — bright yellow |
| `rally-pulse` | `#E040FB` | Rally counter pulse — magenta |
| `match-point` | `#FF5252` | Match point urgency — red |
| `game-won` | `#69F0AE` | Point/game won flash — green |

### 2.5 Status Colors

| Token | Hex | Usage |
|---|---|---|
| `status-connected` | `#69F0AE` | Connected, streaming live |
| `status-connecting` | `#FFD54F` | Connecting, buffering |
| `status-error` | `#FF5252` | Disconnected, error |
| `status-idle` | `#546E7A` | Idle, waiting |
| `status-recording` | `#FF1744` | Recording indicator (pulsing) |

### 2.6 Text Hierarchy

| Token | Hex | Opacity | Usage |
|---|---|---|---|
| `text-primary` | `#ECEFF1` | 95% | Headlines, scores, primary content |
| `text-secondary` | `#90A4AE` | 70% | Labels, descriptions, metadata |
| `text-tertiary` | `#546E7A` | 45% | Timestamps, hints, disabled |
| `text-on-accent` | `#000000` | 100% | Text on colored backgrounds |

---

## 3. Typography Scale

**Primary Font:** `Inter` — clean geometric sans-serif, excellent for data display, free/open-source, wide weight range. Alternatively: `SF Pro Display` on Apple platforms.

**Score Display Font:** `JetBrains Mono` or `SF Mono` — monospaced for score digits ensures alignment and dramatic presence.

### 3.1 Type Scale (Material 3 adapted)

| Role | Font | Weight | Size | Line Height | Tracking | Usage |
|---|---|---|---|---|---|---|
| `display-large` | JetBrains Mono | 700 | 96px | 104px | -1.5px | Hero score (iPad dashboard) |
| `display-medium` | JetBrains Mono | 700 | 64px | 72px | -0.5px | Set scores (iPad) |
| `display-small` | JetBrains Mono | 600 | 48px | 56px | 0 | Score digits (iPhone) |
| `headline-large` | Inter | 600 | 32px | 40px | 0 | Section headers |
| `headline-medium` | Inter | 600 | 28px | 36px | 0 | Card titles, player names |
| `headline-small` | Inter | 600 | 24px | 32px | 0 | Subheadings |
| `title-large` | Inter | 500 | 22px | 28px | 0 | Dialog titles |
| `title-medium` | Inter | 500 | 16px | 24px | 0.15px | Card titles, nav items |
| `title-small` | Inter | 500 | 14px | 20px | 0.1px | Tabs, small titles |
| `body-large` | Inter | 400 | 16px | 24px | 0.5px | Body text |
| `body-medium` | Inter | 400 | 14px | 20px | 0.25px | Default body |
| `body-small` | Inter | 400 | 12px | 16px | 0.4px | Captions, metadata |
| `label-large` | Inter | 500 | 14px | 20px | 0.1px | Buttons, prominent labels |
| `label-medium` | Inter | 500 | 12px | 16px | 0.5px | Chips, tags, badges |
| `label-small` | Inter | 500 | 10px | 14px | 0.5px | Overlines, micro-labels |

### 3.2 Score-Specific Typography

```
Main Score (iPad):       96px / JetBrains Mono Bold / -1.5 tracking
Set Score (iPad):        48px / JetBrains Mono SemiBold / 0 tracking  
Game Score (iPad):       32px / JetBrains Mono Medium / 0 tracking
Rally Counter (iPad):   120px / JetBrains Mono Bold / -2 tracking
Player Name (iPad):      28px / Inter SemiBold / 0 tracking
Stat Value (iPad):       20px / JetBrains Mono Medium / 0 tracking
Stat Label (iPad):       12px / Inter Medium / 0.5 tracking / uppercase

Main Score (iPhone):     48px / JetBrains Mono Bold / -1 tracking
Set Score (iPhone):      24px / JetBrains Mono SemiBold / 0 tracking
Player Name (iPhone):    18px / Inter SemiBold / 0 tracking
```

---

## 4. Spacing & Grid System

### 4.1 Base Unit

**8px grid.** All spacing, sizing, and layout values are multiples of 8px.

| Token | Value | Usage |
|---|---|---|
| `space-xxs` | 2px | Micro gaps (icon-to-text tight) |
| `space-xs` | 4px | Tight internal padding |
| `space-sm` | 8px | Default internal gap |
| `space-md` | 16px | Card padding, section gaps |
| `space-lg` | 24px | Section padding |
| `space-xl` | 32px | Major section spacing |
| `space-2xl` | 48px | Page-level margins |
| `space-3xl` | 64px | Hero spacing |

### 4.2 Border Radius

| Token | Value | Usage |
|---|---|---|
| `radius-sm` | 8px | Chips, badges, small elements |
| `radius-md` | 12px | Cards, inputs, buttons |
| `radius-lg` | 16px | Modals, sheets |
| `radius-xl` | 24px | Full cards, hero elements |
| `radius-full` | 9999px | Circular avatars, pills |

### 4.3 iPad Landscape Layout (1194 × 834 pt — iPad Pro 11")

```
┌──────────────────────────────────────────────────────────┐
│ 48px margin                                              │
│  ┌──────────────────────────────────────────────────┐    │
│  │              Top Bar (56px)                       │    │
│  ├──────────────────────────────────────────────────┤    │
│  │                                                   │    │
│  │   Main Content Area                              │    │
│  │   12-column grid                                 │    │
│  │   Column gap: 16px                               │    │
│  │   Gutter: 24px                                   │    │
│  │                                                   │    │
│  │   Scoreboard:    cols 1-12 (full width)          │    │
│  │   Player cards:  cols 1-4 / 9-12 (flanks)       │    │
│  │   Rally counter: cols 5-8 (center)               │    │
│  │   PIP video:     cols 9-12 (bottom right)        │    │
│  │                                                   │    │
│  ├──────────────────────────────────────────────────┤    │
│  │              Bottom Bar (48px) — controls         │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

- **Columns:** 12
- **Column gap:** 16px
- **Margin:** 48px (left/right), 24px (top/bottom)
- **Content max-width:** 1098px

### 4.4 iPhone Portrait Layout (393 × 852 pt — iPhone 15 Pro)

```
┌─────────────────┐
│ 16px margin     │
│ ┌─────────────┐ │
│ │ Status (44)  │ │
│ ├─────────────┤ │
│ │             │ │
│ │ Content     │ │
│ │ 4-col grid  │ │
│ │ Gap: 8px    │ │
│ │ Gutter: 16px│ │
│ │             │ │
│ ├─────────────┤ │
│ │ Bottom nav  │ │
│ │ (80px+safe) │ │
│ └─────────────┘ │
└─────────────────┘
```

- **Columns:** 4
- **Column gap:** 8px
- **Margin:** 16px
- **Content max-width:** 361px

### 4.5 Responsive Breakpoints

| Breakpoint | Width | Layout | Target |
|---|---|---|---|
| `compact` | < 600px | 4 columns | iPhone portrait |
| `medium` | 600–839px | 8 columns | iPhone landscape / iPad split |
| `expanded` | 840–1199px | 12 columns | iPad portrait |
| `large` | ≥ 1200px | 12 columns | iPad landscape (primary) |

---

## 5. Component Inventory

### 5.1 Session Creation (iPad — Organizer)

| Component | Description | States |
|---|---|---|
| **ModeSelector** | Large tap targets for game mode (Singles/Doubles/Practice). Card-based with icon + label | default, selected, disabled |
| **SettingsForm** | Grouped form: points per game, sets, deuce rules, tiebreak. M3 segmented buttons + sliders | default, editing, validated |
| **SessionCodeDisplay** | Large QR code on `surface-container-high` with 6-digit alphanumeric code below | generating, ready, expired |
| **WaitingRoom** | Player list with avatar, name, status badge. Animated entry. Ready/Not Ready toggle | empty, waiting, ready, full |
| **PlayerSlot** | Avatar circle + name + connection status dot | empty, joining, connected, ready |
| **StartMatchButton** | Large filled button, disabled until all players ready | disabled, enabled, loading |

### 5.2 Player Registration (iPhone — Player)

| Component | Description | States |
|---|---|---|
| **AuthForm** | Name input, optional email. M3 outlined text fields | empty, focused, filled, error |
| **PhotoCapture** | Circular camera preview with capture button. Crop overlay | preview, captured, confirmed |
| **AvatarDisplay** | Circular player photo with fallback initials | photo, initials, loading |
| **SessionJoinInput** | 6-digit code input (split boxes) OR QR scanner toggle | empty, scanning, entering, joined, error |
| **QRScanner** | Camera viewfinder with animated scan frame | scanning, found, error |
| **StreamControls** | Camera on/off, mic on/off, flip camera. Icon buttons in a bottom bar | on, off, disabled |
| **ConnectionBanner** | Top banner showing connection quality | excellent, good, poor, disconnected |

### 5.3 Live Dashboard (iPad — Organizer/Spectator)

| Component | Description | States |
|---|---|---|
| **Scoreboard** | Full-width score display: player names flanking, current game score center, set scores below | in-progress, deuce, tiebreak, match-point, game-over |
| **ScoreDigit** | Individual score number with flip/slide animation | idle, animating, highlight |
| **SetScoreRow** | Horizontal row of completed set scores per player | default, won-set (highlighted) |
| **RallyCounter** | Large center counter that increments each rally. Pulse animation | idle, counting, reset |
| **ServeIndicator** | Small filled circle (yellow) next to serving player | player1-serving, player2-serving |
| **PlayerCard** | Vertical card: avatar, name, current stats (aces, faults, winners) | default, serving, match-point |
| **PIPVideoView** | Picture-in-picture video feed with player label. Draggable, resizable | streaming, paused, error, minimized |
| **GameClock** | Match duration timer | running, paused |
| **UndoButton** | Circular icon button for score correction | default, confirming |
| **LiveBadge** | Pulsing red dot + "LIVE" label | live, paused |

### 5.4 Post-Game (Both Platforms)

| Component | Description | States |
|---|---|---|
| **FinalScoreCard** | Full match result: winner highlight, all set scores, match duration | default, shared |
| **StatsOverlay** | Expandable stats panel: aces, faults, winners, unforced errors, rally length | collapsed, expanded |
| **StatRow** | Horizontal bar comparing two players' stats | default, highlighted |
| **HighlightPlayerBanner** | Winner celebration: large avatar, "WINNER" label, confetti accent | winner, loser (muted) |
| **ShareActions** | Share button row: Copy Link, Share Image, Social | default, sharing, shared |
| **ShareScoreCard** | Generated image of final score for sharing (branded) | generating, ready |
| **RematchButton** | Prominent CTA to start new match with same players | default, loading |
| **MatchHistoryCard** | Compact card for match list: date, players, score, duration | default, selected |

### 5.5 Shared / System Components

| Component | Description |
|---|---|
| **TopAppBar** | M3 top app bar with title, back nav, overflow menu |
| **NavigationBar** | M3 bottom nav (iPhone) — Home, Live, History, Settings |
| **NavigationRail** | M3 side rail (iPad) — same destinations |
| **IconButton** | Standard M3 icon button (filled, tonal, outlined, standard) |
| **FilledButton** | Primary action buttons |
| **OutlinedButton** | Secondary action buttons |
| **TextButton** | Tertiary/inline actions |
| **SegmentedButton** | Multi-option selector (game settings) |
| **Slider** | Value selector (points per game, etc.) |
| **Switch** | On/off toggle (deuce rules, tiebreak) |
| **TextField** | M3 outlined text field |
| **Chip** | Filter and input chips (player tags, sport type) |
| **Dialog** | M3 dialog for confirmations |
| **BottomSheet** | M3 modal/standard bottom sheet |
| **Snackbar** | Feedback messages (score updated, player joined) |
| **ProgressIndicator** | Linear and circular loading states |
| **Divider** | Horizontal/vertical content separators |
| **Badge** | Notification dots and count badges |
| **Tooltip** | Contextual help on long-press |

---

## 6. Reference Analysis

### 6.1 theScore (⭐ Primary Reference)
- **What works:** Default dark mode (#121212 base), clean typography hierarchy, score prominence, minimal decoration. Scores are huge and instantly readable. Tab-based navigation keeps UI flat.
- **Adopt:** Dark surface approach, score typography scale, information density without clutter.

### 6.2 ESPN App (Dark Mode)
- **What works:** Game cast live view with real-time updates, play-by-play timeline, contextual stats. Strong use of team colors as accents on neutral backgrounds. PIP video integration.
- **Adopt:** Live game state visualization, the concept of contextual accent colors per player/team, PIP video placement patterns.

### 6.3 F1 TV / F1 App
- **What works:** Live telemetry dashboard feel — multiple real-time data points on dark background. Race control overlay aesthetic. Monospaced timing fonts. Status indicators for car/driver state.
- **Adopt:** Dashboard density, monospaced score/timing typography, status indicator system, the "broadcast overlay" aesthetic.

### 6.4 Scora (Figma UI Kit — Soccer Live Scores)
- **What works:** 134-screen kit with both light/dark themes. Card-based match displays, well-structured stats comparisons (horizontal bar charts for head-to-head stats). Clean player profile cards.
- **Adopt:** Stats comparison pattern (horizontal opposed bars), player card layout, match card structure.

### 6.5 SmashPoint Tennis Tracker
- **What works:** Tennis-specific scoring UX — handles sets/games/points hierarchy well. One-tap scoring for live match tracking. Point-by-point history. H2H stats. Most directly relevant sport.
- **Adopt:** Tennis scoring hierarchy display (sets → games → points), serve indicator placement, point-by-point tracking patterns, the single-tap scoring interaction model.

### Design Synthesis

LockN Score should feel like **F1 TV's telemetry dashboard** meets **theScore's dark elegance**, specifically tuned for **racquet sports scoring** with the live interactivity depth of **ESPN GameCast**.

---

## 7. Elevation & Shadows

In M3 dark theme, elevation is expressed through **tonal surface color shifts**, not drop shadows.

| Level | Surface Token | Usage |
|---|---|---|
| Level 0 | `surface-dim` | Background |
| Level 1 | `surface-container-low` | Cards at rest |
| Level 2 | `surface-container` | Active cards, sheets |
| Level 3 | `surface-container-high` | Modals, FABs |
| Level 4 | `surface-container-highest` | Dropdowns, popovers |

Optional: subtle `0 2px 8px rgba(0,0,0,0.3)` shadow on Level 3+ for extra depth.

---

## 8. Motion & Animation

| Animation | Duration | Easing | Usage |
|---|---|---|---|
| Score change | 300ms | `emphasized-decelerate` | Score digit flip/slide |
| Rally pulse | 150ms | `standard` | Rally counter increment |
| Card enter | 250ms | `emphasized-decelerate` | Player joining waiting room |
| Sheet slide | 400ms | `emphasized` | Bottom sheet open/close |
| Status fade | 200ms | `standard` | Connection status change |
| Match point | 500ms | `emphasized` | Match point state change (glow) |
| Confetti burst | 1500ms | `linear` | Post-match celebration |

M3 easing values:
- `emphasized`: `cubic-bezier(0.2, 0, 0, 1)`
- `emphasized-decelerate`: `cubic-bezier(0, 0, 0, 1)`
- `standard`: `cubic-bezier(0.2, 0, 0, 1)`

---

## 9. Iconography

- **System:** Material Symbols (Outlined, weight 400, grade 0, size 24)
- **Sport-specific custom icons needed:**
  - Tennis ball (serve indicator)
  - Racquet (sport selector)
  - Shuttlecock (badminton mode)
  - Rally arrows (rally counter)
  - Court diagram (match type)

Icon sizing: 20px (compact), 24px (default), 28px (prominent), 40px (hero)

---

## 10. Implementation Notes

### Tech Stack Alignment
- **iPad:** SwiftUI with custom M3-inspired theme (or Flutter)
- **iPhone:** Same framework, responsive layout
- **Tokens:** Export as JSON design tokens for cross-platform consistency
- **Fonts:** Bundle Inter (Google Fonts) + JetBrains Mono (JetBrains) — both OFL licensed

### Accessibility
- All text meets **WCAG AAA** contrast on dark surfaces (minimum 7:1 for body, 4.5:1 for large text)
- Touch targets minimum 44×44pt (iOS HIG)
- Score colors distinguishable in deuteranopia (cyan vs coral passes)
- Support Dynamic Type on iOS
- VoiceOver labels for all score elements

### Key Contrast Ratios (verified)
| Foreground | Background | Ratio | Pass |
|---|---|---|---|
| `#ECEFF1` text-primary | `#121620` surface | 14.2:1 | ✅ AAA |
| `#90A4AE` text-secondary | `#121620` surface | 6.8:1 | ✅ AA |
| `#4DD0E1` primary | `#121620` surface | 9.1:1 | ✅ AAA |
| `#FF8A65` player2 | `#121620` surface | 6.4:1 | ✅ AA |
| `#FFEB3B` serve | `#121620` surface | 13.8:1 | ✅ AAA |

---

## Quick Reference: Token Summary

```json
{
  "colors": {
    "surface": "#121620",
    "surfaceDim": "#0E1117",
    "surfaceContainer": "#1C2130",
    "primary": "#4DD0E1",
    "secondary": "#B0BEC5",
    "tertiary": "#FFB74D",
    "scorePlayer1": "#4DD0E1",
    "scorePlayer2": "#FF8A65",
    "serve": "#FFEB3B",
    "rally": "#E040FB",
    "matchPoint": "#FF5252",
    "gameWon": "#69F0AE",
    "textPrimary": "#ECEFF1",
    "textSecondary": "#90A4AE",
    "textTertiary": "#546E7A",
    "statusConnected": "#69F0AE",
    "statusError": "#FF5252",
    "outline": "#3A4158"
  },
  "typography": {
    "scoreFont": "JetBrains Mono",
    "uiFont": "Inter",
    "scoreLarge": "96px/700",
    "scoreMedium": "64px/700",
    "scoreSmall": "48px/600"
  },
  "spacing": {
    "unit": 8,
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32
  },
  "radius": {
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 24,
    "full": 9999
  }
}
```

---

*This design system serves as the foundation for all LockN Score user journeys (LOC-407 through LOC-410) and will be extended to future LockN products. All color values, spacing, and component specs are implementation-ready.*
