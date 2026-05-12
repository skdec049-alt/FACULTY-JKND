import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

# --- Utility Functions ---
def calculate_score(subjects, labs, papers):
    """Simple logic: 10 points per subject, 15 per lab, 50 per paper."""
    score = (len(subjects) * 10) + (len(labs) * 15) + (len(papers) * 50)
    return score

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Faculty Performance Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    
    # Basic Details
    pdf.cell(200, 10, txt=f"Name: {data['name']}", ln=True)
    pdf.cell(200, 10, txt=f"Faculty ID: {data['id']}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Academic Workload:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Subjects: {', '.join(data['subjects'])}", ln=True)
    pdf.cell(200, 10, txt=f"Labs: {', '.join(data['labs'])}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Research & Publications:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Papers Published: {len(data['papers'])}", ln=True)
    for i, paper in enumerate(data['papers'], 1):
        pdf.cell(200, 10, txt=f"  {i}. {paper}", ln=True)
        
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Total Performance Score: {data['score']}", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- Streamlit UI ---
st.set_page_config(page_title="Faculty ERP Portal", layout="wide")

st.title("🎓 Faculty ERP & Performance Tracker")
st.markdown("Enter your professional details to calculate your API score and generate a report.")

with st.form("faculty_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name")
        f_id = st.text_input("Faculty ID")
        photo = st.file_uploader("Upload Profile Photo", type=['jpg', 'png', 'jpeg'])

    with col2:
        subjects = st.multiselect("Subjects Taken", 
                                  ["Machine Learning", "Software Engineering", "DBMS", "Operating Systems", "Python Programming", "Data Structures"])
        labs = st.multiselect("Labs Conducted", 
                              ["Data Science Lab", "C Programming Lab", "Java Lab", "AI Lab"])

    st.divider()
    st.subheader("Research & Publications")
    paper_names = st.text_area("Enter Research Paper Titles (one per line)")
    uploaded_papers = st.file_uploader("Upload Research Papers (PDF)", type=['pdf'], accept_multiple_files=True)
    
    submitted = st.form_submit_button("Submit Details & Calculate Score")

if submitted:
    if not name or not f_id:
        st.error("Please provide Name and Faculty ID.")
    else:
        # Process papers
        paper_list = [p.strip() for p in paper_names.split('\n') if p.strip()]
        
        # Calculate Score
        final_score = calculate_score(subjects, labs, paper_list)
        
        # Prepare Data for PDF
        faculty_data = {
            "name": name,
            "id": f_id,
            "subjects": subjects,
            "labs": labs,
            "papers": paper_list,
            "score": final_score
        }
        
        # Display Results
        st.success("Details Submitted Successfully!")
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Subjects/Labs", f"{len(subjects)} / {len(labs)}")
        kpi2.metric("Papers Published", len(paper_list))
        kpi3.metric("Calculated Score", final_score)
        
        # PDF Generation
        pdf_bytes = generate_pdf(faculty_data)
        st.download_button(
            label="📄 Download Performance Report (PDF)",
            data=pdf_bytes,
            file_name=f"Report_{f_id}.pdf",
            mime="application/pdf"
        )
