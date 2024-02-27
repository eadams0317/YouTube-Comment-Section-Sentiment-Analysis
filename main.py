import streamlit as st
import getComments
import getSentiment
import json
import time

# Set page title and favicon
st.set_page_config(page_title="Streamlit Homepage", page_icon=":rocket:")

# Centered title
st.title("YouTube Comment Sentiment Analysis")
st.markdown("---")  # Horizontal line for separation

# Textbox for user input
user_input = st.text_input("Enter a YouTube Video URL:")
commentCount = st.number_input(label="Max Number of Comments (Calculations are CPU Heavy. Recommend 100-200 for reasonable load time.)", value = 100)

# Submit button
if st.button("Get Comment Analysis"):

    #Verify its a YouTube Video URL
    if user_input.startswith("https://www.youtube.com/watch?v="):

        #Show thumbnail
        st.video(user_input)

        with st.spinner("Loading..."):
            #Derive ID
            vidID = user_input.split("v=")[1]

            #Make API Call
            getComments.execute(vidID, commentCount)

            # Open the JSON file and load the data
            with open("data.json", "r") as file:
                json_data = json.load(file)

            # Iterate through the JSON data
            sentimentArray = []
            for item in json_data:
                sentimentArray.append(getSentiment.getSentiment(item["comment"]))

            #Calculate Averages
            positives = 0
            total = 0
            for each in sentimentArray:
                total += 1
                if each == "POSITIVE":
                    positives += 1
            average = round(number=(positives/total), ndigits=2)
            invAverage = round(number=(1 - average), ndigits=2)

        #Present metrics
        st.success(f"Your video has been successfully analysed")
        st.text("")
        st.text(f"Total Comments Analyzed: {total}")
        st.markdown(f"<p style='color:green;'>Positive: {average}%</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:red;'>Negative: {invAverage}%</p>", unsafe_allow_html=True)


    else:
        st.error('Please enter a valid YouTube Video URL', icon="🚨")


