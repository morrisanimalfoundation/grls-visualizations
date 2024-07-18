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
    Reads the input CSV files for dog profiles, female reproductive history, and male reproductive history.

    This function reads three CSV files located in the directory specified by `dirpath`:
    1. "dog_profile.csv" - Contains dog profile information including birth, enrollment date, spayed/neutered date.

    Returns
    -------
    pd.DataFrame
        A tuple containing three pandas DataFrames:
        - df_profile: DataFrame containing the dog profile data.
    """
    behavior_summary = pd.read_csv(dirpath + "behavior_summary.csv")
    return behavior_summary
