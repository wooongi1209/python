import pygame

pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 이미지 로드 및 위치 설정
image = "story1.png"  # 이미지 파일 경로
image_story1 = pygame.image.load(image)  # 이미지 로드
image_story1 = pygame.transform.scale(image_story1, (600, 400))  # 크기 조정
image_center_rect = image_story1.get_rect(600, 350)  # 중앙에 배치

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # 배경색 설정
    screen.blit(image_story1, image_center_rect)  # 이미지 화면에 그리기
    pygame.display.flip()

pygame.quit()
