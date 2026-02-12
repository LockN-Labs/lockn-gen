# LockN Score - Setup & Calibration

## Screen Overview
**Screen Type:** Camera setup and calibration wizard  
**App:** LockN Score  
**Journey:** Technical setup for AI scoring system  
**Route:** `/setup`  
**Component:** `pages/Setup.tsx`

## Layout Description

### Container Structure
- **Layout:** Vertical space with consistent spacing (space-y-6)
- **Background:** Transparent (inherits from app background)
- **Typography:** Consistent with app design system

### Header Section
- **Structure:** Simple header with metadata hierarchy
- **Label:** "Camera Setup" (12px uppercase, wide tracking, slate-400)
- **Title:** "Calibration & Alignment" (36px display font, white)
- **Description:** Setup explanation text (14px, slate-400)

## Section 1: Camera Positioning

### Container
- **Background:** `slate-900/70` with rounded 3xl corners
- **Border:** Ring-1 with `white/10` color
- **Padding:** 24px

### Content Structure
- **Title:** "1. Position Camera" (18px font-semibold, white)
- **Instructions:** Detailed positioning guidance
- **Video Preview:** Live camera feed area
- **Control Button:** Camera enable/test button

### Camera Preview Area
- **Container:** Rounded 2xl with dashed border
- **Border Color:** `slate-700`
- **Background:** `slate-950/40`
- **Dimensions:** Height 224px (h-56), full width
- **Content:** Live video element or placeholder

#### States
- **Loading:** "Live preview unavailable" text
- **Active:** `<video>` element with object-cover styling
- **Error:** Error message display

### Camera Control
- **Button Styling:** Cyan background (`neon`), dark text
- **Padding:** 12px × 20px, rounded 2xl
- **States:** "Enable Camera Preview" / "Re-check Camera"
- **Error Display:** Amber-200 colored error text below button

## Section 2: Calibration

### Container
- **Styling:** Identical to Section 1 container
- **Title:** "2. Calibration"
- **Description:** Corner marking instructions

### Calibration Grid
- **Layout:** Grid with sm:grid-cols-2 (responsive)
- **Gap:** 12px between items

### Calibration Buttons
Four corner marking buttons:
- **Labels:** "Mark baseline A", "Mark baseline B", "Mark sideline A", "Mark sideline B"
- **Styling:** 
  - Border button with `slate-700` border
  - Background: `slate-950/60`
  - Padding: 16px all sides
  - Text alignment: left
  - Font: 14px semibold, white
- **Interactive States:**
  - Hover: border changes to `neon/50`, text changes to `neon`
  - Transition: smooth hover transitions

## Section 3: Verification

### Container
- **Background:** Gradient from `neon/10` to `emerald-500/10`
- **Border:** Ring-1 with `white/10`
- **Visual:** Distinctive success-oriented styling

### Content
- **Title:** "3. Verify"
- **Instructions:** Test rally guidance with confidence metrics
- **Target:** "95%+ confidence across last 10 rallies"

### Action Buttons
- **Layout:** Flex column, gap 12px (sm: flex-row)
- **Primary Button:** "Start Test Rally"
  - Background: Cyan (`neon`)
  - Text: Dark slate-900, 14px semibold
  - Padding: 12px × 20px, rounded 2xl
- **Secondary Button:** "Save Calibration"
  - Border button with `slate-700` border
  - Text: White, 14px semibold
  - Same padding and rounding

## Component States

### Initial State
- **Camera:** Preview disabled, button shows "Enable Camera Preview"
- **Calibration:** All corner buttons enabled but not marked
- **Verification:** Buttons available but no test started

### Camera Active State
- **Preview:** Live video feed displaying
- **Button:** Text changes to "Re-check Camera"
- **Error Cleared:** No error messages visible

### Camera Error State
- **Preview:** Placeholder text showing
- **Error Message:** Specific error text below button
- **Button:** Remains interactive for retry

### Calibration In Progress
- **Buttons:** Visual feedback as corners are marked
- **Progress:** Some form of completion indication
- **Validation:** Ensures all corners marked before proceeding

### Verification Active
- **Test Rally:** In progress state feedback
- **Confidence Display:** Real-time confidence percentage
- **Save Enabled:** Once confidence threshold met

## Responsive Behavior

### Desktop (1200px+)
- **Layout:** Full-width sections with generous spacing
- **Camera Preview:** Large viewing area
- **Button Grid:** Two-column calibration layout
- **Typography:** Full scale sizing

### Tablet (768px - 1199px)
- **Sections:** Maintains vertical stacking
- **Camera:** Slightly reduced preview area
- **Grid:** Two-column calibration maintained
- **Spacing:** Compressed but readable

### Mobile (< 768px)
- **Layout:** Single column throughout
- **Camera:** Full-width preview optimized for mobile
- **Calibration:** Single column button layout
- **Touch:** Optimized for touch interaction

## Text Content

### Headers & Instructions
- "Camera Setup" (section label)
- "Calibration & Alignment" (main title)
- "Configure the scoring camera and validate court detection before starting a match"

### Step Titles
- "1. Position Camera", "2. Calibration", "3. Verify"

### Instructions
- "Mount the camera at least 12ft away, aligned to center court. Use the preview feed to confirm the full playing area is visible."
- "Mark the four baseline corners and let LockN Score detect the rally zone."
- "Run a quick rally to confirm score recognition. Save when confidence is 95%+ across the last 10 rallies."

### Button Labels
- "Enable Camera Preview" / "Re-check Camera"
- Corner marking labels: "Mark baseline A/B", "Mark sideline A/B"
- "Start Test Rally", "Save Calibration"

### Error Messages
- "Camera API unavailable in this browser"
- "Camera permission denied. Allow camera access and retry"

## Interaction Flows

### Initial Setup Flow
1. User accesses setup page
2. Reads positioning instructions
3. Enables camera preview
4. Adjusts physical camera position
5. Proceeds to calibration

### Calibration Flow
1. User marks each corner sequentially
2. System validates corner positions
3. Calculates court boundaries
4. Prepares for verification testing

### Verification Flow
1. User starts test rally
2. System analyzes recognition confidence
3. Real-time confidence feedback
4. Save calibration when threshold met

### Error Recovery
- **Camera Issues:** Permission retry, browser compatibility
- **Calibration Issues:** Re-mark corners, validation feedback
- **Recognition Issues:** Repositioning guidance, threshold adjustment

## Transitions & Animations

### Camera Activation
- **Preview Loading:** Smooth transition from placeholder
- **Stream Start:** Gradual fade-in of video
- **Error States:** Error message slide-in animation

### Calibration Progress
- **Button States:** Visual feedback on corner marking
- **Progress Indication:** Completion status updates
- **Success Feedback:** Confirmation animations

### Verification Testing
- **Confidence Updates:** Real-time meter or percentage
- **Success State:** Achievement animation when threshold met
- **Save Confirmation:** Success feedback for saved calibration

## Technical Notes

### Camera API Integration
- **Media Devices:** `navigator.mediaDevices.getUserMedia()`
- **Video Constraints:** `{ video: true, audio: false }`
- **Stream Management:** Proper cleanup and disposal
- **Error Handling:** Permission and compatibility checks

### Calibration System
- **Corner Detection:** Computer vision for court boundaries
- **Validation:** Geometric verification of marked points
- **Persistence:** Saving calibration data for future sessions

### Verification Analytics
- **Confidence Scoring:** Real-time recognition accuracy
- **Rally Analysis:** Ball tracking and scoring validation
- **Threshold Management:** 95% accuracy requirement
- **Data Storage:** Calibration and performance metrics

### Performance Considerations
- **Video Processing:** Efficient frame handling
- **Real-time Analysis:** Optimized computer vision pipeline
- **Memory Management:** Stream cleanup and resource disposal
- **Error Recovery:** Robust handling of hardware/permission issues

## Related Components
- Camera capture utilities
- Computer vision processing
- Calibration data management
- Real-time confidence monitoring

## Hardware Requirements
- **Camera:** Minimum resolution and frame rate requirements
- **Processing:** Sufficient CPU for real-time analysis
- **Storage:** Calibration data persistence
- **Network:** Optional cloud backup of settings