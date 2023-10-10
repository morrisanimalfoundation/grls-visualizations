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
3. reproductive_history_male.csv

Author: Neha Bhomia
Created Date: September 19th, 2023
"""

from py_secrets import dirpath, vizpath, fontpath
import pandas as pd
from datetime import date, datetime
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as font_manager
import matplotlib.ticker as mtick

# suppressing warnings for category datatype
# TODO: Investigate this further to prevent technical debt
import warnings
warnings.filterwarnings("ignore", "is_categorical_dtype")
warnings.filterwarnings("ignore", "use_inf_as_na")

# reading in our datasets and force setting data types
# note: parsing dates adds 01 as default day in date values if date is missing (df_profile raw data date format yyyy-mm)
df_profile = pd.read_csv(dirpath + "dog_profile.csv", dtype={'subject_id': 'object', 'sex_status': 'category'},
                         parse_dates=['birth_date', 'enrolled_date'])

# earliest year of enrolment record to calculate our baseline year of study
min_year = df_profile['enrolled_date'].min().year

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


def sex_vis(dataframes):
    """
    Creates the Sex Status visualisation - a stacked bar plot - with sex status of dogs on the X-axis and
    the percentage of the dogs on the Y-axis.
    :param dataframes: a tuple of the datasets used to create this visualisation with 3 items (in this order):
    1. profile dataset for baseline data
    2. female dataset and
    3. male dataset
    :return: plot figure
    """
    df_base = dataframes[0][['subject_id', 'sex_status']]
    df_f = dataframes[1]
    df_m = dataframes[2]
    # Changing sex_status labels to uppercase
    df_base.loc[:, 'sex_status'] = df_base['sex_status'].apply(lambda x: x.upper())

    # TODO: create unit test that asserts unique id's in dog profile = sum of unique id's in fem and male repro hist
    # TODO: create ut for assertion that after dropping duplicates there's only one date per subject id

    # there are multiple data points for some subject_ids (different years in study)
    def keep_latest(dataframe, date_col):
        """
        this function sorts the dataframe by date for each id and then
        takes the very last date recorded in spayed_on_date/neutered_on_date for each ID
        this eliminates duplicate data points for
        :param dataframe: the dataframe which needs to be sorted and duplicates dropped
        :param date_col: the name of the date column as string
        :return: cleaned dataframe with only unique id's in rows and latest date
        """
        # Make sure date column is of datetime datatype
        dataframe[date_col] = dataframe[date_col].astype('datetime64[ns]')

        # Sort the DataFrame by 'id' and date in descending order
        dataframe.sort_values(by=['subject_id', date_col], ascending=[True, False], inplace=True)

        # Keep the latest date for each 'id'
        dataframe.drop_duplicates(subset='subject_id', keep='first', inplace=True)

        return dataframe

    df_f = keep_latest(df_f, 'spayed_on_date')
    df_m = keep_latest(df_m, 'neutered_on_date')

    # Merge df_f and df_m to calculate recent counts
    df_recent = pd.merge(df_f, df_m, on='subject_id', how='outer')

    # Adding a recent status column with default value Baseline
    df_recent['recent_status'] = 'Baseline'

    # Fill NaN values in spayed_date and neutered_date with a dummy date to represent no change
    dummy_date = datetime.strptime('1900-01-01', '%Y-%m-%d')
    df_recent['spayed_on_date'].fillna(dummy_date, inplace=True)
    df_recent['neutered_on_date'].fillna(dummy_date, inplace=True)

    # Update recent_status based on changes
    df_recent.loc[df_recent['spayed_on_date'] != dummy_date, 'recent_status'] = 'SPAYED FEMALE'
    df_recent.loc[df_recent['neutered_on_date'] != dummy_date, 'recent_status'] = 'NEUTERED MALE'

    # Combine the dataframes to get a single dataframe for plotting
    combined_df = pd.merge(df_base, df_recent)

    # Function to replace 'Baseline' in column A with values from column B
    def replace_baseline(row):
        if row['recent_status'] == 'Baseline':
            return row['sex_status']
        else:
            return row['recent_status']

    # Apply the function to each row in the DataFrame
    combined_df['recent_status'] = combined_df.apply(replace_baseline, axis=1)

    # Calculate the percentage of dogs for each category
    percentage_baseline = df_base['sex_status'].value_counts(normalize=True).reset_index()
    percentage_baseline.columns = ['sex_status', 'percent']
    percentage_recent = combined_df['recent_status'].value_counts(normalize=True).reset_index()
    percentage_recent.columns = ['sex_status', 'percent']

    # Calculating the latest year of spayed/neutered on dates in the repro_history datasets
    # for calculating our current study year for our visualisation title
    max_year = combined_df[['spayed_on_date', 'neutered_on_date']].max().max().year
    study_year = 'YEAR ' + str(max_year - min_year)

    total_percent = pd.concat([percentage_baseline, percentage_recent], axis=0, keys=['BASELINE', study_year]).reset_index(level=0)
    total_percent['percent'] = total_percent['percent'].apply(lambda x: x*100)

    # Creating the Grouped Seaborn Bar Plot
    sns.set_style('whitegrid', {'grid.color': '#ECECEC'})  # HEX code for the grey colour of the grid lines
    plt.figure(figsize=(8, 6))  # Adjust the figure size as needed
    ax = sns.barplot(x='sex_status', y='percent', hue='level_0', data=total_percent, width=0.7, palette=['#0288D1', '#FF5F1F'], linewidth=4)
    plt.yticks(range(0, int(total_percent.percent.max() + 10), 10))  # Y-axis ticks in increments of 10
    sns.despine(left=True, bottom=True)  # Remove borders

    # Set font properties for title and axis labels
    prop = font_manager.FontProperties(fname=fontpath + 'Buntype - BundaySans-Bold.otf')
    plt.xlabel('', fontproperties=prop, fontsize=14, labelpad=12)
    plt.xticks(fontproperties=prop, fontsize=12)
    plt.ylabel('PERCENTAGE OF DOGS', fontproperties=prop, fontsize=14, labelpad=12)
    plt.yticks(fontproperties=prop, fontsize=12)

    # Define the formatting function to add '%' to y-axis tick labels
    def add_percent(x, pos):
        return f"{x:.0f}%"

    # Apply the formatting function to the y-axis
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(add_percent))
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False, prop=prop, fontsize=14, handleheight=2.5, borderaxespad=-0.25)

    # save the plot as PNG file
    plt.savefig(vizpath + "sex_stat.png")

    # displaying the plot
    plt.show()

    return plt.figure()


if __name__ == "__main__":
    age_vis(df_profile)
    sex_vis(df_tuple)