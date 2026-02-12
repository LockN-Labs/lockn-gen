# Journey 1: Session Creation Flow (iPad/Dashboard)

## Overview
Host-side flow for creating ping pong scoring sessions on iPad in landscape orientation. This journey covers home/landing, game mode selection, settings configuration, and waiting room for player joins.

**Target Device**: iPad (Landscape)  
**Viewport**: 1024×768px (iPad Air), scalable to 1366×1024px (iPad Pro)  
**User Role**: Host/Referee (typically coach or tournament organizer)  
**Duration**: ~30 seconds from start to waiting room

## Screen Flow
```
Home/Landing → Mode Selection → Game Settings → Waiting Room → (Ready to Start)
```

## Screen 1: Home/Landing Dashboard

### Layout Specifications
**Dimensions**: 1024×768px  
**Grid**: 12-column responsive grid, 24px gutters  
**Safe Areas**: 24px margins on all sides

### Header Section (1024×80px)
- **Position**: Top, fixed
- **Background**: `--surface-2` (#232323)
- **Elevation**: `--elevation-2`
- **Content**:
  - **Logo**: LockN Score wordmark (160×32px) - left aligned, 24px from edge
  - **User Menu**: Avatar (40×40px) + dropdown - right aligned, 24px from edge
  - **Connection Status**: WiFi/network indicator - right aligned, 80px from edge

### Hero Section (1024×400px)
- **Position**: Below header, centered
- **Background**: `--surface` (#121212) with subtle gradient
- **Content**:
  - **Main Headline**: "Ready to Play?" 
    - Typography: `--headline-large` (32px/40px, weight 400)
    - Color: `--text-primary` (#FFFFFF)
    - Position: Centered, 120px from top
  - **Subtitle**: "Create a new ping pong scoring session"
    - Typography: `--body-large` (16px/24px)
    - Color: `--text-secondary` (#B3B3B3)
    - Position: 24px below headline
  - **Primary CTA**: "New Game" button
    - Dimensions: 200×56px
    - Background: `--primary` (#1976D2)
    - Text: `--label-large` (14px/20px, weight 500), white
    - Border Radius: `--radius-md` (12px)
    - Position: 40px below subtitle
    - Hover State: `--primary-dark` (#1565C0)
    - Active State: Scale 0.98x, brief animation

### Recent Games Section (1024×288px)
- **Position**: Below hero, full width
- **Background**: `--surface-1` (#1E1E1E)
- **Elevation**: `--elevation-1`
- **Padding**: 32px
- **Content**:
  - **Section Title**: "Recent Games"
    - Typography: `--title-large` (22px/28px, weight 500)
    - Color: `--text-primary`
  - **Game Cards**: Horizontal scrolling list
    - **Card Dimensions**: 280×120px each
    - **Spacing**: 16px between cards
    - **Background**: `--surface-2` (#232323)
    - **Border Radius**: `--radius-md` (12px)
    - **Card Content**:
      - **Date/Time**: `--body-small` (12px/16px), top-right
      - **Players**: Name pairs, `--body-medium` (14px/20px)
      - **Final Score**: Large numbers, `--headline-small` (24px/32px)
      - **Duration**: Small label, `--label-small` (11px/16px)

### States & Variants

#### Loading State
- **Hero Section**: Skeleton placeholders for headline and button
- **Recent Games**: Skeleton cards with shimmer animation
- **Duration**: Show for 0.5-1.5 seconds on initial load

#### Empty State (No Recent Games)
- **Illustration**: Ping pong paddle icon (64×64px)
- **Message**: "No games yet – create your first session!"
- **Typography**: `--body-large`, `--text-secondary`
- **CTA**: "Get Started" button redirects to mode selection

#### Error State (Network/API Issues)  
- **Alert Bar**: Top of screen, `--error` background
- **Message**: "Connection error. Please check your network."
- **Retry Button**: Small button to reload data
- **Fallback**: Show cached recent games if available

## Screen 2: Mode Selection

### Layout Specifications
**Dimensions**: 1024×768px  
**Transition**: Slide left from home (300ms ease-out)
**Background**: `--surface` (#121212)

### Header Section (1024×80px)
- **Back Button**: Left arrow icon (24×24px) + "Back" label
  - Position: 24px from left edge
  - Color: `--primary` (#1976D2)
  - Touch Target: 48×48px minimum
- **Title**: "Select Game Mode"
  - Typography: `--title-large` (22px/28px, weight 500)
  - Color: `--text-primary`
  - Position: Centered horizontally

### Mode Cards Section (1024×608px)
- **Layout**: 3-column grid, centered
- **Grid Spacing**: 40px gaps between cards
- **Card Container**: 920×400px (allows for 3×280px cards + gaps)

#### Solo Practice Card (280×400px)
- **Background**: `--surface-1` (#1E1E1E)
- **Border**: 2px solid transparent (4px `--primary` when selected)
- **Elevation**: `--elevation-1` (higher on hover)
- **Border Radius**: `--radius-lg` (16px)
- **Content**:
  - **Icon**: Single paddle icon (80×80px), centered, 40px from top
  - **Title**: "Solo Practice"
    - Typography: `--headline-small` (24px/32px, weight 400)
    - Position: 24px below icon
  - **Description**: "Track your practice sessions and improve your technique"
    - Typography: `--body-medium` (14px/20px)
    - Color: `--text-secondary`
    - Position: 16px below title
    - Max width: 240px (centered)
  - **Features List**: 
    - "Rally counter"
    - "Technique analysis"
    - "Progress tracking"
    - Typography: `--body-small` (12px/16px)
    - Color: `--text-secondary`
    - Position: 24px below description

#### Rally Mode Card (280×400px) 
- **Layout**: Same structure as Solo Practice
- **Icon**: Two paddles crossed (80×80px)
- **Title**: "Rally Mode"
- **Description**: "Count rallies without keeping game score"
- **Features**:
  - "Rally counting"
  - "Longest rally tracking"
  - "Endurance challenges"

#### Full Game Card (280×400px)
- **Layout**: Same structure as Solo Practice  
- **Icon**: Scoreboard icon (80×80px)
- **Title**: "Full Game"
- **Description**: "Complete ping pong match with official scoring"
- **Features**:
  - "Official scoring rules"
  - "Set tracking"  
  - "Tournament mode"
- **Recommended Badge**: Small pill at top-right
  - Background: `--primary` (#1976D2)
  - Text: "Recommended", `--label-small`
  - Border Radius: `--radius-full`

### Interaction States
- **Default**: `--surface-1` background, `--elevation-1`
- **Hover**: `--surface-2` background, `--elevation-2`, smooth transition (200ms)
- **Selected**: `--primary` border (4px), slight glow effect
- **Disabled**: 50% opacity, no hover effects

### Continue Section (1024×80px)
- **Position**: Bottom, fixed
- **Background**: `--surface-2` with top border
- **Continue Button**: 
  - Dimensions: 160×48px
  - Position: Right aligned, 24px from edges
  - Disabled until mode selected
  - Text: "Continue" → "Continue with [Mode Name]"

## Screen 3: Game Settings

### Layout Specifications  
**Dimensions**: 1024×768px
**Background**: `--surface` (#121212)
**Transition**: Slide left from mode selection (300ms)

### Header Section (1024×80px)
- **Back Button**: Returns to mode selection
- **Title**: "Game Settings" or "[Selected Mode] Settings"
- **Layout**: Same as Mode Selection header

### Settings Panel (680×608px)
- **Position**: Centered horizontally, 32px from header
- **Background**: `--surface-1` (#1E1E1E)
- **Elevation**: `--elevation-1`
- **Border Radius**: `--radius-lg` (16px)
- **Padding**: 40px

#### Points to Win Section
- **Label**: "Points to Win"
  - Typography: `--title-medium` (16px/24px, weight 500)
- **Options**: Radio button group
  - Values: 11, 15, 21 (official), 25
  - Layout: Horizontal, 40px spacing
  - Selection Style: `--primary` fill, white checkmark
  - Labels: `--body-large` (16px/24px)

#### Serve Rules Section (32px margin-top)
- **Label**: "Serve Rules"
- **Options**: Radio button group
  - "Every 2 points" (standard)
  - "Every 5 points" 
  - "Each game"
- **Layout**: Vertical stack, 16px spacing

#### Match Format Section (32px margin-top)
- **Label**: "Match Format"
- **Toggle**: Best of 3 / Best of 5 / Single Game
- **Component**: Segmented control
  - Dimensions: 300×40px
  - Background: `--surface-2`
  - Active: `--primary` background
  - Border Radius: `--radius-sm` (8px)

#### Advanced Settings (Collapsible)
- **Trigger**: "Advanced Settings" with chevron down
- **Content** (when expanded):
  - **Deuce Rule**: Enable/disable deuce play
  - **Timeout**: Allow timeouts (toggle + count)
  - **Video Recording**: Auto-record highlights
  - **AI Coaching**: Enable post-game insights

#### Preview Card (320×200px)
- **Position**: Right side of settings panel
- **Background**: `--surface-2`
- **Content**: Live preview of selected settings
  - Mock scoreboard showing format
  - "Player 1 vs Player 2" placeholder
  - Example: "First to 21 • Best of 3 • Serve every 2"

### Action Buttons (1024×80px)
- **Position**: Bottom, full width
- **Background**: `--surface-2` with top border  
- **Buttons**:
  - **Cancel**: Text button, left side
  - **Create Session**: Primary button, right side
    - Dimensions: 180×48px
    - Background: `--primary`
    - Text: "Create Session"
    - Loading state: Spinner + "Creating..."

### Validation & Error States
- **Missing Required**: Red outline on incomplete sections
- **Invalid Combinations**: Warning message below conflicting settings
- **Network Error**: Toast notification at top

## Screen 4: Waiting Room

### Layout Specifications
**Dimensions**: 1024×768px  
**Background**: `--surface` (#121212)
**Transition**: Slide left from settings (300ms)

### Header Section (1024×80px)
- **Session Status**: "Session Created" with checkmark icon
- **Actions**: Settings gear (edit game settings) + Close session X
- **Layout**: Title left, actions right

### Main Content Grid (1024×608px)
**Layout**: 2-column grid (512px each)

#### Left Column: Join Information (512×608px)
- **Session Code Card** (480×200px)
  - **Background**: `--surface-1`, `--elevation-2`
  - **Border Radius**: `--radius-lg` (16px)
  - **Content**:
    - **Label**: "Session Code"
    - **Code Display**: Large format (6-digit code)
      - Typography: `--display-small` (36px/44px, monospace)
      - Background: `--surface-2`, `--radius-md` (12px)
      - Letter spacing: 4px
    - **Copy Button**: Icon button next to code
    - **Instructions**: "Players enter this code to join"

- **QR Code Card** (480×240px, 24px margin-top)
  - **QR Code**: 160×160px, centered
  - **Background**: White square with `--radius-md`
  - **Label**: "Or scan QR code"
  - **Share Button**: "Share QR" button below

- **Connection Status** (480×144px, 24px margin-top)
  - **WiFi Info**: Network name and signal strength
  - **Device Count**: "iPad connected"
  - **Stream Status**: "Ready to receive player streams"

#### Right Column: Players Panel (512×608px)
- **Players List** (480×400px)
  - **Header**: "Joined Players (0/4)" 
  - **Empty State**: 
    - Illustration: Waiting icon
    - Text: "Waiting for players to join..."
    - Subtext: "Share the session code or QR code"
  - **Player Cards** (when players join):
    - Dimensions: 480×80px each
    - **Content**: Avatar, name, connection status, stream indicator
    - **Layout**: Stack vertically, 16px spacing

- **Game Preview** (480×184px, 24px margin-top)
  - **Settings Summary**: Selected game mode, points, format
  - **Estimated Duration**: Based on settings
  - **Start Button**: Disabled until minimum players joined
    - Text: "Start Game" (or "Waiting for Players...")
    - Dimensions: 200×56px
    - Background: `--primary` (enabled) or `--surface-3` (disabled)

### Real-Time Updates
- **Player Joins**: Slide-in animation for new player cards
- **Connection Status**: Real-time status indicators (green=connected, yellow=connecting, red=disconnected)
- **Stream Status**: Camera icons showing active video streams
- **Sound Effects**: Soft notification sounds for player joins

### States & Interactions

#### Loading State (Creating Session)
- **Overlay**: Semi-transparent background
- **Spinner**: Centered with "Creating session..." text
- **Duration**: 1-3 seconds typical

#### Player Join Animation
- **Entry**: New player card slides in from right
- **Highlight**: Brief blue glow around new card
- **Counter Update**: Animate player count change
- **Sound**: Subtle notification chime

#### Connection Issues
- **Warning**: Yellow alert bar at top
- **Message**: "Connectivity issues detected"
- **Actions**: Refresh connection, check network
- **Auto-retry**: Background reconnection attempts

#### Start Game Conditions
- **Minimum Players**: At least 2 players for Full Game
- **Stream Status**: All players must have active streams
- **Button State**: 
  - Disabled: Gray background, "Waiting for X more players"
  - Enabled: Primary color, "Start Game (X players ready)"

### Responsive Considerations (iPad Pro 12.9")
- **Scale Factor**: 1.33x for 1366×1024px displays
- **QR Code**: Increase to 200×200px
- **Session Code**: Larger typography (48px/56px)
- **Player Cards**: Wider layout (640×100px)
- **Grid Spacing**: Increase gutters to 40px

### Accessibility Features
- **High Contrast**: Alternative color scheme support
- **Large Text**: Respect system text size preferences  
- **Voice Control**: All buttons accessible via voice commands
- **Screen Reader**: Proper ARIA labels for dynamic content
- **Keyboard Navigation**: Tab order for settings and buttons

### Performance Requirements
- **WebSocket Connection**: Maintain real-time player status
- **QR Generation**: Instant generation, high contrast
- **Video Preview**: Low-latency stream thumbnails
- **Battery Optimization**: Reduce CPU usage during waiting

## Handoff Notes for Implementation

### Technical Requirements
- **Real-Time Communication**: WebSocket integration for live updates
- **QR Code Generation**: Use QRCode.js or similar library  
- **Deep Linking**: Support app://join/{session-code} URLs
- **State Management**: Redux/Context for session state
- **Responsive Layout**: CSS Grid with breakpoint adjustments

### API Integration Points
- `POST /sessions/create` - Create new session
- `GET /sessions/{id}` - Get session details
- `WS /sessions/{id}/live` - Real-time updates
- `POST /sessions/{id}/start` - Start the game

### Asset Requirements
- **Icons**: Game mode icons (SVG, 80×80px base)
- **Illustrations**: Empty state graphics
- **Sound Files**: Notification sounds (MP3, <100kb)
- **QR Code Styling**: Custom styling for generated QR codes

### Testing Scenarios
- **Multi-device**: Test with 2-4 simultaneous iPhone connections
- **Network Issues**: Test with poor WiFi, disconnections
- **Edge Cases**: Test with duplicate players, invalid codes
- **Performance**: Test session creation speed, memory usage

This Journey 1 specification provides complete detail for implementing the iPad dashboard session creation flow, ensuring a smooth host experience from game setup to player management.