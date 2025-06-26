import streamlit as st
from PIL import Image
import io
from modules import ai_bot, schemes_mara
from modules.crop_disease_detector import predict_crop_disease
import pandas as pd
from style import load_style
from modules.news_fetcher import scrapper 

# Load custom styles
load_style()

# --------------------------------------------------------------------
# Setup language preference using Streamlit session state
if "language" not in st.session_state:
    st.session_state.language = "en"  # default to English

# Add a language toggle button in the sidebar.
# The button text changes based on the current language.
if st.sidebar.button("Switch to Marathi" if st.session_state.language == "en" else "Switch to English"):
    st.session_state.language = "mr" if st.session_state.language == "en" else "en"

# --------------------------------------------------------------------
# Define text strings based on the selected language
if st.session_state.language == "mr":
    # Sidebar & Navigation
    sidebar_title = "नेव्हिगेशन"
    go_to_label = "वर जा"
    ai_chatbot_text = "एआय चॅटबोट"
    crop_detection_text = "पिकांचे रोग शोधा"
    govt_schemes_text = "सरकारी योजना"
    agri_news_text = "कृषी बातम्या"
    
    # AI Chatbot Section
    ai_chatbot_page_title = "कृषी सहाय्यक चॅटबोट"
    ai_chatbot_description = ("पिके, माती आणि रोग यांच्याबद्दल प्रश्न विचारा. "
                              "तुम्ही पर्यायीपणे पिकांच्या रोगांसाठी चित्र अपलोड करू शकता.")
    
    # Crop Disease Detection Section
    crop_detection_title = "🌿 पिकांचे रोग शोधा"
    crop_detection_description = "तुमच्या पिकाचे चित्र अपलोड करा, रोग ओळखा आणि उपचार शिफारसी मिळवा."
    crop_upload_text = "📤 पिकाचे चित्र अपलोड करा"
    detect_button_text = "🔍 रोग शोधा"
    analyzing_text = "चित्राचा अभ्यास केला जात आहे... कृपया थांबा."
    prediction_results_text = "🩺 भविष्यवाणी निकाल"
    disease_label = "**रोग:**"
    confidence_label = "**विश्वास:**"
    treatment_recommendation_text = "### 💊 उपचार शिफारस"
    marathi_translation_label = "**मराठी अनुवाद:**"
    
    # Government Schemes Section
    govt_schemes_page_title = "सरकारी योजना सहाय्यक चॅटबोट"
    govt_schemes_description = "सरकारी योजना यांचा पुरेपूर लाभ घेण्यासाठी प्रश्न विचारा."
    
    # Agricultural News Section
    agri_news_subtitle = "ताज्या कृषी बातम्या"
    fetch_latest_text = "ताज्या बातम्या आणा"
    success_news_text = "ताज्या बातम्या यशस्वीपणे आणल्या!"
else:
    # Sidebar & Navigation
    sidebar_title = "Navigation"
    go_to_label = "Go to"
    ai_chatbot_text = "AI Chatbot"
    crop_detection_text = "Crop Disease Detection"
    govt_schemes_text = "Government Schemes"
    agri_news_text = "Agricultural News"
    
    # AI Chatbot Section
    ai_chatbot_page_title = "Agricultural Assistant Chatbot"
    ai_chatbot_description = ("Ask questions about crops, soil, and diseases. "
                              "You can also optionally upload an image for crop disease queries.")
    
    # Crop Disease Detection Section
    crop_detection_title = "🌿 Crop Disease Detection"
    crop_detection_description = "Upload an image of your crop to detect diseases and get treatment recommendations."
    crop_upload_text = "📤 Upload Crop Image"
    detect_button_text = "🔍 Detect Disease"
    analyzing_text = "Analyzing the image... Please wait."
    prediction_results_text = "🩺 Prediction Results"
    disease_label = "**Disease:**"
    confidence_label = "**Confidence:**"
    treatment_recommendation_text = "### 💊 Treatment Recommendation"
    marathi_translation_label = "**Marathi Translation:**"  # shown even in English mode if needed
     
    # Government Schemes Section
    govt_schemes_page_title = "Government Schemes Assistant Chatbot"
    govt_schemes_description = "Ask questions to get most out of the Government Schemes"
    
    # Agricultural News Section
    agri_news_subtitle = "Latest Agricultural News"
    fetch_latest_text = "Fetch Latest"
    success_news_text = "Latest news fetched successfully!"

# --------------------------------------------------------------------
# --- Sidebar Navigation ---
st.sidebar.title(sidebar_title)
section = st.sidebar.radio(go_to_label, 
                           [ai_chatbot_text, crop_detection_text, govt_schemes_text, agri_news_text])

# --------------------------------------------------------------------
# --- 1. AI Chatbot Section ---
if section == ai_chatbot_text:
    st.markdown(f"<h1 class='main-title'>{ai_chatbot_page_title}</h1>", unsafe_allow_html=True)
    st.markdown(ai_chatbot_description)
    # Pass the language variable to the chatbot UI function.
    ai_bot.chatbot_ui(language=st.session_state.language)

# --------------------------------------------------------------------
# --- 2. Crop Disease Detection Section ---
elif section == crop_detection_text:
    st.markdown(f"<h1 class='main-title'>{crop_detection_title}</h1>", unsafe_allow_html=True)
    st.markdown(crop_detection_description)
    uploaded_image = st.file_uploader(crop_upload_text, type=["jpg", "jpeg", "png"], key="crop_upload")
    
    if uploaded_image:
        image = Image.open(uploaded_image)
        caption_text = "Uploaded Crop Image" if st.session_state.language == "en" else "अपलोड केलेले पिकाचे चित्र"
        st.image(image, caption=caption_text, width=300)
        if st.button(detect_button_text):
            with st.spinner(analyzing_text):
                try:
                    results = predict_crop_disease(image)
                    st.subheader(prediction_results_text)
                    st.write(f"{disease_label} {results['disease']}")
                    st.write(f"{confidence_label} {results['confidence'] * 100:.1f}%")
                    if "remedy" in results:
                        st.markdown(treatment_recommendation_text)
                        st.write(results["remedy"])
                        st.write(marathi_translation_label)
                        st.write(results["remedy_translation"])
                    else:
                        healthy_text = ("The plant appears to be healthy. No treatment necessary." 
                                        if st.session_state.language == "en" 
                                        else "पिकं निरोगी दिसत आहेत. कोणताही उपचार आवश्यक नाही.")
                        st.write(healthy_text)
                    if results.get("alternatives"):
                        alternatives_label = ("**Alternative Possibilities:**" 
                                              if st.session_state.language == "en" 
                                              else "**पर्यायी शक्यता:**")
                        st.markdown(alternatives_label)
                        for alt in results["alternatives"]:
                            st.write(f"- {alt['disease']} (Confidence: {alt['confidence'] * 100:.1f}%)")
                except Exception as e:
                    st.error(f"🚨 An error occurred while processing the image: {e}")

# --------------------------------------------------------------------
# --- 3. Government Schemes Section ---
elif section == govt_schemes_text:
    st.markdown(f"<h1 class='main-title'>{govt_schemes_page_title}</h1>", unsafe_allow_html=True)
    st.markdown(govt_schemes_description)
    # Pass the language variable to the chatbot UI function.
    schemes_mara.chatbot_ui(language=st.session_state.language)

# --------------------------------------------------------------------
# --- 4. Agricultural News Section ---
elif section == agri_news_text:
    # Function to load the CSV file
    def load_news_data(file_path):
        return pd.read_csv(file_path)

    # Function to display news in card format
    def display_news(news_df):
        for _, row in news_df.iterrows():
            with st.container():
                st.markdown(
                    f"""
                    <div style="border:1px solid #ddd; padding:10px; border-radius:10px; margin-bottom:10px; background-color:#f9f9f9;">
                        <h4 style="color:#2E7D32;">{row['Title']}</h4>
                        <p>{row['Desc']}</p>
                        <a href="{row['Link']}" target="_blank" style="color:#1E88E5; text-decoration:none;">Read more</a>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    news_data = load_news_data("assets/agriculture_news.csv")
    st.subheader(agri_news_subtitle)
    display_news(news_data)

    if st.button(fetch_latest_text):
        scrapper()
        st.success(success_news_text)

# --------------------------------------------------------------------
# Optionally add a footer (if your footer function is defined accordingly)
# footer()
