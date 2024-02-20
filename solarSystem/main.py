import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont("arial", 16)
INFO_FONT = pygame.font.SysFont("arial", 14)

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
    # ... Add more sections for each planet as needed
}

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 Pixels
    TIMESTEP = 3600 * 24  # 1 Day
    ORBIT_TRAIL_LENGTH = 50

    def __init__(self, x, y, radius, color, mass, name=''):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

        # Texture will be loaded later
        self.texture = None

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_orbit = self.orbit[-self.ORBIT_TRAIL_LENGTH:]  # Limit the trail length
            updated_points = []
            for point in updated_orbit:
                orbit_x, orbit_y = point
                orbit_x = orbit_x * self.SCALE + WIDTH / 2
                orbit_y = orbit_y * self.SCALE + HEIGHT / 2
                updated_points.append((orbit_x, orbit_y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        if self.texture:
            win.blit(self.texture, (x - self.radius, y - self.radius))
        else:
            pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            if not self.sun:
                 # Correctly draw the planet name and distance text only once
                name_text = FONT.render(self.name, 1, WHITE)
                text_rect = name_text.get_rect(center=(x, y + self.radius + 20))
                win.blit(name_text, text_rect.topleft)

                distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
                win.blit(distance_text, (x - distance_text.get_width()/2, y - self.radius - 20))

        def draw_text_with_shadow(text, font, color, x, y, shadow_color):
            shadow_offset = 2
            text_surface = font.render(text, True, color)
            shadow_surface = font.render(text, True, shadow_color)
            win.blit(shadow_surface, (x + shadow_offset, y + shadow_offset))
            win.blit(text_surface, (x, y))

        # Drawing planet name and distance with shadow
        if not self.sun:
            draw_text_with_shadow(self.name, FONT, WHITE, x - FONT.size(self.name)[0] / 2, y + self.radius + 10, (0, 0, 0))
            distance_text = f"{round(self.distance_to_sun/1000, 1)}km"
            draw_text_with_shadow(distance_text, FONT, WHITE, x - FONT.size(distance_text)[0] / 2, y - self.radius - 20, (0, 0, 0))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y **2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


    def add_texture(self, texture_path):
        self.texture = pygame.image.load(texture_path)
        self.texture = pygame.transform.scale(self.texture, (self.radius*2, self.radius*2))

def main():
    run = True
    clock = pygame.time.Clock()

    selected_planet = None
    offset = 0  # Initialize scrolling offset
    info_text_height = 0

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, 'Sun')
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, 'Earth')
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, 'Mars')
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, 'Mercury')
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, 'Venus')
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    # Load textures
    # Note: Replace 'path_to_texture' with actual paths to the images
    earth.add_texture('earth_texture.png')
    mars.add_texture('mars_texture.png')
    mercury.add_texture('mercury_texture.png')
    venus.add_texture('venus_texture.png')  # Note the file extension is .jpg for Venus

    background = pygame.image.load('starback.jpg')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    selected_planet = None

    while run:
        clock.tick(30)
        WIN.blit(background, (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mx, my = pygame.mouse.get_pos()  # Get the mouse position
                    planet_found = False  # Indicator if a planet is clicked
                    for planet in planets:
                        # Calculate the distance of the mouse from the planet's center
                        distance = math.hypot((planet.x * Planet.SCALE + WIDTH / 2) - mx, 
                                              (planet.y * Planet.SCALE + HEIGHT / 2) - my)
                        if distance < planet.radius:
                            selected_planet = planet
                            offset = 0  # Reset scrolling offset when a new planet is selected
                            planet_found = True
                            break
                    if not planet_found:
                        selected_planet = None  # No planet was clicked, hide the menu
                elif event.button == 4:  # Scroll up
                    offset = max(offset - INFO_FONT.get_height(), 0)
                elif event.button == 5:  # Scroll down
                    offset = min(offset + INFO_FONT.get_height(), max(info_text_height - HEIGHT, 0))

        # Update and draw planets
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        # If a planet is selected, display the info menu
        if selected_planet:
            info_text_height = draw_info_menu(WIN, selected_planet, offset)

        pygame.display.update()

    pygame.quit()

# Update draw_info_menu to use the offset for scrolling:
def draw_info_menu(win, planet, offset):
    menu_width = 250
    menu_x = WIDTH - menu_width
    menu_bg_rect = pygame.Rect(menu_x, 0, menu_width, HEIGHT)
    pygame.draw.rect(win, BLACK, menu_bg_rect)

    # Start below the title
    y_offset = 30 - offset

    # Loop through each section in the planet's information
    for section_title, section_text in planet_info[planet.name].items():
        # Draw section title
        title_text = FONT.render(section_title, True, WHITE)
        win.blit(title_text, (menu_x + 10, y_offset))
        y_offset += title_text.get_height() + 5

        # Draw section text
        lines = wrap_text(section_text, INFO_FONT, menu_width - 20)
        for line in lines:
            line_surf = INFO_FONT.render(line, True, WHITE)
            win.blit(line_surf, (menu_x + 10, y_offset))
            y_offset += line_surf.get_height() + 2

        # Add some space after the section
        y_offset += 10

    return y_offset - (30 - offset)  # Return the total height of the drawn text


# Your wrap_text function remains unchanged.
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    while words:
        line = ''
        while words and font.size(line + words[0])[0] <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)
    return lines

def draw_text_with_shadow(text, font, color, x, y, shadow_color):
    shadow_offset = 2
    text_surface = font.render(text, True, color)
    shadow_surface = font.render(text, True, shadow_color)
    WIN.blit(shadow_surface, (x + shadow_offset, y + shadow_offset))
    WIN.blit(text_surface, (x, y))

if __name__ == "__main__":
    main()