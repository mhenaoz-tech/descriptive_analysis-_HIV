# ============================================================================
# LIBRARY IMPORTS
# ============================================================================
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# FUNCTION: CREATE COUNTRY DATAFRAMES
# ============================================================================
def create_country_dataframes(df_years, country_list):

    dataframes = {}
    for country in country_list:
        df_country = df_years[df_years['Country'] == country].copy()
        df_country = df_country.sort_values('Years').reset_index(drop=True)
        dataframes[country] = df_country
    return dataframes


# ============================================================================
# LATIN AMERICA COUNTRIES
# ============================================================================
latin_america = [
    'Mexico', 'Belize', 'Honduras', 'El Salvador', 'Costa Rica',
    'Cuba', 'Bahamas', 'Haiti', 'Dominican Republic',
    'Colombia', 'Venezuela', 'Guyana', 'Suriname',
    'Ecuador', 'Peru', 'Brazil', 'Paraguay', 'Chile', 'Argentina'
]

# ============================================================================
# DATA LOADING
# ============================================================================
file_path = "HIV_estimates_from_1990-to-2025.xlsx"
df_years = pd.read_excel(file_path, sheet_name=1, header=0)

# Ensure numeric years
df_years['Years'] = pd.to_numeric(df_years['Years'], errors='coerce')

# Create a DataFrame for each country
dfs_countries = create_country_dataframes(df_years, latin_america)

# ============================================================================
# FILTER DATA FOR YEAR 2024
# ============================================================================
target_year = 2024
records_2024 = []

for country, df_country in dfs_countries.items():
    df_filtered = df_country[df_country['Years'] == target_year]
    if not df_filtered.empty:
        men = pd.to_numeric(df_filtered['(Men, ages 15+).6'].values[0], errors='coerce')
        women = pd.to_numeric(df_filtered['(Women, ages 15+).6'].values[0], errors='coerce')

        # Include only countries with valid data
        if not (pd.isna(men) or pd.isna(women)):
            records_2024.append({
                'País': country,
                'Hombres (15+)': men,
                'Mujeres (15+)': women
            })

# Create summary DataFrame
df_2024 = pd.DataFrame(records_2024)

# Sort by number of men (for visual clarity)
df_2024 = df_2024.sort_values('Hombres (15+)', ascending=False).reset_index(drop=True)

# ============================================================================
# GROUPED BAR CHART
# ============================================================================
plt.figure(figsize=(14, 7))
x = np.arange(len(df_2024['País']))
bar_width = 0.35

plt.bar(x - bar_width/2, df_2024['Hombres (15+)'], width=bar_width, color='steelblue', label='Hombres (15+ años)')
plt.bar(x + bar_width/2, df_2024['Mujeres (15+)'], width=bar_width, color='lightcoral', label='Mujeres (15+ años)')

plt.title('Comparación del VIH en Hombres y Mujeres (15+) - Año 2024',
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('País', fontsize=12)
plt.ylabel('Número de casos / prevalencia', fontsize=12)
plt.xticks(x, df_2024['País'], rotation=45, ha='right')
plt.legend(title='Grupos por sexo', fontsize=10)
plt.grid(axis='y', alpha=0.3, linestyle='--')

# Format y-axis with thousands separator
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y):,}'))

plt.tight_layout()

# ============================================================================
# SAVE & DISPLAY
# ============================================================================
plt.savefig("VIH_Hombres_Mujeres_2024.png", dpi=300, bbox_inches='tight')
plt.show()
