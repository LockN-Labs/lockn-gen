# LockN Score - Spectator Dashboard (Journey 3)

## Screen Overview
**Screen Type:** Live iPad dashboard with real-time updates  
**App:** LockN Score  
**Journey:** Journey 3 - Live Dashboard iPad (scores, serve indicator, rally count, PIP video)  
**Route:** `/spectator` or `/spectator/:sessionId`  
**Component:** `pages/SpectatorDashboard.tsx`

## Layout Description

### Container Structure
- **Background:** Deep dark blue `#04060d` 
- **Layout:** Full viewport height, no scrolling
- **Max Width:** 1600px centered
- **Padding:** 16px (lg: 24px)
- **Text Color:** Light slate-100

### Grid Layout Structure
```
┌─────────────────────────────────────┐
│            Header Bar               │
├─────────────────────────────────────┤
│         Main Score Display          │
├─────────────────┬───────────────────┤
│   Rally Tracker │    PIP Feeds      │
├─────────────────┴───────────────────┤
│         Game Progress               │
├─────────────────────────────────────┤
│         Match History               │
└─────────────────────────────────────┘
```

### Responsive Grid
- **Desktop:** `lg:grid-cols-[0.95fr_1.05fr]` for rally/PIP section
- **Tablet:** Stacked layout
- **Mobile:** Single column flow

## Header Section

### Layout
- **Container:** Rounded 2xl, dark background `slate-950/70`, white/10 border
- **Padding:** 12px × 16px
- **Height:** Auto, flex justify-between

### Left Side Content
- **App Label:** "LockN Score • Spectator View" (11px uppercase, tight tracking, slate-400)
- **Session Info:** "Session [8-char ID]" or "Waiting for active session" (14px, slate-300)

### Right Side Content
- **Game Badge:** Rounded pill
  - Background: `cyan-400/10`
  - Border: `cyan-300/30`
  - Text: "Game X of 3" (12px uppercase, tracked, cyan-200)

## Main Score Display Section

### Component: ScoreDisplay
Large prominent score area for real-time match scores

#### Visual Structure
- **Container:** Full-width, major visual element
- **Player Areas:** Left and right player zones
- **Center Area:** Serve indicator and divider
- **Score Typography:** Very large, bold numbers
- **Player Names:** "Player 1" / "Player 2" labels

#### Score Elements
- **Score Numbers:** Prominent display (likely 48px+ font size)
- **Server Indicator:** Visual marker showing who serves
- **Player Zones:** Color-coded areas (differentiated styling)

### Real-time Updates
- **WebSocket Connected:** Live score updates
- **Animation:** Smooth transitions on score changes
- **Server Changes:** Visual indicator animations

## Rally Tracker Section

### Component: RallyTracker
Displays current rally count and rally statistics

#### Content Elements
- **Current Rally:** Live rally count during active play
- **Longest Rally:** Session/match best rally count
- **Rally History:** Recent rally lengths (last 10 rallies)
- **Visual Progress:** Charts or progress indicators

#### Layout
- **Container:** Rounded corners, border, dark background
- **Typography:** Mixed sizing - large numbers, smaller labels
- **History Display:** Horizontal or vertical list of recent rallies

### States
- **Active Rally:** Current count updating in real-time
- **Rally Complete:** Shows final count, updates longest
- **History Updates:** New rallies slide into list
- **Empty State:** Waiting for rallies to begin

## PIP (Picture-in-Picture) Feeds Section

### Component: PIPFeeds
Multiple camera feeds in picture-in-picture layout

#### Feed Structure
```typescript
interface CameraFeed {
  id: string
  label: string  
  frameDataUrl?: string
}
```

#### Layout
- **Grid:** Multiple camera views
- **Default Feeds:** "Camera 1", "Camera 2"
- **Video Frames:** Live JPEG frames via WebSocket
- **Labels:** Camera identification text

#### Feed Display
- **Aspect Ratio:** Maintained for video content
- **Frame Updates:** Real-time via base64 data URLs
- **Placeholder State:** When no video available
- **Quality:** Optimized for live streaming

### Real-time Features
- **Frame Rate:** Depends on WebSocket push frequency
- **Format:** JPEG frames as data URLs
- **Fallback:** Placeholder when video unavailable
- **Multiple Feeds:** Up to 2 concurrent feeds

## Game Progress Section

### Visual Layout
- **Container:** Rounded 22px, dark background `slate-900/65`
- **Header:** "Game Progress" with "Best of 3" indicator
- **Grid:** 3 columns for games (sm:grid-cols-3)

### Game Cards
Each of 3 games represented by cards:

#### Completed Game State
- **Background:** `lime-300/10` with `lime-300/35` border
- **Content:** Final score display (e.g., "21 - 17")
- **Text Color:** White for completed scores

#### Current Game State
- **Background:** `cyan-300/10` with `cyan-300/35` border
- **Content:** "In progress" text
- **Indicator:** Visual current game marker

#### Pending Game State
- **Background:** `slate-950/60` with `white/10` border
- **Content:** "Pending" text
- **Text Color:** Muted slate-500

### Data Structure
```typescript
interface CompletedGame {
  gameNumber: number
  player1: number
  player2: number
  winner: 1 | 2
}
```

## Match History Section

### Layout
- **Container:** Rounded 20px, fuchsia-tinted border and background
- **Background:** `slate-950/75`
- **Header:** "Match history" (10px uppercase, tracked)

### Event Display
- **Empty State:** "Waiting for events…" placeholder
- **Event Tags:** Rounded pills with event descriptions
- **Styling:** Cyan-tinted pills with cyan text
- **Layout:** Flex wrap for responsive tag flow

### Event Types
- "Session started"
- "Point: X-Y" (score updates)
- "Game complete: X-Y" (final scores)

### Recent Events
- **Limit:** Last 12 events displayed
- **Order:** Most recent first
- **Animation:** New events slide in from top

## Component States

### Connection States

#### Connected State
- **Indicators:** Live data flowing
- **Updates:** Real-time score/rally updates
- **Video:** Active camera feeds
- **Status:** All systems operational

#### Disconnected State
- **Fallback:** Polling API every 2.2 seconds
- **Video:** Static placeholder frames
- **Scores:** Last known state
- **Indicators:** Connection status warnings

#### Loading State
- **Scores:** Skeleton/placeholder numbers
- **Video:** Loading placeholders
- **Events:** Empty or skeleton states

### Game States

#### Pre-Game State
- **Scores:** 0-0 display
- **Progress:** All games pending
- **History:** "Waiting for events"
- **Rally:** No active rallies

#### Active Game State
- **Scores:** Live updating
- **Progress:** Current game highlighted
- **Rally:** Live counts
- **Video:** Active feeds

#### Game Complete State
- **Scores:** Final game scores
- **Progress:** Game marked complete
- **History:** Game completion event
- **Transition:** Next game setup

#### Match Complete State
- **All Games:** Completed status
- **Final Display:** Match winner indication
- **History:** Complete match summary

### Error States
- **Network Error:** Retry mechanisms
- **Session Error:** Invalid session handling
- **Video Error:** Camera feed fallbacks
- **Data Error:** Graceful degradation

## Responsive Behavior

### iPad Landscape (Primary Target)
- **Orientation:** Auto-fullscreen on landscape iPad
- **Touch Points:** Optimized for larger touch targets
- **Grid Layout:** Full two-column rally/PIP layout
- **Typography:** Large, readable from viewing distance

### Desktop (1200px+)
- **Layout:** Full grid layout maintained
- **Mouse Interaction:** Hover states where applicable
- **Scaling:** Optimal for large displays

### Tablet Portrait (768px - 1199px)
- **Rally/PIP:** Stacked sections
- **Scores:** Slightly smaller scaling
- **Navigation:** Touch-optimized

### Mobile (< 768px)
- **Layout:** Single column flow
- **Scores:** Compact but readable
- **Video:** Single feed priority
- **Text:** Compressed sizing

## Text Content

### Headers & Labels
- "LockN Score • Spectator View" (app identifier)
- "Session [ID]" / "Waiting for active session"
- "Game X of 3" (progress indicator)
- "Game Progress", "Match History" (section headers)

### Player Labels
- "Player 1", "Player 2" (default names)
- Server indicators and labels

### Status Messages
- "In progress", "Pending" (game states)
- "Waiting for events…" (empty state)
- Connection status indicators

### Event Descriptions
- "Session started"
- "Point: X-Y"
- "Game complete: X-Y"

## Interaction Flows

### Primary Usage (Passive Spectating)
1. User accesses spectator view (via QR/link)
2. Screen auto-enters fullscreen (iPad)
3. Live data begins flowing
4. Real-time updates throughout match
5. Match completion and final state

### Session Connection
- **Direct Link:** `/spectator/:sessionId` immediately connects
- **Auto Discovery:** `/spectator` waits for active session
- **Reconnection:** Handles session switches gracefully

### Fullscreen Behavior
```javascript
// Auto-fullscreen logic for iPad landscape
const touch = navigator.maxTouchPoints > 0
const isLandscape = window.matchMedia("(orientation: landscape)").matches
if (touch && isLandscape) {
  await document.documentElement.requestFullscreen()
}
```

## Transitions & Animations

### Score Updates
- **Number Changes:** Smooth transitions on score updates
- **Server Changes:** Animated server indicator movement
- **Point Celebrations:** Brief highlight effects

### Rally Updates
- **Count Changes:** Live number updates
- **History Addition:** New rallies slide into view
- **Record Breaking:** Special effects for longest rally

### Game Progress
- **State Changes:** Card background transitions
- **Completion:** Game cards animate to complete state
- **Progress Flow:** Visual progression through games

### Video Feeds
- **Frame Updates:** Smooth frame replacement
- **Feed Switching:** Transition between camera angles
- **Error Recovery:** Graceful fallback to placeholders

## Technical Notes

### Real-time Data Flow

#### WebSocket Integration
- **Primary Connection:** Real-time score/rally updates
- **Video Streaming:** JPEG frame pushes
- **Event Broadcasting:** Match events and status

#### Fallback Polling
- **Interval:** Every 2.2 seconds
- **Purpose:** Backup when WebSocket unavailable
- **API Endpoint:** `GET /api/session/:sessionId`

### Data Management

#### Score State
```typescript
interface ScoreState {
  p1: number
  p2: number  
  server: 1 | 2
}
```

#### Rally State
```typescript
interface RallyState {
  current: number
  longest: number
  history: number[]
}
```

### Performance Optimization
- **Frame Rate:** Optimized video frame updates
- **Memory Management:** Limited event history
- **Re-renders:** Efficient state updates
- **Connection Management:** Robust WebSocket handling

### Platform Considerations
- **iPad Safari:** Fullscreen API compatibility
- **Touch Events:** Optimized for touch interaction
- **Orientation:** Landscape preference for spectating
- **Performance:** Smooth 60fps updates target

## Related Components
- `ScoreDisplay` - Main score visualization
- `RallyTracker` - Rally count and statistics
- `PIPFeeds` - Picture-in-picture video feeds
- `useWebSocket` - Real-time connection management