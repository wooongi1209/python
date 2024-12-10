import pygame
import sys
import os

BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)

def main():
    pygame.init()
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Heart of Truth")
    story_image = pygame.image.load("1story.png")
    story_image = pygame.transform.scale(story_image, (700, 400))
    story_rect = story_image.get_rect(center=(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 100))
    text_image = pygame.image.load("1text.png")
    text_image = pygame.transform.scale(text_image, (700, 200))  
    text_rect = text_image.get_rect(center=(SCREEN_WIDTH // 2 - 30 , SCREEN_HEIGHT // 2 + 200 ))  
    button_font = pygame.font.Font(None, 30)
    next_button = pygame.Rect(1060, 640, 100, 30)
    skip_button = pygame.Rect(940, 640 , 100, 30)  
    next_text = button_font.render("Next", True, (WHITE))
    skip_text = button_font.render("Skip", True, (WHITE))

    # 메인 루프
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if next_button.collidepoint(mouse_pos):
                    import story2
                    story2.main()
                elif skip_button.collidepoint(mouse_pos):
                    import map1
                    map1.main()
                    running = False

        screen.fill((BLACK))
        screen.blit(story_image, story_rect.topleft)
        screen.blit(text_image, text_rect.topleft)

        # 버튼 그리기
        pygame.draw.rect(screen, (GRAY), skip_button)
        pygame.draw.rect(screen, (GRAY), next_button) 

        # 버튼 텍스트 중앙 정렬
        skip_text_rect = skip_text.get_rect(center=skip_button.center)
        next_text_rect = next_text.get_rect(center=next_button.center)
        screen.blit(skip_text, skip_text_rect.topleft)
        screen.blit(next_text, next_text_rect.topleft)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()