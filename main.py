import pygame 
import sys
import os
from classes import Game, Card
import time
import math
# Initialize pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
BACKGROUND_COLOR =  (0 , 0, 0 )  # Color for the background (green)
FPS = 60  # Frames per second for the game
CARD_WIDTH = 85  # Width of a card
CARD_HEIGHT = 125  # Height of a card

# Font for rendering text
font = pygame.font.SysFont("Arial", 30)

# Set up the display screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Solitaire')

# Function to load images
def load_image(file_path):
    try:
        image = pygame.image.load(file_path)  # Load the image from the specified path
        return image
    except pygame.error as e:
        print(f"Error loading image '{file_path}': {e}")
        return None

# Load card back image and resize it
card_back_image = load_image("C:/Users/3 Stars Laptop/Desktop/Game/cards/zback.png")
if card_back_image:
    card_back_image = pygame.transform.scale(card_back_image, (CARD_WIDTH , CARD_HEIGHT ))

# Load mini logo image
mini_image = pygame.image.load('C:/Users/3 Stars Laptop/Desktop/Game/images/logo-black.png')
mini_image = pygame.transform.scale(mini_image, (50, 50))  # Resize the mini image

# Initialize the game instance
game = Game()

# Function to draw a card on the screen
def draw_card(card, x, y):
    if card.face_up:
        screen.blit(card.card_image, (x, y))  # Draw the face-up card
    else:
        screen.blit(card_back_image, (x , y))  # Draw the face-down card

# Function to draw all tableau piles (the piles of cards in the game)
def draw_tableau():
    # Set x positions for the tableau piles
    pile_x_positions = [100 + i * 125 for i in range(7)]
    # Loop through each pile and draw its cards
    for i, pile in game.tableau.piles.items():
        cards = pile.display()
        pile_x = pile_x_positions[i]
        pile_y = 250
        # If the pile is empty, draw an overlay and mini image
        if pile.is_empty():
            overlay = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 125))  # Semi-transparent overlay
            screen.blit(overlay, (pile_x, pile_y))  # Draw overlay
            mini_image_x = pile_x + (CARD_WIDTH - mini_image.get_width()) // 2
            mini_image_y = pile_y + (CARD_HEIGHT - mini_image.get_height()) // 2
            screen.blit(mini_image, (mini_image_x, mini_image_y))  # Draw mini logo image
        else:
            # Draw each card in the pile with a slight offset
            for j, card in enumerate(cards):
                y_position = pile_y + j * 25
                draw_card(card, pile_x, y_position)

# Function to draw the stockpile and waste pile (cards that are face-down or moved to waste)
def draw_stockpile():
    stockpile_cards = game.stockpile.display()
    waste_pile_cards = game.waste_pile.display()
    empty_slot = load_image("C:/Users/3 Stars Laptop/Desktop/Game/cards/empty_slot.png")
    empty_slot = pygame.transform.scale(empty_slot, (CARD_WIDTH, CARD_HEIGHT))

    # Draw stockpile and waste pile cards
    if stockpile_cards:
        screen.blit(card_back_image, (50, 50))  # If stockpile has cards, show the back of the card
    else:
        screen.blit(empty_slot, (50, 50))  # If no cards, show an empty slot image
    if waste_pile_cards:
        top_waste_card = waste_pile_cards[-1]
        draw_card(top_waste_card, 150, 50)  # Draw the top card from the waste pile

# Function to draw hints for valid moves
def draw_hint(valid_moves):
    for move in valid_moves:
        # Highlight tableau-to-foundation moves with yellow rectangle
        if move[0] == 'tableau' and move[2] == 'foundation':
            tableau_x = 100 + move[1] * 125
            tableau_y = 250
            pygame.draw.rect(screen, (255, 255, 0), (tableau_x, tableau_y, CARD_WIDTH, CARD_HEIGHT), 5)
        # Highlight waste-to-tableau moves with yellow rectangle
        elif move[0] == 'waste' and move[2] == 'tableau':
            waste_x, waste_y = 150, 50
            pygame.draw.rect(screen, (255, 255, 0), (waste_x, waste_y, CARD_WIDTH, CARD_HEIGHT), 5)

# Function to draw the foundation piles (where cards are moved to build sequences)
def draw_foundation():
    # Set x positions for the foundation piles
    foundation_x_positions = [450 + i * 125 for i in range(4)]
    for i, pile in enumerate(game.foundation.piles):
        pile_x = foundation_x_positions[i]
        pile_y = 50
        # Draw overlay for empty foundation piles
        overlay = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 158))
        screen.blit(overlay, (pile_x, pile_y))
        mini_image_x = pile_x + (CARD_WIDTH - mini_image.get_width()) // 2
        mini_image_y = pile_y + (CARD_HEIGHT - mini_image.get_height()) // 2
        screen.blit(mini_image, (mini_image_x, mini_image_y))  # Draw mini logo image
        # If the pile has cards, draw the top card
        if not pile.is_empty():
            card = pile.peek()
            draw_card(card, pile_x, pile_y)
        else:
            # Draw an empty rectangle if the foundation pile is empty
            pygame.draw.rect(screen, (50, 50, 50), (pile_x, pile_y, CARD_WIDTH, CARD_HEIGHT), 2)

def starter_animation():
    # Initialize pygame
    pygame.init()

    # Screen settings
    WIDTH, HEIGHT = 700, 500  # Adjust screen size as needed
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Klondike Solitaire")

    # Colors
    BACKGROUND_COLOR = (59, 27, 77)
    TEXT_COLOR = (0, 0, 0)  # Gold color for text (to contrast with background)
    GLOW_COLOR = (255, 255, 255)  # Glow color (white)
    SHADOW_COLOR = (0, 0, 0)  # Black shadow for text

    # Load background image
    background_image = pygame.image.load("C:/Users/3 Stars Laptop/Desktop/Game/images/cards.jfif")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Resize as needed

    # Load mini logo image
    mini_image = pygame.image.load("C:/Users/3 Stars Laptop/Desktop/Game/images/icon.png")
    mini_image = pygame.transform.scale(mini_image, (150, 100))  # Resize mini image

    # Text settings
    font = pygame.font.Font(None, 72)  # You can also use a custom font file here
    full_text = "Klondike Solitaire "
    displayed_text = ""
    typewriter_speed = 150  # Delay between characters in milliseconds

    # Animation settings
    fade_alpha = 0  # Mini image fade-in effect
    fade_speed = 5  # Speed of fading in the mini image
    text_index = 0
    last_time = pygame.time.get_ticks()  # Track the time of the last character added
    animation_complete = False  # Flag to track if the animation is finished

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Display background image
        screen.blit(background_image, (0, 0))

        # Fade in mini image
        if fade_alpha < 255:
            fade_alpha += fade_speed
        mini_image.set_alpha(fade_alpha)
        screen.blit(mini_image, (WIDTH // 2 - mini_image.get_width() // 2, HEIGHT // 2 - mini_image.get_height() // 2))

        # Typewriter effect for "Klondike Solitaire" text
        if text_index < len(full_text):
            current_time = pygame.time.get_ticks()
            if current_time - last_time > typewriter_speed:  # Delay between characters
                displayed_text += full_text[text_index]
                text_index += 1
                last_time = current_time  # Update last_time to current time

        # Create glow and shadow effects for the text
        text_surface = font.render(displayed_text, True, TEXT_COLOR)
        shadow_surface = font.render(displayed_text, True, SHADOW_COLOR)  # Shadow effect
        glow_surface = font.render(displayed_text, True, GLOW_COLOR)  # Glow effect

        # Adjust text position
        text_y_position = HEIGHT // 1.5  # Move text lower
        shadow_offset = 3  # Shadow offset
        glow_offset = 2  # Glow effect offset

        # Render shadow, glow, and text
        screen.blit(shadow_surface, (WIDTH // 2 - shadow_surface.get_width() // 2 + shadow_offset, text_y_position + shadow_offset))
        screen.blit(glow_surface, (WIDTH // 2 - glow_surface.get_width() // 2 + glow_offset, text_y_position + glow_offset))
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, text_y_position))

        # Check if the animation is complete
        if fade_alpha == 255 and text_index == len(full_text):
            animation_complete = True

        # End the screen after the animation is complete
        if animation_complete:
            pygame.time.wait(1000)  # Wait for 1 second before closing the window (optional)
            running = False  # Exit the loop to close the window

        # Update the display
        pygame.display.flip()
        clock.tick(60)  # Maintain 60 FPS

                   
def game_loop():
    starter_animation()
    #initialize variables
    game.save_state()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Solitaire')
    dragging_cards = [] 
    dragging_pile_name = None
    dragging_pile_index = None
    offset_x, offset_y = 0, 0
    global font
    score = 0 
    move_count = 0
    clock = pygame.time.Clock()
    start_time = time.time()
    running = True
    message_time = None
    invalid_move_message = ""
    # Load images and sounds
    undo_image = load_image("C:/Users/3 Stars Laptop/Desktop/Game/images/undo.png")
    card_click_sound = pygame.mixer.Sound("C:/Users/3 Stars Laptop/Desktop/Game/images/stock_pile.mp3")
    card_drop_sound = pygame.mixer.Sound("C:/Users/3 Stars Laptop/Desktop/Game/images/move_card.mp3")
    win_game = pygame.mixer.Sound("C:/Users/3 Stars Laptop/Desktop/Game/images/win_game.mp3")
    point_gain = pygame.mixer.Sound("C:/Users/3 Stars Laptop/Desktop/Game/images/points_gain.mp3")
    invalid_movement = pygame.mixer.Sound("C:/Users/3 Stars Laptop/Desktop/Game/images/invalid_movement.mp3")
    icon_image = pygame.image.load("C:/Users/3 Stars Laptop/Desktop/Game/images/icon.png")
    icon_image = pygame.transform.scale(icon_image, (32, 42))
    pygame.display.set_icon(icon_image)
    # Main game loop
    background_image = pygame.image.load("C:/Users/3 Stars Laptop/Desktop/Game/images/bg.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    while running:
        # screen.fill(BACKGROUND_COLOR)
        screen.blit(background_image, (0, 0))
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_text = f"{minutes:02}:{seconds:02}"
        time_display = font.render(time_text, True, (255, 255, 255))
        screen.blit(time_display, (80, 15))
        score_text = f"Score: {score}" # Score display
        score_display = pygame.font.SysFont("Times New Roman", 30 ,italic=True ).render(score_text, True, (255, 255, 255))
        screen.blit(score_display, ( 750 , 10))
        moves_text = f"Moves: {move_count}" # Moves display
        score_display = pygame.font.SysFont("Times New Roman", 30 ,italic=True ).render(moves_text, True, (255, 255, 255))
        screen.blit(score_display, ( 600 , 10)) 
        undo_image = pygame.transform.scale(undo_image, (40, 40))
        screen.blit(undo_image, (900, 10)) 
        if message_time and time.time() - message_time >= 10:
            invalid_move_message = "" 
            
        for event in pygame.event.get(): # Event handling loop 
            if event.type == pygame.QUIT: # if cross btn is pressed
                running = False
  
            if event.type == pygame.MOUSEBUTTONDOWN: # if mouse is clicked ( user select the card)
                pos = pygame.mouse.get_pos()
                if SCREEN_WIDTH - 100 <= pos[0] <= SCREEN_WIDTH - 100 + 40 and 15 <= pos[1] <= 15 + 40:
                     if (game.undo()): # if undo btn is clicked
                        move_count += 1
                if 50 <= pos[0] <= 50 + CARD_WIDTH and 50 <= pos[1] <= 50 + CARD_HEIGHT: # if stockpile is clicked
                    game.draw_from_stockpile() # draw card from stockpile
                    card_click_sound.play()
                    move_count += 1 # increment move count
                elif 150 <= pos[0] <= 150 + CARD_WIDTH and 50 <= pos[1] <= 50 + CARD_HEIGHT: # if waste pile is clicked
                    if game.waste_pile.top_card() is not None:
                        dragging_cards = [game.waste_pile.top_card()]
                        offset_x, offset_y = pos[0] - 150, pos[1] - 50
                        dragging_pile_name, dragging_pile_index = 'waste', -1 # from waste pile
                pile_x_positions = [100 + i * 125 for i in range(7)]  # x positions for tableau piles
                for pile_idx, pile in game.tableau.piles.items():
                    if not pile.is_empty():
                        for j, card in enumerate(pile.display()): # loop through each card in the pile
                            card_x = pile_x_positions[pile_idx]
                            card_y = 250 + j * 25
                            if card.face_up:
                                if card_x <= pos[0] <= card_x + CARD_WIDTH and card_y <= pos[1] <= card_y + CARD_HEIGHT: # if card is clicked
                                    dragging_cards = []
                                    dragging_pile_name, dragging_pile_index = 'tableau', pile_idx # from tableau pile
                                    offset_x = pos[0] - card_x
                                    offset_y = pos[1] - card_y
                                    for k in range(j, len(pile.display())):
                                        if pile.display()[k].face_up: 
                                            dragging_cards.append(pile.display()[k])
                                            print("Dragging cards in if loop line 148 ", len(dragging_cards)) # print the length of dragging cards
                                        else:
                                            break 
                                    break

                foundation_x_positions = [450 + i * 125 for i in range(4)] # x positions for foundation piles
                for foundation_idx, foundation_pile in enumerate(game.foundation.piles): # loop through each foundation pile
                    if not foundation_pile.is_empty():
                        top_card = foundation_pile.peek() # get the top card of the foundation pile
                        card_x = foundation_x_positions[foundation_idx]
                        card_y = 50
                        if card_x <= pos[0] <= card_x + CARD_WIDTH and card_y <= pos[1] <= card_y + CARD_HEIGHT: # if card is clicked
                            dragging_cards = [top_card]
                            print ("Dragging cards in foundation", len(dragging_cards))
                            dragging_pile_name, dragging_pile_index = 'foundation', foundation_idx  # from foundation pile
                            offset_x = pos[0] - card_x
                            offset_y = pos[1] - card_y
                            break

            if event.type == pygame.MOUSEBUTTONUP and dragging_cards: # if mouse is released
                pos = pygame.mouse.get_pos()
                drop_pile_name, drop_pile_index = None, None
                for pile_idx, pile in game.tableau.piles.items(): # loop through each tableau pile
                    cards = pile.display()
                    pile_x = 100 + pile_idx * 125
                    if pile_x <= pos[0] <= pile_x + CARD_WIDTH:
                        if not cards:
                            print(f"Dropped on empty tableau pile {pile_idx}") # if tableau pile is empty
                            drop_pile_name, drop_pile_index = 'tableau', pile_idx 
                        else:
                            for j, card in enumerate(cards):
                                if card.face_up:
                                    card_y = 250 + j * 25
                                    if card_y <= pos[1] <= card_y + CARD_HEIGHT:
                                        print("Dragging cards in if loop line 182 ", len(dragging_cards)) # print the length of dragging cards
                                        drop_pile_name, drop_pile_index = 'tableau', pile_idx
                                        offset_x = pos[0] - pile_x
                                        offset_y = pos[1] - card_y
                                        break
                for foundation_idx in range(4): # loop through each foundation pile
                    if foundation_x_positions[foundation_idx] <= pos[0] <= foundation_x_positions[foundation_idx] + CARD_WIDTH:
                        if 50 <= pos[1] <= 50 + CARD_HEIGHT:
                            drop_pile_name, drop_pile_index = 'foundation', foundation_idx # if foundation pile is clicked
                            print(f"Dropped on foundation pile {foundation_idx}")
                            break
                print(len(dragging_cards) , "dragging cards") # print the length of dragging cards
                invalid_move_message = game.move_cards(dragging_pile_name, dragging_pile_index, drop_pile_index, drop_pile_name, len(dragging_cards)) # move the cards
                if invalid_move_message == "":
                    move_count += 1 # increment move count
                    
                    card_drop_sound.play()
                    if drop_pile_name == "tableau": # if card is dropped on tableau pile
                        score += 5
                    elif drop_pile_name == "foundation": # if card is dropped on foundation pile
                        score += 15
                else:
                    invalid_movement.play() # invalid sound play 
                    

                dragging_cards = [] 
                dragging_pile_name = None
                dragging_pile_index = None
                drop_pile_index = None
                drop_pile_name = None
                


        draw_tableau() # draw tableau
        draw_stockpile() # draw stockpile
        draw_foundation() # draw foundation
        if invalid_move_message:
            message_font = pygame.font.SysFont(None, 36) # message font
            text = message_font.render(invalid_move_message, True, (255, 255, 255))
            message_rect = pygame.Rect(10, SCREEN_HEIGHT - 50, len(invalid_move_message) * 20, 40) # message rect
            pygame.draw.rect(screen, (0 , 0, 0 , 200), message_rect, border_radius=10)
            screen.blit(text, (message_rect.x + 10, message_rect.y + 10)) 

        if dragging_cards:
            pos = pygame.mouse.get_pos() # get the mouse position
            for idx, card in enumerate(dragging_cards):
                draw_card(card, pos[0] - offset_x, pos[1] - offset_y + idx * 25) # draw the card
        if game.check_win():  # check if game is finished
            win_message = "You Win!"
            win_game.play()  # game won sound play

            message_font = pygame.font.SysFont(None, 36)  # message font
            win_text = message_font.render(f"            {win_message}", True, (255, 255, 255))  # White text
            text_width = win_text.get_width()  # get the width of the text
            text_height = win_text.get_height()  # get the height of the text

            elapsed_time = time.time() - start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            time_text = f"Time: {minutes:02}:{seconds:02}"

            moves_text = f"Moves: {move_count}"
            score_text = f"Score: {score}"
            time_display = pygame.font.SysFont("Arial", 24).render(time_text, True, (255, 255, 255))  # White text for time display
            moves_score_text = pygame.font.SysFont("Arial", 24).render(f"    {moves_text}      {score_text}", True, (255, 255, 255))  # White text for moves and score display

            total_width = max(text_width, moves_score_text.get_width()) + 100  # total width
            total_height = text_height + moves_score_text.get_height() + time_display.get_height() + 80  # total height

            x_position = (SCREEN_WIDTH - total_width) // 2  # x position
            y_position = (SCREEN_HEIGHT - total_height) // 2  # y position

            message_rect = pygame.Rect(x_position, y_position, total_width, total_height)  # message rect
            pygame.draw.rect(screen, (0, 0, 0), message_rect, border_radius=10)  # Black background

            screen.blit(win_text, (x_position + 10, y_position + 20))
            screen.blit(moves_score_text, (x_position + 20, y_position + 20 + text_height))
            screen.blit(time_display, (x_position + 20, y_position + 20 + text_height + moves_score_text.get_height() + 20))  # draw the time display

            pygame.display.flip()  # update the display

            pygame.time.wait(60000)  # wait for 60 seconds
            break  

        pygame.display.flip()
        clock.tick(FPS) # set the frames per second
        pygame.time.Clock().tick(30) # set the frames per second
    pygame.quit() # quit the game
    sys.exit() # exit the game

if __name__ == '__main__':
    game_loop() # call the game loop
