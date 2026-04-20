import math
import pygame
import random
import time
from SilversPyPhysics import Gravity, Momentum
from Player.player import Player
from Enemies.enemy import Enemy

pygame.init()

WIDTH = 500
HEIGHT = 700

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Dodger")

FPS = 60

def draw(player, enemies, font, level, frame):

    player.draw(WIN)

    for enemy in enemies:
        enemy.draw(WIN)

    levelText = font.render(f"Level: {level}", True, (255, 255, 255))
    float_offset_x = math.sin(frame * 0.001) * 10
    float_offset_y = math.sin(frame * 0.001 * 2) * 5
    textRect = levelText.get_rect(center=(WIDTH // 2 + float_offset_x, 30 + float_offset_y))
    WIN.blit(levelText, textRect)

    barWidth = 200
    barHeight = 20
    hpPercent = max(0, min(1, player.Health / 100))
    pygame.draw.rect(WIN, (255, 0, 0), (WIDTH / 2 - barWidth//2, HEIGHT - 50, barWidth, barHeight))
    pygame.draw.rect(WIN, (0, 255, 0), (WIDTH//2 - barWidth//2, HEIGHT- 50, barWidth * hpPercent, barHeight))

    pygame.display.flip()

def main():
    player = Player(250, 600)

    player.Health = 100

    running = True

    clock = pygame.time.Clock()

    enemies = []
    level = 0

    spawnTimer = 0
    spawning = False

    font = pygame.font.Font(None, 32)

    healedThisLevel = False
    frame = 0

    try:
        with open("highscore.txt", "r") as f:
            highscore = int(f.read())
    except:
        highscore = 0

    while running:
        frame += 1
        clock.tick(FPS)
        WIN.fill("black")
        
        keys = pygame.key.get_pressed()
        player.handleInput(keys)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused()
        
        if level != 0 and level % 8 == 0 and not healedThisLevel:
            player.Health = 100
            healedThisLevel = True
        
        if level % 8 != 0:
            healedThisLevel = False

        if len(enemies) == 0 and not spawning:
            level += 1
            spawning = True
            spawnTimer = 0

        if spawning:
            spawnTimer += clock.get_time()
            if spawnTimer >= 1000:
                for i in range(random.randint(3, 8)):
                    x = random.randint(0, WIDTH - 40)
                    y = -random.randint(10, 100)
                    enemies.append(Enemy(x, y, 40, 40, level))
                spawning = False


        # remove enemies that fell off screen
        enemies = [e for e in enemies if not e.offScreenCheck(HEIGHT)]
        newEnemies = []
        for enemy in enemies:
            enemy.update()
            if player.rect.colliderect(enemy.rect):
                player.Health -= 10
                if player.Health <= 0:
                    if level > highscore:
                        with open("highscore.txt", "w") as f:
                            f.write(str(level))
                    return level
            else:
                newEnemies.append(enemy)

        enemies = newEnemies

        # keep player on screen
        if player.rect.left <= 0:
            player.rect.left = 0
        if player.rect.right >= WIDTH:
            player.rect.right = WIDTH

        draw(player, enemies, font, level, frame)

    pygame.quit()

def paused():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill("black")

    fontLarge = pygame.font.SysFont("Aerial", 64, bold=True)
    fontSmall = pygame.font.SysFont("Aerial", 32)

    pausedText = fontLarge.render("Game Paused", True, (255, 255, 255))
    pausedTextRect = pausedText.get_rect(center=(WIDTH//2, 100))

    unpauseText = fontSmall.render("Press ESC to Unpause", True, (255, 255, 255))
    unpauseTextRect = unpauseText.get_rect(center=(WIDTH//2, HEIGHT//2))

    WIN.blit(overlay, (0,0))
    WIN.blit(pausedText, pausedTextRect)
    WIN.blit(unpauseText, unpauseTextRect)
    pygame.display.flip()

    waiting = True
    frame = 0

    while waiting:

        frame += 1
        WIN.blit(overlay, (0,0))

        float_offset_x = math.sin(frame * 0.001) * 5
        float_offset_y = math.sin(frame * 0.001 * 2) * 2

        pausedTextRect = pausedText.get_rect(center=(WIDTH//2 + float_offset_x, 100 + float_offset_y))
        unpauseTextRect = unpauseText.get_rect(center=(WIDTH//2 - float_offset_x, HEIGHT//2 - float_offset_y))

        WIN.blit(pausedText, pausedTextRect)
        WIN.blit(unpauseText, unpauseTextRect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False  # Resume
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.flip()

def gameOver(finalLevel):
    font = pygame.font.Font(None, 48)
    smallFont = pygame.font.Font(None, 32)
    
    gameOverText = font.render("Game Over", True, (255, 0, 0))
    levelText = smallFont.render(f"Level Reached: {finalLevel}", True, (255, 255, 255))
    clickText = smallFont.render("Click to return to menu", True, (200, 200, 200))
    
    frame = 0
    clock = pygame.time.Clock()

    while True:
        frame += 1
        clock.tick(FPS)
        WIN.fill("black")
        
        float_offset_x = math.sin(frame * 0.001) * 5
        float_offset_y = math.sin(frame * 0.001 * 2) * 2

        gameOverRect = gameOverText.get_rect(center=(WIDTH//2 + float_offset_x, HEIGHT//2 - 50 + float_offset_y))
        WIN.blit(gameOverText, gameOverRect)

        levelRect = levelText.get_rect(center=(WIDTH//2 - float_offset_x, HEIGHT//2 + 20 - float_offset_y))
        WIN.blit(levelText, levelRect)

        clickRect = clickText.get_rect(center=(WIDTH//2 + float_offset_x, HEIGHT//2 + 80 + float_offset_y))
        WIN.blit(clickText, clickRect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

def mainMenu():
    try:
        with open("highscore.txt", "r") as f:
            highscore = int(f.read())
    except:
        highscore = 0
        with open("highscore.txt", "w") as f:
            f.write("0")

    startButton = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 -30, 200, 60)
    font = pygame.font.Font(None, 48)
    
    highScoreText = font.render(f"High Score: {highscore}", True, (255, 255, 255))
    startText = font.render("START", True, (255, 255, 255))
    
    frame = 0
    clock = pygame.time.Clock()

    while True:
        frame += 1
        clock.tick(FPS)
        mousePOS = pygame.mouse.get_pos()
        
        float_offset_x = math.sin(frame * 0.001) * 5
        float_offset_y = math.sin(frame * 0.001 * 2) * 2

        if startButton.collidepoint(mousePOS):
            buttonColor = (100, 100, 100)
        else:
            buttonColor = (50, 50, 50)
    
        WIN.fill("black")

        highScoreRect = highScoreText.get_rect(center=(WIDTH//2 + float_offset_x, 100 + float_offset_y))
        WIN.blit(highScoreText, highScoreRect)

        pygame.draw.rect(WIN, buttonColor, startButton)
        startRect = startText.get_rect(center=(startButton.center))
        WIN.blit(startText, startRect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(mousePOS):
                    return

if __name__ == "__main__":
    while True:
        mainMenu()
        finalLevel = main()
        gameOver(finalLevel)