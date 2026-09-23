import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Headless backend for web server compatibility
import matplotlib.pyplot as plt

def generate_comparative_chart(json_path="evaluaciones_2026.json", output_image="comparativa_logros.png", periods_to_compare=None):
    """
    Generates a high-resolution comparative bar chart for requested evaluation periods across all 5 grades & overall average.
    """
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return False
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    available_periods = data.get("meta", {}).get("periodos_disponibles", ["Diagnóstica", "I Bimestre"])
    
    if periods_to_compare is None:
        periods = available_periods
    else:
        periods = [p for p in periods_to_compare if p in available_periods or p in data["grados"]["1° Grado"]]

    if not periods:
        periods = available_periods

    # Grades configuration
    grades = ["1° Grado", "2° Grado", "3° Grado", "4° Grado", "5° Grado", "Promedio General"]
    categories = ["Logro (AD/A)", "Proceso (B)", "Inicio (C)"]
    
    # Palette map for different periods
    period_colors = {
        "Diagnóstica": "#94A3B8",   # Slate Gray
        "I Bimestre": "#2563EB",    # Vivid Royal Blue
        "II Bimestre": "#0D9488",   # Deep Teal
        "III Bimestre": "#D97706",  # Warm Amber
        "IV Bimestre": "#059669"    # Emerald Green
    }

    # Setup matplotlib figure
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, axes = plt.subplots(2, 3, figsize=(16, 9.5), sharey=True)
    axes = axes.flatten()

    x = np.arange(len(categories))
    num_periods = len(periods)
    total_bar_width = 0.75
    bar_width = total_bar_width / num_periods

    for i, grade in enumerate(grades):
        ax = axes[i]
        grade_data = data["grados"].get(grade, {})
        
        for p_idx, period in enumerate(periods):
            p_stats = grade_data.get(period, {"pct_AD_A": 0, "pct_B": 0, "pct_C": 0})
            values = [p_stats.get("pct_AD_A", 0), p_stats.get("pct_B", 0), p_stats.get("pct_C", 0)]
            
            # Position offset
            offset = (p_idx - (num_periods - 1) / 2.0) * bar_width
            color = period_colors.get(period, "#475569")
            
            rects = ax.bar(x + offset, values, bar_width, label=period if i == 0 else "", color=color, edgecolor="black", linewidth=0.5)
            
            # Annotate values
            for rect in rects:
                height = rect.get_height()
                if height > 0:
                    ax.annotate(f'{height:.1f}%',
                                xy=(rect.get_x() + rect.get_width() / 2, height),
                                xytext=(0, 2),
                                textcoords="offset points",
                                ha='center', va='bottom', fontsize=7.5, fontweight='bold')

        # Formatting
        ax.set_title(grade, fontsize=12, fontweight='bold', pad=10, color="#1E293B")
        ax.set_xticks(x)
        ax.set_xticklabels(categories, fontsize=9, fontweight='semibold')
        ax.set_ylim(0, 115)
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        if i % 3 == 0:
            ax.set_ylabel('Porcentaje de Estudiantes (%)', fontsize=10, fontweight='semibold')

    # Global Legend and Title
    fig.legend(loc='upper right', bbox_to_anchor=(0.98, 0.96), frameon=True, facecolor='white', edgecolor='#CBD5E1', fontsize=10)
    
    ano_academico = data.get("meta", {}).get("ano_academico", 2026)
    title_periods = " vs. ".join(periods)
    plt.suptitle(f"Comparativa de Logros de Aprendizaje: {title_periods} (Año {ano_academico})\nÁrea: Educación para el Trabajo (EPT)",
                 fontsize=15, fontweight='bold', y=0.98, color="#0F172A")

    plt.tight_layout()
    plt.subplots_adjust(top=0.88, hspace=0.3, wspace=0.15)
    
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Chart generated successfully: {output_image}")
    return True

if __name__ == "__main__":
    generate_comparative_chart()
