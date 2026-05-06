import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="London Property Portfolio", layout="wide")

st.title("🏙️ London Property Investment Opportunities")

# 1. THE DATA
@st.cache_data
def load_data():
    data = {
        'Property': ['The Skyline Apartment', 'The Heritage Mews', 'The Victoria Quarter'],
        'Borough': ['Canary Wharf (E14)', 'Greenwich (SE10)', 'Battersea (SW11)'],
        'Price': [850000, 620000, 1100000],
        'Rent_PCM': [3800, 2750, 4800],
        'Yield': [5.36, 5.32, 5.24],
        'Growth': [4.5, 5.2, 3.8],
        'Description': [
            "High-rise luxury living in the heart of London's financial district. Strong corporate rental demand.",
            "Charming period conversion near Greenwich Park. High capital growth potential due to local regeneration.",
            "Premium new-build near the Power Station. Iconic location with ultra-prime appreciation prospects."
        ],
        'lat': [51.5054, 51.4826, 51.4791],
        'lon': [-0.0235, -0.0015, -0.1485]
    }
    return pd.DataFrame(data)

df = load_data()

# 2. INDIVIDUAL OPPORTUNITY PRESENTATION
st.header("1. Deep Dive: Property Analysis")
st.info("Select a tab below to view the specifics of each investment.")

# Create one tab for each property
tabs = st.tabs([f"📍 {name}" for name in df['Property']])

for i, tab in enumerate(tabs):
    with tab:
        prop = df.iloc[i]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader(prop['Property'])
            st.write(f"**Location:** {prop['Borough']}")
            st.write(f"**Investment Thesis:** {prop['Description']}")
            
            # Key Stats in a clean format
            st.metric("Purchase Price", f"£{prop['Price']:,}")
            st.metric("Monthly Rent", f"£{prop['Rent_PCM']:,}")
            st.metric("Annual Yield", f"{prop['Yield']}%")

        with col2:
            # Local Map for this specific property
            single_map_df = pd.DataFrame([prop])
            fig_map = px.scatter_mapbox(single_map_df, lat="lat", lon="lon", zoom=13, height=300)
            fig_map.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# 3. SUMMARY COMPARISON TABLE
st.header("2. Portfolio Comparison Summary")
st.markdown("Use this table to compare the core financial metrics side-by-side.")

# Clean up the dataframe for display
summary_df = df[['Property', 'Borough', 'Price', 'Rent_PCM', 'Yield', 'Growth']].copy()

# Add Formatting for the table
formatted_df = summary_df.copy()
formatted_df['Price'] = formatted_df['Price'].map('£{:,.0f}'.format)
formatted_df['Rent_PCM'] = formatted_df['Rent_PCM'].map('£{:,.0f}'.format)
formatted_df['Yield'] = formatted_df['Yield'].map('{:.2f}%'.format)
formatted_df['Growth'] = formatted_df['Growth'].map('{:.1f}%'.format)

# Display as a clean, static table
st.table(formatted_df)

# 4. VISUAL COMPARISON CHART
st.subheader("Yield vs. Capital Growth Comparison")
fig_comp = px.bar(
    summary_df, 
    x='Property', 
    y='Yield', 
    color='Growth',
    title="Relative Performance (Height = Yield | Color = Capital Growth)",
    labels={'Yield': 'Rental Yield (%)', 'Growth': 'Annual Growth (%)'},
    color_continuous_scale='RdYlGn' # Red to Green scale
)
st.plotly_chart(fig_comp, use_container_width=True)
