import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TILE_SIZE = 50

def main():
    pygame.init()
    pygame.display.set_caption("Heart of Truth")
    screen = pygame.display.set_mode((1200, 700))
    clock = pygame.time.Clock()

    # 폰트 설정
    font = pygame.font.Font(None, 36)

    # 플레이어 설정
    player_pos = [1, 1]  # 플레이어 시작 위치
    initial_player_pos = player_pos[:]
    player_images = {
        "up": pygame.image.load("1up.png"),
        "down": pygame.image.load("down.png"),
        "left": pygame.image.load("left.png"),
        "right": pygame.image.load("right.png"),
    }
    current_image = player_images["down"]

    # 0: 움직일수있는 공간 1: 벽(이동x) 2:움직일수있는벽 3: 파괴가능한벽
    level_map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    # 움직이는 벽(2)와 파괴 가능한 벽(3) 위치 추적
    movable_walls = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 2]
    destructible_walls = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 3]

    # 초기 상태 저장
    initial_movable_walls = movable_walls[:]
    initial_destructible_walls = destructible_walls[:]
    initial_level_map = [row[:] for row in level_map]

    break_count = 0
    break_limit = 100

    # 타일 이미지 설정
    wall_image = pygame.image.load("1wall.png")
    wall_image = pygame.transform.scale(wall_image, (TILE_SIZE, TILE_SIZE))

    obstacle_image = pygame.image.load("removewall.png")
    obstacle_image = pygame.transform.scale(obstacle_image, (TILE_SIZE, TILE_SIZE))

    movable_wall_image = pygame.image.load("movewall.png")
    movable_wall_image = pygame.transform.scale(movable_wall_image, (TILE_SIZE, TILE_SIZE))

    goal_image = pygame.image.load("end.png")
    goal_image = pygame.transform.scale(goal_image, (TILE_SIZE, TILE_SIZE))

    # 몬스터 이미지 설정
    monster_images = {
        "monster1": pygame.image.load("monster.png"),
        "monster2": pygame.image.load("monster.png"),
        "monster3": pygame.image.load("monster.png")
    }
    # 이미지 크기 조정
    for key in monster_images:
        monster_images[key] = pygame.transform.scale(monster_images[key], (TILE_SIZE, TILE_SIZE))

    # 방향키 설정
    MOVE_KEYS = {
        pygame.K_LEFT: (-1, 0, "left"),
        pygame.K_RIGHT: (1, 0, "right"),
        pygame.K_UP: (0, -1, "up"),
        pygame.K_DOWN: (0, 1, "down")
    }
    
    # 몬스터 설정
    monsters = [
        {
            "current_pos": [0, 0],
            "direction": 1,
            "move_type": "y",
            "image": "monster3",
            "move_delay": 300,  # 이동 속도
            "last_move_time": pygame.time.get_ticks()
        },
        {
            "current_pos": [0, 0],
            "direction": -1,
            "move_type": "x",
            "image": "monster1",
            "move_delay": 500,
            "last_move_time": pygame.time.get_ticks()
        },
        {
            "current_pos": [0, 0],
            "direction": -1,
            "move_type": "y",
            "image": "monster2",
            "move_delay": 700,
            "last_move_time": pygame.time.get_ticks()
        }
    ]

    death_count = 0  # 플레이어 사망 횟수

    offset_y = 50 

    def draw_map():
        for y, row in enumerate(level_map):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + offset_y, TILE_SIZE, TILE_SIZE)
                if tile == 1:
                    screen.blit(wall_image, rect.topleft)
                elif tile == 3 and [x, y] in destructible_walls:
                    screen.blit(obstacle_image, rect.topleft)
                elif tile == 2 and [x, y] in movable_walls:
                    screen.blit(movable_wall_image, rect.topleft)
                elif tile == 4:
                    screen.blit(goal_image, rect.topleft)
        # 몬스터 그리기
        for monster in monsters:
            monster_image = monster_images[monster["image"]]
            screen.blit(monster_image, (monster["current_pos"][0] * TILE_SIZE, monster["current_pos"][1] * TILE_SIZE + offset_y))

    def move_monsters():
        current_time = pygame.time.get_ticks()
        for monster in monsters:
            if current_time - monster["last_move_time"] >= monster["move_delay"]:
                current_x, current_y = monster["current_pos"]
                direction = monster["direction"]
                move_type = monster["move_type"]

                # 가로 이동
                if move_type == "x":
                    new_x = current_x + direction

                    if (
                        new_x < 0 or new_x >= len(level_map[0]) or
                        level_map[current_y][new_x] in (1, 2, 3)
                    ):
                        monster["direction"] *= -1 
                        new_x = current_x + monster["direction"]
                        if new_x < 0 or new_x >= len(level_map[0]) or level_map[current_y][new_x] in (1, 2, 3):
                            new_x = current_x
                        else:
                            monster["current_pos"][0] = new_x
                    else:
                        monster["current_pos"][0] = new_x

                # 세로 이동
                elif move_type == "y":
                    new_y = current_y + direction

                    if (
                        new_y < 0 or new_y >= len(level_map) or
                        level_map[new_y][current_x] in (1, 2, 3)
                    ):
                        monster["direction"] *= -1  
                        new_y = current_y + monster["direction"]
                        if new_y < 0 or new_y >= len(level_map) or level_map[new_y][current_x] in (1, 2, 3):
                            new_y = current_y
                        else:
                            monster["current_pos"][1] = new_y
                    else:
                        monster["current_pos"][1] = new_y

                monster["last_move_time"] = current_time  # 몬스터별 마지막 이동 시간 업데이트

    def move_player(dx, dy, direction):
        nonlocal player_pos, current_image, break_count
        new_x, new_y = player_pos[0] + dx, player_pos[1] + dy

        if 0 <= new_x < len(level_map[0]) and 0 <= new_y < len(level_map):
            # 움직이는 벽 처리 (2)
            if [new_x, new_y] in movable_walls:
                move_x, move_y = new_x + dx, new_y + dy
                if 0 <= move_x < len(level_map[0]) and 0 <= move_y < len(level_map):
                    if level_map[move_y][move_x] == 0:  # 밀려날 자리가 비어 있으면
                        movable_walls.remove([new_x, new_y])
                        movable_walls.append([move_x, move_y])
                        level_map[new_y][new_x] = 0
                        level_map[move_y][move_x] = 2
                        player_pos = [new_x, new_y]
                    else:
                        return  # 밀 수 없는 경우 이동 불가
                else:
                    return  # 맵 경계 밖으로 이동 불가

            # 파괴 가능한 벽 처리 (3)
            elif [new_x, new_y] in destructible_walls:
                if break_count < break_limit:
                    destructible_walls.remove([new_x, new_y])
                    level_map[new_y][new_x] = 0
                    break_count += 1
                    player_pos = [new_x, new_y]
                else:
                    return  # 벽 부수기 제한 초과

            # 도착지점 처리 (4)
            elif level_map[new_y][new_x] == 4:
                print("Goal Reached!")
                pygame.quit()
                sys.exit()

            # 일반 이동
            elif level_map[new_y][new_x] == 0:
                player_pos = [new_x, new_y]

        current_image = player_images[direction]

    def monster_contact():
        nonlocal death_count, player_pos
        for monster in monsters:
            if player_pos == monster["current_pos"]:
                death_count += 1
                print(f"플레이어 사망! 현재 데스 카운트: {death_count}")
                reset_player_and_walls()  # 플레이어 위치와 벽들만 초기화
                break  # 하나의 몬스터와 충돌하면 더 이상 체크하지 않음

    def reset_player_and_walls():
        nonlocal player_pos, current_image, destructible_walls, movable_walls, level_map, break_count

        # 플레이어 위치 초기화
        player_pos = initial_player_pos[:]
        current_image = player_images["down"]

        # 벽 부수기 횟수 초기화
        break_count = 0

        # 맵 초기화
        level_map = [row[:] for row in initial_level_map]

        # 파괴 가능한 벽 초기화
        destructible_walls = initial_destructible_walls[:]

        # 움직이는 벽 초기화
        movable_walls = initial_movable_walls[:]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in MOVE_KEYS:
                    dx, dy, direction = MOVE_KEYS[event.key]
                    move_player(dx, dy, direction)

        move_monsters()
        monster_contact()

        # 화면 업데이트
        screen.fill(WHITE)  # 흰색 배경으로 채우기
        draw_map()
        # 플레이어 그리기 (오프셋 적용)
        screen.blit(current_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE + offset_y))

        # 남은 벽 부수기 횟수와 데스 카운트 출력
        info_text = font.render(f"Wall Breaks: {break_limit - break_count} | Death: {death_count}", True, BLACK)
        screen.blit(info_text, (10, 10))

        pygame.display.update() 
        clock.tick(30)

if __name__ == '__main__':
    main()
