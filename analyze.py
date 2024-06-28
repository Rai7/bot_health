import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()

AZURE_VISION_KEY = os.getenv('AZURE_VISION_KEY')
AZURE_VISION_ENDPOINT = os.getenv('AZURE_VISION_ENDPOINT')

def analyze():
    st.title("Analyze Image")
    st.markdown("Enter the URL of the image you want to analyze.")

    image_url = st.text_input("Image URL")
    if st.button("Analyze"):
        if image_url:
            result_div = st.empty()
            display_image = st.empty()
            result_div.write("Analyzing...")
            try:
                # Display the image
                display_image.image(image_url, use_column_width=True)

                response = requests.post(
                    f"{AZURE_VISION_ENDPOINT}/vision/v3.2/analyze?visualFeatures=Description",
                    headers={
                        'Ocp-Apim-Subscription-Key': AZURE_VISION_KEY,
                        'Content-Type': 'application/json'
                    },
                    json={"url": image_url}
                )

                response.raise_for_status()

                data = response.json()
                caption = data['description']['captions'][0]
                if caption:
                    result_div.write(f"Caption: '{caption['text']}', Confidence: {caption['confidence']:.4f}")
                else:
                    result_div.write("No caption found.")
            except requests.exceptions.RequestException as e:
                result_div.write(f"Error: {e}")
