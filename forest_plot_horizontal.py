"""
Horizontal Forest Plot for Pairwise Comparisons

Publication-quality horizontal forest plot for visualizing mean differences
with confidence intervals from mixed-effects model pairwise comparisons.

Author: Maria Anwar
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from matplotlib import rcParams

# =============================================================================
# 1. STYLE SETTINGS
# =============================================================================
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

TITLE_FONTSIZE = 14
AXIS_FONTSIZE = 13
TICK_FONTSIZE = 11
BOX_FONTSIZE = 10

# Colors
SIG_COLOR = '#2ecc71'      # Green for significant
NS_COLOR = '#95a5a6'       # Gray for non-significant
ZERO_LINE_COLOR = '#e74c3c'  # Red for zero reference line

# =============================================================================
# 2. DATA INPUT - REPLACE WITH YOUR OWN VALUES
# =============================================================================
# Example pairwise comparisons (REPLACE WITH YOUR SPSS/STATISTICAL OUTPUT)
VARIABLE_NAME = "Outcome Measure"  # <-- CHANGE THIS

comparisons = [
    'Low vs Medium',
    'Low vs High',
    'Medium vs High',
    'Control vs Low',
    'Control vs Medium',
    'Control vs High'
]

# Mean differences (REPLACE WITH YOUR VALUES)
mean_diffs = [-0.50, -2.80, -2.30, 0.75, 0.25, -2.05]

# 95% Confidence Intervals (REPLACE WITH YOUR VALUES)
ci_lower = [-2.20, -4.50, -4.00, -0.95, -1.45, -3.75]
ci_upper = [1.20, -1.10, -0.60, 2.45, 1.95, -0.35]

# P-values (REPLACE WITH YOUR VALUES)
p_values = [0.562, 0.001, 0.008, 0.387, 0.773, 0.018]

# =============================================================================
# 3. CREATE HORIZONTAL FOREST PLOT
# =============================================================================
def create_horizontal_forest_plot(comparisons, mean_diffs, ci_lower, ci_upper, 
                                   p_values, variable_name="", save_name=None):
    """
    Create a horizontal forest plot for pairwise comparisons.
    
    Parameters:
    -----------
    comparisons : list
        Labels for each comparison
    mean_diffs : list
        Mean differences for each comparison
    ci_lower : list
        Lower bounds of 95% CI
    ci_upper : list
        Upper bounds of 95% CI
    p_values : list
        P-values for each comparison
    variable_name : str
        Name of the outcome variable (for title)
    save_name : str
        Filename to save (optional)
    """
    
    n_comparisons = len(comparisons)
    
    # Reverse order for top-to-bottom plotting
    comparisons_rev = comparisons[::-1]
    mean_diffs_rev = mean_diffs[::-1]
    ci_lower_rev = ci_lower[::-1]
    ci_upper_rev = ci_upper[::-1]
    p_values_rev = p_values[::-1]
    
    # Y positions
    y_pos = np.arange(n_comparisons)
    
    # Color mapping based on significance
    colors = [SIG_COLOR if p < 0.05 else NS_COLOR for p in p_values_rev]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, max(4, n_comparisons * 0.8)))
    
    # -------------------------------------------------------------------------
    # A. BACKGROUND SHADING
    # -------------------------------------------------------------------------
    # Calculate x-axis limits
    all_values = ci_lower + ci_upper + mean_diffs
    x_min = min(all_values) - 1
    x_max = max(all_values) + 2
    
    # Shading for negative (left) and positive (right) regions
    ax.axvspan(x_min, 0, alpha=0.05, color='blue', label='Favors First')
    ax.axvspan(0, x_max, alpha=0.05, color='green', label='Favors Second')
    
    # -------------------------------------------------------------------------
    # B. ZERO REFERENCE LINE
    # -------------------------------------------------------------------------
    ax.axvline(x=0, color=ZERO_LINE_COLOR, linestyle='--', 
               linewidth=2.5, alpha=0.8, zorder=1)
    
    # -------------------------------------------------------------------------
    # C. CONFIDENCE INTERVAL LINES WITH CAPS
    # -------------------------------------------------------------------------
    for i in range(n_comparisons):
        # Main CI line
        ax.plot([ci_lower_rev[i], ci_upper_rev[i]], 
                [y_pos[i], y_pos[i]],
                color=colors[i], linewidth=3, alpha=0.8, zorder=2)
        
        # Left cap
        ax.plot([ci_lower_rev[i], ci_lower_rev[i]], 
                [y_pos[i] - 0.15, y_pos[i] + 0.15],
                color=colors[i], linewidth=2, zorder=2)
        
        # Right cap
        ax.plot([ci_upper_rev[i], ci_upper_rev[i]], 
                [y_pos[i] - 0.15, y_pos[i] + 0.15],
                color=colors[i], linewidth=2, zorder=2)
    
    # -------------------------------------------------------------------------
    # D. DIAMOND POINT ESTIMATES
    # -------------------------------------------------------------------------
    diamond_size = 0.2
    for md, y, c in zip(mean_diffs_rev, y_pos, colors):
        diamond = Polygon([
            [md - diamond_size, y],
            [md, y + diamond_size],
            [md + diamond_size, y],
            [md, y - diamond_size]
        ], facecolor=c, edgecolor='black', linewidth=1.5, zorder=5)
        ax.add_patch(diamond)
    
    # -------------------------------------------------------------------------
    # E. VALUE BOXES (Right side)
    # -------------------------------------------------------------------------
    box_x = x_max - 0.5
    
    for i, (md, lo, hi, p) in enumerate(zip(mean_diffs_rev, ci_lower_rev, 
                                             ci_upper_rev, p_values_rev)):
        # Format p-value with significance markers
        if p < 0.001:
            p_str = "p < .001***"
        elif p < 0.01:
            p_str = f"p = {p:.3f}**"
        elif p < 0.05:
            p_str = f"p = {p:.3f}*"
        else:
            p_str = f"p = {p:.3f}"
        
        # Create text box
        box_text = f"Diff: {md:.2f}\n95% CI [{lo:.2f}, {hi:.2f}]\n{p_str}"
        
        ax.text(box_x, y_pos[i], box_text,
                fontsize=BOX_FONTSIZE,
                ha='left', va='center',
                fontweight='bold' if p < 0.05 else 'normal',
                bbox=dict(
                    boxstyle='round,pad=0.4',
                    facecolor='lightyellow' if p < 0.05 else 'white',
                    alpha=0.9,
                    edgecolor='black' if p < 0.05 else 'gray'
                ))
    
    # -------------------------------------------------------------------------
    # F. AXIS FORMATTING
    # -------------------------------------------------------------------------
    ax.set_xlim(x_min, x_max + 3)
    ax.set_ylim(-0.8, n_comparisons - 0.2)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(comparisons_rev, fontsize=TICK_FONTSIZE, fontweight='bold')
    
    ax.set_xlabel("Mean Difference (95% CI)", fontsize=AXIS_FONTSIZE, fontweight='bold')
    
    # Title
    title_prefix = f"{variable_name}: " if variable_name else ""
    ax.set_title(f"{title_prefix}Pairwise Comparisons Forest Plot",
                 fontsize=TITLE_FONTSIZE, fontweight='bold', pad=20)
    
    # Clean spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # -------------------------------------------------------------------------
    # G. LEGEND
    # -------------------------------------------------------------------------
    legend_elements = [
        Line2D([0], [0], marker='D', linestyle='None',
               markerfacecolor=SIG_COLOR, markeredgecolor='black',
               markersize=10, label='p < .05 (Significant)'),
        Line2D([0], [0], marker='D', linestyle='None',
               markerfacecolor=NS_COLOR, markeredgecolor='black',
               markersize=10, label='p ≥ .05 (Not Significant)'),
        Line2D([0], [0], color=ZERO_LINE_COLOR, linestyle='--',
               linewidth=2, label='No Difference (Zero)')
    ]
    
    ax.legend(handles=legend_elements,
              loc='lower right',
              fontsize=9,
              framealpha=0.95,
              title='Significance Level',
              title_fontsize=10)
    
    # -------------------------------------------------------------------------
    # H. INTERPRETATION LABELS
    # -------------------------------------------------------------------------
    ax.text(x_min + 0.5, -0.6, '← Favors First Group', 
            fontsize=9, color='blue', style='italic', ha='left')
    ax.text(x_max - 1, -0.6, 'Favors Second Group →', 
            fontsize=9, color='green', style='italic', ha='right')
    
    # -------------------------------------------------------------------------
    # I. SAVE AND SHOW
    # -------------------------------------------------------------------------
    plt.tight_layout()
    
    if save_name:
        plt.savefig(save_name, dpi=600, bbox_inches='tight')
        print(f"Figure saved as: {save_name}")
    
    plt.show()
    
    return fig, ax


# =============================================================================
# 4. RUN THE PLOT
# =============================================================================
if __name__ == "__main__":
    
    fig, ax = create_horizontal_forest_plot(
        comparisons=comparisons,
        mean_diffs=mean_diffs,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        p_values=p_values,
        variable_name=VARIABLE_NAME,
        save_name="forest_plot_horizontal.png"
    )
    
    # Print summary table
    print("\n" + "=" * 70)
    print("PAIRWISE COMPARISONS SUMMARY")
    print("=" * 70)
    print(f"{'Comparison':<20} {'Diff':>8} {'95% CI':>18} {'p-value':>10} {'Sig':>6}")
    print("-" * 70)
    
    for comp, md, lo, hi, p in zip(comparisons, mean_diffs, ci_lower, ci_upper, p_values):
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"{comp:<20} {md:>8.3f} [{lo:>6.2f}, {hi:>6.2f}] {p:>10.3f} {sig:>6}")
    
    print("=" * 70)
    print("* p < .05, ** p < .01, *** p < .001")


# =============================================================================
# USAGE INSTRUCTIONS:
# =============================================================================
#
# 1. Replace the data in Section 2 with your own values:
#    - VARIABLE_NAME: Name of your outcome measure
#    - comparisons: List of comparison labels
#    - mean_diffs: Mean differences from pairwise comparisons
#    - ci_lower: Lower bounds of 95% confidence intervals
#    - ci_upper: Upper bounds of 95% confidence intervals
#    - p_values: P-values for each comparison
#
# 2. Run the script:
#    python forest_plot_horizontal.py
#
# 3. The plot will be saved as 'forest_plot_horizontal.png' at 600 DPI
#
