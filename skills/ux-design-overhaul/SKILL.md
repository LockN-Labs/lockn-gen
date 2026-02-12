# UX Design Overhaul Skill

## Description

A comprehensive workflow for conducting ad-hoc UX improvements, from initial assessment to implementation-ready deliverables. This skill provides a structured approach to identify UX issues, prioritize improvements, and generate actionable development tickets with proper QA checkpoints.

## Core Workflow

### Phase 1: Intake & Discovery

**Required Inputs:**
- **Current State Screenshots**: High-fidelity screenshots of existing UI/UX (multiple device sizes if applicable)
- **Goals**: Specific business/user objectives for the improvement
- **Constraints**: Technical, budget, timeline, or brand constraints
- **Target Audience**: Primary user personas, demographics, use cases

**Intake Template:**
```
## UX Improvement Request

### Current State
- [ ] Desktop screenshots attached
- [ ] Mobile screenshots attached (if applicable)
- [ ] Current user flow documented

### Goals & Success Metrics
- Primary goal: [e.g., increase conversion by 15%]
- Secondary goals: [e.g., reduce support tickets]
- Success metrics: [measurable outcomes]

### Constraints
- Timeline: [deadline]
- Budget: [development hours/resources]
- Technical: [platform limitations, existing tech stack]
- Brand: [style guide compliance, accessibility requirements]

### Target Audience
- Primary persona: [age, role, tech-savviness]
- Use case context: [when/why they use this feature]
- Pain points: [current frustrations]
```

### Phase 2: UX Audit & Scoring

**Heuristic Evaluation Framework**
Score each area 1-10 (1=poor, 10=excellent):

1. **Usability Heuristics**
   - Visibility of system status
   - Match between system and real world
   - User control and freedom
   - Consistency and standards
   - Error prevention
   - Recognition rather than recall
   - Flexibility and efficiency of use
   - Aesthetic and minimalist design
   - Help users recognize, diagnose errors
   - Help and documentation

2. **Conversion Optimization**
   - Clear value proposition
   - Friction reduction
   - Trust signals
   - Call-to-action effectiveness

3. **Accessibility**
   - WCAG 2.1 compliance
   - Keyboard navigation
   - Screen reader compatibility
   - Color contrast ratios

4. **Mobile Experience** (if applicable)
   - Touch target sizing
   - Responsive design
   - Performance on mobile

**Audit Output:**
```
## UX Audit Results

### Overall Score: [X/10]

### Heuristic Breakdown:
- Usability: [score]/10 - [key issues]
- Conversion: [score]/10 - [key issues]
- Accessibility: [score]/10 - [key issues]
- Mobile: [score]/10 - [key issues]

### Critical Issues (Score < 4):
1. [Issue] - Impact: [high/medium/low]
2. [Issue] - Impact: [high/medium/low]

### Quick Wins (Easy fixes, high impact):
1. [Issue] - Effort: [hours] - Impact: [high/medium/low]
2. [Issue] - Effort: [hours] - Impact: [high/medium/low]
```

### Phase 3: Improvement Plan & Milestones

**Prioritization Matrix:**
- **High Impact, Low Effort** → Milestone 1 (Quick Wins)
- **High Impact, High Effort** → Milestone 2-3 (Major Features)
- **Low Impact, Low Effort** → Milestone 4 (Polish)
- **Low Impact, High Effort** → Backlog/Consider Later

**Milestone Structure:**
```
## Improvement Plan

### Milestone 1: Quick Wins (Week 1-2)
- Goal: Address critical usability issues with minimal dev work
- Success Criteria: [specific metrics]
- Issues Addressed: [list of issues from audit]

### Milestone 2: Core UX Improvements (Week 3-4)
- Goal: Implement major user experience enhancements
- Success Criteria: [specific metrics]
- Issues Addressed: [list of issues from audit]

### Milestone 3: Advanced Features (Week 5-6)
- Goal: Add sophisticated UX patterns and optimizations
- Success Criteria: [specific metrics]
- Issues Addressed: [list of issues from audit]

### Milestone 4: Polish & Optimization (Week 7-8)
- Goal: Fine-tune and perfect the user experience
- Success Criteria: [specific metrics]
- Issues Addressed: [list of issues from audit]
```

### Phase 4: Linear Ticket Generation

**Ticket Template:**
```
## Title
[UX] [Component/Feature Name] - [Specific Improvement]

## Description
**Problem Statement:**
Users experience [specific problem] when [context/scenario].

**Current State:**
[Description of current behavior/design]

**Desired State:**
[Description of improved behavior/design]

**User Impact:**
[How this affects user experience and business metrics]

## Acceptance Criteria
### Functional Requirements
- [ ] [Specific behavior requirement]
- [ ] [Specific behavior requirement]
- [ ] [Specific behavior requirement]

### Design Requirements
- [ ] Matches provided Figma mockups exactly
- [ ] Responsive design works on mobile (320px+)
- [ ] Maintains brand consistency
- [ ] Meets WCAG 2.1 AA accessibility standards

### Technical Requirements
- [ ] Performance impact < 100ms load time increase
- [ ] Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- [ ] Backwards compatibility maintained

## Definition of Done
- [ ] Code review completed
- [ ] Design review approved
- [ ] QA testing passed (see QA checklist)
- [ ] Accessibility audit passed
- [ ] Performance testing completed
- [ ] Documentation updated

## Figma Mockups
- Desktop: [Figma link]
- Mobile: [Figma link]
- Interactive prototype: [Figma link]

## QA Testing Checklist
### Functional Testing
- [ ] Happy path user flow works
- [ ] Edge cases handled gracefully
- [ ] Error states display correctly
- [ ] Loading states appropriate

### Cross-Browser Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

### Device Testing
- [ ] Desktop (1920x1080)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)
- [ ] Mobile (320x568)

### Accessibility Testing
- [ ] Keyboard navigation works
- [ ] Screen reader compatibility
- [ ] Color contrast ratios pass
- [ ] Focus indicators visible

### Performance Testing
- [ ] Page load time < 3 seconds
- [ ] First contentful paint < 1.5 seconds
- [ ] No layout shifts
```

### Phase 5: QA/Verification Checkpoints

**Per Milestone QA Process:**

1. **Design Review Checkpoint**
   - Figma mockups match acceptance criteria
   - Design system consistency maintained
   - Accessibility considerations addressed
   - Mobile responsiveness planned

2. **Development Checkpoint**
   - Code follows established patterns
   - Performance benchmarks met
   - Accessibility features implemented
   - Cross-browser compatibility verified

3. **User Testing Checkpoint** (for major milestones)
   - Usability testing with 3-5 target users
   - A/B testing setup (if applicable)
   - Feedback incorporation plan
   - Success metrics measurement plan

4. **Launch Readiness Checkpoint**
   - All acceptance criteria verified
   - QA checklist completed
   - Performance monitoring in place
   - Rollback plan documented

### Phase 6: Figma Mockup Requirements

**Mockup Standards Per Ticket:**

**Required Artboards:**
- Desktop (1920x1080)
- Tablet (768x1024) - if responsive
- Mobile (375x667)
- Mobile (320x568) - if complex layout

**Required States:**
- Default state
- Hover states (interactive elements)
- Active/selected states
- Loading states
- Error states
- Empty states

**Design System Integration:**
- Use existing component library
- Document new components created
- Specify spacing using 8px grid
- Include typography specifications
- Color values from brand palette
- Icon specifications and usage

**Annotations Required:**
- Interaction specifications
- Animation/transition details
- Responsive behavior notes
- Accessibility considerations
- Implementation notes for developers

**Prototype Requirements:**
- Key user flows prototyped
- Interaction demonstrations
- State transitions shown
- Share settings: "Anyone with link can view"

## Tools Integration

### Linear Integration
- Use `linear_create_issue` for ticket generation
- Include milestone assignment
- Set appropriate labels (ux, design, frontend)
- Link related issues with blocking/blocked relationships

### Figma Integration
- Use `figma_get_figma_data` to extract design specifications
- Use `figma_download_figma_images` to get assets for development
- Maintain design system consistency

## Usage Examples

### Quick UX Audit
```
Please conduct a UX audit of my checkout page. Here are the current screenshots:
[attach screenshots]

Goals: Increase conversion rate by 10%
Constraints: No backend changes allowed, 2-week timeline
Target audience: E-commerce shoppers, mobile-first users
```

### Full UX Overhaul
```
I need a complete UX overhaul of our dashboard. Current state attached.

Goals: 
- Reduce time-to-insight by 50%
- Decrease support tickets by 25%
- Improve user satisfaction (current NPS: 6)

Constraints: 
- Must work with existing API
- 8-week timeline
- Accessibility compliance required

Target Audience: Business analysts, daily users, intermediate tech skills
```

## Best Practices

1. **Always start with user needs** - Technology serves users, not the other way around
2. **Measure everything** - Define success metrics before starting
3. **Iterate based on data** - Use analytics and user feedback to guide decisions
4. **Design for accessibility first** - Inclusive design benefits everyone
5. **Test early and often** - Validate assumptions with real users
6. **Document decisions** - Future teams need context for design choices
7. **Think in systems** - Maintain consistency across the entire product
8. **Consider edge cases** - Design for error states and unusual scenarios

## Common Pitfalls

- **Skipping user research** - Assumptions often lead to poor solutions
- **Designing in isolation** - Not considering system-wide impacts
- **Ignoring technical constraints** - Beautiful designs that can't be built
- **Perfectionism paralysis** - Waiting too long for the "perfect" solution
- **Not measuring impact** - Deploying changes without tracking success
- **Forgetting maintenance** - Not planning for ongoing updates and improvements