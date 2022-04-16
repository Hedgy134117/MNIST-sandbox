import pygame


pygame.init()

width, height = (800, 600)
window = pygame.display.set_mode((width, height))

is_running = True


class Cell(pygame.Rect):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.color = color

    def display(self):
        pygame.draw.rect(window, self.color, super().copy())


class Grid:
    def __init__(self, x, y, width, height, step) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.step = step
        self.rects = self.create_grid()

    def create_grid(self) -> list:
        rects = []
        for y in range(self.y, self.height, self.step):
            for x in range(self.x, self.width, self.step):
                rects.append(Cell(x, y, self.step, self.step, pygame.Color("#000000")))
        return rects

    def draw_grid(self) -> None:
        for rect in self.rects:
            rect.display()
        self.draw_border()

    def draw_border(self) -> None:
        pygame.draw.line(
            window, pygame.Color("#FFFFFF"), (self.x, self.y), (self.width, self.y)
        )
        pygame.draw.line(
            window,
            pygame.Color("#FFFFFF"),
            (self.width, self.y),
            (self.width, self.height),
        )
        pygame.draw.line(
            window,
            pygame.Color("#FFFFFF"),
            (self.width, self.height),
            (self.x, self.height),
        )
        pygame.draw.line(
            window, pygame.Color("#FFFFFF"), (self.x, self.height), (self.x, self.y)
        )

    def get_mouse_index(self) -> int:
        for cell in self.rects:
            if cell.collidepoint(pygame.mouse.get_pos()):
                return self.rects.index(cell)
        return 0

    def highlight_cell(self, index) -> None:
        self.rects[index].color = pygame.Color("#FFFFFF")

    def unhighlight_cell(self, index) -> None:
        self.rects[index].color = pygame.Color("#000000")


step = 10
grid = Grid(step, step, 28 * step, 28 * step, 10)

while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # window.blit(background, (0, 0))

    grid.draw_grid()

    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        grid.highlight_cell(grid.get_mouse_index())
    elif mouse[2]:
        grid.unhighlight_cell(grid.get_mouse_index())

    pygame.display.update()
