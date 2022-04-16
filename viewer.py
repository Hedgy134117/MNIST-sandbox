import pygame
import numpy as np
import model


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
        for y in range(self.y, self.height + self.step, self.step):
            for x in range(self.x, self.width + self.step, self.step):
                rects.append(Cell(x, y, self.step, self.step, pygame.Color("#000000")))
        return rects

    def draw_grid(self) -> None:
        for rect in self.rects:
            rect.display()
        self.draw_border()

    def draw_border(self) -> None:
        pygame.draw.line(
            window,
            pygame.Color("#FFFFFF"),
            (self.x, self.y),
            (self.width + self.step, self.y),
        )
        pygame.draw.line(
            window,
            pygame.Color("#FFFFFF"),
            (self.width + self.step, self.y),
            (self.width + self.step, self.height + self.step),
        )
        pygame.draw.line(
            window,
            pygame.Color("#FFFFFF"),
            (self.width + self.step, self.height + self.step),
            (self.x, self.height + self.step),
        )
        pygame.draw.line(
            window,
            pygame.Color("#FFFFFF"),
            (self.x, self.height + self.step),
            (self.x, self.y),
        )

    def get_mouse_index(self) -> int:
        for cell in self.rects:
            if cell.collidepoint(pygame.mouse.get_pos()):
                return self.rects.index(cell)
        return 0

    def highlight_cell(self, index) -> None:
        self.rects[index - 29].color = pygame.Color("#FFFFFF")
        self.rects[index - 28].color = pygame.Color("#FFFFFF")
        self.rects[index - 27].color = pygame.Color("#FFFFFF")

        self.rects[index - 1].color = pygame.Color("#FFFFFF")
        self.rects[index].color = pygame.Color("#FFFFFF")
        self.rects[index + 1].color = pygame.Color("#FFFFFF")

        self.rects[index + 27].color = pygame.Color("#FFFFFF")
        self.rects[index + 28].color = pygame.Color("#FFFFFF")
        self.rects[index + 29].color = pygame.Color("#FFFFFF")

    def unhighlight_cell(self, index) -> None:
        self.rects[index].color = pygame.Color("#000000")

    def clear(self) -> None:
        for rect in self.rects:
            rect.color = pygame.Color("#000000")

    def generate_np_array(self) -> np.ndarray:
        rowLength = self.width // self.step
        rows = self.height // self.step
        arr = [[] for _ in range(rows)]
        i = 0
        rowI = 0
        for cell in self.rects:
            arr[rowI].append(((cell.color.r + cell.color.g + cell.color.b) // 255) / 3)
            i += 1
            if i >= rowLength:
                rowI += 1
                i = 0
        return np.asarray(arr)


step = 20
grid = Grid(step, step, 28 * step, 28 * step, step)


while is_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                model.predict(grid.generate_np_array())
            if event.key == pygame.K_BACKSPACE:
                grid.clear()

    # window.blit(background, (0, 0))

    grid.draw_grid()

    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        grid.highlight_cell(grid.get_mouse_index())
    elif mouse[2]:
        grid.unhighlight_cell(grid.get_mouse_index())

    pygame.display.update()
