# ============================================================================
# LIBRARY IMPORTS
# ============================================================================
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================================
# FUNCTION: CREATE COUNTRY DATAFRAMES
# ============================================================================
def create_country_dataframes(df_years, country_list):
    """
    Creates a dictionary of DataFrames — one per country.
    Each DataFrame retains all columns from the original dataset.
    """
    dataframes = {}
    for country in country_list:
        df_country = df_years[df_years['Country'] == country].copy()
        df_country = df_country.sort_values('Years').reset_index(drop=True)
        dataframes[country] = df_country
    return dataframes


# ============================================================================
# LATIN AMERICAN COUNTRIES
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

# Ensure 'Years' is numeric
df_years['Years'] = pd.to_numeric(df_years['Years'], errors='coerce')

# Create DataFrames for each country
dfs_countries = create_country_dataframes(df_years, latin_america)

# ============================================================================
# FUNCTION: PREPARE DATA FOR STACKED AREA CHART
# ============================================================================
def prepare_stacked_data(dfs_countries, indicator_column):

    data_stacked = pd.DataFrame()

    for country, df in dfs_countries.items():
        if indicator_column not in df.columns:
            continue
        series = df.set_index("Years")[indicator_column]
        series = pd.to_numeric(series, errors='coerce')
        data_stacked[country] = series

    # Sort by year, remove empty rows, and fill missing values with 0
    data_stacked = data_stacked.sort_index().dropna(how="all").fillna(0)
    return data_stacked

# ============================================================================
# DATA PREPARATION
# ============================================================================
indicator_column = 'All ages.1'
df_stacked = prepare_stacked_data(dfs_countries, indicator_column=indicator_column)
df_stacked = df_stacked.loc[:, (df_stacked != 0).any(axis=0)]
# ============================================================================
# STACKED AREA CHART
# ============================================================================
fig, ax = plt.subplots(figsize=(18, 10))

color_palette = [
    '#1f77b4',  # Azul fuerte - Brazil (mayor contribución)
    '#ff7f0e',  # Naranja intenso - Mexico
    '#2ca02c',  # Verde brillante - Colombia
    '#d62728',  # Rojo intenso - Chile
    '#9467bd',  # Púrpura - Peru
    '#8c564b',  # Marrón - Haiti
    '#e377c2',  # Rosa fuerte - Dominican Republic
    '#7f7f7f',  # Gris medio - Ecuador
    '#bcbd22',  # Verde lima - Cuba
    '#17becf',  # Cian - El Salvador
    '#393b79',  # Azul marino - Honduras
    '#637939',  # Verde oliva - Suriname
    '#8c6d31',  # Marrón dorado - Guyana
    '#843c39',  # Rojo ladrillo - Belize
    '#d6616b',  # Rosa salmón - Bahamas
    '#5254a3'   # Azul lavanda - Paraguay
]

df_stacked.plot.area(
    ax=ax,
    stacked=True,
    alpha=0.8,
    linewidth=0.5,
    color=color_palette
)

# ============================================================================
# CHART CUSTOMIZATION
# ============================================================================
ax.set_title(
    'Evolución del Número de Personas con VIH y Carga Viral Suprimida\n'
    'en Países de Latinoamérica y el Caribe (2010–2024)',
    fontsize=20, fontweight='bold', pad=20
)
ax.set_xlabel('Año', fontsize=14, fontweight='bold')
ax.set_ylabel('Número de personas viviendo con VIH con carga viral suprimida',
              fontsize=14, fontweight='bold')

# Legend configuration
ax.legend(
    title='Países',
    bbox_to_anchor=(1.02, 1),
    loc='upper left',
    frameon=True,
    fontsize=10,
    title_fontsize=12
)

# Grid and formatting
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
ax.set_axisbelow(True)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

plt.tight_layout()

# ============================================================================
# SAVE & SHOW
# ============================================================================
plt.savefig('Evolucion_VIH_Latam_2010_2024.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
