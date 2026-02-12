# LockN Score - Home Dashboard

## Screen Overview
**Screen Type:** Home/Dashboard  
**App:** LockN Score  
**Journey:** Entry point to all app functionality  
**Route:** `/` (root)  
**Component:** `pages/Home.tsx`

## Layout Description

### Container Structure
- **Outer Container:** Full viewport height with transparent background, slate text
- **Inner Container:** Max width 6xl (1152px), centered with responsive padding
- **Main Content:** Rounded 3xl container with dark background `#121620`, white/10 border
- **Grid Layout:** Large devices use `lg:grid-cols-[1.2fr_0.8fr]` split

### Header Section
- **Height:** Auto with padding  
- **Layout:** Flex row, items-center, justify-between
- **Left Side:**
  - App icon: 44px × 44px rounded square, cyan background with ping pong emoji
  - Text stack: "LOCKN SUITE" label (11px uppercase, tracked) + "LockN Score" title (20px semibold)
- **Right Side:**
  - Settings button: 40px circle, border, gear icon
  - User avatar: 40px circle, gradient background, "SK" initials

### Main Content Area (Left Panel - 1.2fr)
- **Background:** `#1C2130` with rounded corners and border
- **Padding:** 24px (6)
- **Content Structure:**
  - Subtitle: Small slate text "Ready to run your next session?"
  - Hero Title: 36px (lg) / 48px (sm) font-semibold, max-width lg, tight leading
  - CTA Button: 56px height, min-width 220px, cyan background `#4DD0E1`, dark text, uppercase tracking, shadow

### Sidebar (Right Panel - 0.8fr)
- **Background:** `#1C2130` matching main panel
- **Sections:**
  1. **Recent Games Header:** Flex justify-between with "View all" link
  2. **Games List:** Space-y-3 with animated cards
  3. **Game Cards:** Each with dark background, 16px padding, rounded corners
     - Game mode + time layout
     - Player info
     - Score display in cyan

### Quick Stats Footer
- **Layout:** Grid with 3 columns on sm+ screens
- **Background:** `#1C2130` with rounded corners
- **Items:** Stats cards with dark backgrounds, uppercase labels, large values

## Component States

### Loading State
- Skeleton placeholders for recent games
- Disabled CTA button
- Loading text in stats areas

### Empty State  
- "No recent games" message in sidebar
- Placeholder stats (0 values)
- CTA remains active

### Active State (Default)
- Live data in all sections
- Interactive hover states on buttons
- Animations on stat updates

### Error State
- Error boundaries for failed data loads
- Fallback UI for network issues
- Retry mechanisms

## Responsive Behavior

### Desktop (1200px+)
- Full two-panel layout
- Large text sizing
- Extended CTA button width

### Tablet (768px - 1199px)
- Maintains grid layout
- Reduced padding
- Smaller text scaling

### Mobile (< 768px)
- Single column stack
- Full-width elements
- Touch-friendly button sizing
- Compressed vertical spacing

## Text Content

### Primary Headlines
- "Ready to run your next session?"
- "Start a new game session for practice, rally challenge, or full match play."

### Button Labels
- "New Game" (primary CTA)
- "View all" (secondary link)

### Section Headers
- "Recent Games"
- Stats labels: "Games Played", "Win Rate", "Best Rally"

### Navigation
- "LOCKN SUITE" (app family label)
- "LockN Score" (app title)

## Interaction Flows

### Primary Flow
1. User lands on dashboard
2. Sees recent activity and stats
3. Clicks "New Game" CTA
4. Navigates to Session Creation (`/create`)

### Secondary Flows
- Settings button → Configuration modal/page
- User avatar → Profile/account menu
- Recent game card → Game details/replay
- "View all" → History page (`/history`)
- Stats section → Detailed stats page (`/stats`)

## Transitions & Animations

### Page Load
- Fade in animation for main content
- Staggered reveal for stats cards
- Smooth hover transitions

### Interactive Elements
- Button hover: brightness increase
- Card hover: subtle elevation/border glow
- Smooth color transitions (0.2s ease)

### Data Updates
- Live stats animate on change
- Recent games slide in from top
- Loading states with pulse animations

## Technical Notes

### Key Dependencies
- React Router for navigation
- Framer Motion for animations (implied)
- Tailwind CSS for styling
- Auth0 integration for user state

### Performance Considerations
- Lazy loading for heavy data
- Memoized expensive calculations
- Optimized re-renders for live data

### Accessibility
- Proper heading hierarchy
- ARIA labels for icon buttons
- Keyboard navigation support
- Screen reader compatibility

## Related Components
- `AuthButton` - Authentication state
- Navigation elements throughout app
- Shared design system tokens