"""
Subgroup Forest Plot for Pairwise Comparisons

Publication-quality forest plot with subgroup analysis for visualizing
mean differences across different subgroups (e.g., phases, conditions, timepoints).

Author: Maria Anwar
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Rectangle
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
SUBGROUP_FONTSIZE = 12
BOX_FONTSIZE = 9

# Colors
SIG_COLOR = '#27ae60'       # Green for significant
NS_COLOR = '#bdc3c7'        # Light gray for non-significant
SUBGROUP_COLORS = ['#3498db', '#e74c3c', '#9b59b6', '#f39c12']  # Blue, Red, Purple, Orange
ZERO_LINE_COLOR = '#c0392b'  # Dark red for zero line

# =============================================================================
# 2. DATA INPUT - REPLACE WITH YOUR OWN VALUES
# =============================================================================
# Example: Comparisons across different phases/timepoints
# REPLACE ALL VALUES WITH YOUR STATISTICAL OUTPUT

VARIABLE_NAME = "Outcome Measure"  # <-- CHANGE THIS

# Define subgroups (e.g., phases, conditions, timepoints)
subgroups = {
    "Phase 1 (Baseline)": {
        "comparisons": ["Low vs Medium", "Low vs High", "Medium vs High"],
        "mean_diffs": [0.25, 0.80, 0.55],
        "ci_lower": [-0.45, 0.10, -0.15],
        "ci_upper": [0.95, 1.50, 1.25],
        "p_values": [0.482, 0.025, 0.124]
    },
    "Phase 2 (Treatment)": {
        "comparisons": ["Low vs Medium", "Low vs High", "Medium vs High"],
        "mean_diffs": [-0.60, -2.40, -1.80],
        "ci_lower": [-1.30, -3.10, -2.50],
        "ci_upper": [0.10, -1.70, -1.10],
        "p_values": [0.093, 0.001, 0.001]
    },
    "Phase 3 (Follow-up)": {
        "comparisons": ["Low vs Medium", "Low vs High", "Medium vs High"],
        "mean_diffs": [-0.35, -1.60, -1.25],
        "ci_lower": [-1.05, -2.30, -1.95],
        "ci_upper": [0.35, -0.90, -0.55],
        "p_values": [0.327, 0.001, 0.001]
    }
}

# =============================================================================
# 3. CREATE SUBGROUP FOREST PLOT
# =============================================================================
def create_subgroup_forest_plot(subgroups, variable_name="", save_name=None):
    """
    Create a forest plot with subgroup analysis.
    
    Parameters:
    -----------
    subgroups : dict
        Dictionary containing subgroup data
    variable_name : str
        Name of the outcome variable (for title)
    save_name : str
        Filename to save (optional)
    """
    
    # Calculate total rows needed
    total_rows = 0
    for subgroup_name, data in subgroups.items():
        total_rows += 1  # Subgroup header
        total_rows += len(data["comparisons"])  # Comparisons
        total_rows += 0.5  # Space after subgroup
    
    # Create figure
    fig_height = max(6, total_rows * 0.5)
    fig, ax = plt.subplots(figsize=(14, fig_height))
    
    # Collect all values for x-axis limits
    all_lowers = []
    all_uppers = []
    all_diffs = []
    
    for data in subgroups.values():
        all_lowers.extend(data["ci_lower"])
        all_uppers.extend(data["ci_upper"])
        all_diffs.extend(data["mean_diffs"])
    
    x_min = min(all_lowers) - 1
    x_max = max(all_uppers) + 3
    
    # -------------------------------------------------------------------------
    # A. BACKGROUND SHADING
    # -------------------------------------------------------------------------
    ax.axvspan(x_min, 0, alpha=0.04, color='blue')
    ax.axvspan(0, x_max, alpha=0.04, color='green')
    
    # -------------------------------------------------------------------------
    # B. ZERO REFERENCE LINE
    # -------------------------------------------------------------------------
    ax.axvline(x=0, color=ZERO_LINE_COLOR, linestyle='--', 
               linewidth=2.5, alpha=0.8, zorder=1)
    
    # -------------------------------------------------------------------------
    # C. PLOT DATA BY SUBGROUP
    # -------------------------------------------------------------------------
    y_position = total_rows - 1
    y_labels = []
    y_positions = []
    subgroup_positions = []
    
    for subgroup_idx, (subgroup_name, data) in enumerate(subgroups.items()):
        subgroup_color = SUBGROUP_COLORS[subgroup_idx % len(SUBGROUP_COLORS)]
        
        # Store subgroup header position
        subgroup_positions.append((y_position, subgroup_name, subgroup_color))
        
        # Add subgroup header background
        ax.add_patch(Rectangle(
            (x_min, y_position - 0.4), 
            x_max - x_min + 3, 0.8,
            facecolor=subgroup_color, alpha=0.15, zorder=0
        ))
        
        y_position -= 1
        
        # Plot each comparison in subgroup
        comparisons = data["comparisons"]
        mean_diffs = data["mean_diffs"]
        ci_lower = data["ci_lower"]
        ci_upper = data["ci_upper"]
        p_values = data["p_values"]
        
        for i, (comp, md, lo, hi, p) in enumerate(zip(
            comparisons, mean_diffs, ci_lower, ci_upper, p_values)):
            
            # Determine color based on significance
            color = SIG_COLOR if p < 0.05 else NS_COLOR
            
            # Store position and label
            y_positions.append(y_position)
            y_labels.append(f"  {comp}")  # Indent comparisons
            
            # CI line
            ax.plot([lo, hi], [y_position, y_position],
                    color=color, linewidth=2.5, alpha=0.8, zorder=2)
            
            # CI caps
            ax.plot([lo, lo], [y_position - 0.1, y_position + 0.1],
                    color=color, linewidth=2, zorder=2)
            ax.plot([hi, hi], [y_position - 0.1, y_position + 0.1],
                    color=color, linewidth=2, zorder=2)
            
            # Diamond marker
            diamond_size = 0.15
            diamond = Polygon([
                [md - diamond_size, y_position],
                [md, y_position + diamond_size],
                [md + diamond_size, y_position],
                [md, y_position - diamond_size]
            ], facecolor=color, edgecolor='black', linewidth=1, zorder=5)
            ax.add_patch(diamond)
            
            # Value box on right side
            if p < 0.001:
                p_str = "p < .001***"
            elif p < 0.01:
                p_str = f"p = {p:.3f}**"
            elif p < 0.05:
                p_str = f"p = {p:.3f}*"
            else:
                p_str = f"p = {p:.3f}"
            
            box_text = f"{md:+.2f} [{lo:.2f}, {hi:.2f}]  {p_str}"
            
            ax.text(x_max + 0.3, y_position, box_text,
                    fontsize=BOX_FONTSIZE,
                    ha='left', va='center',
                    fontweight='bold' if p < 0.05 else 'normal',
                    color='black' if p < 0.05 else 'gray')
            
            y_position -= 1
        
        # Add space between subgroups
        y_position -= 0.5
    
    # -------------------------------------------------------------------------
    # D. ADD SUBGROUP HEADERS
    # -------------------------------------------------------------------------
    for y_pos, name, color in subgroup_positions:
        ax.text(x_min + 0.2, y_pos, name,
                fontsize=SUBGROUP_FONTSIZE, fontweight='bold',
                color=color, va='center')
    
    # -------------------------------------------------------------------------
    # E. AXIS FORMATTING
    # -------------------------------------------------------------------------
    ax.set_xlim(x_min, x_max + 4)
    ax.set_ylim(y_position - 0.5, total_rows)
    
    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels, fontsize=TICK_FONTSIZE)
    
    ax.set_xlabel("Mean Difference (95% CI)", fontsize=AXIS_FONTSIZE, fontweight='bold')
    
    # Title
    title_prefix = f"{variable_name}: " if variable_name else ""
    ax.set_title(f"{title_prefix}Subgroup Forest Plot",
                 fontsize=TITLE_FONTSIZE, fontweight='bold', pad=20)
    
    # Clean spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(left=False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # -------------------------------------------------------------------------
    # F. LEGEND
    # -------------------------------------------------------------------------
    legend_elements = [
        Line2D([0], [0], marker='D', linestyle='None',
               markerfacecolor=SIG_COLOR, markeredgecolor='black',
               markersize=10, label='p < .05 (Significant)'),
        Line2D([0], [0], marker='D', linestyle='None',
               markerfacecolor=NS_COLOR, markeredgecolor='black',
               markersize=10, label='p ≥ .05 (Not Significant)'),
        Line2D([0], [0], color=ZERO_LINE_COLOR, linestyle='--',
               linewidth=2, label='No Difference')
    ]
    
    ax.legend(handles=legend_elements,
              loc='lower right',
              fontsize=9,
              framealpha=0.95,
              title='Significance',
              title_fontsize=10)
    
    # -------------------------------------------------------------------------
    # G. INTERPRETATION LABELS
    # -------------------------------------------------------------------------
    ax.text(x_min + 0.3, y_position, '← Favors First', 
            fontsize=9, color='blue', style='italic', ha='left')
    ax.text(x_max - 0.5, y_position, 'Favors Second →', 
            fontsize=9, color='green', style='italic', ha='right')
    
    # -------------------------------------------------------------------------
    # H. COLUMN HEADER
    # -------------------------------------------------------------------------
    ax.text(x_max + 0.3, total_rows - 0.3, "Diff [95% CI]  p-value",
            fontsize=BOX_FONTSIZE, fontweight='bold', ha='left', va='center')
    
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
    
    fig, ax = create_subgroup_forest_plot(
        subgroups=subgroups,
        variable_name=VARIABLE_NAME,
        save_name="forest_plot_subgroup.png"
    )
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUBGROUP ANALYSIS SUMMARY")
    print("=" * 80)
    
    for subgroup_name, data in subgroups.items():
        print(f"\n{subgroup_name}")
        print("-" * 60)
        print(f"{'Comparison':<20} {'Diff':>8} {'95% CI':>18} {'p-value':>10}")
        print("-" * 60)
        
        for comp, md, lo, hi, p in zip(
            data["comparisons"], data["mean_diffs"], 
            data["ci_lower"], data["ci_upper"], data["p_values"]):
            
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            print(f"{comp:<20} {md:>+8.2f} [{lo:>6.2f}, {hi:>6.2f}] {p:>9.3f}{sig}")
    
    print("\n" + "=" * 80)
    print("* p < .05, ** p < .01, *** p < .001")


# =============================================================================
# USAGE INSTRUCTIONS:
# =============================================================================
#
# 1. Replace the data in Section 2 with your own values:
#    - VARIABLE_NAME: Your outcome measure name
#    - subgroups: Dictionary with your subgroup data
#      Each subgroup needs: comparisons, mean_diffs, ci_lower, ci_upper, p_values
#
# 2. Subgroups can represent:
#    - Different phases (Baseline, Treatment, Follow-up)
#    - Different conditions (Puffing, Post-Puffing)
#    - Different timepoints (T1, T2, T3)
#    - Different populations (Group A, Group B)
#
# 3. Run the script:
#    python forest_plot_subgroup.py
#
# 4. Output: 'forest_plot_subgroup.png' at 600 DPI
#
# =============================================================================
