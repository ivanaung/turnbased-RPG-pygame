import random
import pygame
from sprite_sheet import SpriteSheet
       

# Colors
BACKGROUND_COLOR = (255, 255, 255)
RANK_BAR_COLOR = (200, 20, 0)  # Dark green for the rank bar
CHEVRON_COLOR = (255, 255, 255)  # White for chevrons
WHITE = (255, 255, 255)  
OUTLINE_COLOR = (173, 255, 47)  # Light green for the outline  
GRAY = (200, 200, 200)
GREEN = (0,255,0)
RED = (200, 20, 20)

class Enemy:
    def __init__(self,index, name, enemy_type, position=(0, 0), hp=100, exp=0, rank=0):
        self.font = pygame.font.SysFont("Arial",12)
        self.font.set_bold(True)
        self.name = name
        self.enemy_type = enemy_type
        self.position = position  # (x, y) coordinates
        self.health = hp
        self.max_health = 100
        self.experience = exp
        self.rank = rank
        self.type_name = "Warrior"
        self.atkpoint = 0
        self.defpoint = 0 
        self.die = False
        self.ai_index = index

        imagefile = self.load_enemy_imagePath(enemy_type)
         # Load sheet
        self.sprite_sheet = SpriteSheet(imagefile)
        self.frames = self.sprite_sheet.extract_frames(100,120)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]

        # Load hero image based on hero type
        #self.image = self.load_enemy_image(enemy_type)
        self.rect = self.image.get_rect(topleft=self.position) if self.image else None

    
        
    def load_enemy_imagePath(self, enemy_type):
        """Load an image based on the hero type."""
        enemy_tanker ={
            1 : "GroupProject/enemy/enemy1.png",
            2 : "GroupProject/enemy/enemy2.png",
            3 : "GroupProject/enemy/enemy3.png",

        }
        enemy_warrior = {          
            1 : "GroupProject/enemy/enemy4.png",
            2 : "GroupProject/enemy/enemy5.png",
            3 : "GroupProject/enemy/enemy6.png",           
        }

        try:
            if(enemy_type==1):   #Tanker 
                imagefile = enemy_tanker.get(random.randint(1,3), "default.png")
                self.type_name = "Tanker"
                self.atkpoint = random.randint(1,10)    #Set Tanker Attack Point
                self.defpoint = random.randint(5,15)    #Set Tanker Defence Point
            else:
                imagefile = enemy_warrior.get(random.randint(1,3), "default.png")
                self.type_name = "Warrior"
                self.atkpoint = random.randint(5,20)    #Set Warrior Attack Point
                self.defpoint = random.randint(1,10)    #Set Warrior Defence Point
           
            return imagefile
        except pygame.error as e:
            print(f"Error loading image for {enemy_type}: {e}")
            return None

    def draw(self, screen):
        """Draw the player and health bar on the screen."""        
        if self.image:
            text_name= self.font.render(self.name + " [" + self.type_name + "]" , True, (0,0,0))
            screen.blit(text_name, (self.position[0]+2,self.position[1]+self.image.get_height()+15))
            if(self.health<=0):
                self.image = pygame.image.load("GroupProject/enemy/enemyrip.png")
                self.die = True
            else:
                self.draw_health_bar(screen)
                self.draw_rank_arrow_bar(screen,self.rank)  
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
            screen.blit(self.image, self.position)   

    def draw_health_bar(self, screen):
        """Draw a health bar below the hero image."""
        bar_width = self.rect.width
        bar_height = 8
        bar_x = self.position[0]
        bar_y = self.position[1] + self.rect.height + 5  # Position below the image

        # Calculate current health width
        health_ratio = self.health / self.max_health
        current_health_width = int(bar_width * health_ratio)
        #border
        pygame.draw.rect(screen, (100, 100,100), (bar_x+1, bar_y+1, bar_width+2, bar_height+3))  # Red for empty bar
        # Draw the background (empty bar)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))  # Red for empty bar
        # Draw the current health (filled bar)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_health_width, bar_height))  # Green for filled bar


    def draw_chevron(self,screen,x, y, width, height, color):
        points = [
            (x, y),
            (x + width // 2, y + height // 2),
            (x, y + height),
            (x - width // 2, y + height // 2)
        ]
        pygame.draw.polygon(screen, color, points)

    # Function to draw the main rank bar with a pointed bottom
    def draw_rank_bar(self,screen,x, y, width, height, num_chevrons):
        # Draw the main rectangle
        pygame.draw.rect(screen, RANK_BAR_COLOR, (x, y, width, height))

        # Draw the pointed bottom
        pygame.draw.polygon(screen, RANK_BAR_COLOR, [
            (x, y + height),
            (x + width // 2, y + height + width // 2),
            (x + width, y + height)
        ])

        # Draw the chevrons
        chevron_spacing = 3
        chevron_height = 10
        for i in range(num_chevrons):
            chevron_y = y + height - (i + 1) * (chevron_height + chevron_spacing)            
            self.draw_chevron(screen,x + width // 2, chevron_y, width // 2, chevron_height, CHEVRON_COLOR)


    def draw_rank_arrow_bar(self,screen,rank):
        # Define the width of each rank section       
        x = self.position[0] + (self.rect.width + 5)
        y = self.position[1] + 10
        width=20
        height=40
        section_height = height // 3
        if(rank>=3):
            rank=3

        if(rank>0):
            self.draw_rank_bar(screen,x,y,width,height,rank)
        # Draw the main background bar

    def take_damage(self, damage):
        """Reduce health when taking damage."""
        self.health -= damage
        if self.health < 0:
            self.health = 0  # Ensure health does not drop below 0

    def gain_experience(self, exp_points):
        """Increase experience and check for level up."""
        self.experience += exp_points
        if self.experience >= self.level * 100:
            self.level_up()

    def level_up(self):
        """Level up the player and reset experience."""
        self.level += 1
        self.experience = 0
        self.max_health += 20  # Increase max health on level up
        self.health = self.max_health  # Refill health to new max
        print(f"{self.name} leveled up! Now at level {self.level} with {self.health} health.")

    
  
    
        