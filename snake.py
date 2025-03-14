import pygame, random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Apple:
    def __init__(self):
        x = random.randint(0, int(SCREEN_WIDTH / 30) - 1)
        y = random.randint(0, int(SCREEN_HEIGHT / 30) - 1)
        self.rect = pygame.Rect(x * 30, y * 30, 30, 30)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)


class Snake:
    def __init__(self, spd, d, prev_d, body, colour):
        self.spd = spd
        self.d = d
        self.prev_d = prev_d
        self.body = body
        self.colour = colour
        self.rect = pygame.Rect((30 * start_x), (30 * start_y), 30, 30)

    def draw(self, surface):
        for body in self.body:
            pygame.draw.rect(surface, body.colour, pygame.Rect(body.x, body.y, 30, 30))
        pygame.draw.rect(surface, self.colour, self.rect)

    def update(self):
        int = 0
        for x in prev_coordinates:
            if int == 0:
                prev_coordinates[int][0] = self.rect.x
                prev_coordinates[int][1] = self.rect.y
            else:
                prev_coordinates[int][0] = self.body[int].x
                prev_coordinates[int][1] = self.body[int].y
            int += 1

        if self.d == 1:
            self.rect.y -= self.spd
        elif self.d == -1:
            self.rect.y += self.spd
        elif self.d == 2:
            self.rect.x += self.spd
        elif self.d == -2:
            self.rect.x -= self.spd

        loc = 0
        for body in snake.body:
            body.x = prev_coordinates[loc - 1][0]
            body.y = prev_coordinates[loc - 1][1]
            loc += 1

        for a in self.body:
            a.rect.x = a.x
            a.rect.y = a.y

    def d_change(self, d):
        if d == -self.prev_d:
            pass
        else:
            snake.d = d

    def is_out_of_bounds(self):
        return (self.rect.x >= SCREEN_WIDTH or self.rect.x < 0) or (self.rect.y >= SCREEN_HEIGHT or self.rect.y < 0)


class Snake_Body:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.colour = colour


class Game:
    def __init__(self, snake, apple, surface, state):
        self.snake = snake
        self.apple = apple
        self.surface = surface
        self.state = state

    def update(self):
        if self.snake.is_out_of_bounds():
            self.state = 1

        if is_touching(self.snake, self.apple):
            prev_coordinates.append([self.snake.body[len(self.snake.body) - 1].x, self.snake.body[len(self.snake.body) - 1].y])
            snake.body.append(Snake_Body(self.snake.body[len(self.snake.body) - 1].x, self.snake.body[len(self.snake.body) - 1].y, (154,205,50)))
            self.apple = Apple()

        for i in self.snake.body:
            if i == self.snake.body[0]:
                pass
            elif pygame.Rect.colliderect(self.snake.rect, i.rect):
                self.state = 1

        self.surface.fill((0, 0, 0))
        draw_grid()
        self.snake.update()
        self.snake.draw(self.surface)
        self.apple.draw(self.surface)
        score = len(snake.body) - 1
        message("Score:" + str(score), (200, 100, 134), (0, 0))
        pygame.display.flip()
        pygame.display.update()

    def restart(self):
        start_x = random.randint(0, 18)
        start_y = random.randint(0, 16)
        self.state = 0
        self.snake.rect.x = start_x * 30
        self.snake.rect.y = start_y * 30
        self.snake.d = 0
        self.apple = Apple()
        self.snake.body = [Snake_Body(10, 10, (154,205,50))]
        prev_coordinates = [[self.snake.rect.x, self.snake.rect.y]]

    def end_screen(self):
        message("press space to play again", (255, 0, 0), (SCREEN_WIDTH - 500, 0))
        pygame.display.update()


    def exit(self):
        pygame.quit()
        quit()
        running = False
def message(msg, colour, loc):
    words = pygame.font.SysFont(None, 50).render(msg, True, colour)
    window.blit(words, loc)


def is_touching(object, object1):
    return pygame.Rect.colliderect(object.rect, object1.rect)


def draw_grid():
    block_size = 30
    for x in range(0, SCREEN_WIDTH, block_size):
        for y in range(0, SCREEN_HEIGHT, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(window, (200, 200, 200), rect, 1)


start_x = random.randint(0, int(SCREEN_WIDTH / 30) - 1)
start_y = random.randint(0, int(SCREEN_HEIGHT / 30) - 1)

snake_body = [Snake_Body((30 * start_x), (30 * start_y), (154,205,50))]
snake = Snake(30, 0, 1, snake_body, (61, 145, 64))
apple = Apple()

prev_coordinates = [[snake.rect.x, snake.rect.y]]
running = True
game = Game(snake, apple, window, 0)

while running:
    if game.state == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.exit()
            if event.type == pygame.KEYDOWN:
                game.snake.prev_d = game.snake.d
                if event.key == pygame.K_UP:
                    game.snake.d_change(1)
                if event.key == pygame.K_DOWN:
                    game.snake.d_change(-1)
                if event.key == pygame.K_RIGHT:
                    game.snake.d_change(2)
                if event.key == pygame.K_LEFT:
                    game.snake.d_change(-2)
        game.update()
        clock.tick(10)
    elif game.state == 1:
        game.end_screen()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.restart()
                    prev_coordinates = [[game.snake.rect.x, game.snake.rect.y]]
            if event.type == pygame.QUIT:
                game.exit()


