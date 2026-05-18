import streamlit as st

st.title("Chicago Land Use Explorer (1990–2023)")

st.write("""
Welcome to the interactive Chicago Land Use Data Explorer.

Use the navigation menu on the left to switch between:
- Graduated Color Maps 
- Charts  
- Graduated Color Change Analysis Maps 
- Capstone Paper 
         
My name is Lauren Hunt, and I am an urban planning professional. I created this app in Spring 2026 as 
         my capstone project for my Master's of Sustainable Urban Development at DePaul University. 
         The data visualized in this app are the Land Use Inventory Datasets (1990, 2001, 2005, 2010, 2015, 
         2020, 2023) created by the Chicago Metropolitan Agency for Planning (CMAP). I was a GIS intern at 
         CMAP in Summer 2025, and was inspired to explore the data I helped to create further through this 
         project. The goal of this app is to expand data accessibility and better understand how spatial 
         patterns of land use have developed in Chicago over time. You can read more about the app creation methodology 
         and findings in the Capstone Paper section. 
         
         Thank you for taking the time to explore this app!

** **Data Note:** The CMAP datasets have evolved in their Land Use Inventory Methodology over time, and newer 
         data years have more detailed land use categories and parcels (There were just under 19,000 parcels in Chicago for the 1991 
         dataset and approximately 177,000 parcels in the 2023 dataset). This means that some of the observed changes in 
         land use over time may be due to changes in data collection methods rather than actual land use 
         changes on the ground. Please keep this in mind when interpreting the visualizations. CMAP's land use categories have been standardized since 2010, so the most accurate comparisons can be made between 2010, 2015, 2020, and 2023.
""")