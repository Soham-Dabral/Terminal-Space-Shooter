import random
import sys
import os

EMPTY = '.'
PLAYER = 'A'
ENEMY = 'V'
BULLET = '|'
BORDER = '='

WIDTH = 11
HEIGHT = 11

Pilot_name = input("What's your name? ")
Shipname = "Apex"

def clear_screen():
    os.system('cls')

def game_dict(width: int, height: int, lives: int = 3) -> dict:
    return {
        "Width" : width,
        "Height" : height,
        "Lives" : lives,
        "Turn" : 0,
        "Score" : 0,
        "Player_pos" : (width // 2, height - 1),
        "Bullet_pos" : [],
        "Enemy_pos" : [],
        "Command_hist" : [],
        "Game_over" : False,
        "Bullet_count" : 0,
        "Bomb_activated" : False
    }

game_info = game_dict(WIDTH, HEIGHT)

def render_interface(game_dict: dict) -> None:
    width = game_dict["Width"]
    height = game_dict["Height"]

    px, py = game_dict["Player_pos"]

    board = [[EMPTY for _ in range(width)] for _ in range(height)]
    
    if 0 <= px < width and 0 <= py < height: 
        board[py][px] = PLAYER

    for bx, by in game_dict["Bullet_pos"]:
        if 0 <= bx < width and 0 <= by < height:
            board[by][bx] = BULLET
    
    for ex, ey in game_dict["Enemy_pos"]:
        if 0 <= ex < width and 0 <= ey < height:
            board[ey][ex] = ENEMY

    border = BORDER * (width * 2 + 8)

    print(border)
    print(f"Pilot: {Pilot_name}    Spaceship: {Shipname}")
    print(f"Turn: {game_dict['Turn']}    Score: {game_dict['Score']}    Lives: {game_dict['Lives']}")
    print(border)

    for row in board:
        print("    " + " ".join(row))
    
    print(border)

def move_player(player_position: tuple[int, int], command: str, width: int) -> tuple[int, int]:
    command = command.strip().lower()
    px, py = player_position

    if command == 'a' and px > 0:
        px -= 1
    elif command == 'd' and px < width - 1:
        px +=1

    return (px, py)

def initial_bullet_pos(player_position: tuple[int, int]) -> list[tuple[int, int]]:
    bx, by = player_position
    return (bx, by)

def updated_bullets(initial_bullet_pos: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [(bx, by - 1) for bx, by in initial_bullet_pos]
    
def on_screen_bullets(updated_bullets: list[tuple[int, int]], height: int) -> list[tuple[int, int]]:
    return [(bx, by) for bx, by in updated_bullets if 0 <= by < height - 1]

def initial_enemy_pos(width: int) -> list[tuple[int, int]]:
    ex = random.randint(0, width - 1)
    return(ex, -1)

def updated_enemies(initial_enemy_pos: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return [(ex, ey + 1) for ex, ey in initial_enemy_pos]

def on_screen_enemies(updated_enemies: list[tuple[int, int]], height: int) -> list[tuple[int, int]]:
    return [(ex, ey) for ex, ey in updated_enemies if 0 <= ey < height - 1]

def resolve_bullet_enemy_collisions(on_screen_bullets: list[tuple[int, int]], on_screen_enemies: list[tuple[int, int]], Bomb_activated: bool) -> tuple[list, list, int, bool]:
    collided_bullets = set()
    collided_bullets2 = set()
    collided_enemies = set()

    #Since on_screen_bullets and on_screen_enemies are a list of tuples so we just compare the exact tuple to resolve the bullet and enemy
    for bx, by in on_screen_bullets:
        for ex, ey in on_screen_enemies:
            if bx == ex and by == ey:
                collided_bullets.add((bx, by))
                collided_enemies.add((ex, ey))

                if Bomb_activated == True:
                    collided_enemies.update([(ex, ey), (ex - 1, ey), (ex + 1, ey), (ex, ey - 1), (ex, ey + 1), (ex - 1, ey - 1), (ex + 1, ey + 1), (ex - 1, ey + 1), (ex + 1, ey - 1)])
                    Bomb_activated = False
            
            elif bx == ex and by - 1 == ey:
                collided_bullets2.add((bx, by - 1))
                collided_enemies.add((ex, ey))
                if Bomb_activated == True:
                    collided_enemies.update([(ex, ey), (ex - 1, ey), (ex + 1, ey), (ex, ey - 1), (ex, ey + 1), (ex - 1, ey - 1), (ex + 1, ey + 1), (ex - 1, ey + 1), (ex + 1, ey - 1)])
                    Bomb_activated = False

    remaining_bullets = [
        (bx, by) for (bx, by) in on_screen_bullets
        if (bx, by) not in collided_bullets and (bx, by - 1) not in collided_bullets2
    ]

    remaining_enemies = [
        enemy for enemy in on_screen_enemies
        if enemy not in  collided_enemies
    ]

    score_gain = (len(collided_bullets) + len(collided_bullets2))* 10
    
    return remaining_bullets, remaining_enemies, score_gain, Bomb_activated

def resolve_player_enemy_collisions(on_screen_enemies: list[tuple[int, int]], player_position: tuple[int, int], height: int, lives: int = 3) -> list[tuple[int, int, int]]:
    px, py = player_position
    remaining_enemies = []

    for ex, ey in on_screen_enemies:
        if ey >= height: 
            continue
        
        elif ey == py:
            lives -= 1
        
        else:
            remaining_enemies.append((ex, ey))

    return remaining_enemies, lives

def step(game_dict: dict, command: str, spawn_probability: float = 0.75) -> dict:
    command = command.strip().lower()

    game = {
        "Width" : game_dict["Width"],
        "Height" : game_dict["Height"],
        "Player_pos" : game_dict["Player_pos"],
        "Bullet_pos" : list(game_dict["Bullet_pos"]),
        "Enemy_pos" : list(game_dict["Enemy_pos"]),
        "Score" : game_dict["Score"],
        "Turn" : game_dict["Turn"],
        "Lives" : game_dict["Lives"],
        "Command_hist" : list(game_dict["Command_hist"]),
        "Game_over" : game_dict["Game_over"],
        "Bullet_count" : game_dict["Bullet_count"],
        "Bomb_activated" : game_dict["Bomb_activated"]
    }

    def check_bullet_enemy_collisions():
        bullets, enemies, score_gain, bomb_state = resolve_bullet_enemy_collisions(game["Bullet_pos"], game["Enemy_pos"], game["Bomb_activated"])
        game["Bullet_pos"] = bullets
        game["Enemy_pos"] = enemies
        game["Score"] += score_gain
        game["Bomb_activated"] = bomb_state

    if command == 'q':
        sys.exit(f"Score: {game['Score']}")
        game["Game_over"] = True

    game["Player_pos"] = move_player(game["Player_pos"], command, game["Width"])

    if command == 'f':
        game["Bullet_pos"].append(initial_bullet_pos(game["Player_pos"]))
        game["Bullet_count"] += 1
        
        if game["Bullet_count"] == 4:
            game["Bomb_activated"] = True
            game["Bullet_count"] = 0

    game["Command_hist"].append(command)
        
    game["Turn"] += 1

    #Spawning enemy
    if random.random() < spawn_probability:
        game["Enemy_pos"].append(initial_enemy_pos(game["Width"]))
        
    check_bullet_enemy_collisions()

    game["Bullet_pos"] = updated_bullets(game["Bullet_pos"])
    game["Enemy_pos"] = updated_enemies(game["Enemy_pos"])

    check_bullet_enemy_collisions()
        
    game["Enemy_pos"], game["Lives"] = resolve_player_enemy_collisions(game["Enemy_pos"], game["Player_pos"], game["Height"], game["Lives"])

    if game["Lives"] <= 0:
       game["Game_over"] = True
       sys.exit(f"Score: {game['Score']}")

    return game

while not game_info["Game_over"]:
    clear_screen()
    render_interface(game_info)
    command = input("Your move: ")
    game_info = step(game_info, command)
