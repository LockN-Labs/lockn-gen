# Journey 2: Player Registration + Stream Setup (iPhone)

## Overview
Player-side mobile flow for joining ping pong scoring sessions on iPhone in portrait orientation. Covers authentication, profile setup, session joining, and camera/mic stream initialization.

**Target Device**: iPhone (Portrait)  
**Viewport**: 375×667px (iPhone SE) to 428×926px (iPhone 14 Pro Max)  
**User Role**: Player participating in scoring session  
**Duration**: ~15 seconds from code entry to ready state

## Screen Flow
```
Session Join → Auth (if needed) → Profile Setup → Permissions → Stream Setup → Ready Confirmation
```

## Screen 1: Session Join Entry

### Layout Specifications
**Dimensions**: 375×667px (base), scales to larger iPhones  
**Safe Areas**: Respect device safe areas (notch, home indicator)  
**Status Bar**: Dark content on light background

### Header Section (375×120px)
- **Background**: `--primary` (#1976D2) gradient to `--primary-light`
- **Content**:
  - **Logo**: LockN Score logo (120×40px), centered, white
  - **Subtitle**: "Join a Game Session"
    - Typography: `--body-large` (16px/24px)
    - Color: White with 80% opacity
    - Position: 16px below logo

### Join Methods Card (343×400px)
- **Position**: 16px horizontal margins from screen edge
- **Background**: `--surface-1` (#1E1E1E)
- **Elevation**: `--elevation-3`
- **Border Radius**: `--radius-lg` (16px)
- **Padding**: 24px

#### Method 1: Code Entry (343×180px)
- **Icon**: Keypad icon (40×40px), `--primary` color
- **Title**: "Enter Session Code"
  - Typography: `--title-medium` (16px/24px, weight 500)
  - Color: `--text-primary`
  - Position: 16px below icon
- **Input Field**: 
  - **Dimensions**: 295×56px
  - **Background**: `--surface-2` (#232323)
  - **Border**: 2px solid `--surface-3` (focus: `--primary`)
  - **Border Radius**: `--radius-md` (12px)
  - **Typography**: `--headline-small` (24px/32px, monospace)
  - **Placeholder**: "ABC123"
  - **Letter Spacing**: 4px
  - **Text Transform**: Uppercase
  - **Max Length**: 6 characters
  - **Auto-focus**: Yes
- **Helper Text**: "Enter the 6-digit code from the dashboard"
  - Typography: `--body-small` (12px/16px)
  - Color: `--text-secondary`

#### Method 2: QR Scan (343×140px, 20px margin-top)
- **Divider**: Horizontal line with "OR" text in center
- **Icon**: QR code scan icon (40×40px), `--primary` color
- **Button**: "Scan QR Code"
  - **Dimensions**: 295×48px
  - **Background**: Transparent
  - **Border**: 2px solid `--primary`
  - **Text Color**: `--primary`
  - **Border Radius**: `--radius-md` (12px)
  - **Typography**: `--label-large` (14px/20px, weight 500)

### Continue Button (343×56px)
- **Position**: 24px below join methods card
- **Background**: `--primary` (disabled: `--surface-3`)
- **Text**: "Join Session"
- **Typography**: `--label-large` (14px/20px, weight 500), white
- **Border Radius**: `--radius-md` (12px)
- **State**: Disabled until valid code entered

### Bottom Section (375×147px)
- **Help Link**: "Need help?" 
  - Color: `--primary`
  - Position: Centered, 24px below continue button
- **Terms**: Small legal text about data usage
  - Typography: `--body-small` (12px/16px)
  - Color: `--text-disabled`
  - Position: Bottom safe area

### States & Interactions

#### Code Input States
- **Empty**: Placeholder visible, continue disabled
- **Typing**: Real-time validation, format as XXX-XXX
- **Valid Format**: Green checkmark, continue enabled  
- **Invalid Code**: Red border, error message below
- **Loading**: Spinner overlay, "Joining session..."

#### QR Scan Flow
- **Camera Permission**: Request camera access
- **Scanner View**: Full-screen overlay with scan frame
- **Success**: Green flash, auto-return to join screen
- **Error**: Red flash, "Invalid QR code" message

#### Network States
- **Offline**: "No internet connection" banner
- **Timeout**: "Session not found or expired" error
- **Server Error**: "Connection error, please try again"

## Screen 2: Authentication Flow

### Quick Auth Screen (if not logged in)
**Dimensions**: 375×667px  
**Transition**: Slide up from bottom (400ms ease-out)

### Header (375×80px)
- **Title**: "Sign In to Join"
- **Close Button**: X in top-right (returns to join screen)
- **Background**: `--surface` (#121212)

### Auth Card (343×400px)
- **Position**: Centered vertically
- **Background**: `--surface-1` 
- **Border Radius**: `--radius-lg` (16px)
- **Padding**: 24px

#### Login Tab (Default)
- **Email Field**:
  - **Dimensions**: 295×48px
  - **Label**: "Email", `--body-medium`
  - **Input**: `--body-large`, `--surface-2` background
  - **Validation**: Real-time email format check
- **Password Field**: (16px margin-top)
  - **Dimensions**: 295×48px  
  - **Show/Hide Toggle**: Eye icon in input
  - **Forgot Password**: Link below field
- **Sign In Button**: (24px margin-top)
  - **Dimensions**: 295×48px
  - **Background**: `--primary`
  - **Loading State**: Spinner + "Signing in..."

#### Sign Up Tab
- **Name Field**: Full name input
- **Email Field**: Same as login
- **Password Field**: With strength indicator
- **Confirm Password**: Validation matching
- **Terms Checkbox**: Required, with links
- **Create Account Button**: Similar to sign in

### Social Auth Options (343×120px)
- **Divider**: "Or continue with" text
- **Buttons**: Apple, Google sign-in
  - **Dimensions**: 295×48px each
  - **Spacing**: 12px between buttons
  - **Style**: Dark mode system buttons

### Quick Guest Option (343×80px)
- **Link**: "Continue as Guest"
- **Disclaimer**: "Limited features, no game history"
- **Use Case**: Demo or temporary play

## Screen 3: Profile Setup

### First-Time Profile Creation
**Dimensions**: 375×667px  
**Condition**: New users or users without profile photos

### Header (375×120px)  
- **Progress**: Step 2 of 4 indicator
- **Title**: "Set Up Your Profile"
- **Subtitle**: "This helps identify you during games"

### Photo Capture Section (343×280px)
- **Avatar Circle**: 120×120px placeholder
  - **Background**: `--surface-2` with dashed border
  - **Icon**: Camera icon (40×40px), `--text-secondary`
  - **Position**: Centered horizontally
- **Camera Button**: "Take Photo"
  - **Dimensions**: 200×48px
  - **Position**: 24px below avatar
  - **Background**: `--primary`
- **Gallery Button**: "Choose from Photos"
  - **Dimensions**: 200×48px  
  - **Position**: 12px below camera button
  - **Style**: Outline button, `--primary` border

### Name Section (343×120px)
- **Label**: "Display Name"
  - Typography: `--title-medium` (16px/24px, weight 500)
- **Input Field**:
  - **Dimensions**: 295×48px
  - **Placeholder**: "Enter your name"
  - **Max Length**: 20 characters
  - **Auto-focus**: After photo capture
- **Helper**: "This name will appear on the scoreboard"
  - Typography: `--body-small` (12px/16px)
  - Color: `--text-secondary`

### Continue Button (343×56px)
- **Position**: 32px below name section
- **Text**: "Continue"
- **State**: Enabled when name entered (photo optional)

### Returning User Profile
**Layout**: Same structure, pre-filled with existing data
- **Current Photo**: Display existing avatar
- **Update Options**: "Update Photo", "Keep Current"
- **Name**: Pre-filled, editable
- **Quick Continue**: "Looks good, continue" button

## Screen 4: Permissions Setup

### Permissions Overview
**Dimensions**: 375×667px  
**Purpose**: Request camera and microphone access

### Header (375×120px)
- **Progress**: Step 3 of 4 indicator
- **Title**: "Camera & Microphone"
- **Subtitle**: "Required for game streaming"

### Permissions List (343×400px)
#### Camera Permission (343×160px)
- **Icon**: Camera icon (48×48px), `--primary` color
- **Title**: "Camera Access"
  - Typography: `--title-medium` (16px/24px, weight 500)
- **Description**: "Stream your gameplay to the main dashboard"
  - Typography: `--body-medium` (14px/20px)
  - Color: `--text-secondary`
- **Status Badge**: 
  - **Granted**: Green checkmark + "Allowed"
  - **Pending**: Orange clock + "Tap to allow"
  - **Denied**: Red X + "Denied"

#### Microphone Permission (343×160px, 20px margin-top)
- **Icon**: Microphone icon (48×48px), `--primary` color
- **Title**: "Microphone Access"
- **Description**: "Detect ball bounces with audio analysis"
- **Status Badge**: Same states as camera

#### Optional Notifications (343×80px, 20px margin-top)
- **Icon**: Bell icon (24×24px), `--text-secondary`
- **Title**: "Game Notifications (Optional)"
- **Toggle**: Enable/disable switch
- **Description**: "Get notified about game events"

### Permission Buttons (343×120px)
#### Camera Button
- **Dimensions**: 343×48px
- **Text**: "Allow Camera Access"
- **Background**: `--primary` (or `--success` if granted)
- **Action**: Trigger iOS camera permission dialog

#### Microphone Button (12px margin-top)
- **Dimensions**: 343×48px  
- **Text**: "Allow Microphone Access"
- **Background**: `--primary` (or `--success` if granted)

### Continue Section (343×80px)
- **Continue Button**: Enabled when both permissions granted
- **Skip Button**: "Continue without audio" (camera-only mode)
- **Help**: "Why do we need these permissions?"

### Permission Denied States
#### Camera Denied
- **Alert**: Red warning banner
- **Message**: "Camera required for gameplay streaming"
- **Actions**: 
  - "Open Settings" → iOS Settings app
  - "Try Again" → Re-request permission

#### Microphone Denied (Less Critical)
- **Alert**: Yellow warning banner
- **Message**: "Audio detection disabled"
- **Impact**: "Some features may not work"
- **Action**: "Continue Anyway" button enabled

## Screen 5: Stream Setup

### Stream Configuration  
**Dimensions**: 375×667px  
**Purpose**: Configure video stream and test connection

### Header (375×120px)
- **Progress**: Step 4 of 4 indicator
- **Title**: "Stream Setup"
- **Subtitle**: "Configuring your video feed"

### Camera Preview (343×240px)
- **Position**: 16px from screen edges
- **Background**: `--surface-2`
- **Border Radius**: `--radius-lg` (16px)
- **Content**: Live camera feed preview
- **Overlay Elements**:
  - **Flip Camera**: Button in top-right corner
  - **Quality**: "HD" badge in top-left
  - **Frame Rate**: "30fps" indicator

### Stream Settings (343×180px)
#### Video Quality (343×80px)
- **Label**: "Video Quality"
- **Options**: Segmented control
  - "720p" (default), "1080p", "Auto"
  - **Dimensions**: 295×40px
  - **Style**: `--surface-2` background, `--primary` selection

#### Frame Rate (343×80px, 20px margin-top)
- **Label**: "Frame Rate" 
- **Options**: "30fps" (default), "60fps", "120fps"
- **Note**: Higher = better detection, more battery usage
- **Typography**: `--body-small` for note

### Connection Test (343×140px)
#### Status Indicators
- **Upload Speed**: Test result in Mbps
  - **Good**: >5 Mbps, green indicator
  - **Fair**: 2-5 Mbps, yellow indicator  
  - **Poor**: <2 Mbps, red indicator
- **Latency**: Ping test to dashboard
  - **Target**: <100ms for optimal experience
- **Battery**: Current level and usage estimate

#### Test Button
- **Dimensions**: 295×48px
- **Text**: "Test Connection"
- **Background**: `--info` (#2196F3)  
- **Loading**: "Testing..." with spinner

### Ready Confirmation (343×107px)
#### Status Summary
- **Camera**: Green checkmark + "Ready"
- **Microphone**: Status based on permissions
- **Network**: Connection quality indicator
- **Battery**: Sufficient charge warning if <20%

#### Ready Button
- **Dimensions**: 343×56px
- **Text**: "I'm Ready to Play!"  
- **Background**: `--success` (#4CAF50)
- **State**: Enabled when all systems ready
- **Loading**: "Joining game..." when tapped

## Screen 6: Ready Confirmation

### Game Lobby Screen
**Dimensions**: 375×667px  
**State**: Waiting for host to start game

### Header (375×100px)
- **Session Code**: Display joined session (6-digit code)
- **Status**: "Connected to session" with green dot
- **Exit**: "Leave Session" link in top-right

### Player Status (343×200px)
#### Your Status Card (343×90px)  
- **Avatar**: Your profile photo (60×60px)
- **Name**: Display name
- **Status**: "Ready" with green checkmark
- **Stream**: "Video streaming" indicator
- **Audio**: Microphone status indicator

#### Other Players List (343×90px)
- **Title**: "Other Players"
- **Player Cards**: Mini cards for other joined players
  - **Layout**: Horizontal scroll if >3 players
  - **Content**: Avatar (40×40px) + name + status
  - **Status**: Connected, streaming, etc.

### Game Info (343×160px)
#### Session Details
- **Game Mode**: Display selected mode (Rally, Full Game, etc.)
- **Settings**: Points to win, serve rules summary
- **Host**: Name of session creator
- **Start Time**: "Game will start shortly"

#### Waiting Message
- **Text**: "Waiting for host to start the game..."
- **Animation**: Subtle pulsing dots
- **Typography**: `--body-large` (16px/24px)
- **Color**: `--text-secondary`

### Stream Monitor (343×140px)
#### Your Camera Feed
- **Dimensions**: 120×90px thumbnail
- **Position**: Centered in card
- **Overlay**: "LIVE" indicator in red
- **Quality**: Current resolution and fps
- **Data Usage**: Real-time upload speed

#### Controls
- **Mute Video**: Toggle camera on/off
- **Mute Audio**: Toggle microphone on/off
- **Settings**: Quick access to quality settings

### Error Handling (Full Screen Overlays)

#### Connection Lost
- **Overlay**: Semi-transparent background
- **Icon**: WiFi with slash (48×48px), `--error` color
- **Title**: "Connection Lost"
- **Message**: "Trying to reconnect..."
- **Actions**: "Retry" button, "Leave Session" link

#### Stream Failed
- **Title**: "Stream Error"
- **Message**: "Unable to start video stream"
- **Diagnostics**: 
  - Check camera permissions
  - Check network connection
  - Restart app if needed
- **Actions**: "Try Again", "Join Without Video"

#### Session Ended
- **Title**: "Session Ended"
- **Message**: "The host has ended the session"
- **Actions**: "Return to Home", "Join Another Session"

## Responsive Considerations

### iPhone SE (375×667px) - Base Design
- **All dimensions as specified above**
- **Touch targets**: Minimum 44×44px
- **Text scaling**: Base font sizes

### iPhone Pro Max (428×926px) - Scaled Up  
- **Horizontal spacing**: +26px on each side (53px total)
- **Vertical spacing**: +129px distributed across sections
- **Font scaling**: +2px for display text, +1px for body text
- **Button sizes**: +8px width, same height
- **Camera preview**: +40px width and height

### Safe Area Handling
- **Top Safe Area**: Account for notch (44px typical)
- **Bottom Safe Area**: Account for home indicator (34px typical)  
- **Side Safe Areas**: Account for rounded corners
- **Landscape**: Adjust layout for brief landscape use

## Accessibility Features

### Vision Accessibility
- **Dynamic Type**: Support all system text sizes
- **High Contrast**: Alternative color scheme
- **Reduce Motion**: Disable animations if preferred
- **VoiceOver**: Full screen reader support

### Motor Accessibility  
- **Large Touch Targets**: All buttons minimum 44×44px
- **Switch Control**: Support external switch input
- **Voice Control**: All UI elements voice controllable
- **Reachability**: Important controls in thumb-friendly zones

### Audio Accessibility
- **Visual Indicators**: Flash for audio cues
- **Haptic Feedback**: Confirm button presses
- **Closed Captions**: For any audio instructions

## Performance Requirements

### Loading Times
- **Screen Transitions**: <300ms between screens
- **Camera Initialization**: <2 seconds to preview
- **Permission Requests**: Instant OS dialog trigger
- **Stream Setup**: <5 seconds to ready state

### Battery Optimization
- **Camera Usage**: Efficient video encoding
- **Network**: Adaptive bitrate for poor connections
- **Background**: Minimize CPU when app backgrounded
- **Thermal**: Reduce quality if device overheating

### Network Resilience
- **Poor WiFi**: Adaptive quality reduction
- **Disconnections**: Automatic reconnection attempts  
- **Data Usage**: Warnings for cellular usage
- **Bandwidth**: Real-time monitoring and adjustment

## Handoff Notes for Implementation

### Technical Requirements
- **Camera API**: AVFoundation for iOS video capture
- **Permissions**: Request at appropriate flow points
- **WebRTC**: For real-time video streaming
- **State Management**: Redux for flow state persistence
- **Deep Linking**: Handle session join URLs

### API Integration Points
- `POST /auth/login` - User authentication
- `POST /users/profile` - Profile creation/update
- `POST /sessions/{id}/join` - Join game session
- `WS /sessions/{id}/player/{userId}` - Player WebSocket
- `POST /streams/start` - Initialize video stream

### Asset Requirements
- **Icons**: Permission icons, status indicators (SVG)
- **Sounds**: Success, error, notification sounds
- **Animations**: Loading spinners, success checkmarks
- **Placeholder Images**: Default avatar, empty states

### Testing Requirements
- **Device Testing**: iPhone SE through Pro Max
- **Permission Testing**: Grant, deny, revoke scenarios  
- **Network Testing**: WiFi, cellular, poor connections
- **Edge Cases**: Background/foreground, interruptions
- **Accessibility**: VoiceOver, Dynamic Type, High Contrast

This Journey 2 specification ensures a smooth mobile onboarding experience for players joining ping pong scoring sessions.