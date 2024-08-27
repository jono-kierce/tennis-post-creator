import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from helpers import Colours, Text_Helper

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
    The csv is expected to take the folllowing format, where the first line has 2 entries:
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


def draw_data_from_scratch(stat_title, img_path, players):
    # Create a blank image with white background
    image_width = 1200
    image_height = 1200
    background_color = (255, 255, 255)
    template = Image.new('RGB', (image_width, image_height), background_color)
    draw = ImageDraw.Draw(template)
    text_helper = Text_Helper(draw)
    
    half_width = image_width // 2
    green_color = colours.tnt_colours['Green']
    draw.rectangle([0, 0, half_width, image_height], fill=green_color)
    blue_box_height = image_height // 8

    draw.rectangle([0, 0, half_width, blue_box_height], fill=colours.tnt_colours['Blue'])
    # Set fonts
    font_path = "util/fonts/Roboto_Condensed/RobotoCondensed-VariableFont_wght.ttf"
    anton_path = "util/fonts/Anton/Anton-Regular.ttf"
    oswald_path = "util/fonts/Oswald/Oswald-VariableFont_wght.ttf"
    #Draw caption in blue box
    blue_box_caption = "S3 Regular Season Leaders"
    max_blue_box_text_size = text_helper.get_max_text_size(ImageFont, blue_box_caption, (half_width - 50, blue_box_height), oswald_path)
    text_helper.draw_centered_text(blue_box_caption, ImageFont.truetype(oswald_path, size=max_blue_box_text_size), (half_width/2, blue_box_height/2), fill=colours.tnt_colours['White'])

    title_font = ImageFont.truetype(font_path, size=110)
    text_font = ImageFont.truetype(font_path, size=45)
    oswald_font = ImageFont.truetype(oswald_path, size=58)

    # Draw the statistic title at the top
    max_title_size = text_helper.get_max_text_size(ImageFont, stat_title, (half_width - 50, blue_box_height), anton_path)
    text_helper.draw_centered_text(stat_title, ImageFont.truetype(anton_path, size=max_title_size),(half_width / 2, blue_box_height / 2 + blue_box_height), fill=colours.tnt_colours['Black'])
    # Load the image to be used for the players
    player_image = Image.open(img_path)
    player_image = player_image.resize((200, 200))  # Resize to fit the layout


    # Draw each player's information

    table_heights = (blue_box_height * 2, image_height - blue_box_height/2)
    table_padding = 75
    table_widths = (table_padding, half_width - table_padding) 
    table_row_height = (table_heights[1] - table_heights[0]) // len(players)
    max_stat_value = max(int(player.number_of_stats) for player in players)
    if 0 <= max_stat_value <= 9:
        stat_box_width = 55
    elif 10 <= max_stat_value <= 99:
        stat_box_width = 105  
    else:
        print(f"There's a maximum {stat_title} of {max_stat_value}, which may pose a formatting issue.")
        stat_box_width = 155  

    for idx, player in enumerate(players):
        #Get team colours
        text_colour = colours.team_colour_codes_dark[player.team_colour]
        bg_colour = colours.adjust_color_brightness(colours.team_colour_codes_light[player.team_colour],0.9)
        bg_colour_dark = colours.adjust_color_brightness(bg_colour, 0.8)
        #Draw circle on left edge
        draw.ellipse((table_padding, table_heights[0] + idx*table_row_height, table_padding + table_row_height, (idx+1)*table_row_height+table_heights[0]), fill = bg_colour)
        #Add rectangle from midpoint of circle to end of table
        draw.rectangle((table_widths[0] + table_padding, table_heights[0] + idx*table_row_height,table_widths[1],(idx+1)*table_row_height+table_heights[0]), fill=bg_colour)
        #Draw darkened column on right side of table - for stats to go in
        draw.rectangle((table_widths[1]-stat_box_width, table_heights[0] + idx*table_row_height,table_widths[1],(idx+1)*table_row_height+table_heights[0]), fill=bg_colour_dark)
        
        #Draw stat count in darkened rectangle
        text_helper.draw_centered_text(str(player.number_of_stats), title_font, (half_width - table_padding - stat_box_width // 2,table_heights[0] + (idx+0.5)*table_row_height), fill='White')


        #Write number (rank) in middle of circle
        rank_middle = (table_padding + table_row_height * 0.5 - 5, table_heights[0] + (idx + 0.5) * table_row_height- 2)
        # Use the draw_centered_text function to draw the rank number centered
        
        text_helper.draw_centered_text(str(player.category_rank), title_font, rank_middle, fill=text_colour)
        
        #Write player name
        #Player name can basically fit within the bounds of xcoords: padding*2 -> table_widths[0] - stat_box_width
        first_name, last_name = text_helper.split_name(str(player.player_name))
        player_name_bounds = (table_padding*2,table_heights[0] + idx*table_row_height ,table_widths[1] - stat_box_width-10, (idx+1)*table_row_height+table_heights[0])
        first_name_last_diff = 52
        name_offset = 36
        print(player_name_bounds)
        text_helper.draw_text(first_name, oswald_font, (player_name_bounds[0] + table_padding * 0.4,player_name_bounds[1] + (player_name_bounds[3]-player_name_bounds[1])//2 - first_name_last_diff/2 - name_offset), fill=colours.tnt_colours['White'])
        text_helper.draw_text(last_name, oswald_font, (player_name_bounds[0] + table_padding * 0.4,player_name_bounds[1] + (player_name_bounds[3]-player_name_bounds[1])//2 + first_name_last_diff/2 - name_offset), fill=colours.tnt_colours['White'])

    # Save the final image

    #Add player image
    player_image = Image.open(img_path)
    player_image = player_image.resize((600, 1200))  # Resize to fit the layout

    template.paste(player_image, (half_width, 0))
    template.save("output_image.png")

if __name__ == "__main__":
    colours = Colours()
    stat_title, img_path, players = read_csv("csv.csv")
    draw_data_from_scratch(stat_title.upper(), img_path, players)


    
