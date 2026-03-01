import plotly.express as px
from flask import Blueprint, render_template
from processing.summary import trend_summary
from visualisation.plotly_maps import build_interactive_toggle_map
from processing.mongo_client import collection
from processing.map_regions import (
    plot_population_map,
    plot_percentage_change_map
)

main = Blueprint("main", __name__)

# Dashboard views------------------------------

# Home
@main.route("/")
def index():
    
    # Fetch the single most recent entry from the MongoDB.
    latest = list(collection.find().sort("date", -1).limit(1))[0]

    # Generate the summary data for stats on main dashboard page.
    # Get data from Polars and Pandas.
    summary_df = trend_summary()

    # Calculate the stats.
    total_pop = summary_df["population"].sum()

    # Sorting to find the top stat.
    sorted_df = summary_df.sort("pct_change", descending=True)
    fastest_grower = sorted_df.get_column("region_name")[0]
    # Convert percentage (* 100)
    growth_val = sorted_df.get_column("pct_change")[0] * 100 

    # Pass everything to the template.
    return render_template(
        "index.html", 
        latest=latest,
        total_pop=total_pop,
        fastest_grower=fastest_grower,
        growth_val=growth_val,
    )

# Analytics
@main.route("/trends")
def trends():
    
    # Get summary as Pandas
    df = trend_summary().to_pandas()

    # Convert pct_change to a readable percentage
    df["pct_change"] = df["pct_change"] * 100
    
    # Build Plotly bar chart
    fig = px.bar(
        df,
        x="region_name",
        y="pct_change",
        title="Population Percent Change by Region",
        labels={"pct_change": "% Change", "region_name": "Region"},
        hover_data={
            "population": ":,", 
            "change": ":,",
            "pct_change": ".2f"
        },
    )
    
    fig.update_traces(marker=dict(color="#F6F2F2"))

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="lightslategray",
            bordercolor="#F9F9F4"
        ),
        template="plotly_dark",
        xaxis_tickangle=-45,
        height=500,
        margin=dict(l=40, r=40, t=80, b=120)
    )

    # Convert Plotly figure to HTML fragment.
    graph_html = fig.to_html(full_html=False)

    summary_list = df.to_dict(orient="records")

    return render_template(
        "trends.html", 
        graph_html=graph_html, 
        summary=summary_list
    )

# Maps
@main.route("/maps")
def maps():
    
    # Generate static populations and change map.
    plot_population_map()
    plot_percentage_change_map()
    return render_template("map.html")

# UI using Plotly.
@main.route("/interactive-map")
def interactive_map():
    
    # Build Plotly/JSON map for frontend interactivity (Flask)
    fig = build_interactive_toggle_map()
    graph_json = fig.to_json()
    return render_template("interactive_map.html", graph_json=graph_json)