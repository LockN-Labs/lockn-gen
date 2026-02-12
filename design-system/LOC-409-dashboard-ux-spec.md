# LOC-409: Live Ping Pong Scoring Dashboard — UX Spec

> **Target:** iPad Landscape (1194×834 pt @ 2x = 2388×1668 px)  
> **Design System:** Material Design 3, Dark Mode  
> **Purpose:** Hero screen for investor demo — must be visually stunning  
> **Date:** 2026-02-10

---

## 1. Competitive Analysis — Sports Scoring UIs

### 1.1 ESPN Scoreboard (NBA/NFL)
- **Pattern:** Compact card-based layout. Team logos left, scores right, quarter breakdown in columns
- **Strengths:** High information density without clutter; strong visual hierarchy via bold score vs. light metadata
- **Weakness:** Designed for multi-game browsing, not single-match immersion
- **Takeaway:** Use their typographic weight contrast — scores are 2-3× heavier than surrounding text

### 1.2 ATP/WTA Live Scores (atptour.com, Wimbledon)
- **Pattern:** Two-row table per match. Player name + flag left, set scores in columns, current game score right
- **Strengths:** The **serve indicator dot** (●) next to player name is universally understood. Set scores as small columns with current game score emphasized
- **Weakness:** Dense, spreadsheet-like — works for multi-court, not for a hero display
- **Takeaway:** Serve indicator dot pattern is perfect for ping pong. Tennis set/game hierarchy maps directly to our set/point model

### 1.3 FIFA Match Center
- **Pattern:** Full-width hero card with team crests flanking a massive centered score. Timeline below
- **Strengths:** **Score as centerpiece** — enormous digits, team identity (crests, colors) creates emotional stakes. Match minute shown prominently
- **Weakness:** Time-based sport; less applicable to point-based
- **Takeaway:** The **bilateral symmetry** (team A ← score → team B) is the gold standard for 1v1 sports display. Adopt this layout

### 1.4 F1 Live Timing (formula1.com, f1-dash.com)
- **Pattern:** Dark background, real-time updating grid with color-coded sectors. Neon accents on dark
- **Strengths:** **Best dark-mode sports UI in production.** Uses color sparingly — purple for fastest, green for personal best, white for default. Monospace tabular numerals throughout
- **Weakness:** Information overload for casual viewers
- **Takeaway:** Color-coding philosophy (accent colors on near-black). Tabular numeral typography. The "data on dark" aesthetic is exactly our target

### 1.5 Apple TV Sports App / MLS Season Pass
- **Pattern:** Full-bleed video with floating translucent score overlay. Rounded pill-shaped score widget
- **Strengths:** **Video-first with non-intrusive score.** Uses blur/translucency (vibrancy) for overlays. Beautiful on large screens
- **Weakness:** Score is secondary to video — may not work for our "score as hero" need
- **Takeaway:** If we go video-dominant (Layout B), this is the model. Translucent overlay with SF-style blur

### 1.6 SofaScore
- **Pattern:** Clean card UI, dark mode available. Animated score transitions. Player H2H stats
- **Strengths:** Excellent mobile-first design. Real-time animations give "live" feeling
- **Takeaway:** Animate score changes — a simple scale-up pulse on score increment makes it feel alive

---

## 2. Dark Mode Dashboard Patterns

### 2.1 Bloomberg Terminal
- Background: Pure black (#000000) with colored text (amber #FF8C00, green #00FF00)
- **Lesson:** Maximum contrast = maximum readability. Monochrome backgrounds let data colors pop
- Not aspirational for aesthetic, but the information density principle holds

### 2.2 Grafana Dark Theme
- Background: #111217 (near-black with slight blue shift)
- Cards/panels: #1A1B21 (subtle elevation)
- Accent: Varies, often green/orange for metrics
- **Lesson:** Layered dark surfaces create depth without borders. Panel cards float on background

### 2.3 Apple TV Sports
- Background: Deep blacks with rich photography
- Score overlays: Frosted glass / vibrancy
- Typography: SF Pro with heavy weights
- **Lesson:** On large screens, let images and data breathe. Generous whitespace (darkspace?) is premium

### 2.4 Material Design 3 Dark Theme (Official Spec)
- Surface: #1C1B1F (M3 default dark surface)
- Surface Container: #211F26
- On-Surface: #E6E1E5
- Primary: Tonal palette based on seed color
- **Lesson:** M3 uses "tonal elevation" — lighter surfaces = higher elevation, no drop shadows

---

## 3. Color System

### 3.1 Core Palette

```
Background (Surface Dim)     #0F0F13    Near-black, slight cool shift
Surface Container Low        #1A1A22    Card/panel backgrounds
Surface Container            #222230    Elevated panels (PIP frames)
Surface Container High       #2C2C3A    Interactive elements

On-Surface                   #E4E1E9    Primary text
On-Surface Variant           #C4C0CC    Secondary text
Outline                      #49454F    Borders, dividers

Score Digits                 #FFFFFF    Pure white — maximum contrast
```

### 3.2 Accent Colors

```
Primary (Serve indicator)    #B8C4FF    Soft periwinkle blue (M3 primary)
Rally Active                 #4ADE80    Green pulse for live rally
Match Point                  #FF6B6B    Warm red alert
Deuce                        #FFC857    Amber warning
Set Won Pip                  #B8C4FF    Same as primary
Set Lost Pip                 #49454F    Muted, same as outline
```

### 3.3 Player Color Coding (Optional)
```
Player Left accent           #60A5FA    Cool blue (left side)
Player Right accent          #F472B6    Warm pink (right side)
```

---

## 4. Typography

### 4.1 Score Digits — **The Star of the Show**

**Primary Recommendation: SF Pro Rounded (Heavy) or Roboto Flex (wght 900)**

For the massive score digits, we need:
- **Tabular numerals** (all digits same width — critical so "11" doesn't shift vs "8")  
- **Heavy weight** (800-900) for visual impact
- **Slightly rounded terminals** for approachability (not the cold precision of pure monospace)

| Option | Font | Why |
|--------|------|-----|
| ★ Best | **SF Pro Rounded Heavy** | Native iOS, tabular figures built-in, round terminals feel sporty not clinical |
| Alt 1 | **Roboto Flex 900** | M3 native, variable font allows fine-tuning, excellent tabular support |
| Alt 2 | **DIN 2014 Bold** | Classic sports/automotive scoreboard feel, built for numerals |
| Alt 3 | **Space Grotesk Bold** | Modern geometric, open-source, strong tabular numerals |

**Critical CSS:**
```css
font-variant-numeric: tabular-nums;
font-feature-settings: "tnum" 1;
```

### 4.2 Type Scale

```
Score Digits (hero)     160pt / 192px    SF Pro Rounded Heavy    #FFFFFF
                        Letter-spacing: -0.02em (tighten at large sizes)

Player Name             28pt / 34px      SF Pro Display Medium   #E4E1E9
Game State Label        14pt / 17px      SF Pro Text Medium      #C4C0CC  (ALL CAPS, tracking +0.08em)
Set Score Pips          20pt / 24px      SF Pro Rounded Semibold #E4E1E9
Rally Counter Value     48pt / 58px      SF Pro Rounded Bold     #4ADE80
Rally Counter Label     12pt / 14px      SF Pro Text Medium      #C4C0CC  (ALL CAPS)
Status Chip Text        13pt / 16px      SF Pro Text Semibold    varies
```

---

## 5. Layout Grid

### 5.1 iPad Landscape Coordinates

```
Screen:     1194 × 834 pt (logical)
            2388 × 1668 px (physical @2x)

Margins:    40pt all sides (safe area + breathing room)
Content:    1114 × 754 pt usable area

Columns:    12-column grid, 16pt gutter
            Column width: ~77pt each
```

### 5.2 Vertical Rhythm
```
Base unit: 8pt
Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64, 96
```

---

## 6. Layout Options

### Layout A: Score-Dominant (★ RECOMMENDED)

**Philosophy:** The score IS the product. Massive digits command attention. Video is supplementary.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  40pt margin                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │ SET 1 OF 5        ● LIVE         RALLY 7    ⏱ 12:34               ││
│  │ 12pt caps         green dot      counter     elapsed               ││
│  ├─────────────────────────────────────────────────────────────────────┤│
│  │                                                                     ││
│  │                                                                     ││
│  │    ┌──────┐                                   ┌──────┐             ││
│  │    │avatar│   Player One                       Player Two  │avatar│ ││
│  │    │ 64pt │   28pt medium                     28pt medium  │ 64pt │ ││
│  │    └──────┘   ● Serving                                    └──────┘ ││
│  │                                                                     ││
│  │               ┌─────────────────────────┐                          ││
│  │               │                         │                          ││
│  │               │    7     :     11       │   ← 160pt digits        ││
│  │               │                         │                          ││
│  │               └─────────────────────────┘                          ││
│  │                                                                     ││
│  │            ○ ○ ●           ● ○ ○ ○         ← Set score pips       ││
│  │           (sets won)      (sets won)                                ││
│  │                                                                     ││
│  │                   ┌── MATCH POINT ──┐       ← Status chip          ││
│  │                                                                     ││
│  ├─────────────────────────────────────────────────────────────────────┤│
│  │                                                                     ││
│  │    ┌──────────────────┐    ┌──────────────────┐                    ││
│  │    │                  │    │                  │                     ││
│  │    │   PIP Camera 1   │    │   PIP Camera 2   │   ← 16:9 ratio    ││
│  │    │   240×135pt      │    │   240×135pt      │     w/ 8pt radius  ││
│  │    │                  │    │                  │                     ││
│  │    └──────────────────┘    └──────────────────┘                    ││
│  │                                                                     ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Exact Measurements (Layout A):**
```
Top status bar:         y=40, h=24pt
Player row:             y=96, h=64pt
  - Avatar: 64×64pt, 32pt corner radius (circle)
  - Player name: vertically centered to avatar
  - Serve dot: 8pt circle, 4pt below name, Primary color, animated pulse

Score zone:             y=184, h=200pt (centered vertically in zone)
  - Digits: 160pt, centered horizontally
  - Colon separator: 48pt, #49454F, vertically centered
  - Player 1 score: right-aligned to center-60pt
  - Player 2 score: left-aligned to center+60pt

Set score pips:         y=400, h=24pt
  - Circles: 12pt diameter, 8pt gap
  - Won: filled Primary #B8C4FF
  - Lost/remaining: outline only #49454F

Status chip:            y=440, h=32pt
  - Pill shape: 16pt corner radius
  - MATCH POINT: bg #FF6B6B/20%, text #FF6B6B
  - DEUCE: bg #FFC857/20%, text #FFC857

PIP video zone:         y=520, h=135pt
  - Each PIP: 240×135pt (16:9)
  - Gap between PIPs: 24pt
  - Centered horizontally as a pair
  - Corner radius: 12pt
  - Border: 1pt #49454F
  - Camera label: 10pt, bottom-left inside, translucent bg
```

**Pros:**
- Score digits at 160pt are impossible to miss across a room — perfect for demo
- Clean bilateral symmetry reads immediately as "competition"
- PIP videos at bottom don't compete with score
- Most impressive from 10+ feet away (investor presentation distance)

**Cons:**
- Video feeds are small — if camera quality is a key demo point, may undersell it
- Less "action" feel; more "data display"

---

### Layout B: Video-Dominant

**Philosophy:** The live camera feeds are the hero. Score floats as an overlay — like watching a real broadcast.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  ┌────────────────────────────────┐ ┌────────────────────────────────┐ │
│  │                                │ │                                │ │
│  │                                │ │                                │ │
│  │                                │ │                                │ │
│  │         CAMERA 1               │ │         CAMERA 2               │ │
│  │         (Player 1 side)        │ │         (Player 2 side)        │ │
│  │         537 × 380pt            │ │         537 × 380pt            │ │
│  │                                │ │                                │ │
│  │                                │ │                                │ │
│  │                                │ │                                │ │
│  │                                │ │                                │ │
│  └────────────────────────────────┘ └────────────────────────────────┘ │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │ ┌──┐                                                        ┌──┐  ││
│  │ │av│ Player One  ● ○○   7  :  11   ○○● ○  Player Two  │av│  ││
│  │ └──┘              sets      96pt       sets             └──┘  ││
│  │                          MATCH POINT                           ││
│  └─────────────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │  RALLY 7          SET 2 OF 5           ● LIVE         ⏱ 12:34    ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Exact Measurements (Layout B):**
```
Video zone:             y=40, h=380pt
  - Each feed: 537×380pt (≈ 16:11.3, slightly wider than 16:9 to fill)
  - Gap between feeds: 20pt
  - Corner radius: 16pt

Score bar:              y=444, h=96pt
  - Background: Surface Container #222230
  - Corner radius: 16pt
  - Score digits: 96pt, centered
  - Avatars: 40×40pt, circle
  - Player names: 20pt medium
  - Set pips: 10pt circles

Status bar:             y=556, h=32pt
  - Background: Surface Container Low #1A1A22
  - All items 12pt caps
```

**Pros:**
- Showcases the camera/video tech — the "wow" factor of live PIP feeds
- Feels like a broadcast production — sophisticated
- If camera streams are high quality, this is the most impressive

**Cons:**
- Score digits smaller (96pt vs 160pt) — less dramatic
- Video feeds may show latency/quality issues more prominently at large size
- If cameras aren't running during demo, large empty black rectangles look broken

---

### Layout C: Balanced

**Philosophy:** Equal weight to score and video. The dashboard that does everything well.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  ┌─ LEFT PANEL (Score) ──────────────┐ ┌─ RIGHT PANEL (Video) ───────┐│
│  │                                    │ │                             ││
│  │  SET 2 OF 5    ● LIVE              │ │  ┌───────────────────────┐  ││
│  │                                    │ │  │                       │  ││
│  │  ┌──┐ Player One      ● serving    │ │  │     CAMERA 1          │  ││
│  │  │av│ 28pt                         │ │  │     480 × 270pt       │  ││
│  │  └──┘                              │ │  │     (16:9)            │  ││
│  │                                    │ │  │                       │  ││
│  │         ┌──────────────┐           │ │  └───────────────────────┘  ││
│  │         │              │           │ │                             ││
│  │         │   7  :  11   │  ← 128pt  │ │  ┌───────────────────────┐  ││
│  │         │              │           │ │  │                       │  ││
│  │         └──────────────┘           │ │  │     CAMERA 2          │  ││
│  │                                    │ │  │     480 × 270pt       │  ││
│  │  ┌──┐ Player Two                  │ │  │     (16:9)            │  ││
│  │  │av│ 28pt                         │ │  │                       │  ││
│  │  └──┘                              │ │  └───────────────────────┘  ││
│  │                                    │ │                             ││
│  │  ○●● ○○    Sets    ○○ ●○○         │ │  RALLY  7     ⏱ 12:34     ││
│  │                                    │ │  48pt green                 ││
│  │       ┌── MATCH POINT ──┐          │ │                             ││
│  │                                    │ │                             ││
│  └────────────────────────────────────┘ └─────────────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Exact Measurements (Layout C):**
```
Left panel (Score):     x=40, w=557pt (≈50% minus gap)
Right panel (Video):    x=613, w=541pt
Gap:                    16pt

Left panel contents:
  - Status line: y=56, 14pt caps
  - Player 1 row: y=112, avatar 56×56, name 28pt
  - Score: y=224, 128pt digits, centered in panel
  - Player 2 row: y=388, same as player 1
  - Set pips: y=464
  - Status chip: y=504

Right panel contents:
  - Camera 1: y=56, 480×270pt, 12pt radius
  - Camera 2: y=350, 480×270pt, 12pt radius
  - Rally counter: y=644, 48pt value + 12pt label
```

**Pros:**
- Best of both worlds — nothing feels sacrificed
- Natural left-to-right reading: "check score, watch action"
- Videos stacked vertically = can show both camera angles simultaneously
- Works even if one camera is offline

**Cons:**
- Neither element truly dominates — less dramatic than A or B
- Split attention may confuse at first glance
- Left panel can feel text-heavy

---

## 7. Component Specifications

### 7.1 Serve Indicator
```
Visual: Filled circle, 8pt diameter
Color: Primary #B8C4FF
Animation: Gentle pulse (scale 1.0→1.3→1.0, 2s ease-in-out, infinite)
Position: Inline after player name, 8pt gap
```

### 7.2 Rally Counter
```
Container: Pill shape, bg #4ADE80 at 12% opacity
Value: 48pt SF Pro Rounded Bold, #4ADE80
Label: "RALLY" 12pt caps, #C4C0CC, 4pt above value
Animation: Value scales up 1.0→1.15→1.0 on increment (200ms spring)
```

### 7.3 Score Digits
```
Animation on change:
  - Old digit: slide up + fade out (150ms ease-out)
  - New digit: slide up from below + fade in (200ms ease-out, 50ms delay)
  - Brief flash: text-shadow 0 0 20px rgba(255,255,255,0.5) (300ms fade)
```

### 7.4 Status Chips
```
MATCH POINT:
  - bg: #FF6B6B at 15% opacity → rgba(255,107,107,0.15)
  - text: #FF6B6B
  - border: 1pt #FF6B6B at 30%
  - Pill: h=32pt, px=16pt, radius=16pt
  - Animation: subtle pulse on border opacity

DEUCE:
  - bg: rgba(255,200,87,0.15)
  - text: #FFC857
  - border: 1pt rgba(255,200,87,0.30)

GAME POINT:
  - bg: rgba(184,196,255,0.15)
  - text: #B8C4FF
```

### 7.5 PIP Video Feed
```
Container: rounded rect, 12pt radius
Border: 1pt solid #49454F (or none if video is playing)
Placeholder (no feed): Surface Container #222230 + centered camera icon 32pt #49454F
Camera label: bottom-left, 8pt inset, pill bg rgba(0,0,0,0.6), 11pt text
Connection indicator: top-right, 8pt circle, green=#4ADE80 / red=#FF6B6B
```

### 7.6 Set Score Pips
```
Layout: Horizontal row of circles (best-of-5 = 5 pips, need 3 to win)
Size: 12pt diameter, 8pt gap
Won: filled with Primary #B8C4FF
Lost: filled with #49454F
Remaining: 1pt stroke #49454F, no fill
Current set: subtle glow ring (box-shadow 0 0 6px Primary at 40%)
```

---

## 8. Animation & Motion

### 8.1 Principles (M3 Motion)
- **Score change:** Most dramatic — 300ms with overshoot (spring curve)
- **Rally increment:** Quick pulse — 200ms
- **Status chip appear:** Fade + scale from 0.8 — 250ms ease-out
- **Serve switch:** Dot slides from one player to the other — 400ms ease-in-out
- **Set won:** Pip fills with brief starburst particle effect — 500ms

### 8.2 "Live" Feeling
- Rally counter should have a subtle ambient animation when active (very slow breathe at 0.5% opacity)
- LIVE indicator: green dot + "LIVE" text, dot pulses slowly (3s cycle)
- Clock/timer: updates every second, no animation (let it be steady)

---

## 9. Recommendation

### ★ Layout A: Score-Dominant — for investor demo

**Rationale:**

1. **Legibility at distance.** In a demo room, investors will be 6-15 feet from the iPad. 160pt digits are readable from 20+ feet. Layout B's 96pt digits require closer viewing.

2. **Instant comprehension.** The bilateral "Player ← Score → Player" pattern is universally understood. No learning curve. An investor glances and immediately knows the state of play.

3. **Fail-safe.** If camera feeds have latency, drop frames, or aren't running, the small PIP panels degrade gracefully. In Layout B, empty video panels are 70% of the screen — catastrophic for a demo.

4. **"Product" signal.** A massive, beautifully typeset score display says "we built something intentional and polished." It communicates design taste. Large video feeds say "we have cameras" — less differentiated.

5. **Animation showcase.** The score digit transition animation (slide + flash) is most dramatic at 160pt. It will elicit an involuntary reaction. At 96pt it's just "nice."

6. **Brand memory.** Investors will remember "that beautiful scoreboard with the massive numbers." It's iconic. Video feeds are forgettable.

**One tweak:** Consider making the PIP panels slightly larger than specced (320×180pt instead of 240×135pt) if camera quality is a key part of the pitch. This gives Layout A a touch more video presence without sacrificing the score dominance.

---

## 10. Implementation Notes

### 10.1 Flutter/SwiftUI Considerations
- Use `tabularFigures` text style modifier in SwiftUI, or `fontFeatures: [FontFeature.tabularFigures()]` in Flutter
- Score animation: `AnimatedSwitcher` (Flutter) or `.contentTransition(.numericText())` (SwiftUI 17+)
- PIP feeds: Use `AVPlayerLayer` or platform camera stream widget, masked to `RoundedRectangle`
- Dark theme: Implement as M3 `ColorScheme.dark()` with custom overrides per Section 3

### 10.2 Accessibility
- Score digits should be semantically labeled: "Player One: 7, Player Two: 11"
- Serve indicator needs non-color signal (the pulse animation serves this)
- Minimum contrast ratio exceeded everywhere (white on #0F0F13 = 19.2:1)

### 10.3 Screen Burn-in Prevention
- For OLED iPads: implement subtle pixel-shift (±2pt, 60s cycle) on static elements
- Avoid pure #FFFFFF for large static areas (scores change frequently, so OK)

---

## Appendix: Quick Reference Card

| Element | Size | Font | Color | Position |
|---------|------|------|-------|----------|
| Score digits | 160pt | SF Pro Rounded Heavy | #FFFFFF | Center, y=184 |
| Player name | 28pt | SF Pro Display Medium | #E4E1E9 | Flanking score, y=96 |
| Avatar | 64×64pt | — | — | Outside of names |
| Serve dot | 8pt ⌀ | — | #B8C4FF (pulse) | After serving player |
| Set pips | 12pt ⌀ | — | #B8C4FF / #49454F | Below score, y=400 |
| Rally counter | 48pt val | SF Pro Rounded Bold | #4ADE80 | Top bar |
| Status chip | 32pt h | SF Pro Text Semibold 13pt | varies | Below pips, y=440 |
| PIP video | 240×135pt | — | — | Bottom center, y=520 |
| Background | — | — | #0F0F13 | Full screen |

---

*Spec authored for LOC-409. Ready for design implementation and prototyping.*
