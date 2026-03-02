import plotly.graph_objects as go
import geopandas as gpd
import json
from processing.summary import trend_summary

def build_interactive_toggle_map():
    """Create a Plotly mapbox with a UI layer toggle."""
    
    # Load the gpkg file.
    regions = (gpd.read_file("data/geography/uk_regions.gpkg")
              .to_crs(epsg=4326)
    )

    # Convert the Polars summary into a Pandas DataFrame 
    # so it is compatible with Plotly/Dash.
    summary = trend_summary().to_pandas()

    merged = regions.merge(
        summary,
        left_on="nuts118cd",
        right_on="region_code",
        how="left"
    )
    
    # Convert the GeoDataFrame 
    # into a GeoJSON formatted dictionary for Plotlys mapping engine.
    geojson = json.loads(merged.to_json())

    fig = go.Figure()

    # Population layer
    fig.add_choroplethmapbox(
        geojson=geojson,
        locations=merged["nuts118cd"],
        featureidkey="properties.nuts118cd",
        z=merged["population"],
        colorscale="Viridis",
        colorbar=dict(title="Population"),
        hovertext=merged["nuts118nm"],
        hovertemplate="<b>%{hovertext}</b><br>Population: %{z:,}<extra></extra>",
        visible=True,
        marker=dict(opacity=0.7)
    )

    # Percentage change layer
    fig.add_choroplethmapbox(
        geojson=geojson,
        locations=merged["nuts118cd"],
        featureidkey="properties.nuts118cd",
        z=merged["pct_change"],
        colorscale="RdBu",
        colorbar=dict(title="% Change"),
        hovertext=merged["nuts118nm"],
        hovertemplate="<b>%{hovertext}</b><br>% Change: %{z:.3f}%<extra></extra>",
        visible=False,
        marker=dict(opacity=0.7)
    )
    
    # Configure map (centered on the UK.) 
    # Styled with interactive layer and switch buttons.
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=5,
        mapbox_center={"lat": 55.5, "lon": -2},
        height=800,
        margin={"r":0, "t":0, "l":0, "b":0},
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": "Population",
                        "method": "update",
                        "args": [{"visible": [True, False]}]
                    },
                    {
                        "label": "% Change",
                        "method": "update",
                        "args": [{"visible": [False, True]}]
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 10},
                "showactive": True,
                "type": "buttons",
                "x": 0.1,
                "y": 1.05
            }
        ]
    )

    return fig