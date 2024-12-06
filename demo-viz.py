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
2.

Author: Neha Bhomia
Created Date: September 19th, 2023
"""

from datetime import date

import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from py_secrets import dirpath, fontpath, vizpath

# reading in our dataset and force setting data types
# note: adds 01 as default day in date values (raw data format yyyy-mm)
df_profile = pd.read_csv(dirpath + 'dog_profile.csv', dtype={'subject_id': 'object', 'sex_status': 'category'},
                         parse_dates=['birth_date', 'enrolled_date'])

# calculating age
today = date.today()
born = df_profile['birth_date'].dt
df_profile['current_age'] = today.year - born.year - (today.month < born.month)

# Calculate the count of dogs at each age
age_counts = df_profile['current_age'].value_counts().sort_index()

# Create a bar chart using Seaborn
sns.set_style('whitegrid', {'grid.color': '#ECECEC'})  # HEX code for the grey colour of the grid lines
plt.figure(figsize=(8, 6))  # Adjust the figure size as needed
sns.barplot(x=age_counts.index, y=age_counts.values, color='#FF5F1F', width=0.7)  # Adjust bar colour using HEX code
plt.yticks(range(0, int(age_counts.max() + 100), 400))  # Y-axis ticks in increments of 400
sns.despine(left=True, bottom=True)  # Remove borders

# Set font properties for title and axis labels
prop = font_manager.FontProperties(fname=fontpath + 'Buntype - BundaySans-Bold.otf')
plt.xlabel('AGE (YEARS)', fontproperties=prop, fontsize=14, labelpad=12)
plt.xticks(fontproperties=prop, fontsize=12)
plt.ylabel('DOGS (COUNT)', fontproperties=prop, fontsize=14, labelpad=12)
plt.yticks(fontproperties=prop, fontsize=12)

# save the plot as PNG file
plt.savefig(vizpath + 'age_count.png')

# displaying the plot
plt.show()
