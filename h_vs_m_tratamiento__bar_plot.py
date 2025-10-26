# ============================================================================
# LIBRARY IMPORTS
# ============================================================================
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

        # Include only valid data
        if not (pd.isna(men) or pd.isna(women)):
            records_2024.append({
                'País': country,
                'Sexo': 'Hombres (15+ años)',
                'Valor': men
            })
            records_2024.append({
                'País': country,
                'Sexo': 'Mujeres (15+ años)',
                'Valor': women
            })

# Create summary DataFrame
df_2024 = pd.DataFrame(records_2024)

# Sort countries by male values for visual clarity
order = (
    df_2024[df_2024['Sexo'] == 'Hombres (15+ años)']
    .sort_values('Valor', ascending=False)['País']
)
df_2024['País'] = pd.Categorical(df_2024['País'], categories=order, ordered=True)

# ============================================================================
# SEABORN GROUPED BAR CHART
# ============================================================================
plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid")

ax = sns.barplot(
    data=df_2024,
    x='País',
    y='Valor',
    hue='Sexo',
    palette=['steelblue', 'lightcoral']
)

# Customize the plot
ax.set_title('Comparación del VIH en Hombres y Mujeres (15+) - Año 2024',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('País', fontsize=12)
ax.set_ylabel('Número de casos / prevalencia', fontsize=12)

# Rotate x labels
plt.xticks(rotation=45, ha='right')

# Add gridlines and legend
ax.legend(title='Grupos por sexo', fontsize=10, title_fontsize=11)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Format y-axis with thousands separator
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda y, _: f'{int(y):,}'))

plt.tight_layout()

# ============================================================================
# SAVE & SHOW
# ============================================================================
plt.savefig("VIH_Hombres_Mujeres_2024_Seaborn.png", dpi=300, bbox_inches='tight')
plt.show()
