import math
from .geometry_figure import GeometryFigure
from .color import FigureColor

class Circle(GeometryFigure):
    FIGURE_NAME = "Круг"

    def __init__(self, radius: float, color: str):
        if radius <= 0:
            raise ValueError("Радиус должен быть положительным.")
        self.radius = float(radius)
        self.color_obj = FigureColor(color)

    def area(self) -> float:
        return math.pi * (self.radius ** 2)

    def __repr__(self) -> str:
        return "{0}(r={1:.3f}, color='{2}', area={3:.3f})".format(
            self.name(), self.radius, self.color_obj.color, self.area()
        )