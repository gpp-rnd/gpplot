#!/usr/bin/env python

"""Tests for `gpplot` package."""

import pytest


import gpplot
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

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
