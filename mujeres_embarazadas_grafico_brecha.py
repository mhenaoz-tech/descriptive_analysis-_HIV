# ============================================================================
# LIBRARY IMPORTS
# ============================================================================
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================================
# DATA LOADING
# ============================================================================
file_path = "HIV_estimates_from_1990-to-2025.xlsx"

# Load relevant sheets
df_years = pd.read_excel(file_path, sheet_name=1, header=0)
df_area = pd.read_excel(file_path, sheet_name=2, header=0)

# Filter for Colombia
df_colombia = df_years[df_years['Country'] == 'Colombia'].copy()

# ============================================================================
# DATA PREPARATION
# ============================================================================
# Convert key columns to numeric (ignore errors)
df_colombia['Years'] = pd.to_numeric(df_colombia['Years'], errors='coerce')
df_colombia['Unnamed: 43'] = pd.to_numeric(df_colombia['Unnamed: 43'], errors='coerce')
df_colombia['Effective regimen'] = pd.to_numeric(df_colombia['Effective regimen'], errors='coerce')

# Sort by year
df_colombia = df_colombia.sort_values('Years')

# ============================================================================
# PLOT: GAP BETWEEN NEED AND EFFECTIVE TREATMENT
# ============================================================================
plt.figure(figsize=(12, 7))

# Main lines
plt.plot(df_colombia['Years'], df_colombia['Unnamed: 43'],
         color='red', linewidth=2.5, label='Mujeres que necesitan tratamiento')

plt.plot(df_colombia['Years'], df_colombia['Effective regimen'],
         color='green', linewidth=2.5, label='Mujeres en tratamiento efectivo')

# Fill the gap area
plt.fill_between(df_colombia['Years'],
                 df_colombia['Unnamed: 43'],
                 df_colombia['Effective regimen'],
                 where=(df_colombia['Unnamed: 43'] > df_colombia['Effective regimen']),
                 color='lightcoral', alpha=0.4,
                 label='Brecha (personas sin acceso)',
                 )

# ============================================================================
# STYLING
# ============================================================================
plt.title('Brecha entre necesidad y tratamiento efectivo de VIH en Colombia (2010–2025)',
          fontsize=15, fontweight='bold', pad=20)

plt.xlabel('Año', fontsize=12, fontweight='bold')
plt.ylabel('Número de personas', fontsize=12, fontweight='bold')

plt.legend(title='Indicadores', fontsize=10, title_fontsize=11, loc='upper left')
plt.grid(alpha=0.3, linestyle='--')

# Format Y axis with thousands separator
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Layout adjustments
plt.tight_layout()

# ============================================================================
# SAVE & DISPLAY
# ============================================================================
plt.savefig("brecha_tratamiento_VIH_Colombia.png", dpi=300, bbox_inches='tight')
plt.show()
