import streamlit as st
import pickle
import pandas as pd
import re
from datetime import datetime

# Load trained model
model = pickle.load(open("spam_model.pkl", "rb"))

# Page config
st.set_page_config(
    page_title="AI Email Threat Detection System",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #0f172a, #111827);
    color: white;
}

.main-title {
    font-size: 52px;
    font-weight: bold;
    text-align: center;
    color: white;
    margin-bottom: 10px;
}

.sub-title {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 40px;
    font-size: 18px;
}

.metric-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
}

.safe-box {
    background-color: #16a34a;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: bold;
}

.spam-box {
    background-color: #dc2626;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: bold;
}

.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🛡️ AI Threat Dashboard")

st.sidebar.markdown("---")

st.sidebar.info(
    "Advanced AI-based email spam and threat detection system using NLP and Machine Learning."
)

st.sidebar.markdown("### 🚀 Technologies")
st.sidebar.write("✅ Python")
st.sidebar.write("✅ Machine Learning")
st.sidebar.write("✅ NLP")
st.sidebar.write("✅ Streamlit")
st.sidebar.write("✅ Scikit-learn")
st.sidebar.write("✅ TF-IDF Vectorization")
st.sidebar.write("✅ Naive Bayes Classifier")

st.sidebar.markdown("---")

st.sidebar.metric("Model Accuracy", "96.23%")
st.sidebar.metric("Threat Detection", "Active")
st.sidebar.metric("Live Analysis", "Enabled")

# Main header
st.markdown(
    '<div class="main-title">🛡️ AI Email Threat Detection System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Advanced Email Spam Analysis using Artificial Intelligence & Natural Language Processing</div>',
    unsafe_allow_html=True
)

# Top metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="metric-card"><h2>96.23%</h2><p>Prediction Accuracy</p></div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="metric-card"><h2>AI + NLP</h2><p>Detection Engine</p></div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<div class="metric-card"><h2>Real-Time</h2><p>Threat Monitoring</p></div>',
        unsafe_allow_html=True
    )

st.write("")

# Input section
left, right = st.columns([2, 1])

with left:

    sender = st.text_input("📧 Sender Email")

    receiver = st.text_input("📨 Receiver Email")

    subject = st.text_input("📌 Email Subject")

    message = st.text_area(
        "📝 Email Content",
        height=250,
        placeholder="Paste complete email content here..."
    )

    uploaded_file = st.file_uploader(
        "📂 Upload Email File (.txt)",
        type=["txt"]
    )

    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        message = file_content
        st.success("✅ File uploaded successfully")

    analyze_button = st.button(
        "🚀 Analyze Email",
        use_container_width=True
    )

with right:

    st.subheader("⚠️ Threat Indicators")

    suspicious_keywords = [
        "win",
        "urgent",
        "free",
        "money",
        "offer",
        "prize",
        "lottery",
        "claim",
        "click",
        "verify",
        "bank",
        "password",
        "gift",
        "bonus"
    ]

    detected_keywords = []

    preview_text = (subject + " " + message).lower()

    for word in suspicious_keywords:
        if word in preview_text:
            detected_keywords.append(word)

    if detected_keywords:
        st.error(f"⚠️ Suspicious Keywords Found: {', '.join(detected_keywords)}")
    else:
        st.success("✅ No suspicious keywords detected")

    st.write("")

    st.subheader("🔗 Link Detection")

    links = re.findall(r'https?://\S+|www\.\S+', preview_text)

    if links:
        st.warning(f"⚠️ {len(links)} suspicious link(s) detected")
    else:
        st.success("✅ No suspicious links found")

    st.write("")

    st.subheader("📅 Scan Information")

    st.write(f"Date: {datetime.now().strftime('%d-%m-%Y')}")
    st.write(f"Time: {datetime.now().strftime('%H:%M:%S')}")

# Prediction
if analyze_button:

    full_message = sender + " " + receiver + " " + subject + " " + message

    if full_message.strip() == "":
        st.warning("Please enter email details.")

    else:

        prediction = model.predict([full_message])[0]

        probabilities = model.predict_proba([full_message])[0]

        spam_probability = round(probabilities[1] * 100, 2)
        safe_probability = round(probabilities[0] * 100, 2)

        st.write("")

        # Result box
        if prediction == 1:

            st.markdown(
                f'<div class="spam-box">🚨 SPAM EMAIL DETECTED<br><br>Threat Probability: {spam_probability}%</div>',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f'<div class="safe-box">✅ SAFE EMAIL DETECTED<br><br>Safety Probability: {safe_probability}%</div>',
                unsafe_allow_html=True
            )

        st.write("")

        # AI explanation
        st.subheader("🧠 AI Threat Analysis")

        reasons = []

        if detected_keywords:
            reasons.append("Contains suspicious promotional keywords")

        if links:
            reasons.append("Contains external links")

        if "urgent" in preview_text:
            reasons.append("Contains urgency-based language")

        if prediction == 1 and len(reasons) == 0:
            reasons.append("AI model identified spam-like email patterns")

        if reasons:
            for reason in reasons:
                st.warning(f"⚠️ {reason}")
        else:
            st.success("✅ No major threat indicators detected")

        # Chart section
        st.write("")
        st.subheader("📊 Probability Analysis")

        chart_data = pd.DataFrame({
            'Category': ['Safe', 'Spam'],
            'Probability': [safe_probability, spam_probability]
        })

        st.bar_chart(chart_data.set_index('Category'))

        # Email stats
        st.write("")
        st.subheader("📈 Email Statistics")

        stat1, stat2, stat3 = st.columns(3)

        with stat1:
            st.metric("Characters", len(full_message))

        with stat2:
            st.metric("Words", len(full_message.split()))

        with stat3:
            st.metric("Threat Keywords", len(detected_keywords))

# Example emails
st.write("")
st.markdown("---")

example1, example2 = st.columns(2)

with example1:
    st.subheader("🚨 Spam Email Example")

    st.code(
        "Congratulations! You won ₹50,000. Click the link below to claim your reward immediately.",
        language="text"
    )

with example2:
    st.subheader("✅ Safe Email Example")

    st.code(
        "Hello team, the project review meeting is scheduled tomorrow at 10 AM.",
        language="text"
    )

# Footer
st.markdown("---")

st.markdown(
    '<div class="footer">Built using Python, Machine Learning, NLP, Streamlit & Scikit-learn</div>',
    unsafe_allow_html=True
)

