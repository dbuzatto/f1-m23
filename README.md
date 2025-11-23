# 🏁 Simulador McLaren M23 (1976) – Computação Gráfica

Este projeto é uma simulação gráfica em Python utilizando **PyOpenGL** e **Pygame**, recriando de forma estilizada o lendário carro de Fórmula 1 **McLaren M23 do ano de 1976**.

**Projeto:** Simulador da McLaren M23 (1976)  
**Autor:** Diogo Buzatto  
**RA:** 111809  
**Disciplina:** Computação Gráfica  

---

## 🚗 Sobre o Projeto

O simulador demonstra conceitos essenciais de Computação Gráfica, incluindo:

- Modelagem geométrica procedural do carro McLaren M23 (1976)
- Transformações e visualização em 3D
- Texturas geradas via código
- Renderização utilizando primitivas OpenGL (`GL_QUADS`, `GL_LINES`, etc.)
- Sistema simples de movimentação e partículas
- Câmera controlável em tempo real

---

## 🛠️ Requisitos

Conforme especificado em `requirements.txt`:

- `pygame`
- `PyOpenGL`
- `numpy`

---

## 💾 Instalação e Execução

### 1. Criar ambiente virtual (opcional, recomendado)

macOS/Linux:

~~~bash
python3 -m venv venv
source venv/bin/activate
~~~

Windows:

~~~bash
python -m venv venv
venv\Scripts\activate
~~~

### 2. Instalar dependências

~~~bash
pip install -r requirements.txt
~~~

Ou manualmente:

~~~bash
pip install pygame PyOpenGL PyOpenGL-accelerate numpy
~~~

### 3. Executar o projeto

~~~bash
python3 scene.py
~~~

---

## 🎮 Controles

### Carro

- **W** – Acelerar  
- **S** – Frear / Ré  
- **A / D** – Virar para esquerda / direita  

### Câmera

- **↑ / ↓ / ← / →** – Ajuste de ângulo e zoom da câmera  

### Geral

- **ENTER** – Iniciar corrida / Reiniciar simulação  

---

## 🧩 Detalhes Técnicos

- Cena construída puramente com **PyOpenGL**
- Uso de **GLUT** para renderização de texto bitmap
- Texturas procedurais (grama, madeira, rodas) geradas em tempo de execução
- Estrutura principal e lógica da cena no arquivo `scene.py`
- Arquivo `main.py` como ponto de entrada/organização do projeto (se utilizado)

---

## 📌 Observações

Este projeto foi desenvolvido como trabalho acadêmico para a disciplina de **Computação Gráfica**, utilizando o carro **McLaren M23 (1976)** como tema central para aplicação prática de conceitos de modelagem 3D, texturização procedural e pipeline gráfico.
