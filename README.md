# UK Population Tracker GB

- An end-to-end data engineering and visualization platform that transforms raw UK     population data into actionable geographic insights.

![License](https://img.shields.io/badge/License-MIT-green)
![Repo Size](https://img.shields.io/github/repo-size/reory/uk-population-tracker?cacheSeconds=60)
![Last Commit](https://img.shields.io/github/last-commit/reory/uk-population-tracker?cacheSeconds=60)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Polars](https://img.shields.io/badge/Polars-%23CD792C.svg?style=for-the-badge&logo=polars&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![Faker](https://img.shields.io/badge/Data_Gen-Faker-blue?style=for-the-badge)
![Mimesis](https://img.shields.io/badge/Data_Gen-Mimesis-green?style=for-the-badge)
![GeoPandas](https://img.shields.io/badge/GeoPandas-%23139C5C.svg?style=for-the-badge&logo=geopandas&logoColor=white)

---

## 🚀 Features

- Full-Stack Pipeline: Built a complete data flow using Python to process ONS data and MongoDB for persistent storage.

- Geospatial Intelligence: Integrated Geopandas and Matplotlib to generate high-fidelity choropleth maps with custom silver-on-charcoal styling.

- Interactive Analytics: Developed a dynamic dashboard using Flask and Plotly, allowing users to toggle between population totals, net changes, and percentage shifts.

- Responsive UI: Crafted a sleek "Dark Mode" interface featuring Hero Stat Cards that provide an instant narrative of the UK's top-performing regions.

<details>
  <summary>📸 Gallery & Interface</summary>

Below are snapshots of the application in action, highlighting the Dark/Silver aesthetic and the interactive data layers.

### 1. Main Dashboard
*Overview of the Stat cards and latest population snapshots.*
![Dashboard Screenshot](screenshots/7.png)

### 2. Population Trends
*Interactive bar charts showing percentage change across the 12 UK regions.*
![Bar Chart Graph Main Overview](screenshots/1.png)
![Line Chart Overview](screenshots/8.png)
![Region Overview](screenshots/1a.png)


### 3. Geospatial Analytics
*Interactive choropleth maps generated via Geopandas and Plotly.*
![UK Population Tracker Maps](screenshots/4.png)
![UK Population Tracker Maps](screenshots/5.png)
![UK Population Tracker Maps](screenshots/6.png)
![Interactve Map](screenshots/3.png)
![Interactive Map](screenshots/2.png)

</details>

---

## 🎥 Project Demo

See the **Interactive UK Population Tracker** in action. This video demonstrates the seamless navigation between the dashboard, regional trends, and the interactive Plotly maps.

<p align="center">
  <video src="demo.mp4" width="800" controls muted>
    Your browser does not support the video tag.
  </video>
</p>

> **Note:** If the video does not load, you can find the raw file [here](./demo.mp4).

---

## ⚙️ Installation & Setup

Follow these steps to get the environment running locally using Git Bash:

### 1. Clone the Repository

```bash
git clone [https://github.com/reory/uk-population-tracker.git](https://github.com/reory/uk-population-tracker.git)
cd uk-population-tracker
```

### 2. Set Up a Virtual Environment
```Bash
python -m venv venv
source venv/Scripts/activate
```

### 3. Data Dependencies
- **GeoPackage (.gpkg):** The boundary data for UK regions is located in the `/data` folder. 
- The application uses `pyogrio` and `geopandas` to interface with this file automatically. 
- Ensure the file `uk_regions.gpkg` remains in the `/data` directory for the map engine to function.

### 4. Install Dependencies
```Bash
pip install -r requirements.txt
```

### 5. Data Initialization (Faker & Mimesis)
Run the ingestion script to generate the synthetic dataset, inject noise, and populate your MongoDB instance:
```Bash
python -m processing.mongo_client
```

### 6. Generate Visual Assets
Pre-render the static maps before launching the dashboard:
```Bash
python -m processing.map_regions
```

### 7. Run the Application
```Bash
python run.py
```
The Flask dashboard will be live at http://127.0.0.1:5000/

---

## 🧪 Testing
This project uses `pytest` and `mongomock`.
To run the full suite:
`pytest`

To skip live database checks:
`pytest -m "not live"`

---

<details>
  <summary>🛠️ Tech Stack & Data Engineering</summary>

- Backend: **Python 3.x**, **Flask** (Web Framework)

- Database: **MongoDB** (Atlas/Community)

- Synthetic Data Generation: **Faker:** Used to generate a baseline of realistic regional entities and metadata.

- **Mimesis:** Leveraged for high-performance generation of large-scale population sets.

- Data Augmentation: Applied custom Noise Injection algorithms to baseline data to simulate realistic percentage changes and growth fluctuations over a multi-year timeline.

- Data Analysis: **Polars & Pandas**

- Geospatial: **Geopandas, Shapely**

- Frontend: **HTML5, CSS3, Plotly.js**

</details>

---

<details>
  <summary>📊 Key Features</summary>

- Latest Snapshot: Real-time retrieval of the most recent database entry.

- Multi-View Maps: Static regional analysis with formatted "Millions" labels for report-ready exports.

- Interactive Drill-Down: Hover-enabled Plotly maps for granular data exploration.

- Automated Pipeline: Custom processing modules that handle data cleaning and map generation in one command.

</details>

---

<details>
  <summary>🗺️ V2 Roadmap (The Drill-Down)</summary>

The next phase of the project focuses on Granular Urban Analytics:

- City Drill-Downs: Users will be able to click on a region (starting with London) to explore a new layer of data.

- Borough-Level Mapping: Integration of ONS Local Authority District (LAD) GeoPackages to map the 32 London Boroughs.

- Urban Comparison: Expanding the drill-down feature to other major UK cities like Manchester, Birmingham, and Leeds.

- Predictive Modeling: Using historical trends to forecast population growth over the next 5 years.

- Use prophet along with pandas for high quality forecasting for data.

</details>

---

<details>
  <summary>📝 Notes</summary>

* **Data Privacy:** All data used in this demonstration is synthetically generated via Faker and Mimesis. No real ONS individual records were accessed or stored.
* **Performance:** By utilizing Polars for the initial data joins and aggregation, the pipeline is capable of handling millions of rows while maintaining a sub-second response time for the dashboard.
* **Compatibility:** Designed for modern browsers. Best viewed in Chrome or Edge for full Plotly interactivity.

</details>

---

<details>
  <summary>🙏 Acknowledgments</summary>

* **The ONS Open Geography Portal** for providing the boundary GeoJSON/GeoPackage files.
* **The Open Source Community** for the incredible tools (Flask, Polars, MongoDB) that make projects like this possible.
* **Showcase Viewers:** Thank you for taking the time to explore this project! Feedback is always welcome.

</details>

---

**Built by Roy Peters** [contact details 😁](https://www.linkedin.com/in/roy-p-74980b382/)
