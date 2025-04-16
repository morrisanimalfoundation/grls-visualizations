import matplotlib.pyplot as plt
import pandas as pd
import pytest

@pytest.mark.mpl_image_compare(baseline_dir='baseline', tolerance=10)
def test_sex_vis_image(sample_df):
    fig, ax = plt.subplots()
    sample_df['sex'].value_counts().plot(kind='bar', ax=ax)
    return fig


def test_plot_has_title():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3])
    ax.set_title("My Title")

    assert ax.get_title() == "My Title"

def test_sex_barplot_structure():
    df = pd.DataFrame({"sex": ["M", "F", "F", "M", "F"]})
    fig, ax = plt.subplots()
    df['sex'].value_counts().plot(kind='bar', ax=ax)

    bars = ax.patches
    labels = [bar.get_height() for bar in bars]

    assert labels == [3, 2]  # F has 3, M has 2
