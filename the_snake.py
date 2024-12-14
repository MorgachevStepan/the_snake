import pygame
from random import randint

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """
        Инициализация игрового объекта.

        :param position: начальная позиция объекта (x, y)
        :param body_color: цвет объекта (R, G, B)
        """
        self.position = position
        self.body_color = body_color

    def draw(self, display):
        """
        Отрисовывает объект на экране.

        :param display: поверхность для отрисовки
        """
        pass

    def randomize_position(self):
        """Устанавливает случайную позицию объекта на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )


class Apple(GameObject):
    """Класс для объекта 'Яблоко'."""

    def __init__(self, position=(0, 0), body_color=APPLE_COLOR):
        """
        Инициализация яблока.

        :param position: начальная позиция яблока (x, y)
        :param body_color: цвет яблока
        """
        super().__init__(position, body_color)
        self.body_color = body_color
        self.randomize_position()

    def draw(self, display):
        """
        Отрисовывает яблоко на экране.

        :param display: поверхность для отрисовки
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(display, self.body_color, rect)
        pygame.draw.rect(display, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для объекта 'Змейка'."""

    def __init__(self, position=(0, 0), body_color=SNAKE_COLOR):
        """
        Инициализация змейки.

        :param position: начальная позиция змейки (x, y)
        :param body_color: цвет змейки
        """
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = body_color

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку на одну клетку в направлении движения."""
        head_x, head_y = self.positions[0]
        new_head = (
            head_x + self.direction[0] * GRID_SIZE,
            head_y + self.direction[1] * GRID_SIZE
        )

        # Телепортация при выходе за границы
        if new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])

        if new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        """Увеличивает длину змейки на один сегмент."""
        self.length += 1

    def draw(self, display):
        """
        Отрисовывает змейку на экране.

        :param display: поверхность для отрисовки
        """
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(display, self.body_color, rect)
            pygame.draw.rect(display, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(display, self.body_color, head_rect)
        pygame.draw.rect(display, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки в исходное."""
        self.randomize_position()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для изменения направления змейки.

    :param snake: объект змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """
    Главная функция игры.

    Инициализирует объекты и запускает игровой цикл.
    """
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
            5
        )

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
