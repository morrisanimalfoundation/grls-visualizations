import settings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#Import data
df_behavior = pd.read_csv(settings.datapath + "behavior_summary.csv")

#Subset data
df_behavior = df_behavior[['subject_id', 'year_in_study', 'topic', 'count_0', 'count_1', 'count_2', 'count_3', 'count_4', 'to_date']]
df_behavior_misc = df_behavior[df_behavior['topic'].isin(['score_attachment_attention_seeking', 'score_chasing', 'score_energy', 'score_separation_related_problems', 'score_trainability'])]

#Calculate percentages
df_behavior_misc = (
    df_behavior_misc.groupby(['topic'])[['count_0', 'count_1', 'count_2', 'count_3', 'count_4']]
    .sum()
    .pipe(lambda d: d.div(d.sum(axis=1), axis=0) * 100)
    .reset_index()
)

#Rename topics
topic_rename_map = {
    'score_attachment_attention_seeking': 'Attachment and Attention Seeking',
    'score_chasing': 'Chasing',
    'score_energy': 'Energy Level',
    'score_separation_related_problems': 'Separation Related Behavior',
    'score_trainability': 'Trainability'
}

df_behavior_misc['topic'] = df_behavior_misc['topic'].map(topic_rename_map)

# Sort by the renamed topic
df_behavior_misc = df_behavior_misc.sort_values(by='topic', key=lambda col: col.str.lower(), ascending=True)

#Define colors
colors = {
    'count_0': '#0085AD',  # Never
    'count_1': '#67CFE3',
    'count_2': '#D3D3D3',  # Seldom
    'count_3': '#FDB525',
    'count_4': '#E35205'   # Always
}

#Create plot
fig, ax = plt.subplots(figsize=(20,6))

#Plot each row to center on Seldom
for i, row in df_behavior_misc.iterrows():
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
ax.set_yticks(range(len(df_behavior_misc)))
ax.set_yticklabels(df_behavior_misc['topic'])
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
    (0.15, 'Never', colors['count_0']),
    (0.5, 'Seldom', colors['count_2']),
    (0.85, 'Always', colors['count_4'])
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
ax.set_ylim(-1.5, len(df_behavior_misc))

# Increase top margin globally
plt.subplots_adjust(top=0.95)

ax.invert_yaxis() # So 'Attachment' is at the top, 'Trainability' at the bottom

plt.tight_layout()
plt.savefig(f'{settings.vizpath}behavior_viz2.png', bbox_inches='tight')
plt.show()