# LockN Score - Admin Invites Management

## Screen Overview
**Screen Type:** Administrative interface for beta access management  
**App:** LockN Score  
**Journey:** Admin workflow for managing beta testers and early access invites  
**Route:** `/admin/invites`  
**Component:** `pages/admin/Invites.tsx`

## Layout Description

### Container Structure
- **Layout:** Vertical space with consistent spacing (space-y-6)
- **Background:** Transparent (inherits from app background)
- **Typography:** Consistent with app design system

### Header Section
- **Layout:** Flex column/row responsive layout (sm: flex-row)
- **Responsive:** Single column on mobile, row with space-between on larger screens

#### Left Side Content
- **Title:** "Invite Management" (24px display font-semibold, white)
- **Description:** "Manage beta tester and early access invitations" (14px, slate-400)

#### Right Side Action
- **CTA Button:** "Create Invite" with plus icon
- **Styling:** 
  - Background: Cyan (`neon`)
  - Text: Dark slate-900, 14px font-semibold
  - Padding: 12px × 20px, rounded 2xl
  - Shadow: Glow effect, hover brightness

## Filters Section

### Container
- **Background:** `slate-900/70` with rounded 3xl corners
- **Border:** Ring-1 with `white/10` color
- **Padding:** 20px
- **Layout:** Flex column/row responsive (sm: flex-row, items-center)

#### Search Input (Left Side)
- **Layout:** Flex-1 with relative positioning
- **Icon:** Search SVG positioned absolute left
- **Input Field:**
  - Background: `slate-950`
  - Width: Full
  - Padding: 10px × 40px × 10px × 16px (accommodating icon)
  - Border: `white/10` ring, focus: cyan ring
  - Placeholder: "Search by email..."
  - Text: 14px, white, placeholder slate-500

#### Status Filter (Right Side)  
- **Layout:** Flex items-center with gap
- **Label:** "Status:" (14px, slate-400)
- **Select:** 
  - Background: `slate-950`
  - Padding: 10px × 16px
  - Border: `white/10` ring, focus: cyan ring
  - Options: All, Pending, Accepted, Expired, Revoked

## Data Table Section

### Container
- **Background:** `slate-900/70` with rounded 3xl corners
- **Border:** Ring-1 with `white/10` color

### Loading State
- **Display:** Centered spinner with 32px diameter
- **Animation:** Spinning cyan ring with transparent top
- **Duration:** Shows during API requests

### Error State
- **Display:** Centered error message (red-400)
- **Retry:** "Try again" link (cyan, hover underline)
- **Layout:** Centered in py-16 container

### Empty State
- **Display:** "No invites found" (slate-400)
- **Layout:** Centered in py-16 container

### Desktop Table (Hidden on Mobile)
Full-featured table with columns:

#### Table Structure
- **Overflow:** Hidden with overflow-x-auto
- **Display:** `hidden md:block`

#### Table Headers
- **Styling:** Border-bottom, uppercase text (12px), wide tracking
- **Color:** slate-400
- **Columns:** Email, Role, Status, Invited At, Expires At, Actions
- **Padding:** 24px × 16px per cell

#### Table Rows
- **Hover:** Background `white/5`
- **Divider:** Between rows with `white/5`
- **Transition:** Smooth hover transitions

#### Column Content
1. **Email:** Font-medium, white text
2. **Role:** `<RoleBadge>` component  
3. **Status:** `<StatusBadge>` component
4. **Dates:** Formatted date strings (slate-400)
5. **Actions:** Icon button row (copy, resend, revoke)

### Mobile Cards (Visible on Mobile)
- **Display:** `divide-y divide-white/10 md:hidden`
- **Layout:** Stacked card format for mobile viewing

#### Mobile Card Structure
- **Padding:** 16px
- **Spacing:** 12px gaps (space-y-3)
- **Content:**
  - Email (font-medium, white)
  - Role and status badges (flex gap-2)
  - Date information (12px, slate-400)
  - Action buttons (flex gap-2)

## Badge Components

### StatusBadge Component
Color-coded status indicators:

#### Status Styling Map
```typescript
const styles: Record<Invite["status"], string> = {
  pending: "bg-yellow-500/20 text-yellow-400 ring-yellow-500/30",
  accepted: "bg-green-500/20 text-green-400 ring-green-500/30", 
  expired: "bg-slate-500/20 text-slate-400 ring-slate-500/30",
  revoked: "bg-red-500/20 text-red-400 ring-red-500/30"
}
```

#### Badge Structure
- **Layout:** Inline-flex items-center
- **Padding:** 2.5px × 10px (rounded-full)
- **Font:** 12px medium
- **Border:** Ring-1 with color-matched border

### RoleBadge Component
Role identification with styling:

#### Role Styling Map  
```typescript
const styles: Record<Invite["role"], string> = {
  "beta-tester": "bg-purple-500/20 text-purple-400",
  "early-access": "bg-neon/20 text-neon"
}
```

#### Role Labels
```typescript
const labels: Record<Invite["role"], string> = {
  "beta-tester": "Beta Tester", 
  "early-access": "Early Access"
}
```

## Action Icons & Interactions

### Copy Invite Link
- **Icon:** Copy/clipboard SVG (16px × 16px)
- **Action:** Copy invite URL to clipboard
- **Feedback:** Alert notification "Invite link copied to clipboard!"
- **Styling:** Slate-400, hover: slate-800 bg + white text

### Resend Invite (Disabled)
- **Icon:** Refresh/rotate SVG 
- **State:** Currently disabled (slate-600, cursor-not-allowed)
- **Title:** "Resend (coming soon)"
- **Note:** Placeholder for future functionality

### Revoke Invite
- **Icon:** X/cancel SVG (red-400)
- **Condition:** Only available for "pending" status
- **Confirmation:** Browser confirm dialog
- **Action:** DELETE API call
- **Hover:** Red background with lighter red text

## Pagination Controls

### Pagination Container
- **Location:** Bottom border of table
- **Padding:** 24px × 16px
- **Border:** Top border with `white/10`
- **Layout:** Flex justify-between, items-center

### Left Side: Summary
- **Format:** "Showing X to Y of Z invites"
- **Calculation:** `(page - 1) * limit + 1` to `Math.min(page * limit, total)`
- **Styling:** 14px, slate-400

### Right Side: Controls
- **Layout:** Flex items-center, gap 8px
- **Elements:** Previous button, page indicator, Next button

#### Pagination Buttons
- **Previous/Next:** 
  - Background: `slate-800`
  - Hover: `slate-700`
  - Disabled: opacity 50%, cursor not-allowed
  - Text: 14px, white
  - Padding: 6px × 12px, rounded lg

- **Page Indicator:**
  - Text: "Page X of Y" (14px, slate-400)

## Create Invite Modal

### Modal Backdrop
- **Overlay:** Fixed inset-0, black/60 with backdrop-blur
- **Z-index:** 50 for proper layering
- **Layout:** Flex centered items

### Modal Container
- **Background:** `slate-900` with rounded 3xl
- **Border:** Ring-1 with `white/10`
- **Width:** Full with max-width md (448px)
- **Padding:** 24px

### Modal Header
- **Layout:** Flex justify-between, items-center
- **Title:** "Create New Invite" / "Invite Created!" (18px font-semibold)
- **Close Button:** X icon, hover: `slate-800` bg

### Form State (Before Creation)

#### Email Input
- **Label:** "Email Address" (14px font-medium, slate-400)
- **Input:**
  - Type: email, required
  - Background: `slate-950`
  - Padding: 10px × 16px, rounded xl  
  - Border: `white/10` ring, focus: cyan ring
  - Placeholder: "user@example.com"

#### Role Selection
- **Label:** "Role" (14px font-medium, slate-400)
- **Select:**
  - Background: `slate-950`
  - Options: "Beta Tester", "Early Access"
  - Same styling as email input

#### Error Display
- **Container:** Red background/10, red border/20, rounded xl
- **Text:** 14px, red-400
- **Layout:** Padding 12px × 16px

#### Action Buttons
- **Layout:** Flex gap 12px, padding-top 8px
- **Cancel:** `slate-800` background, hover: `slate-700`
- **Create:** Cyan background, disabled: opacity 50%
- **Both:** Flex-1, rounded 2xl, 14px font-semibold

### Success State (After Creation)

#### Created Invite Display
- **Container:** Rounded 2xl, `slate-950/60` background, 16px padding
- **Content:** Email, role badge
- **Layout:** Invite confirmation details

#### Invite Link Section
- **Label:** "Invite Link" (14px, slate-400)
- **Layout:** Flex gap 8px
- **Input:** Read-only link display (`slate-950` bg)
- **Copy Button:** Cyan background, "Copy"/"Copied!" states

#### Done Button
- **Style:** Full width, `slate-800` background
- **Action:** Close modal and refresh data

## Component States

### Initial Load State
- **Table:** Loading spinner
- **Pagination:** Hidden
- **Search/Filters:** Enabled
- **Create Button:** Enabled

### Data Loaded State
- **Table:** Full invite list displayed
- **Pagination:** Visible if total > limit
- **Interactive:** All features functional
- **Modal:** Ready for creation

### Search/Filter State
- **Debounced:** 300ms delay on search input
- **Reset Pagination:** Page 1 when filters change
- **Loading:** Brief loading state during filter application

### Modal States
- **Closed:** Not rendered (conditional)
- **Form:** Input validation and submission
- **Loading:** During invite creation
- **Success:** Confirmation with invite link
- **Error:** Form validation or API errors

## Data Management

### API Integration
- **Base URL:** Environment variable with fallback
- **Endpoints:**
  - `GET /api/admin/invites` (with query params)
  - `POST /api/admin/invites` (create)
  - `DELETE /api/admin/invites/:id` (revoke)

### Query Parameters
- **limit:** Items per page (default: 10)
- **offset:** Calculated from page number  
- **status:** Filter by status (if not "all")
- **email:** Search query (debounced)

### Data Structures

#### Invite Interface
```typescript
interface Invite {
  id: string
  email: string
  role: "beta-tester" | "early-access"
  status: "pending" | "accepted" | "expired" | "revoked"
  invitedAt: string
  expiresAt: string
  inviteLink?: string
}
```

#### API Response
```typescript
interface InviteListResponse {
  invites: Invite[]
  total: number
  limit: number
  offset: number
}
```

## Responsive Behavior

### Desktop (1024px+)
- **Table:** Full desktop table layout
- **Columns:** All data visible
- **Actions:** Icon-based action buttons
- **Pagination:** Full pagination controls

### Tablet (768px - 1023px)
- **Table:** May show desktop layout
- **Touch:** Optimized for touch interaction  
- **Modal:** Appropriate sizing

### Mobile (< 768px)
- **Table:** Hidden, replaced with card layout
- **Cards:** Stacked mobile-friendly format
- **Actions:** Text-based buttons
- **Modal:** Full-screen behavior

## Text Content

### Headers & Labels
- "Invite Management" (main title)
- "Manage beta tester and early access invitations" (description)
- Form labels: "Email Address", "Role"
- Table headers: "Email", "Role", "Status", "Invited At", "Expires At", "Actions"

### Actions & Buttons
- "+ Create Invite"
- "Search by email..."
- "Try again" (error retry)
- "Copy Link", "Revoke" (mobile actions)
- "Previous", "Next" (pagination)
- "Cancel", "Create Invite", "Done" (modal)

### Status Messages
- "No invites found" (empty state)
- "Creating...", "Copying...", "Copied!" (loading states)
- Error messages from API
- Pagination summary text

### Confirmation Dialogs
- "Are you sure you want to revoke this invite?"
- "Invite link copied to clipboard!"

## Interaction Flows

### Invite Creation Flow
1. Admin clicks "+ Create Invite"
2. Modal opens with form
3. Admin enters email and selects role
4. Form validation occurs
5. Submit triggers API call
6. Success shows invite link
7. Admin copies link and closes modal
8. Table refreshes with new invite

### Search & Filter Flow
1. Admin types in search field
2. 300ms debounce triggers search
3. Page resets to 1
4. API request with new parameters
5. Table updates with filtered results

### Revoke Invite Flow
1. Admin clicks revoke button
2. Confirmation dialog appears
3. If confirmed, DELETE API call
4. Table refreshes without revoked invite

### Pagination Flow
1. Admin clicks Previous/Next
2. Page state updates
3. API request with new offset
4. Table updates with new page data

## Technical Notes

### Debouncing Implementation
- **Search:** 300ms debounce on input changes
- **Effect Hook:** useEffect with cleanup timer
- **State Management:** Separate debounced search state

### Error Handling
- **Network Failures:** Try-catch with user-friendly messages
- **Validation:** Email format validation
- **API Errors:** Display specific error messages
- **Modal Errors:** Form-level error display

### Performance Considerations
- **Pagination:** Limited results per request
- **Debouncing:** Reduces API call frequency
- **Conditional Rendering:** Hidden/shown components for responsive design
- **Memo Optimization:** Potential for component memoization

### Security Considerations
- **Input Validation:** Email format checking
- **XSS Protection:** Proper text sanitization
- **CSRF:** API token handling
- **Admin Authorization:** Route protection required

## Related Components
- Badge components (StatusBadge, RoleBadge)
- Modal management utilities
- API client functions
- Form validation helpers
- Pagination utilities

## Future Enhancements
- **Resend Functionality:** Currently disabled feature
- **Bulk Operations:** Multi-select invite management
- **Export:** CSV/Excel export of invite data
- **Advanced Filtering:** Date ranges, multiple status selection
- **Real-time Updates:** WebSocket updates for invite status changes