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

# Suppressing warnings for category datatype
# TODO: Investigate this further to prevent technical debt
import warnings

import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import seaborn as sns

from settings import dirpath, embargo_year, vizpath

warnings.filterwarnings("ignore", "is_categorical_dtype")
warnings.filterwarnings("ignore", "use_inf_as_na")
warnings.filterwarnings("ignore", category=FutureWarning)


def read_inputs() -> pd.DataFrame:
    """
    Reads the input CSV file for dog profiles.

    This function reads the CSV file located in the directory specified by `dirpath`:
    1. "dog_profile.csv" - Contains dog profile information including birth, enrollment date, and spayed/neutered date.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the dog profile data.
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
    # Only want alive dogs
    dataframe = dataframe[dataframe['death_date'].notna()].copy()

    # Convert birth date to datetime object
    dataframe['birth_date'] = pd.to_datetime(dataframe['birth_date'])
    # Get todays date
    today = pd.to_datetime('today').date()
    # Calculate current age
    dataframe['current_age'] = (today.year - dataframe['birth_date'].dt.year
                                - (today.month < dataframe['birth_date'].dt.month))
    # Calculate the count of dogs at each age
    age_counts = dataframe['current_age'].value_counts().sort_index()

    # Calculate max age for yticks
    max_count = age_counts.max()

    # Set the HEX code for the grey colour of the grid lines
    sns.set_style('whitegrid', {'grid.color': '#ECECEC'})
    # Set font properties for title and axis labels
    prop = font_manager.FontProperties(fname='/usr/local/share/fonts/Buntype - BundaySans-Bold.otf')
    # Adjust the figure size as needed
    plt.figure(figsize=(10, 6))
    # Adjust bar colour using HEX code
    sns.barplot(x=age_counts.index, y=age_counts.values, color='#FF5F1F', width=0.7)
    # Add labels on top of each bar
    for i, count in enumerate(age_counts.values):
        plt.text(i, count + 5, str(count), ha='center', va='bottom',
                 fontsize=10)  # Adjust offset and fontsize as needed

    # Adjust y-axis limits and ticks
    plt.ylim(0, max_count + 100)  # Set y-axis limit slightly above max count
    plt.yticks(range(0, max_count + 100, 100), fontsize=12)  # Y-axis ticks every 100 units
    sns.despine(left=True, bottom=True)  # Remove borders

    # Add axis labels
    plt.xlabel('AGE', fontproperties=prop, fontsize=14, labelpad=12)
    plt.ylabel('DOGS', fontproperties=prop, fontsize=14, labelpad=12)
    plt.xticks(fontproperties=prop, fontsize=12)

    # Make sure the dates are dynamically adjusted
    current_month_year = today.strftime('%B, %Y').upper()
    # Example of setting font properties for title
    plt.title(f'AGE DISTRIBUTIONS AS OF {current_month_year}', fontproperties=prop, fontsize=16)

    # Save the plot as PNG file
    plt.savefig(vizpath + "age_count.png")

    # Uncomment to display the plot
    # plt.show()


def sex_vis(df_base: pd.DataFrame) -> None:
    """
    Creates the Sex Status visualization - a stacked bar plot - with sex status of dogs on the X-axis and
    the percentage of the dogs on the Y-axis.

    Parameters
    ----------
    df_base: pd.DataFrame
        The dog_profile dataset, which should include the following columns:
        - 'sex_status': The current sex status of the dog.
        - 'enrolled_date': The date the dog was enrolled in the study.
        - 'spay_neuter_date': The date the dog was spayed or neutered.
    """
    # Reorder the Gender x Status
    df_base['sex_status'].replace({
        'Neutered Male': 'Male Neutered',
        'Intact Male': 'Male Intact',
        'Spayed Female': 'Female Spayed',
        'Intact Female': 'Female Intact'
    }, inplace=True)

    # Convert date columns to datetime
    df_base['enrolled_date'] = pd.to_datetime(df_base['enrolled_date'])
    df_base['spay_neuter_date'] = pd.to_datetime(df_base['spay_neuter_date'])

    # Calculate the difference in years
    df_base['spay_neuter_year'] = np.floor(
        (df_base['spay_neuter_date'] - df_base['enrolled_date']).dt.days / 365.25)

    # IF spay_neuter_date is before the enrolled date then set spay_neuter_year to 0
    df_base.loc[df_base['spay_neuter_date'] < df_base['enrolled_date'], 'spay_neuter_year'] = 0

    # Ignore rows where spay_neuter_date is NaT by setting spay_neuter_year to NaN
    df_base['spay_neuter_year'] = df_base['spay_neuter_year'].where(df_base['spay_neuter_date'].notna())

    # Create the new_sex_status column for baseline
    df_base['baseline_sex_status'] = df_base.apply(lambda row:
                                                   row['sex_status'] if pd.isnull(row['spay_neuter_date'])
                                                   else 'Female Spayed' if row['spay_neuter_year'] == 0 and row[
                                                       'sex_status'].startswith('Female')
                                                   else 'Male Neutered' if row['spay_neuter_year'] == 0 and row[
                                                       'sex_status'].startswith('Male')
                                                   else 'Female Intact' if row['spay_neuter_year'] > 0 and row[
                                                       'sex_status'].startswith(
                                                       'Female')
                                                   else 'Male Intact' if row['spay_neuter_year'] > 0 and row[
                                                       'sex_status'].startswith('Male')
                                                   else row['sex_status'],
                                                   axis=1
                                                   )

    # Calculate percentages for sex_status
    percentage_sex_status = df_base['baseline_sex_status'].value_counts(
        normalize=True).reset_index()
    percentage_sex_status.columns = ['status', 'percent']

    # Middle point
    middle_year = int(np.floor(embargo_year / 2))
    middle_col_name = 'year_' + str(middle_year) + '_sex_status'
    # Create the new_sex_status column for year_3
    df_base[middle_col_name] = df_base.apply(lambda row:
                                             row['sex_status'] if pd.isnull(row['spay_neuter_date'])
                                             else 'Female Spayed' if 0 < row['spay_neuter_year'] <= middle_year and row[
                                                 'sex_status'].startswith('Female')
                                             else 'Male Neutered' if 0 < row['spay_neuter_year'] <= middle_year and row[
                                                 'sex_status'].startswith('Male')
                                             else 'Female Intact' if row['spay_neuter_year'] > middle_year and row[
                                                 'sex_status'].startswith(
                                                 'Female')
                                             else 'Male Intact' if row['spay_neuter_year'] > middle_year and row[
                                                 'sex_status'].startswith('Male')
                                             else row['sex_status'],
                                             axis=1
                                             )

    # Calculate percentages for new_sex_status within the filtered data
    percentage_middle_year_sex_status = df_base[middle_col_name].value_counts(normalize=True).reset_index()
    percentage_middle_year_sex_status.columns = ['status', 'percent']

    embargo_year_name = 'year_' + str(embargo_year) + '_sex_status'
    # Create the new_sex_status column for year 5
    df_base[embargo_year_name] = df_base.apply(lambda row:
                                               row['sex_status'] if pd.isnull(row['spay_neuter_date'])
                                               else 'Female Spayed' if middle_year < row[
                                                   'spay_neuter_year'] <= embargo_year and row[
                                                   'sex_status'].startswith('Female')
                                               else 'Male Neutered' if middle_year < row[
                                                   'spay_neuter_year'] <= embargo_year and row[
                                                   'sex_status'].startswith('Male')
                                               else 'Female Intact' if row['spay_neuter_year'] > embargo_year and row[
                                                   'sex_status'].startswith(
                                                   'Female')
                                               else 'Male Intact' if row['spay_neuter_year'] > embargo_year and row[
                                                   'sex_status'].startswith('Male')
                                               else row['sex_status'],
                                               axis=1
                                               )
    # Calculate percentages for new_sex_status within the filtered data
    percentage_embargo_year_sex_status = df_base[embargo_year_name].value_counts(normalize=True).reset_index()
    percentage_embargo_year_sex_status.columns = ['status', 'percent']

    # Combine the DataFrames for plotting
    percentage_sex_status['Study Year'] = 'Baseline'
    percentage_middle_year_sex_status['Study Year'] = 'Year ' + str(middle_year)
    percentage_embargo_year_sex_status['Study Year'] = 'Year ' + str(embargo_year)

    combined_df = pd.concat([percentage_sex_status, percentage_middle_year_sex_status, percentage_embargo_year_sex_status])

    # Multiply percent by 100 to get percentage
    combined_df['percent'] = combined_df['percent'] * 100

    # Define the order of the categories
    category_order = ['Male Intact', 'Female Intact', 'Female Spayed', 'Male Neutered']
    combined_df['status'] = pd.Categorical(combined_df['status'], categories=category_order, ordered=True)

    # Plotting
    sns.set_style('whitegrid', {'grid.color': '#ECECEC'})  # HEX code for the grey color of the grid lines
    # Set font properties for title and axis labels
    prop = font_manager.FontProperties(fname='/usr/local/share/fonts/Buntype - BundaySans-Bold.otf')
    plt.figure(figsize=(10, 8))  # Adjust the figure size as needed
    ax = sns.barplot(x='status', y='percent', hue='Study Year', data=combined_df,
                     palette=['#0288D1', '#FF5F1F', '#d0db01'],
                     linewidth=2)

    plt.xlabel('', fontproperties=prop, fontsize=14, labelpad=12)  # Empty x-axis label
    plt.xticks(fontproperties=prop, fontsize=12)
    plt.ylabel('PERCENTAGE OF DOGS  ', fontproperties=prop, fontsize=14, labelpad=12)  # Empty x-axis label
    # Y-axis ticks in increments of 10
    plt.yticks(range(0, int(combined_df['percent'].max() + 10), 10), fontproperties=prop, fontsize=12)
    # Remove borders
    sns.despine(left=True, bottom=True)

    # Define the formatting function to add '%' to y-axis tick labels
    def add_percent(x, pos):
        return f"{x:.0f}%"

    # Apply the formatting function to the y-axis
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(add_percent))

    # Position the legend at the bottom center (where x-axis title would be)
    plt.legend(loc='center', bbox_to_anchor=(0.5, -0.1), frameon=False, prop=prop, fontsize=12, ncol=3)

    # Get the current month and year
    today = pd.Timestamp.today()
    current_month_year = today.strftime('%B, %Y').upper()

    # Set the title of the plot
    plt.title(f'AGE DISTRIBUTIONS AS OF {current_month_year}', fontproperties=prop, fontsize=16)

    # Save the plot as a PNG file
    plt.savefig(vizpath + "sex_status.png")

    # Display the plot
    # plt.show()


if __name__ == "__main__":
    df_profile = read_inputs()
    grls_dogs_age_distrbution_vis(df_profile)
    sex_vis(df_profile)
    warnings.resetwarnings()
