"""
Funnel Plot for Publication Bias Assessment

Publication-quality funnel plot for assessing publication bias
in pairwise comparisons from mixed-effects models.

A symmetrical funnel suggests no publication bias.
Asymmetry may indicate potential publication bias.

Author: Maria Anwar
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from scipy import stats

# =============================================================================
# 1. STYLE SETTINGS
# =============================================================================
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

TITLE_FONTSIZE = 14
AXIS_FONTSIZE = 13
TICK_FONTSIZE = 11

# Colors
SIG_COLOR = '#27ae60'       # Green for significant
NS_COLOR = '#3498db'        # Blue for non-significant
FUNNEL_COLOR = '#ecf0f1'    # Light gray for funnel
LINE_COLOR = '#2c3e50'      # Dark for reference lines

# =============================================================================
# 2. DATA INPUT - REPLACE WITH YOUR OWN VALUES
# =============================================================================
# Example data from pairwise comparisons
# REPLACE ALL VALUES WITH YOUR STATISTICAL OUTPUT

VARIABLE_NAME = "Outcome Measure"  # <-- CHANGE THIS

# Labels for each comparison
comparisons = [
    'Study 1: Low vs Medium',
    'Study 2: Low vs High',
    'Study 3: Medium vs High',
    'Study 4: Low vs Medium',
    'Study 5: Low vs High',
    'Study 6: Medium vs High',
    'Study 7: Low vs Medium',
    'Study 8: Low vs High'
]

# Effect sizes (mean differences) - REPLACE WITH YOUR VALUES
effect_sizes = [0.25, -2.40, -1.80, 0.50, -1.90, -1.50, -0.10, -2.10]

# Standard errors - REPLACE WITH YOUR VALUES
standard_errors = [0.35, 0.42, 0.38, 0.55, 0.48, 0.40, 0.60, 0.45]

# P-values (optional, for coloring) - REPLACE WITH YOUR VALUES
p_values = [0.475, 0.001, 0.001, 0.364, 0.001, 0.001, 0.868, 0.001]

# =============================================================================
# 3. CREATE FUNNEL PLOT
# =============================================================================
def create_funnel_plot(effect_sizes, standard_errors, p_values=None,
                       comparisons=None, variable_name="", save_name=None):
    """
    Create a funnel plot for publication bias assessment.
    
    Parameters:
    -----------
    effect_sizes : list
        Effect sizes (mean differences) for each comparison
    standard_errors : list
        Standard errors for each comparison
    p_values : list, optional
        P-values for coloring points by significance
    comparisons : list, optional
        Labels for each comparison
    variable_name : str
        Name of the outcome variable (for title)
    save_name : str
        Filename to save (optional)
    """
    
    effect_sizes = np.array(effect_sizes)
    standard_errors = np.array(standard_errors)
    
    # Calculate summary effect (weighted mean)
    weights = 1 / (standard_errors ** 2)
    summary_effect = np.sum(weights * effect_sizes) / np.sum(weights)
    
    # Calculate precision (1/SE)
    precision = 1 / standard_errors
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # -------------------------------------------------------------------------
    # A. DRAW FUNNEL SHAPE
    # -------------------------------------------------------------------------
    # Calculate funnel boundaries (95% CI)
    max_precision = max(precision) * 1.2
    min_precision = 0
    
    se_range = np.linspace(0.01, max(standard_errors) * 1.3, 100)
    precision_range = 1 / se_range
    
    # 95% CI boundaries
    ci_left_95 = summary_effect - 1.96 * se_range
    ci_right_95 = summary_effect + 1.96 * se_range
    
    # 99% CI boundaries
    ci_left_99 = summary_effect - 2.58 * se_range
    ci_right_99 = summary_effect + 2.58 * se_range
    
    # Fill funnel regions
    ax.fill_betweenx(precision_range, ci_left_99, ci_right_99,
                     color='#f8f9fa', alpha=0.8, label='99% CI')
    ax.fill_betweenx(precision_range, ci_left_95, ci_right_95,
                     color='#e9ecef', alpha=0.8, label='95% CI')
    
    # Draw funnel lines
    ax.plot(ci_left_95, precision_range, color=LINE_COLOR, 
            linestyle='--', linewidth=1.5, alpha=0.7)
    ax.plot(ci_right_95, precision_range, color=LINE_COLOR, 
            linestyle='--', linewidth=1.5, alpha=0.7)
    ax.plot(ci_left_99, precision_range, color=LINE_COLOR, 
            linestyle=':', linewidth=1, alpha=0.5)
    ax.plot(ci_right_99, precision_range, color=LINE_COLOR, 
            linestyle=':', linewidth=1, alpha=0.5)
    
    # -------------------------------------------------------------------------
    # B. VERTICAL REFERENCE LINE (Summary Effect)
    # -------------------------------------------------------------------------
    ax.axvline(x=summary_effect, color=LINE_COLOR, linestyle='-',
               linewidth=2, alpha=0.8, label=f'Summary Effect ({summary_effect:.2f})')
    
    # Zero line
    ax.axvline(x=0, color='red', linestyle='--',
               linewidth=1.5, alpha=0.6, label='No Effect (0)')
    
    # -------------------------------------------------------------------------
    # C. PLOT DATA POINTS
    # -------------------------------------------------------------------------
    if p_values is not None:
        p_values = np.array(p_values)
        colors = [SIG_COLOR if p < 0.05 else NS_COLOR for p in p_values]
        
        # Plot significant points
        sig_mask = p_values < 0.05
        ax.scatter(effect_sizes[sig_mask], precision[sig_mask],
                   c=SIG_COLOR, s=120, edgecolors='black', linewidths=1.5,
                   zorder=5, label='p < .05')
        
        # Plot non-significant points
        ax.scatter(effect_sizes[~sig_mask], precision[~sig_mask],
                   c=NS_COLOR, s=120, edgecolors='black', linewidths=1.5,
                   zorder=5, label='p ≥ .05')
    else:
        ax.scatter(effect_sizes, precision,
                   c=NS_COLOR, s=120, edgecolors='black', linewidths=1.5,
                   zorder=5, label='Studies')
    
    # -------------------------------------------------------------------------
    # D. ADD POINT LABELS (Optional)
    # -------------------------------------------------------------------------
    if comparisons is not None:
        for i, (es, prec, comp) in enumerate(zip(effect_sizes, precision, comparisons)):
            # Only label if points are not too crowded
            ax.annotate(f'{i+1}', (es, prec),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=8, color='gray')
    
    # -------------------------------------------------------------------------
    # E. AXIS FORMATTING
    # -------------------------------------------------------------------------
    ax.set_xlabel("Effect Size (Mean Difference)", fontsize=AXIS_FONTSIZE, fontweight='bold')
    ax.set_ylabel("Precision (1/SE)", fontsize=AXIS_FONTSIZE, fontweight='bold')
    
    # Title
    title_prefix = f"{variable_name}: " if variable_name else ""
    ax.set_title(f"{title_prefix}Funnel Plot for Publication Bias Assessment",
                 fontsize=TITLE_FONTSIZE, fontweight='bold', pad=20)
    
    ax.tick_params(axis='both', labelsize=TICK_FONTSIZE)
    
    # Set axis limits
    x_margin = (max(effect_sizes) - min(effect_sizes)) * 0.3
    ax.set_xlim(min(effect_sizes) - x_margin - 1, max(effect_sizes) + x_margin + 1)
    ax.set_ylim(0, max(precision) * 1.2)
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # -------------------------------------------------------------------------
    # F. LEGEND
    # -------------------------------------------------------------------------
    ax.legend(loc='upper right', fontsize=9, framealpha=0.95)
    
    # -------------------------------------------------------------------------
    # G. ADD INTERPRETATION BOX
    # -------------------------------------------------------------------------
    interpretation_text = (
        "Interpretation Guide:\n"
        "• Symmetrical funnel → No publication bias\n"
        "• Asymmetry → Possible publication bias\n"
        "• Points outside funnel → Outliers/heterogeneity"
    )
    
    ax.text(0.02, 0.98, interpretation_text,
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment='top',
            fontfamily='sans-serif',
            bbox=dict(boxstyle='round', facecolor='white', 
                      edgecolor='gray', alpha=0.9))
    
    # -------------------------------------------------------------------------
    # H. EGGER'S TEST (Simple Approximation)
    # -------------------------------------------------------------------------
    # Calculate Egger's regression test for asymmetry
    if len(effect_sizes) >= 3:
        slope, intercept, r_value, p_value_egger, std_err = stats.linregress(
            standard_errors, effect_sizes
        )
        
        egger_text = (
            f"Egger's Test (approx.):\n"
            f"Intercept = {intercept:.3f}\n"
            f"p = {p_value_egger:.3f}"
        )
        
        if p_value_egger < 0.05:
            egger_text += "\n⚠ Potential asymmetry"
        else:
            egger_text += "\n✓ No significant asymmetry"
        
        ax.text(0.98, 0.02, egger_text,
                transform=ax.transAxes,
                fontsize=9,
                verticalalignment='bottom',
                horizontalalignment='right',
                fontfamily='sans-serif',
                bbox=dict(boxstyle='round', facecolor='lightyellow', 
                          edgecolor='gray', alpha=0.9))
    
    # -------------------------------------------------------------------------
    # I. SAVE AND SHOW
    # -------------------------------------------------------------------------
    plt.tight_layout()
    
    if save_name:
        plt.savefig(save_name, dpi=600, bbox_inches='tight')
        print(f"Figure saved as: {save_name}")
    
    plt.show()
    
    return fig, ax, summary_effect


# =============================================================================
# 4. RUN THE PLOT
# =============================================================================
if __name__ == "__main__":
    
    fig, ax, summary = create_funnel_plot(
        effect_sizes=effect_sizes,
        standard_errors=standard_errors,
        p_values=p_values,
        comparisons=comparisons,
        variable_name=VARIABLE_NAME,
        save_name="funnel_plot.png"
    )
    
    # Print summary
    print("\n" + "=" * 70)
    print("FUNNEL PLOT SUMMARY")
    print("=" * 70)
    print(f"\nSummary Effect (Weighted Mean): {summary:.3f}")
    print(f"Number of Comparisons: {len(effect_sizes)}")
    print("\n" + "-" * 70)
    print(f"{'#':<4} {'Comparison':<30} {'Effect':>8} {'SE':>8} {'p-value':>10}")
    print("-" * 70)
    
    for i, (comp, es, se, p) in enumerate(zip(
        comparisons, effect_sizes, standard_errors, p_values)):
        sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"{i+1:<4} {comp:<30} {es:>+8.2f} {se:>8.3f} {p:>9.3f}{sig}")
    
    print("=" * 70)
    print("* p < .05, ** p < .01, *** p < .001")
    print("\nNote: Assess funnel symmetry visually and with Egger's test.")


# =============================================================================
# USAGE INSTRUCTIONS:
# =============================================================================
#
# 1. Replace the data in Section 2 with your own values:
#    - VARIABLE_NAME: Your outcome measure name
#    - comparisons: Labels for each study/comparison
#    - effect_sizes: Mean differences from your analyses
#    - standard_errors: SE for each effect size
#    - p_values: P-values (optional, for color-coding)
#
# 2. Run the script:
#    python funnel_plot.py
#
# 3. Output: 'funnel_plot.png' at 600 DPI
#
# 4. Interpretation:
#    - Symmetrical funnel = No publication bias
#    - Asymmetrical funnel = Possible publication bias
#    - Egger's test p < .05 = Significant asymmetry
#
# =============================================================================
