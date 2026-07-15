import torch
import random
import os

WIDTH = 11
HEIGHT = 11

PLAYER = 'A'
ENEMY = 'V'
BULLET = '|'
EMPTY = '.'
BORDER = '='
SHIELD = 'O'
SHIELDED_PLAYER = '@'

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

#Stores information
class GameState1:
    def __init__(self, width: int = WIDTH, height: int = HEIGHT, lives: int = 3 ):
        self.width = width
        self.height = height
        
        self.player_x = width // 2
        self.player_y = height - 1

        self.lives = lives
        self.score = 0
        self.turn = 0
        self.game_over = False
        self.shield_on = False

        self.bullets = torch.empty((0, 2), dtype=torch.long)
        self.enemies = torch.empty((0, 2), dtype=torch.long)
        self.shields = torch.empty((0, 2), dtype=torch.long)

    def is_alive(self) -> bool:
        return self.lives > 0

#Handles input and does related things to it        
class GameState2(GameState1):
    def handle_input(self, command: str):
        command = command.strip().lower()
        
        if command == 'a' and self.player_x > 0:
            self.player_x -= 1

        elif command == 'd' and self.player_x < self.width - 1:
            self.player_x +=1

        elif command == 'f':
            self.fire_bullet()
        
        elif command == 'q':
            self.game_over = True
            return

    def fire_bullet(self):
        new_bullet = torch.tensor([[self.player_x, self.player_y]], dtype=torch.long)
        self.bullets = torch.cat([self.bullets, new_bullet], dim=0)

    def spawn_enemy(self):
            x = random.randint(0, self.width - 1)
            new_enemy = torch.tensor([[x, -1]], dtype=torch.long)
            self.enemies = torch.cat([self.enemies, new_enemy], dim=0)
    
    def spawn_shield(self):
        x = random.randint(0, self.width - 1)
        new_shield = torch.tensor([[x, -1]], dtype=torch.long)
        self.shields = torch.cat([self.shields, new_shield], dim=0)

#Move bullets and enemies
class GameState3(GameState2):
    def move_bullets(self) -> torch.Tensor:
        if self.bullets.shape[0] == 0:
            return self.bullets
        self.bullets[:, 1] -= 1
        return self.bullets
        
    def move_shields(self) -> torch.Tensor:
        if self.shields.shape[0] == 0:
            return self.shields
        self.shields[:, 1] += 1
        return self.shields

        
    def move_enemies(self) -> torch.Tensor:
        if self.enemies.shape[0] == 0:
            return self.enemies
        self.enemies[:, 1] += 1
        return self.enemies

#Checking bullet and enemy collisions and managing scores        
class GameState4(GameState3):
    def resolve_bullet_enemy_collisions(self):
        if self.bullets.shape[0] == 0 or self.enemies.shape[0] == 0:
            return
        
        same_position = (self.bullets[:, None, :] == self.enemies[None, :, :]).all(dim=2)
        
        bullet_hit = same_position.any(dim=1)
        enemy_hit = same_position.any(dim=0)

        #.sum() returns the value of sum of Trues in the table as tensor(number of true values) and .item changes that into an int
        enemies_destroyed = int(enemy_hit.sum().item())
        self.score += enemies_destroyed * 10

        self.bullets = self.bullets[~bullet_hit]
        self.enemies = self.enemies[~enemy_hit]
    
#Checks player enemy collisions
class GameState5(GameState4):
    def resolve_player_shield_collisions(self):
        if self.shields.shape[0] == 0:
            return
        
        sx = self.shields[:, 0]
        sy = self.shields[:, 1]

        shield_on_player =  (sx == self.player_x) & (sy == self.player_y)
        
        if shield_on_player.any():
            self.shield_on = True
            self.shields = self.shields[~shield_on_player]
    
    def resolve_player_enemy_collisions(self):
        if self.enemies.shape[0] == 0:
            return

        ex = self.enemies[:, 0]
        ey = self.enemies[:, 1]

        direct_hit = (self.player_x == ex) & (self.player_y == ey)
        reached_player_row = (self.player_y == ey)
        total_damage = direct_hit | reached_player_row
        
        damage_count = int(total_damage.sum().item())
        if damage_count > 0:
            if self.shield_on:
                self.shield_on = False
            else:
                self.lives -= 1
        
        self.enemies = self.enemies[~total_damage]

        if self.lives <= 0:
            self.game_over = True

#Rendring the board
class GameState6(GameState5):
    def build_grid(self) -> list [list[str]]:
        clear_screen()
        grid = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]

        for x, y in self.shields.tolist():
            if 0 <= x < self.width and 0 <= y < self.height:
                grid[y][x] = SHIELD

        for x, y in self.enemies.tolist():
            if 0 <= x < self.width and 0 <= y < self.height:
                grid[y][x] = ENEMY
            
        for x, y in self.bullets.tolist():
            if 0 <= x < self.width and 0 <= y < self.height:
                grid[y][x] = BULLET
        
        if self.shield_on:
            grid [self.player_y][self.player_x] = SHIELDED_PLAYER    
        
        else:
            grid [self.player_y][self.player_x] = PLAYER
        return grid
    
    def render(self):
        grid = self.build_grid()
        
        BORDER = '=' * (WIDTH * 2 + 8)
        
        print(BORDER)
        print(f"Turn: {self.turn}    Score: {self.score}    Lives: {self.lives}")
        print(BORDER)
        for row in grid:
            print(" " + " ".join(row))
        print(BORDER)
        print(f"Bullets: {self.bullets.shape[0]}\nEnemies: {self.enemies.shape[0]}\nShield Activation Status: {self.shield_on}")

#Handles all the other Game States
class GameState(GameState6):
    def __init__(self, width: int = WIDTH, height: int = HEIGHT, lives: int = 3):
        super().__init__(width = width, height = height, lives = lives)
    
    def step(self, command: str, enemy_spawn_probability: float = 0.45, shield_spawn_probability: float = 0.25):
        if self.game_over:
            print("\n Game Over")
            print(f"Final Score: {self.score}")
            return

        self.handle_input(command)

        command = command.strip().lower()
        if command == 'q':
            self.game_over = True
            return

        self.turn += 1

        if random.random() < enemy_spawn_probability:
            self.spawn_enemy()
        
        if random.random() < shield_spawn_probability:
            self.spawn_shield()

        self.move_bullets()
        self.resolve_bullet_enemy_collisions()
        self.move_enemies()
        self.resolve_bullet_enemy_collisions()
        self.move_shields()
        self.resolve_player_shield_collisions()
        self.resolve_player_enemy_collisions()

    def run(self):
        while not self.game_over:
            cmd = input("Your move: ")
            self.step(cmd)
            
            if not self.game_over:
                self.render()
        
        print("\nGame Over")
        print(f"Final Score: {self.score}")

if __name__ == "__main__":
    random.seed()
    game = GameState()
    game.render()
    game.run()
