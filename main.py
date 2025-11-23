import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class McLarenM23:
    def __init__(self):
        # Definição das cores do carro
        self.COR_VERMELHO = (0.85, 0.0, 0.0)
        self.COR_BRANCO = (1.0, 1.0, 1.0)
        self.COR_PRETO = (0.05, 0.05, 0.05)
        self.COR_CINZA = (0.25, 0.25, 0.25)
        self.COR_CROMADO = (0.7, 0.7, 0.8)
        self.COR_VIDRO = (0.7, 0.85, 0.95)
        self.COR_CAPACETE = (1.0, 0.9, 0.1)

        # Estado do carro
        self.posicao = [0, 0, 0]
        self.rotacao_y = 0
        self.rotacao_roda = 0.0
        self.angulo_direcao = 0.0
        self.id_textura_roda = None

    def desenhar(self):
        glPushMatrix()
        glTranslatef(*self.posicao)
        glRotatef(self.rotacao_y, 0, 1, 0)

        self.desenhar_chassi()
        self.desenhar_entrada_ar()
        self.desenhar_asa_dianteira()
        self.desenhar_asa_traseira()
        self.desenhar_faixas_laterais()
        self.desenhar_suspensao()
        self.desenhar_rodas()
        self.desenhar_detalhes()
        self.desenhar_piloto()

        glPopMatrix()

    def desenhar_chassi(self):
        # Parte branca inferior
        glColor3f(*self.COR_BRANCO)
        glBegin(GL_QUADS)
        glVertex3f(-0.25, 0.28, 2.2); glVertex3f(0.25, 0.28, 2.2)
        glVertex3f(0.20, 0.15, 3.2); glVertex3f(-0.20, 0.15, 3.2)
        glVertex3f(-0.25, 0.28, 2.2); glVertex3f(-0.20, 0.15, 3.2)
        glVertex3f(-0.20, 0.05, 3.2); glVertex3f(-0.25, 0.05, 2.2)
        glVertex3f(0.25, 0.28, 2.2); glVertex3f(0.25, 0.05, 2.2)
        glVertex3f(0.20, 0.05, 3.2); glVertex3f(0.20, 0.15, 3.2)
        glVertex3f(-0.20, 0.15, 3.2); glVertex3f(0.20, 0.15, 3.2)
        glVertex3f(0.20, 0.05, 3.2); glVertex3f(-0.20, 0.05, 3.2)
        glEnd()

        # Cockpit vermelho
        glColor3f(*self.COR_VERMELHO)
        glBegin(GL_QUADS)
        # Topo e laterais
        glVertex3f(-0.45, 0.45, 0.5); glVertex3f(0.45, 0.45, 0.5)
        glVertex3f(0.25, 0.28, 2.2); glVertex3f(-0.25, 0.28, 2.2)
        glVertex3f(-0.45, 0.45, 0.5); glVertex3f(-0.25, 0.28, 2.2)
        glVertex3f(-0.25, 0.05, 2.2); glVertex3f(-0.45, 0.05, 0.5)
        glVertex3f(0.45, 0.45, 0.5); glVertex3f(0.45, 0.05, 0.5)
        glVertex3f(0.25, 0.05, 2.2); glVertex3f(0.25, 0.28, 2.2)
        # Traseira do cockpit
        glVertex3f(-0.45, 0.45, -0.5); glVertex3f(-0.45, 0.45, 0.5)
        glVertex3f(-0.45, 0.05, 0.5); glVertex3f(-0.45, 0.05, -0.5)
        glVertex3f(0.45, 0.45, 0.5); glVertex3f(0.45, 0.45, -0.5)
        glVertex3f(0.45, 0.05, -0.5); glVertex3f(0.45, 0.05, 0.5)
        glEnd()

        # Interior preto (assento)
        glColor3f(*self.COR_PRETO)
        glBegin(GL_QUADS)
        glVertex3f(-0.35, 0.46, -0.4); glVertex3f(0.35, 0.46, -0.4)
        glVertex3f(0.35, 0.46, 0.4); glVertex3f(-0.35, 0.46, 0.4)
        glEnd()

    def desenhar_asa_dianteira(self):
        glColor3f(*self.COR_BRANCO)
        # Base da asa
        glBegin(GL_QUADS)
        glVertex3f(-1.10, 0.25, 2.4); glVertex3f(-0.20, 0.20, 2.4)
        glVertex3f(-0.20, 0.10, 3.1); glVertex3f(-1.10, 0.15, 3.1)
        glEnd()
        # Aletas laterais (esquerda)
        glBegin(GL_QUADS)
        glVertex3f(-1.11, 0.30, 2.3); glVertex3f(-1.11, 0.30, 3.2)
        glVertex3f(-1.11, 0.05, 3.2); glVertex3f(-1.11, 0.05, 2.3)
        glEnd()
        # Base direita
        glBegin(GL_QUADS)
        glVertex3f(0.20, 0.20, 2.4); glVertex3f(1.10, 0.25, 2.4)
        glVertex3f(1.10, 0.15, 3.1); glVertex3f(0.20, 0.10, 3.1)
        glEnd()
        # Aletas laterais (direita)
        glBegin(GL_QUADS)
        glVertex3f(1.11, 0.30, 3.2); glVertex3f(1.11, 0.30, 2.3)
        glVertex3f(1.11, 0.05, 2.3); glVertex3f(1.11, 0.05, 3.2)
        glEnd()

    def desenhar_entrada_ar(self):
        # Parte vermelha superior
        glColor3f(*self.COR_VERMELHO)
        glBegin(GL_QUADS)
        glVertex3f(-0.25, 0.75, -0.5); glVertex3f(0.25, 0.75, -0.5)
        glVertex3f(0.45, 0.45, -0.5); glVertex3f(-0.45, 0.45, -0.5)
        glEnd()

        # Motor (bloco cinza)
        glColor3f(*self.COR_CINZA)
        glBegin(GL_QUADS)
        glVertex3f(-0.30, 0.40, -0.5); glVertex3f(0.30, 0.40, -0.5)
        glVertex3f(0.30, 0.40, -2.0); glVertex3f(-0.30, 0.40, -2.0)
        glEnd()

        # Detalhe branco lateral
        glColor3f(*self.COR_BRANCO)
        glBegin(GL_QUADS)
        glVertex3f(-0.32, 0.38, -0.5); glVertex3f(-0.32, 0.38, -1.8)
        glVertex3f(-0.32, 0.15, -1.8); glVertex3f(-0.32, 0.15, -0.5)
        glVertex3f(0.32, 0.38, -1.8); glVertex3f(0.32, 0.38, -0.5)
        glVertex3f(0.32, 0.15, -0.5); glVertex3f(0.32, 0.15, -1.8)
        glEnd()

    def desenhar_asa_traseira(self):
        glColor3f(*self.COR_CROMADO)
        # Suporte
        glBegin(GL_QUADS)
        glVertex3f(-0.05, 0.80, -2.2); glVertex3f(0.05, 0.80, -2.2)
        glVertex3f(0.05, 0.40, -1.8); glVertex3f(-0.05, 0.40, -1.8)
        glEnd()

        glColor3f(*self.COR_BRANCO)
        # Asa principal
        glBegin(GL_QUADS)
        glVertex3f(-1.0, 0.85, -2.0); glVertex3f(1.0, 0.85, -2.0)
        glVertex3f(1.0, 0.90, -2.6); glVertex3f(-1.0, 0.90, -2.6)
        glEnd()

        glColor3f(*self.COR_VERMELHO)
        # Placas laterais da asa
        glBegin(GL_QUADS)
        glVertex3f(-1.01, 0.95, -2.0); glVertex3f(-1.01, 1.00, -2.6)
        glVertex3f(-1.01, 0.60, -2.6); glVertex3f(-1.01, 0.60, -2.0)
        glEnd()

        glBegin(GL_QUADS)
        glVertex3f(1.01, 1.00, -2.6); glVertex3f(1.01, 0.95, -2.0)
        glVertex3f(1.01, 0.60, -2.0); glVertex3f(1.01, 0.60, -2.6)
        glEnd()

    def desenhar_faixas_laterais(self):
        # Geometria simples para simular decalques/patrocinadores
        glColor3f(*self.COR_VERMELHO)
        y = 0.22
        glBegin(GL_QUADS)
        glVertex3f(-0.12, y, 2.5); glVertex3f(-0.04, y, 2.5)
        glVertex3f(-0.04, y, 2.9); glVertex3f(-0.12, y, 2.9)
        glEnd()
        glBegin(GL_QUADS)
        glVertex3f(0.04, y, 2.5); glVertex3f(0.12, y, 2.5)
        glVertex3f(0.12, y, 2.9); glVertex3f(0.04, y, 2.9)
        glEnd()

        glColor3f(*self.COR_PRETO)
        glBegin(GL_QUADS)
        glVertex3f(-0.9, 0.21, 2.5); glVertex3f(-0.4, 0.19, 2.5)
        glVertex3f(-0.4, 0.14, 2.8); glVertex3f(-0.9, 0.16, 2.8)
        glEnd()
        glBegin(GL_QUADS)
        glVertex3f(0.4, 0.19, 2.5); glVertex3f(0.9, 0.21, 2.5)
        glVertex3f(0.9, 0.16, 2.8); glVertex3f(0.4, 0.14, 2.8)
        glEnd()

    def desenhar_detalhes(self):
        quadric = gluNewQuadric()

        # Santo Antônio (barra de proteção)
        glColor3f(*self.COR_CROMADO)
        glPushMatrix()
        glTranslatef(0, 0.75, -0.5)
        glBegin(GL_LINE_STRIP)
        for angulo in range(0, 181, 10):
            rad = math.radians(angulo)
            glVertex3f(0.2 * math.cos(rad), 0.2 * math.sin(rad), 0)
        glEnd()
        glPopMatrix()

        # Retrovisores
        self._desenhar_retrovisor(-0.35, 0.50, 1.2) # Esquerdo
        self._desenhar_retrovisor(0.35, 0.50, 1.2)  # Direito

        # Escapamentos
        glColor3f(0.3, 0.3, 0.3)
        # Esq
        glPushMatrix()
        glTranslatef(-0.2, 0.2, -2.0)
        glRotatef(180, 0, 1, 0)
        gluCylinder(quadric, 0.05, 0.05, 0.5, 10, 1)
        glPopMatrix()
        # Dir
        glPushMatrix()
        glTranslatef(0.2, 0.2, -2.0)
        glRotatef(180, 0, 1, 0)
        gluCylinder(quadric, 0.05, 0.05, 0.5, 10, 1)
        glPopMatrix()

        # Para-brisa (transparente)
        glColor3f(*self.COR_VIDRO)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_LINE_STRIP)
        glVertex3f(-0.25, 0.45, 1.0)
        glVertex3f(-0.25, 0.55, 1.0)
        glVertex3f(0.25, 0.55, 1.0)
        glVertex3f(0.25, 0.45, 1.0)
        glEnd()
        glDisable(GL_BLEND)

    def _desenhar_retrovisor(self, x, y, z):
        glPushMatrix()
        glTranslatef(x, y, z)
        glDisable(GL_LIGHTING)
        glColor3f(*self.COR_BRANCO)
        
        # Haste
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        if x < 0: glVertex3f(-0.12, 0.12, -0.1)
        else: glVertex3f(0.12, 0.12, -0.1)
        glEnd()
        
        # Espelho
        if x < 0: glTranslatef(-0.12, 0.12, -0.1)
        else: glTranslatef(0.12, 0.12, -0.1)
        
        glScale(0.1, 0.08, 0.05)
        self.desenhar_cubo()
        glEnable(GL_LIGHTING)
        glPopMatrix()

    def desenhar_piloto(self):
        quadric = gluNewQuadric()
        glPushMatrix()
        glTranslatef(0, 0.55, 0)
        
        # Vira a cabeça conforme o volante
        glRotatef(self.angulo_direcao * 1.5, 0, 1, 0)

        # Capacete
        glColor3f(*self.COR_CAPACETE)
        gluSphere(quadric, 0.16, 16, 16)

        # Viseira
        glColor3f(0.1, 0.1, 0.2)
        glPushMatrix()
        glTranslatef(0, 0.02, 0.12)
        glScalef(1, 0.6, 1)
        gluSphere(quadric, 0.08, 16, 16)
        glPopMatrix()

        glPopMatrix()
        gluDeleteQuadric(quadric)

    def desenhar_cubo(self):
        # Primitiva auxiliar
        glBegin(GL_QUADS)
        for x in [-1, 1]:
            glVertex3f(x, -1, -1); glVertex3f(x, 1, -1)
            glVertex3f(x, 1, 1);   glVertex3f(x, -1, 1)
        for y in [-1, 1]:
            glVertex3f(-1, y, -1); glVertex3f(1, y, -1)
            glVertex3f(1, y, 1);   glVertex3f(-1, y, 1)
        for z in [-1, 1]:
            glVertex3f(-1, -1, z); glVertex3f(1, -1, z)
            glVertex3f(1, 1, z);   glVertex3f(-1, 1, z)
        glEnd()

    def desenhar_suspensao(self):
        glColor3f(*self.COR_CROMADO)
        glLineWidth(4)
        glBegin(GL_LINES)
        # Dianteira
        glVertex3f(-0.65, 0.25, 1.6); glVertex3f(-0.25, 0.35, 1.6)
        glVertex3f(-0.65, 0.25, 1.6); glVertex3f(-0.25, 0.15, 1.6)
        glVertex3f(0.65, 0.25, 1.6); glVertex3f(0.25, 0.35, 1.6)
        glVertex3f(0.65, 0.25, 1.6); glVertex3f(0.25, 0.15, 1.6)

        # Traseira
        glVertex3f(-0.70, 0.25, -1.5); glVertex3f(-0.30, 0.35, -1.0)
        glVertex3f(-0.70, 0.25, -1.5); glVertex3f(-0.30, 0.15, -1.0)
        glVertex3f(0.70, 0.25, -1.5); glVertex3f(0.30, 0.35, -1.0)
        glVertex3f(0.70, 0.25, -1.5); glVertex3f(0.30, 0.15, -1.0)
        glEnd()
        glLineWidth(1)

    def desenhar_rodas(self):
        glPushMatrix()

        # Roda Esq Dianteira
        glPushMatrix()
        glTranslatef(-0.65, 0.25, 1.6)
        glRotatef(self.angulo_direcao, 0, 1, 0)
        glRotatef(self.rotacao_roda, 1, 0, 0)
        self.desenhar_unica_roda(0.32, 0.35, espelhado=True)
        glPopMatrix()

        # Roda Esq Traseira
        glPushMatrix()
        glTranslatef(-0.70, 0.25, -1.5)
        glRotatef(self.rotacao_roda, 1, 0, 0)
        self.desenhar_unica_roda(0.40, 0.60, espelhado=True)
        glPopMatrix()

        # Roda Dir Dianteira
        glPushMatrix()
        glTranslatef(0.65, 0.25, 1.6)
        glRotatef(self.angulo_direcao, 0, 1, 0)
        glRotatef(self.rotacao_roda, 1, 0, 0)
        self.desenhar_unica_roda(0.32, 0.35, espelhado=False)
        glPopMatrix()

        # Roda Dir Traseira
        glPushMatrix()
        glTranslatef(0.70, 0.25, -1.5)
        glRotatef(self.rotacao_roda, 1, 0, 0)
        self.desenhar_unica_roda(0.40, 0.60, espelhado=False)
        glPopMatrix()

        glPopMatrix()

    def desenhar_unica_roda(self, raio, largura, espelhado=False):
        quadric = gluNewQuadric()
        glPushMatrix()
        if espelhado:
            glRotatef(180, 0, 1, 0)

        gluQuadricTexture(quadric, GL_FALSE)
        glColor3f(*self.COR_PRETO)
        
        # Pneu (Cilindro)
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        glTranslatef(0, 0, -largura / 2)
        gluCylinder(quadric, raio, raio, largura, 24, 1)
        glPopMatrix()

        # Calota (com textura se disponível)
        gluQuadricTexture(quadric, GL_TRUE)
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        glTranslatef(0, 0, largura / 2)
        if self.id_textura_roda:
            glEnable(GL_TEXTURE_2D); glBindTexture(GL_TEXTURE_2D, self.id_textura_roda)
            glColor3f(1, 1, 1)
        else:
            glColor3f(*self.COR_PRETO)
        gluDisk(quadric, 0, raio, 24, 1)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        # Parte interna da roda
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        glTranslatef(0, 0, -largura / 2)
        glRotatef(180, 0, 1, 0)
        glColor3f(*self.COR_PRETO)
        gluDisk(quadric, 0, raio, 24, 1)
        glPopMatrix()

        glPopMatrix()
        gluDeleteQuadric(quadric)

if __name__ == "__main__":
    print("Execute o arquivo scene.py para iniciar o simulador.")