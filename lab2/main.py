from lab_python_oop import Rectangle, Circle, Square
from tabulate import tabulate
import sys

def build_figures(N: int):
    rect = Rectangle(width=N, height=N, color="синий")
    circ = Circle(radius=N, color="зеленый")
    sqr = Square(side=N, color="красный")
    return rect, circ, sqr

def print_info(figures):
    for f in figures:
        print(repr(f))

    rows = []
    for f in figures:
        rows.append([f.name(), repr(f)])
    print("\nТаблица (tabulate):")
    print(tabulate(rows, headers=["Фигура", "__repr__"], tablefmt="github"))

def main():
    if len(sys.argv) > 1:
        try:
            N = int(sys.argv[1])
        except ValueError:
            print("Первый аргумент должен быть целым числом. Пример: python main.py 7")
            return
    else:
        N = 21

    figures = build_figures(N)
    print_info(figures)

if __name__ == "__main__":
    main()