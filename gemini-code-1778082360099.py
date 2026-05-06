import streamlit as st
import pandas as pd
import plotly.express as px

# --- BRAND COLORS (houseUP) ---
HOUSEUP_BLUE = "#002D40"
HOUSEUP_ORANGE = "#E58A1F"
HOUSEUP_LIGHT = "#F4F4F4"

st.set_page_config(page_title="houseUP | Investment Portfolio", layout="wide")

# Custom Styling
st.markdown(f"""
    <style>
   
    .main {{ background-color: {HOUSEUP_LIGHT}; }}
    .stMetric {{ background-color: white; padding: 15px; border-radius: 10px; border-left: 5px solid {HOUSEUP_ORANGE}; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }}
    div[data-testid="stSidebar"] {{ background-color: {HOUSEUP_BLUE}; color: white; }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = {
        'Property': ['The Skyline Project', 'Greenwich Mews Dev', 'Battersea Quarter'],
        'Borough': ['Canary Wharf (E14)', 'Greenwich (SE10)', 'Battersea (SW11)'],
        'Total Development Cost': [975000, 715000, 1320000],
        'Yield (%)': [5.4, 5.1, 4.8],
        'Annual Cap Growth (%)': [4.2, 5.5, 3.9],
        # New Qualitative Parameters
        'Location Grade': ['A', 'A+', 'A++'],
        'Prestige Score (1-10)': [7, 8, 10],
        'Liquidity': ['High', 'Medium', 'Very High'],
        'lat': [51.5054, 51.4826, 51.4791],
        'lon': [-0.0235, -0.0015, -0.1485]
    }
    return pd.DataFrame(data)

df = load_data()

st.title("🏙️ houseUP Investment Portfolio")
st.markdown("### Development Feasibility & Market Potential")

# 1. INDIVIDUAL TABS (Restructured)
tabs = st.tabs([f"🏗️ {name}" for name in df['Property']])

for i, tab in enumerate(tabs):
    with tab:
        p = df.iloc[i]
        col1, col2, col3 = st.columns([1, 1, 1.2])
        
        with col1:
            st.subheader("Financial Metrics")
            st.metric("Total Cost", f"£{p['Total Development Cost']:,.0f}")
            st.metric("Target Yield", f"{p['Yield (%)']}%")
            st.metric("Est. Cap Growth", f"{p['Annual Cap Growth (%)']}%")
        
        with col2:
            st.subheader("Asset Quality")
            st.write(f"**Location Grade:** {p['Location Grade']}")
            st.write(f"**Prestige Score:** {p['Prestige Score (1-10)']}/10")
            st.write(f"**Market Liquidity:** {p['Liquidity']}")
            # Progress bar for prestige
            st.progress(int(p['Prestige Score (1-10)'] * 10))
        
        with col3:
            st.subheader("Site Location")
            fig_map = px.scatter_mapbox(pd.DataFrame([p]), lat="lat", lon="lon", zoom=12, height=250)
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# 2. COMPARISON SUMMARY
st.header("2. Portfolio Growth & Yield Analysis")

col_a, col_b = st.columns([1.5, 1])

with col_a:
    st.subheader("Market Potential Matrix")
    # This chart shows Yield vs Growth. Top right is the "Gold Mine"
    fig_matrix = px.scatter(
        df, x='Yield (%)', y='Annual Cap Growth (%)', 
        size='Total Development Cost', color='Property',
        text='Property', hover_name='Property',
        color_discrete_sequence=[HOUSEUP_BLUE, HOUSEUP_ORANGE, "#446A7A"]
    )
    fig_matrix.update_traces(textposition='top center')
    fig_matrix.update_layout(plot_bgcolor='white', xaxis=dict(gridcolor='#eee'), yaxis=dict(gridcolor='#eee'))
    st.plotly_chart(fig_matrix, use_container_width=True)

with col_b:
    st.subheader("Prestige vs. Performance")
    # Showing how Prestige correlates to Growth
    fig_prestige = px.bar(
        df, x='Property', y='Prestige Score (1-10)',
        color_discrete_sequence=[HOUSEUP_ORANGE]
    )
    fig_prestige.update_layout(yaxis_range=[0,10])
    st.plotly_chart(fig_prestige, use_container_width=True)

# 3. FINAL SUMMARY TABLE
st.subheader("Full Comparison Table")
display_df = df[['Property', 'Borough', 'Location Grade', 'Prestige Score (1-10)', 'Yield (%)', 'Annual Cap Growth (%)', 'Total Development Cost']]
st.table(display_df.style.format({
    'Total Development Cost': '£{:,.0f}',
    'Yield (%)': '{:.1f}%',
    'Annual Cap Growth (%)': '{:.1f}%'
}))
