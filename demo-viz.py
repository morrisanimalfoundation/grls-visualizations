"""
This Python file contains code to generate the 2 visualisations on the page
https://datacommons.morrisanimalfoundation.org/demographic-data
titled:
1. Age Distribution as of <Month> <year>
2. Sex Status, Baseline vs Year <number>
as well as the data to generate the graphics titled:
1. Geographic Distribution of Enrolled Dogs
2. Urban v/s Suburban v/s Rural

The datasets that power the visualisations and graphics on this page are:
1. dog_profile.csv
2. reproductive_history_female.csv
3. reproductive_history_female.csv

Author: Neha Bhomia
Created Date: September 19th, 2023
"""

from py_secrets import dirpath, vizpath, fontpath
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as font_manager

# reading in our datasets and force setting data types
# note: parsing dates adds 01 as default day in date values if date is missing (df_profile raw data date format yyyy-mm)
df_profile = pd.read_csv(dirpath + "dog_profile.csv", dtype={'subject_id': 'object', 'sex_status': 'category'},
                         parse_dates=['birth_date', 'enrolled_date'])

df_fem = pd.read_csv(dirpath + "reproductive_history_female.csv", usecols=['subject_id', 'spayed_on_date'],
                     parse_dates=['spayed_on_date'])

df_male = pd.read_csv(dirpath + "reproductive_history_male.csv", usecols=['subject_id', 'neutered_on_date'],
                      parse_dates=['neutered_on_date'])

df_tuple = (df_profile, df_fem, df_male)


def age_vis(dataframe):
    """
    Creates the age distribution visualisation - a bar graph - with age buckets (in years) on the x-axis and
    dog counts on the y-axis.
    :param dataframe: the dataset used to generate this visualisation
    :return: seaborn figure
    """
    # calculating age
    today = date.today()
    born = dataframe['birth_date'].dt
    dataframe['current_age'] = today.year - born.year - (today.month < born.month)

    # Calculate the count of dogs at each age
    age_counts = dataframe['current_age'].value_counts().sort_index()

    # Create a bar chart using Seaborn
    sns.set_style('whitegrid', {'grid.color': '#ECECEC'})  # HEX code for the grey colour of the grid lines
    plt.figure(figsize=(8, 6))  # Adjust the figure size as needed
    sns.barplot(x=age_counts.index, y=age_counts.values, color='#FF5F1F', width=0.7)  # Adjust bar colour using HEX code
    plt.yticks(range(0, int(age_counts.max() + 100), 400))  # Y-axis ticks in increments of 400
    sns.despine(left=True, bottom=True)  # Remove borders

    # Set font properties for title and axis labels
    prop = font_manager.FontProperties(fname=fontpath+'Buntype - BundaySans-Bold.otf')
    plt.xlabel('AGE (YEARS)', fontproperties=prop, fontsize=14, labelpad=12)
    plt.xticks(fontproperties=prop, fontsize=12)
    plt.ylabel('DOGS (COUNT)', fontproperties=prop, fontsize=14, labelpad=12)
    plt.yticks(fontproperties=prop, fontsize=12)

    # save the plot as PNG file
    plt.savefig(vizpath+"age_count.png")

    # # displaying the plot
    # plt.show()

    return plt.figure()


def sex_vis(dataframe_list):
    """
    Creates the Sex Status visualisation - a stacked bar plot - with sex status of dogs on the X-axis and
    the percentage of the dogs on the Y-axis.
    :param dataframe_list: a tuple of the datasets used to create this visualisation with 3 items (in this order):
    1. profile dataset for baseline data
    2. female dataset and
    3. male dataset
    :return: plot figure
    """

    return plt.figure()


if __name__ == "__main__":
    age_vis(df_profile)
    sex_vis(df_tuple)
