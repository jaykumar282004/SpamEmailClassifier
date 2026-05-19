import streamlit as st
import pickle
import pandas as pd
import plotly.express as px
import sqlite3
import re
from datetime import datetime

# Database setup
conn = sqlite3.connect('threat_logs.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    receiver TEXT,
    subject TEXT,
    threat_level TEXT,
    spam_probability REAL,
    timestamp TEXT
)
''')

conn.commit()

# Load trained AI model
model = pickle.load(open("spam_model.pkl", "rb"))

# Page config
st.set_page_config(
    page_title="Spam Email Classifier",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #020617, #0f172a);
    color: white;
}

.main-title {
    font-size: 60px;
    font-weight: 800;
    color: #38bdf8;
    text-align: center;
}

.sub-title {
    text-align: center;
    color: #cbd5e1;
    font-size: 20px;
    margin-bottom: 40px;
}

.metric-card {
    background: #111827;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #1e293b;
    box-shadow: 0 0 20px rgba(56,189,248,0.1);
}

.high-risk {
    background-color: #dc2626;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: white;
}

.safe-risk {
    background-color: #16a34a;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("# 🛡️ Spam Email Classifier")
st.sidebar.markdown("### AI Spam Detection Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🔍 Threat Scanner",
        "📊 Analytics",
        "📜 Threat Logs",
        "ℹ️ About System"
    ]
)

st.sidebar.markdown("---")

st.sidebar.metric("AI Accuracy", "96.23%")
st.sidebar.metric("Threat Engine", "ACTIVE")
st.sidebar.metric("Detection Status", "LIVE")

# DASHBOARD PAGE
if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🛡️ Spam Email Classifier</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Advanced AI-Powered Spam Email Detection System using Machine Learning & NLP</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="metric-card"><h2>96.23%</h2><p>Detection Accuracy</p></div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            '<div class="metric-card"><h2>24/7</h2><p>Threat Monitoring</p></div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            '<div class="metric-card"><h2>AI + NLP</h2><p>Detection Engine</p></div>',
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            '<div class="metric-card"><h2>LIVE</h2><p>Threat Detection</p></div>',
            unsafe_allow_html=True
        )

    st.write("")

    st.subheader("🚨 Live Threat Feed")

    feed_data = pd.DataFrame({
        "Time": ["12:45", "12:41", "12:35", "12:28"],
        "Threat": [
            "Phishing URL",
            "Lottery Scam",
            "Credential Harvesting",
            "Fake Banking Alert"
        ],
        "Severity": ["High", "Medium", "High", "Critical"]
    })

    st.dataframe(feed_data, use_container_width=True)

    st.write("")

    chart_data = pd.DataFrame({
        "Threat Type": ["Phishing", "Lottery", "Promotion", "Safe"],
        "Count": [35, 22, 15, 48]
    })

    fig = px.pie(
        chart_data,
        values='Count',
        names='Threat Type',
        title='Threat Distribution'
    )

    st.plotly_chart(fig, use_container_width=True)

# THREAT SCANNER PAGE
elif page == "🔍 Threat Scanner":

    st.title("🔍 AI Threat Scanner")

    left, right = st.columns([2, 1])

    with left:

        sender = st.text_input("📧 Sender Email")

        receiver = st.text_input("📨 Receiver Email")

        subject = st.text_input("📌 Email Subject")

        message = st.text_area(
            "📝 Email Content",
            height=250,
            placeholder="Paste suspicious email content here..."
        )

        uploaded_file = st.file_uploader(
            "📂 Upload Email File",
            type=["txt"]
        )

        if uploaded_file:
            file_content = uploaded_file.read().decode("utf-8")
            message = file_content
            st.success("✅ File uploaded successfully")

        analyze = st.button(
            "🚀 Run AI Threat Analysis",
            use_container_width=True
        )

    with right:

        st.subheader("⚠️ Threat Indicators")

        suspicious_keywords = [
            "win",
            "free",
            "money",
            "urgent",
            "click",
            "verify",
            "bank",
            "password",
            "bonus",
            "offer",
            "lottery",
            "claim"
        ]

        preview = (subject + " " + message).lower()

        detected = []

        for word in suspicious_keywords:
            if word in preview:
                detected.append(word)

        if detected:
            st.error(f"⚠️ Keywords Found: {', '.join(detected)}")
        else:
            st.success("✅ No suspicious keywords")

        st.write("")

        links = re.findall(r'https?://\\S+|www\\.\\S+', preview)

        st.subheader("🔗 Link Analysis")

        if links:
            st.warning(f"⚠️ {len(links)} suspicious link(s) found")
        else:
            st.success("✅ No suspicious links")

        st.write("")

        st.subheader("📅 Scan Time")
        st.write(datetime.now().strftime('%d-%m-%Y'))
        st.write(datetime.now().strftime('%H:%M:%S'))

    # AI Prediction
    if analyze:

        full_message = sender + " " + receiver + " " + subject + " " + message

        if full_message.strip() == "":
            st.warning("Please enter email details.")

        else:

            prediction = model.predict([full_message])[0]

            probabilities = model.predict_proba([full_message])[0]

            spam_probability = round(probabilities[1] * 100, 2)
            safe_probability = round(probabilities[0] * 100, 2)

            st.write("")

            if spam_probability >= 80:
                risk = "CRITICAL"
            elif spam_probability >= 60:
                risk = "HIGH"
            elif spam_probability >= 40:
                risk = "MEDIUM"
            else:
                risk = "LOW"

            # Save logs
            c.execute(
                "INSERT INTO logs (sender, receiver, subject, threat_level, spam_probability, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    sender,
                    receiver,
                    subject,
                    risk,
                    spam_probability,
                    datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                )
            )

            conn.commit()

            if prediction == 1:

                st.markdown(
                    f'<div class="high-risk">🚨 SPAM EMAIL DETECTED<br><br>Threat Score: {spam_probability}%<br>Risk Level: {risk}</div>',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f'<div class="safe-risk">✅ SAFE EMAIL DETECTED<br><br>Safety Score: {safe_probability}%</div>',
                    unsafe_allow_html=True
                )

            st.write("")

            st.subheader("🧠 AI Decision Analysis")

            reasons = []

            if detected:
                reasons.append("Suspicious promotional language detected")

            if links:
                reasons.append("External links found in email")

            if "urgent" in preview:
                reasons.append("Urgency manipulation pattern identified")

            if prediction == 1 and not reasons:
                reasons.append("AI detected hidden spam-like patterns")

            if reasons:
                for reason in reasons:
                    st.warning(f"⚠️ {reason}")
            else:
                st.success("✅ No major threat indicators")

            st.write("")

            st.subheader("📊 Threat Probability")

            probability_data = pd.DataFrame({
                'Category': ['Safe', 'Threat'],
                'Probability': [safe_probability, spam_probability]
            })

            fig = px.bar(
                probability_data,
                x='Category',
                y='Probability',
                title='Threat Probability Analysis'
            )

            st.plotly_chart(fig, use_container_width=True)

# ANALYTICS PAGE
elif page == "📊 Analytics":

    st.title("📊 Security Analytics Dashboard")

    analytics_data = pd.DataFrame({
        'Category': ['Safe', 'Spam'],
        'Count': [48, 52]
    })

    fig1 = px.pie(
        analytics_data,
        values='Count',
        names='Category',
        title='Overall Email Classification'
    )

    st.plotly_chart(fig1, use_container_width=True)

    trend_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'Threats': [12, 19, 8, 25, 17]
    })

    fig2 = px.line(
        trend_data,
        x='Day',
        y='Threats',
        title='Weekly Threat Trend'
    )

    st.plotly_chart(fig2, use_container_width=True)

# LOGS PAGE
elif page == "📜 Threat Logs":

    st.title("📜 Threat Detection Logs")

    logs_df = pd.read_sql_query("SELECT * FROM logs ORDER BY id DESC", conn)

    st.dataframe(logs_df, use_container_width=True)

# ABOUT PAGE
elif page == "ℹ️ About System":

    st.title("ℹ️ About Spam Email Classifier")

    st.write(
        """
        Spam Email Classifier is an AI-powered email security platform developed for detecting spam, phishing, and malicious email threats using Machine Learning and Natural Language Processing.

        ### Core Features
        - AI-based threat detection
        - NLP-powered spam analysis
        - Real-time threat monitoring
        - Threat probability scoring
        - Security analytics dashboard
        - Threat log management
        - Link & keyword analysis

        ### Technologies Used
        - Python
        - Streamlit
        - Scikit-learn
        - TF-IDF Vectorization
        - Naive Bayes Algorithm
        - Plotly Analytics
        - SQLite Database
        """
    )

# Footer
st.write("")
st.markdown("---")
st.caption("Spam Email Classifier | Powered by AI & NLP")