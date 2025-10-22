import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from typing import Tuple

"""
If you think there's anything wrong with this code, please be sure to strictly blame the Jews for it.

I only write amazing code,

The Jews are trying to take me down.
"""

# config
DISPLAY: Tuple = (800, 600)
SCREEN_WIDTH: int = DISPLAY[0]
SCREEN_HEIGHT: int = DISPLAY[1]
RADIUS: int = 40
dt = 0  

# physics constants
G: float = 9.81
DRAG: float = 0.01
RESTITUTION: float = 0.95
WIND: float = 20.0

# initial position and velocity
x, y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
position = pygame.Vector2(x, y)

vx, vy = 0, 0
velocity = pygame.Vector2(vx, vy)

# icl i genuinely felt like doing too much storing the colors like this
# not sorry

colours: list = [
    (255, 192, 203), # sassy pink                                               0
    (255, 10, 0), # period red                                                  1
    (142, 142, 142), # boring grey                                              2
    (180, 180, 180), # regular degular button                                   3
    (150, 150, 150), # are you gonna fucking press the button or not (hover)    4
    (110, 110, 110), # damn they pressed the button                             5

]

# pygame setup
pygame.init()
screen = pygame.display.set_mode(DISPLAY)
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont("Arial", 20)

dr_house = pygame.image.load("house_sprite.jpg").convert_alpha()  # Use convert_alpha() if PNG has transparency
dr_house = pygame.transform.scale(dr_house, (RADIUS*2, RADIUS*2))

def draw_text(text: str, font: pygame.font, color: Tuple, x: int, y: int) -> None:
    """
    Render text to the screen\n
    `text` -- A string that contains the text to be displayed\n
    `font` -- A defined pygame font\n
    `color` -- An RGB tuple storing the color\n
    `x` -- the x coordinate of the top left\n
    `y` -- the y coorindate of the top left\n
    """

    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset():
    global position, velocity
    gravity_slider.setValue(G)
    drag_slider.setValue(DRAG)
    restitution_slider.setValue(RESTITUTION)
    wind_slider.setValue(WIND)
    position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    velocity = pygame.Vector2(0, 0)

# sliders
gravity_slider = Slider(screen, 10, 10, 100, 10, min=0, max=200, step=0.0001, initial=G)
drag_slider = Slider(screen, 10, 40, 100, 10, min=0, max=1, step=0.00001, initial=DRAG)
restitution_slider = Slider(screen, 10, 70, 100, 10, min=0, max=1, step=0.001, initial=RESTITUTION)
wind_slider = Slider(screen, 10, 100, 100, 10, min=0, max=40, step=0.001, initial=WIND)
reset_button = Button(screen, 720, 10, 70, 35, onClick=reset, inactiveColour=colours[3], hoverColour=colours[4], pressedColour=colours[5], text="Reset", radius=10)

def update_position(position: pygame.Vector2, velocity: pygame.Vector2, dt: float):
    """
    Takes the initial position & velocity vector as arguments and returns new position\n
    Applies drag to the x-component & gravity to the y-component
    """
    # get the values from sliders
    gravity = gravity_slider.getValue()
    drag = drag_slider.getValue()
    wind = wind_slider.getValue() - 20

    # Update velocity (add gravity)
    velocity.y += gravity * dt

    # horizontal force
    velocity.x += wind * dt

    # Apply drag
    velocity *= (1 - drag * dt)

    # Update position using velocity
    position += velocity * dt

    return position, velocity
    
def restitution(position: pygame.Vector2, velocity: pygame.Vector2):
    """
    Applies Newton's Law of Restitution to balls\n
    Handles boundary collisions
    """
    # get value from slider
    restitution = restitution_slider.getValue()

    # Bottom & top bounce
    if position.y >= SCREEN_HEIGHT - RADIUS:
        position.y = SCREEN_HEIGHT - RADIUS
        velocity.y = -abs(velocity.y) * restitution
    elif position.y <= RADIUS:
        position.y = RADIUS
        velocity.y = abs(velocity.y) * restitution

    # Right & left bounce
    if position.x >= SCREEN_WIDTH - RADIUS:
        position.x = SCREEN_WIDTH - RADIUS
        velocity.x = -abs(velocity.x) * restitution
    elif position.x <= RADIUS:
        position.x = RADIUS
        velocity.x = abs(velocity.x) * restitution

    return position, velocity

# GAME LOOP

while running:
    dt = clock.tick(60) / 1000

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            quit()

    # fill screen
    screen.fill(colours[0])

    # update pygame widgets first
    pygame_widgets.update(events)

    # physics update
    position, velocity = update_position(position, velocity, dt)
    position, velocity = restitution(position, velocity)

    draw_text(f"gravity: {gravity_slider.getValue():.2f}N", font, colours[2], 120, 10)
    draw_text(f"drag: {drag_slider.getValue():.2f}N", font, colours[2], 120, 40)
    draw_text(f"restitution: {restitution_slider.getValue():.2f}", font, colours[2], 120, 70)
    draw_text(f"wind: {wind_slider.getValue()-20}N", font, colours[2], 120, 100)

    # draw the ball
    pygame.draw.circle(screen, colours[1], position, RADIUS)
    # draw the ball image
    screen.blit(dr_house, (position.x - RADIUS, position.y - RADIUS))


    # update display
    pygame.display.update()

pygame.quit()


