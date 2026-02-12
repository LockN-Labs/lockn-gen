# LockN Score - Match History

## Screen Overview
**Screen Type:** Historical game data and navigation  
**App:** LockN Score  
**Journey:** Review and analyze past matches  
**Route:** `/history`  
**Component:** `pages/History.tsx`

## Layout Description

### Container Structure
- **Layout:** Vertical space with consistent spacing (space-y-6)
- **Background:** Transparent (inherits from app background)
- **Typography:** Consistent with app design system

### Header Section
- **Structure:** Standard header with metadata hierarchy
- **Label:** "History" (12px uppercase, wide tracking, slate-400)
- **Title:** "Past Games (V1.1)" (36px display font, white)
- **Description:** "Review past matches and trends for your team" (14px, slate-400)

## Main Content Section

### Container
- **Background:** `slate-900/70` with rounded 3xl corners
- **Border:** Ring-1 with `white/10` color
- **Padding:** 20px

### Section Header
- **Layout:** Flex justify-between, items-center
- **Margin:** Bottom 16px

#### Left Side
- **Title:** "Recent Games" (20px font-semibold, white)

#### Right Side
- **Link:** "View Full History →"
- **Styling:** 14px font-semibold, cyan (`neon`) color
- **Hover State:** Purple-400 color transition
- **Target:** `/history/player/:id` route

### Game List
- **Layout:** Vertical space with 12px gaps (space-y-3)
- **Items:** Individual game history cards

### Game History Cards
Each game entry contains:

#### Container
- **Layout:** Flex justify-between, items-center
- **Background:** `slate-950/60`
- **Border Radius:** Rounded 2xl
- **Padding:** 16px all sides

#### Left Content
- **Opponent Name:** 14px font-semibold, white
- **Date:** 12px, slate-400
- **Layout:** Stacked vertically

#### Right Content
- **Score:** 18px font-semibold, cyan (`neon`) color
- **Format:** "XX - YY" score display

## Data Management

### Data Structure
```typescript
interface GameHistoryItem {
  id: string
  opponent: string
  score: string
  date: string
}
```

### Default Data (Fallback)
```javascript
[
  { id: "1", opponent: "Matchpoint Elite", score: "21 - 18", date: "Jan 12" },
  { id: "2", opponent: "Baseline Club", score: "21 - 16", date: "Jan 05" }
]
```

### API Integration
- **Endpoint:** `GET /api/games`
- **Fallback:** Mock data on API failure
- **Player ID:** Retrieved from local storage (default: 1)

## Component States

### Loading State
- **Display:** Skeleton cards or loading indicators
- **Games List:** Placeholder cards with loading animations
- **Duration:** During API fetch

### Data Loaded State
- **Games:** Full list of historical games
- **Interactive:** All links and navigation active
- **Sorting:** Most recent games first

### Empty State
- **Display:** "No games found" message
- **Styling:** Centered message in main container
- **Action:** Encourage first game creation

### Error State
- **Fallback:** Mock data displayed
- **No Error UI:** Graceful degradation
- **Retry:** Potential retry mechanism

### API Failure State
- **Behavior:** Continues with mock data
- **User Experience:** Seamless fallback
- **Background Retry:** Possible retry attempts

## Responsive Behavior

### Desktop (1200px+)
- **Layout:** Full-width container with generous spacing
- **Cards:** Comfortable sizing and padding
- **Typography:** Full scale text sizing
- **Hover States:** Enhanced interactive feedback

### Tablet (768px - 1199px)
- **Container:** Maintains single column layout
- **Cards:** Slightly compressed padding
- **Text:** Readable sizing maintained
- **Touch:** Optimized for touch interaction

### Mobile (< 768px)
- **Layout:** Single column with reduced spacing
- **Cards:** Compressed for smaller screens
- **Typography:** Scaled down but readable
- **Touch Targets:** Optimized for mobile interaction

## Text Content

### Headers & Labels
- "History" (section identifier)
- "Past Games (V1.1)" (main title)
- "Review past matches and trends for your team" (description)

### Section Headers
- "Recent Games" (content section title)

### Navigation Elements
- "View Full History →" (detailed view link)

### Game Information
- Opponent names (various club/player names)
- Score formats ("21 - 18", "21 - 16")
- Date formats ("Jan 12", "Jan 05")

### Empty/Error States
- "No games found" (empty state)
- Fallback data labels

## Interaction Flows

### Primary Navigation Flow
1. User views recent games list
2. Reviews game summaries and scores
3. Clicks "View Full History" for detailed view
4. Navigates to player-specific history page

### Game Detail Flow
1. User clicks on individual game (potential future feature)
2. Navigate to detailed game analysis
3. View full match statistics and timeline

### Player History Navigation
- **Target Route:** `/history/player/:id`
- **Player ID:** Sourced from local storage
- **Scope:** Player-specific historical data

## Transitions & Animations

### Page Load
- **Header:** Fade in animation
- **Cards:** Staggered reveal animation
- **Duration:** Smooth entry transitions

### Data Loading
- **Skeleton States:** Loading card animations
- **Progressive Reveal:** Data appears as loaded
- **Smooth Transitions:** No jarring state changes

### Interactive Elements
- **Card Hover:** Subtle elevation or color shifts
- **Link Hover:** Color transition effects
- **Button States:** Smooth state transitions

## Technical Notes

### State Management
- **Local State:** `useState` for history data
- **Player ID:** Local storage integration
- **Effect Hooks:** `useEffect` for data fetching

### API Integration
- **HTTP Method:** GET request
- **Error Handling:** Try-catch with fallback data
- **Response Validation:** Array type checking

### Performance Considerations
- **Data Caching:** Consider caching historical data
- **Pagination:** Future consideration for large datasets
- **Lazy Loading:** Potential optimization for many games

### Local Storage
- **Player ID:** Persistent user identification
- **Fallback:** Default to player ID 1
- **Data Persistence:** Potential for local game caching

### Future Enhancements
- **Detailed Game Views:** Individual game analysis
- **Filtering:** Date range, opponent, score filters
- **Search:** Game search functionality
- **Export:** Data export capabilities
- **Statistics:** Performance trends and analytics

## Related Components
- Player profile management
- Game detail views (future)
- Statistics and analytics
- Navigation and routing utilities

## Data Flow
1. Component mounts with player ID from storage
2. Initiates API request for game history
3. Falls back to mock data on API failure
4. Renders game list with navigation options
5. Handles user interactions for detailed views

## Error Handling
- **Network Failures:** Graceful fallback to mock data
- **Invalid Responses:** Type checking and validation
- **Missing Data:** Default values and empty states
- **User Experience:** No error interruption of core functionality