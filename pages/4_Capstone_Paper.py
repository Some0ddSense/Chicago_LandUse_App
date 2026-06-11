import streamlit as st

# Use Google Docs Viewer to display PDF inline
raw_pdf_url = "https://raw.githubusercontent.com/some0ddsense/Chicago_LandUse_App/main/docs/Chicago_Land_Use_Explorer.pdf"
viewer_url = f"https://docs.google.com/viewer?url={raw_pdf_url}&embedded=true"

st.markdown(f"""
<iframe src="{viewer_url}" width="100%" height="900px"></iframe>
""", unsafe_allow_html=True)


