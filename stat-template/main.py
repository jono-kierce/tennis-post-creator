import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from tnt_colours import Colours

class Player:
    def __init__(self, player_name, category_rank, number_of_stats, team_colour):
        assert team_colour in ['Pink', 'Navy', 'Light Blue', 'Green', 'White', 'Black', 'Red', 'Orange', 'Yellow'], "Colours must be in the valid list"
        assert category_rank <= 5, "Only allow rank of 5 or less"
        self.player_name = player_name
        self.category_rank = category_rank
        self.number_of_stats = number_of_stats
        self.team_colour = team_colour


def read_csv(path):
    """
    This function will read a csv using the provided path, and return the relevant data 
    The csv is expected to take the format, where the first line has 2 entries:
    statistic title,path to image - e.g "Winners","img/img04.png"
    The next 5 lines contain entries for each player in this format:
    player_name,ranking,number_of_stats,team_colour

    The function returns the stat title, image path, and an array of length 5 referring to 5 players
    """
    df = pd.read_csv(path, header=None)

    #Check csv in format specified
    expected_rows = 6
    expected_cols = 4
    assert df.shape == (expected_rows, expected_cols), f"CSV not in expected format of {expected_rows}x{expected_cols}\n. Expected {expected_rows} rows, got {df.shape[0]}\nExpected {expected_cols} cols, got {df.shape[1]}"
    #The first row should contain stat title, img_path and then nothing else. Unpack that here:
    assert str(df[2][0]) == 'nan' and str(df[3][0]) == 'nan', f"Expected no values past column 2 of csv but got {df[2][0]},{df[3][0]}"
    stat_title = df[0][0]
    img_path = df[1][0]

    players = []
    for i in range(1,expected_rows):
        player_name = df[0][i]
        player_rank = int(df[1][i])
        num_stats = int(df[2][i])
        team_col = df[3][i]
        player = Player(player_name, player_rank, num_stats, team_col)
        players.append(player)

    return stat_title, img_path, players 

def get_colour_code(team_colour, colour_dict):
    """
    A function that takes a team colour as string, e.g 'Pink' and returns the colour for that team
    """
    if team_colour not in colour_dict:
        print(f"Maybe an issue: colour {team_colour} not in the dictionary. \nDefaulting to black")

    return colour_dict.get(team_colour, (0, 0, 0))  # Default to black if colour not found
   




def draw_data_from_scratch(stat_title, img_path, players):
    # Create a blank image with white background
    image_width = 1200
    image_height = 1200
    background_color = (255, 255, 255)
    template = Image.new('RGB', (image_width, image_height), background_color)
    draw = ImageDraw.Draw(template)

    left_half_width = image_width // 2
    green_color = get_colour_code('Green', colours.tnt_colour_codes)
    draw.rectangle([0, 0, left_half_width, image_height], fill=green_color)

    # Set font (you need to provide the path to your font file)
    font_path = "util/fonts/Roboto_Condensed/RobotoCondensed-VariableFont_wght.ttf"  # Adjust this path
    title_font = ImageFont.truetype(font_path, size=60)
    text_font = ImageFont.truetype(font_path, size=45)

    # Draw the statistic title at the top
    draw.text((50, 30), stat_title, fill="black", font=title_font)

    # Load the image to be used for the players
    player_image = Image.open(img_path)
    player_image = player_image.resize((200, 200))  # Resize to fit the layout

    # Define the starting position for player data
    start_x = 50
    start_y = 150
    y_offset = 150  # Spacing between players

    # Draw each player's information
    for player in players:
        # Set text color based on the player's team color
        color = get_colour_code(player.team_colour, colours.team_colour_codes_dark)

        # Draw player name, rank, and number of stats
        draw.text((start_x, start_y), f"{player.category_rank}. {player.player_name}", fill=color, font=text_font)
        draw.text((start_x + 400, start_y), f"{player.number_of_stats}", fill=color, font=text_font)
        
        # Place the player image to the right of the text
        template.paste(player_image, (800, start_y - 30))  # Adjust the position to fit the layout
        
        # Move to the next line
        start_y += y_offset

    # Save the final image
    template.save("output_image.png")

if __name__ == "__main__":
    colours = Colours()
    stat_title, img_path, players = read_csv("csv.csv")
    draw_data_from_scratch(stat_title, img_path, players)


    
