import pygame
import math

# Initialize pygame library
pygame.init()

# Set up the display dimensions
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")  # Set the title of the simulation window

# Define color constants using RGB values
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BLACK = (0, 0, 0)

# Fonts for text rendering
FONT = pygame.font.SysFont("arial", 16)
INFO_FONT = pygame.font.SysFont("arial", 14)

# Dictionary containing planet information for the menu
planet_info = {
    'Sun': {
        'About': 'The Sun is the star at the center of the Solar System. It is a nearly perfect sphere of hot plasma and is by far the most important source of energy for life on Earth.',
        'Interesting Facts': 'The Sun contains 99.86% of the Solar System\'s mass. It is about 4.6 billion years old and is expected to be around for another 5 billion years.',
        'Structure': 'The Sun is composed of the photosphere, chromosphere, and corona. It has a core where nuclear fusion produces enormous energy.',
    },
    'Mercury': {
        'About': 'Mercury is the smallest planet in the Solar System and the closest to the Sun. It has no atmosphere to retain heat, causing extreme temperature variations.',
        'Interesting Facts': 'A day on Mercury lasts 176 Earth days, while a year is just 88 days. Its surface is heavily cratered and similar in appearance to the Moon.',
        'Exploration': 'The MESSENGER spacecraft orbited Mercury over 4,000 times and provided significant data before it was deliberately crashed into the planet in 2015.',
    },
    'Venus': {
        'About': 'Venus is the second planet from the Sun. It is named after the Roman goddess of love and beauty and is sometimes referred to as Earth\'s "sister planet" due to their similar size and mass.',
        'Interesting Facts': 'Venus has a thick, toxic atmosphere consisting mainly of carbon dioxide, with clouds of sulfuric acid, making its surface pressure 92 times that of Earth.',
        'Surface': 'The surface of Venus is dominated by volcanic features and has more volcanoes than any other planet in the Solar System.',
    },
    'Earth': {
        'About': 'Earth is the third planet from the Sun and the only astronomical object known to harbor life. Its large amount of liquid water and oxygen-rich atmosphere make life possible.',
        'Interesting Facts': 'Earth\'s rotation is gradually slowing down, adding about 1.7 milliseconds per century to the length of a day. It also has a powerful magnetic field that protects it from the effects of solar wind.',
        'Human Presence': 'Earth is the only planet known to support life, with millions of species existing in its diverse ecosystems. It is also the only planet where water can exist in liquid form on the surface.',
    },
    'Mars': {
        'About': 'Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System. It is referred to as the "Red Planet" because of the presence of iron oxide on its surface.',
        'Interesting Facts': 'Mars is home to the tallest volcano, Olympus Mons, and the deepest canyon, Valles Marineris. Its day is similar in length to Earth\'s at 24.6 hours.',
        'Exploration': 'Mars has been a focal point for space exploration with multiple rovers and landers sent to its surface to study its climate and geology.',
    },
}

# Class to represent planets and their properties
class Planet:
    # Define constants for simulation
    AU = 149.6e6 * 1000  # Distance of 1 Astronomical Unit in meters
    G = 6.67428e-11  # Gravitational constant
    SCALE = 250 / AU  # Scale factor to convert meters to pixels
    TIMESTEP = 3600 * 24  # Simulation timestep (1 day)
    ORBIT_TRAIL_LENGTH = 50  # Maximum length of the orbit trail

    def __init__(self, x, y, radius, color, mass, name=''):
        # Initialize the planet's attributes
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        # Orbit-related attributes
        self.orbit = []  # To store the trail of the planet's orbit
        self.sun = False  # Whether the planet is a star (Sun)
        self.distance_to_sun = 0  # Distance to the Sun

        # Velocity components
        self.x_vel = 0  # Velocity in the x-direction
        self.y_vel = 0  # Velocity in the y-direction

        # Optional texture for graphical rendering
        self.texture = None

    def draw(self, win):
        # Method to draw the planet and its orbit trail
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # Draw orbit trail if it exists
        if len(self.orbit) > 2:
            updated_orbit = self.orbit[-self.ORBIT_TRAIL_LENGTH:]  # Limit the trail length
            updated_points = []
            for point in updated_orbit:
                orbit_x, orbit_y = point
                orbit_x = orbit_x * self.SCALE + WIDTH / 2
                orbit_y = orbit_y * self.SCALE + HEIGHT / 2
                updated_points.append((orbit_x, orbit_y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        # Draw the planet (texture or circle)
        if self.texture:
            win.blit(self.texture, (x - self.radius, y - self.radius))
        else:
            pygame.draw.circle(win, self.color, (x, y), self.radius)

        # If not the Sun, display the planet name and distance to the Sun
        if not self.sun:
            draw_text_with_shadow(self.name, FONT, WHITE, x - FONT.size(self.name)[0] / 2, y + self.radius + 10, (0, 0, 0))
            distance_text = f"{round(self.distance_to_sun / 1000, 1)}km"
            draw_text_with_shadow(distance_text, FONT, WHITE, x - FONT.size(distance_text)[0] / 2, y - self.radius - 20, (0, 0, 0))

    def attraction(self, other):
        # Calculate gravitational attraction between this planet and another
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        # Update the distance to the Sun
        if other.sun:
            self.distance_to_sun = distance

        # Gravitational force computation
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        # Update the planet's position based on gravitational forces
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue  # Skip self-interaction

            # Calculate gravitational force from other planets
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Update velocity based on net force
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Update position based on velocity
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))  # Add current position to the orbit trail

    def add_texture(self, texture_path):
        # Load and scale a texture for the planet
        self.texture = pygame.image.load(texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.radius * 2, self.radius * 2))

# Main function for running the simulation
def main():
    # Main game loop
    run = True
    clock = pygame.time.Clock()

    selected_planet = None  # Currently selected planet for info menu
    offset = 0  # Offset for scrolling in the info menu
    info_text_height = 0  # Height of text in the info menu

    # Create instances of planets
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, 'Sun')
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, 'Earth')
    earth.y_vel = 29.783 * 1000  # Earth's orbital velocity

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, 'Mars')
    mars.y_vel = 24.077 * 1000  # Mars's orbital velocity

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, 'Mercury')
    mercury.y_vel = -47.4 * 1000  # Mercury's orbital velocity

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, 'Venus')
    venus.y_vel = -35.02 * 1000  # Venus's orbital velocity

    planets = [sun, earth, mars, mercury, venus]  # List of planets in the simulation

    # Load textures for planets
    earth.add_texture('earth_texture.png')
    mars.add_texture('mars_texture.png')
    mercury.add_texture('mercury_texture.png')
    venus.add_texture('venus_texture.png')

    # Load background image
    background = pygame.image.load('starback.jpg')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    while run:
        clock.tick(30)  # Set the simulation to run at 30 frames per second
        WIN.blit(background, (0, 0))  # Draw background image

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit the simulation
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Handle mouse clicks
                if event.button == 1:  # Left-click
                    mx, my = pygame.mouse.get_pos()  # Get mouse position
                    selected_planet = None  # Reset selected planet
                    for planet in planets:
                        # Check if a planet was clicked
                        distance = math.hypot((planet.x * Planet.SCALE + WIDTH / 2) - mx,
                                              (planet.y * Planet.SCALE + HEIGHT / 2) - my)
                        if distance < planet.radius:  # Click inside the planet's radius
                            selected_planet = planet  # Select this planet
                            offset = 0  # Reset scroll offset for menu
                            break
                elif event.button == 4:  # Scroll up
                    offset = max(offset - INFO_FONT.get_height(), 0)
                elif event.button == 5:  # Scroll down
                    offset = min(offset + INFO_FONT.get_height(), max(info_text_height - HEIGHT, 0))

        # Update and draw all planets
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        # Display info menu if a planet is selected
        if selected_planet:
            info_text_height = draw_info_menu(WIN, selected_planet, offset)

        pygame.display.update()  # Refresh the display

    pygame.quit()  # Quit pygame when simulation ends

# Function to draw the information menu for the selected planet
def draw_info_menu(win, planet, offset):
    menu_width = 250  # Width of the info menu
    menu_x = WIDTH - menu_width  # X-coordinate for menu placement
    menu_bg_rect = pygame.Rect(menu_x, 0, menu_width, HEIGHT)  # Background rectangle
    pygame.draw.rect(win, BLACK, menu_bg_rect)  # Draw menu background

    y_offset = 30 - offset  # Start offset for scrolling text

    # Display planet information section by section
    for section_title, section_text in planet_info[planet.name].items():
        # Draw section title
        title_text = FONT.render(section_title, True, WHITE)
        win.blit(title_text, (menu_x + 10, y_offset))
        y_offset += title_text.get_height() + 5

        # Wrap and display the section's text
        lines = wrap_text(section_text, INFO_FONT, menu_width - 20)
        for line in lines:
            line_surf = INFO_FONT.render(line, True, WHITE)
            win.blit(line_surf, (menu_x + 10, y_offset))
            y_offset += line_surf.get_height() + 2

        y_offset += 10  # Add spacing between sections

    return y_offset - (30 - offset)  # Return total height of the displayed text

# Helper function to wrap text into multiple lines for a given width
def wrap_text(text, font, max_width):
    words = text.split(' ')  # Split the text into individual words
    lines = []  # List to store lines of text
    while words:
        line = ''  # Start with an empty line
        while words and font.size(line + words[0])[0] <= max_width:  # Add words until max width is reached
            line += (words.pop(0) + ' ')  # Add a word to the line
        lines.append(line)  # Append the completed line to the list
    return lines

# Helper function to draw text with a shadow effect
def draw_text_with_shadow(text, font, color, x, y, shadow_color):
    shadow_offset = 2  # Offset for shadow effect
    text_surface = font.render(text, True, color)  # Render the main text
    shadow_surface = font.render(text, True, shadow_color)  # Render the shadow text
    WIN.blit(shadow_surface, (x + shadow_offset, y + shadow_offset))  # Draw shadow
    WIN.blit(text_surface, (x, y))  # Draw main text

# Entry point for the simulation
if __name__ == "__main__":
    main()  # Run the main simulation function
