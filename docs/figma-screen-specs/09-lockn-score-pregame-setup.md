# LockN Score - Pre-Game Setup

## Screen Overview
**Screen Type:** Device preparation and connection verification  
**App:** LockN Score  
**Journey:** Pre-game camera/microphone setup and session connection  
**Route:** `/pregame` with session parameter  
**Component:** `pages/PreGame.tsx`

## Layout Description

### Container Structure
- **Background:** Design system background color (dark theme)
- **Padding:** 16px horizontal, 24px vertical
- **Max Width:** 384px (max-w-sm) centered
- **Animation:** Framer Motion initial fade-up

### Overall Layout Hierarchy
```
┌─────────────────────────────────────┐
│            Header Info              │
├─────────────────────────────────────┤
│         Camera Preview              │
├─────────────────────────────────────┤
│      Device Permissions             │
├─────────────────────────────────────┤
│      Connection Status              │
├─────────────────────────────────────┤
│         Error Display               │
├─────────────────────────────────────┤
│         Ready Button                │
├─────────────────────────────────────┤
│         Back Action                 │
└─────────────────────────────────────┘
```

## Header Section

### Layout
- **Alignment:** Text center
- **Title:** "Pre-Game Setup" (24px font-bold, primary text color)
- **Session Info:** "Session: [6-char ID]" (14px, secondary text color)

### Session ID Display
- **Format:** First 6 characters of session ID, uppercase
- **Purpose:** Quick session identification for players
- **Styling:** Smaller, muted text color

## Camera Preview Section

### Component Integration
- **Component:** `<StreamPreview>` with custom props
- **Aspect Ratio:** 4:3 (aspect-[4/3])
- **Width:** Full container width
- **Animation:** Scale and opacity entrance (delay 0.2s)

### StreamPreview Props
```typescript
<StreamPreview
  onStreamReady={handleStreamReady}
  onError={handleStreamError}
  className="aspect-[4/3] w-full"
/>
```

### Stream States
- **Loading:** Camera initialization
- **Active:** Live video preview
- **Error:** Error message display
- **Permission Denied:** Fallback state

## Device Permissions Section

### Container
- **Background:** Surface color from design system
- **Border:** Rounded 2xl with subtle border
- **Border Color:** Tertiary text color with 20% opacity
- **Padding:** 16px
- **Animation:** Fade up with 0.4s delay

### Header
- **Title:** "Device Permissions" (14px font-semibold, primary text)
- **Layout:** Section header above permission list

### Permission Items
Two main permissions tracked:

#### 1. Camera Permission
- **Icon:** Camera SVG (20px × 20px)
- **Name:** "Camera" (capitalized)
- **Description:** "Camera access for video streaming"
- **Status Indicator:** Color-coded status dot

#### 2. Microphone Permission
- **Icon:** Microphone SVG (20px × 20px)  
- **Name:** "Microphone" (capitalized)
- **Description:** "Microphone access for voice communication"
- **Status Indicator:** Color-coded status dot

### Permission Layout
Each permission item:
- **Layout:** Flex row with 12px gaps
- **Icon:** Colored based on status
- **Content:** Name and description stacked
- **Status:** Right-aligned with dot and text

### Status Colors (from design system)
```typescript
const getPermissionColor = (status: string) => {
  switch (status) {
    case 'granted': return colors.connected
    case 'denied': return colors.error  
    case 'prompt': return colors.connecting
    case 'checking': return colors.textTertiary
  }
}
```

### Status Animation
- **Checking State:** Pulsing scale animation (1 → 1.2 → 1)
- **Duration:** 1 second, infinite repeat
- **Status Dot:** 8px × 8px rounded full

## Connection Status Section

### Container
- **Styling:** Identical to permissions section
- **Animation:** Fade up with 0.6s delay

### Connection States
- **Connecting:** "Connecting to game session..."
- **Connected:** "Connected to session" 
- **Ready:** "Ready to start"
- **Failed:** "Failed to connect to session"

### Status Display
- **Layout:** Flex row with icon, content, loading indicator
- **Icon:** 12px × 12px status dot with color coding
- **Animation:** Connecting state shows pulsing dot
- **Loading Spinner:** Rotating border animation when connecting

### Connection Colors
```typescript
const getConnectionColor = () => {
  switch (connection.status) {
    case 'connected':
    case 'ready': return colors.connected
    case 'connecting': return colors.connecting
    case 'failed': return colors.error
  }
}
```

## Error Display Section

### Conditional Rendering
- **Display:** Only shown when `streamError` exists
- **Animation:** Slide in from left (-10px x offset)

### Error Container
- **Background:** Error color with 10% opacity
- **Border:** Error color with 30% opacity, rounded 2xl
- **Padding:** 16px

### Error Content
- **Icon:** Warning SVG (20px × 20px, error color)
- **Title:** "Camera/Microphone Error" (14px font-medium, error color)
- **Message:** Specific error text (12px, error color)
- **Layout:** Flex with icon and text content

## Ready Button Section

### Component Integration
- **Component:** `<ReadyButton>` with state management
- **Width:** Full container width
- **Animation:** Fade up with 0.8s delay

### ReadyButton Props
```typescript
<ReadyButton
  onReady={handleReady}
  onCancel={handleCancel}
  disabled={!canStart}
  className="w-full"
/>
```

### Ready State Logic
```typescript
const allPermissionsGranted = permissions.every(p => p.status === 'granted')
const canStart = allPermissionsGranted && connection.status === 'ready' && !streamError
```

### Helper Text
Conditional help text based on state:
- **Permissions Issue:** "Grant camera and microphone permissions to continue"
- **Connection Issue:** "Waiting for connection to be established"
- **Stream Error:** "Fix camera/microphone issues to continue"
- **Generic:** "Please wait..."

#### Help Text Styling
- **Layout:** Centered text, margin-top 12px
- **Font:** 12px
- **Color:** Tertiary text color from design system
- **Animation:** Fade in with 1s delay

## Back Navigation Section

### Layout
- **Container:** Text-center, padding-top 8px
- **Button:** Text link style

### Back Button
- **Text:** "← Leave Session"
- **Action:** Navigate to `/join` route
- **Styling:** 14px font-medium, secondary text color
- **Hover:** Color transitions

## Component States

### Initial Loading State
- **Permissions:** "checking" status for all permissions
- **Connection:** "connecting" with loading animations
- **Camera:** Attempting stream access
- **Ready Button:** Disabled

### Permissions Granted State
- **Permissions:** All show "granted" status with success colors
- **Stream:** Active video preview
- **Connection:** Progresses through connection flow
- **Ready Button:** Enabled when all conditions met

### Permissions Denied State
- **Permissions:** Show "denied" status with error colors
- **Stream Error:** Displays specific error message
- **Ready Button:** Disabled
- **Help Text:** Guidance for permission resolution

### Connection Failed State
- **Connection:** Shows "failed" status with error color
- **Ready Button:** Disabled
- **Behavior:** May include retry mechanisms

### Ready State
- **All Systems:** Green/success status
- **Ready Button:** Enabled and prominent
- **User Action:** Can proceed to game start

## Responsive Behavior

### Mobile Portrait (Primary Target)
- **Container:** Max width 384px, centered
- **Camera Preview:** 4:3 aspect ratio maintained
- **Touch:** Optimized for mobile interaction
- **Typography:** Mobile-appropriate sizing

### Tablet/Desktop
- **Layout:** Maintains centered mobile-style layout
- **Scaling:** Appropriate scaling for larger screens
- **Interaction:** Mouse/keyboard friendly

## Text Content

### Headers & Labels
- "Pre-Game Setup" (main title)
- "Session: [ID]" (session identifier)
- "Device Permissions" (section header)
- "Game Connection" (connection section)

### Permission Names & Descriptions
- "Camera" - "Camera access for video streaming"
- "Microphone" - "Microphone access for voice communication"

### Status Messages
- Permission states: "Checking...", "Granted", "Denied", "Prompt"
- Connection states: Various connection status messages
- Error messages: Camera/microphone specific errors
- Help text: Guidance based on current state

### Actions
- "← Leave Session" (back navigation)
- Ready button text (from ReadyButton component)

## Interaction Flows

### Successful Setup Flow
1. User lands on pre-game setup with session ID
2. Permissions automatically checked
3. Camera preview activates (permission granted)
4. Connection to session established
5. All systems show "ready" state
6. User clicks ready button to join game

### Permission Denied Flow
1. User denies camera/microphone permissions
2. Error message displays with guidance
3. User must manually allow permissions in browser
4. Page refresh or retry mechanism activates stream

### Connection Failed Flow
1. Session connection fails
2. Error status displayed
3. Potential retry mechanisms
4. User may need to rejoin session

### Leave Session Flow
1. User clicks "← Leave Session"
2. Navigates back to join screen
3. Session connection cleaned up

## Transitions & Animations

### Page Entry
- **Initial:** Fade up from 20px below
- **Staggered:** Sections appear with increasing delays
- **Duration:** Smooth entrance animations

### Permission Updates
- **Status Changes:** Color transitions on permission status
- **Checking Animation:** Pulsing dots during permission checks
- **Success:** Smooth transitions to success states

### Connection Updates
- **Loading:** Rotating spinner during connection
- **Status Changes:** Color-coded status transitions
- **Completion:** Success animations when ready

### Error States
- **Error Appearance:** Slide in from left
- **Error Resolution:** Fade out when resolved
- **Visual Feedback:** Clear error state indication

## Technical Notes

### Permission API Integration
- **Query API:** `navigator.permissions.query()`
- **Fallback:** getUserMedia for permission status
- **Error Handling:** Graceful fallback when API unavailable

### Stream Management
- **MediaStream:** Direct camera/microphone access
- **Error Handling:** Permission denied, hardware issues
- **Cleanup:** Proper stream disposal on component unmount

### Session Management
- **URL Parameters:** Session ID from search params
- **Connection:** WebSocket or polling connection to session
- **State Sync:** Real-time session state updates

### Design System Integration
- **Color Tokens:** Consistent with app design system
- **Typography:** Inherited from design system
- **Spacing:** Design system spacing scales
- **Animation:** Consistent with app motion language

## Related Components
- `StreamPreview` - Camera preview functionality
- `ReadyButton` - Ready state management and UI
- Session connection management
- Permission handling utilities
- Design system color tokens and utilities