#!/usr/bin/env python3
import curses
import time
import random
import math

# ==========================
#   CONSTANTES / CONFIG
# ==========================
LAUNCH_INTERVAL   = 2.0   # Intervalo (segundos) entre lotes de foguetes
ROCKETS_PER_BATCH = 8     # Quantos foguetes lançar a cada lote
ASCENT_SPEED      = 1     # Velocidade de subida (linhas por frame)
EXPLOSION_FRAMES  = 12    # Número de quadros da animação de explosão
EXPLOSION_RADIUS  = 8     # Raio máximo dos feixes na explosão
NUM_RAYS          = 12    # Quantidade de feixes (linhas radiais) - MENOR para melhor visibilidade
FRAME_DELAY       = 0.05  # Atraso (segundos) entre frames
POST_EXP_DELAY    = 0.5   # Pausa após a explosão
TOTAL_DURATION    = 60.0  # Duração total (segundos)

# Cada foguete é um dicionário:
# {
#   "x": posição horizontal,
#   "y": posição vertical,
#   "explosion_y": altura em que começa a explodir,
#   "state": "ascend" | "explode" | "done",
#   "explosion_frame": contador de frames da explosão,
#   "exploded_at": frame em que iniciou a explosão
# }

def draw_rocket(stdscr, y, x):
    """Desenha um foguete simples."""
    try:
        stdscr.addstr(y, x, "|")
    except:
        pass

def draw_circle_of_rays(stdscr, center_y, center_x, radius, num_rays, color_pair=0):
    """
    Desenha um “círculo” feito de várias linhas radiais (feixes),
    sem pular a região central. Assim, o centro terá maior densidade de asteriscos.
    
    - `num_rays`: quantas linhas radiais igualmente espaçadas em 360°.
    - `radius`: comprimento máximo de cada feixe.
    """
    for i in range(num_rays):
        angle = 2 * math.pi * i / num_rays
        # Desenha um feixe do centro (r=1) até o raio máximo.
        for r in range(1, radius + 1):
            dx = int(r * math.cos(angle))
            dy = int(r * math.sin(angle))
            try:
                stdscr.addstr(center_y + dy, center_x + dx, "*", curses.color_pair(color_pair))
            except:
                pass

def update_rocket(rocket, frame_count):
    """
    Atualiza o estado do foguete:
      - "ascend": vai subindo até atingir 'explosion_y', então muda para "explode".
      - "explode": incrementa explosion_frame até passar de EXPLOSION_FRAMES;
                   depois aguarda POST_EXP_DELAY e marca como "done".
    """
    if rocket["state"] == "ascend":
        rocket["y"] -= ASCENT_SPEED
        if rocket["y"] <= rocket["explosion_y"]:
            rocket["state"] = "explode"
            rocket["explosion_frame"] = 0
            rocket["exploded_at"] = frame_count

    elif rocket["state"] == "explode":
        rocket["explosion_frame"] += 1
        if rocket["explosion_frame"] > EXPLOSION_FRAMES:
            frames_since_explode = frame_count - rocket["exploded_at"]
            time_since_explode = frames_since_explode * FRAME_DELAY
            if time_since_explode >= (EXPLOSION_FRAMES * FRAME_DELAY + POST_EXP_DELAY):
                rocket["state"] = "done"

def draw_rocket_or_explosion(stdscr, rocket):
    """
    Desenha o foguete se estiver subindo ou os feixes radiais se estiver explodindo.
    Na explosão, o raio cresce na primeira metade dos frames e encolhe na segunda.
    """
    if rocket["state"] == "ascend":
        draw_rocket(stdscr, rocket["y"], rocket["x"])
    elif rocket["state"] == "explode":
        i = rocket["explosion_frame"]
        half_frames = EXPLOSION_FRAMES // 2

        # Raio cresce até a metade dos frames, depois diminui
        if i <= half_frames:
            current_radius = int(EXPLOSION_RADIUS * i / half_frames)
        else:
            current_radius = int(EXPLOSION_RADIUS * (EXPLOSION_FRAMES - i) / half_frames)

        # Seleciona uma cor aleatória
        color_pair = random.randint(1, 6)

        # Desenha o "círculo" de feixes
        draw_circle_of_rays(
            stdscr,
            rocket["explosion_y"],
            rocket["x"],
            current_radius,
            NUM_RAYS,
            color_pair
        )

def spawn_rocket(stdscr):
    """Cria um foguete com posição x aleatória e altura de explosão aleatória."""
    max_y, max_x = stdscr.getmaxyx()
    x = random.randint(2, max_x - 2)
    y = max_y - 2
    explosion_y = random.randint(max_y // 4, max_y // 2)
    return {
        "x": x,
        "y": y,
        "explosion_y": explosion_y,
        "state": "ascend",
        "explosion_frame": 0,
        "exploded_at": 0
    }

def spawn_rockets(stdscr, how_many=3):
    """Cria 'how_many' foguetes ao mesmo tempo (um lote)."""
    return [spawn_rocket(stdscr) for _ in range(how_many)]

def main(stdscr):
    # Configurações do curses
    curses.curs_set(0)
    stdscr.nodelay(True)  # getch() não bloqueante

    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)

    rockets = []
    start_time = time.time()
    last_spawn_time = start_time
    frame_count = 0

    while True:
        # Se o usuário pressionar uma tecla, encerramos
        c = stdscr.getch()
        if c != -1:
            break

        current_time = time.time()
        elapsed = current_time - start_time

        # Após TOTAL_DURATION segundos, paramos
        if elapsed >= TOTAL_DURATION:
            break

        # A cada LAUNCH_INTERVAL, lançamos mais foguetes
        if current_time - last_spawn_time >= LAUNCH_INTERVAL:
            rockets.extend(spawn_rockets(stdscr, how_many=ROCKETS_PER_BATCH))
            last_spawn_time = current_time

        stdscr.clear()

        # Atualiza e desenha cada foguete
        for rocket in rockets:
            if rocket["state"] != "done":
                update_rocket(rocket, frame_count)
            draw_rocket_or_explosion(stdscr, rocket)

        # Remove foguetes concluídos
        rockets = [rk for rk in rockets if rk["state"] != "done"]

        stdscr.refresh()
        time.sleep(FRAME_DELAY)
        frame_count += 1

    # Mensagem final
    stdscr.nodelay(False)
    msg = "Pressione qualquer tecla para sair..."
    max_y, max_x = stdscr.getmaxyx()
    stdscr.addstr(max_y // 2, max_x // 2 - len(msg)//2, msg)
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)

