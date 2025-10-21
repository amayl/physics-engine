import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

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

# sliders
gravity_slider = Slider(screen, 50, 50, 100, 20, min=0, max=9.81 / 10, step=0.0001, initial=G)
drag_slider = Slider(screen, 50, 100, 100, 20, min=0, max = 0.1, step=0.00001, initial=DRAG)
restitution_slider = Slider(screen, 50, 150, 100, 20, min=0, max = 1, step=0.001, initial=RESTITUTION)

# labels
gravity_label = TextBox(screen, 170, 50, 70, 35, fontSize=30)
drag_label = TextBox(screen, 170, 100, 70, 35, fontSize=30)
restitution_label = TextBox(screen, 170, 150, 70, 35, fontSize=30)

# make the textboxes behave as labels
gravity_label.disable()
drag_label.disable()
restitution_label.disable()


def update_position(position, velocity):
    # get the values from sliders
    gravity = gravity_slider.getValue()
    drag = drag_slider.getValue()

    # Update velocity (add gravity)
    velocity.x += drag
    velocity.y += gravity

    # Update position using velocity
    position += velocity
    return position
    
def restitution(position, velocity):
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
    screen.fill("pink")

    # update pygame widgets first
    pygame_widgets.update(events)

    # update label text after widgets are updated
    gravity_label.setText(f"{gravity_slider.getValue():.4f}")
    drag_label.setText(f"{drag_slider.getValue():.4f}")
    restitution_label.setText(f"{restitution_slider.getValue():.4f}")

    # physics update
    position = update_position(position, velocity)
    restitution(position, velocity)

    # draw the ball
    pygame.draw.circle(screen, "red", position, 40)

    # update display
    pygame.display.update()
    clock.tick(60)
pygame.quit()