import settings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams.update({'font.weight': 'bold'})

# Load shared data
df_behavior = pd.read_csv(settings.datapath + "behavior_summary.csv")
df_behavior = df_behavior[['subject_id', 'year_in_study', 'topic', 'count_0', 'count_1', 'count_2', 'count_3', 'count_4', 'to_date']]

# Define color schemes (can be reused)
colors = {
    'count_0': '#0085AD',
    'count_1': '#67CFE3',
    'count_2': '#D3D3D3',
    'count_3': '#FDB525',
    'count_4': '#E35205'
}

### ---- Define reusable plotting function ---- ###
def plot_behavior_chart(df_subset, rename_map, ordered_topics, ax, legend_labels, legend_y=0.94):
    # Filter and process data
    df = df_behavior[df_behavior['topic'].isin(rename_map.keys())]
    df = (
        df.groupby('topic')[['count_0', 'count_1', 'count_2', 'count_3', 'count_4']]
        .sum()
        .pipe(lambda d: d.div(d.sum(axis=1), axis=0) * 100)
        .reset_index()
    )
    df['topic'] = df['topic'].map(rename_map)
    df['topic'] = pd.Categorical(df['topic'], categories=ordered_topics, ordered=True)
    df = df.sort_values('topic')

    # Plot each row to center on count_2
    for i, row in df.iterrows():
        topic = row['topic']
        y_pos = i
        center = row['count_2']
        left = row[['count_0', 'count_1']].sum()
        right = row[['count_3', 'count_4']].sum()
        start_x = -left - center/2

        offset = start_x
        for col in ['count_0', 'count_1']:
            width = row[col]
            ax.barh(y_pos, width, left=offset, color=colors[col], edgecolor='white')
            offset += width

        ax.barh(y_pos, center, left=offset, color=colors['count_2'], edgecolor='white')
        offset += center

        for col in ['count_3', 'count_4']:
            width = row[col]
            ax.barh(y_pos, width, left=offset, color=colors[col], edgecolor='white')
            offset += width

    # Formatting
    ax.set_yticks(range(len(df)))
    # Remove default tick labels
    ax.set_yticklabels([])

    # Add left-aligned topic labels outside the axes
    for i, label in enumerate(df['topic']):
        ax.text(
            -0.22,  # Shift further left in axes coords (0 = left edge, 1 = right edge)
            i,
            label,
            transform=ax.get_yaxis_transform(),
            ha='left',
            va='center',
            fontsize=12,
            fontweight='bold'
        )
    ax.tick_params(axis='y', which='major', pad=30)
    ax.tick_params(axis='y', length=0)

    ax.axvline(0, color='black', linestyle='-', linewidth=1, zorder=0)

    ax.set_xlim(-110, 110)

    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False, labeltop=False)
    ax.tick_params(axis='x', length=0)

    ax.set_ylim(-1.5, len(df))
    ax.invert_yaxis()

    # Remove plot borders (spines)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Legend
    legend_y = 0.94
    box_size = 0.025
    text_offset = 0.01
    for x_pos, label, color_key in legend_labels:
        rect = Rectangle((x_pos - box_size / 2, legend_y - box_size / 2),
                         box_size, box_size,
                         transform=ax.transAxes, color=colors[color_key], clip_on=False)
        ax.add_patch(rect)
        ax.text(x_pos + box_size / 2 + text_offset, legend_y, label,
                transform=ax.transAxes, ha='left', va='center',
                fontsize=12, fontweight='bold')


### ---- Create the full figure ---- ###
fig, axes = plt.subplots(nrows=3, figsize=(20, 18))
plt.subplots_adjust(hspace=0.6, top=0.80, bottom=0.05)

# Add a vertical line behind all subplots using figure coordinates
fig_width = 0.125 + (0.5 * 0.775)  # x = center of the 0 line between -100 and 100
line = plt.Line2D(
    [fig_width, fig_width], [0.05, 0.94],  # full vertical span of the subplots
    transform=fig.transFigure,
    color='black',
    linewidth=1,
    linestyle='-',
    zorder=0
)
fig.add_artist(line)

# Add a shared top axis for x-ticks
shared_ax = fig.add_axes([0.125, 0.94, 0.775, 0.05], zorder=0)  # Adjust position as needed
shared_ax.set_xlim(-100, 100)
shared_ax.set_xticks([-90, -45, 0, 45, 90])
shared_ax.set_xticklabels(['100%', '50%', '0%', '50%', '100%'])
shared_ax.xaxis.set_ticks_position('top')
shared_ax.xaxis.set_label_position('top')
shared_ax.tick_params(axis='x', labelsize=12)
shared_ax.spines['top'].set_visible(False)
shared_ax.spines['right'].set_visible(False)
shared_ax.spines['left'].set_visible(False)
shared_ax.spines['bottom'].set_visible(False)
shared_ax.yaxis.set_visible(False)
shared_ax.tick_params(axis='x', length=0)  # remove x tick marks

# Plot 1: Miscellaneous
plot_behavior_chart(
    df_behavior,
    rename_map={
        'score_attachment_attention_seeking': 'Attachment and Attention Seeking',
        'score_chasing': 'Chasing',
        'score_energy': 'Energy Level',
        'score_separation_related_problems': 'Separation Related Behavior',
        'score_trainability': 'Trainability'
    },
    ordered_topics=[
        'Attachment and Attention Seeking',
        'Chasing',
        'Energy Level',
        'Separation Related Behavior',
        'Trainability'
    ],
    ax=axes[0],
    legend_labels=[
        (0.15, 'Never', 'count_0'),
        (0.5, 'Seldom', 'count_2'),
        (0.85, 'Always', 'count_4')
    ],
    legend_y=0.86
)

# Plot 2: Aggression
plot_behavior_chart(
    df_behavior,
    rename_map={
        'score_dog_rivalry': 'Dog Rivalry',
        'score_dog_directed_aggression': 'Dog-Directed Aggression',
        'score_owner_directed_aggression': 'Owner-Directed Aggression',
        'score_stranger_directed_aggression': 'Stranger-Directed Aggression'
    },
    ordered_topics=[
        'Dog Rivalry',
        'Dog-Directed Aggression',
        'Owner-Directed Aggression',
        'Stranger-Directed Aggression'
    ],
    ax=axes[1],
    legend_labels=[
        (0.15, 'No Aggression', 'count_0'),
        (0.5, 'Moderate Aggression', 'count_2'),
        (0.85, 'Severe Aggression', 'count_4')
    ]
)

# Plot 3: Fear
plot_behavior_chart(
    df_behavior,
    rename_map={
        'score_nonsocial_fear': 'Nonsocial Fear',
        'score_dog_directed_fear': 'Dog-Directed Fear',
        'score_stranger_directed_fear': 'Stranger-Directed Fear',
        'score_touch_sensitivity': 'Touch Sensitivity'
    },
    ordered_topics=[
        'Nonsocial Fear',
        'Dog-Directed Fear',
        'Stranger-Directed Fear',
        'Touch Sensitivity'
    ],
    ax=axes[2],
    legend_labels=[
        (0.15, 'No Fear/Anxiety', 'count_0'),
        (0.5, 'Mild - Moderate Fear/Anxiety', 'count_2'),
        (0.85, 'Extreme Fear/Anxiety', 'count_4')
    ]
)

# Adjust layout
plt.subplots_adjust(hspace=0.1, top=0.95)
#plt.tight_layout()

plt.savefig(f'{settings.vizpath}behavior_combined.png', bbox_inches='tight', pad_inches=0.3)
plt.show()