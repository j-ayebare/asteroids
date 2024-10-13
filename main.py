import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

def main():
    pygame.init()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    color = (0,0,0)
    game_time = pygame.time.Clock()
    dt = 0

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
                print ("Game over!")
                exit()
        
        for shot in shots:
            for sprite in asteroids:
                if sprite.collision(shot):
                    shot.kill()
                    sprite.split()
                    

        pygame.display.flip()
        dt = game_time.tick(60) / 1000

if __name__ == "__main__":
    main()