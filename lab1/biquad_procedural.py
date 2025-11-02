import sys
import math

def get_coef(index, prompt):
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

def get_coefs():
    a = get_coef(1, 'Введите коэффициент A:')
    b = get_coef(2, 'Введите коэффициент B:')
    c = get_coef(3, 'Введите коэффициент C:')
    return a, b, c

def solve_biquadratic(a, b, c):
    roots = []
    eps = 1e-15

    if abs(a) < eps:
        if abs(b) < eps:
            return 0, roots
        y = -c / b
        if y > -eps:
            y = max(0.0, y)
            r = math.sqrt(y)
            if r == 0.0:
                roots.append(0.0)
            else:
                roots.extend([-r, r])
        return len(roots), roots

    D = b*b - 4*a*c
    if D < 0.0:
        return 0, roots
    elif abs(D) <= eps:
        y = -b / (2.0*a)
        if y > -eps:
            y = max(0.0, y)
            r = math.sqrt(y)
            if r == 0.0:
                roots.append(0.0)
            else:
                roots.extend([-r, r])
    else:
        sqD = math.sqrt(D)
        y1 = (-b + sqD) / (2.0*a)
        y2 = (-b - sqD) / (2.0*a)
        for y in (y1, y2):
            if y > -eps:
                y = max(0.0, y)
                r = math.sqrt(y)
                if r == 0.0:
                    roots.append(0.0)
                else:
                    roots.extend([-r, r])
        roots = sorted(set(round(x, 12) for x in roots))
    return len(roots), roots

def print_roots(num_roots, roots_list):
    if num_roots != len(roots_list):
        print(('Ошибка. Уравнение содержит {} действительных корней, ' +
               'но было вычислено {} корней.').format(num_roots, len(roots_list)))
    else:
        if num_roots == 0:
            print('Нет корней')
        elif num_roots == 1:
            print('Один корень: {}'.format(roots_list[0]))
        elif num_roots == 2:
            print('Два корня: {} и {}'.format(roots_list[0], roots_list[1]))
        elif num_roots == 3:
            print('Три корня: {}, {}, {}'.format(roots_list[0], roots_list[1], roots_list[2]))
        elif num_roots == 4:
            print('Четыре корня: {}, {}, {}, {}'.format(roots_list[0], roots_list[1], roots_list[2], roots_list[3]))
        else:
            print('Корней: {}: {}'.format(num_roots, roots_list))

def main():
    a, b, c = get_coefs()
    num_roots, roots = solve_biquadratic(a, b, c)
    print_roots(num_roots, roots)

if __name__ == "__main__":
    main()

# Пример запуска:
# python3 lab1/biquad_procedural.py 1 -5 4 -> -2, -1, 1, 2
# python3 lab1/biquad_procedural.py 1 0 -1 -> -1, 1