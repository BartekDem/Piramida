import pygame
from pygame.locals import *
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
import random

class PygameOpenGLApp:
    def __init__(self):
        pygame.init()
        self.display = (800, 600)
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)
        self.init_opengl()
        self.main_loop()

    def init_opengl(self):
        fov = 45
        gluPerspective(fov, (self.display[0]/self.display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT1)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        self.texture = self.load_texture()
        self.light_pos = [0, 1, 0, 3] 
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.5, 0.5, 0.5, 1]) 

    def load_texture(self):
        textureSurface = Image.open("multi.jpg")  
        textureData = textureSurface.tobytes()
        width, height = textureSurface.size
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)
        self.setup_texture_parameters()
        return texture

    def setup_texture_parameters(self):
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glEnable(GL_TEXTURE_2D)

    def main_loop(self):
        texture_enabled = False
        levels = int(input("Enter level: "))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                self.handle_key_events(event, texture_enabled)

            self.render_scene(levels, texture_enabled) # warunek od tekstury
            pygame.display.flip()
            pygame.time.wait(10)

    def handle_key_events(self, event, texture_enabled):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                self.move_camera(event.key)
            if event.key == pygame.K_q:
                texture_enabled = not texture_enabled # warunek od zmiany tekstury
            if event.key == pygame.K_r:
                self.change_light_color()

    def move_camera(self, key):
        movement = {
            pygame.K_LEFT: (0.1, 0, 0),
            pygame.K_RIGHT: (-0.1, 0, 0),
            pygame.K_UP: (0, 0.1, 0),
            pygame.K_DOWN: (0, -0.1, 0)
        }
        glMatrixMode(GL_PROJECTION)
        glTranslatef(*movement[key])
        glMatrixMode(GL_MODELVIEW)

    def render_scene(self, levels, texture_enabled):
        if texture_enabled:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture)
        else:
            glDisable(GL_TEXTURE_2D)
        glRotatef(0.5, 0, 0.5, 0)
        self.light(self.light_pos)
        self.draw_sierpinski_triangle(levels)
        self.draw_floor()

    def light(self, light_pos):
        glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])  
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])   
        glLightfv(GL_LIGHT1, GL_POSITION, light_pos) 

    def change_light_color(self):
        color = [random.random() for _ in range(3)] + [1.0]
        glLightfv(GL_LIGHT1, GL_DIFFUSE, color)

    def draw_sierpinski_triangle(self, levels):
        vertices = [
            [0, 1, 0],
            [-1, -1, 1],
            [1, -1, 1],
            [-1, -1, -1],
            [1, -1, -1]
        ]
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        self.sierpinski([vertices[0], vertices[1], vertices[2]], levels)
        self.sierpinski([vertices[0], vertices[1], vertices[3]], levels)
        self.sierpinski([vertices[0], vertices[2], vertices[4]], levels)
        self.sierpinski([vertices[0], vertices[3], vertices[4]], levels)

    def sierpinski(self, points, level):
        if level == 0:
            glBegin(GL_TRIANGLES)
            for point in points:
                glVertex3fv(point)
            glEnd()
        else:
            midpoints = [[(points[0][i] + points[1][i]) / 2 for i in range(3)],
                         [(points[1][i] + points[2][i]) / 2 for i in range(3)],
                         [(points[2][i] + points[0][i]) / 2 for i in range(3)]]
            self.sierpinski([points[0], midpoints[0], midpoints[2]], level - 1)
            self.sierpinski([points[1], midpoints[0], midpoints[1]], level - 1)
            self.sierpinski([points[2], midpoints[1], midpoints[2]], level - 1)

    def draw_floor(self):
        glBegin(GL_QUADS) 
        glColor3f(0.5, 0.5, 0.5)
        glVertex3f(-5, -1, 5)
        glVertex3f(5, -1, 5)
        glVertex3f(5, -1, -5)
        glVertex3f(-5, -1, -5)
        glEnd()





if __name__ == "__main__":
    app = PygameOpenGLApp()
