import streamlit as st
import altair as alt
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import joblib
from track_utils import add_prediction_details, view_all_prediction_details, create_emotionclf_table, IST

# Load Model
pipe_lr = joblib.load(open("./models/emotion_classifier_pipe_lr.pkl", "rb"))

# Function
def predict_emotions(text):
    results = pipe_lr.predict([text])
    return results[0]

def get_prediction_proba(text):
    results = pipe_lr.predict_proba([text])
    return results

emotions_emoji_dict = {"anger": "Angry", "disgust": "Disgusting", "fear": "Fear", "happy": "Happy", "joy": "Joy", "neutral": "Neutral", "sad": "Sad", "sadness": "Sadness", "shame": "Shame", "surprise": "Surprise"}

# Main Application
def main():
    st.title("Text Classification by Emotions")
    menu = ["Home", "History"]
    choice = st.sidebar.selectbox("Menu", menu)
    create_emotionclf_table()
    if choice == "Home":
        st.subheader("Emotion Detection in Text")

        with st.form(key='emotion_clf_form'):
            raw_text = st.text_area("Type Here")
            submit_text = st.form_submit_button(label='Submit')

        if submit_text:
            col1, col2 = st.columns(2)

            prediction = predict_emotions(raw_text)
            probability = get_prediction_proba(raw_text)

            add_prediction_details(raw_text, prediction, np.max(probability), datetime.now(IST))

            with col1:
                st.success("Original Text")
                st.write(raw_text)

                st.header("Prediction")
                emoji_icon = emotions_emoji_dict[prediction]
                st.write("{}:{}".format(prediction, emoji_icon))
                st.write("Confidence:{}".format(np.max(probability)))

            with col2:
                st.header("Prediction Probability")
                proba_df = pd.DataFrame(probability, columns=pipe_lr.classes_)
                proba_df_clean = proba_df.T.reset_index()
                proba_df_clean.columns = ["emotions", "probability"]

                fig = alt.Chart(proba_df_clean).mark_bar().encode(x='emotions', y='probability', color='emotions')
                st.altair_chart(fig, use_container_width=True)

    elif choice == "History":
        st.subheader("History")
      
        with st.expander('Emotion Classifier Metrics'):
            df_emotions = pd.DataFrame(view_all_prediction_details(), columns=['Rawtext', 'Prediction', 'Probability', 'Time_of_Visit'])
            st.dataframe(df_emotions)
            prediction_count = df_emotions['Prediction'].value_counts().rename_axis('Prediction').reset_index(name='Counts')
            pc = alt.Chart(prediction_count).mark_bar().encode(x='Prediction', y='Counts', color='Prediction')
            st.altair_chart(pc, use_container_width=True)



if __name__ == '__main__':
    main()
