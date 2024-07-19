import warnings

import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import seaborn as sns

from settings import dirpath, embargo_year, vizpath

# Category names
category_names_normal = ['Never', 'Seldom', 'Sometimes', 'Usually', 'Always', 'N/A']
category_names_reversed = ['Always', 'Usually', 'Sometimes', 'Seldom', 'Never', 'N/A']
# Topics with reversed counting
reversed_topics = ['Stranger-directed fear', 'Nonsocial fear', 'Dog-directed fear', 'Touch sensitivity']
# Calculate cumulative sums
count_columns = ['count_0', 'count_1', 'count_2', 'count_3', 'count_4', 'count_na']


def read_inputs() -> pd.DataFrame:
    """
    Reads the input CSV files for behavior_summary.
    Returns
    -------
    pd.DataFrame
        behavior_summary: DataFrame containing the dog behavior_summary data.
    """
    behavior_summary = pd.read_csv(dirpath + "behavior_summary.csv")
    return behavior_summary


def behavior_categories(behavior_summary: pd.DataFrame) -> dict:
    # The to_date gets the sum of every dog for each study year
    behavior_summary = behavior_summary[behavior_summary['to_date'] == 1]
    # Get the index of the max year_in_study for each subject_id
    idx = behavior_summary.groupby('subject_id')['year_in_study'].idxmax()
    # Filter the DataFrame to keep only the rows with the max year_in_study for each subject_id
    behavior_summary = behavior_summary.loc[idx].reset_index(drop=True)
    # Prepare the results dictionary for each topic
    results = {}
    for topic, group in behavior_summary.groupby('topic'):
        if topic in reversed_topics:
            # Reverse the counts for specified topics
            reversed_counts = group[count_columns].apply(lambda x: x[::-1].values, axis=1)
            results[topic] = reversed_counts.avg().tolist()
        else:
            results[topic] = group[count_columns].avg().tolist()
    return results


def survey(results, category_names, topic):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    topic : str
        The topic for the current survey.
    """
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.cm.RdYlGn(np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    ax.set_title(f'Survey Results for Topic: {topic}')
    return fig, ax


df = read_inputs()

results = behavior_categories(df)

# Plotting the results
for topic in results:
    if topic in reversed_topics:
        survey({topic: results[topic]}, category_names_reversed, topic)
    else:
        survey({topic: results[topic]}, category_names_normal, topic)
    plt.savefig(vizpath + f'/survey_results_{topic}.png')
    plt.show()
