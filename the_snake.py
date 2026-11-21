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


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс объектов игры."""

    def __init__(self):
        """Задаёт начальную позицию и цвет объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Отрисовывает объект на игровом поле."""
        pass


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
        if self.position is None:
            return

        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


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

    def draw(self, tail=None):
        """Затирает след хвоста и рисует все сегменты змейки."""
        if tail is not None:
            tail_rect = pygame.Rect(tail, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, tail_rect)

        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запускает игру и обновляет её до закрытия окна."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

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
            tail = None

        snake.draw(tail)
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
