# Auth + Onboarding Specs (LockN Score)

Source references: `web/src/auth/*`, `web/src/pages/PlayerRegistration.tsx`, `web/src/pages/PreGame.tsx`, route flow in `web/src/App.tsx`.

## Flow Map
1. Protected route hit (`/register`, `/join`, `/pregame`)
2. Auth required prompt
3. Player profile registration
4. Photo capture/update
5. Pre-game permission + stream readiness

---

## Screen A1 — Auth Required Gate

### Frame
- Mobile: 390×844
- Card centered: 358×220 at (x:16, y:220)

### Content
- Title: `Sign in required`
- Body: `Please log in to register your player profile.`
- CTA: `Log in`

### Component usage
- Surface card: border white/10, bg slate-900/70
- Primary button uses neon token (`#4DD0E1`) with dark text

### States
- Loading auth check: `Loading...`
- Error auth provider: `Authentication unavailable. Try again.`
- Success redirect to return route

### Interaction
- Button triggers `loginWithRedirect({ appState: { returnTo: '/register' } })`

---

## Screen A2 — Player Registration (Name)

### Frame (mobile)
- Screen: 390×844
- Profile card: 358×320 at (16, 100)

### Layout
- Eyebrow: `Player Profile`
- H1: `Register to play`
- Body: `Quick setup for match tracking and score history.`
- Label: `Display name`
- Input: placeholder `Your name`
- CTA: `Create Profile`

### States
- Loading submit: button `Registering...`
- Empty validation: `Please enter your name.`
- API error: show amber text from backend detail
- Success: transition to photo step or welcome-back state

### Interaction
- POST `/api/players/register`

---

## Screen A3 — Returning Player (Welcome Back)

### Frame
- Card height reduced to 280

### Content
- Heading: `Welcome back {player.name}`
- Avatar 112×112 centered
- Button: `Update Photo`

### States
- No photo URL → fallback Auth0 avatar
- Update clicked → enters photo-capture mode

---

## Screen A4 — Photo Capture

### Frame
- Camera block: 358×320 at y: 420
- Capture preview image after shot: 358×288
- Actions row: two 173×48 buttons

### Content
- H2: `Capture your photo`
- Body: `Use your front camera for a quick player badge image.`
- Actions: `Retake`, `Use This Photo`

### States
- Camera loading
- Permission denied
- Uploading: `Uploading...`
- Upload success: navigate home
- Upload error: backend detail text

### Interaction
- Upload endpoint: `POST /api/players/{id}/photo`

---

## Screen A5 — Pre-Game Readiness

### Frame
- Mobile container max width: 384
- Sections stacked with 24px gaps

### Layout coordinates (390×844)
1. Header block at y: 32, h: 70
   - Title: `Pre-Game Setup`
   - Subtitle: `Session: {id}`
2. Stream preview at y: 126, size 358×268 (4:3)
3. Permissions card at y: 414, size 358×188
4. Connection card at y: 616, size 358×94
5. Ready CTA at y: 724, size 358×56
6. Leave link at y: 792

### Permissions module
- Camera row + mic row with status dot
- Status values: `checking`, `prompt`, `granted`, `denied`

### Connection module
- States:
  - `connecting` → animated spinner + yellow dot
  - `connected`
  - `ready`
  - `failed`

### Ready button
- Enabled when all permissions granted, connection ready, no stream error
- Disabled helper copy:
  - `Grant camera and microphone permissions to continue`
  - `Waiting for connection to be established`
  - `Fix camera/microphone issues to continue`

### Error state
- Card title: `Camera/Microphone Error`
- Body: stream error detail

### Success state
- Button enters ready mode (`onReady`), host sees ready status

---

## Breakpoints
- **Mobile (<=767)**: single-column as above
- **Tablet (768-1023)**: center column max 520, larger preview (16:9 optional)
- **Desktop (>=1024)**: two-column onboarding (left instructions, right interactive card)

## Motion Specs
- Page enter: opacity 0→1, y +20→0 (220ms)
- Card stagger delay: 120ms increments
- Status pulse (checking/connecting): 1s loop

## Figma Build Notes
- Create reusable components:
  - `AuthGateCard`
  - `ProfileFormCard`
  - `PermissionRow`
  - `ConnectionStatusCard`
  - `ReadyButton`
- Map status colors from tokens:
  - granted `#69F0AE`
  - connecting `#FFD54F`
  - error `#FF5252`
