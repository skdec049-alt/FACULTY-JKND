import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Define the Excel file name
DB_FILE = "faculty_database.xlsx"

def save_to_excel(new_data_dict):
    """Saves data to Excel and ensures it persists after refresh."""
    # Convert the dictionary to a DataFrame
    new_df = pd.DataFrame([new_data_dict])
    
    if os.path.exists(DB_FILE):
        # Load existing data and append
        existing_df = pd.read_excel(DB_FILE)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_excel(DB_FILE, index=False)
    else:
        # Create new file with headers
        new_df.to_excel(DB_FILE, index=False)

# --- Streamlit UI ---
st.title("Faculty ERP (Permanent Excel Storage)")

with st.form("faculty_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        f_id = st.text_input("Faculty ID")
    with col2:
        subjects = st.multiselect("Subjects", ["AI", "ML", "Python", "Data Science"])
        labs = st.multiselect("Labs", ["Lab A", "Lab B"])
    
    papers = st.text_area("Research Papers (One per line)")
    
    submitted = st.form_submit_button("Submit & Save Permanently")

if submitted:
    if name and f_id:
        # 1. Logic: Calculate Score
        paper_list = [p.strip() for p in papers.split('\n') if p.strip()]
        score = (len(subjects) * 10) + (len(labs) * 15) + (len(paper_list) * 50)
        
        # 2. Prepare Data Object
        data_to_save = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Faculty_ID": f_id,
            "Subjects": ", ".join(subjects),
            "Labs": ", ".join(labs),
            "Paper_Count": len(paper_list),
            "Total_Score": score
        }
        
        # 3. Save to Excel
        save_to_excel(data_to_save)
        st.success(f"Data for {name} saved to {DB_FILE}!")
    else:
        st.error("Name and ID are required.")

# --- View Stored Data ---
st.divider()
st.subheader("Stored Faculty Records")
if os.path.exists(DB_FILE):
    df_display = pd.read_excel(DB_FILE)
    st.dataframe(df_display)
    
    # Allow user to download the whole database
    with open(DB_FILE, "rb") as f:
        st.download_button("Download Full Excel Database", f, file_name=DB_FILE)
else:
    st.info("No records found yet. Submit the form to create the database.")
