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
                    label="Yield Efficiency (Tons/Hectare)",
                    value=f"{round(prediction_per_ha, 2)} Tons/Hectare",
                    help="This is the estimated production for every 1 hectare of land."
                )
        
            with col_b:
                st.metric(
                    label="Total Estimated Harvest (Tons)", 
                    value=f"{round(total_harvest, 2)} Tons",
                    help=f"Total production for your specific area of {land_area} hectares."
                )
            st.success(f"Analysis complete for {selected_crop} in {selected_district}!")

        except Exception as e:
            st.error(f"Prediction Error: {e}")


with tab2:
    st.header("🌱 Triple-Variety Seed Matchmaker")
    
    try:
        df_seeds = pd.read_csv('seeds.csv')
        
        # 1. DEBUG: Show actual columns if mapping fails
        actual_cols = df_seeds.columns.tolist()
        
        # 2. Hardcoded selection for speed
        # If your CSV columns are 'District' and 'Crop', this works.
        # If they are different, change the strings below to match actual_cols.
        try:
            target_dist_col = 'District'
            target_crop_col = 'Crop'
            
            filtered_seeds = df_seeds[
                (df_seeds[target_dist_col].str.strip().str.upper() == selected_district.upper()) & 
                (df_seeds[target_crop_col].str.strip().str.capitalize() == selected_crop.capitalize())
            ]
            
            if not filtered_seeds.empty:
                st.success(f"Recommended Varieties for {selected_district}")
                # DISPLAY LOGIC
                for _, row in filtered_seeds.iterrows():
                    st.write(f"**{row['Category']}**: {row['Seed_Name']}")
                    st.caption(row['Justification'])
            else:
                st.warning(f"No match in CSV. Found columns: {actual_cols}")

        except KeyError:
            st.error(f"Header Mismatch! Your CSV headers are: {actual_cols}")
            st.info("Rename your CSV columns to 'District' and 'Crop' exactly.")
            
    except Exception as e:
        st.error(f"Critical Error: {e}")
    

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
