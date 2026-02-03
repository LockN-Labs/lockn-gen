# LOC-61 Architecture

## File Structure
- /docs/LOC-61-architecture.md (this document)
- /src/LockNGen.Api/wwwroot/landing.html
- /src/LockNGen.Api/wwwroot/css/landing.css
- /src/LockNGen.Api/Program.cs updates

## Component Breakdown
1. Header (logo + navigation)
2. Hero section (animated CTA)
3. Features grid (3-column layout)
4. Pricing section (comparative cards)
5. Footer (links + social)

## CSS Architecture
- Base styles from wwwroot/css/styles.css
- Mobile-first responsive breakpoints
- Utility-first class naming convention
- CSS Custom Properties for theme colors

## Mobile-First Approach
- Default styles for mobile view
- @media queries for tablet/desktop
- Touch-friendly interactive elements
- Font size scaling with viewport units