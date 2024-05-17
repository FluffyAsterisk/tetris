from settings import *
from colors import Colors
from position import Position

class Block:
    def __init__(self, id : int):
        self.id = id
        self.cells = {}
        self.cell_size = 30
        self.rotation_state = 0
        self.offset = [0, 0]
        self.colors = Colors.get_cell_colors()

    def draw(self, offset_x, offset_y) -> None:
        tiles = self.get_cell_positions()
        
        for tile in tiles:
            tile_rect = pygame.Rect(tile.col * self.cell_size + 1 + offset_x, tile.row * self.cell_size + 1 + offset_y,
            self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(pygame.display.get_surface(), self.colors[self.id], tile_rect)
    
    def move(self, x : int, y : int):
        self.offset[0] += y
        self.offset[1] += x

    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state <= 0:
            self.rotation_state = len(self.cells) - 1

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for pos in tiles:
            pos = Position(pos.row + self.offset[0], pos.col + self.offset[1])
            moved_tiles.append(pos)
        return moved_tiles

