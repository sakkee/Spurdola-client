from distutils.core import setup
import py2exe, sys, os, numpy
import pygame
from modulefinder import Module
sys.argv.append('py2exe')


def numpy_dll_paths_fix():
    paths = set()
    np_path = numpy.__path__[0]
    for dirpath, _, filenames in os.walk(np_path):
        for item in filenames:
            if item.endswith('.dll'):
                paths.add(dirpath)

    sys.path.append(*list(paths))

numpy_dll_paths_fix()
class pygame2exe(py2exe.build_exe.py2exe): #This hack make sure that pygame default font is copied: no need to modify code for specifying default font
    def copy_extensions(self, extensions):
        #Get pygame default font
        pygamedir = os.path.split(pygame.base.__file__)[0]
        pygame_default_font = os.path.join(pygamedir, pygame.font.get_default_font())
        #print pygame.font.get_default_font(), "PYGAMEDIR"
        #Add font to list of extension to be copied
        extensions.append(Module("pygame.font", pygame_default_font))
        py2exe.build_exe.py2exe.copy_extensions(self, extensions)


setup(
    cmdclass = {'py2exe': pygame2exe},
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': "mapcreator.py"}],
    zipfile = None
)