from .geometry_figure import GeometryFigure
from .color import FigureColor

class Rectangle(GeometryFigure):
    FIGURE_NAME = "Прямоугольник"

    def __init__(self, width: float, height: float, color: str):
        if width <= 0 or height <= 0:
            raise ValueError("Ширина и высота должны быть положительными.")
        self.width = float(width)
        self.height = float(height)
        self.color_obj = FigureColor(color)

    def area(self) -> float:
        return self.width * self.height

    def __repr__(self) -> str:
        return "{0}(w={1:.3f}, h={2:.3f}, color='{3}', area={4:.3f})".format(
            self.name(), self.width, self.height, self.color_obj.color, self.area()
        )