import matplotlib.pyplot as plt
import numpy as np

# Set style for professional charts
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, axes = plt.subplots(2, 3, figsize=(15, 9), sharey=True)
axes = axes.flatten()

# Data structure
# Grades: 1, 2, 3, 4, 5, Overall
grades = ["1° Grado", "2° Grado", "3° Grado", "4° Grado", "5° Grado", "Promedio General"]

# Diagnostic percentages: [AD/A, B, C]
diag_data = {
    "1° Grado": [0, 25, 75],
    "2° Grado": [48, 52, 0],
    "3° Grado": [75, 25, 0],
    "4° Grado": [72, 28, 0],
    "5° Grado": [76, 24, 0],
    "Promedio General": [54.2, 30.8, 15.0]
}

# I Bimester percentages: [AD/A, B, C]
ibim_data = {
    "1° Grado": [57.81, 42.19, 0.0],
    "2° Grado": [34.55, 60.00, 5.45],
    "3° Grado": [62.79, 34.88, 2.33],
    "4° Grado": [51.92, 46.15, 1.92],
    "5° Grado": [75.00, 25.00, 0.0],
    "Promedio General": [56.02, 42.11, 1.88]
}

categories = ["Logro AD/A", "Proceso (B)", "Inicio (C)"]
x = np.arange(len(categories))
width = 0.35

# Color scheme
color_diag = "#a0aec0" # Cool gray for baseline
color_ibim = "#2b6cb0" # Strong professional blue for achievement

for i, grade in enumerate(grades):
    ax = axes[i]
    
    # Draw bars
    rects1 = ax.bar(x - width/2, diag_data[grade], width, label='Eval. Diagnóstica', color=color_diag, edgecolor='black', linewidth=0.5)
    rects2 = ax.bar(x + width/2, ibim_data[grade], width, label='I Bimestre', color=color_ibim, edgecolor='black', linewidth=0.5)
    
    # Add values on top of bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(f'{height:.1f}%',
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=8, fontweight='bold')

    autolabel(rects1)
    autolabel(rects2)
    
    # Titles and formatting
    ax.set_title(grade, fontsize=12, fontweight='bold', pad=10, color="#2d3748")
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9, fontweight='semibold')
    ax.set_ylim(0, 110)
    
    if i % 3 == 0:
        ax.set_ylabel('Porcentaje (%)', fontsize=10, fontweight='semibold')
        
    if i == 0:
        ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none')

plt.suptitle("Comparativa de Logros de Aprendizaje: Evaluación Diagnóstica vs. I Bimestre 2026\nÁrea: Educación para el Trabajo (EPT)", fontsize=16, fontweight='bold', y=0.98, color="#1a365d")
plt.tight_layout()
plt.subplots_adjust(top=0.88)
plt.savefig("comparativa_logros.png", dpi=300)
print("Chart generated successfully and saved as 'comparativa_logros.png'")
