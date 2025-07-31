"""Example: Draw a house with bricks and trees using rectangles.

This example demonstrates how to use the CAD datamodel to create
a simple house drawing and export it to SVG.
"""

from cad_datamodel.document import Document
from cad_datamodel.persistence.svg import SVGExporter
from cad_datamodel.shapes import Rectangle, Style


def create_house_drawing():
    """Create a house drawing with rectangles."""
    # Create document with larger canvas for the house
    doc = Document(canvas_width=1000, canvas_height=800)
    
    # Define colors
    wall_color = "#f4e4c1"  # Beige for walls
    roof_color = "#8b4513"  # Brown for roof
    door_color = "#654321"  # Dark brown for door
    window_color = "#87ceeb"  # Sky blue for windows
    brick_color = "#b22222"  # Fire brick red
    tree_trunk_color = "#654321"  # Brown for tree trunk
    tree_foliage_color = "#228b22"  # Forest green for foliage
    grass_color = "#90ee90"  # Light green for grass
    
    # Ground/grass
    grass = Rectangle(
        x=0, y=600, width=1000, height=200,
        layer_id="ground",
        style=Style(fill_color=grass_color)
    )
    doc.add_shape(grass)
    
    # House base/walls
    house_base = Rectangle(
        x=300, y=300, width=400, height=300,
        layer_id="house",
        style=Style(fill_color=wall_color, stroke_color="#000000", stroke_width=2)
    )
    doc.add_shape(house_base)
    
    # Roof (as a rectangle - simplified)
    roof = Rectangle(
        x=250, y=250, width=500, height=80,
        layer_id="house",
        style=Style(fill_color=roof_color, stroke_color="#000000", stroke_width=2)
    )
    doc.add_shape(roof)
    
    # Door
    door = Rectangle(
        x=450, y=450, width=100, height=150,
        layer_id="house",
        style=Style(fill_color=door_color, stroke_color="#000000", stroke_width=2)
    )
    doc.add_shape(door)
    
    # Door knob
    door_knob = Rectangle(
        x=530, y=520, width=10, height=10,
        corner_radius=5,
        layer_id="house",
        style=Style(fill_color="#ffd700")  # Gold
    )
    doc.add_shape(door_knob)
    
    # Windows
    # Left window
    window_left = Rectangle(
        x=340, y=350, width=80, height=80,
        layer_id="house",
        style=Style(fill_color=window_color, stroke_color="#000000", stroke_width=2)
    )
    doc.add_shape(window_left)
    
    # Window frame (cross)
    window_left_h = Rectangle(
        x=340, y=388, width=80, height=4,
        layer_id="house",
        style=Style(fill_color="#000000")
    )
    doc.add_shape(window_left_h)
    
    window_left_v = Rectangle(
        x=378, y=350, width=4, height=80,
        layer_id="house",
        style=Style(fill_color="#000000")
    )
    doc.add_shape(window_left_v)
    
    # Right window
    window_right = Rectangle(
        x=580, y=350, width=80, height=80,
        layer_id="house",
        style=Style(fill_color=window_color, stroke_color="#000000", stroke_width=2)
    )
    doc.add_shape(window_right)
    
    # Window frame (cross)
    window_right_h = Rectangle(
        x=580, y=388, width=80, height=4,
        layer_id="house",
        style=Style(fill_color="#000000")
    )
    doc.add_shape(window_right_h)
    
    window_right_v = Rectangle(
        x=618, y=350, width=4, height=80,
        layer_id="house",
        style=Style(fill_color="#000000")
    )
    doc.add_shape(window_right_v)
    
    # Bricks pattern on lower part of house
    brick_width = 40
    brick_height = 20
    brick_gap = 2
    
    # Draw bricks in a staggered pattern
    for row in range(5):  # 5 rows of bricks
        y_pos = 580 - (row * (brick_height + brick_gap))
        offset = (brick_width // 2) if row % 2 == 1 else 0
        
        for col in range(11):  # Enough bricks to cover the width
            x_pos = 300 + offset + (col * (brick_width + brick_gap))
            
            # Skip bricks that would overlap with the door
            if x_pos + brick_width > 450 and x_pos < 550 and y_pos > 450:
                continue
                
            # Only draw bricks within house bounds
            if x_pos < 700 and x_pos + brick_width > 300:
                # Clip brick width if it extends beyond house
                actual_width = min(brick_width, 700 - x_pos) if x_pos + brick_width > 700 else brick_width
                if x_pos < 300:
                    actual_width = brick_width - (300 - x_pos)
                    x_pos = 300
                
                brick = Rectangle(
                    x=x_pos, y=y_pos, width=actual_width, height=brick_height,
                    layer_id="house",
                    style=Style(fill_color=brick_color, stroke_color="#8b0000", stroke_width=1)
                )
                doc.add_shape(brick)
    
    # Tree 1 (left side)
    # Trunk
    tree1_trunk = Rectangle(
        x=100, y=450, width=40, height=150,
        layer_id="nature",
        style=Style(fill_color=tree_trunk_color, stroke_color="#000000", stroke_width=1)
    )
    doc.add_shape(tree1_trunk)
    
    # Foliage (using overlapping rectangles for a fuller look)
    tree1_foliage1 = Rectangle(
        x=60, y=300, width=120, height=180,
        corner_radius=60,
        layer_id="nature",
        style=Style(fill_color=tree_foliage_color, stroke_color="#006400", stroke_width=2)
    )
    doc.add_shape(tree1_foliage1)
    
    tree1_foliage2 = Rectangle(
        x=80, y=250, width=80, height=100,
        corner_radius=40,
        layer_id="nature",
        style=Style(fill_color=tree_foliage_color)
    )
    doc.add_shape(tree1_foliage2)
    
    # Tree 2 (right side)
    # Trunk
    tree2_trunk = Rectangle(
        x=820, y=480, width=30, height=120,
        layer_id="nature",
        style=Style(fill_color=tree_trunk_color, stroke_color="#000000", stroke_width=1)
    )
    doc.add_shape(tree2_trunk)
    
    # Foliage
    tree2_foliage1 = Rectangle(
        x=790, y=350, width=90, height=150,
        corner_radius=45,
        layer_id="nature",
        style=Style(fill_color=tree_foliage_color, stroke_color="#006400", stroke_width=2)
    )
    doc.add_shape(tree2_foliage1)
    
    tree2_foliage2 = Rectangle(
        x=800, y=320, width=70, height=80,
        corner_radius=35,
        layer_id="nature",
        style=Style(fill_color=tree_foliage_color)
    )
    doc.add_shape(tree2_foliage2)
    
    # Small bushes
    bush1 = Rectangle(
        x=200, y=560, width=60, height=40,
        corner_radius=20,
        layer_id="nature",
        style=Style(fill_color="#32cd32", stroke_color="#228b22", stroke_width=1)
    )
    doc.add_shape(bush1)
    
    bush2 = Rectangle(
        x=740, y=570, width=50, height=30,
        corner_radius=15,
        layer_id="nature",
        style=Style(fill_color="#32cd32", stroke_color="#228b22", stroke_width=1)
    )
    doc.add_shape(bush2)
    
    # Chimney
    chimney = Rectangle(
        x=600, y=200, width=60, height=100,
        layer_id="house",
        style=Style(fill_color=brick_color, stroke_color="#000000", stroke_width=2)
    )
    doc.add_shape(chimney)
    
    # Sun
    sun = Rectangle(
        x=850, y=50, width=80, height=80,
        corner_radius=40,
        layer_id="sky",
        style=Style(fill_color="#ffff00", stroke_color="#ffa500", stroke_width=3)
    )
    doc.add_shape(sun)
    
    return doc


def main():
    """Main function to create and export the house drawing."""
    print("Creating house drawing...")
    
    # Create the drawing
    doc = create_house_drawing()
    
    # Export to SVG
    exporter = SVGExporter()
    svg_content = exporter.export_document(doc)
    
    # Save to file
    output_file = "house.svg"
    with open(output_file, 'w') as f:
        f.write(svg_content)
    
    print(f"House drawing saved to {output_file}")
    print(f"Total shapes: {len(doc.shapes)}")


if __name__ == "__main__":
    main()