# UX Kickoff Skill

**Purpose:** Streamline UX project initiation with structured intake, Figma setup, journey mapping, and Linear ticket management.

**MCP Tools Used:** `figma_get_figma_data`, `linear_*` tools

## Workflow Overview

This skill provides a systematic approach to launching UX projects from initial requirements through stakeholder alignment.

### Phase 1: Project Intake

**Goal:** Gather comprehensive project context and constraints

**Process:**
1. **Product Requirements Collection**
   - Document business objectives and success metrics
   - Identify core user problems to solve
   - Define feature scope and MVP boundaries
   - Capture technical constraints and dependencies

2. **Target Audience Research**
   - Define primary and secondary user personas
   - Document user goals, pain points, and contexts
   - Identify accessibility requirements
   - Note localization needs if applicable

3. **Platform & Technical Constraints**
   - Specify target platforms (web, mobile, desktop)
   - Document device/browser support requirements
   - Identify performance constraints
   - Note existing design system or brand guidelines

**Deliverable:** Project brief document with all intake information

### Phase 2: Figma Project Setup

**Goal:** Establish organized Figma workspace with proper structure

**Process:**
1. **Figma File Analysis**
   - Use `figma_get_figma_data(fileKey)` to inspect existing files
   - Analyze current structure and components
   - Identify reusable elements and patterns

2. **Project Organization**
   - Create page structure: Research → Wireframes → Designs → Handoff
   - Set up component library if not existing
   - Establish naming conventions and file structure
   - Configure design tokens and styles

3. **Asset Extraction** (if needed)
   - Use `figma_download_figma_images()` for existing assets
   - Organize downloaded assets in project structure

**Deliverable:** Organized Figma project ready for design work

### Phase 3: User Journey Mapping & Screen Inventory

**Goal:** Map complete user experience and catalog required screens

**Process:**
1. **Journey Mapping**
   - Document user flows from entry to completion
   - Identify decision points and error states
   - Map emotional journey and pain points
   - Note cross-platform interactions

2. **Screen Inventory**
   - List all unique screens/views required
   - Categorize by user type and use case
   - Define screen relationships and navigation
   - Identify shared components and patterns

3. **Information Architecture**
   - Create sitemap or app structure
   - Define navigation patterns
   - Plan content hierarchy and organization

**Deliverable:** User journey maps and comprehensive screen inventory

### Phase 4: Design System Token Extraction

**Goal:** Extract and document design tokens from existing systems

**Process:**
1. **Figma Analysis**
   - Use `figma_get_figma_data()` to extract:
     - Color palette and semantic tokens
     - Typography scales and styles
     - Spacing and layout tokens
     - Component variants and properties

2. **Token Documentation**
   - Create design token specification
   - Map semantic meanings to visual properties
   - Document usage guidelines and constraints
   - Plan token naming conventions

3. **System Audit**
   - Identify inconsistencies in current system
   - Recommend token consolidation opportunities
   - Plan for responsive and accessible tokens

**Deliverable:** Design token specification and usage guidelines

### Phase 5: Linear Ticket Creation

**Goal:** Create structured development tickets for each screen and journey

**Process:**
1. **Project Setup**
   - Use `linear_create_project()` for the UX project
   - Set up appropriate labels and milestones
   - Configure project workflow states

2. **Screen-Based Tickets**
   - Use `linear_create_issue()` for each screen in inventory
   - Include:
     - User story format ("As a [user], I want...")
     - Acceptance criteria
     - Design specifications
     - Technical requirements
     - Links to Figma designs

3. **Journey-Based Tickets**
   - Create tickets for complete user flows
   - Include interaction specifications
   - Document state management requirements
   - Add cross-screen dependencies

4. **Ticket Organization**
   - Use `linear_update_issue()` to link related tickets
   - Set priorities and estimates
   - Assign to appropriate team members
   - Configure due dates and milestones

**Deliverable:** Complete Linear project with organized development tickets

### Phase 6: Stakeholder Review Checkpoints

**Goal:** Establish regular review points for alignment and feedback

**Process:**
1. **Review Schedule Setup**
   - Plan review checkpoints at each phase completion
   - Create calendar events and stakeholder notifications
   - Define review materials and presentations

2. **Feedback Collection**
   - Use `linear_create_comment()` to document feedback
   - Track decisions and change requests
   - Update designs and tickets based on feedback

3. **Approval Tracking**
   - Document stakeholder sign-offs
   - Track scope changes and their impacts
   - Maintain change log and rationale

**Deliverable:** Stakeholder review schedule and feedback tracking system

## Usage Examples

### Basic Project Kickoff
```bash
# Start with Figma analysis
figma_get_figma_data(fileKey="abc123", nodeId="1234:5678")

# Create Linear project
linear_create_project(name="Mobile App Redesign", team="Design")

# Create screen tickets
linear_create_issue(title="Login Screen Design", team="Design", 
                   description="Design login screen with social auth options")
```

### Design System Integration
```bash
# Extract design tokens from Figma
figma_get_figma_data(fileKey="design-system-key")

# Create design system documentation tickets
linear_create_issue(title="Design Token Documentation", 
                   description="Document color, typography, and spacing tokens")
```

## Templates & Checklists

### Project Intake Checklist
- [ ] Business objectives defined
- [ ] User personas documented
- [ ] Platform requirements specified
- [ ] Technical constraints identified
- [ ] Success metrics established

### Figma Setup Checklist
- [ ] File structure organized
- [ ] Component library configured
- [ ] Design tokens defined
- [ ] Naming conventions established
- [ ] Collaboration permissions set

### Linear Project Checklist
- [ ] Project created with proper team assignment
- [ ] Screen inventory tickets created
- [ ] User journey tickets created
- [ ] Dependencies mapped between tickets
- [ ] Review milestones scheduled

## Tips & Best Practices

1. **Start Small:** Focus on MVP screens first, then expand
2. **Stay Organized:** Use consistent naming across Figma and Linear
3. **Document Everything:** Capture decisions and rationale in comments
4. **Regular Syncs:** Schedule frequent check-ins with stakeholders
5. **Iterative Approach:** Plan for multiple design and feedback cycles

## Integration Notes

- **Figma → Linear:** Link Figma frames directly in Linear ticket descriptions
- **Design System:** Reference design tokens in development tickets
- **Handoff:** Use Linear attachments for final design specifications
- **Reviews:** Schedule Linear milestone reviews with stakeholders