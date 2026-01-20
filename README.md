UNEMPLOYMENT ANALYSIS WITH PYTHON:
- This project builds an interactive dashboard to analyze unemployment rates across Indian states/UTs during 2020, with a special focus on the impact of the COVID‑19 lockdown starting March 2020. The dashboard lets users explore national and regional unemployment trends, identify peaks, and understand patterns that can inform economic and social policy decisions.​​

LIVE DEMO:
- https://unemploymentanalysiswithpython-2.onrender.com/

FEATURES:
- Visualizes national unemployment trend over time with a vertical marker for the COVID‑19 lockdown start.
- Interactive state/UT selector to view the unemployment trend for a specific region (e.g., West Bengal).
- KPIs showing average and peak unemployment rate for the selected region.
- Bar chart of average unemployment rate by region to compare states/UTs across India.

INSTALLATION:
- git clone https://github.com/IshanGain/UnemploymentAnalysisWithPython.git
- cd UnemploymentAnalysisWithPython
- pip install -r requirements.txt

- Ensure Python and all dependencies in requirements.txt (e.g., pandas, plotly, dash/streamlit) are installed.

USAGE:
- python app.py
- Open the URL shown in the terminal.
- Use the region dropdown to switch states/UTs and explore their unemployment trends, while monitoring changes around the lockdown line and comparing average and peak rates.

PROJECT STRUCTURE:
- India_Unemployment_Analysis/
- ├── app.py                    # Main dashboard app
- ├── data/                     # Unemployment dataset(s)
- ├── notebooks/                # Optional EDA / preprocessing notebooks
- ├── requirements.txt          # Python dependencies
- └── README.md                 # Project documentation
