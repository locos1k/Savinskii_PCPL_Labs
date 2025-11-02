import sys
import math

class BiquadraticRoots:
    def __init__(self):
        self.coef_A = 0.0
        self.coef_B = 0.0
        self.coef_C = 0.0
        self.num_roots = 0
        self.roots_list = []

    def get_coef(self, index, prompt):
        tried_argv = False
        while True:
            value_str = None
            if not tried_argv and len(sys.argv) > index:
                value_str = sys.argv[index]
                tried_argv = True
            else:
                print(prompt)
                value_str = input()

            try:
                return float(value_str.replace(',', '.'))
            except Exception:
                print(f"Некорректный ввод ({value_str}). Попробуйте ещё раз.")

    def get_coefs(self):
        self.coef_A = self.get_coef(1, 'Введите коэффициент A:')
        self.coef_B = self.get_coef(2, 'Введите коэффициент B:')
        self.coef_C = self.get_coef(3, 'Введите коэффициент C:')

    def calculate_roots(self):
        self.roots_list = []
        a = self.coef_A
        b = self.coef_B
        c = self.coef_C

        eps = 1e-15
        if abs(a) < eps:
            if abs(b) < eps:
                self.num_roots = 0
                return
            y = -c / b
            if y > -eps:
                y = max(0.0, y)
                r = math.sqrt(y)
                if r == 0.0:
                    self.roots_list.append(0.0)
                else:
                    self.roots_list.extend([-r, r])
            self.roots_list = sorted(set(round(x, 12) for x in self.roots_list))
            self.num_roots = len(self.roots_list)
            return

        D = b*b - 4*a*c
        if D < 0.0:
            self.num_roots = 0
            return
        elif abs(D) <= eps:
            y = -b / (2.0*a)
            if y > -eps:
                y = max(0.0, y)
                r = math.sqrt(y)
                if r == 0.0:
                    self.roots_list.append(0.0)
                else:
                    self.roots_list.extend([-r, r])
        else:
            sqD = math.sqrt(D)
            y1 = (-b + sqD) / (2.0*a)
            y2 = (-b - sqD) / (2.0*a)
            for y in (y1, y2):
                if y > -eps:
                    y = max(0.0, y)
                    r = math.sqrt(y)
                    if r == 0.0:
                        self.roots_list.append(0.0)
                    else:
                        self.roots_list.extend([-r, r])

        self.roots_list = sorted(set(round(x, 12) for x in self.roots_list))
        self.num_roots = len(self.roots_list)

    def print_roots(self):
        if self.num_roots != len(self.roots_list):
            print(('Ошибка. Уравнение содержит {} действительных корней, ' + 
                  'но было вычислено {} корней.').format(self.num_roots, len(self.roots_list)))
        else:
            if self.num_roots == 0:
                print('Нет корней')
            elif self.num_roots == 1:
                print('Один корень: {}'.format(self.roots_list[0]))
            elif self.num_roots == 2:
                print('Два корня: {} и {}'.format(self.roots_list[0], self.roots_list[1]))
            elif self.num_roots == 3:
                print('Три корня: {}, {}, {}'.format(self.roots_list[0], self.roots_list[1], self.roots_list[2]))
            elif self.num_roots == 4:
                print('Четыре корня: {}, {}, {}, {}'.format(self.roots_list[0], self.roots_list[1], self.roots_list[2], self.roots_list[3]))
            else:
                print('Корней: {}: {}'.format(self.num_roots, self.roots_list))

def main():
    r = BiquadraticRoots()
    r.get_coefs()
    r.calculate_roots()
    r.print_roots()

if __name__ == "__main__":
    main()