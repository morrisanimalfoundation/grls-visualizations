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
"""

from py_secrets import dirpath, vizpath, fontpath
import pandas as pd
from datetime import date, datetime
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as font_manager
import matplotlib.ticker as mtick

# Suppressing warnings for category datatype
# TODO: Investigate this further to prevent technical debt
import warnings
warnings.filterwarnings("ignore", "is_categorical_dtype")
warnings.filterwarnings("ignore", "use_inf_as_na")

# Earliest year of enrolment record to calculate our baseline year of study
#min_year = df_profile['enrolled_date'].min().year

# earliest year of enrolment record to calculate our baseline year of study
#min_year = df_profile['enrolled_date'].min().study_year


def read_inputs() -> pd.DataFrame:
    """
    Reads the input CSV files for dog profiles, female reproductive history, and male reproductive history.

    This function reads three CSV files located in the directory specified by `dirpath`:
    1. "dog_profile.csv" - Contains dog profile information including birth, enrollment date, spayed/neutered date.

    Returns
    -------
    tuple
        A tuple containing three pandas DataFrames:
        - df_profile: DataFrame containing the dog profile data.
    """
    # Check for missing dates
    # df_profile.birth_date.value_counts()
    # df_profile.enrolled_date.value_counts()
    df_profile = pd.read_csv(dirpath + "dog_profile.csv")
    return df_profile


def grls_dogs_age_distrbution_vis(dataframe) -> None:
    """
    Creates the age distribution visualization - a bar graph - with age buckets (in years) on the x-axis and
    dog counts on the y-axis.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The dog_profile dataset.

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
    plt.xlabel('AGE')
    plt.ylabel('DOGS')
    plt.title('AGE DISTRIBUTIONS AS OF JULY, 2024')

    # Save the plot as PNG file
    plt.savefig(vizpath+"age_count.png")

    # Uncomment to display the plot
    # plt.show()


def sex_vis(df_base: pd.DataFrame):
    """
    Creates the Sex Status visualisation - a stacked bar plot - with sex status of dogs on the X-axis and
    the percentage of the dogs on the Y-axis.
    :param dataframes: a tuple of the datasets used to create this visualisation with 3 items (in this order):
    1. profile dataset for baseline data

    :return: plot figure
    """
    # Changing sex_status labels to uppercase
    df_base.loc[:, 'sex_status'] = df_base['sex_status'].apply(lambda x: x.upper())

    # Convert date columns to datetime
    df_base['enrolled_date'] = pd.to_datetime(df_base['enrolled_date'])
    df_base['spay_neuter_date'] = pd.to_datetime(df_base['spay_neuter_date'])

    # Calculate the difference in years
    df_base['spay_neuter_year'] = (df_base['spay_neuter_date'] - df_base['enrolled_date']).dt.days / 365.25

    # Ignore rows where spay_neuter_date is NaT by setting spay_neuter_year to NaN
    df_base['spay_neuter_year'] = df_base['spay_neuter_year'].where(df_base['spay_neuter_date'].notna())

    # Create the new_sex_status column
    df_base['new_sex_status'] = df_base.apply(
        lambda row: 'Female Spayed' if pd.notna(row['spay_neuter_date']) and row['sex_status'] == 'Female Intact'
        else ('Male Neutered' if pd.notna(row['spay_neuter_date']) and row['sex_status'] == 'Male Intact'
              else row['sex_status']),
        axis=1
    )

    # Create final_status column using new_sex_status if available, otherwise sex_status
    df_base['final_status'] = df_base['new_sex_status'].fillna(df_base['sex_status'])

    # Calculate percentages for sex_status
    percentage_sex_status = df_base['final_status'].value_counts(normalize=True).reset_index()
    percentage_sex_status.columns = ['status', 'percent']

    # Filter for spay_neuter_year between 0-3
    df_filtered_year3 = df_base[df_base['spay_neuter_year'].between(0, 3, inclusive='right')]

    # Calculate percentages for new_sex_status within the filtered data
    percentage_year_3_sex_status = df_filtered_year3['final_status'].value_counts(normalize=True).reset_index()
    percentage_year_3_sex_status.columns = ['status', 'percent']

    # Filter for spay_neuter_year between 0-3
    df_filtered_year5 = df_base[df_base['spay_neuter_year'].between(3, 5, inclusive='right')]

    # Calculate percentages for new_sex_status within the filtered data
    percentage_year_5_sex_status = df_filtered_year5['final_status'].value_counts(normalize=True).reset_index()
    percentage_year_5_sex_status.columns = ['status', 'percent']


    # Combine the DataFrames for plotting
    percentage_sex_status['Study Year'] = 'Baseline'
    percentage_year_3_sex_status['Study Year'] = 'Year 3'
    percentage_year_5_sex_status['Study Year'] = 'Year 5'

    combined_df = pd.concat([percentage_sex_status, percentage_year_3_sex_status, percentage_year_5_sex_status])

    # Multiply percent by 100 to get percentage
    combined_df['percent'] = combined_df['percent'] * 100

    # Plotting
    sns.set_style('whitegrid', {'grid.color': '#ECECEC'})  # HEX code for the grey colour of the grid lines
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    ax = sns.barplot(x='status', y='percent', hue='Study Year', data=combined_df, palette=['#0288D1', '#FF5F1F', '#d0db01'],
                     linewidth=2)
    plt.yticks(range(0, int(combined_df['percent'].max() + 10), 10))  # Y-axis ticks in increments of 10
    sns.despine(left=True, bottom=True)  # Remove borders

    # Set font properties for title and axis labels
    #prop = font_manager.FontProperties(fname='/path/to/font/Buntype - BundaySans-Bold.otf')
    #plt.xlabel('', fontproperties=prop, fontsize=14, labelpad=12)
    #plt.xticks(fontproperties=prop, fontsize=12)
    #plt.ylabel('PERCENTAGE OF DOGS', fontproperties=prop, fontsize=14, labelpad=12)
    #plt.yticks(fontproperties=prop, fontsize=12)

    # Define the formatting function to add '%' to y-axis tick labels
    def add_percent(x, pos):
        return f"{x:.0f}%"

    # Apply the formatting function to the y-axis
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(add_percent))
    #plt.legend(loc='upper right', title='Category', frameon=False, prop=prop, fontsize=12)

    # Save the plot as PNG file
    plt.savefig("sex_status_vs_new_sex_status.png")

    # Display the plot
    plt.show()

    # Set font properties for title and axis labels
    #prop = font_manager.FontProperties(fname=fontpath + 'Buntype - BundaySans-Bold.otf')
    #plt.xlabel('', fontproperties=prop, fontsize=14, labelpad=12)
    #plt.xticks(fontproperties=prop, fontsize=12)
    #plt.ylabel('PERCENTAGE OF DOGS', fontproperties=prop, fontsize=14, labelpad=12)
    #plt.yticks(fontproperties=prop, fontsize=12)

    # Define the formatting function to add '%' to y-axis tick labels
    def add_percent(x, pos):
        return f"{x:.0f}%"

    # Apply the formatting function to the y-axis
    #ax.yaxis.set_major_formatter(mtick.FuncFormatter(add_percent))
    #plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False, prop=prop, fontsize=14, handleheight=2.5, borderaxespad=-0.25)


if __name__ == "__main__":
    df_profile = read_inputs()
    #grls_dogs_age_distrbution_vis(df_profile)
    sex_vis(df_profile)
