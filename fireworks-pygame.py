import pygame
import sys
import random
import math

pygame.init()

# Configurações da tela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fogos de Artifício")

# Cores
black = (0, 0, 0)
colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 128, 0), (0, 0, 255), (128, 0, 128), (255, 255, 255)]

# Classe para representar uma partícula da explosão
class Particle:
    def __init__(self, x, y, color, explode_height):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 3
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(2, 5)
        self.explode_height = explode_height
        self.max_lifetime = 100  # Ajuste o valor conforme necessário para aumentar ou diminuir a duração do brilho
        self.lifetime = self.max_lifetime

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Reduz a vida útil da partícula
        self.lifetime -= 1

    def draw(self):
        # Calcula o tamanho proporcional à vida útil
        size_factor = self.lifetime / self.max_lifetime
        size = int(self.radius * size_factor)

        # Calcula a transparência proporcional à vida útil
        alpha = int(255 * size_factor)

        # Desenha a partícula
        try:
            pygame.draw.circle(screen, (self.color[0], self.color[1], self.color[2], alpha), (int(self.x), int(self.y)), max(1, size))
        except ValueError:
            pass

# Classe para representar um foguete
class Rocket:
    def __init__(self):
        self.x = random.randint(0, width)
        self.y = height
        self.color = random.choice(colors)
        self.speed = random.randint(5, 10)
        self.exploded = False
        self.particles = []
        self.explode_height = random.randint(height // 2, height - 50)

    def move(self):
        if not self.exploded:
            self.y -= self.speed

            # Verifica se atingiu a altura da explosão
            if self.y < self.explode_height:
                self.explode()

        # Move as partículas da explosão
        for particle in self.particles:
            particle.move()

    def draw(self):
        if not self.exploded:
            pygame.draw.rect(screen, self.color, (self.x, int(self.y), 5, 10))
        else:
            for particle in self.particles:
                particle.draw()

    def explode(self):
        self.exploded = True

        # Cria partículas da explosão
        for _ in range(100):
            particle = Particle(self.x, self.y, self.color, self.explode_height)
            self.particles.append(particle)

rockets = []

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Cria novos foguetes aleatoriamente
    if random.randint(0, 4) == 0:
        rockets.append(Rocket())

    screen.fill(black)

    for rocket in rockets:
        rocket.move()
        rocket.draw()

    # Remove os foguetes que saíram da tela ou já explodiram completamente
    rockets = [rocket for rocket in rockets if not rocket.exploded or any(0 <= particle.y <= height for particle in rocket.particles)]

    pygame.display.flip()
    clock.tick(30)
