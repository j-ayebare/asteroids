import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

def show_start_menu(screen):
    pygame.font.init()
    font = pygame.font.Font(None, 72)  # Menu title font size
    option_font = pygame.font.Font(None, 48)  # Option font size

    title_text = font.render("Asteroids Game", True, (255, 255, 255))
    start_text = "Start Game"
    quit_text = "Quit"

    selected_option = 0
    options = [start_text, quit_text]

    while True:
        screen.fill((0, 0, 0))  # Fill screen with black

        # Display the title
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 3))

        # Display options
        for i, option in enumerate(options):
            # Highlight the selected option
            color = (255, 0, 0) if i == selected_option else (255, 255, 255)
            rendered_text = option_font.render(option, True, color)
            screen.blit(rendered_text, (SCREEN_WIDTH // 2 - rendered_text.get_width() // 2, SCREEN_HEIGHT // 2 + i * 60))

        pygame.display.flip()

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Quit the program

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if selected_option == 0:
                        return True  # Start the game
                    elif selected_option == 1:
                        return False  # Quit the game

def main():
    pygame.init()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    if not show_start_menu(screen):
        return  # Quit if player chooses 'Quit' in the menu

    color = (0,0,0)
    game_time = pygame.time.Clock()
    dt = 0
    score = 0
    lives = 5

    pygame.font.init()
    font = pygame.font.Font(None, 36)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    new_player = Player(SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 2)
    enemies = AsteroidField()
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        screen.fill(color)

        for drawn in drawable:
            drawn.draw(screen)

        for updated in updatable:
            updated.update(dt)
        
        for sprite in asteroids:
            if sprite.collision(new_player):
                sprite.kill()
                new_player.position.x = SCREEN_WIDTH / 2
                new_player.position.y = SCREEN_HEIGHT / 2
                lives -= 1
                print(f"Lives left: {lives}")
                if lives <= 0:
                    print("Game over!")
                    exit()
        
        for shot in shots:
            for sprite in asteroids:
                if sprite.collision(shot):
                    shot.kill()
                    sprite.split()  
                    score += 100  # Increment score
                    print(f"Score: {score}")
                    
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))

        screen.blit(score_text, (10, 10))  # Position score at top-left corner
        screen.blit(lives_text, (10, 40))  # Position lives below the score
        
        pygame.display.flip()
        dt = game_time.tick(60) / 1000

if __name__ == "__main__":
    main()