import pygame
import pygame_widgets
from pygame_widgets.slider import Slider

# config
DISPLAY: tuple = (700, 600)
SCREEN_WIDTH = DISPLAY[0]
SCREEN_HEIGHT = DISPLAY[1]
dt = 0

# physics constants
G = 9.81 / 20
DRAG = 0.01
RESTITUTION = 0.95


# pygame setup
pygame.init()
screen = pygame.display.set_mode(DISPLAY)
clock = pygame.time.Clock()
running = True

gravity_slider = Slider(screen, 50, 50, 100, 20, min=0, max=9.81 / 10, step=0.0001, initial=G)
drag_slider = Slider(screen, 50, 100, 100, 20, min=0, max = 0.1, step=0.00001, initial=DRAG)

def update_position(position, velocity):

    gravity = gravity_slider.getValue()
    drag = drag_slider.getValue()
    # Update velocity (add gravity)
    velocity.x += drag
    velocity.y += gravity

    # Update position using velocity
    position += velocity
    return position
    
def restitution(position, velocity):
    # Apply restitution (damping) when colliding with walls
    if (position.y > SCREEN_HEIGHT - 40) or (position.y < 40):
        velocity.y *= RESTITUTION
    if (position.x > SCREEN_WIDTH - 40) or (position.x < 40):
        velocity.x *= RESTITUTION

    # Enforce position constraints (keep ball within bounds)
    position.y = max(40, min(SCREEN_HEIGHT - 40, position.y))
    position.x = max(40, min(SCREEN_WIDTH - 40, position.x))

    # Reverse velocity when hitting boundaries
    if (position.y >= SCREEN_HEIGHT - 40) or (position.y <= 40):
        velocity.y = -velocity.y
    if (position.x >= SCREEN_WIDTH - 40) or (position.x <= 40):
        velocity.x = -velocity.x

x, y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
position = pygame.Vector2(x, y)
position1 = pygame.Vector2(x-80, y)

vx, vy = 0, 0
velocity = pygame.Vector2(vx, vy)



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("pink")

    # RENDER YOUR GAME HERE

    # kinda self explanatory icl
    update_position(position, velocity)

    # Draw the ball at its new position
    pygame.draw.circle(screen, "red", position, 40)

    # Apply resitution laws
    restitution(position, velocity)
    
    # update pygame-widgets so sliders/buttons receive events and are drawn
    pygame_widgets.update(events)

    # flip() the display to put your work on screen
    pygame.display.flip()
    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000
pygame.quit()