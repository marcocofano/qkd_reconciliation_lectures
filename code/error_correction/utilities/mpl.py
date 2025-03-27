import matplotlib.pyplot as plt
from cycler import cycler
import numpy as np
import matplotlib
import argparse


#https://stackoverflow.com/questions/11367736/matplotlib-consistent-font-using-latex
def init(font_size=None, legend_font_size=None, modify_cycler=True, tick_size=None):
    custom_cycler = (cycler(color=['r', 'b', 'g', 'y', 'k', 'm', 'c']*4) +
                     cycler(linestyle=['-', '--', ':', '-.']*7))
    if modify_cycler: plt.rc('axes', prop_cycle=custom_cycler)
    matplotlib.rcParams['mathtext.fontset'] = 'stix'
    matplotlib.rcParams['font.family'] = 'STIXGeneral'
    if font_size: matplotlib.rcParams.update({'font.size': font_size})
    if legend_font_size: plt.rc('legend', fontsize=legend_font_size)    # legend fontsize
    # https://stackoverflow.com/questions/3899980/how-to-change-the-font-size-on-a-matplotlib-plot
    if tick_size:
        matplotlib.rcParams['xtick.labelsize'] = tick_size
        matplotlib.rcParams['ytick.labelsize'] = tick_size
    # https://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller

def fmt_ax(ax, xlab, ylab, leg, grid=1, grid_kwargs={}):
    if leg: ax.legend(loc='best')
    if xlab: ax.set_xlabel(xlab)
    if ylab: ax.set_ylabel(ylab)
    if grid: ax.grid(alpha=0.7, linestyle='-.', linewidth=0.3, **grid_kwargs)
    ax.tick_params(axis='both')

def save_show_fig(args, plt, file_path):
    plt.tight_layout()
    if args.save:
        ext_str = ','.join(args.ext)
        if len(args.ext)>1: ext_str = f'{{{ext_str}}}'
        print(f'Saving figure to {file_path}.{ext_str}')
        for ext in args.ext:
            plt.savefig('%s.%s'%(file_path,ext), bbox_inches='tight', pad_inches=args.pad_inches)
    if not args.silent: plt.show()

def bind_fig_save_args(parser):
    parser.add_argument('--silent', help='do not show plots', action='store_true')
    parser.add_argument('--save', help='save plots', action='store_true')
    exts_ = ['png', 'pdf']
    parser.add_argument('--ext', help='plot save extention', nargs='*', default=exts_, choices=exts_)
    parser.add_argument('--pad_inches', type=float, default=None) # good choice is 0.03

def get_subplot_config(count):
    return {1:(1,1), 2:(1,2), 3:(1,3), 4:(2,2),
            5:(2,3), 6:(2,3),
            7:(3,3), 8:(3,3), 9:(3,3),
            10:(3,4), 11:(3,4), 12:(3,4),
            13:(4,4), 14:(4,4), 15:(4,4), 16:(4,4),
            17:(4,5), 18:(4,5), 19:(4,5), 20:(4,5),
           }[count]

def get_subplot_axes(ax_size, count, fig=None):
    # ax_size = [width, height] per axis
    if fig is None: fig = plt.gcf()
    rows_cols = get_subplot_config(count)
    fig.set_size_inches(ax_size[0]*rows_cols[1], ax_size[1]*rows_cols[0])
    axes = [fig.add_subplot(*rows_cols,idx+1) for idx in range(count)]
    return axes, fig

def set_best_time_scale(ax, seconds, label=''):
    if seconds>3600*24 *5: div,unit,steps = 3600*24, 'days', [8.64]
    elif seconds>3600 *5: div,unit,steps = 3600, 'hrs', [9]
    elif seconds>60 *5: div,unit,steps = 60, 'min', [3,6,9]
    elif seconds>1 *1: div,unit,steps = 1, 's', [1,2,3,4,5,10]
    else: div,unit,steps = 1e-3, 'ms', [1,2,4,5,10]

    fmt = plt.FuncFormatter(lambda x,pos:'%g'%(x/div))
    loc = plt.MaxNLocator('auto', steps=steps)
    # hack to get rid of MaxNLocator adding 10 to steps, which results in ugly hour ticks
    # https://stackoverflow.com/questions/62148592/use-matplotlib-ticker-locator-to-put-ticks-only-if-location-is-divisible-by-a-gi
    if unit=='hrs':
        loc._extended_steps = loc._staircase(np.array([0.9, 1.8, 2.7, 3.6, 5.4, 7.2, 9]))
    ax.xaxis.set_major_formatter(fmt)
    ax.xaxis.set_major_locator(loc)
    return f'{label} ({unit})'

# https://stackoverflow.com/questions/4194948/python-argparse-is-there-a-way-to-specify-a-range-in-nargs
class AxSizeAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        l_ = len(values)
        if not (l_==2 or l_==3):
            msg=f'argument {self.dest} accepts only 2 or 3 arguments'
            raise parser.error(msg)
        if l_==3: values = (values[0]*values[2], values[1]*values[2])
        setattr(args, self.dest, values)
