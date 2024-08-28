import random
import curses

# Define as constantes
WIDTH = 40
HEIGHT = 20
SNAKE_CHAR = 'O'
FOOD_CHAR = 'X'
EMPTY_CHAR = ' '

# Função para iniciar o jogo
def init_game():
    # Inicializa a tela do curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)

    # Cria a cobra
    snake = [(WIDTH // 2, HEIGHT // 2)]

    # Cria a comida
    food = generate_food(snake)

    # Retorna a tela do curses, a cobra, a comida e a direção inicial
    return stdscr, snake, food, curses.KEY_RIGHT

# Função para gerar comida aleatoriamente
def generate_food(snake):
    while True:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        if (x, y) not in snake:
            return (x, y)

# Função para mover a cobra
def move_snake(snake, direction):
    # Calcula a nova cabeça da cobra com base na direção
    head_x, head_y = snake[0]
    if direction == curses.KEY_UP:
        new_head = (head_x, head_y - 1)
    elif direction == curses.KEY_DOWN:
        new_head = (head_x, head_y + 1)
    elif direction == curses.KEY_LEFT:
        new_head = (head_x - 1, head_y)
    elif direction == curses.KEY_RIGHT:
        new_head = (head_x + 1, head_y)

    # Adiciona a nova cabeça à cobra
    snake.insert(0, new_head)

    # Remove a cauda se a cobra não comeu comida
    if new_head != food:
        snake.pop()

    return snake

# Função para desenhar o jogo na tela
def draw_game(stdscr, snake, food):
    # Limpa a tela
    stdscr.clear()

    # Desenha a cobra
    for x, y in snake:
        stdscr.addstr(y, x, SNAKE_CHAR)

    # Desenha a comida
    stdscr.addstr(food[1], food[0], FOOD_CHAR)

    # Desenha as bordas
    for x in range(WIDTH):
        stdscr.addstr(0, x, EMPTY_CHAR)
        stdscr.addstr(HEIGHT - 1, x, EMPTY_CHAR)
    for y in range(HEIGHT):
        stdscr.addstr(y, 0, EMPTY_CHAR)
        stdscr.addstr(y, WIDTH - 1, EMPTY_CHAR)

    # Atualiza a tela
    stdscr.refresh()

# Função principal do jogo
def main():
    # Inicializa o jogo
    stdscr, snake, food, direction = init_game()

    # Loop do jogo
    while True:
        # Lê a entrada do usuário
        key = stdscr.getch()

        # Verifica se o usuário pressionou uma tecla válida
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            # Atualiza a direção da cobra
            direction = key

        # Move a cobra
        snake = move_snake(snake, direction)

        # Verifica se a cobra comeu a comida
        if snake[0] == food:
            # Gera nova comida
            food = generate_food(snake)

        # Verifica se a cobra colidiu com ela mesma ou com a borda
        if (
            snake[0][0] < 0
            or snake[0][0] >= WIDTH
            or snake[0][1] < 0
            or snake[0][1] >= HEIGHT
            or snake[0] in snake[1:]
        ):
            # Finaliza o jogo
            break

        # Desenha o jogo
        draw_game(stdscr, snake, food)

    # Finaliza o jogo
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

    # Exibe a pontuação final
    print(f"Game Over! Pontuação: {len(snake) - 1}")

# Chama a função principal do jogo
if __name__ == "__main__":
    main()