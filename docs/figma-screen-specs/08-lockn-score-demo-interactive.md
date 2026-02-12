# LockN Score - Interactive Demo

## Screen Overview
**Screen Type:** Interactive demo and marketing experience  
**App:** LockN Score  
**Journey:** Product demonstration and lead generation  
**Route:** `/demo`  
**Component:** `pages/Demo.tsx`

## Layout Description

### Container Structure
- **Background:** Transparent with inherited app styling
- **Layout:** Full height with bottom padding for navigation
- **Max Width:** 1152px (max-w-6xl) centered
- **Spacing:** Consistent 24px gaps throughout (space-y-6)

### Overall Visual Hierarchy
```
┌─────────────────────────────────────┐
│            Header Banner            │
├─────────────────────────────────────┤
│         Live Demo Scoreboard        │
├─────────────────────────────────────┤
│        Interactive Controls         │
├─────────────────────────────────────┤
│         Feature Cards Grid          │
├─────────────────────────────────────┤
│         Upgrade Banner              │
├─────────────────────────────────────┤
│         Social Proof                │
├─────────────────────────────────────┤
│         Final CTA                   │
└─────────────────────────────────────┘
```

## Header Section

### Container
- **Layout:** Text-center alignment
- **Animation:** Framer Motion fade-up initial animation

### Content Structure
- **Badge:** "Interactive Demo" with special styling
- **Title:** "Experience LockN Score" (36px/48px display font)
- **Description:** Product explanation with max-width constraint

### Badge Styling
- **Background:** `neon/10` with `neon/20` ring
- **Text:** Cyan (`neon`) color, 12px uppercase, wide tracking
- **Padding:** 4px × 16px, rounded full
- **Margin:** Bottom 16px

### Typography
- **Title:** 36px (sm: 48px) display font, white
- **Description:** Slate-400, max-width lg (512px), centered

## Live Demo Section

### Scoreboard Component
- **Component:** `<ScoreBoard homeScore={home} awayScore={away} />`
- **State:** Live updating with simulation
- **Animation:** Real-time score changes

### Interactive Controls
- **Layout:** Flex row, centered, wrapped (flex-wrap)
- **Gap:** 12px between buttons
- **Buttons:** Score manipulation and game controls

### Control Buttons (ScoreButton)
Four main interaction buttons:
1. **"+ Home"** - Increment home score (max 11)
2. **"+ Away"** - Increment away score (max 11) 
3. **"Rally Hit"** - Increment rally counter
4. **"New Game"** - Reset all scores to 0

#### Button Styling
- **Background:** `slate-800` with white/10 ring
- **Hover:** `slate-700` background, `neon/30` ring
- **Active:** Scale 95% (active:scale-95)
- **Text:** 14px semibold, white
- **Padding:** 8px × 16px, rounded xl
- **Transition:** Smooth hover and active states

### Rally Counter Component
- **Component:** `<RallyCounter rallyCount={rally} />`
- **Display:** Current rally count
- **Integration:** Updates with "Rally Hit" button

## Auto-Simulation System

### Automated Demo
- **Interval:** 3.5 seconds between updates
- **Logic:** Probabilistic score and rally changes
  - 40% chance: Rally increment
  - 20% chance: Home score (reset rally)
  - 20% chance: Away score (reset rally)
  - 20% chance: No change

### State Management
```javascript
const [home, setHome] = useState(7)
const [away, setAway] = useState(5)
const [rally, setRally] = useState(3)
```

## Feature Cards Grid

### Layout
- **Grid:** Responsive grid layout
  - Base: Single column
  - sm: 2 columns (sm:grid-cols-2)
  - lg: 3 columns (lg:grid-cols-3)
- **Gap:** 16px between cards

### Card Types

#### 1. AI Camera Scoring (Unlocked)
- **Icon:** 📹
- **Title:** "AI Camera Scoring"
- **Description:** "Point your phone at the court. LockN tracks the ball and scores automatically."
- **Demo Element:** Simulated live feed indicator

#### 2. Voice Commands (Unlocked)
- **Icon:** 🎙️
- **Title:** "Voice Commands" 
- **Description:** '"Score!", "Undo", "New game" — hands-free control while you play.'
- **Demo Element:** Listening indicator with pulse animation

#### 3. Leaderboards (Unlocked)
- **Icon:** 🏆
- **Title:** "Leaderboards"
- **Description:** "Track your stats across games, venues, and friends."
- **Demo Element:** `<HighScoreBoard>` with sample data

#### 4. Advanced Analytics (Locked)
- **Icon:** 📊
- **Title:** "Advanced Analytics"
- **Description:** "Win rates, rally distributions, streak analysis, and more."
- **State:** Locked feature
- **Action:** Opens lead capture modal

#### 5. Multiplayer Sync (Locked)
- **Icon:** 👥
- **Title:** "Multiplayer Sync"
- **Description:** "Real-time score sync across devices. Everyone sees the same game."
- **State:** Locked feature

#### 6. Game History (Locked)
- **Icon:** 📜
- **Title:** "Game History"
- **Description:** "Full history of every game, searchable and exportable."
- **State:** Locked feature

### Demo Feature Card Component
```typescript
<DemoFeatureCard
  icon="📹"
  title="AI Camera Scoring"
  description="..."
  featureId="camera_scoring"
  locked={false}
  onLockedClick={() => openLeadModal("locked_feature")}
>
  {/* Demo content */}
</DemoFeatureCard>
```

## Upgrade Banner

### Component
- **Component:** `<UpgradeBanner onUpgradeClick={handleUpgrade} />`
- **Purpose:** Conversion-focused upgrade promotion
- **Action:** Triggers lead capture or checkout flow

### Behavior
- **Before Lead Capture:** Opens lead capture modal
- **After Lead Capture:** Direct checkout redirect

## Social Proof Section

### Layout
- **Container:** Centered text, py-8, space-y-4
- **Animation:** Framer Motion viewport trigger (once)

### Content Structure
- **Label:** "Trusted by players" (slate-500, uppercase, tracked)
- **Stats Grid:** Flex centered with gap-8

### Statistics Display
Three key metrics:
1. **"500+"** Beta signups
2. **"2,400+"** Games tracked  
3. **"4.8★"** Average rating

#### Stats Styling
- **Numbers:** 24px display font, white
- **Labels:** 14px, slate-400
- **Layout:** Centered stacked text

## Final CTA Section

### Layout
- **Container:** Text-center, pb-8 (bottom padding)
- **Button:** Large conversion-focused CTA
- **Disclaimer:** Small print below button

### CTA Button
- **Text:** "Join the Beta — Free to Start"
- **Styling:** 
  - Background: Cyan (`neon`)
  - Text: Dark slate-900, 18px display font semibold
  - Padding: 16px × 32px, rounded 2xl
  - Shadow: Glow effect
  - Hover: Brightness increase (hover:brightness-110)

### Disclaimer
- **Text:** "No credit card required for the waitlist"
- **Styling:** 14px, slate-500, margin-top 12px

## Lead Capture Modal

### Component
- **Component:** `<LeadCaptureModal>`
- **Trigger Events:** Multiple interaction points
- **State Management:** Open/close state with trigger tracking

### Modal Props
```typescript
<LeadCaptureModal
  open={modalOpen}
  onClose={() => setModalOpen(false)}
  onSubmit={handleLeadSubmit}
  trigger={modalTrigger}
/>
```

### Trigger Types
- **"auto"** - Automatic based on engagement
- **"engagement"** - After 4+ interactions
- **"upgrade_cta"** - Upgrade banner click
- **"locked_feature"** - Locked feature click
- **"bottom_cta"** - Final CTA click

## Interaction Tracking

### Analytics Integration
- **Library:** Custom analytics (`lib/analytics`)
- **Events:** User interaction and engagement tracking

### Tracked Events
- **Page View:** "demo_page_view"
- **Time Spent:** "demo_time_spent" (on unmount)
- **Lead Form Open:** "demo_lead_form_open" with trigger
- **Feature Interactions:** Individual feature tracking

### Engagement Logic
```javascript
const interactionCount = useRef(0)
const handleInteraction = useCallback(() => {
  interactionCount.current += 1
  if (!leadCaptured && interactionCount.current >= 4) {
    setModalTrigger("engagement")
    setModalOpen(true)
  }
}, [leadCaptured])
```

## Component States

### Initial State
- **Scores:** Home: 7, Away: 5, Rally: 3
- **Auto-simulation:** Active and running
- **Lead Capture:** Not triggered
- **Modal:** Closed

### Engaged State
- **Interactions:** User actively clicking controls
- **Tracking:** Interaction count incrementing
- **Features:** Responding to user input
- **Animation:** Live updates and feedback

### Lead Captured State
- **Modal:** Closed after successful submission
- **Behavior:** Upgrade button direct to checkout
- **Tracking:** Lead submission recorded
- **UI:** Potential success indicators

### Locked Feature Interaction
- **Trigger:** Lead capture modal opens
- **Context:** "locked_feature" trigger type
- **Purpose:** Feature-driven conversion

## Responsive Behavior

### Desktop (1200px+)
- **Grid:** Full 3-column feature layout
- **Controls:** Horizontal button row
- **Typography:** Full scale sizing
- **Spacing:** Generous padding and margins

### Tablet (768px - 1199px)
- **Grid:** 2-column feature layout
- **Controls:** May wrap to multiple rows
- **Social Proof:** Maintains horizontal stats
- **Touch:** Optimized for touch interaction

### Mobile (< 768px)
- **Grid:** Single column throughout
- **Controls:** Stacked or wrapped buttons
- **Typography:** Scaled down appropriately
- **CTA:** Full-width button styling

## Transitions & Animations

### Page Entry
- **Header:** Fade up from -10px y offset
- **Duration:** Smooth entrance animation
- **Sequencing:** Staggered component reveals

### Score Updates
- **Live Updates:** Smooth number transitions
- **Button Interactions:** Scale feedback on click
- **Rally Counter:** Animated value changes

### Modal Triggers
- **Lead Capture:** Smooth modal entrance
- **Background:** Overlay fade-in
- **Content:** Modal slide-in animation

### Social Proof
- **Viewport Trigger:** Animation on scroll into view
- **Once:** Animation plays only once
- **Stats:** Number count-up animations (potential)

## Technical Notes

### State Management
- **Score State:** Local state with simulation
- **Lead State:** Capture status and modal control
- **Interaction Tracking:** Ref-based counting
- **Time Tracking:** Session duration measurement

### Auto-Simulation
- **Interval:** 3.5 second timer
- **Cleanup:** Proper interval clearance
- **Logic:** Probabilistic state updates
- **Limits:** Score caps at 11 points

### Performance Considerations
- **Animation Optimization:** Efficient re-renders
- **Event Tracking:** Debounced analytics calls
- **Modal Management:** Proper cleanup and memory management
- **Timer Management:** Cleanup on unmount

### Integration Points
- **Analytics:** Custom tracking implementation
- **Lead Capture:** Form submission handling
- **Checkout Flow:** External URL redirection
- **Environment:** Dynamic checkout URL configuration

## Related Components
- `ScoreBoard` - Live scoring display
- `RallyCounter` - Rally count visualization
- `HighScoreBoard` - Leaderboard display
- `DemoFeatureCard` - Feature showcase cards
- `LeadCaptureModal` - Conversion modal
- `UpgradeBanner` - Upgrade promotion

## Conversion Optimization
- **Multiple CTAs:** Various trigger points throughout
- **Social Proof:** Credibility building elements
- **Interactive Demo:** Hands-on product experience
- **Progressive Disclosure:** Locked features create interest
- **Analytics:** Data-driven optimization tracking