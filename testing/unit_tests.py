import matplotlib.pyplot as plt
import pandas as pd
import time
import os
from matplotlib import font_manager
import settings


def test_font_file_exists_and_loads(font_name: object):
    # We can convert the fonts used into a list later
    font_path = settings.fontpath + font_name
    assert os.path.isfile(font_path), f"Missing font file from the folder: {font_name}."
    prop = font_manager.FontProperties(fname=font_path)
    assert prop.get_name(), f"Font {font_name} failed to load or returned an empty name."


def test_labels_are_not_empty(ax):
    # Check if x-axis label is empty
    xlabel = ax.get_xlabel()
    if not xlabel.strip():
        print("x-axis label is missing or empty")

    # Check if y-axis label is empty
    ylabel = ax.get_ylabel()
    if not ylabel.strip():
        print("y-axis label is missing or empty")

    # Check if title is empty
    title = ax.get_title()
    if not title.strip():
        print("Title is missing or empty")

    # Assert that none of the labels or title are empty
    assert xlabel.strip() != "", "x-axis label is empty"
    assert ylabel.strip() != "", "y-axis label is empty"
    assert title.strip() != "", "Title is empty"


def test_barplot_structure(df, column_name, ax=None):
    """
    Test the structure of a barplot generated from a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data to be plotted.
    column_name : str
        The column name in the DataFrame for which to create the barplot.
    ax : matplotlib.axes.Axes, optional
        The axes object to plot on. If None, a new figure and axes will be created.
    """
    # Create a new figure and axes if none are provided
    if ax is None:
        fig, ax = plt.subplots()

    # Plot the bar chart
    df[column_name].value_counts().plot(kind='bar', ax=ax)

    # Get the bars and their heights
    bars = ax.patches
    bar_heights = [bar.get_height() for bar in bars]

    # Get the expected values based on the column data
    expected_values = df[column_name].value_counts().sort_values(ascending=False).values.tolist()

    # Assert the bar heights match the expected values
    assert bar_heights == expected_values, f"Expected bar heights {expected_values}, but got {bar_heights}"

    # Optionally, check the order of bars if necessary (e.g., descending order)
    bar_labels = [bar.get_height() for bar in bars]
    sorted_labels = sorted(bar_labels, reverse=True)
    assert bar_labels == sorted_labels, f"Bar labels are not sorted in descending order: {bar_labels}"


def test_chart_renders_under_500ms(generate_chart):
    start = time.time()
    chart = generate_chart()
    end = time.time()
    assert (end - start) < 0.5, "Chart rendering is too slow"


def test_memory_footprint_under_limit(generate_plot_function):
    import tracemalloc
    tracemalloc.start()
    # Call your visualization or data prep code here
    generate_plot_function()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert peak < 50_000_000, "Memory usage exceeded 50MB"
