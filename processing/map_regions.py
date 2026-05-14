import matplotlib
matplotlib.use("Agg")
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def load_nuts1_geography():
    """Load the UK Nuts1 geography from the GEO Package."""

    gdf = gpd.read_file("data/geography/uk_regions.gpkg")
    return gdf

def add_labels(ax, gdf, value_column):
    """Adds text labels to the map centroids."""

    for _, row in gdf.iterrows():
        centroid = row.geometry.centroid
        label = f"{row['nuts118nm']}\n{row[value_column]:.2f}%"
        # Using white for labels to ensure they stand out on the colored regions
        ax.text(
            centroid.x,
            centroid.y,
            label,
            fontsize=8,
            ha="center",
            va="center",
            color="white",
            fontweight="bold"
        )

def apply_dark_theme():
    """Helper to set matplotlib global colors to match Silver/Dark theme."""

    plt.rcParams.update({
        'text.color': "#bdc3c7",
        'axes.labelcolor': "#bdc3c7",
        'xtick.color': "#bdc3c7",
        'ytick.color': "#bdc3c7",
        'figure.facecolor': 'none', # Ensures transparency works well
        'axes.facecolor': 'none'
    })

def plot_population_map():
    """Renders the choropleth map using GeoJSON boundaries and MongoDB data."""

    from processing.summary import trend_summary

    apply_dark_theme()

    regions = gpd.read_file("data/geography/uk_regions.gpkg").to_crs(epsg=4326)
    summary = trend_summary().to_pandas()

    merged = regions.merge(
        summary,
        left_on="nuts118cd",
        right_on="region_code",
        how="left"
    )

    # We create the ax first so we can turn off the coordinates correctly
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    def millions_formatter_func(x, pos):
        return f"{x*1e-6:.1f}M"

        merged.plot(
        column="population",
        cmap="viridis",
        legend=True,
        ax=ax,
        edgecolor="black",
        linewidth=0.5,
        legend_kwds={
            "label": "Population (Millions)",
            "orientation": "vertical",
            "format": FuncFormatter(millions_formatter_func)
        }
    )

def plot_population_change_map():
    """Renders a heatmap of UK population growth/decline percentages."""

    from processing.summary import trend_summary
    apply_dark_theme()

    regions = gpd.read_file("data/geography/uk_regions.gpkg").to_crs(epsg=4326)
    summary = trend_summary().to_pandas()

    merged = regions.merge(
        summary,
        left_on="nuts118cd",
        right_on="region_code",
        how="left"
    )

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    merged.plot(
        column="change",
        cmap="coolwarm",
        legend=True,
        ax=ax,
        edgecolor="black",
        linewidth=0.5,
        legend_kwds={"label": "Net Change in People"}
    )

    ax.set_axis_off()
    plt.title("UK Population Chart - Region Changes", fontsize=15, pad=20)
    
    plt.savefig("app/static/images/population_change_map.png", 
                dpi=150, bbox_inches="tight", transparent=True)
    plt.close()

def plot_percentage_change_map():
    """Renders a choropleth map highlighting population growth/decline."""

    from processing.summary import trend_summary
    
    apply_dark_theme()

    regions = gpd.read_file("data/geography/uk_regions.gpkg").to_crs(epsg=4326)
    summary = trend_summary().to_pandas()

    merged = regions.merge(
        summary,
        left_on="nuts118cd",
        right_on="region_code",
        how="left"
    )

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    merged.plot(
        column="pct_change",
        cmap="coolwarm",
        legend=True,
        ax=ax,
        edgecolor="black",
        linewidth=0.5,
        legend_kwds={"label": "% Growth / Decline"}
    )
    
    ax.set_axis_off()
    add_labels(ax, merged, "pct_change")

    plt.title("UK Population Percentage Change", fontsize=15, pad=20)
    plt.savefig("app/static/images/percentage_change_map.png", 
                dpi=150, bbox_inches="tight", transparent=True)
    plt.close()

if __name__ == "__main__":
    plot_population_map()
    plot_population_change_map()
    plot_percentage_change_map()