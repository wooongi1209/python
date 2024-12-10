import pygame
import sys

BLACK = (0, 0, 0)

def main():
    pygame.init()
    # 화면 설정
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Heart of Truth")
    
    # 스토리 이미지 설정
    story_image = pygame.image.load("end3story.png")
    story_image = pygame.transform.scale(story_image, (700, 400))
    story_rect = story_image.get_rect(center=(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100))
    
    # 텍스트 이미지 설정
    text_image = pygame.image.load("end3text.png")
    text_image = pygame.transform.scale(text_image, (700, 200))  
    text_rect = text_image.get_rect(center=(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 + 200))

    # 메인 루프
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((BLACK))
        screen.blit(story_image, story_rect.topleft)
        screen.blit(text_image, text_rect.topleft)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
