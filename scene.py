import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math
import time

from main import McLarenM23


# CONFIGURAÇÕES GERAIS

LARGURA_TELA = 1024
ALTURA_TELA = 768
LARGURA_PISTA = 14.0
COMPRIMENTO_SEGMENTO = 4.0
NUM_SEGMENTOS = 60
VELOCIDADE_MAX = 97.0 

# Paleta de Cores
COR_CEU = (0.5, 0.7, 1.0, 1.0)
COR_ASFALTO = (0.15, 0.15, 0.15)
COR_ZEBRA_VERMELHA = (0.8, 0.0, 0.0)
COR_ZEBRA_BRANCA = (1.0, 1.0, 1.0)
COR_PELE = (1.0, 0.85, 0.75)
COR_SOL = (1.0, 0.9, 0.0, 1.0)
COR_NUVEM = (0.9, 0.9, 0.95, 0.7)
COR_TEXTO = (1.0, 1.0, 0.0)
COR_TERRA = (0.35, 0.25, 0.15) 

# Estados do Jogo
ESTADO_MENU = 0
ESTADO_CORRIDA = 1
ESTADO_FIM = 2

# Variáveis Globais de Textura e Ambiente
ID_TEXTURA_GRAMA = None
ID_TEXTURA_MADEIRA = None
ID_TEXTURA_CHEGADA = None 
ID_TEXTURA_RODA = None  
CORES_TORCIDA = []
NUVENS = []
PARTICULAS = [] 

def criar_textura_grama():
    largura, altura = 256, 256
    dados = []
    for y in range(altura):
        for x in range(largura):
            r = random.randint(0, 30)
            g = random.randint(100, 180)
            b = random.randint(0, 30)
            dados.extend([r, g, b])
    return gerar_textura_opengl(largura, altura, bytes(dados))

def criar_textura_madeira():
    largura, altura = 128, 128
    dados = []
    for y in range(altura):
        base_r = 120 + random.randint(-10, 10)
        base_g = 70 + random.randint(-5, 5)
        base_b = 20
        for x in range(largura):
            ruido = random.randint(-15, 15)
            r = max(0, min(255, base_r + ruido))
            g = max(0, min(255, base_g + ruido))
            b = max(0, min(255, base_b + ruido))
            dados.extend([r, g, b])
    return gerar_textura_opengl(largura, altura, bytes(dados))

def criar_textura_chegada():
    largura, altura = 64, 64
    dados = []
    tamanho_xadrez = 8
    for y in range(altura):
        for x in range(largura):
            if (x // tamanho_xadrez) % 2 == (y // tamanho_xadrez) % 2:
                dados.extend([255, 255, 255]) 
            else:
                dados.extend([20, 20, 20])    
    return gerar_textura_opengl(largura, altura, bytes(dados))

def criar_textura_roda():
    largura, altura = 256, 256
    dados = []
    centro_x, centro_y = largura / 2, altura / 2
    raio_max = largura / 2

    for y in range(altura):
        for x in range(largura):
            dx = x - centro_x
            dy = y - centro_y
            dist = math.sqrt(dx*dx + dy*dy)
            dist_norm = dist / raio_max

            r, g, b = 20, 20, 20 
            if dist_norm < 0.5:
                r, g, b = 40, 40, 45 
            # Efeito de borrão/movimento na borda
            if 0.70 < dist_norm < 0.90:
                ruido = random.randint(0, 150)
                angulo = math.atan2(dy, dx)
                mascara = (math.sin(angulo * 2) + 1) / 2 
                if mascara > 0.8: 
                     r = g = b = min(255, r + ruido + 50)
            dados.extend([r, g, b])
    return gerar_textura_opengl(largura, altura, bytes(dados))

def gerar_textura_opengl(largura, altura, dados_bytes):
    id_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id_tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGB, largura, altura, GL_RGB, GL_UNSIGNED_BYTE, dados_bytes)
    return id_tex

def inicializar_opengl():
    global ID_TEXTURA_GRAMA, ID_TEXTURA_MADEIRA, ID_TEXTURA_CHEGADA, ID_TEXTURA_RODA, CORES_TORCIDA, NUVENS
    
    glutInit() # Necessário para fontes de texto
    
    # Gera cores aleatórias para a plateia
    for _ in range(NUM_SEGMENTOS * 50):
        CORES_TORCIDA.append((random.uniform(0.1, 1.0), random.uniform(0.1, 1.0), random.uniform(0.1, 1.0)))
    
    # Gera nuvens aleatórias
    for _ in range(20):
        NUVENS.append({
            'x': random.uniform(-150, 150), 
            'y': random.uniform(20, 50), 
            'z': random.uniform(-200, 0),
            'tamanho': random.uniform(10, 30), 
            'velocidade': random.uniform(1.0, 3.0)
        })

    glViewport(0, 0, LARGURA_TELA, ALTURA_TELA)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (LARGURA_TELA / ALTURA_TELA), 0.1, 300.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Configuração de neblina (Fog)
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, COR_CEU)
    glFogi(GL_FOG_MODE, GL_EXP2)
    glFogf(GL_FOG_DENSITY, 0.005)
    glHint(GL_FOG_HINT, GL_NICEST)
    
    glClearColor(*COR_CEU)
    
    ID_TEXTURA_GRAMA = criar_textura_grama()
    ID_TEXTURA_MADEIRA = criar_textura_madeira()
    ID_TEXTURA_CHEGADA = criar_textura_chegada()
    ID_TEXTURA_RODA = criar_textura_roda()

def configurar_luz_carro():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_POSITION, (50.0, 100.0, 50.0, 0.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.4, 0.4, 0.4, 1.0))


# SISTEMA DE PARTÍCULAS

def gerar_particulas(carro_x, carro_z, intensidade=1):
    offset_rodas = [-0.7, 0.7]
    for wx in offset_rodas:
        for _ in range(intensidade):
            p = {
                'x': carro_x + wx + random.uniform(-0.1, 0.1),
                'y': 0.1,
                'z': carro_z - 1.5,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(1, 4),
                'vz': -random.uniform(10, 20),
                'vida': 1.0,
                'tamanho': random.uniform(0.05, 0.15)
            }
            PARTICULAS.append(p)

def desenhar_e_atualizar_particulas(dt):
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)
    
    remover = []
    
    glBegin(GL_QUADS)
    for p in PARTICULAS:
        p['x'] += p['vx'] * dt
        p['y'] += p['vy'] * dt
        p['z'] += p['vz'] * dt
        p['vida'] -= dt * 2.0 
        
        if p['vida'] <= 0:
            remover.append(p)
            continue
        
        glColor4f(COR_TERRA[0], COR_TERRA[1], COR_TERRA[2], p['vida'])
        s = p['tamanho']
        glVertex3f(p['x'] - s, p['y'] - s, p['z'])
        glVertex3f(p['x'] + s, p['y'] - s, p['z'])
        glVertex3f(p['x'] + s, p['y'] + s, p['z'])
        glVertex3f(p['x'] - s, p['y'] + s, p['z'])
    glEnd()
    
    for p in remover:
        if p in PARTICULAS: PARTICULAS.remove(p)
    glEnable(GL_LIGHTING)


# DESENHO DO MUNDO

def desenhar_boneco_torcida(x, y, z, cor, escala=1.0):
    quadric = gluNewQuadric()
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(escala, escala, escala)
    
    # Corpo
    glColor3f(*cor)
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quadric, 0.22, 0.18, 0.55, 8, 2)
    glPopMatrix()
    
    # Cabeça
    glColor3f(*COR_PELE)
    glPushMatrix()
    glTranslatef(0, 0.75, 0)
    gluSphere(quadric, 0.22, 8, 8)
    glPopMatrix()
    
    # Mãos
    glPushMatrix(); glTranslatef(-0.30, 0.35, 0); gluSphere(quadric, 0.07, 4, 4); glPopMatrix()
    glPushMatrix(); glTranslatef(0.30, 0.35, 0); gluSphere(quadric, 0.07, 4, 4); glPopMatrix()
    
    glPopMatrix()
    gluDeleteQuadric(quadric)

def desenhar_sol():
    quadric = gluNewQuadric()
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glColor4f(*COR_SOL)
    glTranslatef(50.0, 80.0, -150.0)
    gluSphere(quadric, 15.0, 20, 20)
    glEnable(GL_LIGHTING)
    glPopMatrix()
    gluDeleteQuadric(quadric)

def desenhar_nuvens(tempo):
    quadric = gluNewQuadric()
    glColor4f(*COR_NUVEM)
    glDisable(GL_LIGHTING)
    for nuvem in NUVENS:
        glPushMatrix()
        x_atual = nuvem['x'] + (tempo * nuvem['velocidade'] * 0.5) 
        # Loop da nuvem
        if x_atual > 150: nuvem['x'] = -150; x_atual = -150
        
        glTranslatef(x_atual, nuvem['y'], nuvem['z'])
        # Cria bolinhas aglomeradas
        for i in range(3):
            for j in range(3):
                glPushMatrix()
                glTranslatef(i * 0.5 - 0.5, j * 0.5 - 0.5, 0)
                gluSphere(quadric, nuvem['tamanho'] * 0.3, 8, 8)
                glPopMatrix()
        glPopMatrix()
    glEnable(GL_LIGHTING)
    gluDeleteQuadric(quadric)

def desenhar_chao(movimento_z):
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID_TEXTURA_GRAMA)
    glColor3f(1.0, 1.0, 1.0)
    
    escala_tex = 0.15
    offset_tex = -movimento_z * escala_tex
    tamanho = 400.0
    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0 + offset_tex); glVertex3f(-tamanho, -0.15, -tamanho)
    glTexCoord2f(tamanho * escala_tex, 0.0 + offset_tex); glVertex3f(tamanho, -0.15, -tamanho)
    glTexCoord2f(tamanho * escala_tex, tamanho * escala_tex + offset_tex); glVertex3f(tamanho, -0.15, tamanho)
    glTexCoord2f(0.0, tamanho * escala_tex + offset_tex); glVertex3f(-tamanho, -0.15, tamanho)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)

def desenhar_arquibancada(x_base, z_inicio, z_fim, idx, tempo, lado_direito=False):
    glDisable(GL_LIGHTING)
    degraus = 8
    altura_degrau = 0.6
    profundidade_degrau = 1.0 
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, ID_TEXTURA_MADEIRA)
    glColor3f(1.0, 1.0, 1.0)
    
    # Desenha a estrutura de madeira
    glBegin(GL_QUADS)
    for s in range(degraus):
        if lado_direito: x1, x2 = x_base + (s * profundidade_degrau), x_base + (s * profundidade_degrau) + profundidade_degrau
        else: x1, x2 = x_base - (s * profundidade_degrau), x_base - (s * profundidade_degrau) - profundidade_degrau
        y1, y2 = (s * altura_degrau), (s * altura_degrau) + altura_degrau
        
        # Mapeamento de textura simples
        glTexCoord2f(0, 0); glVertex3f(x1, y1, z_inicio); glTexCoord2f(0, 1); glVertex3f(x1, y2, z_inicio)
        glTexCoord2f(1, 1); glVertex3f(x1, y2, z_fim); glTexCoord2f(1, 0); glVertex3f(x1, y1, z_fim)
        glTexCoord2f(0, 0); glVertex3f(x1, y2, z_inicio); glTexCoord2f(1, 0); glVertex3f(x2, y2, z_inicio)
        glTexCoord2f(1, 1); glVertex3f(x2, y2, z_fim); glTexCoord2f(0, 1); glVertex3f(x1, y2, z_fim)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    
    # Desenha a torcida pulando
    densidade = 2
    for s in range(degraus):
        if lado_direito: x1, x2 = x_base + (s * profundidade_degrau), x_base + (s * profundidade_degrau) + profundidade_degrau
        else: x1, x2 = x_base - (s * profundidade_degrau), x_base - (s * profundidade_degrau) - profundidade_degrau
        y_pos = (s * altura_degrau) + altura_degrau
        
        for k in range(densidade):
            id_assento = (idx * 100) + (s * 10) + k
            if lado_direito: id_assento += 50000
            
            rand_x = math.sin(id_assento * 12.98) * 0.2
            rand_z = math.cos(id_assento * 78.23) * 0.4
            tamanho = 0.9 + (abs(math.sin(id_assento)) * 0.2)
            
            px = (x1 + x2) / 2 + rand_x
            pedaco = (z_fim - z_inicio) / densidade
            pz = z_inicio + (pedaco * k) + (pedaco/2) + rand_z
            
            # Pulo da torcida
            pulo_y = abs(math.sin((tempo + id_assento * 1.5) * (6.0 + math.sin(id_assento)))) * 0.35
            
            desenhar_boneco_torcida(px, y_pos + pulo_y, pz, CORES_TORCIDA[int(abs(id_assento)) % len(CORES_TORCIDA)], escala=tamanho)
    glEnable(GL_LIGHTING)

def desenhar_pista(offset_z, dist_total, tempo, dist_fim_corrida):
    glDisable(GL_LIGHTING)
    mod_offset = offset_z % COMPRIMENTO_SEGMENTO
    idx_inicio = int(dist_total // COMPRIMENTO_SEGMENTO)
    
    glPushMatrix()
    glTranslatef(0, 0, mod_offset)
    
    for i in range(NUM_SEGMENTOS + 6):
        idx_atual = idx_inicio + i
        z_inicio = -(i * COMPRIMENTO_SEGMENTO) + COMPRIMENTO_SEGMENTO 
        z_fim = z_inicio - COMPRIMENTO_SEGMENTO
        
        dist_fim_segmento = (idx_atual * COMPRIMENTO_SEGMENTO) + COMPRIMENTO_SEGMENTO
        eh_linha_chegada = dist_fim_segmento >= dist_fim_corrida and dist_fim_segmento < dist_fim_corrida + COMPRIMENTO_SEGMENTO

        # Linha de chegada
        if eh_linha_chegada:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, ID_TEXTURA_CHEGADA)
            glColor3f(1, 1, 1)
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex3f(-LARGURA_PISTA/2, 0.02, z_inicio) 
            glTexCoord2f(1, 0); glVertex3f(LARGURA_PISTA/2, 0.02, z_inicio)
            glTexCoord2f(1, 1); glVertex3f(LARGURA_PISTA/2, 0.02, z_fim)
            glTexCoord2f(0, 1); glVertex3f(-LARGURA_PISTA/2, 0.02, z_fim)
            glEnd()
            glDisable(GL_TEXTURE_2D)
        
        # Asfalto
        glColor3f(*COR_ASFALTO)
        glBegin(GL_QUADS)
        glVertex3f(-LARGURA_PISTA/2, 0, z_inicio); glVertex3f(LARGURA_PISTA/2, 0, z_inicio)
        glVertex3f(LARGURA_PISTA/2, 0, z_fim); glVertex3f(-LARGURA_PISTA/2, 0, z_fim)
        glEnd()

        # Zebras (Vermelho e Branco)
        if idx_atual % 2 == 0: glColor3f(*COR_ZEBRA_VERMELHA)
        else: glColor3f(*COR_ZEBRA_BRANCA)
        
        largura_zebra = 1.0
        glBegin(GL_QUADS)
        # Esquerda
        glVertex3f(-LARGURA_PISTA/2 - largura_zebra, 0.01, z_inicio); glVertex3f(-LARGURA_PISTA/2, 0.01, z_inicio)
        glVertex3f(-LARGURA_PISTA/2, 0.01, z_fim); glVertex3f(-LARGURA_PISTA/2 - largura_zebra, 0.01, z_fim)
        # Direita
        glVertex3f(LARGURA_PISTA/2, 0.01, z_inicio); glVertex3f(LARGURA_PISTA/2 + largura_zebra, 0.01, z_inicio)
        glVertex3f(LARGURA_PISTA/2 + largura_zebra, 0.01, z_fim); glVertex3f(LARGURA_PISTA/2, 0.01, z_fim)
        glEnd()
        
        # Arquibancadas
        distancia_arq = 6.0 
        desenhar_arquibancada(-LARGURA_PISTA/2 - distancia_arq, z_inicio, z_fim, idx_atual, tempo, False)
        desenhar_arquibancada(LARGURA_PISTA/2 + distancia_arq, z_inicio, z_fim, idx_atual, tempo, True)

    glPopMatrix()
    glEnable(GL_LIGHTING)


# RENDERIZAÇÃO DE TEXTO (GLUT)

def desenhar_texto(x, y, texto):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, LARGURA_TELA, 0, ALTURA_TELA)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    
    glColor3f(*COR_TEXTO)
    glRasterPos2i(x, y)
    
    for char in texto:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


# LOOP PRINCIPAL

def main():
    pygame.init()
    pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Simulador McLaren M23")
    
    inicializar_opengl()
    
    # Instancia o carro e vincula a textura
    mclaren = McLarenM23()
    mclaren.id_textura_roda = ID_TEXTURA_RODA
    
    estado_jogo = ESTADO_MENU
    
    # Variáveis de Controle
    carro_x = 0.0
    carro_z_pos = -6.0
    angulo_roda = 0.0 
    cam_dist = 11.0
    cam_alt = 3.5
    cam_angulo = 0.0
    pista_z = 0.0
    velocidade = 0.0
    tempo_animacao = 0.0 
    distancia_total = 2000.0
    
    ultimo_tempo = time.time()
    rodando = True

    while rodando:
        # Cálculo do Delta Time (dt) para suavidade independente do FPS
        tempo_atual = time.time()
        dt = tempo_atual - ultimo_tempo
        ultimo_tempo = tempo_atual
        
        if dt > 0.1: dt = 0.1 # Evita saltos se travar
        
        tempo_animacao += dt 

        # Eventos Pygame
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if estado_jogo == ESTADO_MENU:
                        estado_jogo = ESTADO_CORRIDA
                        velocidade = 30.0
                        cam_dist = 11.0; cam_alt = 3.5; cam_angulo = 0.0
                        PARTICULAS.clear()
                    elif estado_jogo == ESTADO_FIM:
                        # Reiniciar
                        estado_jogo = ESTADO_MENU
                        pista_z = 0; carro_x = 0; velocidade = 0
                
                if evento.key == pygame.K_r and estado_jogo == ESTADO_FIM:
                    estado_jogo = ESTADO_MENU
                    pista_z = 0; carro_x = 0; velocidade = 0
        
        teclas = pygame.key.get_pressed()
        input_direcao = 0
        tremor_cam_y = 0.0 
        
        if estado_jogo == ESTADO_CORRIDA:
            # Direção
            if teclas[pygame.K_a]: 
                carro_x -= 15.0 * dt
                input_direcao = 20 
            elif teclas[pygame.K_d]: 
                carro_x += 15.0 * dt
                input_direcao = -20 
            
            # Checa se saiu da pista (física simples de grama)
            limite_pista = (LARGURA_PISTA / 2.0) 
            na_grama = abs(carro_x) > limite_pista

            # Aceleração / Freio
            if teclas[pygame.K_w]: 
                if na_grama: velocidade += 5.0 * dt 
                else: velocidade += 25.0 * dt 
            elif teclas[pygame.K_s]: 
                velocidade -= 40.0 * dt 
            else: 
                velocidade -= 5.0 * dt # Desaceleração natural
            
            # Penalidade na grama
            if na_grama:
                velocidade -= 35.0 * dt
                if velocidade > 1.0:
                    tremor_cam_y = random.uniform(-0.05, 0.05)
                    gerar_particulas(carro_x, carro_z_pos, intensidade=2)

            # Limites de velocidade
            if velocidade > VELOCIDADE_MAX: velocidade = VELOCIDADE_MAX
            if velocidade < 0: velocidade = 0
            
            pista_z += velocidade * dt
            angulo_roda -= velocidade * 15.0 * dt 
            
            # Checagem de fim de corrida
            if pista_z >= distancia_total: 
                estado_jogo = ESTADO_FIM
                velocidade = 0
        
        # Controle de Câmera (Setas)
        if teclas[pygame.K_LEFT]:  cam_angulo -= 2.0 * dt
        if teclas[pygame.K_RIGHT]: cam_angulo += 2.0 * dt
        if teclas[pygame.K_UP]:    cam_alt += 5.0 * dt
        if teclas[pygame.K_DOWN]:  cam_alt -= 5.0 * dt
        
        # Giro automático da câmera no menu
        if estado_jogo == ESTADO_MENU and not (teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]): 
            cam_angulo += 0.5 * dt
        
        # Limites da câmera
        if cam_alt < 0.5: cam_alt = 0.5
        if cam_dist < 3.0: cam_dist = 3.0

        # --- RENDERIZAÇÃO ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Posicionamento da Câmera
        alt_final = cam_alt + tremor_cam_y
        cam_x_mundo = carro_x + math.sin(cam_angulo) * cam_dist
        cam_z_mundo = carro_z_pos + math.cos(cam_angulo) * cam_dist
        gluLookAt(cam_x_mundo, alt_final, cam_z_mundo, carro_x, 1.0, carro_z_pos, 0, 1, 0)               

        configurar_luz_carro()
        desenhar_sol()
        desenhar_nuvens(tempo_animacao)
        desenhar_chao(pista_z)
        desenhar_pista(pista_z, pista_z, tempo_animacao, distancia_total) 

        desenhar_e_atualizar_particulas(dt)

        # Atualiza e desenha o carro
        mclaren.posicao = [carro_x, 0.15, carro_z_pos]
        mclaren.rotacao_roda = angulo_roda
        mclaren.angulo_direcao = input_direcao
        mclaren.rotacao_y = input_direcao + 180 
        mclaren.desenhar()
        
        # --- HUD / TEXTOS ---
        if estado_jogo == ESTADO_MENU:
            # Título
            desenhar_texto(LARGURA_TELA//2 - 100, ALTURA_TELA//2 + 50, "SIMULADOR MCLAREN M23")
            # Iniciar
            desenhar_texto(LARGURA_TELA//2 - 110, ALTURA_TELA//2 - 20, "PRESSIONE ENTER PARA INICIAR")
            # Direção
            desenhar_texto(LARGURA_TELA//2 - 90, ALTURA_TELA//2 - 60, "W, A, S, D PARA DIRIGIR")
            # NOVO: Controle da Câmera (Setas)
            desenhar_texto(LARGURA_TELA//2 - 120, ALTURA_TELA//2 - 100, "SETAS PARA MOVER A CÂMERA")
        
        elif estado_jogo == ESTADO_CORRIDA:
            vel_display = int(velocidade * 3) # Escala fictícia para parecer mais rápido
            desenhar_texto(20, ALTURA_TELA - 50, f"VELOCIDADE: {vel_display} KM/H")
            desenhar_texto(20, ALTURA_TELA - 90, f"DISTANCIA: {int(pista_z)}m / {int(distancia_total)}m")
            
            if na_grama and velocidade > 5:
                 desenhar_texto(LARGURA_TELA//2 - 60, ALTURA_TELA - 150, "!!! FORA DA PISTA !!!")

        elif estado_jogo == ESTADO_FIM:
            desenhar_texto(LARGURA_TELA//2 - 90, ALTURA_TELA//2 + 50, "CORRIDA FINALIZADA!")
            desenhar_texto(LARGURA_TELA//2 - 110, ALTURA_TELA//2 - 20, "PRESSIONE ENTER PARA REINICIAR")

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()