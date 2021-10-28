attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

// uniform vec4 u_color;
// GLOBAL COORDINATES
uniform vec4 u_eye_position;

uniform vec4 u_light_position[2];

varying vec2 v_uv;
varying vec4 v_normal;
varying vec4 v_s[2];
varying vec4 v_h[2];

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	v_uv = a_uv;

//	Local coordinates
	position = u_model_matrix * position;
	v_normal = u_model_matrix * normal;

//	Local coordinates
    vec4 v = u_eye_position - position;
    for (int i = 0; i < 2; i++) {
        v_s[i] = u_light_position[i] - position;
        v_h[i] = v_s[i] + v;
    }


	position = u_projection_matrix * (u_view_matrix * position);

	gl_Position = position;
}