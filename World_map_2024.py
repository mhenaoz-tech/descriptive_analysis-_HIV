# ============================================================================
# LIBRARIES IMPORT
# ============================================================================
import pandas as pd
import plotly.express as px

# ============================================================================
# DATA LOADING AND CONFIGURATION
# ============================================================================

# Excel file path containing HIV data
file_path = "HIV_estimates_from_1990-to-2025.xlsx"

# Read Excel sheets
df_years = pd.read_excel(file_path, sheet_name=1, header=0)

# ============================================================================
# FILTERING DATA FOR A SPECIFIC YEAR
# ============================================================================

# Ensure 'Years' is numeric
df_years['Years'] = pd.to_numeric(df_years['Years'], errors='coerce')

# Target year
target_year = 2024

# Filter global data for the selected year
df_global = df_years[df_years['Years'] == target_year].copy()

# Remove potential header row or repeated header line
df_global = df_global.iloc[1:].reset_index(drop=True)

# Select indicator column
indicator_column = 'All ages'

# Convert indicator column to numeric
df_global[indicator_column] = pd.to_numeric(df_global[indicator_column], errors='coerce')

# Keep only valid countries (non-null values)
df_clean = df_global[['Country', 'Code', indicator_column]].dropna()

# ============================================================================
# CREATE CHOROPLETH MAP WITH PLOTLY
# ============================================================================

fig = px.choropleth(
    df_clean,
    locations='Code',                        # ISO country codes
    color=indicator_column,                  # Value to color by
    hover_name='Country',                    # Hover label
    hover_data={indicator_column: ':.2f', 'Code': False},
    color_continuous_scale='YlGn',           # Color scale
    labels={indicator_column: 'Valor'},      # Color bar label
    title=f'Mapa Mundial de VIH - Año {target_year}'
)

# Configure map appearance
fig.update_geos(
    projection_type='robinson',
    showcoastlines=True,
    coastlinecolor='white',
    showland=True,
    landcolor='lightgray',
    showocean=True,
    oceancolor='lightblue',
    showcountries=True,
    countrycolor='white'
)

# Layout settings
fig.update_layout(
    title={
        'text': f'<b>Distribución Mundial de personas que viven con VIH y conocen su condición - {target_year}</b>',  # ← agrega <b> </b> para negrilla
        'x': 0.5,               # mantiene el centrado (0.5 = centro exacto)
        'xanchor': 'center',    # asegura que se ancle al centro
        'y': 0.95,              # opcional: eleva un poco el título
        'font': {'size': 24, 'family': 'Arial, sans-serif'}  # ← aumenta tamaño (por ejemplo 24)
    },
    geo=dict(showframe=False, showcoastlines=True),
    height=600,
    margin=dict(l=0, r=0, t=80, b=0)
)

# ============================================================================
# EXPORT AND DISPLAY
# ============================================================================

fig.show()

# Save as HTML (interactive)
fig.write_html(f'mapa_mundial_hiv_{target_year}.html')

# Save as PNG (static)
fig.write_image(f'mapa_mundial_hiv_{target_year}.png', width=1920, height=1080)
