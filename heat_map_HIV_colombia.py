# ============================================================================
# LIBRARY IMPORTS
# ============================================================================
import pandas as pd                          # Data manipulation
import matplotlib.pyplot as plt              # Visualization
import seaborn as sns                        # Statistical visualizations
from sklearn.preprocessing import StandardScaler  # Data normalization

# ============================================================================
# DATA LOADING AND PREPARATION
# ============================================================================

# File path for the HIV dataset
file_path = "HIV_estimates_from_1990-to-2025.xlsx"

# Read Excel sheets
# sheet_name=1: second sheet (yearly data)
df_years = pd.read_excel(file_path, sheet_name=1, header=0)
df_area = pd.read_excel(file_path, sheet_name=2, header=0)

# Filter only data from Colombia
df_colombia = df_years[df_years['Country'] == 'Colombia'].copy()

# ============================================================================
# DATA SELECTION FOR HEATMAP
# ============================================================================

# Select specific indicator columns to visualize
selected_columns = [
    '(All ages)',      # % of people living with HIV who know their status
    '(All ages).1',    # % on antiretroviral treatment
    '(All ages).2',    # % who know status and are on treatment
    '(All ages).3',    # % with suppressed viral load
    '(All ages).4'     # % on treatment with suppressed viral load
]

# Create a DataFrame containing only selected columns
df_heatmap = df_colombia[selected_columns].copy()

# Convert all values to numeric (invalid entries become NaN)
df_heatmap = df_heatmap.apply(pd.to_numeric, errors='coerce')

# Fill missing values with column means (avoids white gaps in heatmap)
df_heatmap = df_heatmap.fillna(df_heatmap.mean())

# ============================================================================
# DATA NORMALIZATION
# ============================================================================

# Apply Z-score normalization for comparability across indicators
scaler = StandardScaler()
df_normalized = pd.DataFrame(
    scaler.fit_transform(df_heatmap),
    columns=df_heatmap.columns
)

# ============================================================================
# RENAME COLUMNS FOR PRESENTATION
# ============================================================================

# More descriptive indicator names (in Spanish for figure labels)
column_names = {
    '(All ages)': 'Porcentaje de personas que viven con VIH\nque conocen su condición',
    '(All ages).1': 'Porcentaje de personas que viven con VIH\ny están en tratamiento antirretroviral',
    '(All ages).2': 'Porcentaje de personas que viven con VIH\nque conocen su condición\ny están en tratamiento antirretroviral',
    '(All ages).3': 'Porcentaje de personas que viven con VIH\ncon carga viral suprimida',
    '(All ages).4': 'Porcentaje de personas que viven con VIH\nen tratamiento con carga viral suprimida'
}

df_normalized = df_normalized.rename(columns=column_names)

# Set years as index and transpose the DataFrame for plotting
df_normalized.index = df_colombia['Years'].values
df_normalized = df_normalized.T

# ============================================================================
# HEATMAP CREATION
# ============================================================================

plt.figure(figsize=(16, 8))
sns.heatmap(
    df_normalized,
    annot=False,
    cmap='coolwarm',
    center=0,
    linewidths=0.7,
    linecolor='#333333',
    cbar_kws={'label': 'Valores Normalizados'},
    vmin=-2,
    vmax=2,
    square=False
)

# ============================================================================
# AXIS AND BORDER CONFIGURATION
# ============================================================================

ax = plt.gca()

# Ensure all borders are visible and styled
for side in ['top', 'right', 'bottom', 'left']:
    ax.spines[side].set_visible(True)
    ax.spines[side].set_color('black')

# ============================================================================
# TITLES AND LABELS
# ============================================================================

plt.title(
    'Mapa de Calor - Colombia VIH (por Año)',
    fontsize=16,
    pad=20,
    fontweight='bold'
)
plt.xlabel('Años', fontsize=12, fontweight='bold')

plt.xticks(rotation=90, ha='center', fontsize=9)
plt.yticks(fontsize=10, rotation=0)

# Adjust layout to avoid clipping
plt.tight_layout()

# ============================================================================
# SAVE AND DISPLAY
# ============================================================================

# Save figure as high-quality PNG
plt.savefig(
    'mapa_calor_colombia_vih.png',
    dpi=300,
    bbox_inches='tight',
    facecolor='white'
)

# Display plot
plt.show()
