# Journey 3: Live Dashboard (iPad - Game Active)

## Overview
The hero screen of LockN Score: real-time scoring dashboard during active ping pong games. Optimized for iPad landscape viewing with emphasis on score visibility at distance and seamless integration of computer vision tracking.

**Target Device**: iPad (Landscape)  
**Viewport**: 1024×768px (iPad Air) to 1366×1024px (iPad Pro 12.9")  
**User Role**: Host, referee, spectators  
**Viewing Distance**: 2-6 feet from device  
**Context**: Investor demo hero screen, tournament displays

## Design Principles

### Visual Hierarchy
1. **Score** - Dominant, readable from 6+ feet
2. **Player Identity** - Clear association with scores
3. **Game State** - Serve, rally, special conditions
4. **Auxiliary Info** - Stats, time, settings

### Readability Requirements
- **Score Numbers**: Visible from 6 feet (minimum 120px height)
- **Player Names**: Readable from 4 feet (minimum 28px height)  
- **Game State**: Clear indicators, high contrast
- **Real-time Updates**: <200ms latency for score changes

## Main Dashboard Screen

### Layout Specifications
**Dimensions**: 1024×768px  
**Grid System**: Custom layout optimized for score prominence  
**Color Scheme**: Dark mode for reduced eye strain, high contrast ratios  
**Update Frequency**: 60fps smooth animations, real-time WebSocket updates

### Header Bar (1024×60px)
- **Position**: Top, semi-transparent overlay
- **Background**: `rgba(18, 18, 18, 0.9)` with backdrop blur
- **Content**:
  - **Session Info** (left):
    - Session Code: "ABC123" format, `--label-medium` (12px/16px)
    - Game Mode: "Full Game • Best of 3", `--label-small` (11px/16px)
    - Color: `--text-secondary` (#B3B3B3)
  - **Time & Status** (center):
    - Game Timer: "12:34" elapsed time, `--label-large` (14px/20px)  
    - Status: "Set 1 • In Progress", `--label-medium`
    - Color: `--text-primary` (#FFFFFF)
  - **Controls** (right):
    - Settings gear icon (24×24px)
    - Fullscreen toggle icon (24×24px)
    - End game icon (24×24px)
    - Color: `--text-secondary`, hover: `--primary`

### Player 1 Section (480×648px)
**Position**: Left half of screen, 32px from left edge

#### Player 1 Identity Card (480×140px)
- **Background**: `--surface-1` (#1E1E1E) with `--radius-lg` (16px)
- **Elevation**: `--elevation-2`
- **Layout**: Horizontal flex layout
- **Content**:
  - **Avatar** (100×100px):
    - Position: 20px from left, vertically centered
    - Border Radius: `--radius-full` (50%)
    - Border: 4px solid `--score-player-1` (#4CAF50) when serving
    - Fallback: Initials on `--surface-3` background
  - **Player Info** (300×100px):
    - **Name**: "Player 1" 
      - Typography: `--headline-small` (24px/32px, weight 400)
      - Color: `--text-primary`
      - Position: 20px left of avatar
    - **Serve Indicator** (when active):
      - "Serving" pill badge
      - Background: `--serve-indicator` (#FF9800)
      - Typography: `--label-small` (11px/16px, weight 500)
      - Border Radius: `--radius-full`
      - Position: Below name, animated entrance
    - **Connection Status**:
      - Stream indicator: Green dot + "Live" or "Offline"
      - Position: Bottom right of card
      - Typography: `--body-small` (12px/16px)

#### Player 1 Score Display (480×300px)
- **Position**: 20px below identity card
- **Background**: Transparent (score emphasis)
- **Content**:
  - **Current Score**: 
    - Typography: `--display-large` (114px/128px, weight 300)
    - Color: `--score-player-1` (#4CAF50)
    - Position: Centered horizontally
    - Font: Roboto Mono for consistent digit width
    - Animation: Scale pulse on score change (1.1x for 200ms)
  - **Set Scores** (below main score):
    - **Layout**: Horizontal row of set indicators
    - **Set Indicators**: 40×40px circles
    - **Won Sets**: Filled `--score-player-1` background  
    - **Current Set**: Outlined `--score-player-1` border
    - **Future Sets**: `--surface-3` background
    - **Typography**: `--title-medium` (16px/24px, weight 500)
    - **Spacing**: 12px between indicators

#### Player 1 Stats Panel (480×188px)
- **Position**: Below score display, 20px margin-top
- **Background**: `--surface-1` with `--radius-md` (12px)
- **Padding**: 20px
- **Content**:
  - **Rally Count**: 
    - Label: "Rallies Won", `--body-small`
    - Value: "12", `--title-large` (22px/28px, weight 500)
    - Color: `--score-player-1`
  - **Best Rally**:
    - Label: "Longest Rally", `--body-small`  
    - Value: "23 hits", `--title-medium` (16px/24px)
  - **Serve Accuracy** (if tracking enabled):
    - Label: "Serve Accuracy", `--body-small`
    - Value: "78%", `--title-medium`
    - Visual: Small progress bar

### Center Section (64×648px)
**Position**: Between player sections, 32px margins on each side

#### VS Indicator (64×80px)  
- **Position**: Top center, aligned with identity cards
- **Content**: "VS" text
  - Typography: `--headline-medium` (28px/36px, weight 400)
  - Color: `--text-disabled` (#666666)
  - Position: Centered

#### Rally Counter (64×200px)
- **Position**: Center of screen, below VS indicator
- **Background**: `--surface-2` (#232323) with `--radius-lg`
- **Content**:
  - **Label**: "Rally"
    - Typography: `--label-large` (14px/20px, weight 500)
    - Color: `--text-secondary`
    - Position: Top center
  - **Count**: Live rally count
    - Typography: `--display-medium` (45px/52px, weight 400)
    - Color: `--primary` (#1976D2)
    - Position: Center, below label
    - Animation: Increment with bounce effect
  - **Ball Indicator**: 
    - Small ping pong ball icon (20×20px)
    - Color: `--primary`
    - Animation: Bounces on detected hits

#### Game State Badge (64×60px)
- **Position**: Below rally counter, 32px margin-top
- **Background**: Dynamic based on game state
- **Border Radius**: `--radius-lg` (16px)
- **Content**: Context-dependent
  - **Normal Play**: Hidden
  - **Deuce**: "DEUCE" on `--warning` (#FF9800) background
  - **Game Point**: "GAME POINT" on `--error` (#F44336)
  - **Match Point**: "MATCH POINT" on `--error` with pulse animation
  - **Set Point**: "SET POINT" on `--info` (#2196F3)
- **Typography**: `--label-large` (14px/20px, weight 500), white text

### Player 2 Section (480×648px)
**Position**: Right half of screen, 32px from right edge  
**Layout**: Mirror of Player 1 section

#### Player 2 Identity Card (480×140px)
- **Same layout as Player 1**
- **Serve Border**: `--score-player-2` (#2196F3) when serving
- **Avatar Position**: Right-aligned (20px from right edge)
- **Player Info**: Right-aligned text

#### Player 2 Score Display (480×300px)  
- **Same structure as Player 1**
- **Score Color**: `--score-player-2` (#2196F3)
- **Set Indicators**: Right-aligned layout

#### Player 2 Stats Panel (480×188px)
- **Same layout as Player 1**  
- **Accent Color**: `--score-player-2`

### Optional: Picture-in-Picture Video (PIP)

#### PIP Layout Mode (when enabled)
- **Player 1 Video**: 240×180px, top-right of Player 1 section
- **Player 2 Video**: 240×180px, top-left of Player 2 section  
- **Background**: `--surface-2` with `--radius-md`
- **Overlay**: Player name label, connection status
- **Controls**: Minimize, maximize, mute icons
- **Position Adjustment**: Stats panels reduce in height (120px)

#### PIP Controls
- **Toggle**: "Show/Hide Video" in header settings
- **Fullscreen**: Double-tap video to expand
- **Audio**: Mute/unmute individual streams
- **Layout**: Switch between PIP and fullscreen video modes

## Real-Time Updates & Animations

### Score Change Animation
1. **Detection**: Ball bounce detected by computer vision
2. **Validation**: Audio correlation confirms valid point (200ms window)  
3. **Score Update**: Number changes with scale animation
4. **Visual Feedback**: 
   - Winning player's score pulses green (1.1x scale, 300ms)
   - Serve indicator may switch players
   - Rally counter resets to 0 with fade effect
5. **Audio Feedback**: Soft "ding" sound for score changes

### Rally Counter Animation  
- **Increment**: Count increases with bounce effect (scale 1.2x, 150ms)
- **Ball Bounce**: Ping pong ball icon bounces vertically
- **Color Change**: Text color intensifies with longer rallies
  - 1-5 hits: `--primary`
  - 6-15 hits: `--info` 
  - 16+ hits: `--warning` (impressive rally!)

### Serve Indicator Transition
- **Animation**: Slide and fade between players (400ms ease-out)
- **Avatar Border**: Animated border appears/disappears  
- **Badge**: "Serving" pill slides in below player name
- **Timing**: Triggered by serve rules (every 2/5 points, etc.)

### Game State Transitions
- **Badge Entrance**: Slide up from center with elastic animation
- **Critical States**: Pulse animation for match point scenarios
- **Color Coding**: Consistent color language for different states
- **Auto-Hide**: Normal play states auto-hide after 3 seconds

## Interactive Elements

### Touch/Click Areas
- **Player Cards**: Tap to edit player info/photo
- **Score Areas**: Tap to manual adjust (admin mode only)
- **Rally Counter**: Tap to reset (with confirmation)
- **Header Controls**: Access settings, fullscreen, end game

### Settings Overlay (triggered from header)
**Dimensions**: 400×500px modal overlay  
**Background**: `--surface-1` with backdrop blur
**Content**:
- **Display Options**:
  - Toggle PIP video feeds
  - Adjust score size (for different viewing distances)
  - Change color themes (accessibility)
- **Audio Settings**:
  - Mute/unmute system sounds
  - Adjust volume levels
  - Toggle audio analysis feedback
- **Game Settings**:
  - Manual score correction
  - Pause/resume game timer
  - End game confirmation

### Fullscreen Mode
- **Trigger**: Fullscreen button or double-tap
- **Changes**: Hide header bar, maximize score visibility
- **Exit**: Swipe down from top or ESC key
- **Use Case**: Public displays, tournament screens

## States & Error Handling

### Connection States

#### All Players Connected (Normal State)
- **Visual**: Green connection indicators on player cards
- **Performance**: Smooth real-time updates, <200ms latency
- **Features**: Full functionality including video streams

#### Player Disconnected
- **Visual**: Red connection indicator, "Offline" status
- **Impact**: Video stream shows "Connection Lost" overlay
- **Behavior**: Continue game with remaining players
- **Recovery**: Auto-reconnect when player returns

#### Network Issues  
- **Visual**: Orange warning banner at top
- **Message**: "Network issues detected - some features may be delayed"
- **Graceful Degradation**: 
  - Prioritize score updates over video
  - Cache recent state for offline resilience  
  - Show last known good state with timestamp

#### Server Disconnection
- **Visual**: Red error banner covering header
- **Message**: "Server connection lost - attempting to reconnect"
- **Behavior**: 
  - Freeze current game state
  - Show reconnection countdown
  - Offer manual reconnect button
- **Data**: Preserve game state locally for recovery

### Game Flow States

#### Pre-Game (Players Joining)
- **Scores**: Show "0" with low opacity
- **Rally Counter**: "Ready" instead of number
- **Game State**: "Waiting for players" badge
- **Animation**: Subtle pulse on empty player slots

#### Game in Progress (Active State)  
- **Primary state as described above**
- **Real-time updates**: All systems active
- **Interactions**: Full functionality available

#### Game Paused
- **Visual**: Semi-transparent overlay with "PAUSED" text
- **Scores**: Maintain last known state
- **Rally Counter**: Paused at current value
- **Controls**: "Resume" button in center, settings accessible

#### Set Complete
- **Animation**: Winning player's section briefly highlights green
- **Score Reset**: Current scores reset to 0-0 for next set  
- **Set Indicators**: Update with animation
- **Transition**: 3-second countdown to next set

#### Game Complete
- **Transition**: Fade to Post-Game Recap screen (Journey 4)
- **Winner Animation**: Winning player's section expands briefly
- **Final State**: Preserve final score for 2 seconds before transition

### Error Recovery

#### Computer Vision Failure
- **Fallback**: Manual score entry mode
- **Visual**: Warning indicator on rally counter
- **Message**: "Auto-scoring unavailable - manual mode active"
- **Recovery**: Background retry attempts, auto-restore when fixed

#### Audio Processing Error  
- **Impact**: Rally counting may be less accurate
- **Visual**: Microphone icon with warning indicator
- **Behavior**: Continue with vision-only detection
- **User Control**: Option to disable audio analysis

#### Sync Issues Between Devices
- **Detection**: Compare timestamps and score states
- **Resolution**: Use authoritative server state  
- **Visual**: Brief "Syncing..." indicator
- **Prevention**: Heartbeat monitoring, conflict resolution

## Responsive Layout (iPad Pro 12.9")

### Scale Adjustments for 1366×1024px
- **Overall Scale**: 1.33x proportional scaling
- **Score Typography**: `--display-large` becomes 152px/170px
- **Player Sections**: Increase to 640×864px each
- **Center Section**: Increase to 86×864px  
- **Spacing**: Proportional increases (32px → 43px margins)
- **Touch Targets**: Maintain minimum sizes, increase spacing

### Orientation Considerations
- **Primary**: Landscape orientation locked
- **Temporary Portrait**: Show "Rotate device" message
- **Brief Rotation**: Maintain current state, resume on return
- **Accessibility**: Support orientation lock override if needed

## Accessibility Features

### Visual Accessibility  
- **High Contrast Mode**: Alternative color scheme with higher contrast ratios
- **Large Text Support**: Scale all typography proportionally with system settings
- **Color Blindness**: Alternative indicators beyond color (shapes, patterns)
- **Reduce Motion**: Disable animations if system preference set

### Motor Accessibility
- **Touch Targets**: All interactive elements minimum 44×44px
- **Voice Control**: Full support for voice commands ("show settings", "end game")
- **Switch Control**: External switch support for all functions
- **Hover States**: Clear indication of interactive elements

### Cognitive Accessibility
- **Clear Hierarchy**: Strong visual hierarchy for information priority  
- **Consistent Layout**: Stable element positions throughout game
- **Error Prevention**: Confirmation dialogs for destructive actions
- **Status Indicators**: Always-visible connection and game state

## Performance Requirements

### Frame Rate & Responsiveness
- **Display**: Locked 60fps for smooth animations
- **Score Updates**: <200ms from detection to display
- **Rally Counter**: <50ms increment response time
- **Touch Response**: <16ms touch-to-feedback latency

### Resource Management
- **Memory**: Efficient state management, prevent memory leaks
- **CPU**: Optimize for sustained performance over long games
- **Thermal**: Monitor device temperature, reduce effects if overheating
- **Battery**: Power-efficient operations, optional low-power mode

### Network Optimization
- **Bandwidth**: Adaptive quality for video streams
- **Latency**: Prioritize score data over video quality  
- **Reliability**: Graceful degradation on poor connections
- **Data Usage**: Monitor and optimize WebSocket message frequency

## Handoff Notes for Implementation

### Technical Architecture
- **Frontend**: React with WebSocket integration for real-time updates
- **State Management**: Redux with real-time middleware
- **Animations**: Framer Motion or CSS transitions for performance  
- **Video**: WebRTC for PIP streams, fallback to HLS/DASH
- **Audio**: Web Audio API for system sounds

### API Integration
- `WS /games/{id}/live` - Real-time game state updates
- `POST /games/{id}/score` - Manual score adjustments (admin)
- `GET /games/{id}/stats` - Real-time statistics  
- `POST /games/{id}/pause` - Pause/resume game
- `POST /games/{id}/end` - End game transition

### Asset Requirements
- **Icons**: Game state badges, connection indicators (SVG)
- **Sounds**: Score change, rally increment, game state sounds (MP3)
- **Fonts**: Roboto family including Roboto Mono for scores
- **Animations**: Loading states, connection indicators

### Testing Requirements
- **Device Testing**: iPad Air, iPad Pro models
- **Network Testing**: Various connection qualities and interruptions
- **Load Testing**: Sustained performance over 30+ minute games
- **Stress Testing**: Multiple simultaneous sessions
- **Accessibility Testing**: VoiceOver, Switch Control, High Contrast

This Live Dashboard specification creates an impressive, functional scoring interface that serves as the centerpiece of the LockN Score experience, suitable for investor demos and tournament use.