# LockN Score - Player Registration (Journey 2)

## Screen Overview
**Screen Type:** Multi-step registration flow  
**App:** LockN Score  
**Journey:** Journey 2 - Join via code/QR, enter name/photo  
**Route:** `/register`  
**Component:** `pages/PlayerRegistration.tsx`

## Layout Description

### Container Structure
- **Outer Container:** Framer Motion animated wrapper
  - Initial: opacity 0, y 12px
  - Animate: opacity 1, y 0px
- **Width:** Max width xl (576px), centered
- **Spacing:** Space-y-5 between major sections

### Main Panel Structure
- **Background:** `slate-900/70` with white/10 border
- **Border Radius:** Rounded 3xl (24px)
- **Padding:** 20px (sm: 24px)

## Section 1: Profile Setup

### Header
- **Label:** "Player Profile" (12px uppercase, tracked, slate-400)
- **Title:** "Register to play" (24px display font, sm: 36px, white)
- **Subtitle:** "Quick setup for match tracking and score history" (14px, slate-400)

### Pre-Registration State
When no player is registered:

#### Form Fields
- **Label:** "Display name" (14px, slate-300)
- **Input Field:**
  - Full width, rounded 2xl
  - Border: white/10
  - Background: `slate-950/80`  
  - Padding: 12px × 16px
  - Text: white
  - Focus: cyan ring effect
  - Placeholder: "Your name"

#### Submit Button
- **Layout:** Full width, rounded 2xl
- **Background:** Cyan (`neon`)
- **Text:** Dark slate-900, 14px semibold
- **States:** Loading (opacity 50%), Active
- **Text:** "Create Profile" / "Registering..."

### Post-Registration State
When player exists and doesn't need photo:

#### Welcome Message
- **Text:** "Welcome back [Name]" (18px font-semibold, white)
- **Photo Display:** 
  - Circular image: 112px × 112px
  - Centered with margin-top 16px
  - Border: white/10, object-cover
  - Fallback to Auth0 profile image

#### Update Photo Button
- **Style:** Border button (white/20 border)
- **Padding:** 12px × 20px, rounded 2xl
- **Text:** 14px semibold, white
- **Action:** Toggles photo capture mode

## Section 2: Photo Capture

### Header
- **Title:** "Capture your photo" (18px font-semibold, white)
- **Subtitle:** "Use your front camera for a quick player badge image" (14px, slate-400)

### Camera Interface (CameraCapture component)
- **Container:** Margin-top 16px
- **Component:** Custom camera capture interface
- **Functionality:** Front-facing camera access

### Preview & Actions State
When photo is captured:

#### Photo Preview
- **Image:** Full width, 288px height, rounded 3xl, object-cover
- **Margin:** 16px top

#### Action Buttons
- **Layout:** Grid 2 columns, gap 12px
- **Retake Button:**
  - Border: white/20
  - Background: Transparent
  - Text: 14px semibold, white
  - Padding: 12px × 16px, rounded 2xl
- **Confirm Button:**
  - Background: Cyan (`neon`)
  - Text: Dark slate-900, 14px semibold
  - States: "Use This Photo" / "Uploading..."
  - Disabled state: opacity 50%

### Error Handling
- **Error Display:** 14px amber-200 text
- **Positioning:** Below form sections
- **Content:** API error messages or validation feedback

## Component States

### Authentication States

#### Loading State
- **Display:** Simple loading text
- **Text:** "Loading..." (14px, slate-400)
- **Duration:** During Auth0 authentication check

#### Unauthenticated State
- **Container:** Centered card, max-width xl
- **Background:** `slate-900/70` rounded 3xl, border, padding 24px
- **Content:**
  - Title: "Sign in required" (20px semibold, white)
  - Message: "Please log in to register your player profile" (14px, slate-400)
  - Action: Login button (cyan background, dark text)

### Registration Flow States

#### Initial Form State
- **Inputs:** Empty with placeholder text
- **Button:** Enabled, ready for submission
- **Validation:** Real-time name validation

#### Loading State
- **Input:** Disabled during submission
- **Button:** Shows loading text, disabled
- **Feedback:** No user interaction allowed

#### Success State (Player Created)
- **Form:** Hidden/replaced with welcome message
- **Photo Section:** Revealed if photo needed
- **Transition:** Smooth reveal animation

### Photo Capture States

#### Camera Access State
- **Permission:** Request camera permission
- **Loading:** Camera initialization
- **Error:** Permission denied handling

#### Capture Ready State
- **Interface:** Live camera preview
- **Controls:** Capture button prominent
- **Quality:** Front-facing camera preferred

#### Preview State
- **Image:** Captured photo display
- **Actions:** Retake or confirm options
- **Validation:** Image quality checks

#### Upload State
- **Progress:** Upload progress feedback
- **Disabled:** No user interaction
- **Error Handling:** Upload failure retry

## Responsive Behavior

### Desktop (1024px+)
- **Container:** Centered with generous margins
- **Photo Size:** Full 112px avatar display
- **Camera:** Larger preview area
- **Touch Optimized:** No, mouse/keyboard focus

### Tablet (768px - 1023px)
- **Layout:** Maintains single column
- **Photo Size:** Slightly reduced avatar
- **Camera:** Optimized touch controls
- **Spacing:** Compressed vertical margins

### Mobile (< 768px)
- **Container:** Near full-width with minimal margins
- **Photo Size:** Responsive scaling
- **Camera:** Full-width camera interface
- **Touch:** Optimized for mobile interactions
- **Keyboard:** Proper input focus handling

## Text Content

### Headers & Labels
- "Player Profile" (section identifier)
- "Register to play" (main heading)
- "Quick setup for match tracking and score history" (description)
- "Display name" (form label)
- "Capture your photo" (photo section heading)

### Interactive Elements
- "Create Profile" / "Registering..." (submit states)
- "Welcome back [Name]" (success message)
- "Update Photo" (photo action)
- "Use This Photo" / "Uploading..." (photo submit)
- "Retake" (photo action)

### Placeholders & Help Text
- "Your name" (input placeholder)
- "Use your front camera for a quick player badge image" (photo guidance)

### Error Messages
- Form validation errors
- API connection errors
- Photo upload failures
- Authentication failures

## Interaction Flows

### New Player Registration
1. User accesses `/register` route
2. Checks authentication (redirect to login if needed)
3. Shows registration form
4. User enters display name
5. Submits form → API call
6. Success → Player created
7. If photo required → Camera capture flow
8. Otherwise → Redirect to dashboard

### Returning Player Flow
1. Authentication check passes
2. API returns existing player data
3. Shows welcome message with existing photo
4. Option to update photo
5. Quick return to dashboard

### Photo Capture Flow
1. Camera permission request
2. Camera interface loads
3. User captures photo
4. Preview with retake/confirm options
5. Upload photo to server
6. Success → Complete registration
7. Redirect to dashboard

### Error Recovery Flows
- **Network Errors:** Retry mechanisms
- **Camera Errors:** Fallback to file upload
- **Validation Errors:** Inline feedback
- **Auth Errors:** Redirect to login

## Transitions & Animations

### Page Entry
- **Effect:** Fade up from 12px below
- **Duration:** Smooth entry animation
- **Timing:** Coordinated with route transition

### State Transitions
- **Form to Welcome:** Cross-fade transition
- **Photo Reveal:** Slide down reveal
- **Preview States:** Scale and fade effects

### Loading States
- **Button Loading:** Text change with spinner
- **Form Disable:** Opacity reduction
- **Upload Progress:** Progress indicators

### Error States
- **Error Appearance:** Slide down from above
- **Error Dismissal:** Fade out effect
- **Validation:** Real-time field highlighting

## Technical Notes

### API Integration
- **Base URL Resolution:** Dynamic based on environment
- **Authentication:** Auth0 token-based
- **Endpoints:**
  - `POST /api/players/register` - Create player
  - `POST /api/players/{id}/photo` - Upload photo

### File Handling
- **Photo Format:** JPEG blob from canvas
- **Size Limits:** Reasonable file size constraints
- **Quality:** Optimized for badge display
- **Upload:** FormData multipart upload

### State Management
```typescript
interface PlayerResponse {
  id: number
  name: string
  photo_url?: string | null
  needs_photo: boolean
}
```

### Error Handling
- **Network Failures:** Retry with exponential backoff
- **Validation Errors:** Real-time field feedback
- **Camera Errors:** Graceful fallback options
- **Upload Failures:** Clear error messages

### Security Considerations
- **CSRF Protection:** Token-based API calls
- **File Validation:** Server-side image validation
- **Auth State:** Proper token refresh handling
- **Privacy:** Camera permission respect

## Related Components
- `CameraCapture` - Custom camera interface component
- `Auth0Provider` - Authentication state management
- `ProtectedRoute` - Route-level auth protection
- `useAuth` - Authentication hooks and utilities