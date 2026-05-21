import random
import os

WIDTH = 11
HEIGHT = 11

EMPTY = '.'
PLAYER = 'A'
BULLET = '|'
ENEMY = 'V'
SHIELD = 'O'
SHIELDED_PLAYER = '@'

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

class Spaceship:
    def __init__(self, x, y, lives = 3):
        self.x = x
        self.y = y
        self.lives = lives
        self.score = 0

    def move_left(self):
        if self.x > 0:
            self.x -= 1
    
    def move_right(self):
        if self.x < WIDTH - 1:
            self.x += 1

    def fire(self):
        return Bullet(self.x, self.y)
    
    def hit(self):
        self.lives -= 1

    def position(self):
        return (self.x, self.y)
    
    def is_alive(self):
        return self.lives > 0
    
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def move_up(self):
        self.y -= 1

class Shield:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move_down(self):
        self.y += 1

class Enemy:
    def __init__ (self, x, y):
        self.x = x
        self.y = y

    def move_down(self):
        self.y += 1

class GameState:
    def __init__(self):
        self.player = Spaceship(WIDTH // 2, HEIGHT - 1, lives = 3)
        self.bullets = []
        self.shield = []
        self.enemies = []
        self.turn = 0
        self.game_over = False
        self.bullet_count = 0
        self.bomb_activated = False
        self.shield_activated = False

    def spawn_enemy_and_shield(self, spawn_probability_enemy = 0.45, spawn_probability_shield = 0.25):
        if random.random() < spawn_probability_enemy:
            ex = random.randint(0, WIDTH - 1)
            self.enemies.append(Enemy(ex, -1))

        if random.random() < spawn_probability_shield:
            sx = random.randint(0, WIDTH - 1)
            self.shield.append(Shield(sx, -1))

    def handle_input(self, command):
        command = command.strip().lower()

        if command == 'q':
            self.game_over = True

        elif command == 'a':
            self.player.move_left()

        elif command == 'd':
            self.player.move_right()

        elif command == 'f':
            self.bullets.append(self.player.fire())
            self.bullet_count += 1
            if self.bullet_count == 4:
                self.bomb_activated = True
                self.bullet_count = 0

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.move_up()

    def move_shield(self):
        for s in self.shield:
            s.move_down()

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move_down()

    def resolve_bullet_enemy_collisions(self):
        collided_bullets = set()
        collided_enemies = set()
        explosion_tiles = set()

        explosion_radius = 1
        destroyed_count = 0

        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.x == enemy.x and bullet.y == enemy.y:
                    collided_bullets.add(bullet)
                    
                    if self.bomb_activated == True:
                        for dx in range(-explosion_radius, explosion_radius + 1):
                            for dy in range(-explosion_radius, explosion_radius + 1):
                                explosion_tiles.add((enemy.x + dx, enemy.y + dy))
                        self.bomb_activated = False
                    
                    else: collided_enemies.add(enemy)
                    break
        
        new_enemies = []
        for enemy in self.enemies:
            if enemy in collided_enemies or (enemy.x, enemy.y) in explosion_tiles: 
                destroyed_count += 1
            elif enemy.y < HEIGHT: 
                new_enemies.append(enemy)

        self.player.score += destroyed_count * 10
        self.bullets = [bullet for bullet in self.bullets if bullet not in collided_bullets and bullet.y >= 0]
        self.enemies = new_enemies

    def resolve_player_shield_collisions(self):
        remaining_shields = []

        for s in self.shield:
            if self.player.y == s.y and self.player.x == s.x:
                self.shield_activated = True
                continue
            
            elif s.y >= HEIGHT:
                continue

            else:
                remaining_shields.append(s)

        self.shield = remaining_shields

    def resolve_player_enemy_collisions(self):
        remaining_enemies = []

        for enemy in self.enemies:
            if self.player.y == enemy.y:
                if self.shield_activated:
                    self.shield_activated = False
                    continue

                else: self.player.hit()
            
            elif enemy.y >= HEIGHT:
                continue

            else:
                remaining_enemies.append(enemy)

        self.enemies = remaining_enemies
        if not self.player.is_alive():
            self.game_over = True

    def update(self):
        self.turn += 1
        self.spawn_enemy_and_shield()
        self.move_bullets()
        self.resolve_bullet_enemy_collisions()
        self.move_enemies()
        self.move_shield()
        self.resolve_player_shield_collisions()
        self.resolve_bullet_enemy_collisions()
        self.resolve_player_enemy_collisions()

    def build_board(self):
        board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]

        for bullet in self.bullets:
            if 0 <= bullet.x < WIDTH and 0 <= bullet.y < HEIGHT:
                board[bullet.y][bullet.x] = BULLET
    
        for enemy in self.enemies:
            if 0 <= enemy.x < WIDTH and 0 <= enemy.y < HEIGHT:
                board[enemy.y][enemy.x] = ENEMY

        for s in self.shield:
            if 0 <= s.x < WIDTH and 0 <= s.y < HEIGHT:
                board[s.y][s.x] = SHIELD

        if self.shield_activated == True:
            board[self.player.y][self.player.x] = SHIELDED_PLAYER
        
        else: 
            board[self.player.y][self.player.x] = PLAYER
        
        return board
    
    def render(self):
        clear_screen()
        board = self.build_board()
        BORDER = '=' * (WIDTH * 2 + 8) 
        print(BORDER)
        print(f"Turn: {self.turn}    Score: {self.player.score}    Lives: {self.player.lives}")
        print(BORDER)

        for row in board:
            print("    " + " ".join(row))

    def run(self):
        self.render()
        while not self.game_over:
            command = input("Your move: ").strip().lower()
            
            self.handle_input(command)

            if self.game_over == True:
                break
            
            self.update()
            self.render()
        
        print("\n Game Over")
        print(f"Final Score: {self.player.score}")

if __name__ == "__main__":
    random.seed()
    game = GameState()
    game.run()