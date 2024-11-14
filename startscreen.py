import pygame
import sys
import os

pygame.init()

WHITE = (255, 255, 255)

# 화면 크기 
screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("HEART OF TRUTH")

# 배경이미지
background_image = pygame.image.load("start.png") 
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# START버튼 위치,크기
start_button = pygame.Rect(500, 500, 230, 60)
# EXIT버튼 위치, 크기
exit_button = pygame.Rect(500, 600, 230, 60)

font = pygame.font.Font(None, 36)
start_text = font.render("  ", True, WHITE)
exit_text = font.render("   ", True, WHITE)

def main_menu():
    while True:
        screen.blit(background_image, (0, 0))

        screen.blit(start_text, (start_button.x + 70, start_button.y + 10))
        screen.blit(exit_text, (exit_button.x + 80, exit_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    os.system("python main.py")
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

main_menu()
