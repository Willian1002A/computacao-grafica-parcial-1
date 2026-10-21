# Visualizador 3D - Atividade Parcial (Transformações e Seleção)

Aplicação desenvolvida em Python (PyOpenGL, GLFW, PyGLM) para a disciplina de Computação Gráfica. O projeto implementa a leitura e exibição de múltiplos modelos 3D em malhas Wavefront (`.obj` e `.mtl`), com suporte à seleção dinâmica de objetos via teclado e aplicação interativa de transformações geométricas (Translação, Rotação e Escala).

## Execução e Setup

1. Instalar as dependências:
```bash
pip install -r requirements.txt

```

2. Executar a aplicação:
```bash
python main.py

```



*Nota: Os objetos e suas posições iniciais são carregados diretamente a partir dos assets locais do projeto.*

## Controles

* **TAB:** Alterna a seleção entre os objetos disponíveis na cena
* **W, A, S, D:** Movimentação da câmera
* **E / Q:** Elevação da câmera (subir / descer)
* **Botão Direito do Mouse:** Girar a visualização
* **J / L:** Translação do objeto selecionado no eixo X (Esquerda / Direita)
* **U / O:** Translação do objeto selecionado no eixo Y (Cima / Baixo)
* **I / K:** Translação do objeto selecionado no eixo Z (Frente / Trás)
* **R / F:** Rotação do objeto selecionado no eixo X
* **T / G:** Rotação do objeto selecionado no eixo Y
* **Y / H:** Rotação do objeto selecionado no eixo Z
* **N / M:** Diminuir / Aumentar a escala do objeto selecionado
* **ESC:** Encerra a aplicação

## Estrutura do Projeto

* `main.py`: Inicialização do GLFW, loop de renderização, gerenciamento da lista de objetos, estado de seleção e tratamento de eventos.
* `camera.py`: Classe de controle de câmera com matrizes View (`lookAt`) e Projection (`perspective`).
* `obj_loader.py`: Parser para carregamento de malhas `.obj`, arquivos de material `.mtl` e texturas 2D.
* `shader.py`: Utilitário para compilação e gerenciamento de programas GLSL.
* `shaders/vertex_shader.glsl`: Transformações geométricas de vértices (MVP).
* `shaders/fragment_shader.glsl`: Aplicação de texturas e cores na rasterização.
* `requirements.txt`: Lista de dependências do projeto.