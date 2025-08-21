"""
Code-to-Figma Design Converter
=============================

Automatically extracts design specifications from GUI code and generates
Figma-compatible design tokens and component specifications.

This tool analyzes your enterprise_search_gui.py and outputs structured
design data that can be imported into Figma or used with AI design tools.
"""

import re
import json
import ast
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class ColorToken:
    """Design token for colors."""
    name: str
    value: str
    description: str
    category: str

@dataclass
class TypographyToken:
    """Design token for typography."""
    name: str
    font_family: str
    font_size: int
    font_weight: str
    line_height: Optional[str] = None
    color: Optional[str] = None

@dataclass
class SpacingToken:
    """Design token for spacing."""
    name: str
    value: int
    description: str

@dataclass
class ComponentSpec:
    """Component specification for Figma."""
    name: str
    width: Optional[int]
    height: Optional[int]
    padding: Optional[str]
    margin: Optional[str]
    background: Optional[str]
    border: Optional[str]
    border_radius: Optional[str]
    properties: Dict[str, Any]

class CodeToFigmaConverter:
    """
    Converts GUI code to Figma design specifications.
    
    Analyzes tkinter GUI code and extracts:
    - Color palette
    - Typography system
    - Spacing values
    - Component specifications
    - Layout structure
    """
    
    def __init__(self, code_file_path: str):
        self.code_file_path = Path(code_file_path)
        self.code_content = self._read_code_file()
        
        # Design tokens
        self.colors: List[ColorToken] = []
        self.typography: List[TypographyToken] = []
        self.spacing: List[SpacingToken] = []
        self.components: List[ComponentSpec] = []
        
        print(f"🔍 Analyzing GUI code: {self.code_file_path.name}")
    
    def _read_code_file(self) -> str:
        """Read the GUI code file."""
        try:
            with open(self.code_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"❌ Code file not found: {self.code_file_path}")
            return ""
    
    def extract_colors(self) -> List[ColorToken]:
        """Extract color palette from GUI code."""
        print("🎨 Extracting color palette...")
        
        # Find color definitions in the code
        color_pattern = r"['\"]([a-zA-Z_]+)['\"]:\s*['\"]?(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3})['\"]?"
        color_matches = re.findall(color_pattern, self.code_content)
        
        # Standard color categories
        color_categories = {
            'primary': 'Primary Colors',
            'secondary': 'Secondary Colors', 
            'success': 'Status Colors',
            'warning': 'Status Colors',
            'danger': 'Status Colors',
            'error': 'Status Colors',
            'gray': 'Neutral Colors',
            'white': 'Base Colors',
            'black': 'Base Colors',
            'light': 'Background Colors',
            'dark': 'Background Colors'
        }
        
        for name, value in color_matches:
            category = 'Other'
            for key, cat in color_categories.items():
                if key in name.lower():
                    category = cat
                    break
            
            color_token = ColorToken(
                name=name.replace('_', ' ').title(),
                value=value.upper(),
                description=f"Used for {name.replace('_', ' ')} elements",
                category=category
            )
            self.colors.append(color_token)
        
        # Add common GUI colors if found in geometry/configure calls
        geometry_colors = self._extract_inline_colors()
        self.colors.extend(geometry_colors)
        
        print(f"   ✅ Found {len(self.colors)} color tokens")
        return self.colors
    
    def _extract_inline_colors(self) -> List[ColorToken]:
        """Extract colors from inline style definitions."""
        inline_colors = []
        
        # Find configure calls with color values
        configure_pattern = r"configure\([^)]*(?:bg|background|fg|foreground)=['\"](#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3})['\"][^)]*\)"
        matches = re.findall(configure_pattern, self.code_content)
        
        for i, color in enumerate(set(matches)):
            inline_colors.append(ColorToken(
                name=f"Inline Color {i+1}",
                value=color.upper(),
                description="Color found in component styling",
                category="Component Colors"
            ))
        
        return inline_colors
    
    def extract_typography(self) -> List[TypographyToken]:
        """Extract typography system from GUI code."""
        print("📝 Extracting typography system...")
        
        # Find font definitions
        font_pattern = r"font=\(['\"]([^'\"]+)['\"],\s*(\d+)(?:,\s*['\"]([^'\"]*)['\"])?\)"
        font_matches = re.findall(font_pattern, self.code_content)
        
        for i, (family, size, weight) in enumerate(font_matches):
            weight = weight or 'normal'
            
            self.typography.append(TypographyToken(
                name=f"Font Style {i+1}",
                font_family=family,
                font_size=int(size),
                font_weight=weight,
                line_height=f"{int(size) * 1.4}px"  # Standard 1.4 line height
            ))
        
        print(f"   ✅ Found {len(self.typography)} typography tokens")
        return self.typography
    
    def extract_spacing(self) -> List[SpacingToken]:
        """Extract spacing system from GUI code."""
        print("📏 Extracting spacing system...")
        
        # Find padding/margin values
        spacing_patterns = [
            r"padx=(\d+)",
            r"pady=(\d+)", 
            r"ipadx=(\d+)",
            r"ipady=(\d+)",
            r"padding[\"']=(\d+)",
            r"margin[\"']=(\d+)"
        ]
        
        spacing_values = set()
        for pattern in spacing_patterns:
            matches = re.findall(pattern, self.code_content)
            spacing_values.update(int(m) for m in matches)
        
        # Create spacing tokens
        for value in sorted(spacing_values):
            if value <= 4:
                category = "Micro"
            elif value <= 16:
                category = "Small"
            elif value <= 32:
                category = "Medium"
            else:
                category = "Large"
            
            self.spacing.append(SpacingToken(
                name=f"Space {value}",
                value=value,
                description=f"{category} spacing - {value}px"
            ))
        
        print(f"   ✅ Found {len(self.spacing)} spacing tokens")
        return self.spacing
    
    def extract_components(self) -> List[ComponentSpec]:
        """Extract component specifications from GUI code."""
        print("🧩 Extracting component specifications...")
        
        # Find window geometry
        geometry_match = re.search(r'geometry\(["\'](\d+)x(\d+)["\']', self.code_content)
        if geometry_match:
            width, height = geometry_match.groups()
            self.components.append(ComponentSpec(
                name="Main Window",
                width=int(width),
                height=int(height),
                padding=None,
                margin=None,
                background="#f8f9fa",
                border=None,
                border_radius=None,
                properties={"type": "container", "layout": "grid"}
            ))
        
        # Find frame components
        frame_pattern = r'(\w+)\s*=\s*tk\.Frame\([^)]*\)'
        frame_matches = re.findall(frame_pattern, self.code_content)
        
        for frame_name in frame_matches:
            # Try to find styling for this frame
            style_pattern = f'{frame_name}[^=]*=.*?configure\\([^)]*\\)'
            style_match = re.search(style_pattern, self.code_content)
            
            properties = {"type": "frame", "name": frame_name}
            
            if style_match:
                style_text = style_match.group(0)
                
                # Extract background color
                bg_match = re.search(r'(?:bg|background)=["\']([^"\']+)["\']', style_text)
                background = bg_match.group(1) if bg_match else None
                
                # Extract padding
                padx_match = re.search(r'padx=(\d+)', style_text)
                pady_match = re.search(r'pady=(\d+)', style_text)
                padding = None
                if padx_match and pady_match:
                    padding = f"{pady_match.group(1)}px {padx_match.group(1)}px"
                
                self.components.append(ComponentSpec(
                    name=frame_name.replace('_', ' ').title(),
                    width=None,
                    height=None,
                    padding=padding,
                    margin=None,
                    background=background,
                    border=None,
                    border_radius=None,
                    properties=properties
                ))
        
        # Add common UI components
        self._add_common_components()
        
        print(f"   ✅ Found {len(self.components)} component specifications")
        return self.components
    
    def _add_common_components(self):
        """Add specifications for common UI components."""
        common_components = [
            ComponentSpec(
                name="Search Bar",
                width=None,
                height=48,
                padding="12px 16px",
                margin=None,
                background="#F7FAFC",
                border="1px solid #E2E8F0",
                border_radius="8px",
                properties={
                    "type": "input",
                    "placeholder": "Search across your enterprise knowledge base...",
                    "font_size": 14
                }
            ),
            ComponentSpec(
                name="Primary Button",
                width=120,
                height=48,
                padding="12px 24px",
                margin=None,
                background="#2C5282",
                border="none",
                border_radius="8px",
                properties={
                    "type": "button",
                    "color": "white",
                    "font_weight": "medium",
                    "font_size": 14
                }
            ),
            ComponentSpec(
                name="Result Card",
                width=None,
                height=None,
                padding="20px",
                margin="0 0 16px 0",
                background="white",
                border="1px solid #E2E8F0",
                border_radius="8px",
                properties={
                    "type": "card",
                    "shadow": "0 2px 8px rgba(0,0,0,0.06)",
                    "hover_shadow": "0 4px 12px rgba(0,0,0,0.1)"
                }
            )
        ]
        
        self.components.extend(common_components)
    
    def generate_figma_tokens(self) -> Dict[str, Any]:
        """Generate Figma-compatible design tokens."""
        print("🎨 Generating Figma design tokens...")
        
        tokens = {
            "colors": {},
            "typography": {},
            "spacing": {},
            "components": {}
        }
        
        # Colors
        for color in self.colors:
            tokens["colors"][color.name.lower().replace(' ', '_')] = {
                "value": color.value,
                "description": color.description,
                "category": color.category
            }
        
        # Typography  
        for i, typo in enumerate(self.typography):
            tokens["typography"][f"text_{i+1}"] = {
                "fontFamily": typo.font_family,
                "fontSize": typo.font_size,
                "fontWeight": typo.font_weight,
                "lineHeight": typo.line_height
            }
        
        # Spacing
        for space in self.spacing:
            tokens["spacing"][space.name.lower().replace(' ', '_')] = {
                "value": f"{space.value}px",
                "description": space.description
            }
        
        # Components
        for comp in self.components:
            tokens["components"][comp.name.lower().replace(' ', '_')] = asdict(comp)
        
        return tokens
    
    def generate_figma_prompt(self) -> str:
        """Generate AI prompt for Figma creation."""
        print("🤖 Generating AI design prompt...")
        
        prompt = f"""
Create a professional enterprise AI search interface with these specifications:

LAYOUT:
- Main window: {self.components[0].width if self.components else 1400}x{self.components[0].height if self.components else 900}px
- 3-column layout: Search history (300px) | Results (800px) | Analytics (300px)

COLORS:
"""
        
        # Add color specifications
        for color in self.colors[:8]:  # Limit to main colors
            prompt += f"- {color.name}: {color.value}\n"
        
        prompt += f"""
TYPOGRAPHY:
- Primary font: {self.typography[0].font_family if self.typography else 'Arial'}
- Sizes: {', '.join([f'{t.font_size}px' for t in self.typography[:3]])}

COMPONENTS:
"""
        
        # Add key components
        for comp in self.components[:5]:
            if comp.height:
                prompt += f"- {comp.name}: {comp.height}px height"
                if comp.background:
                    prompt += f", {comp.background} background"
                if comp.border_radius:
                    prompt += f", {comp.border_radius} radius"
                prompt += "\n"
        
        prompt += """
STYLE: Professional enterprise software interface, clean and modern design.
"""
        
        return prompt.strip()
    
    def export_design_system(self, output_path: str = "design_system.json"):
        """Export complete design system to JSON."""
        print(f"📤 Exporting design system to {output_path}...")
        
        # Extract all design elements
        self.extract_colors()
        self.extract_typography()
        self.extract_spacing()
        self.extract_components()
        
        # Generate tokens
        tokens = self.generate_figma_tokens()
        
        # Add metadata
        design_system = {
            "meta": {
                "name": "Enterprise AI Search Platform",
                "version": "1.0.0",
                "generated_from": str(self.code_file_path),
                "generated_at": "2024-01-15T10:00:00Z"
            },
            "tokens": tokens,
            "ai_prompt": self.generate_figma_prompt()
        }
        
        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(design_system, f, indent=2)
        
        print(f"✅ Design system exported successfully!")
        return design_system
    
    def print_summary(self):
        """Print extraction summary."""
        print("\n" + "="*50)
        print("📊 DESIGN EXTRACTION SUMMARY")
        print("="*50)
        print(f"Colors found: {len(self.colors)}")
        print(f"Typography styles: {len(self.typography)}")  
        print(f"Spacing values: {len(self.spacing)}")
        print(f"Components: {len(self.components)}")
        print("\n🎨 Top Colors:")
        for color in self.colors[:5]:
            print(f"  • {color.name}: {color.value}")
        print("\n📝 Typography:")
        for typo in self.typography[:3]:
            print(f"  • {typo.font_family} {typo.font_size}px {typo.font_weight}")
        print("="*50)

def main():
    """Demo the code-to-Figma converter."""
    print("🚀 Code-to-Figma Design Converter")
    print("=" * 50)
    
    # Path to your GUI code
    gui_code_path = "../src/enterprise_search_gui.py"
    
    if not Path(gui_code_path).exists():
        print(f"❌ GUI code not found at: {gui_code_path}")
        print("💡 Make sure to run this from the mockups directory")
        return
    
    # Create converter and extract design system
    converter = CodeToFigmaConverter(gui_code_path)
    
    # Export design system
    design_system = converter.export_design_system("enterprise_search_design_system.json")
    
    # Print summary
    converter.print_summary()
    
    # Generate AI prompt
    ai_prompt = converter.generate_figma_prompt()
    
    print("\n🤖 AI DESIGN PROMPT:")
    print("-" * 30)
    print(ai_prompt)
    print("-" * 30)
    
    print("\n💡 NEXT STEPS:")
    print("1. Copy the AI prompt above")
    print("2. Paste into Uizard, Galileo AI, or Figma AI plugin")
    print("3. Use the generated design_system.json for precise styling")
    print("4. Import to Figma for final refinement")
    
    print(f"\n✅ Design system ready! Check 'enterprise_search_design_system.json'")

if __name__ == "__main__":
    main()
