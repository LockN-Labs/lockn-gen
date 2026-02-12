# LockN Score Design System Specification

## Overview

LockN Score design system is a comprehensive dark theme design system optimized for real-time score tracking applications. The system emphasizes high contrast, accessibility, and clear visual hierarchy with sport-specific color coding and motion design.

## Table of Contents

1. [Color Tokens](#color-tokens)
2. [Typography Scale](#typography-scale)
3. [Spacing System](#spacing-system)
4. [Border Radius](#border-radius)
5. [Component Specifications](#component-specifications)
6. [Score-Specific Components](#score-specific-components)
7. [Motion & Transitions](#motion--transitions)
8. [Responsive Breakpoints](#responsive-breakpoints)

---

## Color Tokens

### Primary Color Palette

#### Base Colors
```css
/* CSS Custom Properties */
--color-background: #05070f;
--color-surface-dim: #0E1117;
--color-surface: #121620;
--color-surface-bright: #1A1F2E;
```

#### Semantic Colors
```css
--color-primary: #4DD0E1;      /* cyan-400 - Main brand color */
--color-secondary: #B0BEC5;    /* blue-gray-400 */
--color-tertiary: #FFB74D;     /* amber-300 */
```

#### Player Colors
```css
--color-player1: #4DD0E1;      /* cyan-400 - Home player */
--color-player2: #FF8A65;      /* orange-300 - Away player */
```

#### Game State Colors
```css
--color-serve: #FFEB3B;        /* yellow-400 - Serve indicator */
--color-rally-pulse: #E040FB;  /* purple-500 - Rally highlight */
--color-match-point: #FF5252;  /* red-400 - Match point */
--color-game-won: #69F0AE;     /* green-300 - Game complete */
```

#### Connection Status
```css
--color-connected: #69F0AE;    /* green-300 - Online/stable */
--color-connecting: #FFD54F;   /* yellow-300 - Connecting */
--color-error: #FF5252;        /* red-400 - Error state */
--color-idle: #546E7A;         /* blue-gray-600 - Idle */
```

#### Text Colors
```css
--color-text-primary: #ECEFF1;    /* gray-50 - Primary text */
--color-text-secondary: #90A4AE;  /* gray-400 - Secondary text */
--color-text-tertiary: #546E7A;   /* gray-600 - Muted text */
```

### Tailwind Configuration
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        midnight: "#0b1120",
        neon: "#38bdf8",     // cyan-400 equivalent
        ember: "#fb7185",    // rose-400 equivalent  
        lime: "#a3e635",     // lime-400 equivalent
      },
      boxShadow: {
        glow: "0 0 30px rgba(56, 189, 248, 0.35)",
      },
    },
  },
}
```

---

## Typography Scale

### Font Families
```css
--font-family-primary: 'Inter', system-ui, sans-serif;
--font-family-mono: 'JetBrains Mono', monospace;
--font-family-display: 'Inter Display', system-ui, sans-serif;
```

### Font Sizes
```css
--font-size-hero-score: 96px;    /* Score displays - hero size */
--font-size-score-large: 72px;   /* Score displays - large */
--font-size-score-medium: 48px;  /* Score displays - medium */
--font-size-display: 40px;       /* Page titles */
--font-size-headline: 32px;      /* Section headings */
--font-size-title: 22px;         /* Card titles */
--font-size-body: 16px;          /* Body text */
--font-size-label: 14px;         /* Form labels, metadata */
--font-size-caption: 11px;       /* Fine print, timestamps */
```

### Font Weights
```css
--font-weight-light: 300;
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

### Line Heights
```css
--line-height-tight: 1.15;      /* Large scores, displays */
--line-height-normal: 1.5;      /* UI elements */
--line-height-relaxed: 1.75;    /* Reading text */
```

### Typography Classes
```css
.text-hero-score {
  font-size: var(--font-size-hero-score);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  letter-spacing: -0.02em;
}

.text-score-large {
  font-size: var(--font-size-score-large);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-normal);
  letter-spacing: -0.015em;
}

.text-display {
  font-size: var(--font-size-display);
  font-weight: var(--font-weight-semibold);
  line-height: var(--line-height-relaxed);
}

.text-label {
  font-size: var(--font-size-label);
  font-weight: var(--font-weight-medium);
  line-height: var(--line-height-normal);
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.mono-score {
  font-family: var(--font-family-mono);
  tabular-nums: true;
}
```

---

## Spacing System

### Spacing Scale (4px/8px Grid)
```css
--space-none: 0px;
--space-xxs: 2px;      /* 0.5 * base */
--space-xs: 4px;       /* 1 * base */
--space-sm: 8px;       /* 2 * base */
--space-md: 16px;      /* 4 * base */
--space-lg: 24px;      /* 6 * base */
--space-xl: 32px;      /* 8 * base */
--space-xxl: 48px;     /* 12 * base */
--space-xxxl: 64px;    /* 16 * base */
--space-huge: 96px;    /* 24 * base */
--space-massive: 128px; /* 32 * base */
```

### Usage Patterns
- **Component padding:** 20px (space-lg), 24px (space-xl)
- **Card spacing:** 16px (space-md) to 32px (space-xl)  
- **Button padding:** 12px 16px (space-sm space-md)
- **Input padding:** 12px 16px (space-sm space-md)
- **Section gaps:** 16px (space-md) to 24px (space-lg)

---

## Border Radius

```css
--radius-none: 0px;
--radius-sm: 4px;       /* Small elements, pills */
--radius-md: 8px;       /* Buttons, inputs */
--radius-lg: 12px;      /* Cards, panels */
--radius-xl: 16px;      /* Large cards */
--radius-xxl: 24px;     /* Feature cards */
--radius-xxxl: 32px;    /* Hero elements */
--radius-full: 9999px;  /* Circular elements */
```

### Common Patterns
- **Buttons:** 16px (rounded-2xl)
- **Inputs:** 12px (rounded-xl) 
- **Cards:** 28px (rounded-[28px]) to 32px (rounded-[32px])
- **Modals:** 24px (rounded-3xl)
- **Status indicators:** 9999px (rounded-full)

---

## Component Specifications

### Buttons

#### Base Button Styles
```css
.btn-base {
  padding: 12px 16px;
  border-radius: var(--radius-xl);
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-label);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s ease;
  cursor: pointer;
}
```

#### Primary Button
```css
.btn-primary {
  background: var(--color-primary);
  color: var(--color-surface);
  box-shadow: var(--shadow-glow);
}

.btn-primary:hover {
  filter: brightness(110%);
}
```

#### Secondary Button
```css
.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text-primary);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
}
```

#### Game Control Buttons (4-button grid)
```css
.btn-game-control {
  background: rgba(15, 23, 42, 0.7); /* slate-950/70 */
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--color-text-primary);
  padding: 12px 16px;
  border-radius: var(--radius-xl);
  font-weight: var(--font-weight-semibold);
  transition: all 0.2s ease;
}

/* Color variants */
.btn-start { color: #a5f3fc; }  /* cyan-200 */
.btn-hit { color: #bef264; }    /* lime-200 */
.btn-stop { color: #fde68a; }   /* amber-200 */
.btn-reset { color: #fecaca; }  /* rose-200 */
```

### Cards

#### Base Card
```css
.card-base {
  background: rgba(15, 23, 42, 0.7); /* slate-900/70 */
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 28px;
  padding: 20px;
  backdrop-filter: blur(8px);
}
```

#### Feature Card (with gradients)
```css
.card-feature {
  background: linear-gradient(135deg, 
    rgba(2, 6, 23, 1) 0%,
    rgba(15, 23, 42, 1) 50%, 
    rgba(2, 6, 23, 1) 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 32px;
  padding: 24px;
  box-shadow: 0 20px 60px rgba(15, 23, 42, 0.45);
  position: relative;
  overflow: hidden;
}

/* Ambient lighting effects */
.card-feature::before {
  content: '';
  position: absolute;
  top: -48px;
  left: -48px;
  width: 160px;
  height: 160px;
  background: radial-gradient(circle, rgba(34, 211, 238, 0.2), transparent);
  border-radius: 50%;
  filter: blur(48px);
}
```

### Inputs

#### Text Input
```css
.input-text {
  width: 100%;
  padding: 12px 16px;
  background: rgba(15, 23, 42, 0.8); /* slate-950/80 */
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-xl);
  color: var(--color-text-primary);
  font-size: var(--font-size-body);
  outline: none;
  transition: all 0.2s ease;
}

.input-text:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(77, 208, 225, 0.1);
}

.input-text::placeholder {
  color: var(--color-text-tertiary);
}
```

### Modals

#### Modal Overlay
```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

#### Modal Content
```css
.modal-content {
  width: 100%;
  max-width: 448px; /* max-w-md */
  margin: 16px;
  background: var(--color-surface);
  border-radius: 24px;
  padding: 32px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  position: relative;
}
```

### Status Indicators

#### Connection Status Pill
```css
.status-pill {
  display: flex;
  align-items: center;
  justify-between;
  padding: 12px 16px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: var(--radius-xl);
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  box-shadow: 0 0 12px rgba(74, 222, 128, 0.6);
}

.status-indicator.connected {
  background: var(--color-connected);
}

.status-indicator.connecting {
  background: var(--color-connecting);
}
```

---

## Score-Specific Components

### Score Display

#### Large Score Numbers
```css
.score-large {
  font-size: 72px;        /* sm: 96px, md: 112px */
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.015em;
  font-family: var(--font-family-display);
}

.score-player1 { color: #a5f3fc; } /* cyan-300 */
.score-player2 { color: #bef264; } /* lime-300 */
```

#### Score Container
```css
.score-container {
  background: rgba(15, 23, 42, 0.6); /* slate-950/60 */
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 24px;
  padding: 24px 16px; /* sm: 24px */
  text-align: center;
  position: relative;
}
```

### Rally Counter

```css
.rally-counter {
  border-radius: 28px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(15, 23, 42, 0.7);
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.rally-count {
  font-size: var(--font-size-display);
  font-family: var(--font-family-display);
  color: var(--color-text-primary);
}

.rally-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: rgba(16, 185, 129, 0.15); /* emerald-500/15 */
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6ee7b7; /* emerald-300 */
  font-size: 24px;
}
```

### Serve Indicator

```css
.serve-indicator {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  background: var(--color-serve);
  border-radius: 50%;
  border: 2px solid var(--color-surface);
  box-shadow: 0 0 16px rgba(255, 235, 59, 0.8);
  animation: serve-pulse 2s infinite;
}

@keyframes serve-pulse {
  0%, 100% { 
    transform: scale(1);
    opacity: 1;
  }
  50% { 
    transform: scale(1.1);
    opacity: 0.9;
  }
}
```

### Player Card

```css
.player-card {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 16px;
  text-align: center;
  position: relative;
}

.player-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.1);
  object-fit: cover;
  margin: 0 auto 12px;
}

.player-name {
  font-size: var(--font-size-body);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}
```

### Game State Badges

```css
.badge-base {
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: var(--font-size-caption);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.badge-match-point {
  background: rgba(255, 82, 82, 0.15);
  color: #ff8a95;
  border-color: rgba(255, 82, 82, 0.3);
}

.badge-game-won {
  background: rgba(105, 240, 174, 0.15);
  color: #86efac;
  border-color: rgba(105, 240, 174, 0.3);
}

.badge-live {
  background: rgba(77, 208, 225, 0.15);
  color: #67e8f9;
  border-color: rgba(77, 208, 225, 0.3);
}
```

---

## Motion & Transitions

### Animation Durations
```css
--duration-fast: 150ms;      /* Micro-interactions */
--duration-normal: 300ms;    /* Standard transitions */
--duration-slow: 500ms;      /* Modal/page transitions */
--duration-very-slow: 1000ms; /* Score animations */
```

### Easing Curves
```css
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);       /* Default out */
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);     /* Smooth in-out */
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55); /* Bounce effect */
```

### Common Animations

#### Button Press (Framer Motion)
```javascript
const buttonTapAnimation = {
  whileTap: { scale: 0.96 },
  transition: { duration: 0.15 }
}
```

#### Score Update Animation
```javascript
const scoreVariant = {
  initial: { scale: 1, opacity: 0.8 },
  animate: { scale: 1, opacity: 1 },
  bounce: { 
    scale: [1, 1.08, 1], 
    opacity: [0.8, 1, 1],
    transition: { duration: 0.5 }
  }
}
```

#### Modal Enter/Exit
```javascript
const modalVariants = {
  hidden: { opacity: 0, scale: 0.9, y: 20 },
  visible: { opacity: 1, scale: 1, y: 0 },
  exit: { opacity: 0, scale: 0.9, y: 20 }
}
```

#### Page Transitions
```javascript
const pageVariants = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -12 }
}
```

### CSS Animations

#### Loading Spinner
```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-spinner {
  animation: spin 1s linear infinite;
}
```

#### Glow Pulse
```css
@keyframes glow-pulse {
  0%, 100% {
    box-shadow: 0 0 20px rgba(77, 208, 225, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(77, 208, 225, 0.6);
  }
}

.glow-pulse {
  animation: glow-pulse 2s ease-in-out infinite;
}
```

---

## Responsive Breakpoints

### Tailwind Breakpoints (Default)
```css
/* Mobile-first approach */
sm: '640px',   /* Small devices */
md: '768px',   /* Medium devices */
lg: '1024px',  /* Large devices */
xl: '1280px',  /* Extra large devices */
2xl: '1536px'  /* 2X Extra large devices */
```

### Responsive Patterns

#### Score Display Scaling
```css
/* Mobile: 48px, Tablet: 72px, Desktop: 96px */
.score-responsive {
  font-size: 48px;
}

@media (min-width: 640px) {
  .score-responsive {
    font-size: 72px;
  }
}

@media (min-width: 768px) {
  .score-responsive {
    font-size: 96px;
  }
}
```

#### Grid Responsive Behavior
```css
/* Mobile: 1 column, Tablet+: 2 columns */
.grid-responsive {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

@media (min-width: 640px) {
  .grid-responsive {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}
```

#### Component Padding
```css
/* Mobile: 16px, Desktop: 24px */
.padding-responsive {
  padding: 16px;
}

@media (min-width: 640px) {
  .padding-responsive {
    padding: 24px;
  }
}
```

### Mobile-Specific Considerations

- **Touch targets:** Minimum 44px height for buttons
- **Safe areas:** Account for device notches and home indicators
- **Viewport units:** Use `dvh` for dynamic viewport height when supported
- **Text scaling:** Ensure readability at system font size scaling

---

## Implementation Notes

### CSS Architecture
- Use CSS custom properties for all design tokens
- Leverage Tailwind's utility-first approach for rapid development
- Maintain component-specific CSS classes for complex patterns
- Use CSS-in-JS (Framer Motion) for dynamic animations

### Accessibility
- Maintain WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text)
- Implement focus-visible styles for keyboard navigation
- Use semantic HTML and ARIA labels appropriately
- Support prefers-reduced-motion for animation preferences

### Performance
- Use CSS transforms for animations (GPU acceleration)
- Implement backdrop-filter sparingly for performance
- Optimize font loading with font-display: swap
- Consider using CSS containment for score components

### Dark Theme Optimization
- Use appropriate contrast ratios for dark backgrounds
- Implement subtle gradients and glows for visual interest
- Ensure readability in various ambient lighting conditions
- Test on OLED displays for true black rendering

---

This specification provides the complete foundation for recreating the LockN Score design system in Figma or any design tool. The detailed tokens, component specifications, and behavioral guidelines ensure consistency across all implementations.