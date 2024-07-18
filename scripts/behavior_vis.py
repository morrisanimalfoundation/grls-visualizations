import warnings

import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import seaborn as sns

from settings import dirpath, embargo_year, vizpath


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


def behavior_categories(behavior_summary: pd.DataFrame) -> None:
    likert_colors = ['white', 'firebrick', 'lightcoral', 'gainsboro', 'cornflowerblue', 'darkblue']
    dummy = pd.DataFrame([[1, 2, 3, 4, 5], [5, 6, 7, 8, 5], [10, 4, 2, 10, 5]],
                         columns=["SD", "D", "N", "A", "SA"],
                         index=["Key 1", "Key B", "Key III"])
    middles = dummy[["SD", "D"]].sum(axis=1) + dummy["N"] * .5
    longest = middles.max()
    complete_longest = dummy.sum(axis=1).max()
    dummy.insert(0, '', (middles - longest).abs())

    dummy.plot.barh(stacked=True, color=likert_colors, edgecolor='none', legend=False)
    z = plt.axvline(longest, linestyle='--', color='black', alpha=.5)
    z.set_zorder(-1)

    plt.xlim(0, complete_longest)
    xvalues = range(0, complete_longest, 10)
    xlabels = [str(x - longest) for x in xvalues]
    plt.xticks(xvalues, xlabels)
    plt.show()