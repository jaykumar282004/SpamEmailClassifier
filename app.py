import streamlit as st
import pickle

# Load model
model = pickle.load(open("spam_model.pkl", "rb"))

# Page config
st.set_page_config(
    page_title="AI Spam Detector",
    page_icon="📧",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.title {
    font-size: 45px;
    font-weight: bold;
    text-align: center;
    color: white;
}

.subtitle {
    text-align: center;
    color: #BBBBBB;
    margin-bottom: 30px;
}

.result-box {
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="title">📧 AI Spam Email Detector</p>', unsafe_allow_html=True)

st.markdown(
    '<p class="subtitle">Detect whether an email or message is Spam or Safe using Machine Learning</p>',
    unsafe_allow_html=True
)

# Email Subject
subject = st.text_input("📌 Email Subject")

# Message Body
message = st.text_area("📝 Email Message", height=200)

# Button
if st.button("🚀 Analyze Email"):

    full_message = subject + " " + message

    if full_message.strip() == "":
        st.warning("Please enter email content.")

    else:

        prediction = model.predict([full_message])

        if prediction[0] == 1:

            st.markdown("""
            <div class="result-box" style="background-color:#ff4b4b;color:white;">
            🚨 SPAM EMAIL DETECTED
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="result-box" style="background-color:#28c76f;color:white;">
            ✅ SAFE EMAIL
            </div>
            """, unsafe_allow_html=True)

# Footer
st.write("")
st.write("---")
st.caption("Built using Machine Learning, NLP, Streamlit & Python")