import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="London Development Portfolio", layout="wide")

st.title("🏗️ London Property Development Dashboard")

# 1. THE DATA MODEL
@st.cache_data
def load_data():
    # Adding your specific line items for three investments
    data = {
        'Property': ['The Skyline Project', 'Greenwich Mews Dev', 'Battersea Quarter'],
        'Borough': ['Canary Wharf (E14)', 'Greenwich (SE10)', 'Battersea (SW11)'],
        
        # Site & Entry Costs
        'Site Purchase': [650000, 480000, 850000],
        'Stamp Duty': [35000, 15000, 52000],
        'Finding Fees': [13000, 9600, 17000],
        'Investigations': [5000, 4500, 8000],
        
        # Construction & Professional
        'Construction Costs': [180000, 120000, 250000],
        'Professional Costs': [18000, 12000, 25000], # Architect, Surveyors
        
        # Fees & Taxes
        'Development Management Fees': [20000, 15000, 30000],
        'Taxes & Contributions': [12000, 8000, 22000], # CIL, S106
        
        # Finance & Exit
        'Cost of Capital': [45000, 32000, 60000], # Interest/Finance
        'Agent Fees': [15000, 12000, 20000], # Disposal fees
        
        # Performance
        'Expected GDV': [1200000, 900000, 1650000], # Gross Development Value
        'lat': [51.5054, 51.4826, 51.4791],
        'lon': [-0.0235, -0.0015, -0.1485]
    }
    df = pd.DataFrame(data)
    
    # Calculate Total Development Cost (TDC)
    cost_cols = [
        'Site Purchase', 'Stamp Duty', 'Finding Fees', 'Investigations', 
        'Construction Costs', 'Professional Costs', 'Taxes & Contributions', 
        'Development Management Fees', 'Cost of Capital', 'Agent Fees'
    ]
    df['Total Development Cost'] = df[cost_cols].sum(axis=1)
    df['Projected Profit'] = df['Expected_GDV'] - df['Total Development Cost']
    df['Return on Cost (%)'] = (df['Projected Profit'] / df['Total Development Cost']) * 100
    
    return df

df = load_data()

# 2. INDIVIDUAL DEEP DIVES
st.header("1. Individual Project Feasibility")

tabs = st.tabs([f"🏗️ {name}" for name in df['Property']])

for i, tab in enumerate(tabs):
    with tab:
        p = df.iloc[i]
        
        col1, col2, col3 = st.columns([1, 1.2, 1.2])
        
        with col1:
            st.subheader("Project Summary")
            st.write(f"**Borough:** {p['Borough']}")
            st.metric("Total Investment", f"£{p['Total Development Cost']:,.0f}")
            st.metric("Projected Profit", f"£{p['Projected Profit']:,.0f}", delta=f"{p['Return on Cost (%)']:.1f}% ROC")
        
        with col2:
            st.subheader("Cost Breakdown")
            # Create a pie chart for costs
            breakdown_data = {
                'Category': [
                    'Site Purchase', 'Construction', 'Finance/Capital', 
                    'Professional/Mgmt', 'Taxes/SDLT', 'Other Fees'
                ],
                'Value': [
                    p['Site Purchase'], 
                    p['Construction Costs'], 
                    p['Cost of Capital'],
                    p['Professional Costs'] + p['Development Management Fees'],
                    p['Stamp Duty'] + p['Taxes & Contributions'],
                    p['Finding Fees'] + p['Investigations'] + p['Agent Fees']
                ]
            }
            fig_pie = px.pie(breakdown_data, values='Value', names='Category', hole=0.4)
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=250)
            st.plotly_chart(fig_pie, use_container_width=True)

        with col3:
            st.subheader("Location")
            fig_map = px.scatter_mapbox(pd.DataFrame([p]), lat="lat", lon="lon", zoom=12, height=250)
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# 3. SIDE-BY-SIDE COMPARISON TABLE
st.header("2. Portfolio Comparison Table")

# Prepare a vertical comparison table (easier to read for development)
comp_df = df.set_index('Property').T
# Filter to only show the cost rows for the table
rows_to_show = [
    'Site Purchase', 'Stamp Duty', 'Finding Fees', 'Investigations', 
    'Construction Costs', 'Professional Costs', 'Taxes & Contributions', 
    'Development Management Fees', 'Cost of Capital', 'Agent Fees',
    'Total Development Cost', 'Expected GDV', 'Projected Profit', 'Return on Cost (%)'
]
st.table(comp_df.loc[rows_to_show].style.format(lambda x: f"£{x:,.0f}" if isinstance(x, (int, float)) and x > 100 else (f"{x:.2f}%" if isinstance(x, float) and x < 1 else x)))

# 4. PROFITABILITY CHART
st.subheader("Profit vs. Cost Analysis")
fig_profit = px.bar(
    df, x='Property', y=['Total Development Cost', 'Projected Profit'],
    title="Total Investment Required vs. Projected Profit",
    barmode='stack',
    color_discrete_map={'Total Development Cost': '#636EFA', 'Projected Profit': '#00CC96'}
)
st.plotly_chart(fig_profit, use_container_width=True)
