import streamlit as st
import pickle

# Load trained model
model = pickle.load(open("spam_model.pkl", "rb"))

# Page settings
st.set_page_config(
    page_title="Spam Email Classifier",
    page_icon="📧"
)

# Title
st.title("📧 Spam Email Classifier")

st.write("Enter a message below to check whether it is spam or not.")

# Input box
message = st.text_area("Enter Message")

# Predict button
if st.button("Check Message"):

    if message.strip() == "":
        st.warning("Please enter a message.")

    else:

        prediction = model.predict([message])

        if prediction[0] == 1:
            st.error("🚨 This message is SPAM")

        else:
            st.success("✅ This message is NOT Spam")