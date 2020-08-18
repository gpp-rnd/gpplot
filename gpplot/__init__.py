"""import gpplot imports both the plots and style modules"""
from .plots import ridgeplot, point_densityplot, add_correlation, pandas_barplot, density_rugplot, label_points, \
    dark_boxplot, add_reg_line, add_xy_line
from .style import discrete_palette, diverging_cmap, sequential_cmap, set_aesthetics, savefig

__author__ = """Peter C DeWeirdt"""
__email__ = 'petedeweirdt@gmail.com'
__version__ = '0.5.0'
