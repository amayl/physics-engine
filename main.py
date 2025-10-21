import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from typing import Tuple

# config
DISPLAY: Tuple = (700, 600)
SCREEN_WIDTH = DISPLAY[0]
SCREEN_HEIGHT = DISPLAY[1]

# physics constants
G: float = 9.81 / 20
DRAG: float = 0.01
RESTITUTION: float = 0.95

# icl i genuinely felt like doing too much storing the colors like this
colours: list = [
    (255, 192, 203), # sassy pink
    (255, 10, 0), # period red
    (142, 142, 142) # boring grey
]


# pygame setup
pygame.init()
screen = pygame.display.set_mode(DISPLAY)
clock = pygame.time.Clock()
running = True

font = pygame.font.SysFont("Arial", 20)

def draw_text(text: str, font: pygame.font, color: Tuple, x: int, y: int):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# sliders
gravity_slider = Slider(screen, 50, 50, 100, 20, min=0, max=9.81 / 10, step=0.0001, initial=G)
drag_slider = Slider(screen, 50, 100, 100, 20, min=0, max = 0.1, step=0.00001, initial=DRAG)
restitution_slider = Slider(screen, 50, 150, 100, 20, min=0, max = 1, step=0.001, initial=RESTITUTION)

def update_position(position: pygame.Vector2, velocity: pygame.Vector2):
    # get the values from sliders
    gravity = gravity_slider.getValue()
    drag = drag_slider.getValue()

    # Update velocity (add gravity)
    velocity.x += drag
    velocity.y += gravity

    # Update position using velocity
    position += velocity
    return position
    
def restitution(position: pygame.Vector2, velocity: pygame.Vector2):
    # get value from slider
    restitution = restitution_slider.getValue()

    # Apply restitution (damping) when colliding with walls
    if (position.y > SCREEN_HEIGHT - 40) or (position.y < 40):
        velocity.y *= restitution
    if (position.x > SCREEN_WIDTH - 40) or (position.x < 40):
        velocity.x *= restitution

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

vx, vy = 0, 0
velocity = pygame.Vector2(vx, vy)

# GAME LOOP

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            quit()

    # fill screen
    screen.fill(colours[0])

    # add labels
    draw_text("gravity", font, colours[2], 170, 50)
    draw_text("drag", font, colours[2], 170, 100)
    draw_text("restitution", font, colours[2], 170, 150)

    # update pygame widgets first
    pygame_widgets.update(events)

    # physics update
    position = update_position(position, velocity)
    restitution(position, velocity)

    # draw the ball
    pygame.draw.circle(screen, colours[1], position, 40)

    # update display
    pygame.display.update()
    clock.tick(60)
pygame.quit()