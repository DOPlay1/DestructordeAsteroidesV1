import pygame, random
from PIL.FontFile import WIDTH
from pygame.examples.moveit import HEIGHT
from typer.colors import GREEN

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Destructor de asteroides")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font("serif"), size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, porcentaje):
    if porcentaje < 0:
        porcentaje = 0
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (porcentaje / 100) * BAR_LENGHT
    borde = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, borde, 2)

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/nave.png"), (100, 100)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT + 130
        self.speed_x = 0
        self.shield = 100

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def disparo(self):
        laser = Laser(self.rect.centerx, self.rect.top)
        all_sprites.add(laser)
        lasers.add(laser)


class Asteroide(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(asteroides_imagemes)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-1400, -1000)
        self.speed_y = random.randrange(1, 8)
        self.speed_x = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40 :
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 10)
            self.speed_x = random.randrange(-5, 5)


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/laser.png"), (10, 40)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_list[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # Velocidad de la explosión

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_list):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_list[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_game_over_screen():
    screen.blit(background, [0, 0])
    draw_text(screen, "Destructor de asteroides", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Instrucciones", 22, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Utiliza las flechas para moverte, y la barra espaciadora para disparar", 18, WIDTH // 2, HEIGHT // 2 + 50)
    draw_text(screen, "Presiona una tecla para empezar", 18, WIDTH // 2, HEIGHT * 5/6)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

asteroides_imagemes = []
asteroides_list = ["assets/asteroid1.png", "assets/asteroid2.png", "assets/asteroid3.png"]
for img in asteroides_list:
    asteroides_imagemes.append(pygame.transform.scale(pygame.image.load(img), (100, 100)).convert())
# Explosiones
explosion_list = []
for i in range(4):
    file = "assets/boom{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (90, 90))
    explosion_list.append(img_scale)
# Fondo de juego
background = pygame.transform.scale(pygame.image.load("assets/space.jpeg"), (WIDTH, WIDTH)).convert()


game_over = True
running = True
while running:
    if game_over:
        show_game_over_screen()

        game_over = False

        all_sprites = pygame.sprite.Group()
        asteroides_list = pygame.sprite.Group()
        lasers = pygame.sprite.Group()
        jugador = Jugador()
        all_sprites.add(jugador)
        for i in range(8):
            asteroide = Asteroide()
            all_sprites.add(asteroide)
            asteroides_list.add(asteroide)
        score = 0

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jugador.disparo()
    all_sprites.update()

    # Destruir asteroides
    hits = pygame.sprite.groupcollide(asteroides_list, lasers, True, True)
    for hit in hits:
        score += 10
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        asteroide = Asteroide()
        all_sprites.add(asteroide)
        asteroides_list.add(asteroide)

    # Colisiones
    hits = pygame.sprite.spritecollide(jugador, asteroides_list, True)
    for hit in hits:
        jugador.shield -= 20
        asteroide = Asteroide()
        all_sprites.add(asteroide)
        asteroides_list.add(asteroide)
        if jugador.shield <= 0:
            game_over = True
    screen.blit(background, [0, 0])  # Ajuste de fondo para la ventana.
    all_sprites.draw(screen)
    draw_text(screen, str(score), 20, WIDTH // 2, 10)   # Puntuación
    draw_shield_bar(screen, 5, 5, jugador.shield)
    pygame.display.flip()
pygame.quit()
