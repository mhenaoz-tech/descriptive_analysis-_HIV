# ============================================================================
# LIBRARY IMPORTS
# ============================================================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================
# DATA LOADING
# ============================================================================
file_path = "HIV_estimates_from_1990-to-2025.xlsx"

# Load data from Excel
df_years = pd.read_excel(file_path, sheet_name=1, header=0)

# Filter data for Colombia
df_colombia = df_years[df_years['Country'] == 'Colombia'].copy()

# ============================================================================
# DATA PREPARATION
# ============================================================================
# Convert columns to numeric
df_colombia['Years'] = pd.to_numeric(df_colombia['Years'], errors='coerce')
df_colombia['Unnamed: 43'] = pd.to_numeric(df_colombia['Unnamed: 43'], errors='coerce')
df_colombia['Effective regimen'] = pd.to_numeric(df_colombia['Effective regimen'], errors='coerce')

# Sort data by year
df_colombia = df_colombia.sort_values('Years')

# ============================================================================
# SEABORN STYLING
# ============================================================================
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 7))

# ============================================================================
# LINE PLOTS
# ============================================================================
# Línea 1: Necesidad de tratamiento
sns.lineplot(
    data=df_colombia,
    x='Years', y='Unnamed: 43',
    color='red', linewidth=2.5, label='Personas que necesitan tratamiento'
)

# Línea 2: Tratamiento efectivo
sns.lineplot(
    data=df_colombia,
    x='Years', y='Effective regimen',
    color='green', linewidth=2.5, label='Personas en tratamiento efectivo'
)

# ============================================================================
# GAP (BRECHA) AREA
# ============================================================================
# Rellenar el área entre las dos líneas
plt.fill_between(
    df_colombia['Years'],
    df_colombia['Unnamed: 43'],
    df_colombia['Effective regimen'],
    where=(df_colombia['Unnamed: 43'] > df_colombia['Effective regimen']),
    color='lightcoral',
    alpha=0.4,
    label='Brecha (personas sin acceso)'
)

# ============================================================================
# STYLING
# ============================================================================
plt.title(
    'Brecha entre necesidad y tratamiento efectivo de VIH en Colombia (2010–2025)',
    fontsize=16, fontweight='bold', pad=20
)
plt.xlabel('Año', fontsize=12, fontweight='bold')
plt.ylabel('Número de personas', fontsize=12, fontweight='bold')

# Grid y leyenda
plt.grid(alpha=0.3, linestyle='--')
plt.legend(title='Indicadores', fontsize=10, title_fontsize=11, loc='upper left')

# Formatear eje Y con separadores de miles
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Ajustar márgenes
plt.tight_layout()

# ============================================================================
# SAVE & SHOW
# ============================================================================
plt.savefig("brecha_tratamiento_VIH_Colombia_Seaborn.png", dpi=300, bbox_inches='tight')
plt.show()
