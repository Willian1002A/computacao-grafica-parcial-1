import glfw
from OpenGL.GL import *
import glm

from camera import Camera
from shader import Shader
from obj_loader import load_obj, parse_mtl, load_texture


class Object3D:
    def __init__(self, name, vao, vbo, vertex_count, texture_id, material, pos, rot, scale):
        self.name = name
        self.vao = vao
        self.vbo = vbo
        self.vertex_count = vertex_count
        self.texture_id = texture_id
        self.material = material

        self.pos = glm.vec3(*pos)
        self.rot = glm.vec3(*rot)
        self.scale = glm.vec3(*scale)


camera = None
objects = []
selected_idx = 0
keys = {}

mouse_active = False
last_mouse_x = 0.0
last_mouse_y = 0.0


def key_callback(window, key, scancode, action, mods):
    global selected_idx

    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        elif key == glfw.KEY_TAB:
            selected_idx = (selected_idx + 1) % len(objects)
            obj = objects[selected_idx]
            print(f"Objeto selecionado [{selected_idx + 1}]: {obj.name}")

    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False


def mouse_button_callback(window, button, action, mods):
    global mouse_active, last_mouse_x, last_mouse_y
    if button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            mouse_active = True
            last_mouse_x, last_mouse_y = glfw.get_cursor_pos(window)
        elif action == glfw.RELEASE:
            mouse_active = False


def cursor_pos_callback(window, xpos, ypos):
    global last_mouse_x, last_mouse_y
    if mouse_active:
        dx = xpos - last_mouse_x
        dy = last_mouse_y - ypos
        last_mouse_x, last_mouse_y = xpos, ypos
        camera.process_mouse(dx, dy)


def framebuffer_size_callback(window, width, height):
    if height > 0:
        glViewport(0, 0, width, height)


def process_inputs(dt):
    # Movimentação da Câmera
    if keys.get(glfw.KEY_W, False): camera.process_keyboard("FORWARD", dt)
    if keys.get(glfw.KEY_S, False): camera.process_keyboard("BACKWARD", dt)
    if keys.get(glfw.KEY_A, False): camera.process_keyboard("LEFT", dt)
    if keys.get(glfw.KEY_D, False): camera.process_keyboard("RIGHT", dt)
    if keys.get(glfw.KEY_E, False): camera.process_keyboard("UP", dt)
    if keys.get(glfw.KEY_Q, False): camera.process_keyboard("DOWN", dt)

    if not objects:
        return
    
    obj = objects[selected_idx]
    v_speed = 3.0 * dt
    r_speed = 60.0 * dt
    s_speed = 1.0 * dt

    # Translação (J/L: X, U/O: Y, I/K: Z)
    if keys.get(glfw.KEY_J, False): obj.pos.x -= v_speed
    if keys.get(glfw.KEY_L, False): obj.pos.x += v_speed
    if keys.get(glfw.KEY_U, False): obj.pos.y += v_speed
    if keys.get(glfw.KEY_O, False): obj.pos.y -= v_speed
    if keys.get(glfw.KEY_I, False): obj.pos.z -= v_speed
    if keys.get(glfw.KEY_K, False): obj.pos.z += v_speed

    # Rotação (R/F: X, T/G: Y, Y/H: Z)
    if keys.get(glfw.KEY_R, False): obj.rot.x += r_speed
    if keys.get(glfw.KEY_F, False): obj.rot.x -= r_speed
    if keys.get(glfw.KEY_T, False): obj.rot.y += r_speed
    if keys.get(glfw.KEY_G, False): obj.rot.y -= r_speed
    if keys.get(glfw.KEY_Y, False): obj.rot.z += r_speed
    if keys.get(glfw.KEY_H, False): obj.rot.z -= r_speed

    # Escala (N diminui, M aumenta)
    s_speed = 2.0 * dt
    if keys.get(glfw.KEY_N, False):
        obj.scale = glm.max(glm.vec3(0.05), obj.scale - glm.vec3(s_speed))
    if keys.get(glfw.KEY_M, False):
        obj.scale += glm.vec3(s_speed)


def setup_scene():
    global objects

    obj_path = "assets/pillar.obj"
    mtl_path = "assets/pillar.mtl"
    tex_path = "assets/pillar_diffuse.png"

    vao, vbo, count = load_obj(obj_path)
    material = parse_mtl(mtl_path)
    tex_id = load_texture(tex_path)

    obj1 = Object3D(
        name="Pilar 1",
        vao=vao, vbo=vbo, vertex_count=count,
        texture_id=tex_id, material=material,
        pos=[-1.5, 0.0, 0.0], rot=[0.0, 0.0, 0.0], scale=[1.0, 1.0, 1.0]
    )

    # Objeto 2 (Exemplo à direita - reutiliza os buffers para instanciar outro na tela)
    obj2 = Object3D(
        name="Pilar 2",
        vao=vao, vbo=vbo, vertex_count=count,
        texture_id=tex_id, material=material,
        pos=[1.5, 0.0, 0.0], rot=[0.0, 45.0, 0.0], scale=[1.0, 1.0, 1.0]
    )

    objects.append(obj1)
    objects.append(obj2)


def main():
    global camera
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(1280, 720, "Atividade Parcial - Transformacoes 3D", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.15, 0.15, 0.2, 1.0)

    # Shaders simplificados para cor pura / textura básica (sem luzes)
    shader = Shader("shaders/vertex_shader.glsl", "shaders/fragment_shader.glsl")
    camera = Camera(position=(0.0, 2.0, 5.0))

    setup_scene()

    print("Aplicação iniciada.")
    print("Controles: TAB (Selecionar Objeto), WASD (Câmera), J/L U/O I/K (Translação), R/F T/G Y/H (Rotação), N/M (Escala)")

    last_time = glfw.get_time()

    while not glfw.window_should_close(window):
        current_time = glfw.get_time()
        dt = current_time - last_time
        last_time = current_time

        # Atualiza o título da janela com o objeto selecionado e suas coordenadas
        if objects:
            cur = objects[selected_idx]
            glfw.set_window_title(
                window, 
                f"Parcial | Selecionado [{selected_idx+1}]: {cur.name} | Pos: [{cur.pos.x:.2f}, {cur.pos.y:.2f}, {cur.pos.z:.2f}]"
            )

        process_inputs(dt)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        shader.use()

        # Matrizes de Câmera
        w, h = glfw.get_framebuffer_size(window)
        aspect = w / max(1, h)
        shader.set_mat4("projection", camera.get_projection_matrix(aspect))
        shader.set_mat4("view", camera.get_view_matrix())

        # Renderiza os objetos da lista
        for obj in objects:
            model = glm.mat4(1.0)
            model = glm.translate(model, obj.pos)
            model = glm.rotate(model, glm.radians(obj.rot.x), glm.vec3(1, 0, 0))
            model = glm.rotate(model, glm.radians(obj.rot.y), glm.vec3(0, 1, 0))
            model = glm.rotate(model, glm.radians(obj.rot.z), glm.vec3(0, 0, 1))
            model = glm.scale(model, obj.scale)
            
            shader.set_mat4("model", model)

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, obj.texture_id)
            shader.set_int("texture_diffuse", 0)

            glBindVertexArray(obj.vao)
            glDrawArrays(GL_TRIANGLES, 0, obj.vertex_count)
            glBindVertexArray(0)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()