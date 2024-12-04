import pygame
import sys
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
TILE_SIZE = 50


def main():
    pygame.init()
    pygame.display.set_caption("Heart of Truth")
    screen = pygame.display.set_mode((1200, 700))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    # 플레이어 설정
    player_pos = [1, 1]
    initial_player_pos = player_pos[:]
    player_images = {
        "up": pygame.image.load("1up.png"),
        "down": pygame.image.load("down.png"),
        "left": pygame.image.load("left.png"),
        "right": pygame.image.load("right.png"),
    }
    current_image = player_images["down"]

    # 0: 움직일수있는 공간 1: 벽(이동x) 2:움직일수있는벽 3: 파괴가능한벽 4:도착지점
    #  5:포탈 6:블록 놓는 위치 7: 사라지는 블럭 9: 벽2
    level_map = [
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        [9, 0, 0, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 9, 9, 9, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 0, 9, 0, 0, 0, 0, 0, 9],
        [9, 0, 0, 9, 9, 9, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 0, 9, 0, 0, 9, 0, 0, 9],
        [9, 0, 0, 9, 9, 9, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 9],
        [9, 0, 0, 9, 9, 9, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 9],
        [9, 0, 0, 9, 9, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 0, 0, 9, 0, 0, 9],
        [9, 0, 0, 9, 9, 9, 0, 0, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 0, 0, 9, 0, 0, 9],
        [9, 0, 0, 9, 9, 9, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0, 9, 0, 0, 9],
        [9, 0, 0, 9, 9, 9, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 0, 9, 0, 0, 9, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 0, 9, 0, 0, 9, 4, 4, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 9, 4, 4, 9],
        [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
    ]

    # 움직이는 벽(2)와 파괴 가능한 벽(3) 위치 추적
    move_walls = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 2]
    destructible_walls = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 3]

    # 초기 상태 저장
    initial_move_walls = move_walls[:]
    initial_destructible_walls = destructible_walls[:]
    initial_level_map = [row[:] for row in level_map]
    # 포탈(5) 위치 저장
    portal_positions = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 5]

    # 블록(6) 놓는 위치 저장
    target_positions = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 6]

    # 사라지는 벽(7) 위치 저장
    onoff_positions = [[x, y] for y, row in enumerate(level_map) for x, tile in enumerate(row) if tile == 7]

    break_count = 0
    break_limit = 100

    # 차례대로 1번 2번 3번 4번 5번 6번 7번 이미지
    wall_image = pygame.image.load("1wall.png")
    wall_image = pygame.transform.scale(wall_image, (TILE_SIZE, TILE_SIZE))

    wall2_image = pygame.image.load("2wall.png")
    wall2_image = pygame.transform.scale(wall2_image, (TILE_SIZE, TILE_SIZE))

    removewall_image = pygame.image.load("removewall.png")
    removewall_image = pygame.transform.scale(removewall_image, (TILE_SIZE, TILE_SIZE))

    move_wall_image = pygame.image.load("movewall.png")
    move_wall_image = pygame.transform.scale(move_wall_image, (TILE_SIZE, TILE_SIZE))

    goal_image = pygame.image.load("end.png")
    goal_image = pygame.transform.scale(goal_image, (TILE_SIZE, TILE_SIZE))

    portal_img = pygame.image.load("portal.png")
    portal_img = pygame.transform.scale(portal_img, (TILE_SIZE, TILE_SIZE))

    targets_img = pygame.image.load("target.png")
    targets_img = pygame.transform.scale(targets_img, (TILE_SIZE, TILE_SIZE))

    onoffwall_img = pygame.image.load("onoffWall.png")
    onoffwall_img = pygame.transform.scale(onoffwall_img, (TILE_SIZE, TILE_SIZE))

    floor_img = pygame.image.load("1floor.png")
    floor_img = pygame.transform.scale(floor_img, (TILE_SIZE, TILE_SIZE))

    # 몬스터 이미지
    monster_images = {
        "monster1": pygame.image.load("monster.png")
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
            "current_pos": [1500, 70],
            "direction": 1,
            "move_type": "y",
            "image": "monster1",
            "move_delay": 300,
            "last_move_time": pygame.time.get_ticks()
        }
    ]

    death_count = 0  # 플레이어 사망 횟수

    offset_y = 50

    hint_button_rect = pygame.Rect(1120, 10, 100, 40)

    def draw_map():
        for y, row in enumerate(level_map):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE + offset_y, TILE_SIZE, TILE_SIZE)
                if tile == 1:
                    screen.blit(wall_image, rect.topleft)
                elif tile == 3 and [x, y] in destructible_walls:
                    screen.blit(removewall_image, rect.topleft)
                elif tile == 2 and [x, y] in move_walls:
                    screen.blit(move_wall_image, rect.topleft)
                elif tile == 4:
                    screen.blit(goal_image, rect.topleft)
                elif tile == 5:
                    screen.blit(portal_img, rect.topleft)
                elif [x, y] in target_positions:  # (6 블럭 놓는 곳)
                    screen.blit(targets_img, rect.topleft)
                elif tile == 7:
                    screen.blit(onoffwall_img, rect.topleft)
                elif tile == 9:
                    screen.blit(wall2_image, rect.topleft)
                elif tile == 0:
                    screen.blit(floor_img, rect.topleft)
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
                        level_map[current_y][new_x] in (1, 2, 3, 9)
                    ):
                        monster["direction"] *= -1
                        new_x = current_x + monster["direction"]
                        if new_x < 0 or new_x >= len(level_map[0]) or level_map[current_y][new_x] in (1, 2, 3, 9):
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
                        level_map[new_y][current_x] in (1, 2, 3, 9)
                    ):
                        monster["direction"] *= -1
                        new_y = current_y + monster["direction"]
                        if new_y < 0 or new_y >= len(level_map) or level_map[new_y][current_x] in (1, 2, 3, 9):
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
            if [new_x, new_y] in move_walls:
                move_x, move_y = new_x + dx, new_y + dy
                if 0 <= move_x < len(level_map[0]) and 0 <= move_y < len(level_map):
                    if level_map[move_y][move_x] == 0 or level_map[move_y][move_x] == 6:  # 밀려날 자리가 비어 있으면
                        move_walls.remove([new_x, new_y])
                        move_walls.append([move_x, move_y])
                        level_map[new_y][new_x] = 0
                        level_map[move_y][move_x] = 2
                        player_pos = [new_x, new_y]
                    else:
                        return  # 밀 수 없는 경우 이동 불가
                else:
                    return  # 맵 경계 밖으로 이동 불가
            elif [new_x, new_y] in destructible_walls:
                if break_count < break_limit:
                    destructible_walls.remove([new_x, new_y])
                    level_map[new_y][new_x] = 0
                    break_count += 1
                    player_pos = [new_x, new_y]
                else:
                    return

            # 파괴 가능한 벽 처리 (3)
            elif [new_x, new_y] in destructible_walls:
                if break_count < break_limit:
                    destructible_walls.remove([new_x, new_y])
                    level_map[new_y][new_x] = 0
                    break_count += 1
                    player_pos = [new_x, new_y]
                else:
                    return

            # 도착지점 처리 (4)
            elif level_map[new_y][new_x] == 4:
                os.system("python map2.py")
                pygame.quit()
                sys.exit()

            # 일반 이동
            elif level_map[new_y][new_x] == 0 or level_map[new_y][new_x] == 5 or level_map[new_y][new_x] == 6:
                player_pos = [new_x, new_y]

            # target_position에 움직이는 블록이 있다면 맵에 있는 7을 0으로 바꿈
            cnt = 0
            for [target_x, target_y] in target_positions:
                if level_map[target_y][target_x] == 2:  # 2는 움직이는 벽 번호
                    cnt += 1
                if cnt == len(target_positions):
                    for [off_x, off_y] in onoff_positions:
                        level_map[off_y][off_x] = 0

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
        nonlocal player_pos, current_image, destructible_walls, move_walls, level_map, break_count

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
        move_walls = initial_move_walls[:]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in MOVE_KEYS:
                    dx, dy, direction = MOVE_KEYS[event.key]
                    move_player(dx, dy, direction)
                if event.key == pygame.K_SPACE:
                    if player_pos in portal_positions:
                        portal_positions_copy = portal_positions.copy()  # 포탈 목록 복사
                        portal_positions_copy.remove(player_pos)  # 현재 위치의 포탈을 제외
                        if portal_positions_copy:
                            player_pos = portal_positions_copy[0]

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hint_button_rect.collidepoint(event.pos):
                    os.system('python hint1.py')

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

        # HINT 버튼 
        pygame.draw.rect(screen, WHITE, hint_button_rect)
        hint_text = font.render("HINT", True, BLACK)
        screen.blit(hint_text, hint_button_rect.topleft)

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
