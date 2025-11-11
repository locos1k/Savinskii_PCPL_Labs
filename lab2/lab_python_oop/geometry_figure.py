from abc import ABC, abstractmethod

class GeometryFigure(ABC):
    FIGURE_NAME: str = "Фигура"

    @classmethod
    def name(cls) -> str:
        return cls.FIGURE_NAME

    @abstractmethod
    def area(self) -> float:
        raise NotImplementedError

    def __repr__(self) -> str:
        return "<{0}>".format(self.name())