
class Colours():
    def __init__(self):
        self.tnt_colours = {
        'Green': (0x22, 0xc1, 0x77),
        'Blue': (0x1e, 0x3a, 0x8a),
        'Orange': (0xe9, 0x66, 0x14),
        'Black': (0x2b, 0x2b, 0x2b),
        'White': (0xf7,0xf7,0xf7)
        }
        self.team_colour_codes_dark = {
        'Pink': (0xcb, 0xcc, 0xe6),
        'Navy': (0, 0x4a, 0xad),
        'Light Blue': (0x38, 0xb6, 0xff),
        'Green': (0x0a, 0xc3, 0x0a),
        'White': (0xf7, 0xf7, 0xf7),
        'Black': (0x2b, 0x2b, 0x2b),
        'Red': (0xff, 0x31, 0x31),
        'Orange': (0xce, 0x4f, 0),
        'Yellow': (0xf7, 0xd1, 0x38)
        }
        self.team_colour_codes_light = {
        'Pink': (0xea, 0xa3, 0xf0),
        'Navy': (0x48, 0x84, 0xd5),
        'Light Blue': (0x85, 0xbf, 0xe0),
        'Green': (0x82, 0xf9, 0x82),
        'White': (0xa6, 0xa6, 0xa6),
        'Black': (0x73, 0x73, 0x73),
        'Red': (0xee, 0x74, 0x74),
        'Orange': (0xff, 0xa1, 0x67),
        'Yellow': (0xf5, 0xe8, 0x79)
        }
    def adjust_color_brightness(self, color, factor):
        """
        Adjust the brightness of an RGB color.
        
        Parameters:
            color (tuple): A tuple (R, G, B) representing the original color.
            factor (float): A factor to adjust the brightness. 
                            - Values < 1 darken the color.
                            - Values > 1 lighten the color.
        
        Returns:
            tuple: A new (R, G, B) tuple representing the adjusted color.
        """
        r, g, b = color
        
        # Ensure RGB values are within the valid range after adjustment
        r = max(0, min(255, int(r * factor)))
        g = max(0, min(255, int(g * factor)))
        b = max(0, min(255, int(b * factor)))
        
        return (r, g, b)
    
class Text_Helper():
    def __init__(self, draw):
        self.draw = draw
    def draw_centered_text(self, text, font, position, fill=(0, 0, 0)):
        """
        Draw text centered at the specified position.
        
        Parameters:
            text: The string of text to be drawn.
            font: The ImageFont object representing the font.
            position: A tuple (text_middle_x, text_middle_y) where the text should be centered.
            fill: The color to fill the text with (default is black).
        """
        text_middle_x, text_middle_y = position
        # Calculate the bounding box of the text
        _, _, w, h = self.draw.textbbox((0, 0), text, font=font)
        
        # Calculate the top-left corner of the text to center it
        text_x = text_middle_x - (w / 2) 
        text_y = text_middle_y - (h / 2) - 10#idk why i need 10 but it looks better... play on
        
        # Draw the text at the calculated position
        self.draw.text((text_x, text_y), text, font=font, fill=fill)

    def draw_left_text(self, text, font, position, fill=(0, 0, 0)):
        """
        Draw text left-aligned at the specified position (so left aligned, but centred vertically)
        
        Parameters:
            text: The string of text to be drawn.
            font: The ImageFont object representing the font.
            position: A tuple (text_x, text_middle_y) where the text should be left aligned to.
            fill: The color to fill the text with (default is black).
        """
        text_x, text_middle_y = position
        # Calculate the bounding box of the text
        _, _, w, h = self.draw.textbbox((0, 0), text, font=font)
        
        # Calculate the top-left corner of the text to center it
        text_y = text_middle_y - (h / 2) - 10#idk why i need 10 but it looks better... play on
        
        # Draw the text at the calculated position
        self.draw.text((text_x, text_y), text, font=font, fill=fill)

    def split_name(self, name):
        space_count = name.count(" ")
        assert space_count == 1, f"Incorrect name input. Expecting 1 space, got {space_count}"

        first_name, last_name = name.split(" ")
        return first_name, last_name