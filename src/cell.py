from point import Point
from line import Line

class Cell():
    def __init__(self, window, top_left_point=Point(0,0), bottom_right_point=Point(0,0)):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_down_wall = True
        self._top_left_point = top_left_point
        self._bottom_right_point =bottom_right_point
        self._win = window

    def draw(self, fill_color = "black"):
        print("Draw for ", self)
        if self.has_left_wall:
            self._win.draw_line(Line(self._top_left_point, Point(self._top_left_point.x, self._bottom_right_point.y)), fill_color)
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._bottom_right_point.x, self._top_left_point.y), self._bottom_right_point), fill_color)
        if self.has_top_wall:
            self._win.draw_line(Line(self._top_left_point, Point(self._bottom_right_point.x, self._top_left_point.y)), fill_color)
        if self.has_down_wall:
            self._win.draw_line(Line(Point(self._top_left_point.x, self._bottom_right_point.y), self._bottom_right_point), fill_color)

    def center(self):
        center = Point((self._top_left_point.x + self._bottom_right_point.x) / 2, (self._top_left_point.y + self._bottom_right_point.y) / 2)
        return center
    
    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"
        self._win.draw_line(Line(self.center(), to_cell.center()), color)

    def __repr__(self) -> str:
        return f"Top_left: {self._top_left_point}, Bottom_right: {self._bottom_right_point}"