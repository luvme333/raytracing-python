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
DIFFUSE_REFLECTION = 1
MIRROR_REFLECTION = 2
REFRACTION = 3
sizeofRGBa32f = 34836
height = 300
weight = 300
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
    spheres[0][0] = -1
    spheres[0][1] = -1
    spheres[0][2] = -2
    spheres[0][3] = 2
    spheres[1][0] = 2
    spheres[1][1] = 1
    spheres[1][2] = 2
    spheres[1][3] = 1

def setVec4BufferAsImage(array, unit):
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

def fillMaterials():
    material = [[] for i in range(6)]
    lightCoefs = [0.4, 0.9, 0.2, 2.0]

    material[0].append([0, 1, 0])
    material[0].append(lightCoefs)
    material[0].append(0.5)
    material[0].append(1)
    material[0].append(DIFFUSE_REFLECTION)

    material[1].append([0, 0, 1])
    material[1].append(lightCoefs)
    material[1].append(0.5)
    material[1].append(1)
    material[1].append(DIFFUSE_REFLECTION)

    material[2].append([0, 0.1, 0.8])
    material[2].append(lightCoefs)
    material[2].append(0.5)
    material[2].append(1)
    material[2].append(DIFFUSE_REFLECTION)

    material[3].append([1, 0, 0])
    material[3].append(lightCoefs)
    material[3].append(0.5)
    material[3].append(1)
    material[3].append(DIFFUSE_REFLECTION)

    material[4].append([1, 1, 1])
    material[4].append(lightCoefs)
    material[4].append(0.5)
    material[4].append(1)
    material[4].append(DIFFUSE_REFLECTION)

    material[5].append([0, 1, 1])
    material[5].append(lightCoefs)
    material[5].append(0.5)
    material[5].append(1)
    material[5].append(DIFFUSE_REFLECTION)

    material[6].append([0, 1, 1])
    material[6].append([0.4, 0.9, 0.9, 50.0])
    material[6].append(0.8)
    material[6].append(1.5)
    material[6].append(REFRACTION)

    return material

def initMaterials():
    material = fillMaterials()
    for i in range(len(material)):
        location = glGetUniformLocation(program, "uMaterials[", i, "].Color")
        glUniform3f(location, material[i][0])
        location = glGetUniformLocation(program, "uMaterials[", i, "].LightCoeffs")
        glUniform4f(location, material[i][1])
        location = glGetUniformLocation(program, "uMaterials[", i, "].ReflectionCoef")
        glUniform1f(location, material[i][2])
        location = glGetUniformLocation(program, "uMaterials[", i, "].RefractionCoef")
        glUniform1f(location, material[i][3])
        location = glGetUniformLocation(program, "uMaterials[", i, "].MaterialType")
        glUniform1f(location, material[i][4])

# Процедура перерисовки
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    init()
    initShaders()
    initMaterials()
    initSceneBuffers()
    location = glGetUniformLocation(program, "uCamera.Position")
    glUniform3f(location, (0, 0, -7.5))
    location = glGetUniformLocation(program, "uCamera.Up")
    glUniform3f(location, (0, 1, 0))
    location = glGetUniformLocation(program, "uCamera.Side")
    glUniform3f(location, (1, 0, 0))
    location = glGetUniformLocation(program, "uCamera.View")
    glUniform3f(location, (0, 0, 1))
    location = glGetUniformLocation(program, "uCamera.Scale")
    glUniform2f(location, (1, height / weight))
    location = glGetUniformLocation(program, "uLight.Position")
    glUniform3f(location, (2.0, 0.0, -4.0))

    glColor3b(0, 0, 0)
    glBegin(GL_QUADS)

    glTexCoord2f(0, 1)
    glVertex2f(-1, -1)

    glTexCoord2f(1, 1)
    glVertex2f(1, -1)

    glTexCoord2f(1, 0)
    glVertex2f(1, 1)

    glTexCoord2f(0, 0)
    glVertex2f(-1, 1)

    glEnd()
    glutSwapBuffers()
    glUseProgram(0)

# Здесь начинется выполнение программы
draw()
