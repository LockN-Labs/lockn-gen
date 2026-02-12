# LockN Score - Session Creation (Journey 1)

## Screen Overview
**Screen Type:** Multi-step form wizard  
**App:** LockN Score  
**Journey:** Journey 1 - Host creates game, selects mode, waiting room  
**Route:** `/create`  
**Component:** `pages/SessionCreate.tsx`

## Layout Description

### Container Structure
- **Outer Container:** Rounded 3xl container, dark background `#121620`, white/10 border
- **Padding:** 24px (lg: 32px)
- **Text Color:** `#ECEFF1` (light slate)
- **Min Height:** 420px for content area

### Header Section
- **Layout:** Flex justify-between, items-center
- **Left Side:**
  - Label: "Session setup" (12px uppercase, tight tracking, slate-400)
  - Title: "Create New Session" (24px semibold)
- **Right Side:**
  - Back link: "← Dashboard" (14px medium, slate-300, hover white)

### Progress Indicator
- **Layout:** Flex row with gaps
- **Items:** 3 progress steps (Mode, Settings, Lobby)
- **Visual:** 
  - Progress bar: 64px width × 10px height, rounded full
  - Active: `#4DD0E1` (cyan), Inactive: `white/10`
  - Label: 12px text, slate-400

### Content Area
- **Container:** Min height 420px, overflow hidden
- **Animation:** Framer Motion slide transitions
  - Enter: opacity 0, x ±72px
  - Center: opacity 1, x 0
  - Exit: opacity 0, x ∓72px
  - Duration: 0.26s ease-out

### Navigation Footer
- **Layout:** Flex justify-between, items-center
- **Left:** Back button (disabled on step 0)
- **Right:** Continue/Start Session button
- **Button Styles:**
  - Back: Border button, white/15 border, slate-300 text
  - Continue: Cyan background `#4DD0E1`, dark text, bold font
  - Start: Emerald-400 background, very dark green text

## Step 1: Mode Selection

### Layout
- **Title:** "Select game mode" (18px font-semibold)
- **Grid:** 3 columns on large screens (`lg:grid-cols-3`)
- **Gap:** 16px between cards

### Mode Cards (ModeCard component)
Each mode card contains:
- **Icon Area:** 24px × 24px SVG icons
- **Title:** Mode name (font-semibold)
- **Description:** Mode explanation text
- **Selection State:** Visual feedback for active selection

### Mode Options
1. **Solo Practice**
   - Icon: Arrow with line (left-right movement)
   - Description: "Train consistency with streak tracking and shot rhythm analytics"
   
2. **Rally Challenge**  
   - Icon: Square with cross lines
   - Description: "Track longest exchanges with collaborative or competitive rally play"
   
3. **Full Game**
   - Icon: Three horizontal lines
   - Description: "Run regulation scoring with set tracking and lobby invites"

## Step 2: Game Settings

### Layout
- **Title:** "Configure game settings" (18px font-semibold, margin-bottom 16px)
- **Component:** `GameSettings` form component

### Settings Interface (GameSettings)
Form controls for:
- **Points to Win:** Numeric input/selector
- **Serve Rule:** Dropdown/radio group ("alternate-2" format)
- **Best of Sets:** Numeric selector (default: 3)

### Form Styling
- Consistent with app design system
- Focus states with cyan accents
- Proper label associations
- Validation feedback

## Step 3: Waiting Lobby

### Layout
- **Header:** Flex justify-between
  - Title: "Waiting lobby" (18px font-semibold)  
  - Mode Badge: Rounded pill, cyan background/15 opacity, cyan text

### Content (WaitingLobby component)
Split into two sections:

#### Session Code Panel (Left)
- **Background:** `#1C2130` rounded container
- **Code Display:** 
  - Label: "Session code" (12px uppercase, tracked, slate-400)
  - Code: 60px mono font, bold, cyan color, letter-spaced
- **QR Code Area:**
  - Dashed border container
  - Placeholder: 180px max-width, aspect-square
  - Background: `#121620`

#### Players Panel (Right) 
- **Background:** `#1C2130` rounded container
- **Header:** Players count badge
- **Player List:** Animated cards with Framer Motion
  - Enter animation: opacity 0 → 1, x 20 → 0, scale 0.98 → 1
  - Duration: 0.22s
  - Exit animation: opacity 1 → 0, x 0 → -20

### Player Cards
Each player entry:
- **Layout:** Flex justify-between, rounded container
- **Background:** `black/20` with white/10 border
- **Avatar:** 40px circle, cyan/20 background, emoji
- **Info:** Name + "Joined [time]" timestamp
- **Status:** "Connected" label (emerald-300)

## Component States

### Step 1 States
- **Loading:** Skeleton mode cards
- **Selection:** One mode highlighted, others dimmed
- **Validation:** Continue disabled until selection made

### Step 2 States  
- **Loading:** Form skeleton
- **Validation:** Real-time form validation
- **Error:** Field-level error messages
- **Success:** Valid configuration confirmed

### Step 3 States
- **Waiting:** No players, empty state message
- **Populating:** Players joining with animations
- **Ready:** Minimum players met, start enabled
- **Starting:** Loading state on session start

## Responsive Behavior

### Desktop (1200px+)
- Full 3-column mode selection
- Side-by-side lobby panels
- Large text and spacing

### Tablet (768px - 1199px)
- 2-column mode grid
- Stacked lobby sections
- Medium spacing

### Mobile (< 768px)
- Single column throughout
- Full-width elements
- Touch-friendly sizing
- Reduced text sizes

## Text Content

### Headers
- "Session setup" (progress label)
- "Create New Session" (main title)
- Step titles: "Select game mode", "Configure game settings", "Waiting lobby"

### Mode Descriptions
- Solo: "Train consistency with streak tracking and shot rhythm analytics"
- Rally: "Track longest exchanges with collaborative or competitive rally play" 
- Full: "Run regulation scoring with set tracking and lobby invites"

### Form Labels
- Points to Win, Serve Rule, Best of Sets
- Session Code display
- Player status indicators

### Button Labels
- "Back", "Continue", "Start Session"

## Interaction Flows

### Primary Flow (Happy Path)
1. User lands on mode selection
2. Selects desired game mode (highlights selection)
3. Clicks "Continue" → Settings step
4. Configures game parameters
5. Clicks "Continue" → Lobby step
6. Waits for players to join (real-time updates)
7. Clicks "Start Session" → Game begins

### Back Navigation
- Any step can go back (except step 0)
- Preserves previous selections
- Smooth slide-left animation

### Form Validation
- Mode selection required for step 1
- Settings validation before proceeding
- Live feedback on form fields

### Real-time Updates
- Player join events in lobby
- Session code generation
- QR code display
- Connection status updates

## Transitions & Animations

### Step Transitions
- Slide animations between steps
- Direction-aware (left/right based on navigation)
- Smooth easing curves
- Preserved scroll position

### Player Joins
- Slide-in from right
- Bounce/scale animation
- Status updates with color changes
- Exit animations for disconnects

### Loading States
- Skeleton animations
- Button loading spinners  
- Form field pulse effects
- Progressive disclosure

## Technical Notes

### State Management
- Multi-step form state
- Session configuration object
- Player list with real-time updates
- Navigation history preservation

### WebSocket Integration
- Real-time player updates
- Session status events
- Connection monitoring
- Error handling

### Validation Schema
```typescript
interface SessionSettings {
  pointsToWin: number
  serveRule: string
  bestOfSets: number
}
```

### Performance Optimization
- Debounced form inputs
- Memoized expensive computations
- Lazy component loading
- Efficient re-renders

## Related Components
- `ModeCard` - Selection cards for game modes
- `GameSettings` - Form controls for configuration  
- `WaitingLobby` - Real-time player management
- Shared animation and styling utilities