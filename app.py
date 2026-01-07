import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from datetime import datetime
import joblib

from auth_utils import generate_otp, send_telegram_otp
from track_utils import (
    add_prediction_details,
    view_all_prediction_details,
    create_emotionclf_table,
    IST
)

pipe_lr = joblib.load(open("./models/emotion_classifier_pipe_lr.pkl", "rb"))

def predict_emotions(text):
    return pipe_lr.predict([text])[0]

def get_prediction_proba(text):
    return pipe_lr.predict_proba([text])

emotions_emoji_dict = {
    "anger": "Angry",
    "disgust": "Disgusting",
    "fear": "Fear",
    "happy": "Happy",
    "joy": "Joy",
    "neutral": "Neutral",
    "sad": "Sad",
    "sadness": "Sadness",
    "shame": "Shame",
    "surprise": "Surprise"
}

def login_page():
    st.title("🔐 Login with OTP")

    if "otp" not in st.session_state:
        st.session_state.otp = None
        st.session_state.authenticated = False
        
    phone = st.text_input("Enter your Phone No.")

    if st.button("📩 Send OTP"):
        if phone:
            otp = generate_otp()
            st.session_state.otp = otp
            send_telegram_otp(otp)
            st.success("OTP sent to Telegram")
        else:
            st.error("Enter Valid  Credintials!!")

    user_otp = st.text_input("Enter OTP", type="password")

    if st.button("✅ Verify OTP"):
        if user_otp == st.session_state.otp:
            st.session_state.authenticated = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid OTP")

def emotion_app():
    st.title("🧠 Emotion Detection System")

    menu = ["Home", "History", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    create_emotionclf_table()

    if choice == "Home":
        st.subheader("Emotion Detection from Text")

        with st.form(key="emotion_form"):
            raw_text = st.text_area("Enter text")
            submit = st.form_submit_button("Analyze")

        if submit:
            col1, col2 = st.columns(2)

            prediction = predict_emotions(raw_text)
            probability = get_prediction_proba(raw_text)

            add_prediction_details(
                raw_text,
                prediction,
                np.max(probability),
                datetime.now(IST)
            )

            with col1:
                st.header("Result")
                st.write(raw_text)
                st.success(f"{prediction} {emotions_emoji_dict[prediction]}")
                st.write(f"Confidence: {np.max(probability):.2f}")

            with col2:
                proba_df = pd.DataFrame(
                    probability,
                    columns=pipe_lr.classes_
                ).T.reset_index()
                proba_df.columns = ["Emotion", "Probability"]

                fig = alt.Chart(proba_df).mark_bar().encode(
                    x="Emotion",
                    y="Probability",
                    color="Emotion"
                )
                st.altair_chart(fig, use_container_width=True)

    elif choice == "History":
        st.subheader("Prediction History")

        df = pd.DataFrame(
            view_all_prediction_details(),
            columns=["Text", "Emotion", "Confidence", "Time"]
        )

        st.dataframe(df)

    elif choice == "Logout":
        st.session_state.authenticated = False
        st.success("Logged out")
        st.rerun()
        
if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        emotion_app()
    else:
        login_page()
