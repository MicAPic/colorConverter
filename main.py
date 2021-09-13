# Павлов М., 20.Б06-пу
# README:
# Введите цветовую модель (rgb, cmy, cmyk, hsl или hsv) без учета регистра
# Укажите цвет (rgb и cmy в битах, остальные в целых процентах и/или градусах, значения указываются через пробел)
# Для завершения работы программы напишите вместо модели exit
# Погрешность: ε = ±1

def rgb(color_code):
    r, g, b = color_code
    c, m, y = rgb2cmy(r, g, b, 'CMY')
    cmy2cmyk(c, m, y)
    rgb2hsv(r, g, b)
    rgb2hsl(r, g, b)
    rgb2xyz(r, g, b)


def cmy(color_code):
    c, m, y = color_code
    r, g, b = rgb2cmy(c, m, y, 'RGB')
    cmy2cmyk(c, m, y)
    rgb2hsv(r, g, b)
    rgb2hsl(r, g, b)
    rgb2xyz(r, g, b)


def cmyk(color_code):
    c, m, y, k = color_code
    c2, m2, y2 = cmyk2cmy(c, m, y, k)
    r, g, b = rgb2cmy(c2, m2, y2, 'RGB')
    rgb2hsv(r, g, b)
    rgb2hsl(r, g, b)
    rgb2xyz(r, g, b)


def hsv(color_code):
    h, s, v = color_code
    r, g, b = hsv2rgb(h, s, v)
    c, m, y = rgb2cmy(r, g, b, 'CMY')
    cmy2cmyk(c, m, y)
    rgb2hsl(r, g, b)
    rgb2xyz(r, g, b)


def hsl(color_code):
    h, s, l = color_code
    r, g, b = hsl2rgb(h, s, l)
    c, m, y = rgb2cmy(r, g, b, 'CMY')
    cmy2cmyk(c, m, y)
    rgb2hsv(r, g, b)
    rgb2xyz(r, g, b)


def rgb2cmy(c1, c2, c3, desired_palette):
    a, b, c = 255 - c1, 255 - c2, 255 - c3
    print(f'{desired_palette}: {a}, {b}, {c}')
    return [a, b, c]


def rgb2hsv(r, g, b):
    r, g, b = r / 255, g / 255, b / 255
    Min = min(r, g, b)
    Max = max(r, g, b)
    v = round(Max * 100)
    try:
        s = round((1 - Min / Max) * 100)
    except ZeroDivisionError:
        s = 0
    if Max == Min:
        print(f'HSV: не определен, {s}%, {v}%')
        return [0, s, v]
    elif Max == r and g >= b:
        h = (g - b) / (Max - Min)
    elif Max == r and g < b:
        h = (g - b) / (Max - Min) + 6
    elif Max == g:
        h = (b - r) / (Max - Min) + 2
    else:
        h = (r - g) / (Max - Min) + 4
    h = round(h * 60)
    print(f'HSV: {h}°, {s}%, {v}%')
    return [h, s, v]


def rgb2hsl(r, g, b):
    r, g, b = r / 255, g / 255, b / 255
    Min = min(r, g, b)
    Max = max(r, g, b)
    luminance_range = Max - Min
    total_luminance = Max + Min
    l = total_luminance / 2
    if Max == Min:
        l = round(l * 100)
        print(f'HSL: не определен, 0%, {l}%')
        return [0, 0, l]
    s = luminance_range / total_luminance if l < 0.5 else luminance_range / (2 - total_luminance)
    l, s = round(l * 100), round(s * 100)
    if Max == r:
        h = round((((g - b) / luminance_range) % 6) * 60)
    elif Max == g:
        h = round((2 + (b - r) / luminance_range) * 60)
    else:
        h = round((4 + (r - g) / luminance_range) * 60)
    print(f'HSL: {h}°, {s}%, {l}%')
    return [h, s, l]


def rgb2xyz(r, g, b):
    csrgb = [r, g, b]
    clinear = list(map(lambda x: ((x / 255 + 0.055) / 1.055) ** 2.4, csrgb))  # гамма-коррекция
    rl, gl, bl = clinear
    x = round((0.4124 * rl + 0.3576 * gl + 0.1805 * bl) * 100)
    y = round((0.2126 * rl + 0.7152 * gl + 0.0722 * bl) * 100)
    z = round((0.0193 * rl + 0.1192 * gl + 0.9505 * bl) * 100)
    print(f'XYZ: {x}, {y}, {z}')
    return [x, y, z]


def cmy2cmyk(c, m, y):
    k = min([c, m, y, 255])
    try:
        cmy255 = [(c - k) / (255 - k), (m - k) / (255 - k), (y - k) / (255 - k), k / 255]
    except ZeroDivisionError:
        cmy255 = [0, 0, 0, 1]
    c2, m2, y2, k2 = list(map(lambda x: round(x * 100), cmy255))  # переводим в целые %
    print(f'CMYK: {c2}%, {m2}%, {y2}%, {k2}%')
    return [c2, m2, y2, k2]


def cmyk2cmy(c, m, y, k):
    c, m, y, k = list(map(lambda x: x / 100, [c, m, y, k]))  # переводим в десятичную дробь
    cmy100 = c * (1 - k) + k, m * (1 - k) + k, y * (1 - k) + k
    c2, m2, y2 = list(map(lambda x: round(x * 255), cmy100))  # переводим в биты
    print(f'CMY: {c2}, {m2}, {y2}')
    return [c2, m2, y2]


def hsl2rgb(h, s, l):
    h, s, l = h / 60, s / 100, l / 100
    chroma = (1 - abs(2 * l - 1)) * s
    x = chroma * (1 - abs(h % 2 - 1))
    if h < 1:
        r, g, b = chroma, x, 0
    elif 1 <= h < 2:
        r, g, b = x, chroma, 0
    elif 2 <= h < 3:
        r, g, b = 0, chroma, x
    elif 3 <= h < 4:
        r, g, b = 0, x, chroma
    elif 4 <= h < 5:
        r, g, b = x, 0, chroma
    else:
        r, g, b = chroma, 0, x
    m = l - chroma / 2
    r, g, b = list(map(lambda y: round((y + m) * 255), [r, g, b]))
    print(f'RGB: {r}, {g}, {b}')
    return [r, g, b]


def hsv2rgb(h, s, v):
    h, s, v = h / 60, s / 100, v / 100
    chroma = v * s
    x = chroma * (1 - abs(h % 2 - 1))
    if h <= 1:
        r, g, b = chroma, x, 0
    elif 1 < h <= 2:
        r, g, b = x, chroma, 0
    elif 2 < h <= 3:
        r, g, b = 0, chroma, x
    elif 3 < h <= 4:
        r, g, b = 0, x, chroma
    elif 4 < h <= 5:
        r, g, b = x, 0, chroma
    else:
        r, g, b = chroma, 0, x
    m = v - chroma
    r, g, b = list(map(lambda y: round((y + m) * 255), [r, g, b]))
    print(f'RGB: {r}, {g}, {b}')
    return [r, g, b]


def user_input():
    response = ''
    choices = {'rgb', 'cmy', 'cmyk', 'hsv', 'hsl', 'exit'}
    while response.lower() not in choices:
        response = input('Введите тип вашей модели: ')
    if response == 'exit':
        exit()
    try:
        color_code = list(map(int, input('Укажите цвет: ').split(' ')))
        print('-----------------------------')
        globals()[response](color_code)
    except ValueError:
        print('Неверный код цвета')
    print('-----------------------------')


if __name__ == '__main__':
    while True:
        user_input()
