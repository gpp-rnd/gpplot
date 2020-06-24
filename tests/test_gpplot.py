#!/usr/bin/env python

"""Tests for `gpplot` package."""

import pytest


import gpplot
import seaborn as sns
import pandas as pd
import numpy as np


@pytest.fixture
def scatter_data():
    np.random.seed(7)
    nsamps = 2000
    data = pd.DataFrame({'x': np.random.normal(size=nsamps)}, index=range(nsamps))
    data['y'] = 2 * data['x'] + np.random.normal(size=nsamps)
    return data


def test_ridgeplot():
    iris = sns.load_dataset('iris')
    g = gpplot.ridgeplot(iris, 'sepal_width', 'species')


def test_point_density_plot(scatter_data):
    ax = gpplot.point_densityplot(scatter_data, 'x', 'y')


def test_correlation(scatter_data):
    pearson = gpplot.calculate_correlation(scatter_data, 'x', 'y', 'pearson')
    assert pearson[1] < 0.01
    spearman = gpplot.calculate_correlation(scatter_data, 'x', 'y', 'spearman')
    assert spearman[1] < 0.01
    assert pearson[0] != spearman[0]


def test_add_correlation(scatter_data):
    ax = gpplot.point_densityplot(scatter_data, 'x', 'y')
    ax = gpplot.add_correlation(ax, scatter_data, 'x', 'y', size=12, color='blue')


def test_barplot():
    mpg = sns.load_dataset('mpg')
    mpg_summary = (mpg.groupby(['model_year', 'origin'])
                   .agg({'mpg': 'mean'})
                   .reset_index())
    ax = gpplot.pandas_barplot(mpg_summary, 'model_year', 'origin', 'mpg')


def test_desnity_rugplot():
    data = sns.load_dataset('iris')
    fig, ax = gpplot.density_rugplot(data, 'petal_length', 'species', ['setosa', 'virginica'])


def test_label_points():
    mpg = sns.load_dataset('mpg')
    ax = sns.scatterplot(data=mpg, x='weight', y='mpg')
    label = ['hi 1200d', 'ford f250', 'chevy c20', 'oldsmobile omega']
    gpplot.label_points(ax, mpg, 'weight', 'mpg', label, 'name')


def test_dark_boxplot():
    tips = sns.load_dataset("tips")
    ax = gpplot.dark_boxplot(data=tips, x="size", y="total_bill")
