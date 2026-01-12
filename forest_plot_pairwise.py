"""
Pairwise Forest Plot (Synthetic Example)

This script generates a publication-quality forest plot for pairwise comparisons
(mean difference with 95% CI), styled by p-value significance.

IMPORTANT (IRB / privacy):
- The default values in this script are SYNTHETIC EXAMPLES ONLY.
- Do NOT commit real study results to a public repository.
- If you want to plot real results, load them locally from a CSV (see optional section below).
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

# =============================================================================
# STYLE SETTINGS
# =============================================================================
TITLE_FONTSIZE = 14
XAXIS_FONTSIZE = 13
BOX_FONTSIZE   = 11

SIG_COLOR = '#f1c40f'   # yellow (significant)
NS_COLOR  = '#4b2e83'   # dark purple (non-significant)
ZERO_LINE_COLOR = 'red'

VARIABLE_NAME = "Example Outcome (Synthetic)"
TITLE_PREFIX = f"{VARIABLE_NAME}: " if VARIABLE_NAME else ""

# =============================================================================
# DATA (SYNTHETIC EXAMPLE VALUES — SAFE FOR PUBLIC REPO)
# =============================================================================
# These are NOT from any real participants, studies, or outputs.
comparisons = [
    'Condition A vs B',
    'Condition A vs C',
    'Condition B vs C'
]

# Synthetic mean differences and 95% CI (constructed for demonstration)
mean_diffs = [-1.120, -2.450, -1.330]
ci_lower   = [-2.980, -4.210, -3.050]
ci_upper   = [ 0.740, -0.690,  0.390]
p_values   = [ 0.240,  0.004,  0.180]

# =============================================================================
# FIGURE
# =============================================================================
fig, ax = plt.subplots(figsize=(11, 6))

# Reverse for top-to-bottom plotting
comparisons_rev = comparisons[::-1]
mean_diffs_rev  = mean_diffs[::-1]
ci_lower_rev    = ci_lower[::-1]
ci_upper_rev    = ci_upper[::-1]
p_values_rev    = p_values[::-1]

y_pos = np.arange(len(comparisons_rev))

# Color mapping
colors = [SIG_COLOR if p < 0.05 else NS_COLOR for p in p_values_rev]

# -----------------------------------------------------------------------------
# CI LINES + CAPS
# -----------------------------------------------------------------------------
for i in range(len(y_pos)):
    ax.plot([ci_lower_rev[i], ci_upper_rev[i]],
            [y_pos[i], y_pos[i]],
            color=colors[i], linewidth=3, alpha=0.75)

    ax.plot([ci_lower_rev[i], ci_lower_rev[i]],
            [y_pos[i]-0.1, y_pos[i]+0.1],
            color=colors[i], linewidth=2)

    ax.plot([ci_upper_rev[i], ci_upper_rev[i]],
            [y_pos[i]-0.1, y_pos[i]+0.1],
            color=colors[i], linewidth=2)

# -----------------------------------------------------------------------------
# DIAMOND POINT ESTIMATES
# -----------------------------------------------------------------------------
for md, y, c in zip(mean_diffs_rev, y_pos, colors):
    diamond = Polygon([
        [md-0.15, y],
        [md, y+0.15],
        [md+0.15, y],
        [md, y-0.15]
    ], facecolor=c, edgecolor='black', linewidth=2, zorder=5)
    ax.add_patch(diamond)

# -----------------------------------------------------------------------------
# ZERO LINE + BACKGROUND SHADING
# -----------------------------------------------------------------------------
ax.axvline(x=0, color=ZERO_LINE_COLOR, linestyle='--',
           linewidth=2.5, alpha=0.8)

# Background shading based on current x-limits (computed below)
# We'll set x-limits first, then shade relative regions.

# -----------------------------------------------------------------------------
# RIGHT-SIDE VALUE BOXES (Difference + p only)
# -----------------------------------------------------------------------------
# Place boxes near the right side of plot area using x-limits
# (Computed after x-limits are set)

# -----------------------------------------------------------------------------
# AXES FORMATTING (NO WHITE SPACE)
# -----------------------------------------------------------------------------
# Choose x-limits based on synthetic CI range with a bit of padding
min_x = min(ci_lower) - 0.8
max_x = max(ci_upper) + 1.6
ax.set_xlim(min_x, max_x)
ax.margins(x=0)

ax.set_ylim(-0.8, len(y_pos)-0.2)

ax.set_yticks(y_pos)
ax.set_yticklabels(comparisons_rev, fontsize=12, fontweight='bold')

ax.set_xlabel("Mean Difference",
              fontsize=XAXIS_FONTSIZE, fontweight='bold')

ax.set_title(f"{TITLE_PREFIX}Pairwise Comparisons",
             fontsize=TITLE_FONTSIZE, fontweight='bold', pad=20)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3, linestyle='--')

# Background shading AFTER x-limits are set
x_left, x_right = ax.get_xlim()
ax.axvspan(x_left, 0, alpha=0.05, color='blue')
ax.axvspan(0, x_right, alpha=0.05, color='green')

# Right-side table x position (a bit inside right edge)
table_x = x_right - (x_right - x_left) * 0.18

for md, p, y in zip(mean_diffs_rev, p_values_rev, y_pos):
    if p < 0.01:
        p_str = f"p = {p:.3f}**"
    elif p < 0.05:
        p_str = f"p = {p:.3f}*"
    else:
        p_str = f"p = {p:.3f}"

    ax.text(table_x, y, f"{md:.3f}\n{p_str}",
            fontsize=BOX_FONTSIZE,
            ha='left', va='center',
            fontweight='bold' if p < 0.05 else 'normal',
            bbox=dict(
                boxstyle='round,pad=0.35',
                facecolor='wheat' if p < 0.05 else 'white',
                alpha=0.7,
                edgecolor='black'
            ))

# -----------------------------------------------------------------------------
# LEGEND
# -----------------------------------------------------------------------------
legend_elements = [
    Line2D([0], [0], marker='D', linestyle='None',
           markerfacecolor=SIG_COLOR, markeredgecolor='black',
           markersize=9, label='p < .05'),
    Line2D([0], [0], marker='D', linestyle='None',
           markerfacecolor=NS_COLOR, markeredgecolor='black',
           markersize=9, label='Not significant')
]

ax.legend(handles=legend_elements,
          loc='upper left',
          fontsize=9,
          framealpha=0.9,
          title='Significance Level')

# -----------------------------------------------------------------------------
# SAVE + SHOW
# -----------------------------------------------------------------------------
plt.tight_layout()
plt.savefig(
    "Example_Pairwise_ForestPlot_SYNTHETIC.png",
    dpi=600,
    bbox_inches='tight'
)
plt.show()
