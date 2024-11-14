import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 700
TILE_SIZE = 50
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Heart of Truth")

# 플레이어 설정
player_pos = [1, 12] 
player_images = {
    "up": pygame.image.load("up.png"),
    "down": pygame.image.load("down.png"),
    "left": pygame.image.load("left.png"),
    "right": pygame.image.load("right.png"),
}
current_image = player_images["up"]

# 타일 맵 정의 (0: 빈 칸, 1: 벽)
level_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# 방향키 설정
MOVE_KEYS = {
    pygame.K_LEFT: (-1, 0, "left"),
    pygame.K_RIGHT: (1, 0, "right"),
    pygame.K_UP: (0, -1, "up"),
    pygame.K_DOWN: (0, 1, "down")
}
#맵 설정
def draw_map():
    for y, row in enumerate(level_map):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == 1:
                pygame.draw.rect(screen, GRAY, rect)
#캐릭터 움직임관련
def move_player(dx, dy, direction):
    global player_pos, current_image
    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    if 0 <= new_x < len(level_map[0]) and 0 <= new_y < len(level_map) and level_map[new_y][new_x] != 1:
        player_pos = [new_x, new_y] 
    current_image = player_images[direction] 
#메인 동작함수
running = True
while running:
    screen.fill(WHITE)
    draw_map()
    screen.blit(current_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in MOVE_KEYS:
                dx, dy, direction = MOVE_KEYS[event.key]
                move_player(dx, dy, direction)
                
    pygame.display.flip()
pygame.quit()
