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

from py_secrets import dirpath, vizpath
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns

# reading in our dataset and force setting data types
# note: adds 01 as default day in date values (raw data format yyyy-mm)
df_profile = pd.read_csv(dirpath+"dog_profile.csv", dtype={'subject_id': 'object', 'sex_status': 'category'},
                         parse_dates=['birth_date', 'enrolled_date'])

# calculating age
today = date.today()
born = df_profile['birth_date'].dt
df_profile['current_age'] = today.year - born.year - (today.month < born.month)

# Calculate the count of dogs at each age
age_counts = df_profile['current_age'].value_counts().sort_index()

# Create a bar chart using Seaborn
sns.set_style('whitegrid', {'grid.color': '#ECECEC'})
plt.figure(figsize=(8, 6))  # Adjust the figure size as needed
sns.barplot(x=age_counts.index, y=age_counts.values, color='#FF5F1F', width=0.6)  # Adjust bar colour using HEX code
plt.yticks(range(0, int(age_counts.max() + 100), 400))  # Y-axis ticks in increments of 400
sns.despine(left=True, bottom=True)  # Remove borders

# Set font properties for title and axis labels
title_font = {'weight': 'bold', 'size': 16}
label_font = {'weight': 'bold'}
plt.title('AGE DISTRIBUTION AS OF {}, {}'.format(today.strftime("%B").upper(), today.year), fontdict=title_font)
plt.xlabel('Age (in Years)', fontdict=label_font)
plt.ylabel('Dogs (count)', fontdict=label_font)

# save the plot as PNG file
plt.savefig(vizpath+"dog_age_percent.png")

# displaying the plot
plt.show()
