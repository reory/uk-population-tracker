import plotly.express as px
from processing.load_population import load_population_snapshots

def population_line_chart():

    df = load_population_snapshots()

    # Sort for cleaning plotting
    df = df.sort(["region_code", "date"])

    fig = px.line(
        df,
        x="date",
        y="population",
        color="region_name",
        markers=True,
        title="UK Population Tracker",
    )

    fig.show()

if __name__ == "__main__":
    population_line_chart()