#version 330 core
in vec2 TexCoords;
out vec4 FragColor;

uniform sampler2D texture_diffuse;

void main()
{
    // Apenas exibe a textura do objeto (ou cor padrão se não houver)
    FragColor = texture(texture_diffuse, TexCoords);
}