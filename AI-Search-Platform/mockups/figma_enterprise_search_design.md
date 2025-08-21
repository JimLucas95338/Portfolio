# Enterprise AI Search Platform - Figma Design Specifications

Figma Mockup Guide for Enterprise Search GUI
---

## **📐 Frame Setup**

### **Desktop Frames**
- **Main Interface**: 1400x900px 
- **Full Desktop**: 1920x1080px (for presentation context)
- **Laptop**: 1440x900px (MacBook Pro standard)

### **Responsive Frames**
- **Tablet**: 1024x768px (iPad landscape)
- **Mobile**: 375x812px (iPhone 13 Pro)

---

## **🎨 Design System**

### **Color Palette**
```figma
Primary Colors:
🔷 Primary Blue: #2C5282
🔘 Secondary Gray: #4A5568
🟢 Success Green: #38A169
🟡 Warning Orange: #D69E2E
🔴 Danger Red: #E53E3E

Background Colors:
⚪ White: #FFFFFF
🔘 Light Gray: #F7FAFC
🔘 Gray 100: #F7FAFC
🔘 Gray 200: #EDF2F7
🔘 Gray 300: #E2E8F0
🔘 Gray 600: #718096
🔘 Gray 800: #2D3748
🌫️ App Background: #F8F9FA
```

### **Typography System**
```figma
Font Family: System Default (Arial/Helvetica)

Headers:
- H1 (Main Title): Bold 20px/28px, #2D3748
- H2 (Section Headers): Bold 16px/24px, #4A5568
- H3 (Subsections): Bold 14px/20px, #718096

Body Text:
- Large Body: Regular 14px/20px, #2D3748
- Medium Body: Regular 12px/18px, #4A5568
- Small Text: Regular 10px/14px, #718096

UI Elements:
- Button Text: Medium 12px/16px
- Input Text: Regular 11px/16px
- Labels: Medium 10px/14px
```

### **Spacing System** (8px Grid)
```figma
Base Unit: 8px

Micro Spacing:
- 4px: Element borders, fine adjustments
- 8px: Component internal padding
- 12px: Small component spacing

Standard Spacing:
- 16px: Standard component padding
- 20px: Section padding (matches GUI)
- 24px: Large component spacing

Macro Spacing:
- 32px: Section margins
- 40px: Page margins
- 60px: Major section separation
```

---

## ** Layout Structure**

### **1. Header Section** (Height: 80px)
```figma
Background: Linear Gradient (#2C5282 to #4A5568)
Padding: 20px horizontal

Left Section (Logo Area):
- Enterprise AI Search Platform logo/title
- Font: Bold 18px, White
- Icon: 🔍 (20px)

Center Section (Navigation):
- Search | Analytics | History | Settings
- Font: Medium 14px, rgba(255,255,255,0.9)
- Hover state: rgba(255,255,255,1)

Right Section (User Area):
- User avatar (32px circle)
- Username: "enterprise_user"
- Dropdown indicator
- Font: Medium 12px, White
```

### **2. Search Section** (Height: 120px)
```figma
Background: White (#FFFFFF)
Border Bottom: 1px solid #E2E8F0
Padding: 20px

Search Bar Container:
- Background: #F7FAFC
- Border: 1px solid #E2E8F0
- Border Radius: 8px
- Height: 48px
- Drop Shadow: 0 2px 4px rgba(0,0,0,0.04)

Search Input:
- Padding: 12px 16px
- Font: Regular 14px, #2D3748
- Placeholder: "Search across your enterprise knowledge base..."
- Color: #A0AEC0

Search Button:
- Background: #2C5282
- Width: 120px, Height: 48px
- Border Radius: 8px (right side only)
- Text: "Search" - Medium 14px, White
- Icon: 🔍 (16px, left aligned)

Quick Filters (Below search bar):
- Recent | Documents | Code | Wiki
- Pills: Background #EDF2F7, Border Radius 16px
- Padding: 6px 12px
- Font: Medium 11px, #4A5568
```

### **3. Main Content Area** (Flexible Height)
```figma
Layout: 3-column grid

Left Sidebar (300px):
┌─ Search History ─────────────┐
│ Background: White            │
│ Border: 1px solid #E2E8F0  │
│ Border Radius: 8px           │
│ Padding: 16px                │
│                              │
│ Recent Searches:             │
│ • "AI market analysis"       │
│ • "competitive landscape"    │
│ • "product roadmap"          │
│                              │
│ Saved Queries:               │
│ ⭐ "Weekly reports"         │
│ ⭐ "Team updates"           │
└─────────────────────────────┘

Center Content (800px):
┌─ Search Results ─────────────┐
│ Welcome State:               │
│ - Large search icon (64px)   │
│ - "Ready to search"          │
│ - Feature highlights         │
│                              │
│ Results State:               │
│ - Result count & timing      │
│ - Individual result cards    │
│ - Pagination controls        │
└───────────────────────────-──┘

Right Sidebar (300px):
┌─ Analytics Panel ───────────┐
│ Search Statistics:          │
│ • Total searches today      │
│ • Average response time     │
│ • Top categories            │
│                             │
│ Quick Actions:              │
│ 📊 View Analytics          │
│ 📁 Export Results          │
│ ⚙️ Advanced Filters        │
└───────────────────────────-─┘
```

---

## **🎯 Key Components**

### **Search Result Card**
```figma
Container:
- Background: White
- Border: 1px solid #E2E8F0
- Border Radius: 8px
- Padding: 20px
- Margin Bottom: 16px
- Drop Shadow: 0 2px 8px rgba(0,0,0,0.06)
- Hover: Shadow increases to 0 4px 12px rgba(0,0,0,0.1)

Header Section:
- Title: Bold 16px, #2D3748 (clickable link)
- Source: Medium 12px, #2C5282
- Confidence Badge: 
  * High (90%+): Green pill with ✓
  * Medium (70-89%): Orange pill with ~
  * Low (<70%): Gray pill with ?

Content Preview:
- Snippet: Regular 14px, #4A5568
- Max 3 lines with ellipsis
- Highlighted search terms: Bold + Yellow background

Footer Section:
- Last Updated: Regular 10px, #718096
- Document Type: Pill badge
- Share/Save icons (16px)
```

### **Confidence Indicator Component**
```figma
High Confidence (90%+):
- Background: #C6F6D5 (light green)
- Border: 1px solid #38A169
- Text: "High Confidence" - Bold 10px, #22543D
- Icon: ✓ (12px, green)

Medium Confidence (70-89%):
- Background: #FEEBC8 (light orange)
- Border: 1px solid #D69E2E
- Text: "Medium Confidence" - Bold 10px, #744210
- Icon: ~ (12px, orange)

Low Confidence (<70%):
- Background: #EDF2F7 (light gray)
- Border: 1px solid #A0AEC0
- Text: "Needs Verification" - Bold 10px, #4A5568
- Icon: ? (12px, gray)
```

### **Loading States**
```figma
Search Loading:
- Spinner: 24px, #2C5282
- Text: "Searching..." - Regular 14px, #4A5568
- Background: Semi-transparent overlay

Result Loading:
- Skeleton cards with animated gradients
- Title: 200px width shimmer bar
- Content: 3 lines of varied width shimmer bars
- Duration: 1.5s ease-in-out infinite
```

---

## **📱 Mobile Responsive Design**

### **Mobile Layout (375px)**
```figma
Header (Collapsed):
- Height: 60px
- Hamburger menu (left)
- Search icon (right)
- Title centered

Search Section:
- Full-width search bar
- Voice search icon
- Recent searches as horizontal chips

Results:
- Single column cards
- Simplified result display
- Infinite scroll
- Floating action button for filters
```

### **Tablet Layout (1024px)**
```figma
2-Column Layout:
- Search and results (70%)
- History and analytics (30%)
- Responsive grid system
- Touch-friendly targets (44px minimum)
```

---

## **🎭 Interactive States**

### **Hover States**
```figma
Buttons:
- Background color 10% darker
- Slight scale (1.02x)
- Transition: 0.2s ease

Cards:
- Increased shadow depth
- Subtle lift effect
- Border color change

Links:
- Underline appears
- Color darkens slightly
```

### **Focus States**
```figma
Input Fields:
- Border: 2px solid #2C5282
- Glow: 0 0 0 3px rgba(44, 82, 130, 0.1)
- Remove default outline

Buttons:
- Same as hover + focus ring
- High contrast for accessibility
```

### **Error States**
```figma
Search Errors:
- Red border on search input
- Error message below: Regular 12px, #E53E3E
- Icon: ⚠️ (16px, red)

No Results:
- Large illustration (200px)
- "No results found" - Bold 18px, #4A5568
- Suggestions below - Regular 14px, #718096
```

---

## **🔧 Figma Setup Instructions**

### **Step 1: Create Design System**
1. **Create color styles** for each color in the palette
2. **Set up text styles** for all typography variants
3. **Create effect styles** for shadows and glows
4. **Build component library** with all UI elements

### **Step 2: Build Components**
1. **Search Bar Component** with variants (default, focused, error)
2. **Result Card Component** with confidence variants
3. **Button Components** (primary, secondary, ghost)
4. **Input Components** with all states
5. **Badge Components** for confidence and tags

### **Step 3: Create Main Screens**
1. **Welcome State** - Empty search interface
2. **Search Results** - Populated with sample results
3. **Loading State** - During search processing
4. **Error State** - No results or search errors
5. **Analytics View** - Search statistics and insights

### **Step 4: Responsive Variants**
1. **Desktop** (1400px) - Full feature set
2. **Laptop** (1200px) - Slightly condensed
3. **Tablet** (1024px) - 2-column layout
4. **Mobile** (375px) - Single column, simplified

### **Step 5: Interactive Prototype**
1. **Create user flows** between screens
2. **Add hover interactions** for all interactive elements
3. **Set up search flow** with loading and results
4. **Add micro-interactions** for enhanced UX

---

## **🎬 Animation Specifications**

### **Search Animation**
```figma
Search Button Press:
- Scale: 0.95x for 0.1s
- Return to 1.0x over 0.2s
- Background color darkens 15%

Loading Spinner:
- 360° rotation over 1s
- Ease-in-out timing
- Infinite loop during search

Results Appear:
- Fade in from 0 to 1 opacity over 0.3s
- Slide up 20px over 0.3s
- Stagger delay: 0.1s between cards
```

### **Micro-Interactions**
```figma
Card Hover:
- Scale: 1.02x over 0.2s
- Shadow increase over 0.2s
- Ease-out timing

Confidence Badge Pulse:
- Scale from 1.0x to 1.05x to 1.0x
- Duration: 2s
- Only on high confidence results
```

---

## **📊 Sample Content for Mockups**

### **Search Queries**
- "AI market analysis for Q4 2024"
- "Competitive landscape enterprise search"
- "Product roadmap artificial intelligence"
- "RAG implementation best practices"

### **Sample Results**
```figma
Result 1:
Title: "Enterprise AI Market Report 2024"
Source: market-research.pdf
Confidence: High (94%)
Snippet: "The enterprise AI market is projected to reach $50B by 2024, with search applications leading adoption..."

Result 2:
Title: "RAG Implementation Guidelines"
Source: engineering-docs/ai-search.md
Confidence: High (91%)
Snippet: "Retrieval-Augmented Generation (RAG) combines the power of large language models with real-time information retrieval..."

Result 3:
Title: "Competitive Analysis: Search Platforms"
Source: strategy/competitive-analysis.xlsx
Confidence: Medium (87%)
Snippet: "Analysis of 15 enterprise search platforms including Elasticsearch, Microsoft Search, and emerging AI solutions..."
```

### **Analytics Sample Data**
- Total Searches Today: 1,247
- Average Response Time: 0.8s
- User Satisfaction: 94%
- Top Categories: Documents (45%), Code (30%), Wiki (25%)

---

## **🚀 Export Assets**

### **Icons Needed** (16px, 24px, 32px)
- Search (🔍)
- Filter (⚙️)
- Star (⭐)
- Check (✓)
- Warning (⚠️)
- User (👤)
- Analytics (📊)
- Export (📁)

### **Illustrations**
- Empty state illustration (300x200px)
- No results illustration (200x150px)
- Error state illustration (150x100px)

---

## **📋 Figma File Organization**

```
📄 Cover Page
   - Project overview and navigation

📄 Design System
   - Colors, typography, spacing
   - Component library
   - Style guide

📄 Desktop Designs
   - Welcome state
   - Search results
   - Analytics view
   - Error states

📄 Mobile Designs
   - All mobile screen variants
   - Touch interactions

📄 Prototypes
   - Interactive user flows
   - Animation demonstrations

📄 Developer Handoff
   - Specifications and assets
   - Code snippets
   - Implementation notes
```

---

## **💡 Professional Tips**

### **Design Excellence**
1. **Use consistent spacing** - Stick to 8px grid system
2. **Maintain visual hierarchy** - Clear information structure
3. **Ensure accessibility** - WCAG 2.1 AA compliance
4. **Professional polish** - Subtle shadows, proper alignment
5. **Real content** - Use actual search queries and results

### **Stakeholder Presentation**
1. **Create overview slides** showing key screens
2. **Demonstrate user flows** with interactive prototypes
3. **Show responsive behavior** across devices
4. **Highlight unique features** (confidence indicators, real-time search)
5. **Include business metrics** (search satisfaction, efficiency gains)

---

**This Figma design will showcase your Enterprise AI Search Platform with professional-grade UI/UX design, demonstrating both technical capability and design excellence for your Senior AI Product Manager portfolio!** 🎨🚀
