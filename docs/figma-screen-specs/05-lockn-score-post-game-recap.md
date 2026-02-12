# LockN Score - Post-Game Recap (Journey 4)

## Screen Overview
**Screen Type:** Match summary and statistics  
**App:** LockN Score  
**Journey:** Journey 4 - Post-Game Recap (final score, stats, highlights, share)  
**Route:** `/recap/:sessionId` (planned)  
**Component:** Not yet implemented (types defined in `components/recap/types.ts`)

## Layout Description

### Container Structure
- **Background:** Consistent with app theme (dark slate)
- **Layout:** Full-width responsive container
- **Padding:** Standard app padding (24px)
- **Typography:** Mixed scale for hierarchy

### Planned Section Layout
```
┌─────────────────────────────────────┐
│         Match Header                │
├─────────────────────────────────────┤
│      Final Score Display            │
├─────────────────────────────────────┤
│      Player Statistics              │
├─────────────────────────────────────┤
│      Momentum Chart                 │
├─────────────────────────────────────┤
│      Match Highlights               │
├─────────────────────────────────────┤
│      Timeline & Moments             │
├─────────────────────────────────────┤
│      Share & Actions                │
└─────────────────────────────────────┘
```

## Match Header Section

### Content Elements
- **Match Type:** Game mode indicator
- **Players:** Player information and avatars
- **Duration:** Total match duration
- **Date/Time:** When match was played

### Data Structure (MatchMeta)
```typescript
interface MatchMeta {
  duration: string
  totalRallies: number
  playedAt: string
}
```

### Visual Layout
- **Background:** Dark container with borders
- **Typography:** Large title, medium metadata
- **Player Avatars:** Circular images with colors
- **Meta Info:** Duration, rally count, timestamp

## Final Score Display Section

### Player Information (RecapPlayer)
```typescript
interface RecapPlayer {
  id: string
  name: string
  avatarUrl: string
  color: string  
  score: number
}
```

### Score Presentation
- **Layout:** Two-player comparison display
- **Player Cards:** Avatar, name, final score
- **Winner Indication:** Visual highlighting of winner
- **Color Coding:** Player-specific color schemes

### Score Typography
- **Final Scores:** Very large, prominent numbers
- **Player Names:** Medium, readable sizing
- **Winner Badge:** Special styling for match winner

## Player Statistics Section

### Stat Line Structure (PlayerStatLine)
```typescript
interface PlayerStatLine {
  key: string
  label: string
  leftValue: number
  rightValue: number
  displayLeft: string
  displayRight: string
  winner: "left" | "right" | "tie"
}
```

### Statistics Categories
- **Rally Performance:** Longest rally, average rally length
- **Serve Statistics:** Service points won, aces
- **Point Patterns:** Winning shots, errors
- **Consistency:** Shot accuracy, rally participation

### Visual Presentation
- **Comparison Layout:** Side-by-side player stats
- **Winner Highlighting:** Color coding for best performer
- **Progress Bars:** Visual representation of stat comparisons
- **Icons:** Category identification with iconography

## Momentum Chart Section

### Data Structure (MomentumPoint)
```typescript
interface MomentumPoint {
  point: number
  leftScore: number
  rightScore: number
}
```

### Chart Features
- **X-Axis:** Point progression through match
- **Y-Axis:** Score differential or momentum indicator
- **Line Chart:** Match flow visualization
- **Key Moments:** Highlighted turning points
- **Interactive Elements:** Hover/touch for point details

### Momentum Visualization
- **Score Progression:** How scores changed over time
- **Comeback Moments:** Visual identification of rallies
- **Dominance Periods:** Extended scoring runs
- **Close Battles:** Tight score situations

## Match Highlights Section

### Highlight Structure
```typescript
type HighlightCategory = "🔥 Rally" | "🏆 Winner" | "💪 Clutch"

interface HighlightItem {
  id: string
  category: HighlightCategory
  title: string
  description: string
  timestamp: string
}
```

### Highlight Categories
- **🔥 Rally:** Exceptional rally lengths or quality
- **🏆 Winner:** Match-winning points or shots
- **💪 Clutch:** High-pressure moments and responses

### Visual Presentation
- **Card Layout:** Individual highlight cards
- **Category Icons:** Emoji-based visual categorization
- **Timestamps:** When highlights occurred
- **Descriptions:** Narrative explanation of moments

## Match Timeline Section

### Timeline Structure (TimelineMoment)
```typescript
interface TimelineMoment {
  point: number
  label: string
}
```

### Timeline Features
- **Chronological Flow:** Key moments in sequence
- **Point References:** Specific point numbers
- **Event Labels:** Descriptive moment labels
- **Interactive Timeline:** Clickable/touchable moments

### Timeline Content
- **Game Start/End:** Major match milestones
- **Set Breaks:** Natural match boundaries
- **Momentum Shifts:** Significant turning points
- **Special Events:** Unusual or noteworthy occurrences

## Match Narrative Section

### Narrative Categories
```typescript
type NarrativeCategory = "Dominant" | "Comeback" | "Close Battle" | "Marathon"
```

### Narrative Generation
- **Dominant:** One-sided match analysis
- **Comeback:** Behind-to-victory story
- **Close Battle:** Tight competition narrative
- **Marathon:** Extended match emphasis

### Content Elements
- **Match Summary:** AI/algorithm-generated match story
- **Key Turning Points:** Critical moment identification
- **Player Performance:** Individual player narratives
- **Statistical Insights:** Numbers that tell the story

## Share & Actions Section

### Sharing Features
- **Social Media Integration:** Direct platform sharing
- **Image Generation:** Match summary graphics
- **Link Sharing:** Session replay links
- **Statistics Export:** Data download options

### Action Items
- **Save Match:** Bookmark for future reference
- **Download Report:** PDF or image export
- **Share Results:** Social media posting
- **Challenge Rematch:** Initiate follow-up game

## Component States

### Loading State
- **Data Loading:** Match analysis in progress
- **Skeleton UI:** Placeholder content structure
- **Progress Indicators:** Analysis completion status

### Complete State
- **Full Data:** All statistics and highlights loaded
- **Interactive Elements:** All features functional
- **Sharing Ready:** Export capabilities active

### Error State
- **Data Error:** Match analysis failed
- **Retry Options:** Manual refresh capabilities
- **Fallback Content:** Basic score information

### Empty State
- **No Highlights:** Limited remarkable moments
- **Basic Stats:** Minimal statistical analysis
- **Simple Recap:** Essential information only

## Responsive Behavior

### Desktop (1200px+)
- **Full Layout:** All sections visible
- **Side-by-Side:** Player comparisons prominent
- **Charts:** Full-featured visualization
- **Sharing:** Desktop-optimized options

### Tablet (768px - 1199px)
- **Stacked Sections:** Vertical flow maintained
- **Touch Interactions:** Chart interactions optimized
- **Compressed Stats:** Efficient space usage

### Mobile (< 768px)
- **Single Column:** Linear information flow
- **Simplified Charts:** Mobile-friendly visualizations
- **Touch Sharing:** Native mobile sharing
- **Condensed Content:** Essential information priority

## Text Content

### Headers & Titles
- "Match Recap" / "Game Summary"
- "Final Score", "Player Statistics"
- "Match Highlights", "Timeline"

### Statistical Labels
- Rally performance metrics
- Serve statistics
- Point pattern analysis
- Consistency measurements

### Narrative Content
- Auto-generated match summaries
- Highlight descriptions
- Moment explanations
- Performance insights

### Action Labels
- "Share Results", "Save Match"
- "Download Recap", "View Details"
- "Challenge Rematch", "Return to Dashboard"

## Interaction Flows

### Primary Flow (Post-Match)
1. Match completes in live dashboard
2. Automatic redirect to recap screen
3. Data analysis begins (loading state)
4. Progressive content reveal as analysis completes
5. Full interactive recap available
6. User reviews performance and shares

### Navigation Flows
- **Return to Dashboard:** Primary exit point
- **Start New Game:** Quick rematch option
- **View History:** Access to match archive
- **Player Profile:** Deep dive into player stats

### Sharing Flows
- **Social Media:** Direct platform integration
- **Image Export:** Generated summary graphics
- **Link Sharing:** Shareable match URLs
- **Data Export:** Raw statistics download

## Transitions & Animations

### Content Reveal
- **Progressive Loading:** Sections appear as data loads
- **Staggered Animation:** Smooth content entrance
- **Chart Animations:** Data visualization entrance
- **Highlight Emphasis:** Special moment highlighting

### Interactive Elements
- **Chart Interactions:** Smooth hover/touch responses
- **Timeline Scrubbing:** Fluid moment navigation
- **Highlight Expansion:** Detailed view transitions

### Sharing Actions
- **Export Preparation:** Loading states for generation
- **Success Feedback:** Confirmation animations
- **Error Handling:** Graceful failure states

## Technical Notes

### Data Analysis
- **Real-time Processing:** Match data analysis during game
- **Statistical Computation:** Player performance calculations
- **Highlight Detection:** Algorithm-based moment identification
- **Narrative Generation:** Automated story creation

### Performance Considerations
- **Data Caching:** Match analysis result storage
- **Progressive Loading:** Incremental content delivery
- **Image Generation:** On-demand graphic creation
- **Export Optimization:** Efficient sharing formats

### Integration Points
- **Match Data:** Connection to live game data
- **Player Profiles:** Link to player statistics
- **Social Platforms:** Sharing API integration
- **Analytics:** User engagement tracking

## Related Components
- Statistics visualization components
- Chart and graph rendering
- Social sharing utilities
- Export and download managers

## Implementation Status
**Note:** This screen is planned but not yet implemented. The specification is based on type definitions found in `components/recap/types.ts`. The actual implementation would require building these components according to the defined interfaces and user experience requirements outlined above.