#danihek copyrgiht xd (serio)
import numpy as np
import matplotlib.pyplot as plt
import random
import pygame
import time
import math

window_width = 800
window_height = 800

cell_size = 8

grid_width = 100
grid_height = 100
grid_x = (window_width - grid_width * cell_size) // 2
grid_y = (window_height - grid_height * cell_size) // 2

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)  

print("Population Size: ")
number_of_population = input()

if number_of_population != int:
    number_of_population = 100

print("dangerous place position (1-2): ")

DANGER_TYPE = input()

if DANGER_TYPE != int:
    DANGER_TYPE = 1

_interbolean = True
#number_of_population = 100

class CreatureNetwork:
    def __init__(self, genome):
        self.genome = genome
        self.weights1 = genome[:16].reshape(4, 4)
        self.biases1 = genome[16:20]
        self.weights2 = genome[20:24]
        self.bias2 = genome[24]

    def forward(self, inputs):
        hidden_layer = np.dot(inputs, self.weights1) + self.biases1
        hidden_layer = np.maximum(hidden_layer, 0)
        output_layer = np.dot(hidden_layer, self.weights2) + self.bias2
        return output_layer 

class Creature_:
    def __init__(self,x,y,genome=None):
        self.x = x
        self.y = y
        self.velocity = [0, 0] 
        self.position = [x, y]
        self.acceleration = [0, 0]
        self.hp = 10
        self.skincolor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.genome = genome
        if genome is None:
            self.genome = np.random.randn(25) # 16 weights, 4 biases, 4 weights, 1 bias
        self.network = CreatureNetwork(self.genome)
    
    def move(self):
        # update velocity based on acceleration
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        # cap velocity at a maximum speed of 5 pixels per frame
        speed = np.linalg.norm(self.velocity)
        if speed > 5:
            self.velocity[0] =  self.velocity[0] / speed
            self.velocity[1] =  self.velocity[1] / speed
        # update position based on velocity, keeping the creature inside the grid
        new_position = [self.position[0] + self.velocity[0], self.position[1] + self.velocity[1]]
        if new_position[0] < 0:
            new_position[0] = 1
            self.velocity[0] *= -1
        elif new_position[0] > 99:
            new_position[0] = 99
            self.velocity[0] *= -1
        if new_position[1] < 0:
            new_position[1] = 0
            self.velocity[1] *= -1
        elif new_position[1] > 99:
            new_position[1] = 99
            self.velocity[1] *= -1
        self.position = new_position
    
    def think(self, inputs):
        output = self.network.forward(inputs)
        if isinstance(output, (tuple, list)):
            # scale output to a maximum magnitude of 1
            output_magnitude = np.linalg.norm(output)
            if output_magnitude > 1:
                output /= output_magnitude
            # update acceleration based on scaled output
            self.acceleration = [output[0], output[1]]
        else:
            # handle scalar output as an angle in radians
            angle = output * np.pi
            # convert angle to x and y components of unit vector
            self.acceleration = [ np.cos(angle), np.sin(angle)]

    def update(self):
        inputs = self.position + self.velocity
        self.think(inputs)
        self.move()
        
        self.hp -= 1

    def isSafeToRep(self):
        if (self.position[0] < 30 and self.position[1] < 30) or (self.position[0] > 70 and self.position[1] > 70):
#        if ((self.position[0] < 60 and self.position[1] < 60) and (self.position[0] > 40 and self.position[1] > 40)):
            return True
        else:
            return False

    def reproduce(self):
        mutated_genome = self.network.genome + np.random.randn(25) * 0.1
        return Creature_(self.position[0],self.position[1],mutated_genome)

def interface(window, population,nmbOfGenerations):
    window.fill(gray)
    pygame.display.update() #update method
    for i in range(grid_width):
            for j in range(grid_height):
                pygame.draw.rect(window, black, [grid_x + i * cell_size, grid_y + j * cell_size, cell_size, cell_size], 1) #drawing grid

    pygame.draw.rect(window, black, [grid_x - 2, grid_y - 2, grid_width * cell_size + 4, grid_height * cell_size + 4], 4) #ramka
    text = font.render('Generation: ' + str(nmbOfGenerations), True, (255, 255, 255))
    text2 = font.render('Creatures alive: ' + str(len(population)), True, (255, 255, 255))
    window.blit(text, (25, 25))
    window.blit(text2, (window_width-425, 25))

    for j in range(len(population)):
            pygame.draw.circle(window, population[j].skincolor, [(population[j].position[0]*cell_size)+grid_x,(population[j].position[1]*cell_size)+grid_y], cell_size//2) #drawing creatures

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        

# ================================================ START =============================================
#CONFIG

print("\n================================================\nSize of Population: " + str(number_of_population))
print("Danger Type: " + str(DANGER_TYPE))
print("================================================\n")

population = []

for i in range(number_of_population):
    x = random.randint(0,grid_width)
    y = random.randint(0,grid_height)
    population.append(Creature_(x, y))

oneortwo = False


# stworzenie okna
if _interbolean:    
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption('Sym2')
    font = pygame.font.Font('freesansbold.ttf', 32)

    clock = pygame.time.Clock()
    window.fill(gray)

nmbOfGenerations = -1
while True:

    nmbOfGenerations += 1
    jkk =0
    while jkk <100:
        jkk+=1
        #graphics
        window.fill(gray)
        for i in range(grid_width):
            for j in range(grid_height):
                pygame.draw.rect(window, black, [grid_x + i * cell_size, grid_y + j * cell_size, cell_size, cell_size], 1) #drawing grid

        pygame.draw.rect(window, black, [grid_x - 2, grid_y - 2, grid_width * cell_size + 4, grid_height * cell_size + 4], 4) #ramka
        

        if DANGER_TYPE == 1:
            pygame.draw.line(window, (255,0,0), (0*cell_size,30*cell_size), (30*cell_size,30*cell_size))
            pygame.draw.line(window, (255,0,0), (30*cell_size,0*cell_size), (30*cell_size,30*cell_size))

            pygame.draw.line(window, (255,0,0), (100*cell_size,70*cell_size), (70*cell_size,70*cell_size))
            pygame.draw.line(window, (255,0,0), (70*cell_size,100*cell_size), (70*cell_size,70*cell_size))

        if (DANGER_TYPE == 2):    
            pygame.draw.line(window, (255,0,0), (40*cell_size,40*cell_size), (40*cell_size,60*cell_size))
            pygame.draw.line(window, (255,0,0), (40*cell_size,40*cell_size), (60*cell_size,40*cell_size))
            pygame.draw.line(window, (255,0,0), (60*cell_size,60*cell_size), (40*cell_size,60*cell_size))
            pygame.draw.line(window, (255,0,0), (60*cell_size,60*cell_size), (60*cell_size,40*cell_size))

        text = font.render('Generation: ' + str(nmbOfGenerations), True, (255, 255, 255))
        text2 = font.render('Creatures alive: ' + str(len(population)), True, (255, 255, 255))
        window.blit(text, (25, 25))
        window.blit(text2, (window_width-425, 25))
        for j in range(len(population)):
            population[j].update()
            pygame.draw.circle(window, population[j].skincolor, [(population[j].position[0]*cell_size)+grid_x,(population[j].position[1]*cell_size)+grid_y], cell_size//2) #drawing creatures
        pygame.display.update() #update method  
        #time.sleep(0.01)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
    #reproduce method
    # 
    #and natural selection
    #print(population[0].genome)
    reproduced_ = 0
    killedAndDissapeared = 0
    counter = 0    
    while counter < len(population):
        if population[counter].isSafeToRep():
            population[counter] = population[counter].reproduce()
            reproduced_ += 1
        else:
            population.pop(counter)
            killedAndDissapeared += 1
        counter += 1

    counter = 0
    while counter < killedAndDissapeared:
        x = random.randint(0,grid_width)
        y = random.randint(0,grid_height)
        tempUNIT = population[counter].reproduce()
        population.append(tempUNIT)
        counter+=1
    print("Generation: "+str(nmbOfGenerations))
    print("population lived: " + str(round((reproduced_/number_of_population)*100,2)) + "% from " + str(number_of_population) + " | reproduced: "+str(reproduced_))
	#print("reproduced: "+str(reproduced_)+ " | added to refill populaion: " + str(counter) +" | killed and dissapeared: "+str(killedAndDissapeared)+"\n")
    #print(population[0].genome)
            
