import pygame  # Import the pygame library for game development
pygame.init()  # Initialize all pygame modules

# Constants for screen dimensions and display settings
WIDTH, HEIGHT = 700, 500  # Screen width and height
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Create a display window
pygame.display.set_caption("Pong")  # Set the window title

# Game settings
FPS = 60  # Frames per second

# Colors
WHITE = (255, 255, 255)  # RGB for white color
BLACK = (0, 0, 0)  # RGB for black color

# Paddle and Ball settings
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100  # Paddle dimensions
BALL_RADIUS = 7  # Ball radius

# Font and score settings
SCORE_FONT = pygame.font.SysFont("comicsans", 50)  # Font for score display
WINNING_SCORE = 10  # Score required to win the game

# Paddle class to manage paddle properties and behavior
class Paddle:
    COLOR = WHITE  # Paddle color
    VEL = 4  # Paddle velocity

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x  # Initial and reset x-position
        self.y = self.original_y = y  # Initial and reset y-position
        self.width = width  # Paddle width
        self.height = height  # Paddle height

    def draw(self, win):
        """Draw the paddle on the screen."""
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        """Move the paddle up or down."""
        if up:
            self.y -= self.VEL  # Move up
        else:
            self.y += self.VEL  # Move down

    def reset(self):
        """Reset paddle to its original position."""
        self.x = self.original_x
        self.y = self.original_y

# Ball class to manage ball properties and behavior
class Ball:
    MAX_VEL = 5  # Maximum ball velocity
    COLOR = WHITE  # Ball color

    def __init__(self, x, y, radius):
        self.x = self.original_x = x  # Initial and reset x-position
        self.y = self.original_y = y  # Initial and reset y-position
        self.radius = radius  # Ball radius
        self.x_vel = self.MAX_VEL  # Initial x-velocity
        self.y_vel = 0  # Initial y-velocity

    def draw(self, win):
        """Draw the ball on the screen."""
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        """Update the ball's position based on its velocity."""
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        """Reset the ball to its original position and reverse x-velocity."""
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1  # Reverse direction

# Function to draw all game elements
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)  # Fill the screen with black color

    # Display scores
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    # Draw paddles
    for paddle in paddles:
        paddle.draw(win)

    # Draw centerline
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    # Draw the ball
    ball.draw(win)
    pygame.display.update()  # Update the display

# Function to handle collisions between ball and paddles or walls
def handle_collision(ball, left_paddle, right_paddle):
    # Ball collision with top or bottom wall
    if ball.y + ball.radius >= HEIGHT or ball.y - ball.radius <= 0:
        ball.y_vel *= -1  # Reverse y-velocity

    # Ball collision with left paddle
    if ball.x_vel < 0:
        if left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1  # Reverse x-velocity

                # Calculate ball's new y-velocity
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    # Ball collision with right paddle
    else:
        if right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1  # Reverse x-velocity

                # Calculate ball's new y-velocity
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

# Function to handle paddle movement based on key presses
def handle_paddle_movement(keys, left_paddle, right_paddle):
    # Left paddle controls (W/S keys)
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    # Right paddle controls (Up/Down arrow keys)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)

# Main game loop
def main():
    run = True
    clock = pygame.time.Clock()  # Clock to control frame rate

    # Initialize paddles and ball
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    # Scores
    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)  # Control game speed
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)  # Draw game elements

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check for quit event
                run = False
                break

        keys = pygame.key.get_pressed()  # Get pressed keys
        handle_paddle_movement(keys, left_paddle, right_paddle)  # Handle paddle movements

        ball.move()  # Move the ball
        handle_collision(ball, left_paddle, right_paddle)  # Handle collisions

        # Update scores and reset ball on scoring
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        # Check for game win
        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            # Display win message
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)

            # Reset game
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()  # Quit pygame

if __name__ == '__main__':
    main()  # Run the main game function
