# LOC-408: Player Registration + Stream Setup — iPhone Wireframe Spec

**App:** LockN Score  
**Platform:** iPhone (portrait only, 390×844 logical pts — iPhone 14 baseline)  
**Design System:** Material Design 3, Dark Mode  
**Theme:** `surface: #121212`, `primary: #BB86FC`, `on-surface: #FFFFFF`, `error: #CF6679`  
**Typography:** Roboto (body), Montserrat (headings/logo)  
**Safe Areas:** Top 59pt (status bar + notch), Bottom 34pt (home indicator)  
**Target:** Investor demo — polish > edge-case coverage  

---

## Flow Map

```
┌─────────┐    ┌──────────┐    ┌─────────────┐
│ Welcome  │───▶│ Auth0    │───▶│ Profile     │
│ (S1)     │    │ Login(S2)│    │ Setup (S3/4)│
└─────────┘    └──────────┘    └──────┬──────┘
                                      │
                                      ▼
                               ┌─────────────┐
                               │ Join Session │
                               │ (S5)        │
                               └──────┬──────┘
                                      │
                                      ▼
                               ┌─────────────┐
                               │ Permissions  │
                               │ (S6)        │
                               └──────┬──────┘
                                      │
                                      ▼
                               ┌─────────────┐
                               │ Stream      │
                               │ Connect (S7)│
                               └──────┬──────┘
                                      │
                                      ▼
                               ┌─────────────┐
                               │ Ready State  │
                               │ (S8)        │
                               └─────────────┘

Branching:
  S1 → S2 (Sign In or Create Account — same Auth0 flow)
  S2 → S3 (first-time user) OR S4 (returning user)
  S3/S4 → S5
  S5 → S6 (if permissions not yet granted) OR S7 (if already granted)
  S6 → S7
  S7 → S8
```

---

## Screen 1: Welcome / Auth

### Purpose
Brand-forward entry point. Single decision: sign in or create account.

### ASCII Wireframe

```
┌──────────────────────────────┐
│         ▓ Status Bar ▓       │  ← system status bar
│                              │
│                              │
│                              │
│                              │
│                              │
│          ┌────────┐          │
│          │  LOGO  │          │  ← 80×80pt logo mark
│          │  🏓    │          │
│          └────────┘          │
│                              │
│       L O C K N  S C O R E   │  ← wordmark, 28pt Montserrat Bold
│                              │
│     "Lock in. Play. Win."    │  ← tagline, 14pt Roboto, #888
│                              │
│                              │
│                              │
│                              │
│  ┌──────────────────────────┐│
│  │       Sign In            ││  ← FilledButton, primary #BB86FC
│  └──────────────────────────┘│
│                              │
│  ┌──────────────────────────┐│
│  │     Create Account       ││  ← OutlinedButton, border #BB86FC
│  └──────────────────────────┘│
│                              │
│     Continue as Guest ›      │  ← TextButton, 14pt, #888
│                              │
│         ▓ Home Bar ▓         │
└──────────────────────────────┘
```

### Layout Spec (top → bottom)

| Element | Type | Position | Style |
|---------|------|----------|-------|
| Status bar | System | top 0pt | Transparent, light content |
| Spacer | — | 160pt from top | Pushes logo to ~38% vertical |
| Logo mark | Image | centered | 80×80pt, asset `logo_mark.png` |
| Spacer | — | 16pt | — |
| Wordmark | Text | centered | `Montserrat Bold 28pt`, `#FFFFFF`, letter-spacing 4pt |
| Tagline | Text | centered, 8pt below | `Roboto Regular 14pt`, `#888888` |
| Spacer | Flexible | fills remaining | Pushes buttons toward bottom |
| Sign In | FilledButton | horiz padded 24pt | height 52pt, cornerRadius 26pt, `#BB86FC`, label `Roboto Medium 16pt #121212` |
| Spacer | — | 12pt | — |
| Create Account | OutlinedButton | horiz padded 24pt | height 52pt, cornerRadius 26pt, border 1.5pt `#BB86FC`, label `Roboto Medium 16pt #BB86FC` |
| Spacer | — | 16pt | — |
| Guest link | TextButton | centered | `Roboto Regular 14pt`, `#888888`, underline on press |
| Bottom safe area | — | 34pt | — |

### Behavior

- **Sign In** → navigates to Screen 2 with `screen_hint=login`
- **Create Account** → navigates to Screen 2 with `screen_hint=signup`
- **Continue as Guest** → navigates directly to Screen 5 (Join Session), profile is "Guest Player" with default avatar. Guest cannot stream (view-only mode).
- Entry animation: logo fades in (300ms), wordmark slides up (400ms, 50ms delay), buttons slide up (500ms, 150ms delay). `DecelerateInterpolator`.

### Edge Cases

- **No network:** Show inline banner at top: "No internet connection" with retry. Buttons remain tappable but Auth0 will fail at S2.
- **Already authenticated (valid token):** Skip S1+S2 entirely → route to S4 (returning) or S5 if profile complete.

---

## Screen 2: Auth0 Login

### Purpose
Auth0 Universal Login via in-app browser (ASWebAuthenticationSession on iOS). This is largely Auth0-controlled UI, but we configure its appearance.

### ASCII Wireframe — Auth0 Hosted Page (customized)

```
┌──────────────────────────────┐
│  ✕ Cancel          locknscore│  ← in-app browser chrome
│─────────────────────────────-│
│                              │
│          ┌────────┐          │
│          │  LOGO  │          │  ← 48×48 logo
│          └────────┘          │
│                              │
│       Welcome Back           │  ← or "Create Your Account"
│                              │
│  ┌──────────────────────────┐│
│  │ 🍎  Continue with Apple  ││  ← Apple SSO button (black bg)
│  └──────────────────────────┘│
│                              │
│  ┌──────────────────────────┐│
│  │ G  Continue with Google  ││  ← Google SSO button (white bg)
│  └──────────────────────────┘│
│                              │
│  ─────────── or ────────────-│  ← divider
│                              │
│  ┌──────────────────────────┐│
│  │ email@example.com        ││  ← TextInput
│  └──────────────────────────┘│
│                              │
│  ┌──────────────────────────┐│
│  │ ●●●●●●●●          👁    ││  ← PasswordInput + toggle
│  └──────────────────────────┘│
│                              │
│        Forgot password?      │  ← TextButton
│                              │
│  ┌──────────────────────────┐│
│  │        Continue           ││  ← FilledButton primary
│  └──────────────────────────┘│
│                              │
│  Don't have an account?      │
│  Sign up ›                   │  ← toggle login/signup
│                              │
└──────────────────────────────┘
```

### Auth0 Configuration

| Setting | Value |
|---------|-------|
| Universal Login Experience | New |
| Logo | LockN Score logo 48×48 |
| Primary color | `#BB86FC` |
| Page background | `#121212` |
| Social connections | Apple, Google |
| Database connection | email+password |

### Error States

| Error | Display | Recovery |
|-------|---------|----------|
| Wrong password | Inline red text below password: "Incorrect email or password." Input border → `#CF6679` | Clear password field, focus it |
| Account locked | Full-width banner: "Account locked. Check your email to unlock." | Link to support email |
| Network error | Banner: "Connection failed. Check your internet and try again." | Retry button |
| Email not verified | "Please verify your email. Resend verification →" | Resend link |
| Rate limited | "Too many attempts. Try again in 60 seconds." | Countdown timer, disable button |

### Behavior

- **Cancel (✕)** → returns to Screen 1
- **Successful auth (first time)** → Auth0 callback → app receives tokens → Screen 3
- **Successful auth (returning)** → Auth0 callback → app checks profile completeness → Screen 4 (or S5 if profile complete and session code provided via deep link)
- **Apple SSO:** Uses native `ASAuthorizationAppleIDProvider` (modal sheet, not redirect)
- **Google SSO:** Uses `ASWebAuthenticationSession`

### Edge Cases

- **User cancels Apple SSO modal:** Returns to Auth0 page, no error shown.
- **Auth0 page fails to load:** Blank screen with centered "Unable to load. Tap to retry." and retry icon.
- **Deep link with session code:** After auth completes, preserve the session code and skip to S5 with it pre-filled.

---

## Screen 3: First-Time Profile Setup

### Purpose
Capture player photo and confirm display name. Photo is critical — it appears on the iPad scoreboard during the game.

### ASCII Wireframe — State A: Camera Capture

```
┌──────────────────────────────┐
│         ▓ Status Bar ▓       │
│                              │
│  ←                    Skip › │  ← nav: back to S2 / skip
│                              │
│       Set Up Your Profile    │  ← 22pt Montserrat SemiBold
│                              │
│   Take a photo for the       │
│   scoreboard                 │  ← 14pt Roboto, #AAAAAA
│                              │
│       ┌──────────────┐       │
│       │              │       │
│       │              │       │
│       │   CAMERA     │       │  ← 200×200pt, circular mask
│       │   PREVIEW    │       │    cornerRadius 100pt
│       │   (front)    │       │    border 3pt #BB86FC
│       │              │       │
│       │              │       │
│       └──────────────┘       │
│                              │
│           ┌────┐             │
│           │ ◉  │             │  ← capture button 72pt circle
│           └────┘             │    white ring + inner dot
│                              │
│  ┌──────────────────────────┐│
│  │ Display Name             ││  ← TextInput, pre-filled from
│  │ Sean Murphy              ││    Auth0 user_metadata.name
│  └──────────────────────────┘│
│                              │
│  This helps others identify  │
│  you on the scoreboard.      │  ← 12pt Roboto, #888
│                              │
│  ┌──────────────────────────┐│
│  │        Continue           ││  ← disabled until photo taken
│  └──────────────────────────┘│    OR user explicitly skips
│                              │
│         ▓ Home Bar ▓         │
└──────────────────────────────┘
```

### ASCII Wireframe — State B: Photo Captured (Review)

```
┌──────────────────────────────┐
│         ▓ Status Bar ▓       │
│                              │
│  ←                    Skip › │
│                              │
│       Set Up Your Profile    │
│                              │
│   Looking good! 🔥            │  ← updates on capture
│                              │
│       ┌──────────────┐       │
│       │              │       │
│       │   CAPTURED   │       │  ← frozen frame, circular
│       │   PHOTO      │       │    border → green #4CAF50
│       │              │       │
│       └──────────────┘       │
│                              │
│     Retake        Accept     │  ← two TextButtons side-by-side
│                              │
│  ┌──────────────────────────┐│
│  │ Display Name             ││
│  │ Sean Murphy              ││
│  └──────────────────────────┘│
│                              │
│  This helps others identify  │
│  you on the scoreboard.      │
│                              │
│  ┌──────────────────────────┐│
│  │        Continue           ││  ← enabled after Accept
│  └──────────────────────────┘│
│                              │
│         ▓ Home Bar ▓         │
└──────────────────────────────┘
```

### Layout Spec

| Element | Type | Position | Style |
|---------|------|----------|-------|
| Back arrow | IconButton `←` | top-left, 16pt inset | 24×24pt icon, `#FFFFFF` |
| Skip | TextButton | top-right, 16pt inset | `Roboto Medium 14pt`, `#888` |
| Title | Text | centered, 16pt below nav | `Montserrat SemiBold 22pt`, `#FFFFFF` |
| Subtitle | Text | centered, 8pt below title | `Roboto Regular 14pt`, `#AAAAAA` |
| Camera viewfinder | CameraPreview | centered, 32pt below subtitle | 200×200pt, circular clip, border 3pt `#BB86FC` |
| Capture button | Custom | centered, 24pt below viewfinder | 72×72pt circle, outer ring 3pt `#FFFFFF`, inner circle 56pt `#FFFFFF` |
| Retake / Accept | TextButton pair | centered, replaces capture btn | `Roboto Medium 16pt`, Retake `#888`, Accept `#BB86FC` |
| Name input | OutlinedTextField | horiz padded 24pt, 32pt below | height 56pt, label "Display Name", `#FFFFFF` text, `#BB86FC` focus border |
| Helper text | Text | 8pt below input | `Roboto Regular 12pt`, `#888888` |
| Continue | FilledButton | horiz padded 24pt, 24pt below helper | height 52pt, `#BB86FC`, disabled state `#333` bg `#666` text |
| Bottom safe area | — | 34pt | — |

### Behavior

- Camera activates immediately using front camera (request permission first if not granted — iOS will show native permission dialog).
- **Capture (◉):** Freeze frame → show Retake/Accept.
- **Retake:** Resume camera preview, hide Retake/Accept, show capture button.
- **Accept:** Lock in photo, border turns green, enable Continue.
- **Continue:** Upload photo + name → navigate to Screen 5.
- **Skip:** Show bottom sheet warning:
  ```
  ┌──────────────────────────────┐
  │                              │
  │   Skip photo?                │
  │                              │
  │   Your photo helps other     │
  │   players recognize you on   │
  │   the scoreboard. You can    │
  │   add one later.             │
  │                              │
  │  ┌──────────────────────────┐│
  │  │    Add Photo             ││ ← primary
  │  └──────────────────────────┘│
  │                              │
  │       Skip for now           │ ← TextButton
  │                              │
  └──────────────────────────────┘
  ```
  - "Skip for now" → generate initials avatar (e.g., "SM" on purple circle), navigate to Screen 5.

### Edge Cases

- **Camera permission denied:** Replace viewfinder with placeholder icon + "Camera access required" + "Open Settings" link. Skip button still works.
- **Name field empty:** Continue button disabled. Hint: "Enter your name to continue."
- **Name too long:** Max 24 chars, truncate with ellipsis on scoreboard. Input shows char counter at 20+.
- **Photo upload fails:** Store locally, retry in background. Don't block flow.
- **Low light:** No special handling — camera auto-adjusts. Consider adding a flash toggle (stretch goal).

---

## Screen 4: Returning Player — Profile Review

### Purpose
Quick confirmation for returning players. Get them into the game fast.

### ASCII Wireframe

```
┌──────────────────────────────┐
│         ▓ Status Bar ▓       │
│                              │
│  ←                           │  ← back to S1 (sign out)
│                              │
│        Welcome back!         │  ← 22pt Montserrat SemiBold
│                              │
│                              │
│       ┌──────────────┐       │
│       │              │       │
│       │   PLAYER     │       │  ← 160×160pt circular
│       │   PHOTO      │       │    border 3pt #BB86FC
│       │              │       │
│       └──────────────┘       │
│                              │
│        📷 Update Photo       │  ← TextButton, icon + text
│                              │
│                              │
│  ┌──────────────────────────┐│
│  │ Display Name             ││  ← pre-filled, editable
│  │ Sean Murphy         ✏️   ││
│  └──────────────────────────┘│
│                              │
│                              │
│                              │
│                              │
│                              │
│  ┌──────────────────────────┐│
│  │    Continue to Game       ││  ← FilledButton primary
│  └──────────────────────────┘│
│                              │
│      Sign out                │  ← TextButton, #888, 12pt
│                              │
│         ▓ Home Bar ▓         │
└──────────────────────────────┘
```

### Layout Spec

| Element | Type | Position | Style |
|---------|------|----------|-------|
| Back arrow | IconButton | top-left | navigates back / sign out |
| Title | Text | centered, 80pt from top | `Montserrat SemiBold 22pt`, `#FFFFFF` |
| Photo | CircleImage | centered, 32pt below title | 160×160pt, border 3pt `#BB86FC` |
| Update Photo | TextButton | centered, 12pt below photo | icon `camera_alt` 18pt + `Roboto Medium 14pt`, `#BB86FC` |
| Name input | OutlinedTextField | horiz padded 24pt, 32pt below | pre-filled, editable, trailing edit icon |
| Flexible spacer | — | fills | pushes CTA down |
| Continue to Game | FilledButton | horiz padded 24pt | 52pt height, `#BB86FC` |
| Sign out | TextButton | centered, 16pt below | `Roboto Regular 12pt`, `#888` |
| Bottom safe area | — | 34pt | — |

### Behavior

- **Update Photo:** Opens camera (same viewfinder as S3, presented as modal sheet from bottom).
- **Continue to Game:** Save any changes → navigate to Screen 5.
- **Sign out:** Confirmation dialog → clear tokens → Screen 1.
- **Name field:** Tapping the edit icon or the field enables editing. Save on blur.

### Edge Cases

- **Photo failed to load (CDN error):** Show initials avatar with "Tap to reload" overlay.
- **Name changed to empty:** Show error "Name is required", revert to previous value.
- **Session code in deep link:** Show toast "Session code detected" and auto-advance to S5 after 1.5s.

---

## Screen 5: Join Session

### Purpose
Player joins a specific game session hosted on the iPad. Two input methods: manual code or QR scan.

### ASCII Wireframe — Path A: Code Entry (default)

```
┌──────────────────────────────┐
│         ▓ Status Bar ▓       │
│                              │
│  ←                           │
│                              │
│       Join a Session         │  ← 22pt Montserrat SemiBold
│                              │
│   ┌────────┐ ┌────────┐     │
│   │  Code  │ │  QR    │     │  ← SegmentedButton toggle
│   │ ██████ │ │        │     │    Code selected (filled)
│   └────────┘ └────────┘     │
│                              │
│   Enter the code shown       │
│   on the host iPad.          │  ← 14pt Roboto, #AAA
│                              │
│   ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐
│   │  │ │  │ │  │ │  │ │  │ │  │ │ ← 6 digit boxes
│   │ 4│ │ 2│ │ 8│ │  │ │  │ │  │ │   48×56pt each, 8pt gap
│   └──┘ └──┘ └──┘ └──┘ └──┘ └──┘ │   #1E1E1E bg, #BB86FC border on focus
│                              │      auto-advance on digit entry
│                              │
│                              │
│                              │
│                              │
│                              │
│                              │
│                              │
│  No session code?            │
│  Ask the host to share it.   │  ← 12pt, #888
│                              │
│  ┌──────────────────────────┐│
│  │         Join              ││  ← FilledButton, disabled until
│  └──────────────────────────┘│    6 digits entered
│                              │
│         ▓ Home Bar ▓         │
└──────────────────────────────┘
```

### ASCII Wireframe — Path B: QR Scan

```
┌──────────────────────────────┐
│         ▓ Status Bar ▓       │
│                              │
│  ←                           │
│                              │
│       Join a Session         │
│                              │
│   ┌────────┐ ┌────────┐     │
│   │  Code  │ │  QR    │     │  ← QR selected (filled)
│   │        │ │ ██████ │     │
│   └────────┘ └────────┘     │
│                              │
│   Point your camera at the   │
│   QR code on the host iPad.  │  ← 14pt Roboto, #AAA
│                              │
│  ┌──────────────────────────┐│
│  │                          ││
│  │    ┌──         ──┐       ││
│  │    │              │      ││  ← camera viewfinder
│  │    │   QR TARGET  │      ││    280×280pt
│  │    │   AREA       │      ││    corner brackets as overlay
│  │    │              │      ││    (#BB86FC corner lines)
│  │    └──         ──┘       ││
│  │                          ││
│  └──────────────────────────┘│
│                              │
│  No session code?            │
│  Ask the host to share it.   │
│                              │
│         ▓ Home Bar ▓         │
└──────────────────────────────┘
```

### Layout Spec

| Element | Type | Position | Style |
|---------|------|----------|-------|
| Back arrow | IconButton | top-left | → S3/S4 |
| Title | Text | centered | `Montserrat SemiBold 22pt` |
| Segment toggle | SegmentedButton | centered, 24pt below title | 2 segments: "Code" / "QR", `#BB86FC` selected, `#333` unselected, 40pt height |
| Instruction | Text | centered, 16pt below toggle | `Roboto Regular 14pt`, `#AAAAAA` |
| **Code path:** | | | |
| Digit boxes | 6× OTP InputField | centered row, 24pt below instruction | each 48w×56h pt, `#1E1E1E` bg, `#555` border, `#BB86FC` focus border, `Roboto Bold 28pt` `#FFFFFF` text, `inputType: number` |
| **QR path:** | | | |
| Camera view | CameraPreview | centered, 24pt below instruction | 280×280pt, `#000` bg, corner bracket overlay 4pt `#BB86FC` |
| Helper text | Text | 16pt above bottom button | `Roboto Regular 12pt`, `#888` |
| Join button | FilledButton | horiz padded 24pt (Code path only) | 52pt, `#BB86FC`, disabled until valid |
| Keyboard | System numeric | bottom (Code path) | auto-show on Code tab |

### Behavior

- **Code entry:** Auto-focus first box. Each digit typed → auto-advance to next box. Backspace → go back. On 6th digit → auto-submit (no need to press Join, but button available as fallback).
- **QR scan:** Camera auto-scans. On valid QR detection → haptic feedback (medium impact) → auto-join. QR contains URL: `locknscore://join?session=XXXXXX`.
- **Successful join:** Brief success animation (checkmark in center, 500ms) → navigate to Screen 6 (or S7 if permissions already granted).
- **Toggle animation:** Crossfade 200ms between Code and QR views.

### Error States

| Error | Trigger | Display | Recovery |
|-------|---------|---------|----------|
| Invalid code | API returns 404 | Shake animation on digit boxes + red text: "Invalid session code. Double check with the host." | Clear last 3 digits, focus 4th box |
| Expired session | API returns 410 | Modal: "This session has expired. Ask the host to start a new one." | OK → clear all digits |
| Session full | API returns 409 | Modal: "Session is full ({n}/{max} players). Try again if someone leaves." | OK → stay on screen |
| Network error | API timeout | Snackbar: "Connection failed. Tap to retry." | Snackbar action → retry last code |
| QR invalid format | QR decoded but not locknscore URL | Toast: "Not a LockN Score code. Try the manual code instead." | Continue scanning |
| Camera denied (QR) | No camera permission | Swap to Code tab, disable QR tab with tooltip: "Camera access required for QR scanning" | — |

---

## Screen 6: Camera & Mic Permissions

### Purpose
Explain why A/V permissions are needed before triggering iOS system dialogs. Reduces permission denial rate.

### ASCII Wireframe — State A: Pre-Permission Ask

```
┌──────────────────────────────┐
│         ▓ Status Bar ▓       │
│                              │
│                              │
│                              │
│                              │
│                              │
│          ┌────────┐          │
│          │  📹🎤  │          │  ← illustration/icon
│          │  64pt  │          │    Lottie animation preferred
│          └────────┘          │
│                              │
│    Camera & Microphone       │  ← 22pt Montserrat SemiBold
│        Access                │
│                              │
│   LockN Score streams your   │
│   gameplay to the main       │  ← 16pt Roboto, #AAAAAA
│   display. We need camera    │    centered, max 280pt width
│   and mic access to make     │
│   that happen.               │
│                              │
│                              │
│   📹 Camera — show your      │  ← feature list
│      game angle              │    14pt Roboto, #CCC
│                              │
│   🎤 Microphone — capture    │
│      game sounds             │
│                              │
│                              │
│  ┌──────────────────────────┐│
│  │     Enable Access         ││  ← FilledButton primary
│  └──────────────────────────┘│
│                              │
│       Maybe later            │  ← TextButton, #888
│                              │
│         ▓ Home Bar ▓         │
└──────────────────────────────┘
```

### ASCII Wireframe — State B: Permission Denied Recovery

```
┌──────────────────────────────┐
│         ▓ Status Bar ▓       │
│                              │
│                              │
│                              │
│                              │
│          ┌────────┐          │
│          │  ⚠️    │          │  ← warning icon, amber
│          └────────┘          │
│                              │
│   Permissions Required       │  ← 22pt Montserrat SemiBold
│                              │
│   LockN Score can't stream   │
│   without camera and mic     │  ← 16pt Roboto, #AAAAAA
│   access. Please enable      │
│   them in Settings.          │
│                              │
│   ┌────────────────────────┐ │
│   │ ☑ Camera     ✅ / ❌   │ │  ← permission checklist
│   │ ☑ Microphone ✅ / ❌   │ │    green check or red X
│   └────────────────────────┘ │
│                              │
│  ┌──────────────────────────┐│
│  │     Open Settings         ││  ← FilledButton primary
│  └──────────────────────────┘│
│                              │
│  ┌──────────────────────────┐│
│  │   Continue Without        ││  ← OutlinedButton (view-only)
│  └──────────────────────────┘│
│                              │
│         ▓ Home Bar ▓         │
└──────────────────────────────┘
```

### Layout Spec

| Element | Type | Position | Style |
|---------|------|----------|-------|
| Illustration | Lottie / Image | centered, 120pt from top | 120×120pt, `camera_mic_illustration` |
| Title | Text | centered, 24pt below | `Montserrat SemiBold 22pt`, `#FFFFFF` |
| Description | Text | centered, 12pt below title | `Roboto Regular 16pt`, `#AAAAAA`, max-width 280pt, line-height 24pt |
| Feature list | 2× Row | left-aligned 40pt inset, 24pt below desc | icon 20pt + `Roboto Regular 14pt`, `#CCCCCC` |
| Enable Access | FilledButton | horiz padded 24pt, 40pt below list | 52pt, `#BB86FC` |
| Maybe later | TextButton | centered, 12pt below | `Roboto Regular 14pt`, `#888` |

### Behavior

- **Enable Access:** Triggers iOS permission dialogs sequentially:
  1. Camera permission (`AVCaptureDevice.requestAccess(for: .video)`)
  2. On grant → Microphone permission (`AVCaptureDevice.requestAccess(for: .audio)`)
  3. Both granted → navigate to Screen 7
  4. Either denied → transition to State B (denied recovery)
- **Maybe later:** Navigate to Screen 7 in view-only mode (no stream). Show persistent banner on S7/S8: "Streaming disabled — enable in Settings."
- **Open Settings:** `UIApplication.open(URL(string: UIApplication.openSettingsURLString)!)` — deep links to app settings.
- **Return from Settings:** `sceneDidBecomeActive` → re-check permissions → update checklist → if both granted, auto-advance to S7.
- **Continue Without:** Proceed to S7 in view-only mode.

### Edge Cases

- **Permissions already granted (from S3 camera use):** Skip this screen entirely → go to S7.
- **Only camera granted (from profile photo):** Show screen but with camera pre-checked ✅. Only request mic.
- **iOS "Don't Allow" with "Ask Next Time":** Can re-prompt on next app launch. Store flag to not show pre-permission screen again.

---

## Screen 7: Stream Connection

### Purpose
Connect to the WebRTC session and confirm A/V is working before the game starts.

### ASCII Wireframe — State A: Connecting

```
┌──────────────────────────────┐
│         ▓ Status Bar ▓       │
│                              │
│  ←                           │
│                              │
│                              │
│                              │
│                              │
│         ┌──────────┐         │
│         │ CAMERA   │         │  ← 240×320pt camera PIP
│         │ PREVIEW  │         │    cornerRadius 16pt
│         │          │         │    border 2pt #333
│         │ (self)   │         │
│         │          │         │
│         └──────────┘         │
│                              │
│      ┌─┬─┬─┬─┬─┬─┬─┐        │  ← audio level meter
│      │▓│▓│▓│░│░│░│░│        │    7 bars, animated
│      └─┴─┴─┴─┴─┴─┴─┘        │    green → yellow → red
│                              │
│         ● Connecting...      │  ← pulsing dot + status text
│                              │  ← 16pt Roboto, #AAAAAA
│                              │
│                              │
│                              │
│                              │
│                              │
│                              │
│                              │
│         ▓ Home Bar ▓         │
└──────────────────────────────┘
```

### ASCII Wireframe — State B: Connected

```
┌──────────────────────────────┐
│         ▓ Status Bar ▓       │
│                              │
│  ←                           │
│                              │
│                              │
│                              │
│                              │
│         ┌──────────┐         │
│         │ CAMERA   │         │  ← same PIP, green border now
│         │ PREVIEW  │         │    border 2pt #4CAF50
│         │          │         │
│         │ (self)   │         │
│         │          │         │
│         └──────────┘         │
│                              │
│      ┌─┬─┬─┬─┬─┬─┬─┐        │  ← audio level active
│      │▓│▓│▓│▓│░│░│░│        │
│      └─┴─┴─┴─┴─┴─┴─┘        │
│                              │
│     ✅ Connected              │  ← green check + status
│                              │
│     Waiting for host         │  ← 14pt Roboto, #888
│     to start the game...     │    with animated ellipsis
│                              │
│                              │
│                              │
│                              │
│                              │
│         ▓ Home Bar ▓         │
└──────────────────────────────┘
```

### ASCII Wireframe — State C: Connection Error

```
┌──────────────────────────────┐
│         ▓ Status Bar ▓       │
│                              │
│  ←                           │
│                              │
│                              │
│                              │
│                              │
│         ┌──────────┐         │
│         │          │         │  ← black/frozen preview
│         │   ⚠️     │         │    with warning overlay
│         │          │         │
│         └──────────┘         │
│                              │
│                              │
│   Connection Failed          │  ← 20pt Montserrat SemiBold
│                              │    #CF6679 (error red)
│   Unable to connect to the   │
│   session. The host may have │  ← 14pt Roboto, #AAA
│   ended it, or your          │
│   connection dropped.        │
│                              │
│  ┌──────────────────────────┐│
│  │       Try Again           ││  ← FilledButton primary
│  └──────────────────────────┘│
│                              │
│     Return to Join Screen    │  ← TextButton → S5
│                              │
│         ▓ Home Bar ▓         │
└──────────────────────────────┘
```

### Layout Spec

| Element | Type | Position | Style |
|---------|------|----------|-------|
| Back arrow | IconButton | top-left | → S5 (with confirmation: "Leave session?") |
| Camera PIP | CameraPreview | centered, 80pt from top | 240×320pt, cornerRadius 16pt, border 2pt (`#333` connecting, `#4CAF50` connected) |
| Audio meter | Custom 7-bar widget | centered, 16pt below PIP | each bar 8w×24h, 4pt gap, gradient: bars 1-3 `#4CAF50`, 4-5 `#FFC107`, 6-7 `#F44336` |
| Status indicator | Dot + Text | centered, 24pt below meter | 8pt dot (pulsing amber connecting / static green connected) + `Roboto Medium 16pt` |
| Subtitle | Text | centered, 8pt below status | `Roboto Regular 14pt`, `#888` |

### Behavior

- **Connecting state:** Immediately begin WebRTC signaling. Pulsing amber dot. Camera preview active but border is neutral gray. Audio meter shows levels (confirms mic working even before connection completes).
- **Connected state:** Border turns green. Status updates. After 1 second hold at "Connected", auto-transition to Screen 8.
- **Connection timeout (10s):** Transition to error state.
- **Try Again:** Re-initiate WebRTC connection. Return to connecting state.
- **Return to Join Screen:** Tear down connection → navigate to S5.
- **Back arrow (←):** Show alert: "Leave this session?" / "Stay" / "Leave" → if leave, tear down → S5.

### Edge Cases

- **Camera disabled (view-only mode):** Show placeholder with user's profile photo instead of camera preview. Hide audio meter. Show banner: "View-only mode — streaming disabled."
- **Poor connection:** Show quality indicator (1-3 bars) in top-right of PIP. If quality drops below threshold, show inline warning: "Weak connection — video may be choppy."
- **Host ends session while connecting:** Error state with message: "Session ended by host." Single button: "OK" → S5.
- **App backgrounded during connection:** Maintain connection for 30s, then tear down. On foreground, if torn down, show reconnecting state.

---

## Screen 8: Ready State

### Purpose
Final holding screen. Player confirms they're ready. Waits for host to start the game.

### ASCII Wireframe

```
┌──────────────────────────────┐
│         ▓ Status Bar ▓       │
│                              │
│  ←                           │
│                              │
│                              │
│        🎉 You're In!         │  ← 24pt Montserrat Bold
│                              │    with confetti Lottie (1s)
│                              │
│       ┌──────────────┐       │
│       │              │       │
│       │   PLAYER     │       │  ← 96×96pt circular photo
│       │   PHOTO      │       │    border 3pt #4CAF50
│       │              │       │
│       └──────────────┘       │
│         Sean Murphy          │  ← 18pt Roboto Medium
│                              │
│  ┌──────────────────────────┐│
│  │  Session: Table 3        ││  ← info card
│  │  Mode: Singles            ││    #1E1E1E bg, cornerRadius 12
│  │  Players: 2/2 ✅          ││    padding 16pt
│  │                          ││
│  │  👤 Sean M.    ● Ready   ││  ← player list
│  │  👤 Alex T.    ○ Waiting ││    green dot = ready
│  └──────────────────────────┘│
│                              │
│  ┌──────────────────────────┐│
│  │    ● I'm Ready            ││  ← Toggle button
│  └──────────────────────────┘│    Off: outlined, "I'm Ready"
│                              │    On: filled green #4CAF50,
│     Waiting for host...      │        "Ready ✅"
│     ◠ ◡ ◠                   │  ← animated dots
│                              │
│         ▓ Home Bar ▓         │
└──────────────────────────────┘
```

### ASCII Wireframe — Ready Toggled ON

```
         (same layout, button changes:)

│  ┌──────────────────────────┐│
│  │    ✅ Ready!              ││  ← filled #4CAF50
│  └──────────────────────────┘│    white text
│                              │
│     Waiting for host         │
│     to start the game...     │
```

### Layout Spec

| Element | Type | Position | Style |
|---------|------|----------|-------|
| Back arrow | IconButton | top-left | "Leave session?" confirm → S5 |
| Celebration text | Text | centered, 80pt from top | `Montserrat Bold 24pt`, `#FFFFFF` |
| Confetti | Lottie overlay | full screen, plays once | `confetti.json`, 1200ms |
| Player photo | CircleImage | centered, 24pt below text | 96×96pt, border 3pt `#4CAF50` |
| Player name | Text | centered, 8pt below photo | `Roboto Medium 18pt`, `#FFFFFF` |
| Session card | Card | horiz padded 24pt, 24pt below name | `#1E1E1E` bg, cornerRadius 12pt, padding 16pt |
| Card — Session | Text | inside card, top | `Roboto Regular 14pt`, `#888` label + `#FFF` value |
| Card — Mode | Text | 8pt below | same |
| Card — Players | Text | 8pt below | count + status indicator |
| Card — Player list | List | 12pt below, divider above | avatar 24pt + name + status dot |
| Ready button | ToggleButton | horiz padded 24pt, 24pt below card | **Off:** outlined, 52pt, border `#4CAF50`, icon `○`, label "I'm Ready" `#4CAF50`. **On:** filled `#4CAF50`, icon `✅`, label "Ready!" `#FFFFFF` |
| Waiting text | Text | centered, 12pt below button | `Roboto Regular 14pt`, `#888`, animated ellipsis |
| Loading dots | Custom | centered, 4pt below | 3 dots, phase-offset pulse animation |

### Behavior

- **I'm Ready (toggle):** Sends `player.ready` event to session. Button transitions to filled green. Reversible — tap again to un-ready.
- **All players ready + host starts:** Screen transitions to game view (out of scope for this spec). Transition: zoom-in on camera PIP → full-screen game view.
- **Player list updates:** Real-time via WebSocket. Players joining/leaving animate in/out (slide + fade, 300ms).
- **Back arrow:** Confirm dialog → leave session → S5. Sends `player.leave` event.

### Edge Cases

- **Host ends session:** Modal: "The host ended this session." / "OK" → S1.
- **Network disconnect:** Show reconnecting overlay on screen (semi-transparent `#121212CC` with spinner). Auto-reconnect for 15s. If fails, transition to S7 error state.
- **Player kicked by host:** Modal: "You've been removed from this session." / "OK" → S5.
- **Long wait (>5min):** Subtle pulse animation on "Waiting for host" to indicate app is alive. Screen does NOT auto-lock (use `UIApplication.shared.isIdleTimerDisabled = true`).
- **Only player in session:** Player list shows just self. Waiting text: "Waiting for other players to join..."

---

## Global Design Tokens

### Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `surface` | `#121212` | Screen backgrounds |
| `surface-variant` | `#1E1E1E` | Cards, input backgrounds |
| `primary` | `#BB86FC` | CTAs, focus borders, accents |
| `primary-variant` | `#9C64FF` | Pressed state |
| `on-primary` | `#121212` | Text on primary buttons |
| `on-surface` | `#FFFFFF` | Primary text |
| `on-surface-medium` | `#AAAAAA` | Secondary text |
| `on-surface-disabled` | `#666666` | Disabled text |
| `error` | `#CF6679` | Error states |
| `success` | `#4CAF50` | Connected, ready, confirmed |
| `warning` | `#FFC107` | Caution states |
| `outline` | `#333333` | Default borders |

### Typography Scale

| Style | Font | Size | Weight | Tracking |
|-------|------|------|--------|----------|
| H1 (screen title) | Montserrat | 24pt | Bold (700) | 0 |
| H2 (section title) | Montserrat | 22pt | SemiBold (600) | 0 |
| Body1 | Roboto | 16pt | Regular (400) | 0.5pt |
| Body2 | Roboto | 14pt | Regular (400) | 0.25pt |
| Button | Roboto | 16pt | Medium (500) | 1.25pt |
| Caption | Roboto | 12pt | Regular (400) | 0.4pt |
| OTP Digit | Roboto | 28pt | Bold (700) | 0 |

### Component Specs

| Component | Height | Corner Radius | Padding |
|-----------|--------|---------------|---------|
| FilledButton | 52pt | 26pt (pill) | horiz 24pt |
| OutlinedButton | 52pt | 26pt (pill) | horiz 24pt |
| TextButton | 40pt (tap target) | — | horiz 8pt |
| TextField | 56pt | 12pt | horiz 16pt |
| Card | auto | 12pt | 16pt all |
| SegmentedButton | 40pt | 20pt | horiz 16pt each |
| OTP digit box | 56pt | 8pt | centered |

### Transitions

| From → To | Animation | Duration | Easing |
|-----------|-----------|----------|--------|
| S1 → S2 | Slide right (push) | 350ms | ease-out |
| S2 → S3/S4 | Fade + slide up | 400ms | decelerate |
| S3/S4 → S5 | Slide right | 350ms | ease-out |
| S5 → S6 | Slide right | 350ms | ease-out |
| S6 → S7 | Fade crossfade | 300ms | ease-in-out |
| S7 → S8 | Zoom in from PIP | 500ms | spring(damping: 0.8) |
| Back navigation | Slide left (pop) | 300ms | ease-out |
| Error modal | Slide up from bottom | 350ms | decelerate |
| Bottom sheet | Slide up + dim bg | 300ms | decelerate |

---

## Accessibility Notes

- All interactive elements: min 44×44pt tap target
- Color contrast: all text meets WCAG AA on `#121212` background
- VoiceOver labels for all buttons, inputs, status indicators
- Camera preview: `accessibilityLabel = "Camera preview showing your face"`
- Audio meter: `accessibilityValue = "Microphone level: moderate"`
- Ready toggle: `accessibilityTraits = .toggleButton`, value = on/off
- Reduce Motion: Replace Lottie animations with static states; replace transitions with crossfades

---

## Figma Handoff Notes

1. **Create 8 frames** at 390×844 (iPhone 14) with `#121212` background
2. **Component library:** Build shared components first — FilledButton, OutlinedButton, TextField, Card, SegmentedButton, CircleImage, StatusDot, AudioMeter
3. **Auto Layout:** All screens should use vertical auto-layout for responsive spacing
4. **Variants:** Create button variants (default, pressed, disabled) and input variants (default, focused, error, filled)
5. **Prototyping:** Wire S1→S2→S3→S5→S6→S7→S8 as primary happy path
6. **States:** Use Figma component properties to toggle between screen states (e.g., S7 connecting vs connected vs error)
7. **Assets needed:** Logo mark SVG, confetti Lottie, camera/mic illustration, app icon
