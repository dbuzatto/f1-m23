# 🏁 Simulador McLaren M23 (1976) – Computação Gráfica

Simulação interativa desenvolvida em **Python + PyOpenGL + Pygame** que recria, em tempo real, uma volta com a lendária **McLaren M23 (1976)**. O projeto foi construído como trabalho da disciplina de Computação Gráfica e reúne modelagem procedural, texturas geradas por código e um loop de jogo completo (menu → corrida → game over).

**Projeto:** Simulador da McLaren M23 (1976)  
**Autor:** Diogo Buzatto  
**RA:** 111809  
**Disciplina:** Computação Gráfica  

---

## 🚗 Visão Geral

- Carro modelado via primitivas do OpenGL (quads, linhas e quadrics) com detalhes de cockpit, asas, rodas texturizadas e piloto animado.
- Pista infinita com curvas suaves, zebras dinâmicas, arquibancadas com torcida animada e partículas de poeira quando o carro sai da pista.
- Ambiente com **fog**, iluminação básica, sol, nuvens animadas e texturas procedurais de grama, madeira e roda geradas em tempo de execução.
- HUD com velocidade aproximada em km/h, distância percorrida e alertas quando o carro pisa na grama.
- Máquina de estados simples: tela inicial com câmera em órbita, corrida e tela de game over ao bater nas arquibancadas.

---

## 🧱 Arquitetura do Projeto

| Arquivo | Descrição |
| --- | --- |
| `main.py` | Declara a classe `McLarenM23`, responsável por desenhar o carro, piloto e animações de rodas/direção. |
| `scene.py` | Loop principal do jogo: inicialização do OpenGL, geração de texturas procedurais, ambiente, lógica de estados, câmera e controles. Execute este arquivo para rodar o simulador. |
| `requirements.txt` | Lista as dependências necessárias (Pygame, PyOpenGL e NumPy). |

---

## 🛠️ Requisitos

Instale as dependências listadas em `requirements.txt`:

- `pygame`
- `PyOpenGL`
- `numpy`

---

## 💾 Instalação e Execução

1. *(Opcional)* Crie e ative um ambiente virtual
   - macOS/Linux
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Windows
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
2. Instale as dependências
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o simulador
   ```bash
   python scene.py
   ```

---

## 🎮 Controles

| Ação | Tecla |
| --- | --- |
| Iniciar / reiniciar corrida | `ENTER` |
| Acelerar / Frear (ré) | `W` / `S` |
| Virar esquerda / direita | `A` / `D` |
| Ajustar câmera (órbita / altura) | Setas `← → ↑ ↓` |

Quando o carro sai da pista, a velocidade reduz, a câmera treme e partículas de sujeira aparecem. Bater nas arquibancadas encerra a corrida (tela *Game Over*).

---

## 🧩 Detalhes Técnicos

- Renderização 3D inteira em **PyOpenGL**, com **GLUT** para a escrita do HUD.
- Texturas procedurais geradas na inicialização (grama, madeira das arquibancadas, bandeira de chegada e calota das rodas).
- Sistema de partículas simples para poeira, controlado pelo estado do carro.
- Fog exponencial e iluminação ambiente/difusa para dar profundidade à cena.
- Câmera orbitando o carro, com distância e altura ajustáveis em tempo real.

---