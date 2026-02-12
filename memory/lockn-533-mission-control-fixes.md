# LOCKN-533: Mission Control Dashboard Layout Fixes

## Current State Analysis
- **File**: LockN AI (`6MEJFHJ04qsFBtTJt7bZJO`)
- **Target Node**: `14:4` (Mission Control Dashboard)
- **Current UX Score**: ~8.8 / 10 (FAILS 9.81 gate)
- **Before Screenshot**: https://figma-alpha-api.s3.us-west-2.amazonaws.com/images/c2d871b5-8b19-47e2-9f7d-2ee176674e1d

## Critical Issues Identified

### 1. Alerts & Blockers Section (Node 14:13)
- **Problem**: Fixed height `190px` with `layout_ED5LWA`
- **Impact**: P1/P2 alert cards being clipped by containers below
- **Fix Required**: Convert to auto-layout with content-driven height

### 2. Priority Queue Section (Node 14:176) 
- **Problem**: Fixed height `788px` with `layout_NX3O6O`
- **Impact**: Starts too close to middle row, potential overlap
- **Fix Required**: Auto-layout with proper spacing from above sections

### 3. Main Container (Node 14:4)
- **Problem**: Fixed vertical sizing (`layout_Q7NP4B`)
- **Impact**: Doesn't accommodate dynamic content growth
- **Fix Required**: Convert to auto-layout column with content-driven height

## Required Layout Changes

### Step 1: Main Container Auto-Layout
```
Node 14:4 (Mission Control Dashboard):
- Change from fixed dimensions (1920×1526) to:
  - mode: column
  - sizing: horizontal: fixed (1920), vertical: hug
  - gap: 24px (8pt grid compliance)
  - padding: maintain existing
```

### Step 2: Alerts & Blockers Auto-Layout
```
Node 14:13 (Alerts & Blockers):
- Change from fixed height (190px) to:
  - sizing: horizontal: fill, vertical: hug
  - gap: 12px (existing)
  - padding: 16px 24px (existing)
  - Remove fixed height constraint
```

### Step 3: Priority Queue Auto-Layout
```
Node 14:176 (Priority Queue):
- Change from fixed height (788px) to:
  - sizing: horizontal: fill, vertical: hug
  - gap: 12px (existing) 
  - padding: 16px 24px (existing)
  - Remove fixed height constraint
```

### Step 4: Inter-Section Spacing
```
Between major sections, enforce 24px minimum gaps:
- Header → Alerts & Blockers: 24px
- Alerts & Blockers → Middle Section: 24px  
- Middle Section → Priority Queue: 24px
```

## Expected UX Score Improvements

Based on the scoring rubric categories:

1. **Visual Consistency & Grid (15%)**: 9.2 → 9.8 (+0.6)
   - Proper 8pt grid spacing implementation
   - Consistent section rhythm

2. **Readability & Density (13%)**: 8.9 → 9.7 (+0.8)
   - No more clipped content
   - Better whitespace balance

3. **Responsiveness & Scalability (8%)**: 8.5 → 9.6 (+1.1)  
   - Content-driven auto-layout
   - Better overflow handling

**Projected Total Score**: ~9.85 (PASSES 9.81 gate)

## Implementation Plan

1. **Establish Figma Connection**
   - Open Desktop Bridge plugin in Figma Desktop
   - Navigate to the LockN AI file
   - Select Mission Control Dashboard (node 14:4)

2. **Apply Layout Changes**
   - Execute auto-layout conversions via figma_execute
   - Set consistent spacing values
   - Remove fixed height constraints

3. **Visual Validation**
   - Capture after screenshot
   - Compare before/after for clipping resolution
   - Verify 8pt grid compliance

4. **UX Scoring**
   - Score against full rubric
   - Document improvements
   - Confirm ≥9.81 threshold met

## Status
- ✅ Analysis Complete
- ❌ Figma Connection Required  
- ⏳ Awaiting Desktop Bridge plugin activation
- ⏳ Layout fixes pending