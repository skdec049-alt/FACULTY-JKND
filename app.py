import streamlit as st
import pandas as pd
from fpdf import FPDF
from PIL import Image
import io

# --- SESSION STATE INITIALIZATION ---
# This acts as a temporary database for the current session
if 'faculty_data' not in st.session_state:
    st.session_state['faculty_data'] = []

# --- PDF GENERATION ---
def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Faculty Performance Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    
    # Adding data to PDF
    for key, value in data.items():
        if key not in ['Photo', 'Paper_File']: # Don't write raw bytes to PDF text
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, txt="Generated via Faculty Portal System", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- MAIN APP ---
def main():
    st.set_page_config(page_title="Advanced Faculty Portal", layout="wide")
    
    # Sidebar Navigation
    menu = ["Faculty Submission", "Admin Dashboard"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Faculty Submission":
        st.title("📄 Faculty Data Entry")
        
        with st.form("faculty_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                f_name = st.text_input("Faculty Name")
                f_id = st.text_input("Faculty ID")
                subject = st.text_input("Subject Name")
            with col2:
                f_photo = st.file_uploader("Upload Photo", type=['jpg', 'png', 'jpeg'])
                lab_name = st.text_input("Lab Name")
                paper_title = st.text_input("Research Paper Title")
            
            paper_file = st.file_uploader("Upload Research Paper (PDF)", type=['pdf'])
            
            submitted = st.form_submit_button("Submit Details")

        if submitted:
            if f_name and f_id:
                # Create a record
                entry = {
                    "Name": f_name,
                    "ID": f_id,
                    "Subject": subject,
                    "Lab": lab_name,
                    "Paper Title": paper_title,
                    "Photo": f_photo,
                    "Paper_File": paper_file
                }
                
                # Save to session state
                st.session_state['faculty_data'].append(entry)
                st.success(f"Record for {f_name} saved successfully!")
                
                # Individual PDF Download
                pdf_bytes = create_pdf(entry)
                st.download_button(
                    label="📥 Download My Report",
                    data=pdf_bytes,
                    file_name=f"Report_{f_id}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Name and ID are required!")

    elif choice == "Admin Dashboard":
        st.title("🛠️ Admin Control Panel")
        
        if len(st.session_state['faculty_data']) > 0:
            df = pd.DataFrame(st.session_state['faculty_data'])
            
            # Display table without the raw file objects for cleanliness
            st.subheader("Submitted Records")
            st.table(df.drop(columns=['Photo', 'Paper_File']))
            
            # View Individual Details
            selected_faculty = st.selectbox("Select Faculty to View Photo/Paper", df['Name'].tolist())
            
            detail = next(item for item in st.session_state['faculty_data'] if item["Name"] == selected_faculty)
            
            c1, c2 = st.columns(2)
            with c1:
                if detail['Photo'] is not None:
                    st.image(detail['Photo'], caption=f"Photo of {detail['Name']}", width=200)
            with c2:
                if detail['Paper_File'] is not None:
                    st.write(f"📄 Paper: {detail['Paper Title']}")
                    st.download_button("Download Paper", detail['Paper_File'], file_name="paper.pdf")
        else:
            st.info("No records submitted yet.")

if __name__ == "__main__":
    main()
