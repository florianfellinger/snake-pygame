import pygame
from enum import Enum
import random
import colorsys
import Map1


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


global direction

# Spielfeld und Geschwindigkeit
global speed
global move_rate  # Rate, in der sich die Schlange bewegt (move = 3 -> Schlange bewegt sich nur jeden 3. Frame)
window_width = 600
window_height = 600

# pygame related
pygame.init()
pygame.display.set_caption("Snake")
window = pygame.display.set_mode((window_width, window_height))
refresh_controller = pygame.time.Clock()

# Game Rules
global snake_position
global snake_body


def generate_snake(_pos, _body):
    global snake_position
    global snake_body
    snake_position = _pos
    snake_body = _body


scale = 10
global num_food
global num_food_5
global num_walls

food_positions = []
food_5_positions = []
global wall_positions
score = 0

# Items

global has_magnet
has_magnet = True

# Paint
global hue
hue = 0.0
global R
global G
global B


def is_wall(x, y):
    for wall in wall_positions:
        if wall[0] == x and wall[1] == y:
            return True
    return False


def is_food(x, y):
    for food in food_positions:
        if food[0] == x and food[1] == y:
            return True
    return False


def wall_test():  # setze Wand an bestimmte Position (zu Testzwecken)
    wall_positions.append([300, 100])


def food_5_test():  # setze 5-Punkte-Food an bestimmte Position (zu Testzwecken)
    food_5_positions.append([20, 20])


def generate_walls(_custom_walls=None):
    global wall_positions
    wall_positions = []
    if _custom_walls is not None:
        wall_positions = _custom_walls
    else:
        for i in range(0, num_walls):
            position_ok = False
            while not position_ok:
                new_wall_zero = random.randint(1, (window_width // scale)) * scale
                new_wall_one = random.randint(1, (window_height // scale)) * scale
                # Mindestens 10 Felder rechts vom Start des Schlangenkopfes (und am Kopf selbst) darf keine Wand spawnen
                if new_wall_one == snake_position[1]:
                    if not (snake_position[0] < new_wall_zero < snake_position[0] + 150):
                        position_ok = True
                # nicht bereits eine Wand auf dem Feld
                elif not is_wall(new_wall_zero, new_wall_one):
                    position_ok = True
                else:
                    position_ok = False
                if position_ok:
                    wall_positions.append([new_wall_zero, new_wall_one])


def generate_food():
    food_positions.clear()
    for i in range(0, num_food):
        position_ok = False
        while not position_ok:
            new_food_zero = random.randint(5, ((window_width - 2) // scale)) * scale
            new_food_one = random.randint(5, ((window_height - 2) // scale)) * scale
            # food darf nicht dort spawnen, wo eine Wand oder ein anderes Food ist
            if not is_wall(new_food_zero, new_food_one) and not is_food(new_food_zero, new_food_one):
                position_ok = True
            if position_ok:
                food_positions.append([new_food_zero, new_food_one])
    # 5-Punkte-Food spawnen
    food_5_positions.clear()
    for i in range(0, num_food_5):
        position_ok = False
        while not position_ok:
            new_food_5_zero = random.randint(5, ((window_width - 2) // scale)) * scale
            new_food_5_one = random.randint(5, ((window_height - 2) // scale)) * scale
            # food darf nicht dort spawnen, wo eine Wand oder ein anderes Food ist
            if not is_wall(new_food_5_zero, new_food_5_one) and not is_food(new_food_5_zero, new_food_5_one):
                position_ok = True
            if position_ok:
                food_5_positions.append([new_food_5_zero, new_food_5_one])


def handle_keys(direction):
    new_direction = direction
    for event in [e for e in pygame.event.get() if e.type == pygame.KEYDOWN]:
        if event.key == pygame.K_w and direction != direction.DOWN:
            new_direction = direction.UP
        if event.key == pygame.K_s and direction != direction.UP:
            new_direction = direction.DOWN
        if event.key == pygame.K_d and direction != direction.LEFT:
            new_direction = direction.RIGHT
        if event.key == pygame.K_a and direction != direction.RIGHT:
            new_direction = direction.LEFT
    return new_direction


def move_snake(direction):
    if direction == Direction.UP:
        snake_position[1] -= scale
    if direction == Direction.DOWN:
        snake_position[1] += scale
    if direction == Direction.LEFT:
        snake_position[0] -= scale
    if direction == Direction.RIGHT:
        snake_position[0] += scale
    snake_body.insert(0, list(snake_position))


def generate_new_food(new_food):  # das Food, was aufgesammelt wurde, neu generieren
    same = True
    while same:
        same = False
        new_pos_zero_coord = random.randint(5, ((window_width - 2) // scale)) * scale
        new_pos_one_coord = random.randint(5, ((window_height - 2) // scale)) * scale
        # Prüfen, ob neue food location sich mit bestehender food location oder Wand deckt:
        if not is_food(new_pos_zero_coord, new_pos_one_coord) and not is_wall(new_pos_zero_coord, new_pos_one_coord):
            food_positions[new_food][0] = new_pos_zero_coord
            food_positions[new_food][1] = new_pos_one_coord
        else:
            same = True


def generate_new_food_5(new_food):  # das 5-Punkte-Food, was aufgesammelt wurde, neu generieren
    same = True
    while same:
        same = False
        new_pos_zero_coord = random.randint(5, ((window_width - 2) // scale)) * scale
        new_pos_one_coord = random.randint(5, ((window_height - 2) // scale)) * scale
        # Prüfen, ob neue food location sich mit bestehender food location oder Wand deckt:
        if not is_food(new_pos_zero_coord, new_pos_one_coord) and not is_wall(new_pos_zero_coord, new_pos_one_coord):
            food_5_positions[new_food][0] = new_pos_zero_coord
            food_5_positions[new_food][1] = new_pos_one_coord
        else:
            same = True


def adjust_score(points):
    global score
    score += points


def reset_game():
    # reset snake
    global snake_body
    snake_position[0] = 300
    snake_position[1] = 300
    snake_body = [[300, 300],
                  [290, 300],
                  [280, 300]]
    generate_walls()
    generate_food()
    # reset RGB
    global R
    R = 0
    global G
    G = 0
    global B
    B = 0
    global hue
    hue = 0


def add_additional_snake_segments(num_segments):
    # Richtung des Schwanzendes ermitteln
    snake_end_last_0 = snake_body[len(snake_body) - 1]
    snake_end_last_1 = snake_body[len(snake_body) - 2]
    end_direction = ""
    # rechts
    if snake_end_last_0[0] - 10 == snake_end_last_1[0]:
        end_direction = "right"
    # links
    elif snake_end_last_0[0] + 10 == snake_end_last_1[0]:
        end_direction = "left"
    # oben
    elif snake_end_last_0[1] + 10 == snake_end_last_1[1]:
        end_direction = "up"
    # unten
    elif snake_end_last_0[1] - 10 == snake_end_last_1[1]:
        end_direction = "down"

    # Schlange um <num_segment> weitere Segmente wachsen lassen
    if end_direction == "right":
        for j in range(0, num_segments):
            new_element = [snake_body[len(snake_body) - 1][0] + 10, snake_body[len(snake_body) - 1][1]]
            snake_body.insert(len(snake_body), new_element)
    elif end_direction == "left":
        for j in range(0, num_segments):
            new_element = [snake_body[len(snake_body) - 1][0] - 10, snake_body[len(snake_body) - 1][1]]
            snake_body.insert(len(snake_body), new_element)
    elif end_direction == "up":
        for j in range(0, num_segments):
            new_element = [snake_body[len(snake_body) - 1][0], snake_body[len(snake_body) - 1][1] - 10]
            snake_body.insert(len(snake_body), new_element)
    elif end_direction == "down":
        for j in range(0, num_segments):
            new_element = [snake_body[len(snake_body) - 1][0], snake_body[len(snake_body) - 1][1] + 10]
            snake_body.insert(len(snake_body), new_element)


def get_food(_has_magnet):
    global score
    food = False
    for i in range(0, len(food_positions)):
        if snake_position[0] == food_positions[i][0] and snake_position[1] == food_positions[i][1]:
            adjust_score(1)
            generate_new_food(i)
            food = True
            break
        # Mit Magnet zusätzlich auf zur snake_position benachbartes Food prüfen (auch diagonal)
        if _has_magnet:
            if ((snake_position[0] - 10 == food_positions[i][0] and snake_position[1] - 10 == food_positions[i][1]) or
                    (snake_position[0] - 0 == food_positions[i][0] and snake_position[1] - 10 == food_positions[i][
                        1]) or
                    (snake_position[0] + 10 == food_positions[i][0] and snake_position[1] - 10 == food_positions[i][
                        1]) or
                    (snake_position[0] - 10 == food_positions[i][0] and snake_position[1] - 0 == food_positions[i][
                        1]) or
                    (snake_position[0] + 10 == food_positions[i][0] and snake_position[1] - 0 == food_positions[i][
                        1]) or
                    (snake_position[0] - 10 == food_positions[i][0] and snake_position[1] + 10 == food_positions[i][
                        1]) or
                    (snake_position[0] - 0 == food_positions[i][0] and snake_position[1] + 10 == food_positions[i][
                        1]) or
                    (snake_position[0] + 10 == food_positions[i][0] and snake_position[1] + 10 == food_positions[i][
                        1])):
                adjust_score(1)
                generate_new_food(i)
                food = True
                break
    # 5-Punkte-Food
    for i in range(0, len(food_5_positions)):
        if snake_position[0] == food_5_positions[i][0] and snake_position[1] == food_5_positions[i][1]:
            adjust_score(5)
            generate_new_food_5(i)
            food = True
            add_additional_snake_segments(4)
            break
        # Mit Magnet zusätzlich auf zur snake_position benachbartes Food prüfen (auch diagonal)
        if _has_magnet:
            if ((snake_position[0] - 10 == food_5_positions[i][0] and snake_position[1] - 10 == food_5_positions[i][
                1]) or
                    (snake_position[0] - 0 == food_5_positions[i][0] and snake_position[1] - 10 == food_5_positions[i][
                        1]) or
                    (snake_position[0] + 10 == food_5_positions[i][0] and snake_position[1] - 10 == food_5_positions[i][
                        1]) or
                    (snake_position[0] - 10 == food_5_positions[i][0] and snake_position[1] - 0 == food_5_positions[i][
                        1]) or
                    (snake_position[0] + 10 == food_5_positions[i][0] and snake_position[1] - 0 == food_5_positions[i][
                        1]) or
                    (snake_position[0] - 10 == food_5_positions[i][0] and snake_position[1] + 10 == food_5_positions[i][
                        1]) or
                    (snake_position[0] - 0 == food_5_positions[i][0] and snake_position[1] + 10 == food_5_positions[i][
                        1]) or
                    (snake_position[0] + 10 == food_5_positions[i][0] and snake_position[1] + 10 == food_5_positions[i][
                        1])):
                adjust_score(5)
                generate_new_food_5(i)
                food = True
                add_additional_snake_segments(4)
    if not food:
        snake_body.pop()


# Items

def use_magnet():
    global has_magnet
    has_magnet = True


def rgb_background():
    global R
    global G
    global B
    global hue

    (r, g, b) = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    R, G, B = int(255 * r), int(255 * g), int(255 * b)
    hue += 0.0005


def wall_above(wall_x, wall_y):
    if is_wall(wall_x, wall_y - 10):
        return True
    return False


def wall_below(wall_x, wall_y):
    if is_wall(wall_x, wall_y + 10):
        return True
    return False


def wall_right(wall_x, wall_y):
    if is_wall(wall_x + 10, wall_y):
        return True
    return False


def wall_left(wall_x, wall_y):
    if is_wall(wall_x - 10, wall_y):
        return True
    return False


def repaint():
    global R
    global G
    global B
    global hue

    rgb_background()

    window.fill(pygame.Color(R, G, B))

    for body in snake_body:
        pygame.draw.circle(window, pygame.Color(0, 255, 0), (body[0] - scale / 2, body[1] - scale / 2), scale / 2)
    for body in snake_body:
        pygame.draw.circle(window, pygame.Color(0, 0, 0), (body[0] - scale / 2, body[1] - scale / 2), scale / 2, 2)

    for i in range(0, len(food_positions)):
        pygame.draw.rect(window, pygame.Color(255, 0, 0),
                         pygame.Rect(food_positions[i][0] - scale + 1, food_positions[i][1] - scale + 1, scale - 2,
                                     scale - 2))
        pygame.draw.rect(window, pygame.Color(100, 0, 0),
                         pygame.Rect(food_positions[i][0] - scale + 1, food_positions[i][1] - scale + 1, scale - 2,
                                     scale - 2), 2)

    for i in range(0, len(food_5_positions)):
        pygame.draw.rect(window, pygame.Color(0, 0, 255),
                         pygame.Rect(food_5_positions[i][0] - scale, food_5_positions[i][1] - scale, scale,
                                     scale))
        pygame.draw.rect(window, pygame.Color(100, 0, 0),
                         pygame.Rect(food_5_positions[i][0] - scale, food_5_positions[i][1] - scale, scale,
                                     scale), 2)

    for i in range(0, len(wall_positions)):
        pygame.draw.rect(window, pygame.Color(141, 141, 141),
                         pygame.Rect(wall_positions[i][0] - scale, wall_positions[i][1] - scale, scale, scale))  # Farbe
        # prüfe, ob oben/links/rechts/unten von der Mauer keine weitere Mauer ist; Wenn keine Mauer, dann setze entsprechende Linie zu dieser Richtung
        if not wall_right(wall_positions[i][0], wall_positions[i][1]):
            pygame.draw.line(window, pygame.Color(0, 0, 0), [wall_positions[i][0], wall_positions[i][1] - 1],
                             [wall_positions[i][0], wall_positions[i][1] - 10], 1)  # Rand rechts
        if not wall_left(wall_positions[i][0], wall_positions[i][1]):
            pygame.draw.line(window, pygame.Color(0, 0, 0), [wall_positions[i][0] - 11, wall_positions[i][1] - 1],
                             [wall_positions[i][0] - 11, wall_positions[i][1] - 10], 1)  # Rand links
        if not wall_above(wall_positions[i][0], wall_positions[i][1]):
            pygame.draw.line(window, pygame.Color(0, 0, 0), [wall_positions[i][0] - 1, wall_positions[i][1] - 11],
                             [wall_positions[i][0] - 10, wall_positions[i][1] - 11], 1)  # Rand oben
        if not wall_below(wall_positions[i][0], wall_positions[i][1]):
            pygame.draw.line(window, pygame.Color(0, 0, 0), [wall_positions[i][0], wall_positions[i][1]],
                             [wall_positions[i][0] - 11, wall_positions[i][1]], 1)  # Rand unten


def game_over_message():
    global score
    font = pygame.font.SysFont("Arial", scale * 3)
    render = font.render(f"Score: {score}", True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    rect.midtop = (window_width / 2, window_height / 2)
    window.blit(render, rect)
    pygame.display.flip()


def game_over():
    # Schlange gerät ausserhalb des Spielfeldes
    if snake_position[0] < 0 or snake_position[0] > window_width:
        game_over_message()
        return True
    if snake_position[1] < 0 or snake_position[1] > window_height:
        game_over_message()
        return True
    # Schlange berührt sich selbst
    for blob in snake_body[1:]:
        if snake_position[0] == blob[0] and snake_position[1] == blob[1]:
            game_over_message()
            return True
    # Schlange berührt Wand
    for wall in wall_positions:
        if snake_position[0] == wall[0] and snake_position[1] == wall[1]:
            game_over_message()
            return True
    return False


def paint_hud():
    font = pygame.font.SysFont("Arial", scale * 2)
    render = font.render(f"Score: {score}", True, pygame.Color(255, 255, 255))
    rect = render.get_rect()
    window.blit(render, rect)
    pygame.display.flip()


def game_loop():
    global direction
    direction = Direction.RIGHT
    global move_rate
    move_number = 0
    while True:
        print(move_number)
        direction = handle_keys(direction)
        # nur jeden n. Durchlauf Schlange bewegen und nach food testen
        if move_number >= move_rate:
            move_snake(direction)
            print(has_magnet)
            get_food(has_magnet)
            move_number = 0
        move_number += 1
        repaint()
        game_over()
        paint_hud()
        pygame.display.update()
        refresh_controller.tick(speed)
        if game_over():
            break


def set_speed(n):
    global speed
    speed = n


def set_move_rate(n):
    global move_rate
    move_rate = speed * 1 / n


def set_num_walls(n):
    global num_walls
    num_walls = n


def set_num_food(n):
    global num_food
    num_food = n


def set_num_food_5(n):
    global num_food_5
    num_food_5 = n


if __name__ == "__main__":
    # Einstellungen (im Code ändern)
    set_speed(60)  # fps
    set_move_rate(20)  # Anzahl Bewegungen der Schlange pro Sekunde
    set_num_walls(100)
    set_num_food(10)
    set_num_food_5(2)

    # custom Map
    custom_map = Map1  # vordefinierte Karte wird benutzt (sonst None eingeben)
    xy_0 = None
    xy_1 = None
    xyb = None

    if custom_map is not None:
        xy_0 = custom_map.map1_snake_position[0]
        xy_1 = custom_map.map1_snake_position[1]
        xyb_00 = custom_map.map1_snake_body[0][0]
        xyb_01 = custom_map.map1_snake_body[0][1]
        xyb_10 = custom_map.map1_snake_body[1][0]
        xyb_11 = custom_map.map1_snake_body[1][1]
        xyb_20 = custom_map.map1_snake_body[2][0]
        xyb_21 = custom_map.map1_snake_body[2][1]
        snake_start_walls = custom_map.map1
        generate_snake([xy_0, xy_1], [[xyb_00, xyb_01], [xyb_10, xyb_11], [xyb_20, xyb_21]])
        generate_walls(snake_start_walls)
    else:
        generate_snake([300, 300], [[300, 300], [290, 300], [280, 300]])
        generate_walls()
    generate_food()

    running = True
    while running:
        game_loop()
        # Neues Spiel
        adjust_score(score * -1)
        reset_game()
        if custom_map:
            generate_snake([xy_0, xy_1], [[xyb_00, xyb_01], [xyb_10, xyb_11], [xyb_20, xyb_21]])
            generate_walls(snake_start_walls)
