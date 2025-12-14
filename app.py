import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go   # needed for add_shape / add_annotation
import datetime                    # just for the docstring – not used for the line

# --------------------------------------------------------------
# 1️⃣ Load & clean the CSV (cached)
# --------------------------------------------------------------
if hasattr(st, "cache_data"):          # Streamlit ≥ 1.18
    @st.cache_data
    def load_data() -> pd.DataFrame:
        df = pd.read_csv(
            "Unemployment_Rate_upto_11_2020.csv",
            skipinitialspace=True,      # strip spaces after commas
            na_values=["", " "],        # treat blank fields as NaN
            engine="python",            # robust for malformed rows
        )
        # tidy column names and drop duplicated columns (the file repeats “Region”)
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.duplicated()]

        # give the unemployment column a stable name
        target = "Estimated Unemployment Rate (%)"
        if target not in df.columns:
            matches = [c for c in df.columns if "Unemployment Rate" in c]
            if not matches:
                raise KeyError("Unemployment column not found in CSV")
            df = df.rename(columns={matches[0]: target})

        # parse dates – format known: day‑month‑year
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")

        # drop rows that are completely empty (the file contains many ,,,,, lines)
        df = df.dropna(subset=["Region", "Date"])

        # force the unemployment column to numeric
        df[target] = pd.to_numeric(df[target], errors="coerce")

        return df.reset_index(drop=True)
else:                                   # fallback for Streamlit < 1.18
    @st.cache
    def load_data() -> pd.DataFrame:
        df = pd.read_csv(
            "Unemployment_Rate_upto_11_2020.csv",
            skipinitialspace=True,
            na_values=["", " "],
            engine="python",
        )
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.duplicated()]
        target = "Estimated Unemployment Rate (%)"
        if target not in df.columns:
            matches = [c for c in df.columns if "Unemployment Rate" in c]
            if not matches:
                raise KeyError("Unemployment column not found in CSV")
            df = df.rename(columns={matches[0]: target})
        df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
        df = df.dropna(subset=["Region", "Date"])
        df[target] = pd.to_numeric(df[target], errors="coerce")
        return df.reset_index(drop=True)

df = load_data()
unemp_col = "Estimated Unemployment Rate (%)"

# --------------------------------------------------------------
# 2️⃣ Streamlit page configuration
# --------------------------------------------------------------
st.set_page_config(
    page_title="India Unemployment Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 India Unemployment Analysis Dashboard")
st.markdown(
    """
**Explore the data**

- National average and peak unemployment rates  
- Trend for any state / union territory (pick from the dropdown)  
- COVID‑19 lockdown impact (vertical line)  
- Average unemployment rate per region (bar chart)
"""
)

# --------------------------------------------------------------
# 3️⃣ Overall metrics
# --------------------------------------------------------------
avg_unemp = df[unemp_col].mean()
max_unemp = df[unemp_col].max()

c1, c2 = st.columns(2)
c1.metric("Average Unemployment Rate", f"{avg_unemp:.2f}%")
c2.metric("Peak Unemployment Rate", f"{max_unemp:.2f}%")

# --------------------------------------------------------------
# 4️⃣ Region selector
# --------------------------------------------------------------
region = st.selectbox(
    "Select Region",
    options=sorted(df["Region"].unique()),
    index=0,
)

region_df = df[df["Region"] == region]

# --------------------------------------------------------------
# 5️⃣ Helper: add a vertical line (Lockdown) using add_shape
# --------------------------------------------------------------
def add_lockdown_vline(fig: go.Figure, date_str: str = "2020-03-01"):
    """
    Adds a red dashed vertical line at *date_str* and a small annotation.
    The line spans the full y‑range of the plot (yref="paper").
    """
    # ---- the line itself -------------------------------------------------
    fig.add_shape(
        dict(
            type="line",
            x0=date_str,
            x1=date_str,
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            line=dict(dash="dash", color="red", width=2),
        )
    )
    # ---- a tiny label that appears at the top of the plot ---------------
    fig.add_annotation(
        dict(
            x=date_str,
            y=1,
            xref="x",
            yref="paper",
            text="Lockdown start",
            showarrow=False,
            xanchor="left",
            yanchor="bottom",
            font=dict(color="red", size=12),
            bgcolor="rgba(255,255,255,0.7)",
        )
    )
    return fig

# --------------------------------------------------------------
# 6️⃣ Time‑series for the chosen region (with lockdown line)
# --------------------------------------------------------------
st.subheader(f"Unemployment Trend – {region}")

if region_df.empty:
    st.warning("No data available for the selected region.")
else:
    fig_region = px.line(
        region_df,
        x="Date",
        y=unemp_col,
        title=f"Unemployment Trend – {region}",
        markers=True,
    )
    fig_region = add_lockdown_vline(fig_region, "2020-03-01")
    st.plotly_chart(fig_region, use_container_width=True)

# --------------------------------------------------------------
# 7️⃣ National trend (with same lockdown line)
# --------------------------------------------------------------
st.subheader("COVID‑19 Impact (Lockdown started 01‑Mar‑2020)")

fig_national = px.line(
    df,
    x="Date",
    y=unemp_col,
    title="National Unemployment Trend (All Regions)",
    color="Region",
    line_group="Region",
    hover_name="Region",
)

fig_national = add_lockdown_vline(fig_national, "2020-03-01")
st.plotly_chart(fig_national, use_container_width=True)

# --------------------------------------------------------------
# 8️⃣ Average unemployment by region (bar chart)
# --------------------------------------------------------------
st.subheader("Average Unemployment Rate by Region (2020)")

region_avg = (
    df.groupby("Region")[unemp_col]
    .mean()
    .reset_index()
    .sort_values(by=unemp_col, ascending=False)
)

fig_bar = px.bar(
    region_avg,
    x="Region",
    y=unemp_col,
    title="Average Unemployment Rate per Region",
    text=unemp_col,
    color=unemp_col,
    color_continuous_scale="Blues",
)

fig_bar.update_traces(texttemplate="%{text:.2f}%")
st.plotly_chart(fig_bar, use_container_width=True)

