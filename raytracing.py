from OpenGL.GL import *
from OpenGL.GLUT import *

import numpy as np
import sys


DIFFUSE_REFLECTION = 1
MIRROR_REFLECTION = 2
REFRACTION = 3
height = 500
weight = 500
vertexShaderPath = "raytracing.vert"
fragmentShaderPath = "raytracing.frag"


class Material:
    def __init__(self, color=None, lightCoefs=None, reflectionCoef=None, refractionCoef=None, materialType=None):
        self.color = color
        self.lightCoefs = lightCoefs
        self.reflectionCoef = reflectionCoef
        self.refractionCoef = refractionCoef
        self.materialType = materialType


# Процедура подготовки шейдера (путь к файлу, тип шейдера)
def loadShader(filename, shaderType):
    shader = glCreateShader(shaderType)
    with open(filename) as file:
        shaderText = file.read()
    glShaderSource(shader, shaderText)
    glCompileShader(shader)
    return shader


def fillTriangleArrays():
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


spheres = np.zeros((2, 4))


def initSpheres():
    spheres[0][0] = -1
    spheres[0][1] = -1
    spheres[0][2] = -2
    spheres[0][3] = 2
    spheres[1][0] = 2
    spheres[1][1] = 1
    spheres[1][2] = 2
    spheres[1][3] = 1


def setVec4BufferAsImage(array, unit):
    py_id = glGenBuffers(1)
    glBindBuffer(GL_TEXTURE_BUFFER, py_id)
    glBufferData(GL_TEXTURE_BUFFER, 16 * len(array), array, GL_STATIC_DRAW)
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_BUFFER, tex)
    glTexBuffer(GL_TEXTURE_BUFFER, GL_RGBA32F, py_id)
    glBindImageTexture(unit, tex, 0, GL_FALSE, 0, GL_READ_ONLY, GL_RGBA32F)


points = np.zeros((11, 4), dtype=int)
indexes = np.zeros((13, 4), dtype=int)
material = [Material() for i in range(7)]


def initSceneBuffers():
    fillTriangleArrays()
    initSpheres()

    setVec4BufferAsImage(points, 2)
    setVec4BufferAsImage(indexes, 3)
    setVec4BufferAsImage(spheres, 4)


def fillMaterials():
    lightCoefs = [0.4, 0.9, 0.2, 2.0]
    spheresCoefs = [0.4, 0.9, 0.9, 50.0]

    material[0] = Material([0, 1, 0], lightCoefs, 0.5, 1, DIFFUSE_REFLECTION)
    material[1] = Material([0, 0, 1], lightCoefs, 0.5, 1, DIFFUSE_REFLECTION)
    material[2] = Material([0, 0.1, 0.8], lightCoefs, 0.5, 1, DIFFUSE_REFLECTION)
    material[3] = Material([1, 0, 0], lightCoefs, 0.5, 1, DIFFUSE_REFLECTION)
    material[4] = Material([1, 1, 1], lightCoefs, 0.5, 1, DIFFUSE_REFLECTION)
    material[5] = Material([0, 1, 1], lightCoefs, 0.5, 1, DIFFUSE_REFLECTION)
    material[6] = Material([0, 1, 1], spheresCoefs, 0.8, 1.5, REFRACTION)


def initMaterials():
    fillMaterials()

    for i in range(len(material)):
        colorLocation = "uMaterials[" + str(i) + "].Color"
        lightCoefsLocation = "uMaterials[" + str(i) + "].LightCoeffs"
        reflectionCoefsLocation = "uMaterials[" + str(i) + "].ReflectionCoef"
        refractionCoefsLocation = "uMaterials[" + str(i) + "].RefractionCoef"
        materialTypeLocation = "uMaterials[" + str(i) + "].MaterialType"
        location = glGetUniformLocation(program, colorLocation)
        glUniform3fv(location, 1, material[i].color)
        location = glGetUniformLocation(program, lightCoefsLocation)
        glUniform4fv(location, 1, material[i].lightCoefs)
        location = glGetUniformLocation(program, reflectionCoefsLocation)
        glUniform1f(location,  material[i].reflectionCoef)
        location = glGetUniformLocation(program, refractionCoefsLocation)
        glUniform1f(location, material[i].refractionCoef)
        location = glGetUniformLocation(program, materialTypeLocation)
        glUniform1i(location, material[i].materialType)


def initCamera():
    location = glGetUniformLocation(program, "uCamera.Position")
    glUniform3fv(location, 1, [0, 0, -7.5])
    location = glGetUniformLocation(program, "uCamera.Up")
    glUniform3fv(location, 1, [0, 1, 0])
    location = glGetUniformLocation(program, "uCamera.Side")
    glUniform3fv(location, 1, [1, 0, 0])
    location = glGetUniformLocation(program, "uCamera.View")
    glUniform3fv(location, 1, [0, 0, 1])
    location = glGetUniformLocation(program, "uCamera.Scale")
    glUniform2fv(location, 1, [1, height / weight])
    location = glGetUniformLocation(program, "uLight.Position")
    glUniform3fv(location, 1, [2.0, 0.0, -4.0])


# Процедура перерисовки
def draw():
    glColor3f(255, 255, 255)
    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2f(-1, -1)

    glTexCoord2f(1, 1)
    glVertex2f(1, -1)

    glTexCoord2f(1, 0)
    glVertex2f(1, 1)

    glTexCoord2f(0, 0)
    glVertex2f(-1, 1)

    glEnd
    glutSwapBuffers()
    glUseProgram(0)


# Здесь начинется выполнение программы
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
# Указываем начальный размер окна (ширина, высота)
glutInitWindowSize(height, weight)
# Указываем начальное
# положение окна относительно левого верхнего угла экрана
glutInitWindowPosition(500, 500)
# Инициализация OpenGl
glutInit(sys.argv)
# Создаем окно с заголовком
glutCreateWindow("Raytracing")
# Определяем процедуру, отвечающую за перерисовку
glutDisplayFunc(draw)
# Задаем серый цвет для очистки экрана
glClearColor(0.2, 0.2, 0.2, 1)

glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
glEnable(GL_COLOR_MATERIAL)
glShadeModel(GL_SMOOTH)
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)

#Подключение шейдеров к программе
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

initMaterials()
initCamera()
initSceneBuffers()

glutMainLoop()
