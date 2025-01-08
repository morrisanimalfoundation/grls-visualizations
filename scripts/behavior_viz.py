"""
A simple visualization script for behavior visualizations.
"""
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import settings

#Import data file
def read_inputs() -> pd.DataFrame:
    df_behavior = pd.read_csv(settings.datapath + "behavior_summary.csv")
    return df_behavior

df_behavior = read_inputs()

def grls_cbarq_behavior_categories_vis(dataframe) -> None:
    """
    Creates the C-Barq Behavior Categories visualization - a horizontal stacked bar graph - with frequency on
    the x-axis and behavior on the y-axis.

    Parameters
    ----------
    dataframe : pd.DataFrame
        The behavior_summary dataset.

    """

#Aggregate data
behavior_aggregated = df_behavior.groupby('topic')[['count_0', 'count_1', 'count_2', 'count_3', 'count_4']].sum()

#Calculate proportions
proportions = behavior_aggregated.div(behavior_aggregated.sum(axis=1), axis=0)

#Rename topics
topic_rename_map = {
    'score_trainability': 'Trainability', 'score_touch_sensitivity': 'Touch Sensitivity',
    'score_stranger_directed_fear': 'Stranger-Directed Fear',
    'score_stranger_directed_aggression': 'Stranger-Directed Aggression',
    'score_separation_related_problems': 'Separation Related Behavior',
    'score_owner_directed_aggression': 'Owner-Directed Aggression', 'score_nonsocial_fear': 'Nonsocial Fear',
    'score_excitability': 'Excitability', 'score_energy': 'Energy Level', 'score_dog_rivalry': 'Dog Rivalry',
    'score_dog_directed_fear': 'Dog-Directed Fear', 'score_dog_directed_aggression': 'Dog-Directed Aggression',
    'score_chasing': 'Chasing', 'score_attachment_attention_seeking': 'Attachment and Attention Seeking'
}
proportions = proportions.rename(index=topic_rename_map)

# Define colors and labels
colors = ['#0085AD', '#67CFE3', '#d3d3d3', '#FDB525', '#E35205']
labels = ['Never', 'Seldom', 'Sometimes', 'Often', 'Always']

categories = [
    'Attachment and Attention Seeking', 'Chasing', 'Energy Level', 'Excitability',
    'Separation Related Behavior', 'Trainability', '',
    'Dog Rivalry', 'Dog-Directed Aggression', 'Owner-Directed Aggression',
    'Stranger-Directed Aggression', '',
    'Nonsocial Fear', 'Dog-Directed Fear', 'Stranger-Directed Fear',
    'Touch Sensitivity'
]

#Configure plot
fig, ax = plt.subplots(figsize=(14,8))

#Plot each category as a stacked bar
current_y = 0
spacing = 1.5

for index, (topic, row) in enumerate(proportions.iterrows()):
    left = -row['count_2'] / 2
    for i, color in enumerate(colors):
        ax.barh(current_y, row[i], left=left, color=color)
        left += row[i]
    current_y += 1 if categories[index] != '' else spacing

###left = -proportions['count_2']/2
### #   #np.zeros(len(proportions)))
###for i, (color, label) in enumerate(zip(colors, labels)):
###   ax.barh(proportions.index, proportions.iloc[:, i], left=left, color=color, label=label)
 ###  left += proportions.iloc[:, i]

# Customize the plot

#Set x tick marks
ax.set_xticks([-1, -.5, 0, .5, 1])
ax.set_xticklabels(['100%', '50%', '0%', '50%', '100%'])

#Set y tick marks
ax.set_yticks(np.arange(len(categories)) + 0.5)
ax.set_yticklabels(categories)

##ax.set_yticks(range(len(proportions)))
##ax.set_yticklabels(proportions.index)

#Set positions and labels
ax.set_xlim(0, 1)
ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_title('C-BARQ BEHAVIOR CATEGORIES')
ax.legend(labels, title='Response', bbox_to_anchor=(1.05, 1), loc='upper left')

# Add legend boxes for larger categories
ax.text(-1.5, 2.5, 'Attachment and Attention', fontsize=10, color='#0085AD')
ax.text(-1.5, 7.5, 'Aggression', fontsize=10, color='#0085AD')
ax.text(-1.5, 12.5, 'Fear / Anxiety', fontsize=10, color='#0085AD')

#Add legend boxes
ax.text(-1.2, 2, 'Never', fontsize=10, color='#0085AD')
ax.text(-1.2, 7, 'No Aggression', fontsize=10, color='#0085AD')
ax.text(-1.2, 12, 'No Fear / Anxiety', fontsize=10, color='#0085AD')

plt.tight_layout()
plt.show()