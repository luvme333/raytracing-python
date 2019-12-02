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
