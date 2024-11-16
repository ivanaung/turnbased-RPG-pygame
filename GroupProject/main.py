
import pygame
import pygame_menu
from custom_theme import * 
from gamelog import GameLog
from player import *
from enemy import *
from button import *

#for sound and game engin
pygame.mixer.init()
pygame.init()

#main game screen
screen_width = 900
screen_height = 600

#keyboard shortcut
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
LIGHT_GREEN = (100,255,0)


#background music
intro_music = "GroupProject/sound/intro.mp3"
gameplay_music = "GroupProject/sound/game_play.mp3"

#sound effect
mouse_click_sound = pygame.mixer.Sound("GroupProject/sound/mouseclick.mp3")
attack_sound = pygame.mixer.Sound("GroupProject/sound/update.mp3")
die_sound = pygame.mixer.Sound("GroupProject/sound/die.wav")
win_sound = pygame.mixer.Sound("GroupProject/sound/win.wav")
lose_sound = pygame.mixer.Sound("GroupProject/sound/lose.wav")
promoted_sound = pygame.mixer.Sound("GroupProject/sound/promoted.mp3")

#set the game area
surface = pygame.display.set_mode((screen_width, screen_height))
log_rect = pygame.Rect(0,0,int(screen_width * 0.2),screen_height)
game_rect = pygame.Rect(int(screen_width * 0.2), 0, screen_width, screen_height)
game_log = GameLog(surface,int(screen_width * 0.2),screen_height-20,20)

#set fond
font = pygame.font.SysFont("Times New Roman",40)
font.set_bold(True)
font.set_italic(True)
label = font.render("Level - "+str(game_level), True, (255, 0, 0))  # White color
turnfont = pygame.font.SysFont("Times New Roman",25)
turnfont.set_bold(True)

#set backgound image
background_image = pygame.image.load('GroupProject/menu_bg.png')
background_image = pygame.transform.scale(background_image,(screen_width,screen_height))

background_fight1 = pygame.image.load('GroupProject/level/level1bg.png')
background_fight1 = pygame.transform.scale(background_fight1,(int(screen_width * 0.8),screen_height))

#Attack logic (Main game logic)
def start_attack(attacker,target,game_log):
     #game_log.add_log("Attacker Attack Point :" + str(attacker.atkpoint))
     #game_log.add_log("Target Defence Point :" + str(attacker.defpoint))
     play_short_sound(attack_sound)       
     game_log.add_log(attacker.name +"  attack to "+ target.name)
     if(target.die==False):
        
        Damage= (attacker.atkpoint - target.defpoint) + (random.randint(-5,10))  #Damage point calculate         
       
        if(Damage>0):
             target.health -= Damage                                                #Assigned the target HP
             attacker.experience += Damage                                         #Increase attacker EXP
             if(target.health<= 0):
                  play_short_sound(die_sound)    
        else:
            Damage=0    
        
        if(Damage > 10):
            target.experience += int(target.experience * 0.20)
        elif(Damage <= 0):            
            target.experience += int(target.experience * 0.50)

        
        game_log.add_log("Tgt:" + target.name +" |Damage :" + str(Damage) + "|Exp:"+ str(target.experience))
        game_log.add_log("Atk:" + attacker.name +" |Exp:"+ str(attacker.experience))
     
        if(attacker.experience >=100):
            attacker.rank +=1            
            attacker.defpoint +=2                                                   #Increase defence point based on rank
            attacker.atkpoint +=3
            attacker.experience -= 100
            play_short_sound(promoted_sound)
            game_log.add_log(attacker.name + " Promoted Rank!")
    

#Game play screen    
def start_game():
    play_music(gameplay_music)
    game_log.add_log("Starting game")
    player1 = Player(name="Hero1", hero_type=random.randint(1,2), position=(int(screen_width * 0.2)+100,screen_height-520),rank=0)
    game_log.add_log(player1.name + "|" + player1.type_name + "|atk:" +str(player1.atkpoint) + "|def:" + str(player1.defpoint))

    player2 = Player(name="Hero2", hero_type=random.randint(1,2), position=(int(screen_width * 0.2)+50,screen_height-350),rank=0)
    game_log.add_log(player2.name + "|" + player2.type_name + "|atk:" +str(player2.atkpoint) + "|def:" + str(player2.defpoint))

    player3 = Player(name="Hero3", hero_type=random.randint(1,2), position=(int(screen_width * 0.2)+100,screen_height-180),rank=0)
    game_log.add_log(player3.name + "|" + player3.type_name + "|atk:" +str(player3.atkpoint) + "|def:" + str(player3.defpoint))

    ainameArray = []
    ainameArray = generate_enemy_name(3)
    enemy1 = Enemy(1,name=ainameArray[0], enemy_type=random.randint(1,2), position=(int(screen_width)-200,screen_height-520),rank=0)
    game_log.add_log(enemy1.name + "|" + enemy1.type_name + "|atk:" +str(enemy1.atkpoint) + "|def:" + str(enemy1.defpoint))
    
    enemy2 = Enemy(2,name=ainameArray[1], enemy_type=random.randint(1,2), position=(int(screen_width)-150,screen_height-350),rank=0)
    game_log.add_log(enemy2.name + "|" + enemy2.type_name + "|atk:" +str(enemy2.atkpoint) + "|def:" + str(enemy2.defpoint))

    enemy3 = Enemy(3,name=ainameArray[2], enemy_type=random.randint(1,2), position=(int(screen_width)-200,screen_height-180),rank=0)
    game_log.add_log(enemy3.name + "|" + enemy3.type_name + "|atk:" +str(enemy3.atkpoint) + "|def:" + str(enemy3.defpoint))

    #Set Array to define player and enemy attack sequence
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
            label_surface = turnfont.render("Player Turn", True, BLACK)
           
        #Win/Lose condition checking
        if(enemy1.die and enemy2.die and  enemy3.die):
             game_log.add_log("Enemy all RIP ")            
             surface.blit(font.render("You Win", True, LIGHT_GREEN),(int(screen_width * 0.5)+20, int(screen_height * 0.5))) 
             game_log.add_log("You win Enemy defeated!")
             play_short_sound(win_sound)
             pygame.display.flip()
             pygame.time.delay(3000)             
             running=False
             main()

        elif(player1.die and player2.die and player3.die):
              game_log.add_log("Hero all RIP ")           
              surface.blit(font.render("You Lose", True, DARK_RED),(int(screen_width * 0.5)+20, int(screen_height * 0.5)))
              game_log.add_log("You lose Enemy defeated!")
              play_short_sound(lose_sound)
              pygame.display.flip()
              pygame.time.delay(3000)
              running=False
              main()
              

        pygame.time.delay(100) #main game delay to animinate smooth      
        pygame.display.flip()
        clock.tick(60)          
    pygame.mixer.music.stop()
    pygame.quit()

#sound setting
sound_on = True

def toggle_sound(value):
    global sound_on
    if(sound_on):
        sound_on = False
        pygame.mixer.music.stop()
    else:
        sound_on = True
        play_music(intro_music) 

#create game menu 
menu = pygame_menu.Menu('Welcome', 400, 300,theme= menutheme())
setting_menu = pygame_menu.Menu('Settings',400,300,theme= menutheme())
setting_menu.add.toggle_switch('Music:', sound_on,onchange=toggle_sound)

#create menu action
menu.add.button('Play', start_game)
menu.add.button('Settings', setting_menu)
menu.add.button('Quit', pygame_menu.events.EXIT)

#sound setting
def play_music(musicfile):
    pygame.mixer.stop()  # Stop any currently playing sound
    if(sound_on):
       pygame.mixer.music.load(musicfile)
       pygame.mixer.music.play(-1)          # loop play

def play_short_sound(sound):
        sound.play()



#main menu function
def main():   
    play_music(intro_music)
    while True:   
        #surface.fill(WHITE)      
        pygame.draw.rect(surface, GRAY, log_rect) 
        surface.blit(background_image, (0, 0))

        events = pygame.event.get()
        for event in events:            
            if event.type == pygame.QUIT:        
                exit()
            game_log.handle_events(event)

        if menu.is_enabled():
            menu.update(events)
            menu.draw(surface)
        pygame.display.flip()




if __name__ == '__main__':
    main()



