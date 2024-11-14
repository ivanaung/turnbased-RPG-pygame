import pygame_menu
import pygame
import random

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)

# Button properties
button_x = 150
button_y = 120
button_width = 100
button_height = 50
button_color = BLUE
hover_color = DARK_BLUE
text_color = WHITE



def menutheme():
    main_menu_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
    main_menu_theme.title_background_color = (43,24,70)
    main_menu_theme.set_background_color_opacity(0.9)  # 50% opacity
    main_menu_theme.title_font = pygame_menu.font.FONT_PT_SERIF
    main_menu_theme.title_font_color = (251,251,213)
    main_menu_theme.widget_font = pygame_menu.font.FONT_PT_SERIF
    main_menu_theme.widget_background_color = (251,251,213)
    main_menu_theme.selection_color = (238,90,49)
    main_menu_theme.widget_selection_effect = pygame_menu.widgets.HighlightSelection(border_width=5)
    main_menu_theme.widget_padding =(5,30)
    main_menu_theme.widget_margin =(0,10)

    return main_menu_theme


  
def generate_enemy_name(count):
    ainame = []
    if count > 0:
        number = random.sample(range(10,99),count)
        for i in range(count):
            ainame.append("AI" + str(number[i]))
    
    return ainame 