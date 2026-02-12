# LockN AI Speak - Voice Cloning & TTS

## Screen Overview
**Screen Type:** Voice cloning and text-to-speech application  
**App:** LockN AI Platform - Speak Module  
**Journey:** Voice synthesis, cloning, and audio generation  
**Route:** `/speak/`  
**Component:** `web/speak/index.html`

## Layout Description

### Container Structure
- **Background:** Dark theme (`#0a0a0a`)
- **Typography:** System font stack
- **Max Width:** 900px centered
- **Padding:** 2rem all sides (1rem on mobile)

### Suite Navigation (Shared Component)
- **Position:** Sticky top with backdrop blur
- **Background:** `rgba(10,10,10,0.9)` with border
- **Content:** LockN Suite navigation with logo and app links

## Header Section

### Title & Branding
- **Title:** "LockN Speak" (2rem, white with purple accent)
- **Subtitle:** Muted description text (#888)
- **Margin Bottom:** 2rem

## Tab Navigation System

### Tab Container
- **Layout:** Flex with no gaps
- **Border:** Bottom border (#333)
- **Margin Bottom:** 2rem

### Tab Buttons
- **Styling:**
  - Padding: 0.75rem × 1.5rem
  - Background: None (transparent)
  - Color: #888 default, #7c3aed active, #fff hover
  - Border: 2px bottom border (transparent default, purple active)
  - Transition: All 0.2s

### Tab Structure
Three main sections:
1. **Text to Speech** - Main TTS functionality
2. **Voice Profiles** - Voice cloning and management  
3. **Teleprompter** - Real-time speech synthesis with following

## Text to Speech Panel

### Panel Container
- **Display:** Block when active, none when inactive
- **Background:** Dark cards with consistent styling

### TTS Form Card
- **Container:** Card styling (#1a1a1a background, #333 border, 12px radius)
- **Padding:** 1.5rem
- **Margin Bottom:** 1rem

#### Voice Profile Selection
- **Label:** "Voice Profile" (small, muted)
- **Select:** Full width dropdown
- **Styling:** Dark background (#0a0a0a), purple focus border
- **Options:** Dynamically loaded from API

#### Text Input Area
- **Label:** "Text to synthesize"
- **Element:** Textarea, full width
- **Min Height:** 120px
- **Resize:** Vertical only
- **Placeholder:** Input guidance text

#### Synthesis Controls
- **Generate Button:** Purple background (#7c3aed)
- **States:** Normal, loading (with spinner), disabled
- **Hover:** Darker purple (#6d28d9)

### Audio Output Section
- **Audio Element:** Full width HTML5 audio player
- **Margin:** Top 1rem
- **Controls:** Standard browser audio controls

### Advanced Settings (Collapsed/Expandable)
- **Speed Control:** Slider or input
- **Pitch Control:** Slider or input  
- **Volume Control:** Slider or input
- **Format Selection:** MP3, WAV options

## Voice Profiles Panel

### Profile Management Header
- **Title:** Section header with create new profile CTA
- **Layout:** Flex justify-between

### Profile Creation Form

#### Audio Upload Section
- **Drop Zone:** Dashed border (#333), 2rem padding, centered
- **Hover State:** Purple border and text (#7c3aed)
- **Drag State:** Visual feedback for file dropping
- **Text:** "Drop audio file here or click to upload"

#### Profile Metadata
- **Name Input:** Required text field
- **Description Input:** Optional textarea
- **Create Button:** Purple CTA with loading states

### Profile List Display

#### Loading State
- **Spinner:** Centered with loading text
- **Animation:** Rotating border animation

#### Empty State
- **Message:** "No voice profiles yet. Create one above!"
- **Color:** Muted text (#666)

#### Profile Cards
Each profile displays in a card format:

##### Card Container
- **Layout:** Flex column with card styling
- **Background:** #1a1a1a with border
- **Padding:** 1.5rem

##### Profile Information
- **Name:** Primary text, font-weight 600, white
- **Description:** Secondary text, #888, or "No description"
- **Created Date:** Small text, #666, formatted timestamp

##### Usage Statistics
Real-time stats display:
- **Generations Count:** "🎙️ X generations"
- **Total Duration:** "⏱️ X min total"
- **Last Used:** "📅 Last: Date"

##### Action Buttons
- **Preview:** 🔊 button to play sample audio
- **Edit:** ✏️ button to modify profile
- **Delete:** Red button with confirmation

### Profile Actions

#### Preview Audio
- **Trigger:** Preview button click
- **Behavior:** Play sample audio from profile
- **Feedback:** Audio controls appear

#### Edit Profile
- **Trigger:** Edit button click
- **Modal:** Popup with current name/description
- **Actions:** Save/cancel with API integration

#### Delete Profile  
- **Trigger:** Delete button click
- **Confirmation:** Browser confirm dialog
- **API:** DELETE request with error handling

## Teleprompter Panel

### Script Input Section
- **Layout:** Large textarea for script input
- **Features:** Word-level highlighting and tracking
- **Real-time:** Speech synthesis with visual following

### Speech-to-Text Integration
- **Status Indicator:** Color-coded connection status
  - Green: Active and listening
  - Red: Error state
  - Gray: Inactive
- **Visual:** Pulsing dot animation when active

### Script Display Modes
- **Reading Mode:** Standard text display
- **Teleprompter Mode:** Large text with word highlighting
- **Synchronized Mode:** Real-time TTS with visual cursor

### Word Tracking States
CSS classes for different word states:
- **.script-word.spoken:** Gray text (#666)
- **.script-word.current:** Purple highlight with background
- **.script-word.upcoming:** Larger white text
- **.script-word.upcoming-near:** Even larger, bold

## Component States

### Loading States
- **Button Loading:** Spinner with disabled state
- **Profile Loading:** Centered spinner with text
- **Audio Loading:** Progress indicators

### Error States
- **API Errors:** Toast notifications with error messages
- **Validation Errors:** Inline form validation
- **Network Errors:** Retry mechanisms

### Success States
- **Profile Created:** Success toast notification
- **Audio Generated:** Automatic audio playback
- **File Uploaded:** Visual confirmation

### Empty States
- **No Profiles:** Guidance message and create CTA
- **No Audio:** Placeholder for audio player
- **No Text:** Guidance for text input

## Responsive Behavior

### Desktop (900px+)
- **Layout:** Full horizontal layout maintained
- **Cards:** Comfortable padding and spacing
- **Controls:** Full-size interactive elements
- **Typography:** Standard sizing throughout

### Tablet (768px - 899px)
- **Layout:** Maintains most desktop features
- **Cards:** Slightly compressed spacing
- **Touch:** Optimized for touch interaction
- **Navigation:** May stack on smaller tablets

### Mobile (< 768px)
- **Container:** Reduced to 1rem padding
- **Tabs:** Flex direction changes to column
- **Profile Cards:** Stack actions vertically
- **Input:** Full-width mobile-optimized controls

## Text Content

### Headers & Navigation
- "LockN Speak" (main title)
- Tab labels: "Text to Speech", "Voice Profiles", "Teleprompter"

### Form Labels & Placeholders
- "Voice Profile", "Text to synthesize"
- "Profile Name", "Description"
- Input placeholders and guidance text

### Button Labels
- "Generate Speech", "Create Profile"
- "🔊 Preview", "✏️ Edit", "Delete"
- "Drop audio file here or click to upload"

### Status & Feedback Messages
- Loading: "Generating speech...", "Creating profile..."
- Success: "Voice profile created successfully"
- Error: "Error: [specific message]"
- Empty states: "No voice profiles yet..."

### Statistics & Metadata
- Usage stats: generations, duration, last used
- Date formatting: "Created: [timestamp]"
- File info: audio format, duration, size

## Interaction Flows

### TTS Generation Flow
1. User selects voice profile from dropdown
2. Enters text to synthesize
3. Clicks "Generate Speech" button
4. Audio generates and auto-plays
5. User can replay or save audio

### Voice Profile Creation Flow
1. User uploads audio file (drag/drop or click)
2. Enters profile name and description
3. Clicks "Create Profile" button  
4. Profile processes and appears in list
5. Profile available for TTS selection

### Profile Management Flow
1. User views profile list with statistics
2. Can preview, edit, or delete profiles
3. Edit opens modal with current information
4. Delete requires confirmation
5. Changes reflect immediately in UI

### Teleprompter Usage Flow
1. User inputs script text
2. Selects voice profile and settings
3. Starts speech synthesis
4. Visual highlighting follows speech
5. Real-time feedback and control

## Technical Implementation

### API Integration
- **Profile Management:** CRUD operations for voice profiles
- **Audio Generation:** TTS API with profile selection
- **File Upload:** Audio file processing for cloning
- **Statistics:** Usage tracking and analytics

### Real-time Features
- **Speech Recognition:** Browser Speech API integration
- **Audio Playback:** HTML5 audio with custom controls
- **Visual Feedback:** CSS animations and transitions
- **Progress Tracking:** Real-time status updates

### Data Management
- **Local Storage:** User preferences and settings
- **Profile Caching:** Recent voice profiles
- **Audio Caching:** Generated audio files
- **Settings Persistence:** User interface preferences

### Performance Considerations
- **Audio Streaming:** Progressive audio loading
- **File Processing:** Client-side audio validation
- **UI Responsiveness:** Async operations with feedback
- **Memory Management:** Audio file cleanup

## Advanced Features

### Voice Cloning Technology
- **Audio Analysis:** Voice characteristic extraction
- **Model Training:** Custom voice model generation
- **Quality Assessment:** Audio quality validation
- **Profile Optimization:** Voice model refinement

### Speech Synthesis Options
- **Speed Control:** Variable playback speed
- **Pitch Adjustment:** Voice pitch modification
- **Emotion Control:** Emotional tone variation
- **Format Selection:** Multiple audio output formats

### Accessibility Features
- **Keyboard Navigation:** Full keyboard accessibility
- **Screen Reader:** ARIA labels and descriptions
- **High Contrast:** Visual accessibility options
- **Audio Descriptions:** Voice guidance for UI

## Integration Points

### LockN Suite Integration
- **Shared Navigation:** Consistent platform navigation
- **Authentication:** Unified user management
- **API Gateway:** Centralized API access
- **Cross-app Features:** Voice profiles across apps

### Third-party Integration
- **Cloud Storage:** Audio file backup
- **Speech APIs:** External TTS services
- **Analytics:** Usage and performance tracking
- **Export Options:** Audio file sharing and download