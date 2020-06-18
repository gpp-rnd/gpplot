"""style module. Contains functions to standardize styles for matplotlib-based plots"""

import seaborn as sns
import matplotlib as mpl

def discrete_palette(palette='Set2', n=8):
    """ Default discrete palette"""
    return sns.color_palette(palette, n)


def diverging_cmap(cmap='RdBu_r'):
    return cmap


def sequential_cmap(cmap='viridis'):
    return cmap


def set_aesthetics(style='ticks', context='notebook', font='Arial',
                   font_scale=1, palette=discrete_palette(), rc=None):
    """Set aesthetics for plotting, using seaborn.set_style and matplotlib.rcParams

    Parameters
    ----------
    style: str, optional
        One of darkgrid, whitegrid, dark, white, ticks
    context: str, optional
        One of paper, notebook, talk, poster
    font: str, optional
        Font family
    font_scale: int, optional
        Scaling factor to scale the size of font elements
    palette: str or seaborn.color_palette, optional
        Discrete color palette to use in plots
    rc: dict, optional
        Mappings to pass to matplotlib.rcParams
    """
    sns.set(style=style, context=context, font=font,
            palette=palette,
            font_scale=font_scale)
    mpl.rc('pdf', fonttype=42)
    if rc is not None:
        for key, value in rc:
            mpl.rcParams[key] = value


def savefig(fig, path, bbox_inches='tight', transparent=True, **kwargs):
    """Wrapper function to save figures

    Parameters
    ----------
    fig: matplotlib.figure.Figure
        Figure to be saved
    path: str
        Location to save figure
    bbox_inches: str, optional
        Bounding box of figure
    transparent: bool, optional
        Whether to include a background to the plot
    **kwargs
        Other keyword arguments are passed through to matplotlib.pyplot.savefig
    """
    fig.savefig(path, bbox_inches=bbox_inches, transparent=transparent, **kwargs)
