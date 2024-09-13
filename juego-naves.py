import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 700, 775
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego Naves")

# Cargar imágenes y escalarlas
player_image = pygame.image.load("imagenes/jugador.png")
player_image = pygame.transform.scale(player_image, (64, 80))

bullet_image = pygame.image.load("imagenes/bala.png")
bullet_image = pygame.transform.scale(bullet_image, (5, 40))

enemy_image = pygame.image.load("imagenes/enemigo.png")
enemy_image = pygame.transform.scale(enemy_image, (60, 44))

background_image = pygame.image.load("imagenes/fondo.png")
background_image = pygame.transform.scale(background_image, (width, height))

# Cargar sonidos
shoot_sound = pygame.mixer.Sound("sonidos/disparo.wav")
hit_sound = pygame.mixer.Sound("sonidos/golpe.WAV")
lose_life_sound = pygame.mixer.Sound("sonidos/vida_perdida.wav")

# Configurar fuente
game_font = pygame.font.Font("fuentes/PressStart2P-Regular.ttf", 24)

# Jugador
player_rect = player_image.get_rect()
player_rect.topleft = (width // 2 - player_rect.width // 2, height - player_rect.height - 10)
player_speed = 15

# Bala
bullet_speed = 10
bullets = []

# Enemigos
enemy_speed = 3
enemies = []

# Puntaje y vidas
score = 0
lives = 3

# Incremento de dificultad
enemy_spawn_rate = 5

# Estado del juego
game_over = False

# Reloj
clock = pygame.time.Clock()

# Mantener registro de las teclas presionadas
keys_pressed = {'left': False, 'right': False, 'up': False, 'down': False}

# Función para mostrar texto centrado en pantalla
def draw_text_centered(text, font, color, surface, x_center, y_center):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x_center, y_center))
    surface.blit(text_obj, text_rect)

# Bucle principal del juego
while True:
    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Manejar movimientos del jugador
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    keys_pressed['left'] = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    keys_pressed['right'] = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    keys_pressed['up'] = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    keys_pressed['down'] = True
                elif event.key == pygame.K_SPACE:
                    # Crear una nueva bala y reproducir sonido
                    bullet_rect = bullet_image.get_rect(center=(player_rect.centerx, player_rect.top))
                    bullets.append(bullet_rect)
                    shoot_sound.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    keys_pressed['left'] = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    keys_pressed['right'] = False
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    keys_pressed['up'] = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    keys_pressed['down'] = False

        # Aumentar dificultad cada 10 puntos
        if score > 0 and score % 5 == 0:
            enemy_speed = 3 + score // 10
            enemy_spawn_rate = 5 + score // 10

        # Actualizar posición del jugador
        if keys_pressed['left'] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys_pressed['right'] and player_rect.right < width:
            player_rect.x += player_speed
        if keys_pressed['up'] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys_pressed['down'] and player_rect.bottom < height:
            player_rect.y += player_speed

        # Generar enemigos aleatorios
        if random.randint(0, 100) < enemy_spawn_rate:
            enemy_rect = enemy_image.get_rect()
            enemy_rect.x = random.randint(0, width - enemy_rect.width)
            enemy_rect.top = 0
            enemies.append(enemy_rect)

        # Mover enemigos hacia abajo
        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.bottom > height:
                enemies.remove(enemy)
                lives -= 1  # El jugador pierde una vida si un enemigo llega al fondo
                lose_life_sound.play()

        # Actualizar posición de las balas
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Detectar colisiones de balas con enemigos
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1  # Aumentar el puntaje por cada enemigo eliminado
                    hit_sound.play()
                    break

        # Detectar colisiones del jugador con enemigos
        for enemy in enemies[:]:
            if player_rect.colliderect(enemy):
                enemies.remove(enemy)
                lives -= 1  # El jugador pierde una vida si un enemigo lo toca
                lose_life_sound.play()

        # Terminar el juego si el jugador se queda sin vidas
        if lives <= 0:
            game_over = True

        # Limpiar la pantalla con el fondo
        screen.blit(background_image, (0, 0))

        # Dibujar al jugador
        screen.blit(player_image, player_rect)

        # Dibujar las balas
        for bullet in bullets:
            screen.blit(bullet_image, bullet)

        # Dibujar enemigos
        for enemy in enemies:
            screen.blit(enemy_image, enemy)

        # Dibujar el puntaje en la esquina superior derecha
        score_text = game_font.render(f"Puntaje: {score}", True, (255, 255, 255))
        screen.blit(score_text, (width - 275, 10))

        # Dibujar las vidas en la esquina superior izquierda
        lives_text = game_font.render(f"Vidas: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))

    else:
        # Mostrar el fondo congelado con el mensaje de Game Over
        draw_text_centered(f"Game Over - Puntaje: {score}", game_font, (255, 0, 0), screen, width // 2, height // 2 - 50)
        draw_text_centered("Haz clic para cerrar", game_font, (255, 255, 255), screen, width // 2, height // 2 + 20)

        # Esperar que el jugador haga clic para salir
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()

    # Actualizar la pantalla
    pygame.display.flip()

    # Establecer límite de FPS
    clock.tick(25)
