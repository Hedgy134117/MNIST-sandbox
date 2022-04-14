import pygame


pygame.init()

width, height = (800, 600)
window = pygame.display.set_mode((width, height))

is_running = True

step = 50


class Cell(pygame.Rect):
    def __init__(self, x, y, width, height, color):
        pygame.Rect.__init__(self, x, y, width, height)
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def display(self):
        pygame.draw.rect(window, self.color, self.rect)


class Grid:
    def __init__(self, step) -> None:
        self.step = step
        self.rects = self.create_grid()

    def create_grid(self) -> list:
        rects = []
        for y in range(0, height, self.step):
            for x in range(0, width, self.step):
                rects.append(Cell(x, y, self.step, self.step, pygame.Color("#FFFFFF")))
        return rects

    def draw_grid(self) -> None:
        self.draw_grid_lines()
        for rect in self.rects:
            rect.display()

    def draw_grid_lines(self) -> None:
        for y in range(0, height, self.step):
            pygame.draw.line(window, pygame.Color("#FFFFFF"), (0, y), (width, y))

        for x in range(0, width, self.step):
            pygame.draw.line(window, pygame.Color("#FFFFFF"), (x, 0), (x, height))

    def get_mouse_index(self) -> int:
        for cell in self.rects:
            if cell.collidepoint(pygame.mouse.get_pos()):
                return self.rects.index(cell)

    def highlight_cell(self, index) -> None:
        for rect in self.rects:
            rect.color = pygame.Color("#FFFFFF")
        self.rects[index].color = pygame.Color("#000000")


grid = Grid(50)

while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    # window.blit(background, (0, 0))

    grid.draw_grid()
    grid.highlight_cell(grid.get_mouse_index())

    pygame.display.update()
