uniform vec4 u_global_ambient;

// uniform vec4 u_light_diffuse;
// uniform vec4 u_light_specular;
// uniform vec4 u_light_ambient;

uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;
uniform vec4 u_mat_ambient;
uniform float u_mat_shininess;

uniform vec4 u_light_diffuse[2];
uniform vec4 u_light_specular[2];
uniform vec4 u_light_ambient[2];

varying vec4 v_normal;
varying vec4 v_s[2];
varying vec4 v_h[2];


float calc_lambert(vec4 s) {
    return max(dot(normalize(v_normal), normalize(s)), 0.0);
}

float calc_phong(vec4 h) {
    return max(dot(normalize(v_normal), normalize(h)), 0.0);
}

void main(void)
{
    vec4 stuff = vec4(0.0, 0.0, 0.0, 1.0);

    for (int i = 0; i < 2; i++) {
        float lambert = calc_lambert(v_s[i]);
        float phong = calc_phong(v_h[i]);

        stuff += (u_light_diffuse[i] * u_mat_diffuse * lambert
			    + u_light_specular[i] * u_mat_specular * pow(phong, u_mat_shininess)
                + u_light_ambient[i] * u_mat_ambient);
    }

	gl_FragColor = stuff;
            // + u_global_ambient * u_light_ambient;
}