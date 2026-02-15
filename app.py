import pandas as pd
import streamlit as st
import joblib

#---Load Data (CSV)---
df_seeds=pd.read_csv('seeds.csv')
df_disease=pd.read_csv('Disease_Advice.csv')

try:
    with open('annapurna_model (1).pkl', 'rb') as file:
        yield_model=joblib.load(file)
except FileNotFoundError:
    yield_model=None

#---Page Config---
st.set_page_config(page_title="Annapurna 1.0", layout="wide")
st.title("🌾Annapurna 1.0: Purvanchal Agri-Intelligence")
st.markdown("---")


districts= ["ALLAHABAD", "AMBEDKAR NAGAR", "AZAMGARH", "BAHRAICH", "BALLIA", 
    "BALRAMPUR", "BASTI", "CHANDAULI", "DEORIA", "FATEHPUR", 
    "GHAZIPUR", "GONDA", "GORAKHPUR", "JAUNPUR", "KAUSHAMBI", 
    "KUSHI NAGAR", "MAHARAJGANJ", "MAU", "MIRZAPUR", "PRATAPGARH", 
    "SANT KABEER NAGAR", "SANT RAVIDAS NAGAR", "SHRAVASTI", 
    "SIDDHARTH NAGAR", "SONBHADRA", "SULTANPUR", "VARANASI"]



st.write("AI Model Creator: Shishir Dwivedi")
st.write("Integration and Website Development: Deepanshu Sinha and Sanshay Singh")

#Main Interface
tab1, tab2, tab3=st.tabs(["📈 Yield Prediction", "🌱 Variety Details", "🛡️ Disease Prevention"])

with tab1:
    selected_crop=st.selectbox("**Select Crop**", ["Rice", "Wheat", "Barley", "Mustard"])
    st.header(f"Yield Forecast: {selected_crop}")
    
    # 1. Setup UI for the required inputs
    col1, col2 = st.columns(2)
    with col1:
        # These will be passed as STRINGS because of the Pipeline
        selected_district = st.selectbox("Select District", 
            ["ALLAHABAD", "AMBEDKAR NAGAR", "AZAMGARH", "BAHRAICH", "BALLIA", 
    "BALRAMPUR", "BASTI", "CHANDAULI", "DEORIA", "FATEHPUR", 
    "GHAZIPUR", "GONDA", "GORAKHPUR", "JAUNPUR", "KAUSHAMBI", 
    "KUSHI NAGAR", "MAHARAJGANJ", "MAU", "MIRZAPUR", "PRATAPGARH", 
    "SANT KABEER NAGAR", "SANT RAVIDAS NAGAR", "SHRAVASTI", 
    "SIDDHARTH NAGAR", "SONBHADRA", "SULTANPUR", "VARANASI"])
        selected_season = st.selectbox("Select Season", ["Kharif", "Rabi"])
    
    with col2:
        target_year=st.selectbox("Select Year", [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030])
        land_area = st.number_input("Area (in Hectares)", value=1.0)

    if st.button("🚀 Run Prediction"):
        # 2. Season Mapping (Team ID: 1 for Rabi, 0 for Kharif)
        s_id = 1 if selected_season == "Rabi" else 0

        input_data = pd.DataFrame([[
            selected_district, 
            selected_crop, 
            target_year, 
            s_id, 
            land_area
        ]], columns=['District', 'Crop', 'Year', 'Season', 'Area'])
        
    try:
        # 1. Get the raw prediction (Tons per Hectare)
        prediction_per_ha = yield_model.predict(input_data)[0]
    
        # 2. Calculate the total yield based on user's land area
        total_harvest = prediction_per_ha * land_area
    
        # 3. Display both metrics
        st.markdown("---")
        col_a, col_b = st.columns(2)
    
        with col_a:
            st.metric(
                label="Yield Efficiency", 
                value=f"{round(prediction_per_ha, 2)} Tons/Hectare",
                help="This is the estimated production for every 1 hectare of land."
           )
        
        with col_b:
            st.metric(
                label="Total Estimated Harvest", 
                value=f"{round(total_harvest, 2)} Tons",
                help=f"Total production for your specific area of {land_area} hectares."
           )
        st.success(f"Analysis complete for {selected_crop} in {selected_district}!")

    except Exception as e:
        st.error(f"Prediction Error: {e}")


with tab2:
    st.header(f"Recommended {selected_crop} Varieties")
    # Case-insensitive matching with the 'CROP' column
    seed_data = df_seeds[df_seeds['Crop'].str.contains(selected_crop, case=False, na=False)]
    
    if not seed_data.empty:                                                                                                                                                                                                              
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("**Stable Variety**")
            st.write(seed_data['Stable Variety'].values[0])
        with col2:
            st.success("**High Yield Variety**")
            st.write(seed_data['High Yield Variety'].values[0])
        with col3:
            st.warning("**Short Duration**")
            st.write(seed_data['Short Duration Variety'].values[0])
    else:
        st.error("No variety data found for this selection.")

with tab3:
    st.header(f"🛡️ {selected_crop} Health Protection")
    # Matching with the 'Crop' column in your Disease_Advice CSV
    crop_diseases = df_disease[df_disease['Crop_Name'].str.contains(selected_crop, case=False, na=False)]
    
    if not crop_diseases.empty:
        for _, row in crop_diseases.iterrows():
            with st.expander(f"🔴 Threat: {row['Disease_Name']}"):
                st.markdown(f"**Risk Level:** {row['Risk_Level']}")
                st.markdown(f"**Prevention Strategy:** {row['Prevention_Advice']}")
    else:
        st.success(f"No active disease threats logged for {selected_crop}.")
