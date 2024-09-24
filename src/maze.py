import time
import random

from cell import Cell
from point import Point

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed = None,
    ):
        self.cells = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        for _ in range(self.num_cols):
            col_cells = []
            for _ in range(self.num_rows):
                col_cells.append(Cell(self._win))
            self.cells.append(col_cells)
        for col in range(self.num_cols):
            for row in range(self.num_rows):
                self._draw_cells(col, row)

    def _draw_cells(self, i, j):
        if self._win is None:
            return
        x1 = self.x1 + i * self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y
        self.cells[i][j]._top_left_point = Point(x1, y1)
        self.cells[i][j]._bottom_right_point = Point(x2, y2)
        self.cells[i][j].draw()
        self._animate()

        

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.03)

    def _break_entrance_and_exit(self):
        top_left_cell = self.cells[0][0]
        top_left_cell.has_top_wall = False
        top_left_cell.draw()
        
        bottom_right_cell = self.cells[-1][-1]
        bottom_right_cell.has_down_wall = False
        bottom_right_cell.draw()

    def _break_walls_r(self, i, j):
        self.cells[i][j]._visited = True
        while True:
            to_visit = []
            if i > 0:
                if not self.cells[i-1][j]._visited:
                    to_visit.append((i-1, j, "left"))
            if i < self.num_cols - 1:
                if not self.cells[i+1][j]._visited:
                    to_visit.append((i+1, j, "right"))
            if j > 0:
                if not self.cells[i][j-1]._visited:
                    to_visit.append((i, j-1, "top"))
            if j < self.num_rows - 1:
                if not self.cells[i][j+1]._visited:
                    to_visit.append((i, j+1, "down"))

            if len(to_visit) == 0:
                self.cells[i][j].draw()
                self._animate()
                return
            
            new_direction = random.choice(to_visit)
            to_visit.remove(new_direction)
            new_i, new_j = new_direction[:2]
            match new_direction[2]:
                case "left":
                    self.cells[i][j].has_left_wall = False
                    self.cells[new_i][new_j].has_right_wall = False
                case "right":
                    self.cells[i][j].has_right_wall = False
                    self.cells[new_i][new_j].has_left_wall = False
                case "top":
                    self.cells[i][j].has_top_wall = False
                    self.cells[new_i][new_j].has_down_wall = False
                case "down":
                    self.cells[i][j].has_down_wall = False
                    self.cells[new_i][new_j].has_top_wall = False

            self._break_walls_r(new_i, new_j)


    def _reset_cells_visited(self):
        for cells in self.cells:
            for cell in cells:
                cell._visited = False

    def solve(self):
        return self._solve_r(0,0)
    
    def _solve_r(self, i, j):
        self._animate()
        current_cell = self.cells[i][j]
        current_cell._visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True
        # Right
        if i < self.num_cols - 1 and not self.cells[i+1][j]._visited and not current_cell.has_right_wall:
            current_cell.draw_move(self.cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            current_cell.draw_move(self.cells[i+1][j], undo=True)
        # Down
        if j < self.num_rows - 1 and not self.cells[i][j+1]._visited and not current_cell.has_down_wall:
            current_cell.draw_move(self.cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            current_cell.draw_move(self.cells[i][j+1], undo=True)
        # Left
        if i > 0 and not self.cells[i-1][j]._visited and not current_cell.has_left_wall:
            current_cell.draw_move(self.cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            current_cell.draw_move(self.cells[i-1][j], undo=True)
        # Down
        if j > 0 and not self.cells[i][j-1]._visited and not current_cell.has_top_wall:
            current_cell.draw_move(self.cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            current_cell.draw_move(self.cells[i][j-1], undo=True)
        
        return False