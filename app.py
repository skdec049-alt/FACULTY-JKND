import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

# --- CALCULATOR LOGIC ---
def calculate_score(classes, labs, papers):
    # Custom scoring logic (Example)
    # 5 points per class, 3 per lab, 10 per research paper
    return (classes * 5) + (labs * 3) + (papers * 10)

# --- PDF GENERATION ---
def create_pdf(name, dept, classes, labs, papers, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Faculty Performance Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Faculty Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Department: {dept}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Classes Taken: {classes}", ln=True)
    pdf.cell(200, 10, txt=f"Labs Conducted: {labs}", ln=True)
    pdf.cell(200, 10, txt=f"Research Papers Published: {papers}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"Total Calculated Score: {score}", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- STREAMLIT UI ---
def main():
    st.set_page_config(page_title="Faculty Portal", layout="centered")
    
    st.title("🎓 Faculty Performance Portal")
    st.markdown("Enter your academic details below to calculate your API score and generate a report.")

    with st.form("faculty_form"):
        st.header("Personal Details")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
        with col2:
            dept = st.selectbox("Department", ["Computer Science", "Mechanical", "Electrical", "Civil", "Physics"])

        st.header("Academic Workload")
        c1, c2, c3 = st.columns(3)
        with c1:
            classes = st.number_input("Classes Taken", min_value=0, step=1)
        with c2:
            labs = st.number_input("Labs Taken", min_value=0, step=1)
        with c3:
            papers = st.number_input("Research Papers", min_value=0, step=1)

        submitted = st.form_submit_button("Calculate Score & Preview")

    if submitted:
        if name:
            score = calculate_score(classes, labs, papers)
            
            # Display Results
            st.success(f"Form Submitted Successfully for {name}!")
            
            st.metric(label="Total Performance Score", value=score)
            
            # Generate PDF
            pdf_bytes = create_pdf(name, dept, classes, labs, papers, score)
            
            st.download_button(
                label="📥 Download Report (PDF)",
                data=pdf_bytes,
                file_name=f"Report_{name.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Please enter your name before submitting.")

if __name__ == "__main__":
    main()
