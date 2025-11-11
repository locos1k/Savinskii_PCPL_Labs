from .rectangle import Rectangle

class Square(Rectangle):
    FIGURE_NAME = "Квадрат"

    def __init__(self, side: float, color: str):
        if side <= 0:
            raise ValueError("Сторона должна быть положительной.")
        super().__init__(width=side, height=side, color=color)

    def __repr__(self) -> str:
        return "{0}(a={1:.3f}, color='{2}', area={3:.3f})".format(
            self.name(), self.width, self.color_obj.color, self.area()
        )