'''
Matplotlib parameters to create pretty plots
'''

from matplotlib import rc, rcParams


DEF_AXIS_LEFT = 0.15
DEF_AXIS_RIGHT = 0.95
DEF_AXIS_BOTTOM = 0.1
DEF_AXIS_TOP = 0.95
DEF_AXIS_WIDTH = DEF_AXIS_RIGHT - DEF_AXIS_LEFT
DEF_AXIS_HEIGHT = DEF_AXIS_TOP - DEF_AXIS_BOTTOM
# add_axes takes [left, bottom, width, height]
DEF_AXES = [DEF_AXIS_LEFT, DEF_AXIS_BOTTOM, DEF_AXIS_WIDTH, DEF_AXIS_HEIGHT]

AXIS_2Y_RIGHT = 0.8
AXIS_2Y_WIDTH = AXIS_2Y_RIGHT - DEF_AXIS_LEFT
AXES_2Y = [DEF_AXIS_LEFT, DEF_AXIS_BOTTOM, AXIS_2Y_WIDTH, DEF_AXIS_HEIGHT]

AXES_LABELSIZE = 16
TICK_LABELSIZE = 16
TEXT_LABELSIZE = 16

COLOR_LIGHTGRAY = '#cccccc'

#COLOR_HLINES = '#606060'
COLOR_HLINES = 'black'
HLINE_LABELSIZE = 24
HLINE_LINEWIDTH = 2

rc('axes', **{'labelsize' : 'large',
              'titlesize' : 'large',
              'grid' : True})
rc('legend', **{'fontsize': 'xx-large'})
rcParams['axes.labelsize'] = AXES_LABELSIZE
rcParams['xtick.labelsize'] = TICK_LABELSIZE
rcParams['ytick.labelsize'] = TICK_LABELSIZE
rcParams['xtick.major.pad'] = 4
rcParams['ytick.major.pad'] = 6
rcParams['figure.subplot.top'] = DEF_AXIS_TOP
rcParams['figure.subplot.bottom'] = DEF_AXIS_BOTTOM
rcParams['figure.subplot.left'] = DEF_AXIS_LEFT
rcParams['figure.subplot.right'] = DEF_AXIS_RIGHT
rcParams['lines.linewidth'] = 2
rcParams['grid.color'] = COLOR_LIGHTGRAY
rcParams['grid.linewidth'] = 0.6
rcParams['ps.useafm'] = True
rcParams['pdf.use14corefonts'] = True
#rcParams['text.usetex'] = True

def quarter_size():
    QUARTER_AXIS_LEFT = 0.25
    QUARTER_AXIS_RIGHT = 0.92
    QUARTER_AXIS_BOTTOM = 0.20
    QUARTER_AXIS_TOP = 0.95
    QUARTER_AXIS_WIDTH = QUARTER_AXIS_RIGHT - QUARTER_AXIS_LEFT
    QUARTER_AXIS_HEIGHT = QUARTER_AXIS_TOP - QUARTER_AXIS_BOTTOM

    QUARTER_AXES_LABELSIZE = 40
    QUARTER_TICK_LABELSIZE = 40
    QUARTER_TEXT_LABELSIZE = 40

    rc('axes', **{'labelsize' : 'xx-large',
                  'titlesize' : 'xx-large',
                  'grid' : True})
    rc('legend', **{'fontsize': 'xx-large'})
    rcParams['axes.labelsize'] = QUARTER_AXES_LABELSIZE
    rcParams['xtick.labelsize'] = QUARTER_TICK_LABELSIZE
    rcParams['ytick.labelsize'] = QUARTER_TICK_LABELSIZE
    rcParams['xtick.major.pad'] = 16
    rcParams['ytick.major.pad'] = 20
    rcParams['figure.subplot.top'] = QUARTER_AXIS_TOP
    rcParams['figure.subplot.bottom'] = QUARTER_AXIS_BOTTOM
    rcParams['figure.subplot.left'] = QUARTER_AXIS_LEFT
    rcParams['figure.subplot.right'] = QUARTER_AXIS_RIGHT
