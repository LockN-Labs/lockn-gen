# LockN AI Platform - Main Landing Page

## Screen Overview
**Screen Type:** Marketing landing page and platform launcher  
**App:** LockN AI Platform  
**Journey:** Entry point to the LockN AI Suite ecosystem  
**Route:** `/` (root)  
**Component:** `web/index.html`

## Layout Description

### Container Structure
- **Background:** Dark theme (`--bg: #06070a`)
- **Typography:** System font stack with fallbacks
- **Max Width:** 1200px centered container
- **Padding:** 0 2rem responsive padding

### CSS Variables (Design System)
```css
:root {
  --primary: #00d4ff;
  --secondary: #7b2cbf;
  --bg: #06070a;
  --surface: rgba(255,255,255,0.04);
  --surface-strong: rgba(255,255,255,0.08);
  --border: rgba(255,255,255,0.1);
  --text: #f5f6f9;
  --text-muted: #9aa0a8;
  --success: #4ade80;
  --warning: #facc15;
}
```

## Navigation Section

### Nav Container
- **Position:** Sticky top with z-index 10
- **Background:** `rgba(6,7,10,0.85)` with backdrop-blur 16px
- **Border:** Bottom border with `--border` color
- **Padding:** 1.5rem vertical

### Nav Layout
- **Structure:** Flex justify-between, items-center
- **Gap:** 2rem between elements

### Logo Section (Left)
- **Font Size:** 1.4rem (22.4px)
- **Font Weight:** 700 (bold)
- **Layout:** Flex items-center with 0.5rem gap
- **Icon:** 🔐 emoji or equivalent

### Navigation Links (Center)
- **Layout:** Flex with 1.5rem gaps, flex-wrap
- **Color:** `--text-muted` default, `--text` on hover
- **Links:** Platform navigation (Speak, Score, Gen, etc.)

### Navigation Actions (Right)
- **Layout:** Flex with 0.75rem gaps, items-center
- **Buttons:** Login/signup CTAs with button styling

## Hero Section

### Container
- **Padding:** 5rem 0 4rem (80px top, 64px bottom)
- **Text Alignment:** Center

### Hero Badge
- **Layout:** Inline-flex, items-center, 0.6rem gap
- **Background:** `rgba(0,212,255,0.12)` (primary with 12% opacity)
- **Color:** `--primary`
- **Padding:** 0.4rem 1rem
- **Border Radius:** 999px (fully rounded)
- **Font Size:** 0.85rem
- **Margin Bottom:** 1.5rem

### Hero Title
- **Font Size:** `clamp(2.6rem, 6vw, 4.5rem)` (responsive)
- **Line Height:** 1.05 (tight)
- **Margin Bottom:** 1.2rem
- **Gradient Text:** Linear gradient from `--primary` to `--secondary`

### Hero Description
- **Color:** `--text-muted`
- **Max Width:** 720px centered
- **Font Size:** 1.15rem
- **Margin:** 0 auto 2rem

### Hero CTA Section
- **Layout:** Flex justify-center, gap 1rem, flex-wrap
- **Buttons:** Primary and secondary button styles

## Button Components

### Base Button Styles
- **Layout:** Inline-flex, items-center, 0.5rem gap
- **Padding:** 0.75rem 1.4rem
- **Border Radius:** 12px
- **Font Weight:** 600
- **Font Size:** 0.95rem
- **Transition:** All 0.2s

### Primary Button (.btn-primary)
- **Background:** Linear gradient (primary → secondary)
- **Color:** #fff
- **Hover Effect:** translateY(-2px) + shadow glow

### Secondary Button (.btn-secondary)
- **Background:** `--surface`
- **Border:** `--border`
- **Color:** #fff
- **Hover:** Border color changes to `--primary`

### Ghost Button (.btn-ghost)
- **Background:** Transparent
- **Border:** `--border`
- **Color:** `--text`

## Feature Grid Section

### Section Container
- **Padding:** 4.5rem 0 (72px vertical)

### Section Title
- **Text Alignment:** Center
- **Margin Bottom:** 2.5rem

#### Title Styling
- **Font Size:** `clamp(2rem, 4vw, 2.6rem)` (responsive)
- **Margin Bottom:** 0.6rem

#### Title Description
- **Color:** `--text-muted`
- **Max Width:** 720px centered

### Feature Grid Layout
- **Grid:** `repeat(auto-fit, minmax(240px, 1fr))`
- **Gap:** 1.5rem between cards

### Feature Card Component

#### Card Container
- **Background:** `--surface`
- **Border:** 1px solid `--border`
- **Border Radius:** 18px
- **Padding:** 1.8rem
- **Layout:** Flex column with 1rem gaps
- **Min Height:** 220px
- **Transition:** All 0.3s

#### Card Hover Effects
- **Border:** Changes to `rgba(0,212,255,0.6)`
- **Transform:** translateY(-4px)
- **Shadow:** `0 18px 40px rgba(0,0,0,0.35)`

#### Card Content Structure
1. **Feature Icon/Title:** 1.2rem font-size, 600 weight
2. **Description:** `--text-muted`, 0.95rem font-size
3. **Meta Section:** Flex justify-between, margin-top auto

#### Feature Meta Section
- **Layout:** Flex justify-between, items-center
- **Gap:** 0.75rem
- **Content:** Status chips and action links

### Status Chips

#### Base Chip Styling
- **Layout:** Inline-flex, items-center, 0.35rem gap
- **Padding:** 0.25rem 0.6rem
- **Border Radius:** 999px
- **Font Size:** 0.75rem
- **Background:** `rgba(255,255,255,0.08)`
- **Border:** 1px solid transparent

#### Chip Variants
- **Live Chip (.chip-live):**
  - Color: `--success`
  - Border: `rgba(74,222,128,0.4)`
  - Background: `rgba(74,222,128,0.12)`

- **Warning Chip (.chip-warn):**
  - Color: `--warning`
  - Border: `rgba(250,204,21,0.4)`
  - Background: `rgba(250,204,21,0.12)`

## Demo Grid Section

### Demo Cards Layout
- **Grid:** `repeat(auto-fit, minmax(260px, 1fr))`
- **Gap:** 1.5rem between demo cards

### Demo Card Component

#### Card Container
- **Background:** `--surface-strong`
- **Border:** 1px solid `--border`
- **Border Radius:** 18px
- **Padding:** 1.5rem
- **Layout:** Flex column with 0.8rem gaps

#### Card Content
- **Title:** 1.1rem font-size
- **Description:** `--text-muted`, 0.9rem font-size
- **Actions:** Flex wrap with 0.6rem gaps, margin-top auto

#### Demo Actions
- **Links:** 0.85rem font-size
- **Styling:** Consistent with button component system

## Documentation Grid Section

### Doc Grid Layout
- **Grid:** `repeat(auto-fit, minmax(240px, 1fr))`
- **Gap:** 1.2rem between documentation cards

### Doc Card Styling
- **Border:** 1px solid `--border`
- **Additional styling:** Consistent with feature cards but optimized for documentation links

## Platform Integration Links

### Suite Navigation
The landing page serves as a launcher for multiple LockN apps:
- **Speak:** `/speak/` - Voice/TTS application
- **Score:** `/score/` - Real-time scoring system  
- **Gen:** `/gen/` - AI generation tools
- **Listen:** `/listen/` - Audio processing
- **Look:** `/look/` - Computer vision
- **Brain:** `/brain/` - AI orchestration
- **Sense:** `/sense/` - Multi-modal sensing

## Responsive Behavior

### Desktop (1200px+)
- **Navigation:** Full horizontal layout
- **Hero:** Large text sizing with full CTA row
- **Feature Grid:** Multi-column layout with hover effects
- **Typography:** Maximum font sizes

### Tablet (768px - 1199px)
- **Navigation:** May wrap navigation links
- **Hero:** Medium text scaling
- **Grids:** Fewer columns but maintain readability
- **Touch:** Optimized for touch interaction

### Mobile (< 768px)
- **Navigation:** Collapsed or stacked navigation
- **Hero:** Minimum text sizes but readable
- **Grids:** Single column layout
- **Spacing:** Compressed but maintains hierarchy

## Text Content

### Navigation
- **Brand:** "LockN Suite" or equivalent branding
- **Links:** Platform app names
- **Actions:** "Login", "Sign Up", "Get Started"

### Hero Section
- **Badge:** "New", "Beta", "AI-Powered", etc.
- **Title:** "Multimodal AI Infrastructure" or similar value proposition
- **Description:** Platform capabilities and benefits
- **CTAs:** "Get Started", "View Demo", "Learn More"

### Feature Cards
- **Titles:** Individual app/feature names
- **Descriptions:** Brief capability descriptions
- **Status:** "Live", "Beta", "Coming Soon"
- **Actions:** "Try Demo", "Documentation", "API"

### Section Headers
- **Features:** "Platform Capabilities" or similar
- **Demo:** "Try It Live" or equivalent
- **Documentation:** "Get Started" or "Developer Resources"

## Interaction Flows

### Primary Navigation Flow
1. User lands on main platform page
2. Reviews available applications and features
3. Selects specific app (Speak, Score, etc.)
4. Navigates to dedicated app interface

### Demo Exploration Flow
1. User explores feature cards with hover effects
2. Clicks on demo links or "Try" CTAs
3. Navigates to specific demo interfaces
4. Returns to main platform for other features

### Documentation Flow
1. User seeks technical information
2. Accesses documentation cards
3. Views API documentation or guides
4. Implements platform integrations

### Sign-up/Authentication Flow
1. User clicks login/signup CTAs
2. Redirects to authentication interface
3. Completes registration or login
4. Returns to platform with authenticated state

## Technical Implementation

### Static HTML Structure
- **File Type:** Single HTML file with embedded CSS/JS
- **Styling:** CSS custom properties (variables)
- **Interactivity:** Vanilla JavaScript for interactions
- **Performance:** Optimized loading and minimal dependencies

### CSS Architecture
- **Custom Properties:** Consistent design system
- **Component Classes:** Reusable button and card styles
- **Responsive Design:** CSS Grid and Flexbox layouts
- **Animations:** CSS transitions and transforms

### Performance Considerations
- **Loading:** Optimized asset delivery
- **Responsiveness:** Fluid typography and layouts
- **Accessibility:** Proper semantic HTML structure
- **SEO:** Meta tags and structured content

## Integration Points

### App Launcher Functionality
- **Routing:** Links to individual application interfaces
- **State Management:** Potential shared authentication state
- **Branding:** Consistent visual identity across apps

### Analytics Integration
- **User Tracking:** Platform usage and navigation patterns
- **Conversion Tracking:** Sign-up and demo engagement
- **Performance Monitoring:** Page load and interaction metrics

### Authentication Integration
- **Single Sign-On:** Shared authentication across platform
- **User Management:** Centralized user account handling
- **Access Control:** Feature access based on user permissions

This landing page serves as the central hub for the entire LockN AI platform ecosystem, providing navigation, feature discovery, and user onboarding for the comprehensive suite of AI-powered applications.