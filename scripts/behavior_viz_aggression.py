import settings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#Import data
df_behavior = pd.read_csv(settings.datapath + "behavior_summary.csv")

#Subset data
df_behavior = df_behavior[['subject_id', 'year_in_study', 'topic', 'count_0', 'count_1', 'count_2', 'count_3', 'count_4', 'to_date']]
df_behavior_aggression = df_behavior[df_behavior['topic'].isin(['score_dog_rivalry', 'score_dog_directed_aggression', 'score_owner_directed_aggression', 'score_stranger_directed_aggression'])]

#Calculate percentages
df_behavior_aggression = (
    df_behavior_aggression.groupby(['topic'])[['count_0', 'count_1', 'count_2', 'count_3', 'count_4']]
    .sum()
    .pipe(lambda d: d.div(d.sum(axis=1), axis=0) * 100)
    .reset_index()
)

#Rename topics
topic_rename_map = {
    'score_dog_rivalry': 'Dog Rivalry',
    'score_dog_directed_aggression': 'Dog-Directed Aggression',
    'score_owner_directed_aggression': 'Owner-Directed Aggression',
    'score_stranger_directed_aggression': 'Stranger-Directed Aggression'
}

df_behavior_aggression['topic'] = df_behavior_aggression['topic'].map(topic_rename_map)

# Sort by the renamed topic
df_behavior_aggression = df_behavior_aggression.sort_values(by='topic', key=lambda col: col.str.lower(), ascending=True)

#Define colors
colors = {
    'count_0': '#0085AD',  # No Aggression
    'count_1': '#67CFE3',
    'count_2': '#D3D3D3',  # Moderate Aggression
    'count_3': '#FDB525',
    'count_4': '#E35205'   # Severe Aggression
}

#Create plot
fig, ax = plt.subplots(figsize=(20,6))

#Plot each row to center on Moderate Aggression
for i, row in df_behavior_aggression.iterrows():
    topic = row['topic']
    y_pos = i
    center = row['count_2']
    left = row[['count_0', 'count_1']].sum()
    right = row[['count_3', 'count_4']].sum()

    # Start position so that count_2 is centered
    start_x = -left - center/2

    # Plot left segments (count_0, count_1)
    offset = start_x
    for col in ['count_0', 'count_1']:
        width = row[col]
        ax.barh(y_pos, width, left=offset, color=colors[col], edgecolor='white')
        offset += width

    # Plot center segment (count_2)
    ax.barh(y_pos, center, left=offset, color=colors['count_2'], edgecolor='white')
    offset += center

    # Plot right segments (count_3, count_4)
    for col in ['count_3', 'count_4']:
        width = row[col]
        ax.barh(y_pos, width, left=offset, color=colors[col], edgecolor='white')
        offset += width

# Formatting
ax.set_yticks(range(len(df_behavior_aggression)))
ax.set_yticklabels(df_behavior_aggression['topic'])
# Draw center line
center_line_y = 0.85
ax.axvline(0, color='black', linestyle='--', linewidth=1, ymax=center_line_y)

#Customize x axis
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')

ax.set_xlim(-100, 100)
ax.set_xticks([-100, -50, 0, 50, 100])
ax.set_xticklabels(['100%', '50%', '0%', '50%', '100%'])

###Custom legend
# Custom responsive legend using Axes coordinates
legend_y = 0.94          # Vertical position (just below the top x-axis ticks)
box_size = 0.025         # Box height and width (square in axes coordinates)
text_offset = 0.01       # Horizontal space between box and label

# Legend items: horizontal positions are normalized (0 = far left, 1 = far right)
legend_items = [
    (0.15, 'No Aggression', colors['count_0']),
    (0.5, 'Moderate Aggression', colors['count_2']),
    (0.85, 'Severe Aggression', colors['count_4'])
]

for x_pos, label, color in legend_items:
    # Add a square box
    rect = Rectangle((x_pos - box_size / 2, legend_y - box_size / 2),
                     box_size, box_size,
                     transform=ax.transAxes, color=color, clip_on=False)
    ax.add_patch(rect)

    # Add label next to the box
    ax.text(x_pos + box_size / 2 + text_offset, legend_y, label,
            transform=ax.transAxes, ha='left', va='center',
            fontsize=12, fontweight='bold')

# Adjust ylim to give space between bars and legend
ax.set_ylim(-1.5, len(df_behavior_aggression))

# Increase top margin globally
plt.subplots_adjust(top=0.95)

ax.invert_yaxis() # So 'Dog Rivalry' is at the top, 'Stranger-Directed Aggression' at the bottom

plt.tight_layout()
plt.savefig(f'{settings.vizpath}behavior_viz_aggression.png', bbox_inches='tight')
plt.show()