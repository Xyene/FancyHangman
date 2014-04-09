import sys

try:
    from pyglet.gl import *
    from pyglet.window import key, mouse
except ImportError:
    print "Pyglet not installed correctly, or at all."
    sys.exit()

from glgeom import *

from time import clock
from conex import *

TORUS_DETAIL = 7         # 2 ** detail edges/torus
TICKS_PER_SECOND = 100   # How many times to update/second
LIGHTING = True
SHADING = True


class Applet(pyglet.window.Window):
    def update(self, dt):
        self.rot += 2.5 # Make torus rotate slightly

        width, height = 80, 48
        pixels = (3 * width * height * GLubyte)()
        # Read screen buffer
        glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE, pixels)
        DIM = FOREGROUND_BLUE
        NORMAL = DIM | FOREGROUND_INTENSITY

        if not SHADING:
            DIM = NORMAL

        cursor_pos(0, 0) # Reset cursor position
        # Convert pixels to ASCII
        for y in xrange(0, height * 3, 3):
            for x in xrange(0, width * 3, 3):
                i = y * width + x
                r, g, b = pixels[i:i + 3]

                # Calculate the light value of the pixel, 0..1
                # Green is brightest: has a higher amplifier
                l = (0.3 * r + 0.4 * g + 0.3 * b) / 255

                # Determine best suited character & colour for light value
                if l <= 0.1:
                    printc(DIM, " ")
                elif l <= 0.2:
                    printc(DIM, ":")
                elif l <= 0.3:
                    printc(DIM, "I")
                elif l <= .4:
                    printc(DIM, "Y")
                elif l <= .5:
                    printc(DIM, "N")
                elif l <= .7:
                    printc(DIM, "B")
                else:
                    printc(NORMAL, "N")

        d = clock() - self.start_time # Get time elapsed since startup
        printc(FOREGROUND_GREEN | FOREGROUND_INTENSITY, # Notify
               "Loading der Hangman... %.1f seconds remaining...\t" % max(10 - d, 0))

        flushc()
        if d >= 10: # Loading screen should exit after 10 seconds have passed
            pyglet.app.EventLoop.has_exit = True

    def __init__(self, *args, **kwargs):
        super(Applet, self).__init__(*args, **kwargs)
        self.start_time = clock()
        self.rot = 0
        # Refresh the console buffer
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SECOND)

        glClearColor(0, 0, 0, 1) # Black background
        glClearDepth(1.0)

        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

        glMatrixMode(GL_MODELVIEW)
        # This does not need to be here, but it makes me happy that it is
        glEnable(GL_POLYGON_OFFSET_FILL)

        fv4 = GLfloat * 4

        if LIGHTING:
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_LIGHT1)

            # Verbose lighting fun
            glLightfv(GL_LIGHT0, GL_POSITION, fv4(.5, .5, 1, 0))
            glLightfv(GL_LIGHT0, GL_SPECULAR, fv4(.5, .5, 1, 1))
            glLightfv(GL_LIGHT0, GL_DIFFUSE, fv4(1, 1, 1, 1))
            glLightfv(GL_LIGHT1, GL_POSITION, fv4(1, 0, .5, 0))
            glLightfv(GL_LIGHT1, GL_DIFFUSE, fv4(.5, .5, .5, 1))
            glLightfv(GL_LIGHT1, GL_SPECULAR, fv4(1, 1, 1, 1))

        # Compile a torus display list
        self.torus_id = compile(torus, 3, 0.5, TORUS_DETAIL ** 2, TORUS_DETAIL ** 2, fv4(1, 1, 0, 1))

        print "Bootloader initialized in %s seconds." % (clock() - self.start_time)

    def on_resize(self, width, height):
        """
            Dummy resize method. Does nothing but update viewport.
        """
        glViewport(0, 0, 80, 50)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # A field of view of 45
        gluPerspective(45.0, 80 / float(50), 0.1, 50000000.0)
        glMatrixMode(GL_MODELVIEW)

    def on_draw(self):
        """
            Draws the scene.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear all relevant buffers
        glLoadIdentity()

        glPushMatrix()
        glTranslatef(0, 0, -10) # Move the torus a bit back
        glRotatef(self.rot, 0, 1, 0)
        glPushAttrib(GL_CURRENT_BIT) # Push material state
        glCallList(self.torus_id) # Draw the torus
        glPopAttrib() # Pop material state to restore colouring
        glPopMatrix() # Dispose of the translated matrix