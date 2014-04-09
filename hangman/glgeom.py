from math import *
from pyglet.gl import *

TWOPI = pi * 2


def compile(pointer, *args, **kwargs):
    """
        Runs a function in a display list.
    """
    display = glGenLists(1) # Generate list
    glNewList(display, GL_COMPILE) # Initiate
    pointer(*args, **kwargs) # Run function
    glEndList() # end
    return display # and return list id

def torus(major_radius, minor_radius, n_major, n_minor, material, shininess=125):
    """
        Torus function inspired from the OpenGL red book.
    """
    glPushAttrib(GL_CURRENT_BIT) # Push material attribute so we don't destroy the scene
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, material)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (GLfloat * 4)(1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, shininess)

    major_s = TWOPI / n_major
    minor_s = TWOPI / n_minor

    def n(x, y, z):
        """
            Normalize a given vector.
        """
        m = 1.0 / sqrt(x * x + y * y + z * z)
        return [x * m, y * m, z * m]

    for i in xrange(n_major):
        a0 = i * major_s
        a1 = a0 + major_s
        x0 = cos(a0)
        y0 = sin(a0)
        x1 = cos(a1)
        y1 = sin(a1)

        glBegin(GL_TRIANGLE_STRIP)

        for j in xrange(n_minor + 1):
            b = j * minor_s
            c = cos(b)
            r = minor_radius * c + major_radius
            z = minor_radius * sin(b)

            glNormal3fv((GLfloat * 3)(*n(x0 * c, y0 * c, z / minor_radius)))
            glVertex3f(x0 * r, y0 * r, z)

            glNormal3fv((GLfloat * 3)(*n(x1 * c, y1 * c, z / minor_radius)))
            glVertex3f(x1 * r, y1 * r, z)

        glEnd()
    glPopAttrib()