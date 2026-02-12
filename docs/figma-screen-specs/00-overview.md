# LockN Score - Complete Screen Specifications for Figma

## Project Overview
Comprehensive screen specifications for **LockN Score**, an AI-powered ping pong scoring and coaching application. The system uses computer vision and audio analysis to automatically track games and provide real-time scoring.

**Generated**: February 10, 2026  
**Target Platform**: Responsive web app (iPad dashboard + iPhone mobile flows)
**Design System**: Clean, minimal, dark mode, Material Design
**Tone**: Professional, sporty-but-refined, data-forward

## Design System Foundation

### Color Palette (Dark Mode Material)
```css
/* Primary Colors */
--primary: #1976D2;           /* Material Blue 700 */
--primary-light: #42A5F5;     /* Material Blue 400 */
--primary-dark: #1565C0;      /* Material Blue 800 */

/* Surface Colors (Dark Theme) */
--surface: #121212;           /* Primary surface */
--surface-1: #1E1E1E;        /* Elevated surface 1dp */
--surface-2: #232323;        /* Elevated surface 2dp */
--surface-3: #252525;        /* Elevated surface 3dp */
--surface-4: #272727;        /* Elevated surface 4dp */

/* Text Colors */
--text-primary: #FFFFFF;      /* 87% white */
--text-secondary: #B3B3B3;    /* 60% white */
--text-disabled: #666666;     /* 38% white */

/* Accent Colors */
--success: #4CAF50;           /* Green 500 */
--warning: #FF9800;           /* Orange 500 */
--error: #F44336;            /* Red 500 */
--info: #2196F3;             /* Blue 500 */

/* Score Colors */
--score-player-1: #4CAF50;    /* Green for Player 1 */
--score-player-2: #2196F3;    /* Blue for Player 2 */
--serve-indicator: #FF9800;   /* Orange for serve */
```

### Typography Scale
**Font Family**: Roboto (Material Design standard)  
**Fallback**: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif

```css
/* Display */
--display-large: 57px/64px, weight: 400;
--display-medium: 45px/52px, weight: 400;
--display-small: 36px/44px, weight: 400;

/* Headline */
--headline-large: 32px/40px, weight: 400;
--headline-medium: 28px/36px, weight: 400;
--headline-small: 24px/32px, weight: 400;

/* Title */
--title-large: 22px/28px, weight: 500;
--title-medium: 16px/24px, weight: 500;
--title-small: 14px/20px, weight: 500;

/* Body */
--body-large: 16px/24px, weight: 400;
--body-medium: 14px/20px, weight: 400;
--body-small: 12px/16px, weight: 400;

/* Label */
--label-large: 14px/20px, weight: 500;
--label-medium: 12px/16px, weight: 500;
--label-small: 11px/16px, weight: 500;
```

### Spacing Scale (8px base unit)
```css
--space-1: 4px;   /* 0.5 unit */
--space-2: 8px;   /* 1 unit */
--space-3: 12px;  /* 1.5 units */
--space-4: 16px;  /* 2 units */
--space-5: 20px;  /* 2.5 units */
--space-6: 24px;  /* 3 units */
--space-8: 32px;  /* 4 units */
--space-10: 40px; /* 5 units */
--space-12: 48px; /* 6 units */
--space-16: 64px; /* 8 units */
--space-20: 80px; /* 10 units */
--space-24: 96px; /* 12 units */
```

### Border Radius
```css
--radius-xs: 4px;   /* Small elements */
--radius-sm: 8px;   /* Cards, buttons */
--radius-md: 12px;  /* Panels */
--radius-lg: 16px;  /* Modals */
--radius-xl: 24px;  /* Large containers */
--radius-full: 50%; /* Circular */
```

### Elevation (Material Design)
```css
--elevation-0: none;
--elevation-1: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
--elevation-2: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
--elevation-3: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
--elevation-4: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
--elevation-5: 0 19px 38px rgba(0,0,0,0.30), 0 15px 12px rgba(0,0,0,0.22);
```

## Screen Architecture & User Journeys

### Core User Flows

#### 1. Session Creation Flow (iPad/Dashboard) - Journey 1
**Screens**: [Journey 1 Screens](./01-session-creation-ipad.md)
- **Home/Landing Screen**: Primary "New Game" CTA
- **Mode Selection**: Solo, Rally, Game modes
- **Game Settings**: Points to win, serve rules configuration
- **Waiting Room**: Session code/QR display, join notifications

#### 2. Player Registration + Stream Setup (iPhone) - Journey 2  
**Screens**: [Journey 2 Screens](./02-player-registration-iphone.md)
- **Auth Flow**: Login/signup integration with LockN Auth
- **Profile Setup**: Photo capture for identification
- **Session Join**: Code entry or QR scan
- **Stream Setup**: Camera/mic permissions, connection status
- **Ready State**: Confirmation and stream readiness

#### 3. Live Dashboard (iPad - Game Active) - Journey 3
**Screens**: [Journey 3 Screens](./03-live-dashboard-ipad.md)  
- **Live Scoring Interface**: Real-time score display
- **Player Cards**: Names, photos, serve indicators
- **Game State**: Rally counter, game status badges
- **Video Feeds**: Optional PIP iPhone stream displays

#### 4. Post-Game Recap (iPad & iPhone) - Journey 4
**Screens**: [Journey 4 Screens](./04-post-game-recap.md)
- **Final Score**: Winner announcement, complete score
- **Statistics Panel**: Rally count, longest rally, serve accuracy
- **Timeline**: Key points and game progression  
- **Highlights**: Auto-detected clips, share/export actions

### Supporting Flows

#### 5. Landing & Marketing
**Screens**: [Landing Pages](./05-landing-marketing.md)
- **Hero Landing**: Value proposition, demo preview
- **Feature Overview**: Computer vision scoring, AI coaching
- **Pricing/Plans**: Subscription tiers, feature comparison
- **Getting Started**: Setup guide, device requirements

#### 6. Authentication & Onboarding  
**Screens**: [Auth & Onboarding](./06-auth-onboarding.md)
- **Login/Signup**: LockN Auth integration
- **Onboarding Flow**: App introduction, permissions
- **Account Setup**: Profile creation, preferences
- **Device Pairing**: iPad/iPhone connection guide

#### 7. Dashboard & Settings
**Screens**: [Dashboard & Settings](./07-dashboard-settings.md) 
- **Main Dashboard**: Game history, statistics overview
- **Settings Panel**: Audio/video preferences, game rules
- **Profile Management**: User profile, photo updates
- **Help & Support**: FAQs, troubleshooting, contact

## Responsive Design Strategy

### Device Targets
- **iPad (Landscape)**: 1024×768px to 1366×1024px (primary dashboard)
- **iPhone (Portrait)**: 375×667px to 428×926px (player mobile flows) 
- **Desktop Fallback**: 1200×800px+ (web access)

### Breakpoint System
```css
/* Mobile First Approach */
@media (max-width: 767px) { /* Mobile */ }
@media (min-width: 768px) and (max-width: 1023px) { /* Tablet Portrait */ }
@media (min-width: 1024px) and (max-width: 1365px) { /* Tablet Landscape */ }
@media (min-width: 1366px) { /* Desktop */ }
```

### Responsive Patterns
- **Fluid Grid System**: 12-column grid with flexible gutters
- **Progressive Disclosure**: Hide secondary features on smaller screens
- **Touch-First Design**: 44px minimum touch targets
- **Adaptive Typography**: Scale text based on viewport size
- **Contextual Navigation**: Bottom tabs on mobile, side nav on desktop

## Component Library

### Interactive Components
- **Buttons**: Primary, secondary, text, icon variants
- **Form Controls**: Text inputs, dropdowns, toggles, sliders
- **Navigation**: Bottom tabs, side nav, breadcrumbs
- **Cards**: Player cards, game cards, stat cards
- **Modals**: Settings, confirmations, full-screen overlays

### Data Display
- **Score Displays**: Large format scores, mini scores
- **Progress Indicators**: Rally counters, game progress
- **Statistics**: Charts, graphs, numeric displays
- **Video Components**: PIP feeds, full-screen video
- **Tables**: Game history, player stats

### Feedback Components  
- **Alerts**: Success, error, warning, info states
- **Loading States**: Spinners, skeleton screens, progress bars
- **Empty States**: No data, no connection, first-time use
- **Notifications**: Toast messages, system alerts

## Implementation Priorities

### Phase 1: Core Gameplay (MVP)
1. **Session Creation Flow** (iPad)
2. **Player Registration** (iPhone)  
3. **Live Dashboard** (iPad)
4. **Basic Post-Game** (iPad)

### Phase 2: Enhanced Features
1. **Mobile Post-Game** (iPhone)
2. **Statistics Dashboard**
3. **Video Integration**
4. **Settings & Preferences**

### Phase 3: Marketing & Growth
1. **Landing Pages**
2. **Onboarding Flow**
3. **Help & Documentation**
4. **Advanced Analytics**

## Technical Integration Notes

### API Endpoints (Existing)
- `/score/vision` - Computer vision ball detection
- `/score/audio` - Audio bounce detection
- `/score/fusion` - Data correlation engine
- `/score/websocket` - Real-time updates

### Data Models
- **Session**: Game configuration, players, state
- **Player**: Profile, photo, statistics
- **Score**: Current score, serve indicator, rally count
- **Event**: Ball position, bounce detection, timestamps

### Real-Time Features
- **WebSocket Updates**: Live score changes, game events
- **Video Streaming**: iPhone camera feeds to dashboard
- **Audio Processing**: Real-time bounce detection
- **State Synchronization**: Multi-device game state

## File Structure
```
docs/figma-screen-specs/
├── 00-overview.md                    # This overview document
├── 01-session-creation-ipad.md       # Journey 1: Session creation (iPad)
├── 02-player-registration-iphone.md  # Journey 2: Player setup (iPhone)  
├── 03-live-dashboard-ipad.md         # Journey 3: Live scoring (iPad)
├── 04-post-game-recap.md             # Journey 4: Post-game recap
├── 05-landing-marketing.md           # Landing & marketing pages
├── 06-auth-onboarding.md             # Authentication & onboarding
├── 07-dashboard-settings.md          # Dashboard & settings
├── components/                       # Component specifications
│   ├── buttons.md                   # Button variants and states
│   ├── forms.md                     # Form controls and inputs
│   ├── navigation.md                # Navigation patterns  
│   ├── cards.md                     # Card components
│   └── feedback.md                  # Alerts, loading, empty states
└── assets/                          # Reference images and icons
    ├── icons/                       # SVG icon set
    ├── images/                      # Sample photos and graphics
    └── mockups/                     # Wireframe sketches
```

## Success Metrics & KPIs

### User Experience
- **Session Creation Time**: <30 seconds from start to waiting room
- **Player Join Time**: <15 seconds from code entry to ready
- **Score Accuracy**: >95% automated scoring accuracy  
- **Latency**: <200ms from ball bounce to score update

### Technical Performance
- **Load Time**: <3 seconds initial page load
- **Video Latency**: <100ms iPhone stream to dashboard
- **Connection Reliability**: >99% uptime during games
- **Cross-Device Sync**: <50ms state synchronization

This specification serves as the comprehensive blueprint for creating all LockN Score screens in Figma, ensuring consistency, usability, and technical feasibility across the entire application.