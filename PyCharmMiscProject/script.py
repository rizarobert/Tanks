import pygame
import math
import random
import sys
pygame.init()
move_sound = pygame.mixer.Sound('move.wav')
shoot_sound = pygame.mixer.Sound('shoot.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tanks Game")
clock = pygame.time.Clock()
try:
    TITLE_FONT = pygame.font.Font("freesansbold.ttf", 36)
    HEADER_FONT = pygame.font.Font("freesansbold.ttf", 28)
    UI_FONT = pygame.font.Font(None, 24)
    SMALL_FONT = pygame.font.Font(None, 20)
    LARGE_FONT = pygame.font.Font("freesansbold.ttf", 48)
except:
    TITLE_FONT = pygame.font.SysFont("impact", 36)
    HEADER_FONT = pygame.font.SysFont("impact", 28)
    UI_FONT = pygame.font.SysFont("arial", 24)
    SMALL_FONT = pygame.font.SysFont("arial", 20)
    LARGE_FONT = pygame.font.SysFont("impact", 48)

GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
GREY = (100, 100, 100)
SKY = (135, 206, 235)
YELLOW = (255, 255, 0)
HIGHLIGHT = (200, 200, 255)
ORANGE = (255, 165, 0)


def generate_terrain(width, min_height=300, max_height=450, num_hills=8):
    base = (min_height + max_height) // 2
    control_points = [random.randint(min_height, max_height) for _ in range(num_hills)]
    control_points[0] = control_points[-1] = base
    step = width // (num_hills - 1)
    x_points = [i * step for i in range(num_hills)]

    terrain = []
    for x in range(width):
        for i in range(1, num_hills):
            if x < x_points[i]:
                seg = i - 1
                break
        x0, x1 = x_points[seg], x_points[seg + 1]
        y0, y1 = control_points[seg], control_points[seg + 1]
        t = (x - x0) / (x1 - x0)
        t_smooth = t * t * (3 - 2 * t)
        height = y0 + t_smooth * (y1 - y0)
        variation = 10 * math.sin(0.05 * x) + 5 * math.sin(0.1 * x + 3)
        terrain.append(int(height + variation))
    return terrain


terrain = generate_terrain(WIDTH)


class Tank:
    def __init__(self, x, color, name=""):
        self.x = x
        self.color = color
        self.name = name
        self.angle = 45 if x < WIDTH // 2 else 135
        self.power = 50
        self.hp = 100
        self.fuel = 100
        self.projectile_type = 0
        self.ammo = {1: 3, 2: 2, 3: 1}
        self.update_y()

    def update_y(self):
        self.y = terrain[self.x] - 15

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x - 15, self.y - 8, 30, 12))
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)
        rad = math.radians(self.angle)
        end_x = self.x + math.cos(rad) * 25
        end_y = self.y - math.sin(rad) * 25
        pygame.draw.line(screen, BLACK, (self.x, self.y), (end_x, end_y), 4)
        pygame.draw.rect(screen, GREY, (self.x - 18, self.y + 5, 36, 8))
        for i in range(3):
            pygame.draw.rect(screen, DARK_BROWN, (self.x - 15 + i * 12, self.y + 7, 6, 4))

    def move(self, direction):
        if self.fuel <= 0:
            return False
        step = 3 * direction
        new_x = self.x + step
        if 20 < new_x < WIDTH - 20:
            for check_x in range(min(self.x, new_x), max(self.x, new_x) + 1):
                if terrain[check_x] > self.y + 20:
                    return False
            self.x = new_x
            self.update_y()
            self.fuel -= abs(step)
            move_sound.play()
            return True
        return False


def draw_terrain():
    pts = [(x, terrain[x]) for x in range(WIDTH)]
    pts.append((WIDTH - 1, HEIGHT))
    pts.append((0, HEIGHT))
    pygame.draw.polygon(screen, BROWN, pts)
    for x in range(0, WIDTH, 4):
        pygame.draw.line(screen, DARK_BROWN, (x, terrain[x] - random.randint(0, 3)), (x, terrain[x]))


def create_crater(x_center, radius=25, depth=15):
    for x in range(max(0, x_center - radius), min(WIDTH, x_center + radius)):
        dx = x - x_center
        if abs(dx) < radius:
            crater_depth = depth * (1 - (dx / radius) ** 2)
            terrain[x] = min(HEIGHT, terrain[x] + int(crater_depth))


def update_tank_positions():
    tank1.update_y()
    tank2.update_y()


def draw_power_bar(x, y, w, h, p):
    pygame.draw.rect(screen, GREY, (x, y, w, h), 2)
    pygame.draw.rect(screen, RED, (x, y, p * w / 100, h))
    screen.blit(UI_FONT.render(f"Power: {p}%", True, BLACK), (x, y + h + 5))


def draw_angle_indicator(x, y, angle):
    screen.blit(UI_FONT.render(f"Angle: {angle}°", True, BLACK), (x, y))


def draw_health_bar(x, y, w, h, hp):
    pygame.draw.rect(screen, GREY, (x, y, w, h), 2)
    pygame.draw.rect(screen, GREEN, (x, y, hp * w / 100, h))
    screen.blit(UI_FONT.render(f"HP: {hp}", True, BLACK), (x, y + h + 5))


def draw_fuel_bar(x, y, w, h, f):
    pygame.draw.rect(screen, GREY, (x, y, w, h), 2)
    pygame.draw.rect(screen, YELLOW, (x, y, f * w / 100, h))
    screen.blit(UI_FONT.render(f"Fuel: {f}", True, BLACK), (x, y + h + 5))


def draw_ui(t1, t2, current):
    draw_power_bar(WIDTH // 2 - 100, 20, 200, 20, current.power)
    draw_angle_indicator(WIDTH // 2 - 50, 65, current.angle)
    proj = ["Standard", "Homing", "Mega Bomb"]
    screen.blit(UI_FONT.render(f"Projectile: {proj[current.projectile_type]}", True, BLACK), (WIDTH // 2 - 80, 85))
    if current.projectile_type > 0:
        screen.blit(UI_FONT.render(f"Ammo left: {current.ammo.get(current.projectile_type, 0)}", True, BLACK),
                    (WIDTH // 2 - 80, 105))
    draw_health_bar(20, 10, 150, 20, t1.hp)
    draw_fuel_bar(20, 60, 150, 20, t1.fuel)
    screen.blit(UI_FONT.render(t1.name, True, RED), (20, 105))
    draw_health_bar(WIDTH - 170, 10, 150, 20, t2.hp)
    draw_fuel_bar(WIDTH - 170, 60, 150, 20, t2.fuel)
    screen.blit(UI_FONT.render(t2.name, True, GREEN), (WIDTH - 170, 105))

    turn_text = UI_FONT.render(f"{current.name}'s turn", True, BLACK)
    pygame.draw.rect(screen, HIGHLIGHT, (WIDTH // 2 - 80, HEIGHT - 40, 160, 30))
    screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, HEIGHT - 35))


def fire_projectile(shooter, target):
    shoot_sound.play()
    rad = math.radians(shooter.angle)
    vx = math.cos(rad) * shooter.power / 5
    vy = -math.sin(rad) * shooter.power / 5
    x, y = shooter.x, shooter.y
    gravity = 0.3


    if shooter.projectile_type == 0:
        color = BLACK
        size = 5
        trail_color = (100, 100, 100)
    elif shooter.projectile_type == 1:
        color = YELLOW
        size = 7
        trail_color = (255, 255, 100)
    else:
        color = RED
        size = 10
        trail_color = (255, 50, 50)

    trail = []
    max_trail_length = 100
    explosion_particles = []
    hit = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if shooter.projectile_type == 1 and not hit:  # Homing missile
            dx = target.x - x
            dy = target.y - y
            dist = max(math.hypot(dx, dy), 1)
            vx += dx / dist * 0.2
            vy += dy / dist * 0.2

        vx *= 0.99
        vy += gravity
        x += vx
        y += vy

        trail.append((int(x), int(y)))
        if len(trail) > max_trail_length:
            trail.pop(0)

        if not (0 <= int(x) < WIDTH and 0 <= int(y) < HEIGHT):
            break

        collision = y >= terrain[int(x)] or math.hypot(target.x - x, target.y - y) < 20
        if collision and not hit:
            hit = True
            explosion_sound.play()

            for _ in range(50):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 10)
                lifetime = random.randint(20, 40)
                explosion_particles.append({
                    'x': x,
                    'y': y,
                    'vx': math.cos(angle) * speed,
                    'vy': math.sin(angle) * speed,
                    'color': (
                        random.randint(200, 255),
                        random.randint(100, 200),
                        random.randint(0, 100)
                    ),
                    'size': random.randint(2, 5),
                    'lifetime': lifetime
                })

            if shooter.projectile_type == 2:  # Mega Bomb
                create_crater(int(x), 40, 30)
            elif shooter.projectile_type == 1:  # Homing missile
                create_crater(int(x), 30, 20)
            else:  # Standard projectile
                create_crater(int(x), 25, 15)
            update_tank_positions()

            d = math.hypot(target.x - x, target.y - y)
            if d < 50:
                if shooter.projectile_type == 1:  # Homing missile
                    dmg = (50 - d) * 0.5
                elif shooter.projectile_type == 2:  # Mega Bomb
                    dmg = (50 - d) * 2.0
                else:  # Standard projectile
                    dmg = (50 - d) * 1.0
                target.hp -= int(dmg)
        for particle in explosion_particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.1
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                explosion_particles.remove(particle)

        screen.fill(SKY)
        draw_terrain()
        tank1.draw()
        tank2.draw()


        if not hit:
            for i, (tx, ty) in enumerate(trail):
                alpha = int(200 * i / len(trail))
                if shooter.projectile_type == 0:
                    pygame.draw.circle(screen, (*trail_color, alpha), (tx, ty), size * i / len(trail))
                else:
                    pygame.draw.circle(screen, trail_color, (tx, ty), size * i / len(trail))


            pygame.draw.circle(screen, color, (int(x), int(y)), size)


            if shooter.projectile_type == 1 and random.random() < 0.3:  # Scânteie
                spark_x = x + random.uniform(-5, 5)
                spark_y = y + random.uniform(-5, 5)
                pygame.draw.circle(screen, (255, 255, 150), (int(spark_x), int(spark_y)), 2)
            elif shooter.projectile_type == 2:  # Fum Mega Bomb
                if random.random() < 0.5:
                    smoke_x = x + random.uniform(-8, 8)
                    smoke_y = y + random.uniform(-8, 8)
                    pygame.draw.circle(screen, (100, 100, 100, 150), (int(smoke_x), int(smoke_y)),
                                       random.randint(3, 7))


        for particle in explosion_particles:
            pygame.draw.circle(
                screen,
                particle['color'],
                (int(particle['x']), int(particle['y'])),
                particle['size']
            )

        draw_ui(tank1, tank2, shooter)
        pygame.display.update()
        clock.tick(60)

        if hit and len(explosion_particles) == 0:
            break



player1_name = ""
player2_name = ""
input_active = 0
name_input_mode = True
input_rect1 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 40)
input_rect2 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 10, 300, 40)

while name_input_mode:
    screen.fill(SKY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if input_active == 0:
                    input_active = 1
                else:
                    name_input_mode = False
            elif event.key == pygame.K_BACKSPACE:
                if input_active == 0:
                    player1_name = player1_name[:-1]
                else:
                    player2_name = player2_name[:-1]
            else:
                if input_active == 0 and len(player1_name) < 15:
                    player1_name += event.unicode
                elif input_active == 1 and len(player2_name) < 15:
                    player2_name += event.unicode

    title = TITLE_FONT.render("ENTER PLAYER NAMES", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    pygame.draw.rect(screen, HIGHLIGHT if input_active == 0 else WHITE, input_rect1)
    pygame.draw.rect(screen, RED if input_active == 0 else GREY, input_rect1, 3)
    pygame.draw.rect(screen, HIGHLIGHT if input_active == 1 else WHITE, input_rect2)
    pygame.draw.rect(screen, GREEN if input_active == 1 else GREY, input_rect2, 3)
    screen.blit(HEADER_FONT.render(player1_name, True, BLACK), (input_rect1.x + 10, input_rect1.y + 5))
    screen.blit(HEADER_FONT.render(player2_name, True, BLACK), (input_rect2.x + 10, input_rect2.y + 5))
    screen.blit(UI_FONT.render("Player 1:", True, RED), (input_rect1.x - 100, input_rect1.y + 10))
    screen.blit(UI_FONT.render("Player 2:", True, GREEN), (input_rect2.x - 100, input_rect2.y + 10))
    screen.blit(UI_FONT.render("Press ENTER to confirm and start game", True, BLACK),
                (WIDTH // 2 - 200, HEIGHT - 50))
    pygame.display.flip()
    clock.tick(60)


show_instructions = True
instructions = [
    ("GAME INSTRUCTIONS", HEADER_FONT),
    ("", SMALL_FONT),
    ("Objective:", UI_FONT),
    ("- Destroy the opponent's tank", SMALL_FONT),
    ("- Adjust angle and power to shoot", SMALL_FONT),
    ("", SMALL_FONT),
    ("Controls:", UI_FONT),
    ("A/D - Move tank left/right", SMALL_FONT),
    ("Up/Down - Adjust cannon angle", SMALL_FONT),
    ("Left/Right - Adjust shot power", SMALL_FONT),
    ("1/2/3 - Change projectile type", SMALL_FONT),
    ("SPACE - Fire", SMALL_FONT),
    ("", SMALL_FONT),
    ("After game:", UI_FONT),
    ("R - Restart game", SMALL_FONT),
    ("Q - Quit game", SMALL_FONT),
    ("", SMALL_FONT),
    ("Press ENTER to start...", UI_FONT)
]

while show_instructions:
    screen.fill(SKY)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                show_instructions = False

    y_offset = 50
    for line, font in instructions:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y_offset))
        y_offset += 30 if font == SMALL_FONT else 35

    pygame.display.flip()
    clock.tick(60)


tank1 = Tank(100, RED, player1_name)
tank2 = Tank(WIDTH - 100, GREEN, player2_name)
turn = 0
game_over = False
winner = None
winner_color = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over and event.type == pygame.KEYDOWN:
            current = tank1 if turn == 0 else tank2
            if event.key == pygame.K_1:
                current.projectile_type = 0
            elif event.key == pygame.K_2:
                if current.ammo.get(1, 0) > 0:
                    current.projectile_type = 1
            elif event.key == pygame.K_3:
                if current.ammo.get(2, 0) > 0:
                    current.projectile_type = 2
            elif event.key == pygame.K_SPACE:
                if current.projectile_type == 0 or current.ammo.get(current.projectile_type, 0) > 0:
                    fire_projectile(current, tank2 if turn == 0 else tank1)
                    if current.projectile_type > 0:
                        current.ammo[current.projectile_type] -= 1
                    turn = 1 - turn
                    tank1.fuel = tank2.fuel = 100

    if not game_over:
        current = tank1 if turn == 0 else tank2
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: current.angle = min(180, current.angle + 1)
        if keys[pygame.K_DOWN]: current.angle = max(0, current.angle - 1)
        if keys[pygame.K_RIGHT]: current.power = min(100, current.power + 1)
        if keys[pygame.K_LEFT]: current.power = max(10, current.power - 1)
        if keys[pygame.K_a]: current.move(-1)
        if keys[pygame.K_d]: current.move(1)

        if tank1.hp <= 0 or tank2.hp <= 0:
            game_over = True
            if tank1.hp <= 0:
                winner, winner_color = tank2.name, GREEN
            else:
                winner, winner_color = tank1.name, RED


    screen.fill(SKY)
    draw_terrain()
    tank1.draw()
    tank2.draw()
    draw_ui(tank1, tank2, tank1 if turn == 0 else tank2)


    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        win_text = LARGE_FONT.render(f"{winner} WINS!", True, winner_color)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 50))
        restart_text = HEADER_FONT.render("Press R to restart or Q to quit", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            terrain = generate_terrain(WIDTH)
            tank1 = Tank(100, RED, player1_name)
            tank2 = Tank(WIDTH - 100, GREEN, player2_name)
            turn = 0
            game_over = False
            winner = None
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)