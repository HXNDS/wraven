import sys
import pygame as pg
from pygame.locals import *
 
pg.init() # initiates pg
 
clock = pg.time.Clock()
pg.display.set_caption('WRAVEN')
 
WINDOW_SIZE = (1000,800)
 
screen = pg.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
 
display = pg.Surface((500,400)) # used as the surface for rendering, which is scaled
global dashes
dashes = 2
JUMPING = True 
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
global dashing
dashing = False
global player_img

true_scroll = [0,0]
 
def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
 
global animation_frames
animation_frames = {}
 
def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pg.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data
 
def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame
        
 
animation_database = {}
 
animation_database['run'] = load_animation('anims/run',[7,7])
animation_database['idle'] = load_animation('anims/idle',[7,7,40])


"""MAP LOADING""" 
game_map = load_map('DreadedCourts')
#game_map = load_map('map')
#game_map = load_map('0xfiller')
#game_map = load_map('nugmap')

"""TILES"""
grass_img = pg.image.load('imgs/grass.png')
dirt_img = pg.image.load('imgs/dirt.png')
dcSandOne = pg.image.load('imgs/dreadSandOne.png')


player_action = 'idle'
player_frame = 0
player_flip = False
 
player_rect = pg.Rect(150,100,16,16)
 
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]


#healtbar rect 
hpb = pg.Rect(150,150,15,2)

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list
 
def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types
 
        

while True: # game loop
    
    display.fill((50,0,5)) # clear screen by filling it with blue
    
    

    true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
 
    
    """DRAW DISNTANT BG"""

    '''pg.draw.rect(display,(7,0,3),pg.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pg.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pg.draw.rect(display,(50,50,50),obj_rect)
        else:
            pg.draw.rect(display,(90,90,90),obj_rect)'''

    
    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '2':
                display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '3':
                display.blit(dcSandOne,(x*16-scroll[0],y*16-scroll[1]))
            if tile != '0':
                tile_rects.append(pg.Rect(x*16,y*16,16,16))
            x += 1
        y += 1
 

    '''PLAYER MVMNT VARS'''
    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    

    '''JUMPING'''
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.3
    if vertical_momentum > 3:
        vertical_momentum = 3
 
    """DASHING"""
    lop = 2
    if dashing and moving_right:
        player_rect[0] += 50
        print(lop)
        lop -= 1
        print(lop)
    if dashing and moving_left:
        player_rect[0] -= 50
        print(lop)
        lop -= 1
        print(lop)
    if dashing and lop == 0:
        dashing == False
        print(lop)



    if player_movement[0] == 0:
        player_action,player_frame = change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action,player_frame = change_action(player_action,player_frame,'run')
    if player_movement[0] < 0:
        player_flip = True
        player_action,player_frame = change_action(player_action,player_frame,'run')
 
    player_rect,collisions = move(player_rect,player_movement,tile_rects)
 

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    elif player_rect.bottom > WINDOW_SIZE[1]:   #respawn
        player_rect.center = (100,100)
    else:
        air_timer += 1
    
    player_frame += 1
    
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    
    display.blit(pg.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))    
    
    hpb.bottom = player_rect.top
    
    #pg.draw.rect(display,(255,0,0),hpb)  #draw hp bar

    for event in pg.event.get(): # event loop
        if event.type == QUIT:
            pg.quit()
            print("\nGame Closed\n")
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_SPACE:
                JUMPING = True
                #print(air_timer)
                if air_timer < 6 and JUMPING:
                    vertical_momentum -= 5
            if JUMPING and event.key == K_s:
                vertical_momentum = 10
            
            if moving_right and event.key == K_LSHIFT:
                dashing = True
            if moving_left and event.key == K_LSHIFT:
                dashing = True
            
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
            if event.key == K_LSHIFT:
                dashing = False
    screen.blit(pg.transform.scale(display,WINDOW_SIZE),(0,0))
    pg.display.update()
    clock.tick(60)
