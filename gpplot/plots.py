"""Main module."""

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap
import numpy as np
from scipy.interpolate import interpn
from scipy.stats import pearsonr, gaussian_kde

def label(x, color, label, text_xpos, text_ypos, text_ha, text_va):
    # For use with ridgeplot
    # Define and use a simple function to label the kde plots in axes coordinates
    ax = plt.gca()
    ax.text(text_xpos, text_ypos, label, color=color,
            ha=text_ha, va=text_va, transform=ax.transAxes)

def ridgeplot(df, x, hue, aspect=5, height=1, alpha=0.7, text_xpos=0, text_ypos=0.2, text_ha='left',
              text_va='center', lw=0.5, **kwargs):
    """
    Creates a ridgeplot of overlapping kde plots

    Parameters
    ----------
    df : DataFrame
    x : str
        Variables that define subsets of the data to plot on the FacetGrid. x defines the variable that
        will be plotted on the x-axis.
    hue : str
        Variables that define subsets of the data to plot on the FacetGrid. hue defines the variable that
        will be plotted on the rows.
    aspect : int, optional
        Defines aspect ratio of FacetGrid
    height : float, optional
        Defines height of each row in FacetGrid
    alpha : float, optional
        Defines opacity of kde plot
    text_xpos : float, optional
        Specify the horizontal position of text labels
    text_ypos : float, optional
        Specify the vertical position of text labels
    text_ha: str, optional
        Specify the horizontal alignment of text labels
    text_va : str, optional
        Specify the vertical alignment of text labels
    lw : float, optional
        Specifies the linewidth for kdeplot
    **kwargs
        Other keyword arguments are passed through to the FacetGrid

    Returns
    -------
    sns.FacetGrid
        seaborn FacetGrid with ridges

    Notes
    -----
    This code is slightly modified from https://seaborn.pydata.org/examples/kde_ridgeplot

    Examples
    --------
    >> iris = sns.load_dataset('iris')
    >> g = gpplot.ridgeplot(iris, 'sepal_width', 'species')
    """
    # Change background to be transparent and set style to white
    sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    # Initialize a facetgrid
    g = sns.FacetGrid(df, row=hue, hue=hue, aspect=aspect, height=height, **kwargs)
    # Draw the densities in a few steps
    g.map(sns.kdeplot, x, clip_on=False, shade=True, alpha=alpha, lw=lw)
    # Label axes with the values from hue
    g.map(label, x, text_xpos=text_xpos, text_ypos=text_ypos, text_ha=text_ha, text_va=text_va)
    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-0.25)
    # Remove axes details that don't play well with overlap
    g.set_titles('')
    g.set(yticks=[])
    g.despine(bottom=True, left=True)
    return g

def point_density_plot(data, x, y, bins=None, alpha=0.6, edgecolor='',
                         marker='o', rasterized=True,
                         palette='viridis', legend=False, **kwargs):
    """Scatter plot with points colored by density

    Rasterized scatterplot for easy illustrator import

    Parameters
    ----------
        data: DataFrame
            DataFrame with columns x and y
        x: str
            Variable to plot on the x axis
        y: str
            Variable to plot on the y axis
        bins: list of ints, optional
            Binsize for density estimate. Defaults to [20, 20]
        alpha: float, optional
            Opacity of points
        edgecolor: str, optional
            Point edge color
        marker: str, optional
            Point shape
        ratsterized: bool, optional
            Whether to rasterize scatterplot
        palette: str, optional
            Color map
        legend: bool, optional
            Whether to include legend for density
        **kwargs
            Additional aruments passed to scatterplot function

    Returns
    -------
        axis object
    """
    # copy dataframe since we'll be manipulating it before plotting
    df = data.copy()
    x_val = df[x]
    y_val = df[y]
    if bins is None:
        bins = [20, 20]
    hist_data, x_e, y_e = np.histogram2d(x_val, y_val, bins=bins, density=True)
    z = interpn((0.5 * (x_e[1:] + x_e[:-1]), 0.5 * (y_e[1:] + y_e[:-1])),
                hist_data, np.vstack([x_val, y_val]).T,
                method="splinef2d", bounds_error=False)
    # Be sure to plot all data
    z[np.where(np.isnan(z))] = 0.0
    df['color'] = z
    df = df.sort_values('color', ascending=True)
    ax = sns.scatterplot(x=x, y=y, data=df, hue='color',
                         alpha=alpha, edgecolor=edgecolor,
                         marker=marker, rasterized=rasterized,
                         palette=palette, legend=legend, **kwargs)
    return ax
