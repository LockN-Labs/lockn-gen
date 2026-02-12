# LockN AI Platform - Waitlist & Beta Access

## Screen Overview
**Screen Type:** User acquisition and waitlist signup  
**App:** LockN AI Platform  
**Journey:** Beta access registration and user onboarding  
**Route:** `/waitlist/`  
**Component:** `web/waitlist/index.html`

## Layout Description

### Container Structure
- **Background:** Dark theme (`--bg: #06070a`)
- **Max Width:** 520px centered
- **Margin:** 4rem auto 2rem
- **Padding:** 0 2rem horizontal

### CSS Design System
```css
:root {
  --primary: #00d4ff;
  --secondary: #7b2cbf;
  --bg: #06070a;
  --surface: rgba(255,255,255,0.04);
  --border: rgba(255,255,255,0.08);
  --text: #f2f3f5;
  --text-muted: #8a8f98;
  --success: #4ade80;
  --info: #60a5fa;
}
```

## Header Section

### Icon Display
- **Size:** 4rem font-size
- **Icon:** 🔐 lock emoji or equivalent
- **Margin:** Bottom 1.5rem

### Title
- **Text:** "Waitlist & Beta Access" (or similar)
- **Font Size:** 2rem
- **Styling:** Gradient text (primary → secondary)
- **Background Clip:** Text with transparent fill
- **Margin:** Bottom 1rem

### Subtitle
- **Font Size:** 1.1rem (larger than body)
- **Color:** `--text-muted`
- **Line Height:** 1.6 for readability
- **Margin:** Bottom 2rem
- **Content:** Platform value proposition

## User Information Card

### Card Container
- **Background:** `--surface` (4% white opacity)
- **Border:** 1px solid `--border` (8% white opacity)
- **Border Radius:** 16px
- **Padding:** 2rem
- **Margin Bottom:** 2rem

### User Profile Section

#### Avatar & Info Layout
- **Layout:** Flex with 1rem gap, items-center
- **Margin Bottom:** 1.5rem

#### Avatar Component
- **Size:** 64px × 64px circular
- **Background:** Linear gradient (primary → secondary)
- **Content:** User initials or profile image
- **Fallback:** Centered text (1.5rem font, white)
- **Image Styling:** 100% size, border-radius 50%, object-fit cover

#### User Details
- **Name:** Large text (1.25rem), semibold weight
- **Email:** Smaller text (0.9rem), muted color
- **Layout:** Stacked vertically

### Status Display

#### Status Badge
- **Layout:** Inline-flex with center alignment
- **Padding:** 0.5rem 1rem
- **Border Radius:** 24px (pill shape)
- **Font Size:** 0.85rem
- **Font Weight:** 600
- **Text Transform:** Uppercase

#### Status Variants
```css
.status-pending {
  background: rgba(96, 165, 250, 0.2);
  color: var(--info);
}
.status-approved {
  background: rgba(74, 222, 128, 0.2);
  color: var(--success);
}
.status-waitlist {
  background: rgba(250, 204, 21, 0.2);
  color: #facc15;
}
```

### Position Information
- **Display:** Waitlist position when applicable
- **Format:** "Position #X in line" or similar
- **Font:** Monospace for numbers
- **Color:** Muted text

## Action Buttons Section

### Button Container
- **Layout:** Flex column with 1rem gaps
- **Margin:** Top auto (pushed to bottom)

### Primary Action Button
- **Width:** Full width
- **Padding:** 1rem
- **Border Radius:** 12px
- **Font Weight:** 600
- **Font Size:** 1rem
- **Background:** Linear gradient (primary → secondary)
- **Color:** White
- **Transition:** All 0.2s

#### Hover Effects
- **Transform:** translateY(-2px)
- **Box Shadow:** 0 8px 24px primary with 30% opacity
- **Brightness:** Slight increase

### Secondary Actions
- **Style:** Ghost buttons with border
- **Background:** Transparent
- **Border:** 1px solid `--border`
- **Color:** `--text`
- **Hover:** Border color changes to primary

## Features Overview Section

### Grid Layout
- **Display:** Grid with responsive columns
- **Grid Template:** `repeat(auto-fit, minmax(200px, 1fr))`
- **Gap:** 1rem between feature cards
- **Margin:** Top 2rem

### Feature Cards

#### Card Structure
- **Background:** `--surface`
- **Border:** 1px solid `--border`
- **Border Radius:** 12px
- **Padding:** 1.5rem
- **Text Alignment:** Center

#### Card Content
- **Icon:** Large emoji or SVG (2rem size)
- **Title:** 1.1rem font-weight 600
- **Description:** Small text, muted color
- **Margin:** Appropriate spacing between elements

### Feature Examples
1. **AI Voice Cloning:** "🎙️ Voice Cloning"
2. **Real-time Scoring:** "🏓 Live Sports Analytics"
3. **Multi-modal AI:** "🧠 Integrated AI Suite"
4. **Developer APIs:** "⚡ API Access"

## Social Proof Section

### Stats Display
- **Layout:** Grid with even columns
- **Text Alignment:** Center
- **Margin:** Top 2rem

### Individual Stats
- **Number:** Large text (2rem), primary color gradient
- **Label:** Small text, muted color
- **Examples:** "500+ Beta Users", "10k+ API Calls", "99.9% Uptime"

### Testimonials (Optional)
- **Layout:** Carousel or static cards
- **Content:** User quotes with attribution
- **Styling:** Italic text with quotation marks

## FAQ Section (Expandable)

### FAQ Container
- **Layout:** Accordion-style expandable sections
- **Border:** Top border for section separation

### Question & Answer Pairs
- **Question:** Clickable header with expand/collapse icon
- **Answer:** Hidden/shown content area
- **Animation:** Smooth height transitions

### Common Questions
- "When will I get access?"
- "What's included in the beta?"
- "Is it free during beta?"
- "How do I use the API?"

## Form Components (If Signup Required)

### Email Input
- **Width:** Full width
- **Padding:** 1rem
- **Border:** 1px solid `--border`
- **Border Radius:** 8px
- **Background:** Darker surface color
- **Focus State:** Primary border color

### Submit Button
- **Styling:** Matches primary action button
- **Loading State:** Spinner animation
- **Disabled State:** Reduced opacity

### Validation Messages
- **Error:** Red text with warning icon
- **Success:** Green text with checkmark
- **Position:** Below form fields

## Component States

### Loading State
- **Spinner:** Rotating animation
- **Text:** "Loading your status..."
- **Disabled:** All interactive elements

### Authenticated State
- **Display:** User information and current status
- **Actions:** Status-appropriate buttons
- **Personalization:** Customized messaging

### Unauthenticated State
- **Display:** Generic signup form
- **CTA:** "Join Waitlist" or similar
- **Social Login:** Optional OAuth buttons

### Success State
- **Message:** Confirmation of signup
- **Next Steps:** Clear instructions
- **Social Sharing:** Optional sharing buttons

### Error State
- **Message:** Clear error description
- **Actions:** Retry mechanisms
- **Support:** Contact information

## Responsive Behavior

### Desktop (520px+)
- **Container:** Full max-width maintained
- **Grid:** Multi-column feature layout
- **Typography:** Full scale sizing
- **Spacing:** Generous margins and padding

### Tablet (400px - 519px)
- **Container:** Reduced max-width
- **Grid:** May reduce to fewer columns
- **Spacing:** Slightly compressed
- **Touch:** Optimized for touch interaction

### Mobile (< 400px)
- **Container:** Minimal side padding
- **Grid:** Single column layout
- **Typography:** Reduced sizing
- **Spacing:** Compact but readable

## Text Content

### Headers & Titles
- "Waitlist & Beta Access" (main title)
- "Join the LockN AI Beta" (CTA section)
- Feature titles and descriptions

### Status Messages
- "You're in!" (approved status)
- "Position #X in line" (waitlist position)
- "Access Pending" (waiting status)

### Action Labels
- "Access Dashboard" (approved users)
- "Join Waitlist" (new users)
- "Update Profile" (existing users)
- "Share with Friends" (social actions)

### Feature Descriptions
- Brief, compelling descriptions of platform capabilities
- Benefits-focused messaging
- Technical accuracy with marketing appeal

### FAQ Content
- Common questions about beta access
- Platform capabilities and limitations
- Timeline and expectations

## Interaction Flows

### New User Signup Flow
1. User lands on waitlist page
2. Reviews platform features and benefits
3. Enters email (and optionally other info)
4. Submits signup form
5. Receives confirmation and position

### Existing User Check Flow
1. User visits page (potentially with token)
2. System checks current status
3. Displays personalized status information
4. Provides appropriate next actions

### Status Update Flow
1. User status changes (approved/moved up)
2. Page updates with new information
3. New actions become available
4. User can proceed to platform access

### Social Sharing Flow
1. User clicks share button
2. Pre-populated share content appears
3. User shares via social platform
4. Potential referral tracking

## Technical Implementation

### Authentication Integration
- **OAuth:** Social login options
- **Email Verification:** Signup confirmation
- **Token Management:** Session handling
- **Status Checking:** Real-time status updates

### API Integration
- **Signup Endpoint:** New user registration
- **Status Endpoint:** Current user status
- **Updates Endpoint:** Real-time status changes
- **Analytics:** User interaction tracking

### Data Management
- **Local Storage:** User preferences
- **Session Storage:** Temporary status
- **Cookie Management:** Authentication tokens
- **State Persistence:** Form data preservation

### Performance Considerations
- **Loading Speed:** Fast initial page load
- **Progressive Enhancement:** Works without JavaScript
- **Caching:** Static asset optimization
- **Analytics:** User behavior tracking

## Conversion Optimization

### A/B Testing Elements
- **Headlines:** Value proposition variations
- **CTAs:** Button text and color testing
- **Social Proof:** Different stats and testimonials
- **Form Fields:** Required vs optional information

### User Experience Optimization
- **Friction Reduction:** Minimal required fields
- **Trust Building:** Security and privacy messaging
- **Expectation Setting:** Clear timeline communication
- **Follow-up:** Email sequences and updates

### Analytics Tracking
- **Conversion Funnel:** Signup completion rates
- **User Engagement:** Time on page, interactions
- **Source Attribution:** Traffic source tracking
- **Cohort Analysis:** User behavior patterns