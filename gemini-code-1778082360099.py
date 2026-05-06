import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="London Property Investment Portfolio", layout="wide")

# Title and Intro
st.title("🏙️ London Property Investment Analysis")
st.markdown("### Portfolio Overview: Three High-Yield Opportunities")

# Load Data (Replace with your actual file path if needed)
@st.cache_data
def load_data():
    # This matches the structure of the Excel file I generated for you
    data = {
        'Property': ['The Skyline Apartment', 'The Heritage Mews', 'The Victoria Quarter'],
        'Borough': ['Canary Wharf (E14)', 'Greenwich (SE10)', 'Battersea (SW11)'],
        'Price': [850000, 620000, 1100000],
        'Rent_PCM': [3800, 2750, 4800],
        'Yield': [5.36, 5.32, 5.24],
        'Growth': [4.5, 5.2, 3.8],
        'lat': [51.5054, 51.4826, 51.4791],
        'lon': [-0.0235, -0.0015, -0.1485]
    }
    return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Investment Assumptions")
growth_years = st.sidebar.slider("Projection Horizon (Years)", 1, 10, 5)
management_fee = st.sidebar.slider("Management Fee (%)", 0, 15, 10)

# --- TOP ROW: KPI CARDS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg. Rental Yield", f"{df['Yield'].mean():.2f}%")
with col2:
    st.metric("Total Portfolio Value", f"£{df['Price'].sum():,.0f}")
with col3:
    st.metric("Total Monthly Income", f"£{df['Rent_PCM'].sum():,.0f}")

st.divider()

# --- MIDDLE ROW: MAP & COMPARISON ---
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("Geographic Distribution")
    fig_map = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="Property", 
                                hover_data=["Borough", "Price"],
                                color_discrete_sequence=["red"], zoom=10, height=400)
    fig_map.update_layout(mapbox_style="carto-positron")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with right_col:
    st.subheader("Yield vs Growth")
    fig_chart = px.bar(df, x='Property', y='Yield', color='Growth',
                       title="Yield (Bar) & Growth Potential (Color)")
    st.plotly_chart(fig_chart, use_container_width=True)

# --- BOTTOM ROW: PROJECTIONS ---
# --- BOTTOM ROW: PROJECTIONS (FIXED) ---
st.subheader(f"Projected Capital Appreciation ({growth_years} Years)")

# Calculate future value based on user-selected growth years
df['Projected_Value'] = df['Price'] * ((1 + (df['Growth']/100)) ** growth_years)

# Create a grouped bar chart for comparison
fig_proj = px.bar(
    df, 
    x='Property', 
    y=['Price', 'Projected_Value'], 
    barmode='group',
    title="Current Price vs Future Valuation",
    labels={'value': 'Value (£)', 'variable': 'Status'},
    color_discrete_sequence=['#3366CC', '#109618'] # Blue for current, Green for future
)

st.plotly_chart(fig_proj, use_container_width=True)

# Data Table
st.subheader("Raw Investment Data")
st.dataframe(df[['Property', 'Borough', 'Price', 'Rent_PCM', 'Yield', 'Growth']], use_container_width=True)
