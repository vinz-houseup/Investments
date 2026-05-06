import streamlit as st
import pandas as pd
import plotly.express as px

# --- BRAND COLORS (houseUP) ---
HOUSEUP_BLUE = "#002D40"
HOUSEUP_ORANGE = "#E58A1F"
HOUSEUP_LIGHT = "#F4F4F4"

st.set_page_config(page_title="houseUP | Investor Portfolio", layout="wide")

# Custom Styling for houseUP aesthetic
st.markdown(f"""
    <style>
    .main {{ background-color: {HOUSEUP_LIGHT}; }}
    .stMetric {{ background-color: white; padding: 15px; border-radius: 10px; border-left: 5px solid {HOUSEUP_ORANGE}; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: {HOUSEUP_BLUE}; border-radius: 5px; }}
    .stTabs [data-baseweb="tab"] {{ color: white; }}
    .stProgress > div > div > div > div {{ background-color: {HOUSEUP_ORANGE}; }}
    h1, h2, h3 {{ color: {HOUSEUP_BLUE}; }}
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = {
        'Property': ['The Skyline Project', 'Greenwich Mews Dev', 'Battersea Quarter'],
        'Borough': ['Canary Wharf (E14)', 'Greenwich (SE10)', 'Battersea (SW11)'],
        
        # 1. ACQUISITION PHASE
        'Site Purchase': [650000, 480000, 850000],
        'Stamp Duty': [35000, 15000, 52000],
        'Finding Fees': [13000, 9600, 17000],
        
        # 2. REFURBISHMENT PHASE (houseUP Services)
        'Construction Costs': [150000, 110000, 220000],
        'Professional Costs': [15000, 11000, 22000], # Architect, Structural, Survey
        'Investigations': [5000, 4000, 7000],
        
        # 3. MANAGEMENT & EXIT
        'Development Management Fees': [15000, 10000, 25000],
        'Agent Fees (Rental/Mgmt)': [12000, 9000, 18000],
        'Taxes & Contributions': [10000, 7000, 15000],
        'Cost of Capital': [40000, 30000, 55000],
        
        # MARKET PERFORMANCE
        'Yield (%)': [5.4, 5.1, 4.8],
        'Annual Cap Growth (%)': [4.2, 5.5, 3.9],
        'Prestige Score (1-10)': [7, 8, 10],
        'Expected GDV': [1150000, 880000, 1580000],
        
        'lat': [51.5054, 51.4826, 51.4791],
        'lon': [-0.0235, -0.0015, -0.1485]
    }
    df = pd.DataFrame(data)
    
    # Calculate Total Investment Required
    cost_cols = ['Site Purchase', 'Stamp Duty', 'Finding Fees', 'Construction Costs', 
                 'Professional Costs', 'Investigations', 'Development Management Fees', 
                 'Agent Fees (Rental/Mgmt)', 'Taxes & Contributions', 'Cost of Capital']
    df['Total Investment'] = df[cost_cols].sum(axis=1)
    return df

df = load_data()

st.title("🏗️ houseUP | Investment & Development Portfolio")
st.markdown("#### End-to-End Property Acquisition, Renovation, and Management")

# 1. PROPERTY DEEP DIVES
tabs = st.tabs([f"📍 {name}" for name in df['Property']])

for i, tab in enumerate(tabs):
    with tab:
        p = df.iloc[i]
        c1, c2, c3 = st.columns([1, 1.2, 1.2])
        
        with c1:
            st.subheader("Key ROI Metrics")
            st.metric("Total Capital Required", f"£{p['Total Investment']:,.0f}")
            st.metric("Net Yield", f"{p['Yield (%)']}%")
            st.write(f"**Prestige Rating:** {int(p['Prestige Score (1-10)'])}/10")
            st.progress(int(p['Prestige Score (1-10)'] * 10))
            st.write(f"**Borough:** {p['Borough']}")

        with c2:
            st.subheader("Cost Lifecycle Breakdown")
            # Grouped data for the pie chart
            lifecycle_data = {
                'Phase': ['Acquisition', 'houseUP Refurbishment', 'Professional/Finance'],
                'Cost': [
                    p['Site Purchase'] + p['Stamp Duty'] + p['Finding Fees'],
                    p['Construction Costs'] + p['Investigations'],
                    p['Professional Costs'] + p['Development Management Fees'] + p['Cost of Capital'] + p['Agent Fees (Rental/Mgmt)']
                ]
            }
            fig_pie = px.pie(lifecycle_data, values='Cost', names='Phase', hole=0.4,
                             color_discrete_sequence=[HOUSEUP_BLUE, HOUSEUP_ORANGE, "#446A7A"])
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250, showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)

        with c3:
            st.subheader("Location Strategy")
            fig_map = px.scatter_mapbox(pd.DataFrame([p]), lat="lat", lon="lon", zoom=12, height=250)
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# 2. MARKET POTENTIAL MATRIX
st.header("2. Market Performance & Growth")
col_a, col_b = st.columns([1.5, 1])

with col_a:
    st.subheader("Yield vs. Capital Growth Matrix")
    fig_matrix = px.scatter(
        df, x='Yield (%)', y='Annual Cap Growth (%)', 
        size='Total Investment', color='Property', text='Property',
        color_discrete_sequence=[HOUSEUP_BLUE, HOUSEUP_ORANGE, "#446A7A"]
    )
    fig_matrix.update_layout(plot_bgcolor='white')
    st.plotly_chart(fig_matrix, use_container_width=True)

with col_b:
    st.subheader("Financial Comparison")
    st.table(df[['Property', 'Yield (%)', 'Annual Cap Growth (%)', 'Total Investment']].style.format({
        'Total Investment': '£{:,.0f}',
        'Yield (%)': '{:.1f}%',
        'Annual Cap Growth (%)': '{:.1f}%'
    }))

# 3. DETAILED COST TABLE (The Full Breakdown)
st.subheader("Full Development & Management Cost Breakdown")
full_comp_df = df.set_index('Property').T
# Select all cost rows for the final investor review
cost_rows = ['Site Purchase', 'Stamp Duty', 'Finding Fees', 'Construction Costs', 
             'Professional Costs', 'Investigations', 'Development Management Fees', 
             'Agent Fees (Rental/Mgmt)', 'Cost of Capital', 'Total Investment']
st.table(full_comp_df.loc[cost_rows].style.format(lambda x: f"£{x:,.0f}" if isinstance(x, (int, float)) else x))
