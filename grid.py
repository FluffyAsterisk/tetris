from settings import *
from colors import Colors

class Grid:
    def __init__(self):
        self.__num_rows = 20
        self.__num_cols = 10
        self.__cell_size = 30
        self.grid = [[0 for j in range(self.__num_cols)] for i in range(self.__num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self) -> None:
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                print(self.grid[row][col], end = " ")
            print()
            
    # Offset is coords
    def draw(self, offset_x, offset_y) -> None:
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_val = self.grid[row][col]
                cell_rect = pygame.Rect(col*self.cell_size + 1 + offset_x, row*self.cell_size + 1 + offset_y, self.cell_size-1, self.cell_size-1)
                pygame.draw.rect(pygame.display.get_surface(), self.colors[cell_val], cell_rect)
                

    def is_inside(self, row, col) -> bool:
        if row >= 0 and row < self.num_rows  and col >= 0 and col < self.num_cols:
            return True
        return False

    @property
    def num_rows(self) -> int:
        return self.__num_rows

    @property
    def num_cols(self) -> int:
        return self.__num_cols

    @property
    def cell_size(self) -> int:
        return self.__cell_size


