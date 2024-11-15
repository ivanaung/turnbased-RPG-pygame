
import pygame
import pygame_menu
from custom_theme import * 
from gamelog import GameLog
from player import *
from enemy import *
from button import *


pygame.mixer.init()
pygame.init()

screen_width = 900
screen_height = 600

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

game_level =1

# Colors
WHITE = (255, 255, 255)
GRAY = (20, 20, 20)
BLUE = (20, 20, 200)
RED = (200, 20, 20)
DARK_BLUE = (0, 143, 250)
GREEN = (0,128,128)

intro_music = pygame.mixer.Sound("./sound/intro.mp3")
gameplay_music = pygame.mixer.Sound("./sound/game_play.mp3")
mouse_click = pygame.mixer.Sound("./sound/mouseclick.mp3")
helth_update = pygame.mixer.Sound("./sound/update.mp3")
die = pygame.mixer.Sound("./sound/die.wav")
win = pygame.mixer.Sound("./sound/win.wav")
lose = pygame.mixer.Sound("./sound/lose.wav")
promoted = pygame.mixer.Sound("./sound/promoted.mp3")

#set the game area
surface = pygame.display.set_mode((screen_width, screen_height))
log_rect = pygame.Rect(0,0,int(screen_width * 0.2),screen_height)
game_rect = pygame.Rect(int(screen_width * 0.2), 0, screen_width, screen_height)
game_log = GameLog(surface,int(screen_width * 0.2),screen_height-20,20)

font = pygame.font.SysFont("Times New Roman",40)
font.set_bold(True)
font.set_italic(True)
label = font.render("Level - "+str(game_level), True, (255, 0, 0))  # White color
#label_rect = label.get_rect(center=(int(screen_width * 0.5), 30))  # Centering the label on the screen

turnfont = pygame.font.SysFont("Times New Roman",25)
turnfont.set_bold(True)


background_image = pygame.image.load('./menu_bg.png')
background_image = pygame.transform.scale(background_image,(screen_width,screen_height))

background_fight1 = pygame.image.load('./level/level1bg.png')
background_fight1 = pygame.transform.scale(background_fight1,(int(screen_width * 0.8),screen_height))

def start_attack(attacker,target,game_log):
     #game_log.add_log("Attacker Attack Point :" + str(attacker.atkpoint))
     #game_log.add_log("Target Defence Point :" + str(attacker.defpoint))
     if(target.die==False):
        Damage= (attacker.atkpoint - target.defpoint) + (random.randint(5,10))  #Damage point calculate          
       
        if(Damage > 10):
            target.experience += int(target.experience * 1.20)
        elif(Damage <= 0):            
            target.experience += int(target.experience * 1.50)

        
        if(Damage>0):
             target.health -= Damage    
             play_short_sound(helth_update)                                       #Assigned the target HP
             if(target.health<= 0):
                  play_short_sound(die)        
        
        attacker.experience += Damage                                         #Increase attacker EXP
        game_log.add_log("Tgt:" + target.name +" |Damage :" + str(Damage) + "|Exp:"+ str(target.experience))
        game_log.add_log("Atk:" + attacker.name +" |Exp:"+ str(attacker.experience))
     
        if(attacker.experience >100):
            attacker.rank +=1            
            attacker.experience = 0
            play_short_sound(promoted)
    
     
def start_game():
    play_sound(gameplay_music)
    player1 = Player(name="Hero1", hero_type=random.randint(1,2), position=(int(screen_width * 0.2)+100,screen_height-180),rank=0)
    player2 = Player(name="Hero2", hero_type=random.randint(1,2), position=(int(screen_width * 0.2)+50,screen_height-350),rank=0)
    player3 = Player(name="Hero3", hero_type=random.randint(1,2), position=(int(screen_width * 0.2)+100,screen_height-520),rank=0)

    ainameArray = []
    ainameArray = generate_enemy_name(3)
    enemy1 = Enemy(name=ainameArray[0], enemy_type=random.randint(1,2), position=(int(screen_width)-200,screen_height-180),rank=0)
    enemy2 = Enemy(name=ainameArray[1], enemy_type=random.randint(1,2), position=(int(screen_width)-150,screen_height-350),rank=0)
    enemy3 = Enemy(name=ainameArray[2], enemy_type=random.randint(1,2), position=(int(screen_width)-200,screen_height-520),rank=0)

    enemys = [enemy1,enemy2,enemy3]   
    players = [player1,player2,player3] 

    label_surface = turnfont.render("Player Turn", True, BLACK)
    aiturn = False
    running = True
    clock = pygame.time.Clock()    
    restart_button = Button(10,int(screen_height-30), 60, 20,"Restart")
    exit_button = Button(80,int(screen_height-30), 60, 20,"Exit")
    while running:
        for event in pygame.event.get():          
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    game_log.add_log("Back to main menu")
                    main()                  
            elif exit_button.is_clicked(event):
                    game_log.add_log("Back to main menu")
                    main()
            
            elif restart_button.is_clicked(event):
                    game_log.add_log("Restart the game")
                    running = False
                    start_game()
                    
            elif player1.ackbtn.is_clicked(event):  
                    play_short_sound(mouse_click)
                    target =  random.choice(enemys)
                    game_log.add_log("Player " + player1.name + " attatck " + target.name)                     
                    start_attack(player1,target,game_log)      
                    label_surface = turnfont.render("AI Turn", True, RED)                      
                    aiturn=True                 
                    hero =  random.choice(players)
                    game_log.add_log("AI " + target.name + " attatck " + hero.name)    
                    start_attack(target,hero,game_log)
                    
                    if(target.die):
                         enemys.remove(target)
                    if(player1.die):
                         players.remove(player1)
                  
            
            elif player2.ackbtn.is_clicked(event):
                    play_short_sound(mouse_click)
                    target =  random.choice(enemys)
                    game_log.add_log("Player " + player2.name + " attatck " + target.name)                     
                    start_attack(player1,target,game_log)                                   
                    target.draw_health_bar(surface)                    
                    label_surface = turnfont.render("AI Turn", True, RED)   
                    aiturn=True    
                    hero =  random.choice(players)
                    game_log.add_log("AI " + target.name + " attatck " + hero.name)    
                    start_attack(target,hero,game_log)

                    if(target.die):
                         enemys.remove(target)
                    if(player2.die):
                         players.remove(player2)

            elif player3.ackbtn.is_clicked(event):
                    play_short_sound(mouse_click)
                    target =  random.choice(enemys)
                    game_log.add_log("Player " + player3.name + " attatck " + target.name)                     
                    start_attack(player1,target,game_log)                                   
                    target.draw_health_bar(surface)                   
                    label_surface = turnfont.render("AI Turn", True, RED)
                    aiturn=True      
                    hero =  random.choice(players)
                    game_log.add_log("AI " + target.name + " attatck " + hero.name)    
                    start_attack(target,hero,game_log)

                    if(target.die):
                         enemys.remove(target)
                    if(player3.die):
                         players.remove(player3)

            elif event.type == pygame.QUIT:
                running = False
            
        # Game logic (placeholder for main game content)
        surface.fill(GRAY)  # Blue background as an example
        game_log.draw()  # Draw the game log
        #game_log.add_log("new game ")
        surface.blit(background_fight1,(int(screen_width * 0.2),0))
        player1.health
        player2.health
        player3.health

        enemy1.health
        enemy2.health
        enemy3.health
        
        player1.draw(surface)
        player2.draw(surface)
        player3.draw(surface)

        enemy1.draw(surface)
        enemy2.draw(surface)
        enemy3.draw(surface)
        surface.blit(label, (int(screen_width * 0.5), 20))
        restart_button.draw(surface)
        exit_button.draw(surface)
     
        surface.blit(label_surface, (int(screen_width * 0.5)+20, 100))  # Adjust position as needed  
        if(aiturn):
            pygame.time.delay(500) 
            label_surface = turnfont.render("Player Turn", True, BLACK)
           
        if(enemy1.die and enemy2.die and  enemy3.die):
             game_log.add_log("Enemy all RIP ")            
             surface.blit(font.render("You WIN", True, GREEN),(int(screen_width * 0.5)+20, int(screen_height * 0.5))) 
             play_short_sound(win)
             pygame.time.delay(2000) 
             main()

        elif(player1.die and player2.die and player3.die):
              game_log.add_log("Hero all RIP ")           
              surface.blit(font.render("You Lose", True, DARK_RED),(int(screen_width * 0.5)+20, int(screen_height * 0.5)))
              play_short_sound(lose)
              pygame.time.delay(2000) 
              main()
              
             
        #draw_button(surface,10,int(screen_height-30), 60, 20, RED, "Exit")
        pygame.display.flip()

        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.quit()

def play_sound(sound):
    pygame.mixer.stop()  # Stop any currently playing sound
    sound.play(loops=-1)

def play_short_sound(sound):
     sound.play()

#create menu
menu = pygame_menu.Menu('Welcome', 400, 300,theme= menutheme())
#menu.set_absolute_position(int(background_image.get_width()//2), 140)

#create menu action
menu.add.button('Play', start_game)
menu.add.button('Quit', pygame_menu.events.EXIT)



#main function
def main():   
    play_sound(intro_music)
    while True:   
        #surface.fill(WHITE)      
        pygame.draw.rect(surface, GRAY, log_rect)       
        #game_log.add_log("Player scored 10 points.")
        #game_log.add_log("Enemy defeated!")
        #pygame.draw.rect(surface, (0, 100, 255), game_rect) 
        surface.blit(background_image, (0, 0))
        #surface.blit(background_image,(int(screen_width * 0.2),0))

        events = pygame.event.get()
        for event in events:            
            if event.type == pygame.QUIT:
                pygame.time.delay(500) 
                exit()
            game_log.handle_events(event)

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)
        pygame.display.flip()




if __name__ == '__main__':
    main()

