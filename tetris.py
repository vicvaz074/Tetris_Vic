import sys
import pygame
import random
import cv2
import numpy as np

# Configuración de pantalla
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (128, 128, 128)
WHITE = (255, 255, 255)
FPS = 60
MENU_BACKGROUND_SPEED = 0.01

# Tetriminos
SHAPES = [
    [
        [1, 1, 1],
        [0, 1, 0],
    ],
    [
        [0, 1, 1],
        [1, 1, 0],
    ],
    [
        [1, 1, 0],
        [0, 1, 1],
    ],
    [
        [1, 1],
        [1, 1],

    ],
    [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ],
    [
        [1, 0, 0],
        [1, 1, 1],
    ],
    [
        [0, 0, 1],
        [1, 1, 1],
    ],
]

# Colores
COLORS = [
    (255, 0, 0),
    (255, 127, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 0, 255),
    (75, 0, 130),
    (148, 0, 211),
]

# Variables de estado
game_state = "menu"  # Agregado
max_score = 0  # Agregado

class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color, (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0
        )
        pygame.draw.rect(
            surface,
            (255, 255, 255),
            (self.x * GRID_SIZE, self.y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
            1,
        )

class Tetrimino:
    def __init__(self, x, y, shape_index):
        self.x = x
        self.y = y
        self.shape = SHAPES[shape_index]
        self.color = COLORS[shape_index]

    def get_blocks(self):
        blocks = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    block_x = self.x + x
                    block_y = self.y + y
                    blocks.append(Block(block_x, block_y, self.color))
        return blocks
    
    def move_down(self):
        self.y += 1 

    def rotate(self):
        self.shape = list(zip(*reversed(self.shape)))

def draw_falling_tetriminos(surface, speed_factor=1):
    tetrimino_count = int(20 * speed_factor)
    tetriminos = []
    
    for _ in range(tetrimino_count):
        shape_index = random.randint(0, len(SHAPES) - 1)
        x = random.randint(0, SCREEN_WIDTH // GRID_SIZE)
        y = -random.randint(1, SCREEN_HEIGHT // GRID_SIZE)
        tetriminos.append(Tetrimino(x, y, shape_index))

    for tetrimino in tetriminos:
        for block in tetrimino.get_blocks():
            block.draw(surface)
        tetrimino.move_down()

class FallingTetrimino:
    def __init__(self, x, y, shape_index, speed):
        self.x = x
        self.y = y
        self.shape = SHAPES[shape_index]
        self.color = COLORS[shape_index]
        self.speed = speed

    def get_blocks(self):
        blocks = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    block_x = self.x + x
                    block_y = self.y + y
                    blocks.append(Block(block_x, block_y, self.color))
        return blocks

    def update(self):
        self.y += self.speed
        if self.y * GRID_SIZE >= SCREEN_HEIGHT:
            self.y = -len(self.shape)

falling_tetriminos = [FallingTetrimino(random.randint(0, SCREEN_WIDTH // GRID_SIZE), random.randint(0, SCREEN_HEIGHT // GRID_SIZE), random.randint(0, len(SHAPES) - 1), MENU_BACKGROUND_SPEED) for _ in range(20)]  # Pasar "MENU_BACKGROUND_SPEED" al constructor

def generate_non_overlapping_tetriminos(num_tetriminos, speed):
    tetriminos = []
    for _ in range(num_tetriminos):
        shape_index = random.randint(0, len(SHAPES) - 1)
        x = random.randint(0, SCREEN_WIDTH // GRID_SIZE)
        y = -random.randint(1, SCREEN_HEIGHT // GRID_SIZE)
        new_tetrimino = FallingTetrimino(x, y, shape_index, speed)
        
        while any(tetrimino_collision(new_tetrimino, tetrimino) for tetrimino in tetriminos):
            x = random.randint(0, SCREEN_WIDTH // GRID_SIZE)
            y = -random.randint(1, SCREEN_HEIGHT // GRID_SIZE)
            new_tetrimino.x = x
            new_tetrimino.y = y
        
        tetriminos.append(new_tetrimino)
    
    return tetriminos

def tetrimino_collision(t1, t2):
    for block1 in t1.get_blocks():
        for block2 in t2.get_blocks():
            if block1.x == block2.x and block1.y == block2.y:
                return True
    return False

falling_tetriminos = generate_non_overlapping_tetriminos(20, MENU_BACKGROUND_SPEED)

def draw_background(speed_factor=1):
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for tetrimino in falling_tetriminos:
        tetrimino.speed = speed_factor  # Establecer la velocidad de cada tetrimino en función del factor de velocidad
        tetrimino.update()
        
        while any(tetrimino_collision(tetrimino, other) for other in falling_tetriminos if tetrimino != other):
            tetrimino.y -= 1
        
        for block in tetrimino.get_blocks():
            block.color = tetrimino.color
            block.draw(surface)
    return surface
    

def generate_star_positions(num_stars=50):
    star_positions = []
    for _ in range(num_stars):
        x = random.randint(0, SCREEN_WIDTH - 1)
        y = random.randint(0, SCREEN_HEIGHT - 1)
        star_positions.append((x, y))
    return star_positions

def draw_stars(screen, star_positions):
    for x, y in star_positions:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, 2, 2))

star_positions = generate_star_positions()


def create_board(width, height):
    return [[None for _ in range(width)] for _ in range(height)]

def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

def draw_board(board, surface):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                Block(x, y, cell).draw(surface)

def check_collision(tetrimino, board):
    for block in tetrimino.get_blocks():
        if block.x < 0 or block.x >= len(board[0]) or block.y >= len(board):
            return True
        if block.y >= 0 and board[block.y][block.x]:
            return True
    return False

def merge_tetrimino(tetrimino, board):
    for block in tetrimino.get_blocks():
        board[block.y][block.x] = block.color

def clear_lines(board):
    lines_cleared = 0
    for i, row in enumerate(board):
        if all(cell for cell in row):
            del board[i]
            board.insert(0, [None for _ in range(len(board[0]))])
            lines_cleared += 1
    return lines_cleared

def game_over(board):
    return any(cell for cell in board[0])

def blur_surface(surface, blur_size):
    np_surface = pygame.surfarray.array3d(surface)
    np_surface = cv2.blur(np_surface, (blur_size, blur_size))
    return pygame.surfarray.make_surface(np_surface)

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def draw_menu(screen, max_score):
    background = draw_background(MENU_BACKGROUND_SPEED)  # Modificado
    screen.blit(background, (0, 0))
    # Resto del código sin cambios
    draw_text(screen, "Tetris", 60, 90, 150)
    draw_text(screen, "Presiona espacio para empezar", 20, 50, 250)
    draw_text(screen, f"Máximo puntaje: {max_score}", 20, 90, 300)
    draw_text(screen, "Hecho por Vic", 20, 100, 550)
    pygame.display.flip()

def main():
    global game_state, max_score
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    board_width = 10
    board_height = 20
    board = create_board(board_width, board_height)
    falling_tetriminos_timer = pygame.time.get_ticks()

    background = draw_background(MENU_BACKGROUND_SPEED)

    while True:
        if game_state == "menu":
            draw_menu(screen, max_score)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "game"
                        board = create_board(board_width, board_height)
                        score = 0
                        game_speed = 500
                        game_timer = pygame.time.get_ticks()
                        tetrimino = Tetrimino(board_width // 2 - 2, 0, random.randint(0, len(SHAPES) - 1))
                        drop_speed_multiplier = 1

        elif game_state == "game":
            screen.fill(BACKGROUND_COLOR)
            draw_grid(screen)
            draw_board(board, screen)

            for block in tetrimino.get_blocks():
                block.draw(screen)

            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        tetrimino.x -= 1
                        if check_collision(tetrimino, board):
                            tetrimino.x += 1
                    elif event.key == pygame.K_RIGHT:
                        tetrimino.x += 1
                        if check_collision(tetrimino, board):
                            tetrimino.x -= 1
                    elif event.key == pygame.K_UP:
                        tetrimino.rotate()
                        if check_collision(tetrimino, board):
                            for _ in range(3):
                                tetrimino.rotate()
            if keys[pygame.K_DOWN]:
                drop_speed_multiplier = 10
            else:
                drop_speed_multiplier = 1

            current_time = pygame.time.get_ticks()
            if current_time - game_timer > game_speed / drop_speed_multiplier:
                tetrimino.y += 1
                if check_collision(tetrimino, board):
                    tetrimino.y -= 1
                    merge_tetrimino(tetrimino, board)
                    score += clear_lines(board)
                    if game_over(board):
                        game_state = "game_over"
                        if score > max_score:
                            max_score = score
                    else:
                        tetrimino = Tetrimino(board_width // 2 - 2, 0, random.randint(0, len(SHAPES) - 1))
                game_timer = current_time

            draw_text(screen, f"Puntuación: {score}", 20, 5, 5)
            pygame.display.flip()
            clock.tick(FPS)

        elif game_state == "game_over":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))

            # Dibuja las estrellas en el fondo
            # Dibuja las estrellas en el fondo
            draw_stars(overlay, star_positions)



            draw_text(overlay, "Game Over", 60, 40, 200)
            draw_text(overlay, "Presiona espacio para jugar de nuevo", 20, 30, 300)
            draw_text(overlay, "Presiona M para volver al menú", 20, 50, 350)
            draw_text(overlay, f"Máxima puntuación: {max_score}", 20, 80, 400)

            current_time = pygame.time.get_ticks()
            if current_time - falling_tetriminos_timer > 2000 / MENU_BACKGROUND_SPEED:  # Ajustar el valor 2000 según la velocidad deseada
                falling_tetriminos_timer = current_time
                background = draw_background(MENU_BACKGROUND_SPEED)
            screen.blit(background, (0, 0))
            screen.blit(overlay, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_state = "game"
                        board = create_board(board_width, board_height)
                        score = 0
                        game_speed = 500
                        game_timer = pygame.time.get_ticks()
                        tetrimino = Tetrimino(board_width // 2 - 2, 0, random.randint(0, len(SHAPES) - 1))
                        drop_speed_multiplier = 1
                    elif event.key == pygame.K_m:
                        game_state = "menu"

if __name__ == "__main__":
    main()