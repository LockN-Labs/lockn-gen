# LOC-407 + LOC-408: Mobile UX Flows
## Session Creation (iPad) + Player Registration (iPhone)

**Version:** 1.0 · **Date:** 2026-02-10
**Design System:** Material Design 3 · **Theme:** Dark mode
**Typography:** M3 type scale (Display, Headline, Title, Body, Label)
**Color tokens:** `surface` #121212, `surfaceContainer` #1E1E1E, `surfaceContainerHigh` #2C2C2C, `primary` #A0E77D (lime-green accent), `onPrimary` #1A1A1A, `onSurface` #E6E6E6, `onSurfaceVariant` #A0A0A0, `error` #FFB4AB, `outline` #444444

---

## Flow Diagram (Text-Based)

```
═══════════════════════════════════════════════════════════════
                    FLOW 1: SESSION HOST (iPad Landscape)
═══════════════════════════════════════════════════════════════

  ┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐
  │  1.1    │────▶│   1.2    │────▶│   1.3    │────▶│   1.4   │
  │  Home   │     │  Mode    │     │ Settings │     │  Lobby  │
  │         │     │ Select   │     │          │     │         │
  └─────────┘     └──────────┘     └──────────┘     └─────────┘
       │               │                │                 │
       │          [Back] ◀──────  [Back] ◀────────   [Cancel]
       │                                                  │
       ▼                                                  ▼
  Game History                                     Game Screen
  (tap to view)                                   (LOC-409+)


═══════════════════════════════════════════════════════════════
                  FLOW 2: PLAYER JOIN (iPhone Portrait)
═══════════════════════════════════════════════════════════════

  ┌─────────┐     ┌──────────┐     ┌──────────┐
  │  2.1    │────▶│   2.2    │────▶│   2.4    │
  │  Auth   │     │ Profile  │     │  Join    │
  │         │     │ Setup    │     │ Session  │
  └─────────┘     └──────────┘     └──────────┘
       │                                 │
       │          ┌──────────┐           │
       └────────▶│   2.3    │           │
     (returning) │ Profile  │───────────┘
                 │ Update   │
                 └──────────┘
                                         │
                                         ▼
                                   ┌──────────┐     ┌──────────┐
                                   │   2.5    │────▶│   2.6    │
                                   │ Pre-Game │     │  Ready   │
                                   │          │     │  State   │
                                   └──────────┘     └──────────┘
                                                         │
                                                         ▼
                                                    Game Stream
                                                    (LOC-409+)
```

---

# FLOW 1: SESSION CREATION (iPad Landscape)

**Device:** iPad (all sizes) · **Orientation:** Landscape locked
**Viewport:** 1194 × 834 pt (11" iPad Pro reference)

---

## Screen 1.1 — Home / Landing

### Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  [Logo]  LockN Score                          [⚙] [👤 Profile]  │  ← Top app bar, 64pt
│──────────────────────────────────────────────────────────────────│
│                                                                  │
│   ┌─────────────────────────┐    ┌────────────────────────────┐  │
│   │                         │    │  RECENT GAMES              │  │
│   │                         │    │                            │  │
│   │    🏓                   │    │  ┌──────────────────────┐  │  │
│   │                         │    │  │ Rally · 21-18       │  │  │
│   │   [ NEW GAME ]          │    │  │ vs Alex, Sam · 2h ago│  │  │
│   │                         │    │  └──────────────────────┘  │  │
│   │   Start a match         │    │  ┌──────────────────────┐  │  │
│   │                         │    │  │ Game · 11-7          │  │  │
│   │                         │    │  │ vs Jordan · Yesterday│  │  │
│   │                         │    │  └──────────────────────┘  │  │
│   │                         │    │  ┌──────────────────────┐  │  │
│   │                         │    │  │ Solo · 15 pts        │  │  │
│   │                         │    │  │ Practice · 3 days ago│  │  │
│   │                         │    │  └──────────────────────┘  │  │
│   │                         │    │                            │  │
│   └─────────────────────────┘    │  [View All History →]      │  │
│                                  └────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Element Specs

| Element | Type | Spec |
|---|---|---|
| Top bar | M3 `TopAppBar` | `surfaceContainer`, 64pt height |
| Logo | Icon + text | 28pt icon, `titleLarge` text, `primary` color |
| Settings icon | `IconButton` | 24pt, `onSurfaceVariant` |
| Profile avatar | `IconButton` with image | 36pt circle, border `outline` |
| Left panel | Hero area | 55% width, centered content |
| Paddle icon | Animated SVG | 80pt, subtle floating animation (2s ease-in-out loop, 4pt Y translate) |
| NEW GAME button | M3 `FilledButton` | `primary` fill, `onPrimary` text, `labelLarge`, 56pt height, 24pt corner radius, min-width 240pt |
| Subtitle | `bodyMedium` | `onSurfaceVariant`, "Start a match" |
| Right panel | Scrollable list | 45% width, `surfaceContainer` background, 16pt corner radius |
| "Recent Games" header | `titleMedium` | `onSurface`, 16pt padding top |
| Game card | M3 `Card` (outlined) | `surfaceContainerHigh`, 12pt radius, 12pt padding, 8pt gap between cards |
| Game card — mode | `labelMedium` | `primary` color |
| Game card — score | `titleSmall` | `onSurface` |
| Game card — meta | `bodySmall` | `onSurfaceVariant` |
| "View All" link | `TextButton` | `primary`, `labelMedium` |

### Interactions

- **NEW GAME tap:** M3 ripple → shared-axis-X transition to Screen 1.2 (300ms `emphasizedDecelerate`)
- **Game card tap:** Expand into detail sheet (bottom sheet, 50% height) showing full game stats
- **Profile avatar tap:** Navigate to profile/settings
- **Pull-to-refresh:** Refresh game history list (circular indicator, `primary` color)
- **Empty state (no history):** Replace right panel with illustration + "No games yet — start your first match!"

### Edge Cases

- **Offline:** Show cached history with `bodySmall` "Offline — showing cached data" chip below header
- **Auth expired:** Redirect to auth flow with toast "Session expired, please sign in again"
- **No profile set up:** Badge on profile avatar, nudge banner at top of right panel

### Accessibility

- NEW GAME button: `accessibilityLabel = "Start a new game"`, minimum 48pt touch target (exceeds at 56pt)
- Game cards: `accessibilityLabel = "[Mode] game, score [X]-[Y], against [players], [time ago]"`
- VoiceOver reading order: Top bar → NEW GAME → subtitle → Recent Games header → cards top-to-bottom
- All text meets WCAG AAA contrast on dark surface (lime-green on #121212 = 8.2:1)
- Dynamic Type supported up to `xxxLarge`

---

## Screen 1.2 — Mode Selection

### Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  [← Back]  Select Mode                                          │  ← 64pt
│──────────────────────────────────────────────────────────────────│
│                                                                  │
│   ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│   │                  │  │                  │  │              │  │
│   │   🎯 SOLO        │  │   🏓 RALLY       │  │  🏆 GAME     │  │
│   │                  │  │                  │  │              │  │
│   │  Practice on     │  │  Casual back-   │  │  Full comp-  │  │
│   │  your own.       │  │  and-forth.     │  │  etitive     │  │
│   │  Track points,   │  │  No formal      │  │  match with  │  │
│   │  improve your    │  │  serves. Just   │  │  serves,     │  │
│   │  game.           │  │  rally and      │  │  rules, and  │  │
│   │                  │  │  score.         │  │  winner.     │  │
│   │  1 player        │  │  2 players      │  │  2-4 players │  │
│   │                  │  │                 │  │              │  │
│   │  [ SELECT ]      │  │  [ SELECT ]     │  │  [ SELECT ]  │  │
│   │                  │  │                 │  │              │  │
│   └──────────────────┘  └──────────────────┘  └──────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Element Specs

| Element | Type | Spec |
|---|---|---|
| Back button | M3 `IconButton` + label | `←` icon 24pt + `labelLarge` "Back", `onSurface` |
| Title | `headlineMedium` | `onSurface`, centered or start-aligned |
| Mode cards | M3 `Card` (filled) | `surfaceContainerHigh`, 16pt radius, equal 3-column with 16pt gaps, max-height 360pt |
| Mode icon | Emoji or custom icon | 48pt, centered top of card |
| Mode name | `headlineSmall` | `primary`, centered |
| Description | `bodyMedium` | `onSurfaceVariant`, centered, 16pt horizontal padding |
| Player count | `labelMedium` | `onSurfaceVariant`, with person icon, centered |
| SELECT button | M3 `TonalButton` | `secondaryContainer`/`onSecondaryContainer`, `labelLarge`, 48pt height, full width minus 24pt padding |
| Selected state | Card border | 2pt `primary` border + scale(1.02) + glow shadow |

### Interactions

- **Enter:** Cards stagger in from bottom (100ms delay each, 300ms `emphasizedDecelerate`)
- **Hover/focus:** Card lifts with 8dp elevation, subtle `primary` border appears (200ms)
- **SELECT tap:** Card pulses (scale 1.0→1.03→1.0, 200ms), 400ms delay, then shared-axis-X to Screen 1.3
- **Back:** Shared-axis-X reverse to Screen 1.1

### Edge Cases

- **Solo mode:** Skip Screen 1.3 player count, go directly to lobby with simplified settings
- **Feature-gated modes:** If a mode is unavailable (e.g., beta), show card with reduced opacity (0.5) and "Coming Soon" badge, disabled interaction

### Accessibility

- Cards: `accessibilityRole = "button"`, `accessibilityLabel = "[Mode] mode. [Description]. [Player count]"`
- Selected card: `accessibilityValue = "selected"`
- Focus order: Back → Solo → Rally → Game (left to right)
- Keyboard navigation: Arrow keys move between cards, Enter/Space selects

---

## Screen 1.3 — Game Settings

### Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  [← Back]  Game Settings                       [Rally] badge    │
│──────────────────────────────────────────────────────────────────│
│                                                                  │
│   ┌──────────────────────────────┐  ┌─────────────────────────┐  │
│   │  Points to Win               │  │  SUMMARY               │  │
│   │  ○ 11  ● 21  ○ Custom [__]  │  │                         │  │
│   │                              │  │  Mode:   Rally          │  │
│   │  Win by 2?                   │  │  Points: 21             │  │
│   │  [======●===] ON             │  │  Win by 2: Yes          │  │
│   │                              │  │  Serve: Alt. every 5    │  │
│   │  Serve Rules                 │  │  Players: 2             │  │
│   │  ○ Alternate every point     │  │                         │  │
│   │  ● Alternate every 5 pts    │  │                         │  │
│   │  ○ No serve tracking         │  │                         │  │
│   │                              │  │                         │  │
│   │  Players                     │  │                         │  │
│   │  [ 2 ]  [−] [+]             │  │                         │  │
│   │                              │  │                         │  │
│   └──────────────────────────────┘  │  [ CREATE GAME ]        │  │
│                                     └─────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Element Specs

| Element | Type | Spec |
|---|---|---|
| Mode badge | M3 `AssistChip` | `secondaryContainer`, `labelMedium`, top-right of app bar |
| Left panel | Settings form | 60% width, `surface` background |
| "Points to Win" | Section header `titleMedium` | `onSurface`, 24pt top margin |
| Point options | M3 `RadioButton` group | Horizontal row, `primary` selected, `outline` unselected |
| Custom field | M3 `OutlinedTextField` | 64pt width, `keyboardType: number`, appears only when "Custom" selected (slide-down 200ms) |
| "Win by 2" | M3 `Switch` | `primary` track when on, label `bodyLarge` to left |
| Serve rules | M3 `RadioButton` group | Vertical list, 48pt row height each |
| Players stepper | M3 custom stepper | `titleLarge` number centered, `IconButton` minus/plus, min 2 max 4 (for Game), fixed 2 (for Rally), fixed 1 (for Solo) |
| Right panel | Summary card | 40% width, `surfaceContainer`, 16pt radius, 24pt padding, sticky |
| Summary labels | `bodyMedium` | `onSurfaceVariant` for labels, `onSurface` for values |
| CREATE GAME | M3 `FilledButton` | `primary`, `onPrimary`, `labelLarge`, 56pt height, full width, 24pt radius |

### Interactions

- **Radio select:** Morph animation on selection dot (scale 0→1, 150ms `standard`)
- **Switch toggle:** M3 thumb slides with haptic feedback
- **Stepper:** Number cross-fades (fade out/in 150ms), buttons disable at min/max with reduced opacity
- **Custom points:** Text field slides down when selected, auto-focuses, validates 1–99
- **Summary panel:** Values animate (cross-fade) when settings change — provides live feedback
- **CREATE GAME:** Ripple → 300ms pulse → loading spinner replaces text → navigate to 1.4

### Edge Cases

- **Invalid custom points:** Red `error` underline, `supportingText` "Enter 1–99"
- **Solo mode:** Hide serve rules and player count sections entirely (animated collapse)
- **Rally mode:** Player count locked to 2, stepper disabled with `bodySmall` "Rally is always 2 players"

### Accessibility

- All form controls: proper `accessibilityRole`, labels linked via `labelFor`
- Radio groups: `accessibilityRole = "radiogroup"`, individual items `"radio"`
- Switch: `accessibilityLabel = "Win by 2 rule"`, `accessibilityValue = "on/off"`
- Stepper: `accessibilityLabel = "Number of players, [N]"`, buttons "Decrease players" / "Increase players"
- Summary: `accessibilityLiveRegion = "polite"` — announces changes

---

## Screen 1.4 — Lobby / Waiting Room

### Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  [✕ Cancel]  Game Lobby                    Rally · 21 pts       │
│──────────────────────────────────────────────────────────────────│
│                                                                  │
│   ┌───────────────────────────────┐  ┌────────────────────────┐  │
│   │                               │  │  PLAYERS (1/2)         │  │
│   │     Session Code              │  │                        │  │
│   │                               │  │  ┌──────────────────┐  │  │
│   │     A 7 K 3 M 2              │  │  │ 👤 You (Host)    │  │  │
│   │                               │  │  │ ✓ Connected      │  │  │
│   │     ┌──────────────┐          │  │  └──────────────────┘  │  │
│   │     │              │          │  │                        │  │
│   │     │  [QR CODE]   │          │  │  ┌──────────────────┐  │  │
│   │     │              │          │  │  │ ··· Waiting...   │  │  │
│   │     │              │          │  │  │                  │  │  │
│   │     └──────────────┘          │  │  └──────────────────┘  │  │
│   │                               │  │                        │  │
│   │  Scan or enter code to join   │  │                        │  │
│   │  [ Copy Code ] [ Share ]      │  │  ┌──────────────────┐  │  │
│   │                               │  │  │ [ START GAME ]   │  │  │
│   └───────────────────────────────┘  │  │  (disabled)      │  │  │
│                                      └────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Element Specs

| Element | Type | Spec |
|---|---|---|
| Cancel button | `TextButton` with ✕ icon | `onSurfaceVariant`, triggers confirmation dialog |
| Settings badge | `AssistChip` | Top-right, shows mode + points |
| Left panel | Code display area | 55% width, centered content |
| Session code | Custom display | `displayLarge` (57pt), `primary` color, monospace font (`Roboto Mono`), letter-spacing 16pt, each character in its own `surfaceContainerHigh` rounded rect (48×56pt, 12pt radius) |
| QR code | Generated QR | 200×200pt, white on `surfaceContainerHigh` background, 16pt padding, 12pt corner radius container, encodes deep link `locknscore://join/{code}` |
| Instruction text | `bodyMedium` | `onSurfaceVariant`, centered below QR |
| Copy Code | M3 `OutlinedButton` | `primary` border/text, clipboard icon left |
| Share | M3 `TonalButton` | `secondaryContainer`, share icon left |
| Right panel | Player list | 45% width |
| Players header | `titleMedium` | `onSurface`, with `(current/max)` counter in `onSurfaceVariant` |
| Player card (connected) | M3 `Card` (filled) | `surfaceContainerHigh`, 12pt radius, avatar (48pt circle) + name `bodyLarge` + status `labelSmall` `primary` |
| Player card (waiting) | M3 `Card` (outlined) | `outline` border dashed, pulsing opacity (0.4→0.7, 2s loop), "Waiting for player..." `bodyMedium` `onSurfaceVariant` |
| START GAME (disabled) | M3 `FilledButton` | Opacity 0.38, `onSurface` text, no ripple |
| START GAME (active) | M3 `FilledButton` | `primary`, `onPrimary`, 56pt height, full-width, pulsing glow animation (box-shadow `primary` at 20% opacity, 2s breathe loop) |

### Interactions

- **Player joins:** Card transforms from "waiting" to "connected" — border solidifies, avatar fades in, subtle confetti burst (3-4 particles, `primary` color, 500ms), haptic success
- **Player disconnects:** Card reverts to waiting state with 300ms transition, toast "Player disconnected"
- **All players connected:** START GAME enables with spring animation (scale 0.95→1.05→1.0, 400ms), haptic notification
- **START GAME tap:** Ripple → full-screen `primary` wipe transition → game screen
- **Copy Code:** Button text changes to "Copied ✓" for 2s, haptic light
- **Share:** iOS share sheet with text "Join my LockN Score game! Code: {code}" + deep link
- **Cancel:** M3 `AlertDialog` — "End this session? Players will be disconnected." [Keep Playing] [End Session]
- **QR code:** Subtle breathing scale animation (1.0→1.01→1.0, 4s loop) to draw attention

### Edge Cases

- **Session timeout (5 min no activity):** Warning dialog at 4:00, auto-cancel at 5:00 with toast
- **All players disconnect:** Revert to waiting state, keep session alive
- **Network loss (host):** Overlay banner "Connection lost — reconnecting..." with progress indicator, auto-retry 3× at 2s intervals, then "Unable to reconnect" with [Retry] [Cancel] options
- **Code collision (server-side):** Server regenerates — transparent to user

### Accessibility

- Session code: `accessibilityLabel = "Session code: A, 7, K, 3, M, 2"` (spelled out)
- QR code: `accessibilityLabel = "QR code for joining session. Use Copy Code button for text alternative"`
- Player cards: `accessibilityLiveRegion = "polite"` — announces joins/disconnects
- START GAME disabled: `accessibilityHint = "Waiting for [N] more players to connect"`
- Cancel: `accessibilityLabel = "Cancel and end game session"`

---

# FLOW 2: PLAYER REGISTRATION + STREAM (iPhone Portrait)

**Device:** iPhone (all sizes) · **Orientation:** Portrait
**Viewport:** 393 × 852 pt (iPhone 15 Pro reference)
**Safe areas:** 59pt top, 34pt bottom (home indicator)

---

## Screen 2.1 — Auth (Login / Sign Up)

### Layout

```
┌─────────────────────────┐
│                         │
│                         │
│        🏓               │
│     LockN Score         │
│                         │
│  ┌───────────────────┐  │
│  │ Email             │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ Password      [👁] │  │
│  └───────────────────┘  │
│                         │
│  [ SIGN IN            ] │
│                         │
│  ── or continue with ── │
│                         │
│  [G Google] [🍎 Apple]  │
│                         │
│                         │
│  Don't have an account? │
│  Sign Up                │
│                         │
│                         │
└─────────────────────────┘
```

**Sign Up variant** (toggled inline, no navigation):

```
┌─────────────────────────┐
│        🏓               │
│     LockN Score         │
│                         │
│  ┌───────────────────┐  │
│  │ Email             │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ Password      [👁] │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │ Confirm Password  │  │
│  └───────────────────┘  │
│                         │
│  [ CREATE ACCOUNT     ] │
│                         │
│  ── or continue with ── │
│  [G Google] [🍎 Apple]  │
│                         │
│  Already have an account│
│  Sign In                │
└─────────────────────────┘
```

### Element Specs

| Element | Type | Spec |
|---|---|---|
| Logo area | Centered block | 120pt from safe-area top, icon 64pt, app name `headlineMedium` `primary`, 8pt gap |
| Email field | M3 `OutlinedTextField` | Full width − 32pt margins, 56pt height, `bodyLarge` |
| Password field | M3 `OutlinedTextField` | Same, with trailing `IconButton` visibility toggle |
| SIGN IN / CREATE ACCOUNT | M3 `FilledButton` | `primary`, full width − 32pt, 56pt height, `labelLarge` |
| Divider | M3 `Divider` + centered text | `outline` line, `bodySmall` "or continue with" `onSurfaceVariant` |
| Social buttons | M3 `OutlinedButton` row | 2 buttons, equal width, 48pt height, 8pt gap, brand icons 20pt |
| Toggle text | `bodyMedium` + `TextButton` | `onSurfaceVariant` + `primary` for link |

### Interactions

- **Sign In / Sign Up toggle:** Content cross-fades (200ms), Confirm Password field slides down/up (250ms `emphasizedDecelerate`)
- **Field focus:** Label floats up (M3 standard), border becomes `primary`
- **Submit:** Button shows circular progress indicator (replacing text), 24pt, `onPrimary`
- **Success:** Fade out entire screen → Screen 2.2 or 2.3 (shared-axis-Y up, 350ms)
- **Keyboard:** View scrolls up to keep focused field visible + submit button in view

### Edge Cases

- **Invalid email:** `error` color border + `supportingText` "Enter a valid email address" on blur
- **Wrong password:** Shake animation on password field (translateX ±8pt, 3 cycles, 300ms), `supportingText` "Incorrect password"
- **Account exists (sign up):** `supportingText` "An account with this email already exists. Sign in?"
- **Network error:** M3 `Snackbar` at bottom: "Can't connect. Check your internet." [Retry]
- **OAuth failure:** Snackbar "Sign in with [provider] failed. Try again."
- **Rate limited:** Disable submit for 30s, show countdown in button text

### Accessibility

- Fields: `accessibilityLabel` matches label text, `textContentType` for autofill (`emailAddress`, `password`, `newPassword`)
- Password visibility: `accessibilityLabel = "Show/Hide password"`, `accessibilityValue = "hidden/visible"`
- Social buttons: `accessibilityLabel = "Sign in with Google/Apple"`
- Error messages: announced immediately via `accessibilityLiveRegion = "assertive"`
- Minimum touch targets: all 48pt+

---

## Screen 2.2 — Profile Setup (First-Time)

### Layout

```
┌─────────────────────────┐
│                         │
│     Set Up Your         │
│     Profile             │
│                         │
│     ┌─────────────┐     │
│     │             │     │
│     │   Camera    │     │
│     │   Preview   │     │
│     │   (circle)  │     │
│     │             │     │
│     │    [📸]     │     │
│     └─────────────┘     │
│                         │
│     [ Take Photo ]      │
│                         │
│  ┌───────────────────┐  │
│  │ Display Name      │  │
│  └───────────────────┘  │
│                         │
│  This is how other      │
│  players will see you   │
│                         │
│  [ CONTINUE           ] │
│                         │
│  Skip for now →         │
│                         │
└─────────────────────────┘
```

### Element Specs

| Element | Type | Spec |
|---|---|---|
| Title | `headlineMedium` | `onSurface`, center-aligned, 32pt from safe area |
| Camera preview | Circular container | 180pt diameter, `outline` border 2pt, centered, shows front camera live feed, clipped to circle |
| Camera icon (no permission) | `FilledTonalIconButton` | 48pt, centered in circle, `surfaceContainerHigh` background |
| Take Photo button | M3 `TonalButton` | `secondaryContainer`, camera icon left, centered below preview |
| After capture | Preview shows frozen frame | Overlay small "Retake" `TextButton` bottom-right of circle |
| Display Name | M3 `OutlinedTextField` | Full width − 32pt, 56pt, `bodyLarge`, max 24 chars, character counter |
| Helper text | `bodySmall` | `onSurfaceVariant`, center-aligned |
| CONTINUE | M3 `FilledButton` | `primary`, full width − 32pt, 56pt, disabled until name entered (min 2 chars) |
| Skip | `TextButton` | `primary`, `labelMedium`, centered |

### Interactions

- **Camera preview:** Live front-camera feed in circle, subtle vignette at edges
- **Take Photo tap:** Shutter animation (white flash overlay 100ms at 0.8 opacity), haptic medium, freeze frame in circle
- **After capture:** "Retake" appears with fade-in (200ms), captured image gently scales from 1.05→1.0 (settle animation)
- **CONTINUE:** Shared-axis-Y → Screen 2.4 (Join Session)
- **Skip:** Same transition, sets default avatar (initials or silhouette)
- **Name field:** Real-time character count (`labelSmall` aligned right under field)

### Edge Cases

- **Camera permission denied:** Circle shows placeholder silhouette icon, "Take Photo" becomes "Open Settings" linking to iOS Settings, explanatory text "Camera access needed for your profile photo"
- **Camera unavailable:** Show file picker alternative "Choose from Library"
- **Name with special chars:** Allow Unicode (emoji, accents), sanitize server-side
- **Name too short (< 2):** CONTINUE stays disabled, `supportingText` appears "Name must be at least 2 characters"

### Accessibility

- Camera preview: `accessibilityLabel = "Camera preview for profile photo"`
- Take Photo: `accessibilityLabel = "Take profile photo"`, after capture: `accessibilityLabel = "Profile photo captured. Double tap to retake"`
- Character counter: `accessibilityLabel = "[N] of 24 characters used"`
- Skip: `accessibilityHint = "Continue without a profile photo"`
- VoiceOver order: Title → camera → take photo → name → continue → skip

---

## Screen 2.3 — Profile Update (Returning)

### Layout

```
┌─────────────────────────┐
│                         │
│     Welcome Back,       │
│     Alex! 👋            │
│                         │
│     ┌─────────────┐     │
│     │             │     │
│     │  [Current   │     │
│     │   Photo]    │     │
│     │             │     │
│     └─────────────┘     │
│                         │
│     [ Retake Photo ]    │
│                         │
│  ┌───────────────────┐  │
│  │ Alex              │  │
│  └───────────────────┘  │
│                         │
│  [ CONTINUE           ] │
│                         │
│                         │
│                         │
│                         │
│                         │
└─────────────────────────┘
```

### Element Specs

- Same layout as 2.2 but pre-populated
- Title: `headlineMedium` "Welcome Back," + `headlineMedium` `primary` "[Name]! 👋"
- Photo circle: Shows stored profile photo (180pt, same as 2.2)
- Retake Photo: M3 `TonalButton` (same as Take Photo styling)
- Name field: Pre-filled with current name, editable
- CONTINUE: Always enabled (existing data is valid)
- No "Skip" option (already has profile)

### Interactions

- **Enter:** Photo loads with fade-in (300ms), name auto-populated
- **Retake Photo:** Opens camera capture (same as 2.2 flow), replaces current photo with transition
- **CONTINUE:** Uploads any changes → Screen 2.4
- **No changes made:** Skip upload, navigate immediately

### Edge Cases

- **Stored photo load failure:** Show initials avatar with `bodySmall` "Photo unavailable" and Retake button
- **Profile data corrupted:** Fall back to Screen 2.2 (first-time setup)

### Accessibility

- Same as 2.2, plus `accessibilityLabel` on photo: "Your current profile photo. Double tap Retake to change"

---

## Screen 2.4 — Join Session

### Layout

```
┌─────────────────────────┐
│  [← Back]               │
│                         │
│     Join a Game         │
│                         │
│  ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐│
│  │ │ │ │ │ │ │ │ │ │ │ ││
│  └─┘ └─┘ └─┘ └─┘ └─┘ └─┘│
│                         │
│  Enter the code shown   │
│  on the host's screen   │
│                         │
│  ──────── or ────────   │
│                         │
│  ┌───────────────────┐  │
│  │                   │  │
│  │   QR Scanner      │  │
│  │   Viewfinder      │  │
│  │                   │  │
│  │   [ 🔦 ]         │  │
│  └───────────────────┘  │
│                         │
│  Point at the QR code   │
│  on the host's screen   │
│                         │
│  [ JOIN              ]  │
│                         │
└─────────────────────────┘
```

### Element Specs

| Element | Type | Spec |
|---|---|---|
| Back | M3 `IconButton` | `←`, navigates to profile screen |
| Title | `headlineMedium` | `onSurface`, center-aligned |
| Code input | 6 individual `OutlinedTextField` boxes | 48×56pt each, 8pt gaps, `displaySmall` text, `primary` border on focus, auto-advance on input, monospace |
| Helper text | `bodyMedium` | `onSurfaceVariant`, centered |
| Divider | Same as auth screen | "or" centered |
| QR viewfinder | Camera preview | 280×200pt, 16pt corner radius, `outline` border, corner bracket overlays (L-shapes at corners, `primary`, 3pt stroke) |
| Torch toggle | `IconButton` | Positioned bottom-right of viewfinder, `surfaceContainerHigh` circle background, 40pt |
| Scanner instruction | `bodyMedium` | `onSurfaceVariant` |
| JOIN | M3 `FilledButton` | `primary`, full width − 32pt, 56pt, disabled until 6 chars entered or QR scanned |

### Interactions

- **Code input:** Auto-advance cursor to next box on input. Backspace moves to previous. Paste support (fills all 6 from clipboard). Each box scales slightly on focus (1.0→1.05). Auto-uppercase.
- **QR scan detected:** Viewfinder flashes `primary` border (200ms), haptic success, code auto-fills in boxes (stagger fill animation, 50ms per box), JOIN enables
- **JOIN tap:** Loading spinner in button → validate code → if valid: shared-axis-Y → Screen 2.5. If invalid: shake animation on code boxes + `error` border + `supportingText` "Invalid code. Check and try again."
- **Torch:** Toggle icon between flashlight-on/off, haptic light
- **Code entry complete (6 chars):** JOIN auto-pulses once to draw attention

### Edge Cases

- **Camera permission denied for QR:** Hide viewfinder section entirely, show only code entry with expanded layout. `bodySmall` "Enable camera in Settings to scan QR codes" with link
- **Invalid code:** Error state as above, clear fields after 2s for re-entry
- **Session full:** `Snackbar` "This game is full. Ask the host to increase player count."
- **Session already started:** `Snackbar` "This game has already started."
- **Session expired/not found:** `Snackbar` "Session not found. Ask the host for a new code."
- **Network error:** Snackbar with retry
- **Rapid QR re-scans:** Debounce 2s after first successful scan

### Accessibility

- Code boxes: Treated as single `accessibilityElement`, `accessibilityLabel = "Game code, [N] of 6 characters entered"`, `accessibilityHint = "Enter the 6-character code from the host screen"`
- QR viewfinder: `accessibilityLabel = "QR code scanner. Point camera at QR code on host screen"`
- Torch: `accessibilityLabel = "Flashlight [on/off]"`
- JOIN disabled: `accessibilityHint = "Enter complete code or scan QR to enable"`

---

## Screen 2.5 — Pre-Game (Camera/Mic + Stream Preview)

### Layout

```
┌─────────────────────────┐
│  Rally · 21 pts    [✕]  │
│                         │
│  ┌───────────────────┐  │
│  │                   │  │
│  │                   │  │
│  │   Camera          │  │
│  │   Preview         │  │
│  │   (Your stream)   │  │
│  │                   │  │
│  │                   │  │
│  │         [🔄]      │  │
│  └───────────────────┘  │
│                         │
│  Alex                   │
│  ● Connected            │
│                         │
│  ┌─────┐  ┌─────┐      │
│  │ 🎤  │  │ 📷  │      │
│  │ On  │  │ On  │      │
│  └─────┘  └─────┘      │
│                         │
│  Waiting for host to    │
│  start the game...      │
│                         │
│  [ READY ✓            ] │
│                         │
└─────────────────────────┘
```

### Element Specs

| Element | Type | Spec |
|---|---|---|
| Top bar | Inline | Game info `labelLarge` `onSurfaceVariant` left, `IconButton` ✕ right |
| Camera preview | Full-width card | Full width − 32pt, 4:3 aspect ratio, 16pt radius, front camera default, mirrored |
| Flip camera | `IconButton` | 40pt, `surfaceContainerHigh` 50% opacity background, bottom-right of preview, 12pt offset |
| Player name | `titleMedium` | `onSurface`, left-aligned below preview |
| Connection status | `labelSmall` with dot | `primary` dot (8pt circle) + "Connected" `primary`, or `error` dot + "Reconnecting..." `error` |
| Mic toggle | M3 `FilledTonalIconButton` | 64pt, `secondaryContainer` when on, `errorContainer` when off (muted), icon swaps mic/mic-off |
| Camera toggle | Same | 64pt, camera/camera-off icon |
| Status text | `bodyMedium` | `onSurfaceVariant`, centered |
| READY | M3 `FilledButton` | `primary`, full width − 32pt, 56pt |

### Interactions

- **Enter:** Camera permission dialog (system). If granted → preview appears with fade-in (400ms). Mic permission follows.
- **Flip camera:** Icon rotates 180° (300ms), preview cross-fades between front/back
- **Mic toggle:** Icon morphs (mic ↔ mic-off, 200ms), haptic light. When muted, red slash appears over icon
- **Camera toggle:** Preview dims and shows camera-off icon centered, toggle turns `errorContainer`
- **READY tap:** Button transforms → green check fills from left (wipe, 300ms), text changes to "Ready ✓", button becomes `OutlinedButton` with `primary` border (can tap again to un-ready). Notifies host.
- **Connection status:** Dot pulses when "Reconnecting..." (opacity 0.4→1.0, 1s loop)
- **✕ tap:** Confirmation dialog "Leave this session?" [Stay] [Leave]

### Edge Cases

- **Camera denied:** Preview area shows dark card with camera-off icon + "Camera access required for streaming" + "Open Settings" `TextButton`. Player can still join audio-only with `bodySmall` "You'll join without video"
- **Mic denied:** Mic toggle shows disabled state, `bodySmall` "Microphone access required" + "Open Settings". Can play without mic
- **Both denied:** Show both messages stacked, emphasize "Open Settings"
- **Connection lost:** Status changes to "Reconnecting...", overlay on preview "⚠ Connection lost", auto-retry with exponential backoff (1s, 2s, 4s, 8s). After 30s: "Unable to reconnect" with [Retry] [Leave] dialog
- **Host cancels session:** Navigate back to Screen 2.4 with `Snackbar` "The host ended the session"
- **Low bandwidth:** `labelSmall` "Poor connection" warning below status, auto-reduce video quality

### Accessibility

- Camera preview: `accessibilityLabel = "Your camera preview"`
- Flip camera: `accessibilityLabel = "Switch to [front/back] camera"`
- Mic toggle: `accessibilityLabel = "Microphone [on/off]"`, `accessibilityRole = "switch"`
- Camera toggle: `accessibilityLabel = "Camera [on/off]"`, `accessibilityRole = "switch"`
- Connection status: `accessibilityLiveRegion = "polite"`, announces changes
- READY: `accessibilityLabel = "Ready"` / `"Not ready. Tap to toggle"`

---

## Screen 2.6 — Ready State

### Layout

```
┌─────────────────────────┐
│                         │
│                         │
│                         │
│         ✅              │
│                         │
│     You're In!          │
│                         │
│  ┌───────────────────┐  │
│  │  ┌──┐  ┌──┐      │  │
│  │  │👤│  │··│      │  │
│  │  │You│  │  │      │  │
│  │  └──┘  └──┘      │  │
│  │                   │  │
│  │  1 of 2 players   │  │
│  └───────────────────┘  │
│                         │
│  Waiting for host       │
│  to start...            │
│                         │
│  ● ● ● (animated dots) │
│                         │
│                         │
│  [ LEAVE GAME ]         │
│                         │
└─────────────────────────┘
```

### Element Specs

| Element | Type | Spec |
|---|---|---|
| Check icon | Animated | 64pt, `primary`, draw-on animation (checkmark path draws from center-left to bottom to top-right, 500ms `emphasizedDecelerate`), then subtle pulse (scale 1.0→1.1→1.0, 300ms) |
| Title | `headlineMedium` | `onSurface`, centered |
| Player card area | M3 `Card` (filled) | `surfaceContainer`, 16pt radius, horizontal scroll if > 3 players, centered |
| Player avatars | Circular | 56pt, photo if available, initials if not. Your avatar has `primary` 2pt border. Unjoined slots: dashed `outline` border, `?` icon |
| Player count | `bodyMedium` | `onSurfaceVariant`, centered in card |
| Waiting text | `bodyLarge` | `onSurfaceVariant`, centered |
| Animated dots | 3 circles | 8pt each, `onSurfaceVariant`, sequential opacity animation (each dot fades 0.3→1.0→0.3 with 200ms offset), loops |
| LEAVE GAME | M3 `OutlinedButton` | `error` border/text, full width − 32pt, 48pt |

### Interactions

- **Enter (from 2.5):** Check icon draw animation → title fades in (200ms delay) → card slides up (300ms delay) → waiting text + dots fade in (500ms delay). Total choreography ~800ms.
- **Player joins:** New avatar slides in from right (300ms), count updates with cross-fade, haptic light
- **Host starts game:** Dots stop → text changes to "Starting..." → full-screen transition wipe (`primary` color radial expand from center, 500ms) → Game stream screen
- **LEAVE GAME:** Confirmation dialog → navigate to Home or Screen 2.4
- **Background:** Keep WebSocket alive, show local notification if app backgrounded and game starts: "Your LockN Score game is starting!"

### Edge Cases

- **Host disconnects:** After 30s timeout → "Host disconnected. Waiting for reconnection..." If 60s: "Session ended" with [OK] → navigate to Screen 2.4
- **Player kicked:** `Snackbar` "You were removed from the session" → Screen 2.4
- **App backgrounded > 5 min:** Reconnect on foreground, if session still exists rejoin silently; if not, show "Session expired" dialog
- **Push notification permission:** If not granted, show inline `bodySmall` "Enable notifications to know when the game starts" with `TextButton` "Enable"

### Accessibility

- Check animation: `accessibilityLabel = "Successfully joined the game"`
- Player avatars: `accessibilityLabel = "[Name], connected"` / `"Waiting for player"`
- Waiting dots: `accessibilityElementsHidden = true` (decorative)
- Waiting text: `accessibilityLabel = "Waiting for host to start the game"`
- LEAVE GAME: `accessibilityLabel = "Leave game session"`
- Live updates: `accessibilityLiveRegion = "polite"` on player count and status text

---

## Global Design Tokens

### Spacing Scale
- `4pt` — micro gap
- `8pt` — tight (between related elements)
- `12pt` — default inner padding
- `16pt` — standard gap / margin
- `24pt` — section separation
- `32pt` — screen horizontal margin
- `48pt` — large section gap

### Animation Curves (M3)
- `standard` — 300ms cubic-bezier(0.2, 0, 0, 1)
- `emphasizedDecelerate` — 400ms cubic-bezier(0.05, 0.7, 0.1, 1)
- `emphasizedAccelerate` — 200ms cubic-bezier(0.3, 0, 0.8, 0.15)

### Transitions Between Screens
- **Forward navigation:** Shared-axis-X (horizontal) or shared-axis-Y (vertical), 350ms `emphasizedDecelerate`
- **Back navigation:** Reverse of forward, 300ms `emphasizedAccelerate`
- **Modal/dialog:** Fade + scale from 0.9 center, 250ms

### Haptic Feedback
- **Button tap:** Light impact
- **Success (join, connect):** Success notification
- **Error (invalid code):** Error notification (3 short)
- **Toggle:** Light impact

### Dark Mode Elevation
- Level 0: `surface` #121212
- Level 1: `surfaceContainer` #1E1E1E
- Level 2: `surfaceContainerHigh` #2C2C2C
- Level 3: `surfaceContainerHighest` #383838

---

## Implementation Notes for Figma

1. **Component library:** Build on M3 Design Kit for Figma (Google official). Override color tokens with the dark palette above.
2. **Auto-layout:** Every screen should use auto-layout for responsive behavior across iPad/iPhone sizes.
3. **Prototyping:** Use Smart Animate for shared-axis transitions. Wire all flows in a single Figma file with two pages (iPad / iPhone).
4. **Variants:** Create variants for every interactive state (default, focused, disabled, error, loading) on custom components (code input boxes, player cards, toggle buttons).
5. **Device frames:** iPad Pro 11" landscape, iPhone 15 Pro portrait as primary frames. Test with iPad mini and iPhone SE for minimum sizes.
6. **Handoff:** Use Figma Dev Mode with token references matching the design tokens above.
