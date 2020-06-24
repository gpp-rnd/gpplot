"""Plots module - contains functions to generate plots."""

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interpn
from scipy import stats
from matplotlib.offsetbox import AnchoredText
from matplotlib import ticker
from adjustText import adjust_text


def label_axes(x, color, label, text_xpos, text_ypos, text_ha, text_va):
    """For use with ridgeplot, define and use a simple function
    to label the kde plots in axes coordinates"""
    ax = plt.gca()
    ax.text(text_xpos, text_ypos, label, color=color,
            ha=text_ha, va=text_va, transform=ax.transAxes)


def ridgeplot(data, x, hue, aspect=5, height=1, alpha=0.7, text_xpos=0, text_ypos=0.2, text_ha='left',
              text_va='center', lw=0.5, **kwargs):
    """
    Creates a ridgeplot of overlapping kde plots

    Parameters
    ----------
    data : DataFrame
        Dataframe with columns x and hue
    x : str
        Defines the variable that will be plotted on the x-axis
    hue : str
        Hue defines the variable that will be plotted for the rows
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
        Other keyword arguments are passed through to sns.FacetGrid

    Returns
    -------
    sns.FacetGrid
        seaborn FacetGrid with ridges

    Notes
    -----
    This code is slightly modified from https://seaborn.pydata.org/examples/kde_ridgeplot

    Examples
    --------
    >>> iris = sns.load_dataset('iris')
    >>> g = gpplot.ridgeplot(iris, 'sepal_width', 'species')
    """
    # Change background to be transparent and set style to white
    sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    # Initialize a facetgrid
    g = sns.FacetGrid(data, row=hue, hue=hue, aspect=aspect, height=height, **kwargs)
    # Draw the densities in a few steps
    g.map(sns.kdeplot, x, clip_on=False, shade=True, alpha=alpha, lw=lw)
    # Label axes with the values from hue
    g.map(label_axes, x, text_xpos=text_xpos, text_ypos=text_ypos, text_ha=text_ha, text_va=text_va)
    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-0.25)
    # Remove axes details that don't play well with overlap
    g.set_titles('')
    g.set(yticks=[])
    g.despine(bottom=True, left=True)
    return g


def point_densityplot(data, x, y, bins=None, alpha=0.6, edgecolor='',
                      marker='o', rasterized=True,
                      palette='viridis', legend=False, **kwargs):
    """Scatter plot with points colored by density

    Rasterized for easy illustrator import

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
    rasterized: bool, optional
        Whether to rasterize scatterplot
    palette: str, optional
        Color map
    legend: bool, optional
        Whether to include legend for density
    **kwargs
        Additional aruments passed to scatterplot function

    Returns
    -------
    matplotlib.axes.Axes
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


def calculate_correlation(data, x, y, type):
    """
    Parameters
    ----------
    data: DataFrame
        DataFrame with columns x and y
    x: str
        x variable to correlate
    y: str
        y variable to correlate
    type: str
        pearson or spearman

    Returns
    -------
     tuple:
        (correlation between x and y, significance)
    """
    if type == 'spearman':
        cor = stats.spearmanr(data[x], data[y])
    elif type == 'pearson':
        cor = stats.pearsonr(data[x], data[y])
    else:
        raise ValueError("type must be 'pearson' or 'spearman'")
    return cor


def add_correlation(ax, data, x, y, method='pearson', signif=2, loc='upper left',
                    fontfamily='Arial', **kwargs):
    """Add correlation to a scatterplot

    Parameters
    ----------
    ax: Axis object
        Plot to add correlation to
    data: DataFrame
        DataFrame with columns x and y, same data used to create the plot
    x: str
        x variable to correlate
    y: str
        y variable to correlate
    method: str, optional
        pearson or spearman
    signif: int, optional
        number of significant figures
    loc: string, optional
        location of label, passed to matplotlib.offsetbox.AnchoredText
    size: int, optional
        text size
    fontfamily: str, optional
        text font family
    **kwargs
        Other key word arguments passed to text object

    Returns
    -------
    matplotlib.axes.Axes
    """
    r = calculate_correlation(data, x, y, method)
    label = 'r = ' + str(round(r[0], signif))
    text = AnchoredText(label, loc=loc, frameon=False,
                        prop=dict(fontfamily=fontfamily,
                                  **kwargs))
    ax.add_artist(text)
    return ax


def pandas_barplot(data, x, hue, y, x_order=None, hue_order=None,
                   horizontal=True, stacked=True, **kwargs):
    """Create a barplot using pandas plot functionality

    Mainly allows for stacked barplots

    Parameters
    ----------
    data : DataFrame
        DataFrame with columns x and y
    x : str
        x defines the discrete variable that will be plotted on the x-axis.
    hue : str
        hue defines the variable that will separate variables with the same x value.
    y: str
        y is the continuous variable defining the height of each bar
    x_order: list, optional
        order of x axis
    hue_order: list, optional
        order of colors
    horizontal: bool, optional
        whether to lay the bar plot out horizontally
    stacked: bool, optional
        whether to stack barplots
    **kwargs
        passed on to Pandas' plot function or matplotlib's bar function

    Returns
    -------
    matplotlib.axes.Axes
    """
    spread_data = data.pivot(index=x, columns=hue, values=y)
    if x_order is not None:
        spread_data = spread_data.reindex(index=x_order)
    if hue_order is not None:
        spread_data = spread_data[hue_order]
    if horizontal:
        ax = spread_data.plot.barh(stacked=stacked, **kwargs)
    else:  # vertical
        ax = spread_data.plot.bar(stacked=stacked, **kwargs)
    return ax


def density_rugplot(data, x, y, y_values, density_height=2, rug_height=1,
                    density_color='black', rug_color='black', rug_alpha=0.5,
                    figsize=plt.rcParams['figure.figsize'], ref_line=None,
                    ref_line_color='black', **kwargs):
    """Creates a density rugplot

    first subplot is a distribution of values and subsequent subplots are
    rugplots of values for some discrete number of variables

    Parameters
    ----------
    data: DataFrame
        DataFrame with columns x and y
    x: str
        Column in data of continuous values
    y: str
        Column in data of discrete values
    y_values: list
        List of y values to include as subplots
    density_height: int, optional
        Relative height of density plot
    rug_height: int, optional
        Relative height of rug plot
    density_color: str, optional
        Color of density plot
    rug_color: str, optional
        Color of rug plot
    rug_alpha: float, optional
        Opacity of rug plot
    figsize: tuple, optional
        Size of entire figure
    ref_line: int, optional
        x value of reference line to include for all plots
    ref_line_color: str, optional
        Color of reference line
    **kwargs
        Other keyword arguments are passed through to sns.rugplot

    Returns
    -------
    matplotlib.figure.Figure
        figure
    numpy.ndarray of matplotlib.axes.Axes
        individual subplots
    """
    height_ratios = [density_height] + ([rug_height] * len(y_values))
    fig, ax = plt.subplots((len(y_values) + 1), 1,
                           gridspec_kw={'height_ratios': height_ratios}, sharex=True,
                           figsize=figsize)
    # KDE plot of all x
    sns.kdeplot(data=data[x], color=density_color, legend=False, ax=ax[0])
    lims = (data[x].min(), data[x].max())
    ax[0].set_xlim(lims)
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    ax[0].set_ylabel('All', rotation='horizontal', ha='right', va='center')
    if ref_line is not None:
        ax[0].axvline(x=ref_line, color=ref_line_color, linestyle='--')
    # Rugplots for each y value
    for i, value in enumerate(y_values):
        sns.rugplot(a=data.loc[data[y] == value, x], height=1, ax=ax[i + 1],
                    color=rug_color, alpha=rug_alpha, **kwargs)
        ax[i + 1].set_ylabel(value, rotation='horizontal', ha='right', va='center')
        ax[i + 1].set_yticks([])
        ax[i + 1].get_xaxis().set_major_locator(ticker.AutoLocator())
        if ref_line is not None:
            ax[i+1].axvline(x=ref_line, color=ref_line_color, linestyle='--')
    plt.xlabel(x)
    return fig, ax


def label_points(ax, data, x, y, label, label_col, arrowstyle='-', arrow_color='black',
                 arrow_lw=1, **kwargs):
    """Label points in a scatterplot

    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Plot to label
    data: DataFrame
        Data to create labels
    x: str
        x position of labels
    y: str
        y position of labels
    label: list
        DataFrame elements to label
    label_col: str
        Column to match 'label' points
    arrowstyle: str, optional
        Style of arrow
    arrow_color: str, optional
        Color of arrow
    arrow_lw: float, optional
        Line weight of arrow
    **kwargs
        Other keyword arguments are passed through to matplotlib.plt.text

    Returns
    -------
    matplotlib.axes.Axes
    """
    labelled_data = data[data[label_col].isin(label)]
    texts = []
    for i, row in labelled_data.iterrows():
        texts.append(ax.text(row[x], row[y], row[label_col], **kwargs))
    # ensures text labels are non-overlapping
    adjust_text(texts, arrowprops=dict(arrowstyle=arrowstyle, color=arrow_color,
                                       lw=arrow_lw))
    return ax


def dark_boxplot(data, x, y, boxprops=None, medianprops=None,
                 whiskerprops=None, capprops=None, flierprops=None, **kwargs):
    """Wrapper for seaborn.boxplot, which defaults to black lines for boxplot elements

    Parameters
    ----------
    data: DataFrame
        Data to create boxplot
    x: str
        x value of boxplot
    y: str
        y value of boxplot
    boxprops: dict, optional
        Style of box, passed to matplotlib.pyplot.boxplot
    medianprops: dict, optional
        Style of median line, passed to matplotlib.pyplot.boxplot
    whiskerprops: dict, optional
        Style of whiskers, passed to matplotlib.pyplot.boxplot
    capprops: dict, optional
        Sytle of cap on top of whiskers, passed to matplotlib.pyplot.boxplot
    flierprops: dict, optional
         Style of outlier points, passed to matplotlib.pyplot.boxplot
    **kwargs
        Other keyword arguments are passed through to seaborn.boxplot

    Returns
    -------
    matplotlib.axes.Axes
    """
    if boxprops is None:
        boxprops = {'edgecolor': 'black'}
    if medianprops is None:
        medianprops = {'color': 'black'}
    if whiskerprops is None:
        whiskerprops = {'color': 'black'}
    if capprops is None:
        capprops = {'color': 'black'}
    if flierprops is None:
        flierprops = {'marker': 'o', 'markerfacecolor': 'black'}
    ax = sns.boxplot(data=data, x=x, y=y,
                     boxprops=boxprops, medianprops=medianprops,
                     whiskerprops=whiskerprops, capprops=capprops,
                     flierprops=flierprops, **kwargs)
    return ax
