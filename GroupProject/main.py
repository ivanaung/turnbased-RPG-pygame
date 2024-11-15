
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
GREEN = (10,150,128)
LIGHT_GREEN =(100,250.150)

intro_music = pygame.mixer.Sound("GroupProject/sound/intro.mp3")
gameplay_music = pygame.mixer.Sound("GroupProject/sound/game_play.mp3")
mouse_click = pygame.mixer.Sound("GroupProject/sound/mouseclick.mp3")
helth_update = pygame.mixer.Sound("GroupProject/sound/update.mp3")
die = pygame.mixer.Sound("GroupProject/sound/die.wav")
win = pygame.mixer.Sound("GroupProject/sound/win.wav")
lose = pygame.mixer.Sound("GroupProject/sound/lose.wav")
promoted = pygame.mixer.Sound("GroupProject/sound/promoted.mp3")

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


background_image = pygame.image.load('GroupProject/menu_bg.png')
background_image = pygame.transform.scale(background_image,(screen_width,screen_height))

background_fight1 = pygame.image.load('GroupProject/level/level1bg.png')
background_fight1 = pygame.transform.scale(background_fight1,(int(screen_width * 0.8),screen_height))

def start_attack(attacker,target,game_log):
     #game_log.add_log("Attacker Attack Point :" + str(attacker.atkpoint))
     #game_log.add_log("Target Defence Point :" + str(attacker.defpoint))
     game_log.add_log(attacker.name +"  attack to "+ target.name)
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
            attacker.defpoint +=2                                                   #Increase defence point based on rank
            attacker.experience = 0
            play_short_sound(promoted)
            game_log.add_log(attacker.name + " Promoted Rank!")
    
     
def start_game():
    play_sound(gameplay_music)
    player1 = Player(name="Hero1", hero_type=random.randint(1,2), position=(int(screen_width * 0.2)+100,screen_height-520),rank=0)
    player2 = Player(name="Hero2", hero_type=random.randint(1,2), position=(int(screen_width * 0.2)+50,screen_height-350),rank=0)
    player3 = Player(name="Hero3", hero_type=random.randint(1,2), position=(int(screen_width * 0.2)+100,screen_height-180),rank=0)

    ainameArray = []
    ainameArray = generate_enemy_name(3)
    enemy1 = Enemy(1,name=ainameArray[0], enemy_type=random.randint(1,2), position=(int(screen_width)-200,screen_height-520),rank=0)
    enemy2 = Enemy(2,name=ainameArray[1], enemy_type=random.randint(1,2), position=(int(screen_width)-150,screen_height-350),rank=0)
    enemy3 = Enemy(3,name=ainameArray[2], enemy_type=random.randint(1,2), position=(int(screen_width)-200,screen_height-180),rank=0)

    enemys = [enemy1,enemy2,enemy3]   
    players = [player1,player2,player3] 

    label_surface = turnfont.render("Player Turn", True, BLACK)
    aiturn = False
    running = True
    clock = pygame.time.Clock()    
    restart_button = Button(10,int(screen_height-30), 60, 20,"Restart",True,BLUE,DARK_BLUE)
    exit_button = Button(80,int(screen_height-30), 60, 20,"Exit",True)
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

            elif player1.ackbtn1.active and player1.ackbtn1.is_clicked(event):
                    start_attack(player1,enemy1,game_log)
                    label_surface = turnfont.render(enemy1.name + " Turn", True, RED) 
                    hero =  random.choice(players)
                    start_attack(enemy1,hero,game_log)
                    aiturn=True
            
            elif player1.ackbtn2.active and player1.ackbtn2.is_clicked(event):
                    start_attack(player1,enemy2,game_log)
                    label_surface = turnfont.render(enemy2.name + " Turn", True, RED) 
                    hero =  random.choice(players)
                    start_attack(enemy2,hero,game_log)
                    aiturn=True
            
            elif player1.ackbtn3.active and player1.ackbtn3.is_clicked(event):
                    start_attack(player1,enemy3,game_log)
                    label_surface = turnfont.render(enemy3.name + " Turn", True, RED) 
                    hero =  random.choice(players)
                    start_attack(enemy3,hero,game_log)
                    aiturn=True
            
            elif player2.ackbtn1.active and player2.ackbtn1.is_clicked(event):
                    start_attack(player2,enemy1,game_log)
                    label_surface = turnfont.render(enemy1.name + " Turn", True, RED) 
                    hero =  random.choice(players)
                    start_attack(enemy1,hero,game_log)
                    aiturn=True
            
            elif player2.ackbtn2.active and player2.ackbtn2.is_clicked(event):
                    start_attack(player2,enemy2,game_log)
                    label_surface = turnfont.render(enemy2.name + " Turn", True, RED) 
                    hero =  random.choice(players)
                    start_attack(enemy2,hero,game_log)
                    aiturn=True
            
            elif player2.ackbtn3.active and player2.ackbtn3.is_clicked(event):
                    start_attack(player2,enemy3,game_log)
                    label_surface = turnfont.render(enemy3.name + " Turn", True, RED) 
                    hero =  random.choice(players)
                    start_attack(enemy3,hero,game_log)
                    aiturn=True

            elif player3.ackbtn1.active and player3.ackbtn1.is_clicked(event):
                    start_attack(player3,enemy1,game_log)
                    label_surface = turnfont.render(enemy1.name + " Turn", True, RED) 
                    hero =  random.choice(players)
                    start_attack(enemy1,hero,game_log)
                    aiturn=True
            
            elif player3.ackbtn2.active and player3.ackbtn2.is_clicked(event):
                    start_attack(player3,enemy2,game_log)
                    label_surface = turnfont.render(enemy2.name + " Turn", True, RED) 
                    hero =  random.choice(players)
                    start_attack(enemy2,hero,game_log)
                    aiturn=True
            
            elif player3.ackbtn3.active and player3.ackbtn3.is_clicked(event):
                    start_attack(player3,enemy3,game_log)
                    label_surface = turnfont.render(enemy3.name + " Turn", True, RED) 
                    hero =  random.choice(players)
                    start_attack(enemy3,hero,game_log)
                    aiturn=True

            elif event.type == pygame.QUIT:
                running = False
        

        for enemy in enemys:
             if(enemy.die):  
                  game_log.add_log("Enemy die" + enemy.name)            
                  for player in players:
                       game_log.add_log("Enemy die" + str(enemy.ai_index))   
                       if(enemy.ai_index==1):
                            player.ackbtn1.active=False   
                            player.ackbtn1.draw(surface)                         
                       elif(enemy.ai_index==2):
                            player.ackbtn2.active=False
                            player.ackbtn2.draw(surface)       
                       elif(enemy.ai_index==3):
                            player.ackbtn3.active=False
                            player.ackbtn3.draw(surface)       
                        
                  enemys.remove(enemy)

        for player in players:
             if(player.die):
                  players.remove(player)
            
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
     
        surface.blit(label_surface, (int(screen_width * 0.5)+20, 70))  # Adjust position as needed  
        if(aiturn):
            pygame.time.delay(500) 
            label_surface = turnfont.render("Player Turn", True, BLACK)
           
        if(enemy1.die and enemy2.die and  enemy3.die):
             game_log.add_log("Enemy all RIP ")            
             surface.blit(font.render("You WIN", True, LIGHT_GREEN),(int(screen_width * 0.5)+20, int(screen_height * 0.5))) 
             play_short_sound(win)
             pygame.display.flip()
             pygame.time.delay(3000)             
             running=False
             main()

        elif(player1.die and player2.die and player3.die):
              game_log.add_log("Hero all RIP ")           
              surface.blit(font.render("You Lose", True, DARK_RED),(int(screen_width * 0.5)+20, int(screen_height * 0.5)))
              play_short_sound(lose)
              pygame.display.flip()
              pygame.time.delay(3000)
              running=False
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



