import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- BRAND COLORS (houseUP) ---
HOUSEUP_BLUE = "#002D40"    # Deep Navy/Teal
HOUSEUP_ORANGE = "#E58A1F"  # Branding Orange
HOUSEUP_LIGHT = "#F4F4F4"   # Light Grey Background
HOUSEUP_WHITE = "#FFFFFF"

# Set page config
st.set_page_config(page_title="houseUP | Investment Dashboard", layout="wide")

# Custom CSS to inject houseUP styling
st.markdown(f"""
    <style>
    .main {{ background-color: {HOUSEUP_LIGHT}; }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: {HOUSEUP_BLUE}; border-radius: 5px; padding: 5px; }}
    .stTabs [data-baseweb="tab"] {{ color: white; }}
    .stMetric {{ background-color: {HOUSEUP_WHITE}; padding: 15px; border-radius: 10px; border-left: 5px solid {HOUSEUP_ORANGE}; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }}
    h1, h2, h3 {{ color: {HOUSEUP_BLUE}; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
    div[data-testid="stSidebar"] {{ background-color: {HOUSEUP_BLUE}; color: white; }}
    </style>
    """, unsafe_allow_html=True)

# 1. THE DATA MODEL
@st.cache_data
def load_data():
    data = {
        'Property': ['The Skyline Project', 'Greenwich Mews Dev', 'Battersea Quarter'],
        'Borough': ['Canary Wharf (E14)', 'Greenwich (SE10)', 'Battersea (SW11)'],
        'Site Purchase': [650000, 480000, 850000],
        'Stamp Duty': [35000, 15000, 52000],
        'Finding Fees': [13000, 9600, 17000],
        'Investigations': [5000, 4500, 8000],
        'Construction Costs': [180000, 120000, 250000],
        'Professional Costs': [18000, 12000, 25000],
        'Development Management Fees': [20000, 15000, 30000],
        'Taxes & Contributions': [12000, 8000, 22000],
        'Cost of Capital': [45000, 32000, 60000],
        'Agent Fees': [15000, 12000, 20000],
        'Expected GDV': [1200000, 900000, 1650000],
        'lat': [51.5054, 51.4826, 51.4791],
        'lon': [-0.0235, -0.0015, -0.1485]
    }
    df = pd.DataFrame(data)
    cost_cols = ['Site Purchase', 'Stamp Duty', 'Finding Fees', 'Investigations', 'Construction Costs', 
                 'Professional Costs', 'Taxes & Contributions', 'Development Management Fees', 
                 'Cost of Capital', 'Agent Fees']
    df['Total Development Cost'] = df[cost_cols].sum(axis=1)
    df['Projected Profit'] = df['Expected GDV'] - df['Total Development Cost']
    df['Return on Cost (%)'] = (df['Projected Profit'] / df['Total Development Cost']) * 100
    return df

df = load_data()

# Header with houseUP Logo Placeholder
st.title("🏙️ houseUP Investment Portfolio")
st.markdown("#### Intelligent Construction & Development Analysis")

# 2. INDIVIDUAL DEEP DIVES
st.header("1. Individual Project Feasibility")
tabs = st.tabs([f"🏗️ {name}" for name in df['Property']])

for i, tab in enumerate(tabs):
    with tab:
        p = df.iloc[i]
        col1, col2, col3 = st.columns([1, 1.2, 1.2])
        
        with col1:
            st.subheader("Project Summary")
            st.metric("Total Investment", f"£{p['Total Development Cost']:,.0f}")
            st.metric("Projected Profit", f"£{p['Projected Profit']:,.0f}", delta=f"{p['Return on Cost (%)']:.1f}% ROC")
            st.write(f"**Borough:** {p['Borough']}")
        
        with col2:
            st.subheader("Cost Breakdown")
            breakdown_data = {
                'Category': ['Site Purchase', 'Construction', 'Finance', 'Professional/Mgmt', 'Taxes', 'Fees'],
                'Value': [p['Site Purchase'], p['Construction Costs'], p['Cost of Capital'],
                          p['Professional Costs'] + p['Development Management Fees'],
                          p['Stamp Duty'] + p['Taxes & Contributions'],
                          p['Finding Fees'] + p['Investigations'] + p['Agent Fees']]
            }
            # Color pie with houseUP theme
            fig_pie = px.pie(breakdown_data, values='Value', names='Category', hole=0.5,
                             color_discrete_sequence=[HOUSEUP_BLUE, HOUSEUP_ORANGE, "#446A7A", "#88A0A8", "#B0B0B0"])
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250, showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col3:
            st.subheader("Site Map")
            fig_map = px.scatter_mapbox(pd.DataFrame([p]), lat="lat", lon="lon", zoom=12, height=250)
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# 3. SIDE-BY-SIDE SUMMARY
st.header("2. Comparative Analytics")
st.markdown("Comprehensive view of the **houseUP** investment pipeline.")

# Styled Comparison Table
comp_df = df.set_index('Property').T
rows_to_show = ['Site Purchase', 'Construction Costs', 'Cost of Capital', 'Total Development Cost', 
                'Expected GDV', 'Projected Profit', 'Return on Cost (%)']
st.table(comp_df.loc[rows_to_show].style.format(lambda x: f"£{x:,.0f}" if x > 100 else f"{x:.1f}%"))

# Final Chart with houseUP Colors
st.subheader("Investment Efficiency (Profit vs. Total Cost)")
fig_profit = px.bar(
    df, x='Property', y=['Total Development Cost', 'Projected Profit'],
    barmode='stack',
    color_discrete_map={'Total Development Cost': HOUSEUP_BLUE, 'Projected Profit': HOUSEUP_ORANGE}
)
fig_profit.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_profit, use_container_width=True)
