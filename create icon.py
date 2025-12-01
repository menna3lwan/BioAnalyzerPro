"""
DNA Helix Icon Generator
Creates a colorful DNA helix icon for BioAnalyzer Pro
"""

from PIL import Image, ImageDraw
import math

def create_dna_helix_icon(size=256):
    """
    Create DNA helix icon with gradient colors
    
    Args:
        size: Icon size (default 256x256)
    """
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Parameters
    center_x = size // 2
    helix_height = int(size * 0.8)
    helix_width = int(size * 0.6)
    start_y = (size - helix_height) // 2
    num_turns = 3
    points_per_turn = 20
    
    # Colors for gradient (blue to cyan to green to yellow to red)
    colors = [
        (52, 152, 219),   # Blue
        (46, 204, 113),   # Green
        (241, 196, 15),   # Yellow
        (231, 76, 60),    # Red
    ]
    
    # Calculate points for two helices
    left_helix = []
    right_helix = []
    total_points = num_turns * points_per_turn
    
    for i in range(total_points):
        t = (i / total_points) * num_turns * 2 * math.pi
        y = start_y + (i / total_points) * helix_height
        
        # Left helix (cos wave)
        x_left = center_x + math.cos(t) * (helix_width / 2)
        left_helix.append((x_left, y))
        
        # Right helix (cos wave shifted by pi)
        x_right = center_x + math.cos(t + math.pi) * (helix_width / 2)
        right_helix.append((x_right, y))
    
    # Draw connecting lines between helices
    for i in range(0, len(left_helix), 4):
        # Calculate color based on position
        color_index = int((i / len(left_helix)) * (len(colors) - 1))
        color1 = colors[color_index]
        color2 = colors[min(color_index + 1, len(colors) - 1)]
        
        # Interpolate color
        t = (i / len(left_helix)) * (len(colors) - 1) - color_index
        r = int(color1[0] * (1 - t) + color2[0] * t)
        g = int(color1[1] * (1 - t) + color2[1] * t)
        b = int(color1[2] * (1 - t) + color2[2] * t)
        color = (r, g, b, 255)
        
        # Draw connection line
        line_width = max(2, size // 64)
        draw.line([left_helix[i], right_helix[i]], fill=color, width=line_width)
    
    # Draw helix strands
    strand_width = max(4, size // 32)
    
    for i in range(len(left_helix) - 1):
        # Calculate color gradient
        color_index = int((i / len(left_helix)) * (len(colors) - 1))
        color1 = colors[color_index]
        color2 = colors[min(color_index + 1, len(colors) - 1)]
        
        t = (i / len(left_helix)) * (len(colors) - 1) - color_index
        r = int(color1[0] * (1 - t) + color2[0] * t)
        g = int(color1[1] * (1 - t) + color2[1] * t)
        b = int(color1[2] * (1 - t) + color2[2] * t)
        color = (r, g, b, 255)
        
        # Draw left helix
        draw.line([left_helix[i], left_helix[i + 1]], fill=color, width=strand_width)
        
        # Draw right helix
        draw.line([right_helix[i], right_helix[i + 1]], fill=color, width=strand_width)
        
        # Draw circles at connection points for better look
        if i % 4 == 0:
            circle_size = max(3, size // 48)
            draw.ellipse([
                left_helix[i][0] - circle_size,
                left_helix[i][1] - circle_size,
                left_helix[i][0] + circle_size,
                left_helix[i][1] + circle_size
            ], fill=color)
            
            draw.ellipse([
                right_helix[i][0] - circle_size,
                right_helix[i][1] - circle_size,
                right_helix[i][0] + circle_size,
                right_helix[i][1] + circle_size
            ], fill=color)
    
    return img


def create_simple_dna_icon(size=64):
    """
    Create simplified DNA icon for smaller sizes
    
    Args:
        size: Icon size (default 64x64)
    """
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center_x = size // 2
    helix_height = int(size * 0.8)
    helix_width = int(size * 0.5)
    start_y = (size - helix_height) // 2
    num_segments = 4
    
    colors = [
        (52, 152, 219),   # Blue
        (46, 204, 113),   # Green
        (231, 76, 60),    # Red
    ]
    
    segment_height = helix_height // num_segments
    
    for i in range(num_segments):
        y_top = start_y + i * segment_height
        y_bottom = y_top + segment_height
        
        # Alternate left and right
        if i % 2 == 0:
            x_left_top = center_x - helix_width // 2
            x_right_top = center_x + helix_width // 2
            x_left_bottom = center_x + helix_width // 2
            x_right_bottom = center_x - helix_width // 2
        else:
            x_left_top = center_x + helix_width // 2
            x_right_top = center_x - helix_width // 2
            x_left_bottom = center_x - helix_width // 2
            x_right_bottom = center_x + helix_width // 2
        
        # Color based on position
        color_idx = int((i / num_segments) * (len(colors) - 1))
        color = colors[color_idx] + (255,)
        
        # Draw strands
        line_width = max(2, size // 16)
        draw.line([(x_left_top, y_top), (x_left_bottom, y_bottom)], fill=color, width=line_width)
        draw.line([(x_right_top, y_top), (x_right_bottom, y_bottom)], fill=color, width=line_width)
        
        # Draw connection
        y_mid = (y_top + y_bottom) // 2
        x_left_mid = (x_left_top + x_left_bottom) // 2
        x_right_mid = (x_right_top + x_right_bottom) // 2
        draw.line([(x_left_mid, y_mid), (x_right_mid, y_mid)], fill=color, width=line_width // 2)
    
    return img


def main():
    """Generate icon in multiple sizes"""
    print("🧬 Generating BioAnalyzer Pro Icons...")
    
    # Standard icon sizes
    sizes = [16, 32, 48, 64, 128, 256, 512]
    
    for size in sizes:
        print(f"Creating {size}x{size} icon...")
        
        if size <= 64:
            # Use simplified version for small sizes
            icon = create_simple_dna_icon(size)
        else:
            # Use detailed version for larger sizes
            icon = create_dna_helix_icon(size)
        
        # Save as PNG
        icon.save(f'/mnt/user-data/outputs/icon_{size}x{size}.png')
        print(f"✓ Saved icon_{size}x{size}.png")
    
    # Create main icon.ico with multiple sizes
    print("\nCreating icon.ico with multiple resolutions...")
    icons = []
    for size in [16, 32, 48, 256]:
        if size <= 64:
            icons.append(create_simple_dna_icon(size))
        else:
            icons.append(create_dna_helix_icon(size))
    
    icons[0].save('/mnt/user-data/outputs/icon.ico', 
                  format='ICO', 
                  sizes=[(16, 16), (32, 32), (48, 48), (256, 256)],
                  append_images=icons[1:])
    print("✓ Saved icon.ico")
    
    # Create logo for header (larger, horizontal)
    print("\nCreating header logo...")
    logo = create_dna_helix_icon(128)
    logo.save('/mnt/user-data/outputs/logo.png')
    print("✓ Saved logo.png")
    
    print("\n✅ All icons generated successfully!")
    print("\nGenerated files:")
    print("  - icon.ico (multi-resolution)")
    print("  - icon_16x16.png to icon_512x512.png")
    print("  - logo.png (for app header)")


if __name__ == "__main__":
    main()