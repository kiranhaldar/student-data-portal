# student-data-portal
all about a student
# 🏛️ Central Candidate Enrollment & Academic Archive Portal

An enterprise-grade, dynamic academic record archiving portal built with **Streamlit**, designed to streamline student registration, identity verification, and multi-tier educational documentation.

The portal automatically adapts its user interface based on the applicant's selected educational qualification—dynamically adjusting form fields from primary levels up through Post-Doctoral tiers.

---

##  Key Features

* **Dynamic Multi-Tier Form Logic:** Form fields conditionally render according to the applicant's qualification (e.g., selecting below 10th standard omits Secondary, Higher Secondary, and University sections).
* **Statutory Identification Registry:** Collects statutory details including PAN, Voter EPIC, Bank Details, and civil records.
* **Document Vault:** Automatically archives submitted PDF/Image documents into the dedicated `data_photo.file` directory with sanitized user prefixing.
* **Excel Data Persistence:** Consolidates all applicant metadata into an Excel master ledger (`student_master_records.xlsx`) powered by `pandas` and `openpyxl`.
* **Automated SMTP Telemetry:** Instantly dispatches application summaries to the designated administrator email address via secure Gmail SMTP.

---

## Repository Structure

```text
├── app.py                          # Primary Streamlit application
├── requirements.txt                # Production Python dependencies
├── student_master_records.xlsx     # Generated master records ledger
├── data_photo.file/                # File directory for uploaded payloads
├── LICENSE                         # MIT License file
└── README.md                       # Documentation & setup guide
