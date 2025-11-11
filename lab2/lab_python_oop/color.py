class FigureColor:

    def __init__(self, color: str):
        if not isinstance(color, str) or not color.strip():
            raise ValueError("Цвет должен быть непустой строкой.")
        self.color = color.strip()

    def __repr__(self) -> str:
        return "{0}".format(self.color)