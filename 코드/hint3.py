import pygame
import sys

BLACK = (0, 0, 0)

def main():
    pygame.init()
    screen_width = 600
    screen_height = 300
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Hint")
    screen.fill((BLACK))
    image_path = "hint3text.png"
    center_image = pygame.image.load(image_path)
    center_image_rect = center_image.get_rect(center=(screen_width // 2, screen_height // 2))

    # 메인 루프
    running = True
    while running:
        screen.fill((BLACK))  # 배경색 검정으로 설정
        screen.blit(center_image, center_image_rect.topleft)  # 이미지 가운데 출력
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
