from OpenGL.GL import *
from OpenGL.GLUT import *
#import sys
# Из модуля random импортируем одноименную функцию random
from random import random
# объявляем массив pointcolor глобальным (будет доступен во всей программе)
global pointcolor
global vertexShaderPath 
global fragmentShaderPath
global vertexShader
global fragmentShader
global program
global sizeofRGBa32f
sizeofRGBa32f = 34836
vertexShaderPath = "raytracing.vert"
fragmentShaderPath = "raytracing.frag"


# Процедура подготовки шейдера (тип шейдера, текст шейдера)
def loadShader(filename, shaderType):
    shader = glCreateShader(shaderType)
    with open(filename) as file:
        shaderText = file.read()
    print(" ( ° ͜ʖ͡°)╭∩╮")
    glShaderSource(shader, shaderText)
    glCompileShader(shader)
    
    return shader

def initShaders():
    vertexShader = loadShader(vertexShaderPath, GL_VERTEX_SHADER)
    fragmentShader = loadShader(fragmentShaderPath, GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    # Приcоединяем вершинный шейдер к программе
    glAttachShader(program, vertexShader)
    # Присоединяем фрагментный шейдер к программе
    glAttachShader(program, fragmentShader)
    # "Собираем" шейдерную программу
    glLinkProgram(program)
    # Сообщаем OpenGL о необходимости использовать данную шейдерну программу при отрисовке объектов
    glUseProgram(program)

# Процедура перерисовки
def draw():
    glClear(GL_COLOR_BUFFER_BIT)                    # Очищаем экран и заливаем серым цветом
    glEnableClientState(GL_VERTEX_ARRAY)            # Включаем использование массива вершин
    glEnableClientState(GL_COLOR_ARRAY)             # Включаем использование массива цветов
    # Указываем, где взять массив верши:
    # Первый параметр - сколько используется координат на одну вершину
    # Второй параметр - определяем тип данных для каждой координаты вершины
    # Третий парметр - определяет смещение между вершинами в массиве
    # Если вершины идут одна за другой, то смещение 0
    # Четвертый параметр - указатель на первую координату первой вершины в массиве
    glVertexPointer(3, GL_FLOAT, 0, pointdata)
    # Указываем, где взять массив цветов:
    # Параметры аналогичны, но указывается массив цветов
    glColorPointer(3, GL_FLOAT, 0, pointcolor)
    # Рисуем данные массивов за один проход:
    # Первый параметр - какой тип примитивов использовать (треугольники, точки, линии и др.)
    # Второй параметр - начальный индекс в указанных массивах
    # Третий параметр - количество рисуемых объектов (в нашем случае это 3 вершины - 9 координат)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glDisableClientState(GL_VERTEX_ARRAY)           # Отключаем использование массива вершин
    glDisableClientState(GL_COLOR_ARRAY)            # Отключаем использование массива цветов
    glutSwapBuffers()                               # Выводим все нарисованное в памяти на экран

def init():
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def fillTriangleArrays(points, indexes):
    # front
    points[0][0] = -5
    points[0][1] = 5
    points[0][2] = -8
    points[0][3] = 0
    points[1][0] = 5
    points[1][1] = 5
    points[1][2] = -8
    points[1][3] = 0
    points[2][0] = 5
    points[2][1] = -5
    points[2][2] = -8
    points[2][3] = 0
    points[3][0] = -5
    points[3][1] = -5
    points[3][2] = -8
    points[3][3] = 0

    indexes[0][0] = 3
    indexes[0][1] = 0
    indexes[0][2] = 1
    indexes[0][3] = 4
    indexes[1][0] = 3
    indexes[1][1] = 1
    indexes[1][2] = 2
    indexes[1][3] = 4

    # back
    points[4][0] = -5
    points[4][1] = 5
    points[4][2] = 8
    points[4][3] = 0
    points[5][0] = 5
    points[5][1] = 5
    points[5][2] = 8
    points[5][3] = 0
    points[6][0] = 5
    points[6][1] = -5
    points[6][2] = 8
    points[6][3] = 0
    points[7][0] = -5
    points[7][1] = -5
    points[7][2] = 8
    points[7][3] = 0

    indexes[2][0] = 4
    indexes[2][1] = 7
    indexes[2][2] = 5
    indexes[2][3] = 5
    indexes[3][0] = 5
    indexes[3][1] = 7
    indexes[3][2] = 6
    indexes[3][3] = 5

    # right
    indexes[4][0] = 2
    indexes[4][1] = 1
    indexes[4][2] = 5
    indexes[4][3] = 0
    indexes[5][0] = 2
    indexes[5][1] = 5
    indexes[5][2] = 6
    indexes[5][3] = 0

    # left
    indexes[6][0] = 4
    indexes[6][1] = 0
    indexes[6][2] = 3
    indexes[6][3] = 3
    indexes[7][0] = 4
    indexes[7][1] = 3
    indexes[7][2] = 7
    indexes[7][3] = 3

    # bottom
    indexes[8][0] = 3
    indexes[8][1] = 2
    indexes[8][2] = 6
    indexes[8][3] = 4
    indexes[9][0] = 3
    indexes[9][1] = 6
    indexes[9][2] = 7
    indexes[9][3] = 4

    # top
    indexes[10][0] = 0
    indexes[10][1] = 4
    indexes[10][2] = 5
    indexes[10][3] = 4
    indexes[11][0] = 0
    indexes[11][1] = 5
    indexes[11][2] = 1
    indexes[11][3] = 4

    points[8][0] = -1
    points[8][1] = 0
    points[8][2] = 15
    points[8][3] = 0
    points[9][0] = 0
    points[9][1] = 2
    points[9][2] = 15
    points[9][3] = 0
    points[10][0] = 0
    points[10][1] = 0
    points[10][2] = 15
    points[10][3] = 0

    indexes[12][0] = 8
    indexes[12][1] = 10
    indexes[12][2] = 9
    indexes[12][3] = 6

def initSpheres(spheres):
    spheres[0] [0] = -1
    spheres[0] [1] = -1
    spheres[0] [2] = -2
    spheres[0] [3] = 2
    spheres[1] [0] = 2
    spheres[1] [1] = 1
    spheres[1] [2] = 2
    spheres[1] [3] = 1

def setVec4BufferAsImage(array, bufferUsageHint, unit):
    ptr = array.index(0)
    buf = glGenBuffers()
    glBindBuffer(GL_TEXTURE_BUFFER, buf)
    glBufferData(GL_TEXTURE_BUFFER, sizeof(float) * 4 * len(array), ptr, GL_STATIC_DRAW)
    tex = glBindTexture()
    glBindTexture(GL_TEXTURE_BUFFER, tex)
    glTexBuffer(GL_TEXTURE_BUFFER, sizeofRGBa32f, buf)
    glBindImageTexture(unit, tex, 0, False, 0, GL_READ_ONLY, sizeofRGBa32f)

    
def initSceneBuffers():
    points = [[0 for j in range(4)] for i in range(11)]
    indexes = [[0 for j in range(4)] for i in range(13)]
    fillTriangleArrays(points, indexes)
    spheres = [[0 for j in range(4)] for i in range(2)]
    initSpheres(spheres)

    setVec4BufferAsImage(points, GL_STATIC_DRAW, 2)
    setVec4BufferAsImage(indexes, GL_STATIC_DRAW, 3)
    setVec4BufferAsImage(spheres, GL_STATIC_DRAW, 4)

# Здесь начинется выполнение программы
# Использовать двойную буферезацию и цвета в формате RGB (Красный Синий Зеленый)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
# Указываем начальный размер окна (ширина, высота)
glutInitWindowSize(300, 300)
# Указываем начальное
# положение окна относительно левого верхнего угла экрана
glutInitWindowPosition(50, 50)
# Инициализация OpenGl
glutInit(sys.argv)
# Создаем окно с заголовком
glutCreateWindow("Raytracing")
init()
# Определяем процедуру, отвечающую за перерисовку
glutDisplayFunc(draw)
# Определяем процедуру, выполняющуюся при "простое" программы
glutIdleFunc(draw)
# Задаем серый цвет для очистки экрана
glClearColor(0.2, 0.2, 0.2, 1)
# Создаем вершинный шейдер:
# Положение вершин не меняется
# Цвет вершины - такой же как и в массиве цветов
initShaders()

# Определяем массив вершин (три вершины по три координаты)
pointdata = [[0, 0.5, 0], [-0.5, -0.5, 0], [0.5, -0.5, 0]]
# Определяем массив цветов (по одному цвету для каждой вершины)
pointcolor = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
# Запускаем основной цикл
#print(glGetProgramInfoLog(program))
glutMainLoop()
