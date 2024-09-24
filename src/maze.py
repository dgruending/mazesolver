import time

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
        win,
    ):
        self.cells = []
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._create_cells()

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
        print(f"New cell with ({x1}, {y1}) ({x2}, {y2})")
        self.cells[i][j]._top_left_point = Point(x1, y1)
        self.cells[i][j]._bottom_right_point = Point(x2, y2)
        self.cells[i][j].draw()
        self._animate()

        

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)
