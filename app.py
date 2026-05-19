import streamlit as st
import pickle
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# =====================================
# DATABASE
# =====================================

conn = sqlite3.connect("threat_logs.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_type TEXT,
    result TEXT,
    score REAL,
    timestamp TEXT
)
""")

conn.commit()

# =====================================
# LOAD MODEL
# =====================================

model = pickle.load(open("spam_model.pkl", "rb"))

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Spam Email Classifier",
    page_icon="📧",
    layout="wide"
)

# =====================================
# PREMIUM LIGHT UI
# =====================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* MAIN APP */

.stApp {
    background-color: #f5f7fb;
    color: #111827;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}

/* SIDEBAR TEXT */

section[data-testid="stSidebar"] * {
    color: #111827 !important;
}

/* TITLES */

.main-title {
    font-size: 42px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 5px;
}

.sub-title {
    font-size: 16px;
    color: #6b7280;
    margin-bottom: 30px;
}

/* CARDS */

.card {
    background-color: white;
    border: 1px solid #e5e7eb;
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.card h2 {
    color: #111827;
    font-size: 28px;
    margin-bottom: 5px;
}

.card p {
    color: #6b7280;
    font-size: 14px;
}

/* RESULT BOXES */

.safe-box {
    background-color: #ecfdf5;
    border: 1px solid #10b981;
    padding: 25px;
    border-radius: 12px;
    color: #065f46;
    font-size: 22px;
    font-weight: 600;
}

.spam-box {
    background-color: #fef2f2;
    border: 1px solid #ef4444;
    padding: 25px;
    border-radius: 12px;
    color: #991b1b;
    font-size: 22px;
    font-weight: 600;
}

/* NORMAL BUTTONS */

div.stButton > button {
    background-color: #2563eb;
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-weight: 500;
    font-size: 15px;
    width: 100%;
}

div.stButton > button:hover {
    background-color: #1d4ed8;
}

/* DOWNLOAD BUTTON */

div.stDownloadButton > button {
    background-color: white !important;
    color: black !important;
    border: 1px solid #d1d5db !important;
    border-radius: 10px;
    padding: 12px;
    font-weight: 500;
}

div.stDownloadButton > button:hover {
    background-color: #f3f4f6 !important;
}

/* FILE UPLOADER */

[data-testid="stFileUploader"] {
    background-color: #111827 !important;
    border: 2px dashed #374151 !important;
    padding: 20px !important;
    border-radius: 12px !important;
}

/* ALL TEXT INSIDE */

[data-testid="stFileUploader"] * {
    color: white !important;
}

/* ACTUAL BUTTON */

[data-testid="stFileUploader"] section button,
[data-testid="stFileUploader"] button {
    background: white !important;
    color: black !important;
    border: 1px solid #d1d5db !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 18px !important;
}

/* BUTTON TEXT */

[data-testid="stFileUploader"] button p {
    color: black !important;
}

/* ICON */

[data-testid="stFileUploader"] button svg {
    fill: black !important;
}

/* INPUT LABELS */

label {
    color: #111827 !important;
    font-weight: 500 !important;
}

/* INPUT BOXES */

div[data-testid="stTextInput"] input {
    background-color: white !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
}

div[data-testid="stTextArea"] textarea {
    background-color: white !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
}

/* TABLES */

[data-testid="stDataFrame"] {
    border: 1px solid #e5e7eb;
    border-radius: 10px;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #6b7280;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================

st.sidebar.markdown("## 📧 Spam Email Classifier")
st.sidebar.caption("Enterprise AI Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Single Email Scanner",
        "Bulk Email Scanner",
        "Analytics",
        "Threat Logs",
        "About System"
    ]
)

st.sidebar.markdown("---")

st.sidebar.metric("Model Accuracy", "96.23%")
st.sidebar.metric("Threat Engine", "Active")
st.sidebar.metric("Status", "Live")

# =====================================
# DASHBOARD
# =====================================

if page == "Dashboard":

    st.markdown(
        '<div class="main-title">Spam Email Classifier</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">AI-powered email spam detection system using Machine Learning and NLP</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="card"><h2>96.23%</h2><p>Detection Accuracy</p></div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="card"><h2>24/7</h2><p>Threat Monitoring</p></div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="card"><h2>AI + NLP</h2><p>Detection Engine</p></div>',
            unsafe_allow_html=True
        )

    st.subheader("Recent Threat Activity")

    try:

        recent_logs = pd.read_sql_query(
            "SELECT scan_type, result, score AS Percentage, timestamp FROM logs ORDER BY id DESC LIMIT 5",
            conn
        )

        recent_logs["Percentage"] = recent_logs["Percentage"].astype(str) + "%"

        st.dataframe(
            recent_logs,
            use_container_width=True
        )

    except:
        st.warning("No recent activity found.")

# =====================================
# SINGLE EMAIL SCANNER
# =====================================

elif page == "Single Email Scanner":

    st.title("Single Email Scanner")

    sender = st.text_input("Sender Email")

    subject = st.text_input("Email Subject")

    message = st.text_area(
        "Email Content",
        height=250
    )

    analyze = st.button("Analyze Email")

    if analyze:

        full_message = sender + " " + subject + " " + message

        prediction = model.predict([full_message])[0]

        probabilities = model.predict_proba([full_message])[0]

        spam_probability = round(probabilities[1] * 100, 2)
        safe_probability = round(probabilities[0] * 100, 2)

        result = "Spam" if prediction == 1 else "Safe"

        c.execute(
            "INSERT INTO logs (scan_type, result, score, timestamp) VALUES (?, ?, ?, ?)",
            (
                "Single Email",
                result,
                spam_probability,
                datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            )
        )

        conn.commit()

        if prediction == 1:

            st.markdown(
                f'<div class="spam-box">Spam Email Detected<br><br>Threat Percentage: {spam_probability}%</div>',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f'<div class="safe-box">Safe Email Detected<br><br>Safety Percentage: {safe_probability}%</div>',
                unsafe_allow_html=True
            )

# =====================================
# BULK EMAIL SCANNER
# =====================================

elif page == "Bulk Email Scanner":

    st.title("Bulk Email Scanner")

    st.write(
        "Upload CSV file to analyze multiple emails using AI."
    )

    uploaded_csv = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_csv is not None:

        try:

            df = pd.read_csv(uploaded_csv, encoding="latin-1")

            df.columns = df.columns.str.strip().str.lower()

            st.subheader("Uploaded Data")

            st.dataframe(df.head(), use_container_width=True)

            if "text" in df.columns:
                email_column = "text"

            elif "email" in df.columns:
                email_column = "email"

            elif "message" in df.columns:
                email_column = "message"

            elif "v2" in df.columns:
                email_column = "v2"

            else:
                email_column = df.columns[0]

            st.success(f"Using column: {email_column}")

            analyze_bulk = st.button(
                "Analyze Bulk Emails"
            )

            if analyze_bulk:

                predictions = model.predict(
                    df[email_column].astype(str)
                )

                probabilities = model.predict_proba(
                    df[email_column].astype(str)
                )

                df["Prediction"] = [
                    "Spam" if pred == 1 else "Safe"
                    for pred in predictions
                ]

                df["Threat Percentage"] = [
                    str(round(prob[1] * 100, 2)) + "%"
                    for prob in probabilities
                ]

                st.subheader("Bulk Scan Results")

                st.dataframe(df, use_container_width=True)

                spam_count = len(
                    df[df["Prediction"] == "Spam"]
                )

                safe_count = len(
                    df[df["Prediction"] == "Safe"]
                )

                total = len(df)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Total Emails", total)

                with col2:
                    st.metric("Spam Emails", spam_count)

                with col3:
                    st.metric("Safe Emails", safe_count)

                chart_df = pd.DataFrame({
                    "Category": ["Spam", "Safe"],
                    "Count": [spam_count, safe_count]
                })

                fig = px.pie(
                    chart_df,
                    values="Count",
                    names="Category"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                csv = df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="Download Report",
                    data=csv,
                    file_name="bulk_email_report.csv",
                    mime="text/csv"
                )

                bulk_percentage = round(
                    (spam_count / total) * 100,
                    2
                )

                c.execute(
                    "INSERT INTO logs (scan_type, result, score, timestamp) VALUES (?, ?, ?, ?)",
                    (
                        "Bulk Email",
                        f"{spam_count} Spam / {safe_count} Safe",
                        bulk_percentage,
                        datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    )
                )

                conn.commit()

        except Exception as e:
            st.error(f"Error reading CSV: {e}")

# =====================================
# ANALYTICS
# =====================================

elif page == "Analytics":

    st.title("Security Analytics")

    logs_df = pd.read_sql_query(
        "SELECT * FROM logs",
        conn
    )

    spam_total = 0
    safe_total = 0

    for value in logs_df["result"].astype(str):

        if "Spam" in value:
            spam_total += 1

        if "Safe" in value:
            safe_total += 1

    analytics_data = pd.DataFrame({
        "Category": ["Spam", "Safe"],
        "Count": [spam_total, safe_total]
    })

    fig = px.pie(
        analytics_data,
        values="Count",
        names="Category"
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Spam Detected", spam_total)

    with col2:
        st.metric("Safe Emails", safe_total)

# =====================================
# THREAT LOGS
# =====================================

elif page == "Threat Logs":

    st.title("Threat Logs")

    try:

        logs_df = pd.read_sql_query(
            "SELECT id, scan_type, result, score AS Percentage, timestamp FROM logs ORDER BY id DESC",
            conn
        )

        logs_df["Percentage"] = logs_df["Percentage"].astype(str) + "%"

        st.dataframe(logs_df, use_container_width=True)

    except:
        st.warning("No logs available.")

# =====================================
# ABOUT
# =====================================

elif page == "About System":

    st.title("About Spam Email Classifier")

    st.write("""
    Spam Email Classifier is an AI-powered email security platform developed using Machine Learning and NLP techniques to detect spam and phishing emails.

    The system supports both single email scanning and bulk email analysis through CSV uploads while maintaining threat logs and analytics dashboards.
    """)

    st.subheader("Technologies Used")

    tech_data = pd.DataFrame({
        "Technology": [
            "Python",
            "Streamlit",
            "Scikit-learn",
            "Pandas",
            "Plotly",
            "SQLite"
        ],
        "Purpose": [
            "Core backend programming language",
            "Frontend web application framework",
            "Machine Learning model training",
            "CSV and data processing",
            "Interactive analytics charts",
            "Threat log database management"
        ],
        "Version": [
            "Python 3.13",
            "Latest",
            "Latest",
            "Latest",
            "Latest",
            "SQLite3"
        ]
    })

    st.dataframe(
        tech_data,
        use_container_width=True
    )

# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.markdown(
    '<div class="footer">Spam Email Classifier | Powered by AI & NLP</div>',
    unsafe_allow_html=True
)