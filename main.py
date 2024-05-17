from settings import *
from blocks import *
from grid import Grid
from colors import Colors
import random

class Game():
    screens = {
        1 : 'main_menu',
        2 : 'game',
        3 : 'settings'
    }

    isClick = False

    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Tetris')

        self.GAME_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.GAME_UPDATE, 500)

        self.font = pygame.font.SysFont('Arial', 27)
        self.clock = pygame.time.Clock()

        self.cur_screen = 1

        self.grid = Grid()
        self.grid_pos = (self.display_surface.get_size()[0] // 2 - self.grid.cell_size * self.grid.num_cols // 2, self.display_surface.get_size()[1] // 2 - self.grid.cell_size * self.grid.num_rows // 2)
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), IBlock(), ZBlock()]
        self.current_block = self.get_rand_block()
        self.next_block = self.get_rand_block()

        self.score = 0
        self.level = 1


    def __render_text(self, text, font, color, x, y):
            textobj = font.render(text, 1, color)
            textrect = textobj.get_rect()
            textrect.topleft = (x,y)
            self.display_surface.blit(textobj, textrect)


    def get_rand_block(self) -> Block:
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), IBlock(), ZBlock()]

        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def check_btn_clicked(self, btn) -> bool:
        mx, my = pygame.mouse.get_pos()
        if btn.collidepoint((mx, my)) and self.isClick:
            return True
        return False

    def block_collisde(self) -> bool:
        tiles = self.current_block.get_cell_positions()

        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.col) or self.grid.grid[tile.row][tile.col]:
                return False
        
        return True

    def is_line_full(self):
        score_mult = 0
        # Counter for non zero grid cells
        cell_cnt = 0
        full_lines = 0
        new_grid = []
        empty_line = [0 for i in range(self.grid.num_cols)]

        for row in self.grid.grid:
            for col in row:
                if col == 0:
                    cell_cnt = 0
                    new_grid.append(row)
                    break

                cell_cnt += 1
            
                if cell_cnt == self.grid.num_cols:
                    score_mult += 1
                    new_grid.insert(0, empty_line)
                    full_lines += 1
                    cell_cnt = 0
        
        self.grid.grid = new_grid
                    
        if full_lines:
            self.count_score(score_mult)

    def count_score(self, score_mult : int) -> None:
        self.score += (100 + score_mult) * score_mult
    
    def move_left(self) -> None:
        self.current_block.move(-1, 0)
        if self.block_collisde() == False:
            self.current_block.move(1, 0)

    def move_right(self) -> None:
        self.current_block.move(1, 0)
        if self.block_collisde() == False:
            self.current_block.move(-1, 0)

    def move_down(self) -> None:
        self.current_block.move(0, 1)
        if self.block_collisde() == False:
            self.current_block.move(0, -1)
            self.lock_block()
            self.is_line_full()
    
    def lock_block(self) -> None:
        tiles = self.current_block.get_cell_positions()
        for pos in tiles:
            self.grid.grid[pos.row][pos.col] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_rand_block()

    def rotate(self) -> None:
        self.current_block.rotate()
        if not self.block_collisde():
            self.current_block.undo_rotation()

    def game_logic(self) -> None:
        self.current_block.draw(self.grid_pos[0], self.grid_pos[1])

    def main_menu(self) -> None:
        self.display_surface.fill('grey')

        # Buttons width and height
        b_dimensions = (200, 50)

        # Place buttons in center
        b1_coord = (self.display_surface.get_size()[0] // 2 - b_dimensions[0] // 2, 100)
        b2_coord = (self.display_surface.get_size()[0] // 2 - b_dimensions[0] // 2, 200)
        
        button_1 = pygame.Rect(*b1_coord, *b_dimensions)
        button_2 = pygame.Rect(*b2_coord, *b_dimensions)

        # Draw buttons
        pygame.draw.rect(self.display_surface, (200, 50, 50), button_1, 0, 3)
        pygame.draw.rect(self.display_surface, (200, 50, 50), button_2, 0, 3)

        self.__render_text('Play', self.font, 'WHITE', *b1_coord)
        self.__render_text('Settings', self.font, 'WHITE', *b2_coord)
        
        if self.check_btn_clicked(button_1):
            self.cur_screen = 2

        if self.check_btn_clicked(button_2):
            self.cur_screen = 3

        self.isClick = False


    # Game screen
    def game(self):
        self.display_surface.fill('grey')
        self.grid.draw(self.grid_pos[0], self.grid_pos[1])

        self.__render_text(f'Score: {self.score}', self.font, 'WHITE', 70, 100)
        self.__render_text(f'Level: {self.level}', self.font, 'WHITE', 75, 150)

        self.game_logic()


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.isClick = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.rotate()
                    if event.key == pygame.K_DOWN:
                        self.move_down()
                    if event.key == pygame.K_LEFT:
                        self.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()

                if event.type == self.GAME_UPDATE:
                    self.move_down()
            
            # Draw current screen
            getattr(self, self.screens[self.cur_screen])()
            
            self.clock.tick(60)
            pygame.display.update()



if __name__ == '__main__':
    game = Game()
    game.run()
