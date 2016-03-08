import os
from os.path import join, abspath, dirname

PARAMETER_DIR = abspath(join(dirname(__file__), '..', 'parameters', 'params'))

BLUE_PARAMS = 'blue.p'
BLUE_PARAMS_DEFAULT = {'b1': 101, 'g1': 45, 'r1': 30, 'b2': 180, 'g2': 143, 'r2': 101}

PINK_PARAMS = 'pink.p'
PINK_PARAMS_DEFAULT = {'b1': 0, 'g1': 0, 'r1': 75, 'b2': 195, 'g2': 79, 'r2': 206}

HOUGHLINES_PARAMS = 'houghlines.p'
HOUGHLINES_PARAMS_DEFAULT = {'canny_threshold1': 50,'canny_threshold2': 150,'canny_apertureSize': 3,'rho': 1,'theta': 180,'threshold': 200}

CIRCLE_PARAMS = 'circles.p'
CIRCLE_PARAMS_DEFAULT = {'dp': 1,'minDist': 33,'param1': 51,'param2': 27,'minRadius': 9,'maxRadius': 25}
