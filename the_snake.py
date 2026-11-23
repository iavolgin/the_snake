from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
KEY_DIRECTIONS = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def draw_cell(position, color, border_color=BORDER_COLOR):
    """Рисует клетку заданным цветом и добавляет обводку, если она задана."""
    rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, color, rect)
    if border_color is not None:
        pygame.draw.rect(screen, border_color, rect, 1)


class GameObject:
    """Базовый класс объектов игры."""

    def __init__(self):
        """Задаёт начальную позицию и цвет объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Отрисовывает объект на игровом поле."""
        raise NotImplementedError


class Apple(GameObject):
    """Яблоко, которое появляется в случайной клетке поля."""

    def __init__(self, occupied_positions=()):
        """Задаёт цвет яблока и выбирает его начальную позицию."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=()):
        """Выбирает случайную свободную клетку, если она есть."""
        occupied = set(occupied_positions)
        free_positions = [
            (x, y)
            for x in range(0, SCREEN_WIDTH, GRID_SIZE)
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE)
            if (x, y) not in occupied
        ]
        self.position = choice(free_positions) if free_positions else None

    def draw(self):
        """Рисует яблоко с обводкой в его клетке."""
        if self.position is not None:
            draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Змейка, тело которой хранится списком координат клеток."""

    def __init__(self):
        """Создаёт зелёную змейку в начальном состоянии."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def update_direction(self):
        """Применяет выбранное направление движения."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку и возвращает координаты снятого хвоста."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_x = (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))

        if len(self.positions) > self.length:
            return self.positions.pop()
        return None

    def draw(self):
        """Рисует голову змейки в её текущей клетке."""
        draw_cell(self.get_head_position(), self.body_color)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Возвращает змейку длиной в одну клетку в центр поля."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Обрабатывает стрелки и закрытие окна игры."""
    direction_x, direction_y = game_object.direction
    opposite_direction = (-direction_x, -direction_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            direction = KEY_DIRECTIONS.get(event.key)
            if direction is not None and direction != opposite_direction:
                game_object.next_direction = direction


def main():
    """Запускает игру и обновляет её до закрытия окна."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake.draw()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        tail = snake.move()

        head = snake.get_head_position()
        if head == apple.position:
            snake.length += 1
            snake.positions.append(tail)
            tail = None
            apple.randomize_position(snake.positions)

        if head in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        elif tail is not None:
            draw_cell(tail, BOARD_BACKGROUND_COLOR, border_color=None)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
