import plotly.express as px

from processing.load_population import load_population_snapshots


def population_line_chart():
    """Generate a time series line chart for regional population trends."""

    # Load data from MongoDB
    df = load_population_snapshots()

    # Sort by date to ensure the lines draw chronologically
    # Use both region and date for a perfectly ordered dataframe
    df = df.sort(["region_name", "date"])
    
    # Convert to Pandas for Plotly compatibility
    df_pandas = df.to_pandas()

    # Generate the line chart
    fig = px.line(
        df_pandas,
        x="date",
        y="population",
        color="region_name",
        markers=True,
        title="Historical Population Growth",
        template="plotly_dark"
    )

    # Apply global styling and Legend fixes
    fig.update_layout(
        paper_bgcolor="#2c2c2e",  # Matches dashboard card background
        plot_bgcolor="#2c2c2e",   # Matches inner chart background
        font={
            "family":"'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
            "size": 14,
            "color": "#ecf0f1"
        },
        legend={
            "title_text": "UK Regions",
            "font": {"size": 12, "color": "#ecf0f1"},
            "bgcolor": "rgba(26, 26, 27, 0.8)",  # Dark gray with slight transparency
            "bordercolor": "#3a3a3c",
            "borderwidth": 1,
        },
        margin={"l": 40, "r": 40, "t": 60, "b": 40},
        hovermode="closest",  # Shows all regional data in one tooltip on hover
        hoverlabel={
            "bgcolor": "#1a1a1b",
            "font_size": 12,
            "font_color": "#0d19f4",
            "bordercolor": "#3498db",
        },
    )

    # Update Axes
    fig.update_xaxes(
        title_font={"size": 14, "color": "#3498db"},
        tickfont={"family": "'Segoe UI'", "size": 12, "color": "#bdc3c7"},
        gridcolor="#3a3a3c",
    )

    fig.update_yaxes(
        title_font={"size": 14, "color": "#3498db"},
        tickfont={"family": "'Segoe UI'", "size": 12, "color": "#bdc3c7"},
        gridcolor="#3a3a3c",
        tickformat=",.0f",  # Adds commas to population numbers (e.g., 10,000,000)
    )
    
    return fig

if __name__ == "__main__":

    # Test run to see if it generates without errors
    chart = population_line_chart()
    chart.show()