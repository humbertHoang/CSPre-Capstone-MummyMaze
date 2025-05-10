import pygame
from pygame.locals import *
import json
from graph import Graph

with open("./assets/map.json", "r") as file:
    map_data = json.load(file)

def get_key(X, Y):
    for item in map_data:
        if item["X"] == X and item["Y"] == Y:
            return item["key"]

def get_pos(key):
    return {"X": map_data[key]["X"], "Y": map_data[key]["Y"]}


graph = Graph(6,6)
graph.add_rectangle_vertex()
graph.add_rectangle_edges()

pygame.init()
pygame.display.set_caption("Mummy Maze")

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

MAP_IMG = pygame.image.load("./assets/image/floor.jpg")

# Player's Sprites
PLAYER_UP = pygame.image.load("./assets/image/player/player_up.png")
PLAYER_DOWN = pygame.image.load("./assets/image/player/player_down.png")
PLAYER_LEFT = pygame.image.load("./assets/image/player/player_left.png")
PLAYER_RIGHT = pygame.image.load("./assets/image/player/player_right.png")

# Mummy's Sprites
MUMMY_UP = pygame.image.load("./assets/image/mummy/mummy_up.png")
MUMMY_DOWN = pygame.image.load("./assets/image/mummy/mummy_down.png")
MUMMY_LEFT = pygame.image.load("./assets/image/mummy/mummy_left.png")
MUMMY_RIGHT = pygame.image.load("./assets/image/mummy/mummy_right.png")

SPRITES_OPTIONS = {
    0: (0, 0, 60, 60),
    1: (60, 0, 60, 60),
    2: (120, 0, 60, 60),
    3: (180, 0, 60, 60),
    4: (240, 0, 60, 60)
}

MAP_SURFACE = pygame.transform.scale(MAP_IMG, (WINDOW_WIDTH, WINDOW_HEIGHT))
SPEED = 5
GO_DISTANCE = 100

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MAPS = [
    {
        "name": "1",
        "win_key": 32,
        "player_start": {"x": 0, "y": 0},
        "mummy_start": {"x": 500, "y": 500},
        "walls": [
            {"key": 20, "color": RED, "orientation": "vertical"},
            {"key": 26, "color": RED, "orientation": "horizontal"},
            {"key": 16, "color": BLUE, "orientation": "vertical"},
        ],
    },
    {
        "name": "2",
        "win_key": 17,
        "player_start": {"x": 0, "y": 400},
        "mummy_start": {"x": 500, "y": 100},
        "walls": [
            {"key": 21, "color": RED, "orientation": "vertical"},
            {"key": 26, "color": RED, "orientation": "horizontal"}
        ],
        "traps": [23]
    }
]
CURRENT_MAP_INDEX = 0

def load_map_config(map_config):
    global WIN_KEY, WIN_POS, player, mummy
    WIN_KEY = map_config["win_key"]
    WIN_POS = get_pos(WIN_KEY)
    player.x, player.y = map_config["player_start"]["x"], map_config["player_start"]["y"]
    mummy.x, mummy.y = map_config["mummy_start"]["x"], map_config["mummy_start"]["y"]
    mummy.run_pos = {'X': mummy.x, 'Y': mummy.y}
    GameManager.wall_list.clear()
    for wall_info in map_config["walls"]:
        wall = Wall(wall_info["key"], wall_info["color"])
        GameManager.wall_list.append((wall, wall_info["orientation"]))

class Wall:
    def __init__(self, wall_key, color):
        self.width = None
        self.height = None
        self.surface = None
        self.wall_pos = get_pos(wall_key)
        self.color = color
    
    def setup(self, orientation):   
        if orientation == "horizontal":
            self.width = GO_DISTANCE
            self.height = 8
        elif orientation == "vertical":
            self.width = 8
            self.height = GO_DISTANCE
    
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        
    def draw(self, orientation):
        self.setup(orientation)
        DISPLAY.blit(self.surface, (self.wall_pos['X'], self.wall_pos['Y']))

class GameManager:
    mummy_move = 0 
    can_player_move = True
    game_over = False
    win = False
    
    wall_list = []

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = PLAYER_DOWN
        self.surface = pygame.Surface((100, 100), SRCALPHA)
        self.option = 0
        self.time_count = 0
        
        self.go = 0
        
        self.rect = self.surface.get_rect()
        
    def animate(self):
        if self.option in SPRITES_OPTIONS:
            coords = SPRITES_OPTIONS[self.option]
            self.surface.blit(self.img, (20, 20), coords)
            
    def draw(self):
        DISPLAY.blit(self.surface, (self.x, self.y))
        
    def update_rect(self):
        self.rect.topleft = (self.x, self.y)
        
    def update(self, left, down, up, right):
        
        if GameManager.mummy_move == 0:
            if self.go < GO_DISTANCE:
                if self.time_count < SPEED:
                    self.option = 0
                elif self.time_count < SPEED*2:
                    self.option = 1
                elif self.time_count < SPEED*3:
                    self.option = 2
                elif self.time_count < SPEED*4:
                    self.option = 3
                elif self.time_count < SPEED*5:
                    self.option = 4
                
                if self.time_count > SPEED*5:
                    self.time_count = 0
                    
                if left or right or up or down:
                    self.surface.fill((0, 0, 0, 0))
                    self.time_count += 1
                    self.go += SPEED
                
                    if left:
                        self.img = PLAYER_LEFT
                        self.x -= SPEED
                        
                    if right:
                        self.img = PLAYER_RIGHT
                        self.x += SPEED
                        
                    if up:
                        self.img = PLAYER_UP
                        self.y -= SPEED
                        
                    if down:
                        self.img = PLAYER_DOWN
                        self.y += SPEED
                    
                self.animate()
            else:
                self.go = 0
                
                if player.rect.colliderect(mummy.rect):
                    GameManager.game_over = True
                else:
                    player_key = get_key(player.x, player.y)
                    
                    if player_key == WIN_KEY:
                        GameManager.game_over = True
                        GameManager.win = True
                    else:
                        GameManager.mummy_move = 1

class Mummy:
    def __init__(self):
        self.x = 500
        self.y = 500
        self.img = MUMMY_DOWN
        self.surface = pygame.Surface((100, 100), SRCALPHA)
        self.option = 0
        self.time_count = 0
        
        self.go = 0
        self.run_pos = {"X": self.x, "Y": self.y}
        
        self.rect = self.surface.get_rect()
        
    def animate(self):
        if self.option in SPRITES_OPTIONS:
            coords = SPRITES_OPTIONS[self.option]
            self.surface.blit(self.img, (20, 20), coords)
            
    def draw(self):
        DISPLAY.blit(self.surface, (self.x, self.y))
    
    def update_rect(self):
        self.rect.topleft = (self.x, self.y)
        
    def update(self, left, right, up, down):
        if self.go < GO_DISTANCE:
            if self.time_count < SPEED:
                self.option = 0
            elif self.time_count < SPEED*2:
                self.option = 1
            elif self.time_count < SPEED*3:
                self.option = 2
            elif self.time_count < SPEED*4:
                self.option = 3
            elif self.time_count < SPEED*5:
                self.option = 4
            
            if self.time_count > SPEED*5:
                self.time_count = 0
                
            if left or right or up or down:
                self.surface.fill((0, 0, 0, 0))
                self.time_count += 1
                self.go += SPEED
            
                if left:
                    self.img = MUMMY_LEFT
                    self.x -= SPEED
                    
                if right:
                    self.img = MUMMY_RIGHT
                    self.x += SPEED
                    
                if up:
                    self.img = MUMMY_UP
                    self.y -= SPEED
                    
                if down:
                    self.img = MUMMY_DOWN
                    self.y += SPEED
                    
            self.animate()
        else:
            self.go = 0
            GameManager.mummy_move += 1
            
            if GameManager.mummy_move == 3:
                GameManager.mummy_move = 0
                GameManager.can_player_move = True
    
    def run(self, key_player, player_x, player_y):

        if self.go == 0:
            key_mummy = get_key(self.x, self.y)
        if self.y != self.run_pos["Y"]:
            if self.go == 0:
                direction = "up" if self.y > self.run_pos["Y"] else "down"
            
            if self.y > self.run_pos["Y"]:
                self.update(up=True, down=False, left=False, right=False)
            else:
                self.update(up=False, down=True, left=False, right=False)
        elif self.x != self.run_pos["X"]:
            if self.go == 0:
                direction = "left" if self.x > self.run_pos["X"] else "right"
            
            if self.x > self.run_pos["X"]: 
                self.update(up=False, down=False, left=True, right=False)
            else:
                self.update(up=False, down=False, left=False, right=True)
        else:
            key_mummy = get_key(self.x, self.y)

            if key_mummy == key_player:
                GameManager.game_over = True
            else:
                vertical_walls = [wall['key'] for wall in MAPS[CURRENT_MAP_INDEX]['walls'] if wall['orientation'] == 'vertical']
                horizontal_walls = [wall['key'] for wall in MAPS[CURRENT_MAP_INDEX]['walls'] if wall['orientation'] == 'horizontal']

                left_key, right_key = key_mummy - 1, key_mummy + 1
                up_key,   down_key  = key_mummy - 6, key_mummy + 6

                if (player_x < mummy.x and key_mummy in vertical_walls) or (player_x > mummy.x and right_key in vertical_walls):
                    if player_y == mummy.y:
                        GameManager.mummy_move = 0
                        GameManager.can_player_move = True
                    elif player_y < mummy.y:
                        if key_mummy in horizontal_walls or key_player in horizontal_walls:
                            GameManager.mummy_move = 0
                            GameManager.can_player_move = True
                        else:
                            self.run_pos["Y"] -= GO_DISTANCE
                    elif player_y > mummy.y:
                        if down_key in horizontal_walls or key_player in horizontal_walls:
                            GameManager.mummy_move = 0
                            GameManager.can_player_move = True
                        else:
                            self.run_pos["Y"] += GO_DISTANCE
                
                elif (player_y < mummy.y and key_mummy in horizontal_walls) or (player_y > mummy.y and down_key in horizontal_walls):
                    if player_x == mummy.x:
                        GameManager.mummy_move = 0
                        GameManager.can_player_move = True
                    elif player_x < mummy.x:
                        if key_mummy in vertical_walls or key_player in vertical_walls:
                            GameManager.mummy_move = 0
                            GameManager.can_player_move = True
                        else:
                            self.run_pos["X"] -= GO_DISTANCE
                    elif player_x > mummy.x:
                        if right_key in vertical_walls or key_player in vertical_walls:
                            GameManager.mummy_move = 0
                            GameManager.can_player_move = True
                        else:
                            self.run_pos["X"] += GO_DISTANCE

                else:
                    run_key = graph.find_next_step(key_mummy, key_player)
                    self.run_pos = get_pos(run_key)

is_running = True

player = Player()
mummy = Mummy()

win_surface = pygame.Surface((100, 100))

player_up, player_down, player_left, player_right = False, False, False, False

load_map_config(MAPS[CURRENT_MAP_INDEX])

while is_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_running = False
            
        if event.type == KEYDOWN and GameManager.can_player_move:
            if event.key == K_UP:
                player_up = True
            if event.key == K_DOWN:
                player_down = True
            if event.key == K_LEFT:
                player_left = True
            if event.key == K_RIGHT:
                player_right = True
            if event.key == K_SPACE:
                GameManager.can_player_move = False
                GameManager.mummy_move = 1
                continue
            
            GameManager.can_player_move = False
            
        if event.type == KEYDOWN and event.key == K_r and GameManager.game_over == True:
            load_map_config(MAPS[CURRENT_MAP_INDEX])
            player.go = 0
            GameManager.game_over = False
            GameManager.win = False
            GameManager.mummy_move = 0
            GameManager.can_player_move = True

        if event.type == KEYDOWN and event.key == K_TAB:
            CURRENT_MAP_INDEX = (CURRENT_MAP_INDEX + 1) % len(MAPS)
            load_map_config(MAPS[CURRENT_MAP_INDEX])
            player.go = 0
            GameManager.game_over = False
            GameManager.win = False
            GameManager.mummy_move = 0
            GameManager.can_player_move = True
        
            
    DISPLAY.fill((0, 0, 0, 0))
    
    DISPLAY.blit(MAP_SURFACE, (0, 0))
    
    TRAP_COLOR = (128, 128, 128)
    for trap_key in MAPS[CURRENT_MAP_INDEX].get("traps", []):
        trap_pos = get_pos(trap_key)
        pygame.draw.rect(DISPLAY, TRAP_COLOR, (trap_pos["X"], trap_pos["Y"], GO_DISTANCE, GO_DISTANCE))

    for wall, orientation in GameManager.wall_list:
        wall.draw(orientation)

    win_surface.fill((0, 255, 0))
    DISPLAY.blit(win_surface, (WIN_POS['X'], WIN_POS['Y']))
    
    player.draw()
    player.update(up=player_up, down=player_down, left=player_left, right=player_right)
    
    player_key = get_key(player.x, player.y)
    if player_key in MAPS[CURRENT_MAP_INDEX].get("traps", []):
        GameManager.game_over = True
        GameManager.win = False

    mummy.draw()
    mummy.animate()
    
    player.update_rect()
    mummy.update_rect()

    
    if GameManager.game_over == False:
        if player.go == 0:
            player_up, player_down, player_left, player_right = False, False, False, False
        
        if GameManager.mummy_move >= 1:
            player_key = get_key(player.x, player.y)
            mummy.run(player_key, player.x, player.y)
    else:
        player_up, player_down, player_left, player_right = False, False, False, False
        
        if GameManager.win == False:
            lose_message = pygame.transform.scale(pygame.image.load("./assets/image/tryagain_red.png"), (250, 46))
            lose_background = pygame.transform.scale(pygame.image.load("./assets/image/end.png"), (540, 401))
            
            lose_board_surface = pygame.Surface((540, 401), SRCALPHA)
            lose_board_surface.blit(lose_background, (0, 0))
            lose_board_surface.blit(lose_message, (150, 300))
            DISPLAY.blit(lose_board_surface, (30, 100))
        else:
            win_message = pygame.transform.scale(pygame.image.load("./assets/image/win.png"), (591, 282))
            DISPLAY.blit(win_message, (0, 150))
    
    pygame.display.update()
    pygame.time.Clock().tick(30)
    
pygame.quit()