# LockN Score - Player History & Statistics

## Screen Overview
**Screen Type:** Detailed player performance analytics  
**App:** LockN Score  
**Journey:** Individual player statistics and game history analysis  
**Route:** `/history/player/:id`  
**Component:** `pages/PlayerHistory.tsx`

## Layout Description

### Container Structure
- **Layout:** Vertical space with consistent spacing (space-y-6)
- **Background:** Transparent (inherits from app background)
- **Typography:** Consistent with app design system

### Header Section
- **Structure:** Standard header with metadata hierarchy
- **Label:** "Player History" (12px uppercase, wide tracking, slate-400)
- **Title:** "Player #[ID] Stats & History" (36px display font, white)
- **Description:** "Comprehensive performance metrics and game history" (14px, slate-400)

## Performance Stats Section

### Container
- **Background:** `slate-900/70` with rounded 3xl corners
- **Border:** Ring-1 with `white/10` color
- **Padding:** 20px

### Section Header
- **Title:** "Performance Stats" (20px font-semibold, white)
- **Margin:** Bottom 16px

### Stats Grid Layout
- **Grid:** `grid-cols-2` base, `sm:grid-cols-4` on small screens+
- **Gap:** 16px between stat cards

### Individual Stat Cards
8 total performance metrics displayed:

#### 1. Games Played
- **Container:** Rounded 2xl, `slate-950/60` background, 16px padding
- **Label:** "Games Played" (12px, slate-400)
- **Value:** Large number (24px font-bold, white)

#### 2. Wins
- **Styling:** Same container as above
- **Label:** "Wins" 
- **Value:** Win count (24px font-bold, cyan/`neon` color)

#### 3. Losses  
- **Styling:** Same container
- **Label:** "Losses"
- **Value:** Loss count (24px font-bold, red-500 color)

#### 4. Win Rate
- **Styling:** Same container
- **Label:** "Win Rate"
- **Value:** Percentage (24px font-bold, purple-400 color)
- **Format:** Calculated as `((rate || 0) * 100).toFixed(1)%`

#### 5. Average Rally Length
- **Styling:** Same container
- **Label:** "Avg Rally Length"
- **Value:** Seconds with decimal (24px font-bold, white)
- **Format:** `stats.avg_rally_length.toFixed(1)s`

#### 6. Best Rally
- **Styling:** Same container
- **Label:** "Best Rally"
- **Value:** Number (24px font-bold, white)

#### 7. High Score
- **Styling:** Same container
- **Label:** "High Score" 
- **Value:** Number (24px font-bold, yellow-400 color)

#### 8. Last Updated
- **Styling:** Same container
- **Label:** "Last Updated"
- **Value:** Formatted date (14px font-medium, white)
- **Format:** `new Date(stats.last_updated).toLocaleDateString()`

## Game History Section

### Container
- **Background:** `slate-900/70` with rounded 3xl corners
- **Border:** Ring-1 with `white/10` color
- **Padding:** 20px

### Section Header
- **Layout:** Flex justify-between, items-center
- **Title:** "Game History" (20px font-semibold, white)
- **Count:** "[X] games" (14px, slate-400)
- **Margin:** Bottom 16px

### Game List Layout
- **Spacing:** 12px vertical gaps (space-y-3)
- **Empty State:** Centered message when no games

### Individual Game Cards
Each game displays comprehensive match information:

#### Card Container
- **Background:** Conditional based on win/loss
  - **Win:** `neon/10` background with `neon/50` ring
  - **Loss:** `slate-950/60` background with `white/10` ring
- **Border Radius:** Rounded 2xl
- **Padding:** 16px
- **Transition:** Smooth color transitions

#### Card Layout Structure
- **Layout:** Flex column, gap 8px (sm: flex-row, items-center, justify-between)
- **Responsive:** Single column on mobile, row on larger screens

#### Player Information (Left Section)
- **Player Role:** "Player 1" or "Player 2" (14px font-semibold, white)
- **Date:** Game date (12px, slate-400)
- **Layout:** Stacked vertically

#### Score Display (Center Section)
- **Layout:** Flex items-center, gap 16px
- **Your Score:** 
  - Number: 24px font-bold, white
  - Label: "You" (12px, slate-400)
- **Versus:** "vs" text (slate-500)
- **Opponent Score:**
  - Number: 24px font-bold, white
  - Label: Opponent name or "Unknown" (12px, slate-400)

#### Result & Metadata (Right Section)
- **Win/Loss Badge:**
  - **Win:** Cyan background, dark text, "WIN" label
  - **Loss:** Red background/20, red-400 text, "LOSS" label
  - **Styling:** Rounded full, 12px font-bold, px-3 py-1

- **Game Metadata:** (12px, slate-400, flex with gaps)
  - Rally count: "[X] rallies"
  - Average rally length: "• [X]s avg" (if available)
  - Duration: "• [MM:SS]" (if available)

### Duration Formatting
```typescript
const formatDuration = (seconds: number | null) => {
  if (!seconds) return null
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, "0")}`
}
```

## Component States

### Loading State
- **Display:** Centered loading animation
- **Spinner:** 48px × 48px spinning ring (cyan border, transparent top)
- **Text:** "Loading player data..." (slate-400)
- **Layout:** Full height centered container

### Error State  
- **Display:** Centered error message
- **Text:** "Error: [message]" (red-500 color)
- **Layout:** Full height centered container

### No Data State
- **Display:** "No data found for this player" (slate-400)
- **Condition:** When `!stats && player_id > 0`
- **Layout:** Centered message

### Empty Games State
- **Display:** "No games recorded yet." in games section
- **Container:** Centered padding, py-8
- **Text Color:** slate-400

### Data Loaded State
- **Stats Section:** Full performance metrics displayed
- **Games Section:** Complete game history with win/loss styling
- **Interactive:** All data visible and properly formatted

## Data Management

### API Integration
- **Endpoints:** 
  - `GET /api/players/${player_id}/stats`
  - `GET /api/players/${player_id}/games`
- **Method:** Parallel Promise.all requests
- **Error Handling:** Individual endpoint failure handling

### Data Structures

#### PlayerStats Interface
```typescript
interface PlayerStats {
  id: number
  player_id: number
  games_played: number
  wins: number
  losses: number
  win_rate: number
  avg_rally_length: number
  best_rally: number
  high_score: number
  last_updated: string
}
```

#### PlayerGame Interface  
```typescript
interface PlayerGame {
  id: number
  timestamp: string
  duration_seconds: number | null
  player1_name: string | null
  player2_name: string | null
  player1_score: number
  player2_score: number
  winner_name: string | null
  rally_count: number
  avg_rally_length: number | null
}
```

### Game Logic Processing
```typescript
const isPlayer1 = game.player1_name !== null
const playerScore = isPlayer1 ? game.player1_score : game.player2_score
const opponentScore = isPlayer1 ? game.player2_score : game.player1_score
const opponentName = isPlayer1 ? game.player2_name : game.player1_name
const isWin = game.winner_name !== null && 
  game.winner_name === (isPlayer1 ? game.player1_name : game.player2_name)
```

## Responsive Behavior

### Desktop (1200px+)
- **Stats Grid:** Full 4-column layout for statistics
- **Game Cards:** Row layout with all information visible
- **Typography:** Full scale text sizing
- **Spacing:** Generous padding and margins

### Tablet (768px - 1199px)
- **Stats Grid:** Maintains 4-column on sm+ screens  
- **Game Cards:** May compress to single row with wrapping
- **Text:** Readable sizing maintained

### Mobile (< 768px)
- **Stats Grid:** 2-column layout (grid-cols-2)
- **Game Cards:** Single column layout (flex-col)
- **Typography:** Compressed but readable
- **Touch:** Optimized for mobile interaction

## Text Content

### Headers & Labels
- "Player History" (section identifier)
- "Player #[ID] Stats & History" (main title)
- "Comprehensive performance metrics and game history" (description)

### Section Headers
- "Performance Stats" 
- "Game History"

### Stat Labels
- "Games Played", "Wins", "Losses", "Win Rate"
- "Avg Rally Length", "Best Rally", "High Score", "Last Updated"

### Game Information
- Player roles: "Player 1", "Player 2", "You"
- Result badges: "WIN", "LOSS"
- Metadata: rallies, averages, duration

### State Messages
- "Loading player data..."
- "No data found for this player"
- "No games recorded yet."
- API error messages

## Interaction Flows

### Successful Data Load Flow
1. Extract player ID from route parameters
2. Validate player ID > 0
3. Make parallel API requests for stats and games
4. Process and display performance metrics
5. Render game history with win/loss styling

### Error Handling Flow
1. API request fails
2. Error state displayed with specific message
3. User sees error but app remains functional
4. No retry mechanism currently implemented

### Empty Data Flow
1. API returns empty or null data
2. Appropriate empty state messages shown
3. User guided on what the empty state means

## Transitions & Animations

### Page Load
- **Initial:** Standard page entrance
- **Data Loading:** Loading spinner animation
- **Content Reveal:** Smooth transition from loading to content

### Data Updates
- **Stats:** Number updates if data refreshes
- **Games:** List updates with new game additions
- **Win/Loss:** Color transitions on game result changes

## Technical Notes

### Route Parameter Handling
```typescript
const { id } = useParams<{ id: string }>()
const player_id = id ? parseInt(id, 10) : 0
```

### Error Handling
- **Network Failures:** Try-catch around API requests
- **Data Validation:** Array and object type checking
- **Graceful Degradation:** Fallback values for missing data

### Performance Considerations
- **Parallel Requests:** Stats and games fetched simultaneously
- **Data Processing:** Client-side game analysis and formatting
- **Memory Management:** Proper cleanup of API responses

### Data Processing
- **Win Rate Calculation:** Percentage formatting with 1 decimal
- **Duration Formatting:** MM:SS format for game duration
- **Date Formatting:** Localized date display
- **Player Role Detection:** Logic to determine player 1 vs player 2

## Related Components
- Player profile management
- Game detail views (potential future feature)
- Statistics calculation utilities
- API response processing utilities
- Route parameter handling

## Future Enhancements
- **Interactive Charts:** Visual representation of performance trends
- **Filtering:** Date range, opponent, game type filters
- **Comparison:** Multi-player performance comparison
- **Export:** Data export capabilities
- **Real-time Updates:** Live statistics updates