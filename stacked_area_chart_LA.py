# ============================================================================
# LIBRARY IMPORTS
# ============================================================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    """
    Combines individual country DataFrames into one table
    with 'Years' as the index and countries as columns.
    """
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

# Remove countries with all-zero data
df_stacked = df_stacked.loc[:, (df_stacked != 0).any(axis=0)]

# Reset index to use in Seaborn
df_long = df_stacked.reset_index().melt(id_vars='Years', var_name='País', value_name='Valor')

# ============================================================================
# SEABORN STYLING
# ============================================================================
sns.set_theme(style="whitegrid")
palette = sns.color_palette("Spectral", n_colors=len(df_long['País'].unique()))

# ============================================================================
# STACKED AREA CHART USING SEABORN STYLE + MATPLOTLIB
# ============================================================================
plt.figure(figsize=(18, 10))

# Crear el gráfico apilado manualmente
for i, country in enumerate(df_stacked.columns):
    plt.fill_between(
        df_stacked.index,
        df_stacked.iloc[:, :i+1].sum(axis=1),
        df_stacked.iloc[:, :i].sum(axis=1),
        label=country,
        color=palette[i],
        alpha=0.8,
        linewidth=0.5
    )

# ============================================================================
# CUSTOMIZATION
# ============================================================================
plt.title(
    'Evolución del Número de Personas con VIH y Carga Viral Suprimida\n'
    'en Países de Latinoamérica y el Caribe (2010–2024)',
    fontsize=20, fontweight='bold', pad=20
)
plt.xlabel('Año', fontsize=14, fontweight='bold')
plt.ylabel('Número de personas viviendo con VIH con carga viral suprimida', fontsize=14, fontweight='bold')

# Legend
plt.legend(
    title='Países',
    bbox_to_anchor=(1.02, 1),
    loc='upper left',
    frameon=True,
    fontsize=10,
    title_fontsize=12
)

# Grid and format
plt.grid(alpha=0.3, linestyle='--', linewidth=0.5)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.tight_layout()

# ============================================================================
# SAVE & SHOW
# ============================================================================
plt.savefig('Evolucion_VIH_Latam_2010_2024_Seaborn.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.show()
